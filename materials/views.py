import base64
import hashlib
import hmac
import html
import ecdsa
import re
import requests
import json
import logging
import datetime
import random
from functools import wraps
from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse, JsonResponse, Http404
from django.templatetags.static import static
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.utils.http import url_has_allowed_host_and_scheme
from django.db.models import Case, Count, F, Prefetch, Q, When
from django.conf import settings
from django.core.cache import cache

from users.forms import UserProfileForm
from users.views import terms_required
from . import homework, practice
from .forms import StudentReportForm
from .games import record_game_answer, short_answer_matches

# ОНОВЛЕНІ ІМПОРТИ: Видалено Category та DiagnosticTopic, додано CurriculumTopic
from .models import (
    StudyMaterial, Cart, CartItem, DiagnosticOffer, Order, OrderItem, Question,
    Homework, PracticeAttempt, PracticeRun, TutorStudentRequest, Review, StudentPresentation,
    QuestionError, StudentReport, CurriculumSubject, CurriculumGrade, CurriculumTopic, DEFAULT_MATERIAL_DESCRIPTION,
    NMT_SUBJECT_NAME,
)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import StudyMaterialSerializer, PurchasedMaterialSerializer
from django.utils import timezone

User = get_user_model()
logger = logging.getLogger(__name__)


def is_teacher(user):
    return user.is_authenticated and (user.is_superuser or user.is_staff)


MAX_DB_INT = 2 ** 63 - 1


def to_int(value):
    try:
        number = int(value)
    except (TypeError, ValueError):
        return None
    return number if -MAX_DB_INT <= number <= MAX_DB_INT else None


def post_required(redirect_to):
    def decorator(view):
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            if request.method != 'POST':
                return redirect(redirect_to(**kwargs) if callable(redirect_to) else redirect_to)
            return view(request, *args, **kwargs)

        return wrapper

    return decorator


def material_page(material_id, **kwargs):
    return reverse('material_detail', args=[material_id])


def parse_id_list(ids_str):
    return [i for i in (to_int(x) for x in (ids_str or '').split(',')) if i is not None]


def questions_in_order(q_id_list):
    if not q_id_list:
        return []
    preserved_order = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(q_id_list)])
    return (Question.objects.filter(id__in=q_id_list).select_related('curriculum_topic')
            .prefetch_related('options', 'match_items__correct_option').order_by(preserved_order))


# ОНОВЛЕНО: Тепер використовуємо curriculum_topic_id
def is_own_question(question, material, material_num=None):
    if question.curriculum_topic_id and material.curriculum_topic_id:
        return question.curriculum_topic_id == material.curriculum_topic_id
    return False


def seen_question_ids(user):
    seen = set()
    for answers in PracticeAttempt.objects.filter(user=user).values_list('answers_json', flat=True):
        if isinstance(answers, dict):
            seen.update(parse_id_list(str(answers.get('question_ids') or '')))
    return seen


def sample_unseen_first(pool, count, seen_ids):
    unseen = [q for q in pool if q.id not in seen_ids]
    picked = random.sample(unseen, min(count, len(unseen)))
    if len(picked) < count:
        seen = [q for q in pool if q.id in seen_ids]
        picked += random.sample(seen, min(count - len(picked), len(seen)))
    return picked


def find_option(question, option_id):
    option_id = to_int(option_id)
    if option_id is None:
        return None
    return next((opt for opt in question.options.all() if opt.id == option_id), None)


DIAGNOSTIC_MATERIAL_TITLE = "Вхідне діагностичне тестування НМТ"


def user_owns_material(user, material):
    if not user.is_authenticated:
        return False
    if user.purchased_materials.filter(id=material.id).exists():
        return True
    if material.is_bundle:
        included_ids = list(material.included_materials.values_list('id', flat=True))
        return bool(included_ids) and \
            user.purchased_materials.filter(id__in=included_ids).count() == len(included_ids)
    return False


def rate_limit_exceeded(key, limit, window):
    key = f'rate-limit:{key}'
    cache.add(key, 0, window)
    try:
        count = cache.incr(key)
    except ValueError:
        cache.set(key, 1, window)
        count = 1
    return count > limit


def safe_back_url(request, fallback='cabinet'):
    referer = request.META.get('HTTP_REFERER', '')
    if referer and url_has_allowed_host_and_scheme(referer, allowed_hosts={request.get_host()},
                                                   require_https=request.is_secure()):
        return referer
    return fallback


# ==========================================
# ОНОВЛЕНИЙ ГЕНЕРАТОР ДІАГНОСТИКИ
# ==========================================
def diagnostic_stats(saved_answers):
    """Бали й статистика за темами зі збережених відповідей діагностики — і щойно надісланої, і старої з бази."""
    topics_stats = {}
    total_score = max_score = 0
    for question in questions_in_order(parse_id_list(saved_answers.get('question_ids', ''))):
        topic = question.curriculum_topic
        stat = topics_stats.setdefault(topic.id if topic else 0, {'topic': topic, 'correct': 0, 'total': 0})
        key = str(question.id)

        if question.question_type == 'CHOICE':
            points, earned = 1, 0
            selected_option = find_option(question, saved_answers.get('q_choice', {}).get(key))
            if selected_option and selected_option.is_correct:
                earned = 1
        elif question.question_type == 'MATCH':
            points = 3
            answers = saved_answers.get('q_match', {}).get(key, {})
            earned = sum(to_int(answers.get(str(item.id))) == item.correct_option_id
                         for item in question.match_items.all())
        else:
            points = 2
            earned = 2 if short_answer_matches(saved_answers.get('q_short', {}).get(key),
                                               question.correct_short_answer) else 0

        stat['total'] += points
        stat['correct'] += earned
        max_score += points
        total_score += earned
    return total_score, max_score, topics_stats


def weak_topic_stats(topics_stats):
    """Теми, де менше 50%: найслабші першими, за рівного результату — у порядку курсу."""
    weak = [s for s in topics_stats.values() if s['topic'] and s['total'] > 0 and s['correct'] / s['total'] < 0.5]
    return sorted(weak, key=lambda s: (s['correct'] / s['total'], s['topic'].order))


def diagnostic_summary(topics_stats):
    """Слабкі теми (менше 50%), матеріали для них і статистика за темами в порядку курсу."""
    weak_topics = sorted((s['topic'] for s in weak_topic_stats(topics_stats)), key=lambda t: t.order)
    recommendations = []
    if weak_topics:
        recommendations = sorted(
            StudyMaterial.objects.filter(curriculum_topic__in=weak_topics, is_published=True)
            .select_related('curriculum_topic').distinct(),
            key=lambda m: m.curriculum_topic.order if m.curriculum_topic else 999)
    sorted_stats = sorted([s for s in topics_stats.values() if s['topic']], key=lambda s: s['topic'].order)
    return weak_topics, recommendations, sorted_stats


def user_diagnostics(user):
    return (PracticeAttempt.objects.filter(user=user, material__title=DIAGNOSTIC_MATERIAL_TITLE)
            .defer('material__html_content').order_by('-created_at'))


def diagnostic_test_view(request):
    if request.method == 'POST':
        question_ids_str = request.POST.get('question_ids', '')
        saved_answers = {
            'q_choice': {}, 'q_match': {}, 'q_short': {},
            'question_ids': question_ids_str, 'note': 'Вхідна діагностика НМТ'
        }
        scope = request.POST.get('scope', 'all')
        if scope != 'all':
            scope = ','.join(map(str, sorted(set(parse_id_list(scope))))) or 'all'
        saved_answers['scope'] = scope
        questions = list(questions_in_order(parse_id_list(question_ids_str)))
        for question in questions:
            key = str(question.id)
            if question.question_type == 'MATCH':
                saved_answers['q_match'][key] = {str(item.id): request.POST.get(f'match_{item.id}')
                                                 for item in question.match_items.all()}
            else:
                bucket = 'q_choice' if question.question_type == 'CHOICE' else 'q_short'
                saved_answers[bucket][key] = request.POST.get(f'question_{question.id}')

        # Без жодної відповіді — це не результат: не зберігаємо і не рахуємо «слабкими» всі теми
        answered = any(saved_answers['q_choice'].values()) or any(saved_answers['q_short'].values()) or any(
            any(pairs.values()) for pairs in saved_answers['q_match'].values())
        if not answered:
            return render(request, 'materials/diagnostic_results.html', {'no_answers': True})

        total_score, max_score, topics_stats = diagnostic_stats(saved_answers)
        percent_total = int((total_score / max_score) * 100) if max_score > 0 else 0

        previous_percent = None
        if request.user.is_authenticated:
            previous = next((d for d in user_diagnostics(request.user)[:30] if diagnostic_scope(d) == scope), None)
            previous_percent = previous.get_percent() if previous else None
            diag_material, _ = StudyMaterial.objects.get_or_create(
                title=DIAGNOSTIC_MATERIAL_TITLE,
                defaults={'price': 0, 'is_published': False, 'is_free': True}
            )
            PracticeAttempt.objects.create(
                user=request.user, material=diag_material,
                score=total_score, max_score=max_score, answers_json=saved_answers
            )

        weak_topics, recommendations, sorted_stats = diagnostic_summary(topics_stats)
        offer_materials = offer_candidates(request.user, recommendations)
        if request.user.is_authenticated:
            offer = DiagnosticOffer.offer_for(request.user, offer_materials)
        else:
            # Гість побачить пакет і знижку; отримає її, коли увійде (уроки запам'ятовуємо в сесії)
            offer = None
            request.session['diagnostic_offer_materials'] = [m.id for m in offer_materials]
        return render(request, 'materials/diagnostic_results.html', {
            'total_score': total_score, 'max_score': max_score, 'percent_total': percent_total,
            'weak_topics': weak_topics, 'topics_stats': sorted_stats, 'recommendations': recommendations,
            'previous_percent': previous_percent,
            'percent_change': None if previous_percent is None else percent_total - previous_percent,
            **offer_context(offer, offer_materials),
            'countdown': nmt_countdown(len(weak_topics)),
        })

    # Спершу учень обирає теми: кілька або всі теми НМТ
    nmt_topics = CurriculumTopic.objects.filter(chapter__grade__subject__name=NMT_SUBJECT_NAME)
    if request.GET.get('topics') == 'all':
        topic_ids = None
    else:
        topic_ids = sorted({int(t) for t in request.GET.getlist('topic') if t.isdigit()}
                           & set(nmt_topics.values_list('id', flat=True)))
        if not topic_ids:
            return diagnostic_choose_topics(request, nmt_topics)

    questions = Question.objects.filter(curriculum_topic__in=nmt_topics)
    if topic_ids is None:
        selected = pick_all_topics(questions)
    else:
        selected = pick_from_topics(questions.filter(curriculum_topic_id__in=topic_ids))

    final_questions = list(questions_in_order(selected))
    question_ids_str = ','.join(str(q.id) for q in final_questions)

    return render(request, 'materials/diagnostic_test.html', {
        'questions': final_questions,
        'question_ids_str': question_ids_str,
        'total_selected': len(final_questions),
        'tasks_word': tasks_word(len(final_questions)),
        'scope': 'all' if topic_ids is None else ','.join(map(str, topic_ids)),
        'scope_label': scope_label('all' if topic_ids is None else topic_ids),
    })


def offer_candidates(user, recommendations):
    """Платні уроки слабких тем, яких учень ще не має, — з них складається пакет після діагностики."""
    return [m for m in recommendations
            if not m.is_free and m.price > 0 and not m.is_bundle and not user_owns_material(user, m)]


def offer_context(offer, materials):
    """Ціни пакета для сторінки: повна сума, сума зі знижкою, економія і до коли діє знижка."""
    materials = list(offer.materials.all()) if offer else list(materials)
    if not materials:
        return {}
    full = sum(m.price for m in materials)
    percent = offer.discount_percent if offer else DiagnosticOffer.DISCOUNT_PERCENT
    discount = int(round(full * percent / 100))
    return {'offer': offer, 'offer_materials': materials, 'offer_full': full, 'offer_price': full - discount,
            'offer_saving': discount, 'offer_percent': percent,
            'offer_hours': int(DiagnosticOffer.DURATION.total_seconds() // 3600)}


def nmt_countdown(weak_count):
    """Скільки днів до НМТ і скільки днів припадає на одну слабку тему, якщо почати зараз."""
    days = (datetime.date.fromisoformat(settings.NMT_DATE) - timezone.localdate()).days
    if days <= 0:
        return None
    per_topic = days // weak_count if weak_count else None
    return {'days': days, 'days_word': uk_plural(days, 'день', 'дні', 'днів'), 'exact': settings.NMT_DATE_EXACT,
            'weak': weak_count, 'weak_word': uk_plural(weak_count, 'тему', 'теми', 'тем'),
            'days_per_topic': per_topic, 'per_topic_word': uk_plural(per_topic or 0, 'день', 'дні', 'днів')}


@login_required
def diagnostic_offer_view(request):
    """Пакет слабких тем зі знижкою: сторінка після входу гостя й кнопка «Купити пакет» (додає уроки в кошик)."""
    offer = DiagnosticOffer.objects.filter(user=request.user, expires_at__gt=timezone.now()).first()
    claimed_ids = request.session.pop('diagnostic_offer_materials', None)
    if offer is None and claimed_ids:
        candidates = offer_candidates(request.user, StudyMaterial.objects.filter(id__in=claimed_ids, is_published=True))
        offer = DiagnosticOffer.offer_for(request.user, candidates)

    if request.method == 'POST' and offer:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        added = 0
        for material in offer.materials.all():
            if not user_owns_material(request.user, material):
                _, created = CartItem.objects.get_or_create(cart=cart, material=material)
                added += created
        messages.success(request, f"🎯 Уроки слабких тем у кошику, знижка −{offer.discount_percent}% уже врахована."
                         if added else "Ці уроки вже у вашому кошику.")
        return redirect('cart_detail')

    if offer is None:
        messages.info(request, "Пропозиції зі знижкою зараз немає. Пройдіть діагностику, щоб побачити слабкі теми.")
        return redirect('diagnostic_test')
    return render(request, 'materials/diagnostic_offer.html', offer_context(offer, []))


def uk_plural(count, one, few, many):
    """1, 21… — one; 2–4, 22–24… — few; решта (і 11–14) — many."""
    if count % 10 == 1 and count % 100 != 11:
        return one
    if count % 10 in (2, 3, 4) and count % 100 not in (12, 13, 14):
        return few
    return many


def tasks_word(count):
    return uk_plural(count, 'завдання', 'завдання', 'завдань')


# Склад як на НМТ: 15 з вибором відповіді, 3 на відповідність, 4 з короткою відповіддю
DIAGNOSTIC_COUNTS = {'CHOICE': 15, 'MATCH': 3, 'SHORT': 4}


def pick_all_topics(questions):
    """Усі теми НМТ: дві третини алгебри й третина геометрії, як в екзамені."""
    buckets = {}
    for q_id, q_type, chapter_order in questions.values_list('id', 'question_type', 'curriculum_topic__chapter__order'):
        buckets.setdefault((q_type, chapter_order <= 540), []).append(q_id)

    def pick(q_type, is_algebra, count):
        ids = buckets.get((q_type, is_algebra), [])
        return random.sample(ids, min(count, len(ids)))

    selected = []
    for q_type, (algebra, geometry) in (('CHOICE', (10, 5)), ('MATCH', (2, 1)), ('SHORT', (2, 2))):
        group = pick(q_type, True, algebra) + pick(q_type, False, geometry)
        random.shuffle(group)
        selected += group
    return selected


def pick_from_topics(questions):
    """Обрані теми: завдань кожного типу порівну з кожної теми (по колу), скільки є в банку."""
    by_type = {}
    for q_id, q_type, topic_id in questions.values_list('id', 'question_type', 'curriculum_topic_id'):
        by_type.setdefault(q_type, {}).setdefault(topic_id, []).append(q_id)

    selected = []
    for q_type, count in DIAGNOSTIC_COUNTS.items():
        pools = [random.sample(ids, len(ids)) for ids in by_type.get(q_type, {}).values()]
        random.shuffle(pools)
        group = []
        while len(group) < count and any(pools):
            for pool in pools:
                if pool and len(group) < count:
                    group.append(pool.pop())
        random.shuffle(group)
        selected += group
    return selected


def scope_label(scope):
    """«Усі теми НМТ» або назви обраних тем — щоб у кабінеті було видно, що саме перевіряли."""
    if scope in ('all', None, ''):
        return 'Усі теми НМТ'
    ids = scope if isinstance(scope, list) else parse_id_list(scope)
    names = list(CurriculumTopic.objects.filter(id__in=ids).values_list('name', flat=True))
    return ', '.join(names) if len(names) <= 3 else f"{', '.join(names[:3])} та ще {len(names) - 3}"


def diagnostic_scope(attempt):
    # Старі діагностики (до вибору тем) — по всіх темах
    return (attempt.answers_json or {}).get('scope') or 'all'


def number_in_name(name):
    """«Розділ 3. …» → 3, «15. Системи рівнянь» → 15; без номера — у кінець."""
    match = re.search(r'\d+', name or '')
    return int(match.group()) if match else 10 ** 6


def diagnostic_choose_topics(request, nmt_topics):
    # Запит із Count групує рядки, і Django тоді не застосовує сортування з Meta моделі —
    # тож розділи збираємо словником, а порядок задаємо самі: за номером у назві, як бачить учень
    with_questions = (nmt_topics.annotate(n=Count('diagnostic_questions'))
                      .filter(n__gt=0).select_related('chapter'))
    by_chapter = {}
    for topic in with_questions:
        by_chapter.setdefault(topic.chapter_id, {'chapter': topic.chapter, 'topics': []})['topics'].append(topic)
    chapters = sorted(by_chapter.values(),
                      key=lambda g: (number_in_name(g['chapter'].name), g['chapter'].order, g['chapter'].id))
    for group in chapters:
        group['topics'].sort(key=lambda t: (number_in_name(t.name), t.order, t.id))
    return render(request, 'materials/diagnostic_choose.html', {'chapters': chapters})


# ==========================================
# ПРАКТИКА НМТ ПІСЛЯ УРОКУ
# ==========================================
@login_required
def practice_session_view(request, material_id):
    material = get_object_or_404(StudyMaterial, id=material_id)
    has_access = (is_teacher(request.user) or user_owns_material(request.user, material)
                  or homework.grants_access(request.user, material))

    if not material.is_published and not has_access:
        raise Http404("Матеріал не знайдено.")
    if not (material.is_free or has_access):
        messages.error(request, f"Практика доступна після придбання матеріалу «{material.title}».")
        return redirect('material_detail', pk=material.id)

    profile = practice.practice_profile(material)
    if profile:
        return school_practice(request, material, profile)

    if request.method == 'POST':
        total_score = 0
        max_score = 0
        results_data = []

        saved_answers = {'q_choice': {}, 'q_match': {}, 'q_short': {}}

        question_ids_str = request.POST.get('question_ids', '')
        saved_answers['question_ids'] = question_ids_str

        questions = questions_in_order(parse_id_list(question_ids_str))
        if questions:
            questions = questions.filter(materials=material).distinct()

        for q in questions:
            q_result = {
                'question': q, 'type': q.question_type, 'is_correct': False,
                'user_answer': None, 'correct_answer': None, 'points_earned': 0, 'max_points': 0
            }

            if q.question_type == 'CHOICE':
                q_result['max_points'] = 1
                q_result['correct_answer'] = next((opt for opt in q.options.all() if opt.is_correct), None)
                user_ans = request.POST.get(f'q_{q.id}')
                saved_answers['q_choice'][str(q.id)] = user_ans

                opt = find_option(q, user_ans)
                if opt:
                    q_result['user_answer'] = opt
                    if opt.is_correct:
                        total_score += 1
                        q_result['points_earned'] = 1
                        q_result['is_correct'] = True
                max_score += 1

            elif q.question_type == 'MATCH':
                q_result['max_points'] = 3
                q_result['matches'] = []
                match_points = 0
                saved_answers['q_match'][str(q.id)] = {}

                for item in q.match_items.all():
                    user_match = request.POST.get(f'match_{item.id}')
                    saved_answers['q_match'][str(q.id)][str(item.id)] = user_match

                    user_opt = find_option(q, user_match)
                    is_match_correct = user_opt is not None and user_opt.id == item.correct_option_id
                    if is_match_correct:
                        match_points += 1
                        total_score += 1

                    q_result['matches'].append({
                        'item': item, 'user_option': user_opt,
                        'correct_option': item.correct_option, 'is_correct': is_match_correct
                    })

                q_result['points_earned'] = match_points
                q_result['is_correct'] = (match_points == 3)
                max_score += 3

            elif q.question_type == 'SHORT':
                q_result['max_points'] = 2
                q_result['correct_answer'] = q.correct_short_answer
                user_ans = request.POST.get(f'q_{q.id}')
                saved_answers['q_short'][str(q.id)] = user_ans
                q_result['user_answer'] = user_ans

                if user_ans:
                    if short_answer_matches(user_ans, q.correct_short_answer):
                        total_score += 2
                        q_result['points_earned'] = 2
                        q_result['is_correct'] = True
                max_score += 2

            record_game_answer(request.user, q, q_result['is_correct'])
            results_data.append(q_result)

        PracticeAttempt.objects.create(
            user=request.user,
            material=material,
            score=total_score,
            max_score=max_score,
            answers_json=saved_answers
        )

        context = {
            'material': material,
            'total_score': total_score,
            'max_score': max_score,
            'results_data': results_data,
        }
        return render(request, 'materials/practice_results.html', context)

    match_current = re.match(r'^(\d+)', material.title)
    current_topic_num = int(match_current.group(1)) if match_current else 0
    # ОНОВЛЕНО: select_related('curriculum_topic')
    raw_pool = (Question.objects.filter(materials=material).select_related('curriculum_topic')
                .prefetch_related('options', 'match_items', 'materials'))

    safe_pool = []
    for q in raw_pool:
        is_safe = is_own_question(q, material, current_topic_num)
        if not is_safe:
            is_safe = True
            for mat in q.materials.all():
                match_mat = re.match(r'^(\d+)', mat.title)
                mat_num = int(match_mat.group(1)) if match_mat else 0
                if mat_num > current_topic_num:
                    is_safe = False
                    break
        if is_safe:
            safe_pool.append(q)

    choice_pool = [q for q in safe_pool if q.question_type == 'CHOICE']
    match_pool = [q for q in safe_pool if q.question_type == 'MATCH']
    short_pool = [q for q in safe_pool if q.question_type == 'SHORT']

    seen_ids = seen_question_ids(request.user)
    q_choice = sample_unseen_first(choice_pool, 10, seen_ids)
    q_match = sample_unseen_first(match_pool, 2, seen_ids)
    q_short = sample_unseen_first(short_pool, 1, seen_ids)

    selected_questions = q_choice + q_match + q_short
    random.shuffle(selected_questions)

    if len(selected_questions) == 0:
        messages.info(request, "Для цієї теми ще не додано практичних завдань.")
        return redirect('cabinet')

    question_ids_str = ','.join(str(q.id) for q in selected_questions)
    context = {
        'material': material, 'q_choice': q_choice, 'q_match': q_match,
        'q_short': q_short, 'question_ids_str': question_ids_str, 'total_selected': len(selected_questions)
    }
    return render(request, 'materials/practice_session.html', context)


def practice_access(request, material):
    """Шкільну практику бачить той, хто може відкрити саму тему (як і в practice_session_view)."""
    has_access = (is_teacher(request.user) or user_owns_material(request.user, material)
                  or homework.grants_access(request.user, material))
    return (material.is_published or has_access) and (material.is_free or has_access)


class PracticeActor:
    """Для кого йде практика. Учень практикується сам (домашнє завдання). Вчитель на уроці показує екран і сам
    натискає: обирає учня (?student=<id заявки>) — спроба й оцінки зараховуються учневі, — групу учнів
    (?g=…&g=…&student=<хто відповідає зараз>; у кожного свої сходинки), або демонстрацію без збереження (?demo=1)."""

    def __init__(self, user, teacher=None, student=None, demo=False, group=()):
        self.user, self.teacher, self.student, self.demo, self.group = user, teacher, student, demo, list(group)

    @property
    def lesson(self):
        return self.teacher is not None

    def query_for(self, student):
        group = ''.join(f'g={s.id}&' for s in self.group)
        return f'?{group}student={student.id}'

    @property
    def query(self):
        if self.demo:
            return '?demo=1'
        return self.query_for(self.student) if self.student else ''

    @property
    def next_query(self):
        """У групі після завдання відповідає наступний учень."""
        if not self.group:
            return self.query
        index = next((i for i, s in enumerate(self.group) if s.id == self.student.id), -1)
        return self.query_for(self.group[(index + 1) % len(self.group)])

    @classmethod
    def from_request(cls, request):
        """None — вчитель ще не обрав, для кого практика."""
        if not is_teacher(request.user):
            return cls(request.user)
        if request.GET.get('demo') == '1':
            return cls(request.user, teacher=request.user, demo=True)
        approved = TutorStudentRequest.objects.filter(status='approved').select_related('user')
        ids = [i for i in (to_int(v) for v in request.GET.getlist('g')) if i is not None][:10]
        by_id = {s.id: s for s in approved.filter(id__in=ids)}
        group = [by_id[i] for i in dict.fromkeys(ids) if i in by_id]
        wanted = to_int(request.GET.get('student'))
        if group:
            student = next((s for s in group if s.id == wanted), group[0])
            return cls(student.user, teacher=request.user, student=student, group=group)
        student = approved.filter(id=wanted).first()
        return cls(student.user, teacher=request.user, student=student) if student else None


def active_run(actor, material):
    return (PracticeRun.objects.filter(user=actor.user, teacher=actor.teacher, material=material,
                                       finished_at__isnull=True)
            .order_by('-id').first())


def choose_student_page(request, material):
    """Вчитель відкрив практику: для кого вона? Спершу учні того класу, що й тема."""
    grade_number = material.curriculum_grade.number if material.curriculum_grade else None
    students = list(TutorStudentRequest.objects.filter(status='approved').order_by('real_name'))
    students.sort(key=lambda s: s.course != f'grade_{grade_number}')
    in_progress = set(PracticeRun.objects.filter(teacher=request.user, material=material, finished_at__isnull=True)
                      .values_list('user_id', flat=True))
    return render(request, 'materials/practice_choose_student.html', {
        'material': material, 'students': students, 'in_progress': in_progress,
        'grade_course': f'grade_{grade_number}',
    })


def school_practice(request, material, profile):
    """Практика «сходинками»: сторінка показує одне поточне завдання; відповіді перевіряє practice_check_view."""
    actor = PracticeActor.from_request(request)
    if actor is None:
        return choose_student_page(request, material)
    run = active_run(actor, material)
    if run is None or run.profile != profile:
        run = PracticeRun.objects.create(user=actor.user, teacher=actor.teacher, material=material, profile=profile,
                                         state=practice.new_state(kind=practice.topic_kind(material)))
    if request.method == 'POST':
        if actor.group and request.POST.get('scope') == 'group':
            return finish_group(request, material, actor)
        return finish_run(request, run, actor)

    state = run.state
    entry = practice.current_entry(state)
    if entry is None and state['status'] == 'active':
        own, review = practice.question_pools(material, profile)
        seen = seen_question_ids(actor.user)
        if not state['history']:
            state['top_skills'] = sorted(practice.top_skills(own))
            if state.get('kind') == 'diagnostic':
                state['plan'] = practice.diagnostic_plan(own, seen)
        question, is_review = practice.next_question(state, own, review, seen)
        if question is None and not state['history']:
            run.delete()
            messages.info(request, "Для цієї теми ще не додано практичних завдань.")
            return redirect('cabinet')
        if question is None:
            state['status'] = 'empty'
        else:
            entry = practice.start_task(state, question, review=is_review)
        run.save(update_fields=['state', 'updated_at'])

    question = None
    if entry is not None:
        question = (Question.objects.prefetch_related('options', 'match_items')
                    .filter(id=entry['qid']).first())
    return render(request, 'materials/practice_school.html', {
        'material': material, 'profile': profile, 'cfg': practice.PROFILES[profile], 'state': state,
        'question': question, 'spec': practice.public_spec(question, entry) if question else {},
        'task_number': len(state['history']), 'levels': practice.LEVELS,
        'max_tasks': len(state['plan']) if state.get('plan') is not None else practice.MAX_TASKS,
        'kind': state.get('kind', 'lesson'),
        'solved_count': sum(1 for e in state['history'] if e.get('tries')),
        'check_url': reverse('practice_check', args=[material.id]) + actor.query,
        'actor': actor, 'next_query': actor.next_query,
        'group_tabs': [(s, actor.query_for(s), s.id == actor.student.id) for s in actor.group],
    })


def build_attempt(run, actor):
    """Спроба з розв'язаних завдань практики (ще не збережена) і розбір; None — відповідей немає."""
    state = run.state
    history = [entry for entry in state['history'] if entry.get('tries')]
    if not history:
        return None, []
    questions_by_id = {q.id: q for q in questions_in_order([entry['qid'] for entry in history])}
    results, total, maximum, grades = practice.build_results(questions_by_id, history, run.profile)
    diagnostic = state.get('kind') == 'diagnostic'
    if diagnostic:   # діагностика — карта прогалин, а не оцінка
        grades = {field: None for field in grades}
    attempt = PracticeAttempt(
        user=actor.user, conducted_by=actor.teacher, material=run.material, score=total, max_score=maximum, **grades,
        answers_json={'mode': run.profile, 'question_ids': ','.join(str(entry['qid']) for entry in history),
                      'history': history, 'level': state['level'], 'status': state['status'],
                      'stuck': not diagnostic and practice.is_stuck(history), 'gaps': practice.gap_topics(history),
                      'kind': state.get('kind', 'lesson'), 'topic_map': practice.topic_map(history)})
    return attempt, results


def save_attempt(run, attempt):
    attempt.save()
    run.finished_at = timezone.now()
    run.save(update_fields=['finished_at', 'updated_at'])
    if attempt.conducted_by_id is None:
        homework.link_attempt(attempt)


def finish_run(request, run, actor):
    """Завершити практику: зберегти спробу з оцінками й показати розбір (через redirect — без повторної відправки).
    Демонстрацію не зберігаємо — розбір показуємо одразу."""
    attempt, results = build_attempt(run, actor)
    if attempt is None:
        run.delete()
        messages.info(request, "Ще немає жодної відповіді — практику не збережено.")
        return redirect('cabinet')
    if actor.demo:
        run.delete()
        context = school_results_context(request, attempt, results)
        context['again_url'] = reverse('practice_session', args=[run.material_id]) + actor.query
        return render(request, 'materials/practice_school_results.html', context)
    save_attempt(run, attempt)
    return redirect('view_attempt_details', attempt_id=attempt.id)


def finish_group(request, material, actor):
    """Групове заняття закінчено: зберегти спроби всіх учнів групи, які щось розв'язали."""
    rows = []
    for student in actor.group:
        member = PracticeActor(student.user, teacher=actor.teacher, student=student)
        run = active_run(member, material)
        attempt = build_attempt(run, member)[0] if run else None
        if attempt is not None:
            save_attempt(run, attempt)
        elif run is not None:
            run.delete()
        rows.append((student, attempt))
    return render(request, 'materials/practice_group_results.html', {'material': material, 'rows': rows})


@login_required
@post_required('cabinet')
def attempt_manage(request, attempt_id):
    """Вчитель виправляє промах: спробу записано не тому учневі (перенести) або випадково (видалити)."""
    if not is_teacher(request.user):
        return redirect('cabinet')
    attempt = get_object_or_404(PracticeAttempt.objects.select_related('material'), id=attempt_id)
    if request.POST.get('action') == 'delete':
        attempt.delete()
        messages.success(request, f"🗑 Спробу «{attempt.material.title}» видалено.")
        return redirect('cabinet')
    student = get_object_or_404(TutorStudentRequest, id=to_int(request.POST.get('student_id')), status='approved')
    Homework.objects.filter(attempt=attempt).update(attempt=None)
    attempt.user = student.user
    attempt.save(update_fields=['user'])
    if attempt.conducted_by_id is None:
        homework.link_attempt(attempt)
    messages.success(request, f"↪ Спробу перенесено: {student.real_name}.")
    return redirect('view_attempt_details', attempt_id=attempt.id)


@login_required
def practice_start(request):
    """Кабінет вчителя: почати узагальнення розділу чи діагностику за клас (обрано зі списку)."""
    material = get_object_or_404(StudyMaterial, id=to_int(request.GET.get('material_id')))
    if not is_teacher(request.user) or practice.practice_profile(material) is None:
        return redirect('cabinet')
    return redirect('practice_session', material_id=material.id)


@login_required
@post_required('cabinet')
def homework_assign(request):
    """Задати учневі практику з теми додому до дати."""
    if not is_teacher(request.user):
        return redirect('cabinet')
    student = get_object_or_404(TutorStudentRequest, id=to_int(request.POST.get('student_id')), status='approved')
    material = get_object_or_404(StudyMaterial, id=to_int(request.POST.get('material_id')))
    try:
        due_date = datetime.date.fromisoformat(request.POST.get('due_date', ''))
    except ValueError:
        messages.error(request, "Вкажіть дату, до якої виконати ДЗ.")
        return redirect(safe_back_url(request))
    if practice.practice_profile(material) is None:
        messages.error(request, "Домашню практику можна задати лише з теми шкільного курсу.")
        return redirect(safe_back_url(request))
    Homework.objects.create(teacher=request.user, student=student, material=material, due_date=due_date)
    messages.success(request, f"✅ {student.real_name}: задано «{material.title}» до {due_date:%d.%m.%Y}.")
    return redirect(safe_back_url(request))


@login_required
@post_required('cabinet')
def homework_credit(request, homework_id):
    """Учень почав ДЗ і не завершив — зарахувати те, що вже розв'язано."""
    if not is_teacher(request.user):
        return redirect('cabinet')
    hw = get_object_or_404(Homework.objects.select_related('student__user', 'material'), id=homework_id,
                           attempt__isnull=True)
    run = (PracticeRun.objects.filter(user=hw.student.user, material=hw.material, teacher__isnull=True,
                                      finished_at__isnull=True, created_at__gte=hw.created_at).order_by('-id').first())
    attempt = build_attempt(run, PracticeActor(hw.student.user))[0] if run else None
    if attempt is None:
        messages.info(request, "Учень ще не розв'язав жодного завдання.")
        return redirect('cabinet')
    save_attempt(run, attempt)
    messages.success(request, f"✅ Зараховано розв'язане: {hw.student.real_name}, «{hw.material.title}».")
    return redirect('view_attempt_details', attempt_id=attempt.id)


def answer_is_empty(answer):
    if answer in (None, '', [], {}):
        return True
    if isinstance(answer, list):
        return any(item is None or item == '' for item in answer)
    if isinstance(answer, dict):
        return any(value == '' for value in answer.values())
    return False


@login_required
def practice_check_view(request, material_id):
    """Перевірка відповіді на поточне завдання. Правильну відповідь і розв'язання повертаємо лише тоді,
    коли спроби на це завдання закінчились; тоді ж учень рухається сходинками."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST only'}, status=405)
    material = get_object_or_404(StudyMaterial, id=material_id)
    profile = practice.practice_profile(material)
    if not profile or not practice_access(request, material):
        raise Http404
    try:
        data = json.loads(request.body)
        question_id = int(data.get('question_id'))
    except (ValueError, TypeError, AttributeError, json.JSONDecodeError):
        return JsonResponse({'error': 'bad request'}, status=400)

    actor = PracticeActor.from_request(request)
    if actor is None:
        raise Http404
    run = active_run(actor, material)
    entry = practice.current_entry(run.state) if run else None
    if entry is None or entry['qid'] != question_id:
        return JsonResponse({'error': 'stale'}, status=409)
    question = get_object_or_404(Question.objects.prefetch_related('options', 'match_items'), id=question_id)

    answer = practice.clean_answer(question, data.get('answer'), entry)
    if answer_is_empty(answer):
        return JsonResponse({'error': 'empty'}, status=400)
    entry['tries'].append(answer)
    if actor.lesson and data.get('assisted') is True:
        entry['assisted'] = True
    state = run.state
    response = {'correct': practice.is_correct(question, answer),
                'finished': practice.is_finished(question, entry['tries'], practice.max_tries(state, profile))}
    if response['finished']:
        level_before = state['level']
        first_ok = practice.finish_task(state, question, entry)
        if not actor.demo:
            practice.record_mistake(actor.user, question, first_ok)
        response.update(practice.reveal(question, entry), solution=question.solution, level=state['level'],
                        level_change=state['level'] - level_before, status=state['status'])
    else:
        response['hint'] = question.hint or practice.DEFAULT_HINT
    run.save(update_fields=['state', 'updated_at'])
    return JsonResponse(response)


def next_material(material):
    """Наступна тема того самого класу за деревом тем — для учня, який опанував поточну."""
    topic = material.curriculum_topic
    chapter = topic.chapter
    later = (Q(curriculum_topic__chapter__order__gt=chapter.order)
             | Q(curriculum_topic__chapter__order=chapter.order, curriculum_topic__order__gt=topic.order))
    return (StudyMaterial.objects.filter(later, is_published=True, is_bundle=False,
                                         curriculum_topic__chapter__grade=chapter.grade)
            .order_by('curriculum_topic__chapter__order', 'curriculum_topic__order').defer('html_content').first())


def gap_materials(topic_ids):
    """[(тема, урок або None)] — що повторити за помилками в завданнях на повторення."""
    topics = {t.id: t for t in CurriculumTopic.objects.filter(id__in=topic_ids).select_related('chapter')}
    lessons = {}
    for m in StudyMaterial.objects.filter(curriculum_topic_id__in=topic_ids, is_published=True, is_bundle=False) \
            .defer('html_content'):
        lessons.setdefault(m.curriculum_topic_id, m)
    return [(topics[t], lessons.get(t)) for t in topic_ids if t in topics]


def topic_rows(topic_map):
    """Розклад по темах для узагальнення й діагностики: [(тема, урок, правильно, усього, стан)] у порядку програми."""
    ids = [int(t) for t in topic_map]
    rows = []
    for topic, lesson in gap_materials(ids):
        right, total = topic_map[str(topic.id)]
        state = 'ok' if right == total else ('partial' if right else 'repeat')
        rows.append({'topic': topic, 'lesson': lesson, 'right': right, 'total': total, 'state': state})
    rows.sort(key=lambda r: (r['topic'].chapter.order, r['topic'].order))
    return rows


def attention_list(since_days=30):
    """Учні, на яких варто звернути увагу: застрягли або помиляються в повторенні попередніх тем."""
    since = timezone.now() - datetime.timedelta(days=since_days)
    rows = []
    for attempt in (PracticeAttempt.objects.filter(created_at__gte=since, user__tutor_request__status='approved')
                    .select_related('user__tutor_request', 'material').defer('material__html_content')
                    .order_by('-created_at')[:200]):
        saved = attempt.answers_json or {}
        if saved.get('mode') in practice.PROFILES and (saved.get('stuck') or saved.get('gaps')):
            rows.append({'attempt': attempt, 'stuck': saved.get('stuck'), 'gaps': saved.get('gaps') or []})
    topic_names = dict(CurriculumTopic.objects.filter(id__in={t for r in rows for t in r['gaps']})
                       .values_list('id', 'name'))
    for row in rows:
        row['gap_names'] = [topic_names[t] for t in row['gaps'] if t in topic_names]
    return rows[:20]


def school_results_context(request, attempt, results):
    saved = attempt.answers_json or {}
    context = {
        'material': attempt.material, 'attempt': attempt, 'results': results, 'profile': saved.get('mode'),
        # Найвища складність, на якій учень розв'язав завдання (сходинка учня може бути вищою, якщо банк неповний)
        'level': max((r['level'] for r in results if r['earned']), default=0),
        'status': saved.get('status'), 'levels': practice.LEVELS,
        'again_url': reverse('practice_session', args=[attempt.material.id]),
        'stuck': saved.get('stuck'), 'gaps': gap_materials(saved.get('gaps') or []),
        'kind': saved.get('kind', 'lesson'), 'topic_rows': topic_rows(saved.get('topic_map') or {}),
        'next_material': next_material(attempt.material) if saved.get('status') == 'mastered' else None,
    }
    # Вчитель після уроку: оцінки одразу в звіт заняття учня
    if is_teacher(request.user) and attempt.pk and attempt.user_id != request.user.id:
        student = TutorStudentRequest.objects.filter(user_id=attempt.user_id).first()
        if student:
            context['report_student'] = student
            context['hw_choices'] = StudentReport.HW_CHOICES
            context['hw_default'] = homework.report_status(student)
            context['default_due'] = timezone.localdate() + datetime.timedelta(days=7)
            context['again_url'] += f'?student={student.id}'
            context['other_students'] = TutorStudentRequest.objects.filter(status='approved').exclude(id=student.id) \
                .order_by('real_name')
    return context


# ==========================================
# КОШИК
# ==========================================
@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'apply_promo':
            promo = request.POST.get('promo_code', '').strip().upper()
            if promo == Cart.PROMO_CODE:
                now = timezone.localdate()
                start_date, end_date = Cart.PROMO_START, Cart.PROMO_END

                if start_date <= now <= end_date:
                    cart.promo_code = promo
                    cart.save()
                    messages.success(request, "🎉 Промокод ВЧИТЕЛЬ успішно застосовано! Ваша знижка 40%.")
                elif now < start_date:
                    messages.error(request, f"⏳ Цей промокод почне діяти з {start_date:%d.%m}!")
                else:
                    messages.error(request, "❌ Термін дії цього промокоду минув.")
            else:
                messages.error(request, "❌ Невірний промокод.")

        elif action == 'remove_promo':
            cart.promo_code = None
            cart.save()
            messages.info(request, "Промокод скасовано.")

        return redirect('cart_detail')

    return render(request, 'materials/cart.html', {'cart': cart, 'cart_items': cart.cached_items()})


@login_required
@post_required(material_page)
def add_to_cart(request, material_id):
    material = get_object_or_404(StudyMaterial, id=material_id, is_published=True)

    if user_owns_material(request.user, material):
        messages.warning(request, "Ви вже придбали цей матеріал!")
        return redirect('cabinet')

    if material.is_free or material.price == 0:
        if material.is_bundle:
            for sub_material in material.included_materials.all():
                request.user.purchased_materials.add(sub_material)
            messages.success(request, f"🎉 Всі матеріали з пакету «{material.title}» додано до вашого кабінету!")
        else:
            request.user.purchased_materials.add(material)
            messages.success(request, f"🎉 Безкоштовний матеріал «{material.title}» додано до вашого кабінету!")
        return redirect('cabinet')

    cart, created = Cart.objects.get_or_create(user=request.user)

    if CartItem.objects.filter(cart=cart, material=material).exists():
        messages.info(request, "Цей матеріал вже є у вашому кошику.")
    else:
        CartItem.objects.create(cart=cart, material=material)
        messages.success(request, f"«{material.title}» додано до кошика! 🛒")

    return redirect('cart_detail')


@login_required
@post_required('cart_detail')
def remove_from_cart(request, item_id):
    cart = get_object_or_404(Cart, user=request.user)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    item.delete()
    messages.success(request, "Матеріал видалено з кошика.")
    return redirect('cart_detail')


class HomeView(TemplateView):
    template_name = 'materials/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['general_reviews'] = Review.objects.filter(material__isnull=True, is_approved=True)
        return context


class AboutView(TemplateView):
    template_name = 'materials/about.html'


class OfferView(TemplateView):
    template_name = 'materials/offer.html'


class PrivacyView(TemplateView):
    template_name = 'materials/privacy.html'


def web_manifest(request):
    icons = [{'src': static(f'images/icon-{size}.png'), 'sizes': f'{size}x{size}', 'type': 'image/png'}
             for size in (192, 512)]
    icons += [{'src': static(f'images/icon-maskable-{size}.png'), 'sizes': f'{size}x{size}', 'type': 'image/png',
               'purpose': 'maskable'} for size in (192, 512)]
    data = {
        'name': 'ДО КВАДРАТУ — підготовка до НМТ з математики',
        'short_name': 'ДО КВАДРАТУ',
        'start_url': '/',
        'display': 'browser',
        'background_color': '#344e86',
        'theme_color': '#344e86',
        'icons': icons,
    }
    response = JsonResponse(data, json_dumps_params={'ensure_ascii': False})
    response['Content-Type'] = 'application/manifest+json'
    return response


def booking_view(request):
    return render(request, 'booking.html')


# ==========================================
# ОНОВЛЕНА ВІТРИНА
# ==========================================
class MaterialListView(ListView):
    model = StudyMaterial
    template_name = 'materials/list.html'
    context_object_name = 'materials'

    def get_queryset(self):
        queryset = StudyMaterial.objects.filter(is_published=True) \
            .select_related('curriculum_topic__chapter__grade__subject') \
            .prefetch_related('tags')

        filter_type = self.request.GET.get('type')
        if filter_type == 'free':
            queryset = queryset.filter(is_free=True)
        elif filter_type == 'bundle':
            queryset = queryset.filter(is_bundle=True)

        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)

        subject_id = self.request.GET.get('subject')
        grade_id = self.request.GET.get('grade')

        if grade_id:
            queryset = queryset.filter(curriculum_topic__chapter__grade_id=grade_id)
        elif subject_id:
            queryset = queryset.filter(curriculum_topic__chapter__grade__subject_id=subject_id)

        materials_list = list(queryset)

        def get_sort_key(material):
            if material.curriculum_topic:
                ct = material.curriculum_topic
                return (
                    ct.chapter.grade.subject.order,
                    ct.chapter.grade.order,
                    ct.chapter.order,
                    ct.order
                )
            else:
                match = re.match(r'^(\d+)', material.title)
                num = int(match.group(1)) if match else 99999
                return (999, 999, 999, num)

        materials_list.sort(key=get_sort_key)
        return materials_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subjects'] = CurriculumSubject.objects.prefetch_related('grades').all()
        context['current_subject'] = self.request.GET.get('subject', '')
        context['current_grade'] = self.request.GET.get('grade', '')
        context['search_query'] = self.request.GET.get('search', '')
        context['nmt_countdown'] = nmt_countdown(0)
        return context


class MaterialDetailView(DetailView):
    model = StudyMaterial
    template_name = 'materials/detail.html'
    context_object_name = 'material'

    def get_object(self, queryset=None):
        material = super().get_object(queryset)
        user = self.request.user
        if not (material.is_published or is_teacher(user) or user_owns_material(user, material)):
            raise Http404("Матеріал не знайдено.")
        return material

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        material = self.object
        context['is_owned'] = user_owns_material(self.request.user, material)
        context['default_description'] = DEFAULT_MATERIAL_DESCRIPTION
        context['approved_reviews'] = material.reviews.filter(is_approved=True).select_related('user')

        if material.is_bundle:
            total_original_price = sum(item.price for item in material.included_materials.all())
            context['total_original_price'] = total_original_price
            context['savings'] = total_original_price - material.price

        return context


class CabinetView(LoginRequiredMixin, TemplateView):
    template_name = 'materials/cabinet.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        with_tree = 'curriculum_topic__chapter__grade__subject'
        purchased_list = list(self.request.user.purchased_materials.select_related(with_tree).prefetch_related(
            Prefetch('included_materials', queryset=StudyMaterial.objects.select_related(with_tree))))

        def get_number(material):
            if material.curriculum_topic:
                ct = material.curriculum_topic
                return (ct.chapter.grade.subject.order, ct.chapter.grade.order, ct.chapter.order, ct.order)

            match = re.match(r'^(\d+)', material.title)
            if match:
                return (999, 999, 999, int(match.group(1)))
            return (999, 999, 999, 99999)

        purchased_list.sort(key=get_number)
        context['purchased_materials'] = purchased_list

        # Бібліотека: окремі теми групуємо за курсом і класом (список уже відсортовано за деревом тем)
        library_groups = []
        for material in purchased_list:
            if material.is_bundle:
                continue
            grade = material.curriculum_grade
            label = grade.short_label if grade else 'Інші матеріали'
            if not library_groups or library_groups[-1]['label'] != label:
                library_groups.append({'label': label, 'materials': []})
            library_groups[-1]['materials'].append(material)
        context['library_groups'] = library_groups

        # Пакет сам не має контенту — показуємо його теми; посилання лише на ті, до яких є доступ
        owned_ids = {m.id for m in purchased_list}
        context['library_bundles'] = [
            {'bundle': bundle, 'topics': [{'material': m, 'owned': m.id in owned_ids}
                                          for m in sorted(bundle.included_materials.all(), key=get_number)]}
            for bundle in purchased_list if bundle.is_bundle
        ]

        context['form'] = UserProfileForm(instance=self.request.user)
        context['tutor_request'] = getattr(self.request.user, 'tutor_request', None)
        context['course_choices'] = TutorStudentRequest.COURSE_CHOICES
        context['personal_presentations'] = self.request.user.personal_presentations.all()
        # Діагностики — в окремому розділі нижче, тут лише практика тем
        context['my_attempts'] = PracticeAttempt.objects.filter(
            user=self.request.user
        ).exclude(material__title=DIAGNOSTIC_MATERIAL_TITLE).select_related('material').defer(
            'material__html_content').order_by('-created_at')[:15]

        # Діагностики: динаміка від разу до разу і що повторити за останньою
        diagnostics = list(user_diagnostics(self.request.user)[:10])
        labels = {}
        for i, attempt in enumerate(diagnostics):
            scope = diagnostic_scope(attempt)
            if scope not in labels:
                labels[scope] = scope_label(scope)
            attempt.scope_label = labels[scope]
            # Зміна — лише відносно попередньої діагностики за тими самими темами
            previous = next((d for d in diagnostics[i + 1:] if diagnostic_scope(d) == scope), None)
            attempt.change = attempt.get_percent() - previous.get_percent() if previous else None
        context['diagnostics'] = diagnostics
        if diagnostics:
            # Не стіна з усіх слабких тем, а 5 найслабших і матеріали саме до них
            weak = weak_topic_stats(diagnostic_stats(diagnostics[0].answers_json or {})[2])
            focus = weak[:5]
            context['diagnostic_weak_topics'] = focus
            context['diagnostic_more_weak'] = len(weak) - len(focus)
            context['diagnostic_recommendations'] = sorted(
                StudyMaterial.objects.filter(curriculum_topic__in=[s['topic'] for s in focus], is_published=True)
                .select_related('curriculum_topic').distinct(),
                key=lambda m: m.curriculum_topic.order)

        tutor_request = context['tutor_request']
        if tutor_request and tutor_request.status == 'approved':
            context['my_homeworks'] = homework.annotate(
                Homework.objects.filter(student=tutor_request).select_related('student', 'material', 'attempt')
                .defer('material__html_content')[:10])

        if is_teacher(self.request.user):
            context['attention'] = attention_list()
            context['homeworks'] = homework.annotate(
                Homework.objects.select_related('student', 'material', 'attempt')
                .defer('material__html_content')[:40])
            context['school_materials'] = sorted(
                (m for m in StudyMaterial.objects.filter(is_bundle=False, curriculum_topic__isnull=False)
                 .select_related('curriculum_topic__chapter__grade__subject').defer('html_content')
                 if practice.practice_profile(m)),
                key=lambda m: (m.curriculum_grade.subject.order, m.curriculum_grade.order,
                               m.curriculum_topic.chapter.order, m.curriculum_topic.order))
            context['default_due'] = timezone.localdate() + datetime.timedelta(days=7)
            context['special_materials'] = [m for m in context['school_materials']
                                            if m.curriculum_topic.kind in ('summary', 'diagnostic')]
            context['students_attempts'] = PracticeAttempt.objects.filter(
                user__tutor_request__status='approved'
            ).select_related('user', 'user__tutor_request', 'material').defer(
                'material__html_content').order_by('-created_at')[:50]
            context['my_students'] = TutorStudentRequest.objects.filter(status='approved').order_by('-created_at')
            context['nmt_materials'] = StudyMaterial.objects.filter(is_published=True).order_by('title')

            # ОНОВЛЕНО: Теми для звітів НУШ
            context['all_curriculum_topics'] = CurriculumTopic.objects.exclude(
                chapter__grade__subject__name="Підготовка до НМТ / ЗНО"
            ).select_related('chapter__grade').order_by('chapter__grade__subject__order', 'chapter__grade__order',
                                                        'chapter__order', 'order')

        return context

    def post(self, request, *args, **kwargs):
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('cabinet')

        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)


@login_required(login_url='/login/')
def download_material_view(request, material_id):
    material = get_object_or_404(StudyMaterial, id=material_id)

    if not request.user.purchased_materials.filter(id=material.id).exists() and not is_teacher(request.user):
        raise Http404("У вас немає доступу до цього матеріалу.")

    return render(request, 'materials/reader.html', {'material': material})


@api_view(['GET'])
def api_materials_list(request):
    materials = StudyMaterial.objects.filter(is_published=True).select_related('curriculum_topic')
    materials_list = list(materials)

    def get_number(material):
        match = re.match(r'^(\d+)', material.title)
        return int(match.group(1)) if match else 99999

    materials_list.sort(key=get_number)
    serializer = StudyMaterialSerializer(materials_list, many=True)
    return Response({
        'status': 'success',
        'materials': serializer.data
    })


@api_view(['GET'])
def api_bot_user_library(request, telegram_id):
    expected_token = getattr(settings, 'BOT_API_TOKEN', '') or ''
    provided_token = request.headers.get('X-Bot-Token', '')
    if not expected_token or not hmac.compare_digest(provided_token, expected_token):
        return Response({'status': 'error', 'message': 'Forbidden'}, status=403)

    user = User.objects.filter(telegram_id=telegram_id).first()

    if not user:
        return Response({'status': 'error', 'message': 'Учня не знайдено в базі платформи.'}, status=404)

    purchased = list(user.purchased_materials.all())

    def get_number(material):
        match = re.match(r'^(\d+)', material.title)
        return int(match.group(1)) if match else 99999

    purchased.sort(key=get_number)
    serializer = PurchasedMaterialSerializer(purchased, many=True)

    return Response({
        'status': 'success',
        'student_email': user.email,
        'library': serializer.data
    })


@login_required
@post_required('cart_detail')
@terms_required('/cart/')
def pay_from_balance(request):
    cart = get_object_or_404(Cart, user=request.user)

    if request.POST.get('agree') != 'on':
        messages.error(request, "Щоб перейти до оплати, поставте галочку про згоду з умовами "
                                "і з відкриттям матеріалів одразу після оплати.")
        return redirect('cart_detail')

    with transaction.atomic():
        user = User.objects.select_for_update().get(pk=request.user.pk)
        cart_items = list(cart.items.select_related('material').defer('material__html_content'))

        if not cart_items:
            messages.error(request, "Ваш кошик порожній.")
            return redirect('materials_list')

        total_price = cart.get_total_price()
        if user.balance < total_price:
            messages.error(request,
                           "На вашому балансі недостатньо коштів. Будь ласка, оберіть оплату карткою (Monobank).")
            return redirect('cart_detail')

        user.balance -= total_price
        user.save(update_fields=['balance'])

        order = Order.objects.create(
            user=user,
            total_amount=total_price,
            status='paid',
            paid_at=timezone.now(),
            mono_invoice_id='balance_payment',
            instant_access_agreed_at=timezone.now(),
        )

        for item in cart_items:
            if item.material.is_bundle:
                for sub_material in item.material.included_materials.all():
                    user.purchased_materials.add(sub_material)
            else:
                user.purchased_materials.add(item.material)

            OrderItem.objects.create(
                order=order,
                material=item.material,
                price=item.material.price
            )

        cart.items.all().delete()

    messages.success(request, f"Оплата пройшла успішно! Списано {total_price} ₴. Матеріали вже у вашому кабінеті. 🎉")
    return redirect('cabinet')


def send_telegram_notification(message):
    token = getattr(settings, 'TELEGRAM_BOT_TOKEN', '')
    chat_id = getattr(settings, 'TELEGRAM_ADMIN_ID', '')

    if token and chat_id:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'HTML'
        }
        try:
            response = requests.post(url, json=payload, timeout=5)
            if not response.ok:
                logger.warning("Telegram відхилив повідомлення: %s %s", response.status_code, response.text[:300])
        except Exception as e:
            logger.warning("Помилка відправки в Telegram: %s", e)


SITE_URL = "https://dokvadratu.com.ua"
MONO_API_URL = "https://api.monobank.ua/api/merchant"


def mono_headers():
    return {'X-Token': getattr(settings, 'MONOBANK_TOKEN', '') or '', 'Content-Type': 'application/json'}


def create_mono_invoice(order, amount_kopecks):
    payload = {
        "amount": amount_kopecks,
        "ccy": 980,
        "reference": str(order.id),
        "redirectUrl": f"{SITE_URL}{reverse('payment_result', args=[order.id])}",
        "webHookUrl": f"{SITE_URL}/mono/webhook/",
    }
    try:
        response = requests.post(f"{MONO_API_URL}/invoice/create", json=payload, headers=mono_headers(), timeout=15)
        data = response.json()
    except Exception:
        logger.exception("Не вдалося створити рахунок Monobank для замовлення #%s", order.id)
        return None

    if 'pageUrl' not in data:
        logger.error("Monobank не створив рахунок для замовлення #%s: %s", order.id, str(data)[:300])
        return None
    order.mono_invoice_id = data['invoiceId']
    order.save(update_fields=['mono_invoice_id'])
    return data['pageUrl']


@login_required
@post_required('cart_detail')
@terms_required('/cart/')
def pay_with_mono(request):
    cart = get_object_or_404(Cart, user=request.user)
    total_price = cart.get_total_price()

    if not cart.items.exists():
        messages.error(request, "Ваш кошик порожній.")
        return redirect('materials_list')

    if request.POST.get('agree') != 'on':
        messages.error(request, "Щоб перейти до оплати, поставте галочку про згоду з умовами "
                                "і з відкриттям матеріалів одразу після оплати.")
        return redirect('cart_detail')

    with transaction.atomic():
        order = Order.objects.create(
            user=request.user,
            total_amount=total_price,
            status='pending',
            instant_access_agreed_at=timezone.now(),
        )
        for item in cart.items.all():
            OrderItem.objects.create(order=order, material=item.material, price=item.material.price)

    page_url = create_mono_invoice(order, int(total_price * 100))
    if page_url:
        return redirect(page_url)
    messages.error(request, "Помилка платіжної системи. Спробуйте пізніше або спишіть з балансу.")
    return redirect('cart_detail')


@login_required
@terms_required('/cabinet/')
def topup_balance_view(request):
    if request.method == 'POST':
        amount = to_int(request.POST.get('amount'))
        if amount is None or not 1 <= amount <= 100000:
            messages.error(request, "Введіть коректну суму (ціле число гривень від 1 до 100 000).")
            return redirect('cabinet')

        order = Order.objects.create(
            user=request.user,
            total_amount=amount,
            status='pending',
            source='web'
        )

        page_url = create_mono_invoice(order, amount * 100)
        if page_url:
            return redirect(page_url)
        messages.error(request, "Помилка платіжної системи. Спробуйте пізніше.")
        return redirect('cabinet')

    return redirect('cabinet')


def apply_mono_status(invoice_id, status):
    msg = None
    with transaction.atomic():
        order = Order.objects.select_for_update().filter(mono_invoice_id=invoice_id).first()
        if order is None:
            return None
        email = html.escape(order.buyer_email)
        if order.user_id is None:
            if status == 'success' and order.status in ('pending', 'cancelled'):
                order.status = 'paid'
                order.paid_at = timezone.now()
                order.save(update_fields=['status', 'paid_at'])
                msg = (f"⚠️ <b>Оплата за замовленням видаленого акаунта</b>\nЗамовлення #{order.id}, {email}, "
                       f"{order.total_amount} ₴. Зв'яжіться з покупцем і за потреби поверніть кошти.")
            elif status in ('failure', 'expired') and order.status == 'pending':
                order.status = 'cancelled'
                order.save(update_fields=['status'])
            elif status == 'reversed' and order.status in ('pending', 'paid', 'cancelled'):
                order.status = 'refunded'
                order.save(update_fields=['status'])
        elif status == 'success' and order.status in ('pending', 'cancelled'):
            order.status = 'paid'
            order.paid_at = timezone.now()
            order.save(update_fields=['status', 'paid_at'])

            order_items = list(order.items.select_related('material').defer('material__html_content'))
            if order_items:
                materials = [item.material for item in order_items if item.material]
                for material in materials:
                    if material.is_bundle:
                        for sub_material in material.included_materials.all():
                            order.user.purchased_materials.add(sub_material)
                    else:
                        order.user.purchased_materials.add(material)

                CartItem.objects.filter(cart__user=order.user, material__in=materials).delete()
                msg = f"🛒 Нова покупка!\nУчень: {email}\nОплачено: {order.total_amount} ₴"
            else:
                User.objects.filter(pk=order.user_id).update(balance=F('balance') + int(order.total_amount))
                msg = f"💰 Нове поповнення!\nУчень: {email}\nСума: {order.total_amount} ₴"

        elif status in ('failure', 'expired') and order.status == 'pending':
            order.status = 'cancelled'
            order.save(update_fields=['status'])

        elif status == 'reversed' and order.status in ('pending', 'paid', 'cancelled'):
            was_paid = order.status == 'paid'
            order.status = 'refunded'
            order.save(update_fields=['status'])
            if was_paid:
                what = "матеріали з замовлення" if order.items.exists() else "суму поповнення з балансу"
                msg = (f"↩️ <b>Повернення коштів через Monobank</b>\nЗамовлення #{order.id}, {email}, "
                       f"{order.total_amount} ₴.\nАвтоматично нічого не змінено — за потреби заберіть {what} в адмінці.")

    if msg:
        send_telegram_notification(msg)
    return order


def check_mono_invoice(order):
    if not order.mono_invoice_id or order.mono_invoice_id == 'balance_payment':
        return order
    try:
        response = requests.get(f"{MONO_API_URL}/invoice/status", params={'invoiceId': order.mono_invoice_id},
                                headers=mono_headers(), timeout=10)
        response.raise_for_status()
        status = response.json().get('status')
    except Exception:
        logger.warning("Не вдалося перевірити статус рахунку Monobank для замовлення #%s", order.id, exc_info=True)
        return order
    return apply_mono_status(order.mono_invoice_id, status) or order


@login_required
def payment_result(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status in ('pending', 'cancelled'):
        order = check_mono_invoice(order)
    return render(request, 'materials/payment_result.html', {
        'order': order,
        'is_topup': not order.items.exists(),
    })


MONO_PUBKEY_URL = "https://api.monobank.ua/api/merchant/pubkey"
MONO_PUBKEY_CACHE_KEY = 'monobank_pubkey'
MONO_PUBKEY_REFRESHED_KEY = 'monobank_pubkey_refreshed'


class MonoPubKeyUnavailable(Exception):
    pass


def get_mono_pubkey(force_refresh=False):
    key = None if force_refresh else cache.get(MONO_PUBKEY_CACHE_KEY)
    if not key:
        try:
            response = requests.get(MONO_PUBKEY_URL, headers={'X-Token': getattr(settings, 'MONOBANK_TOKEN', '') or ''},
                                    timeout=10)
            response.raise_for_status()
            key = response.json()['key']
        except Exception as e:
            raise MonoPubKeyUnavailable(str(e))
        cache.set(MONO_PUBKEY_CACHE_KEY, key, 60 * 60 * 24)
        cache.set(MONO_PUBKEY_REFRESHED_KEY, True, 60 * 10)
    return key


def _signature_matches(pub_key_base64, signature, body):
    try:
        verifying_key = ecdsa.VerifyingKey.from_pem(base64.b64decode(pub_key_base64).decode())
        return verifying_key.verify(signature, body, sigdecode=ecdsa.util.sigdecode_der, hashfunc=hashlib.sha256)
    except Exception:
        return False


def verify_mono_signature(body, x_sign):
    if not x_sign:
        return False
    try:
        signature = base64.b64decode(x_sign, validate=True)
    except Exception:
        return False

    if _signature_matches(get_mono_pubkey(), signature, body):
        return True

    if cache.get(MONO_PUBKEY_REFRESHED_KEY):
        return False
    return _signature_matches(get_mono_pubkey(force_refresh=True), signature, body)


@csrf_exempt
def mono_webhook(request):
    if request.method != 'POST':
        return HttpResponse("Method not allowed", status=405)

    try:
        if not verify_mono_signature(request.body, request.headers.get('X-Sign', '')):
            return HttpResponse("Invalid signature", status=403)
    except MonoPubKeyUnavailable as e:
        logger.error("Webhook Monobank: не вдалося отримати ключ: %s", e)
        return HttpResponse("Temporary error", status=503)

    try:
        data = json.loads(request.body)
    except ValueError:
        return HttpResponse("Error", status=400)

    invoice_id = data.get('invoiceId')
    if invoice_id:
        apply_mono_status(invoice_id, data.get('status'))
    return HttpResponse("OK", status=200)


@login_required
def request_tutor_student_status(request):
    if request.method == 'POST':
        student_name = request.POST.get('real_name', '').strip()[:100]
        course_type = request.POST.get('course', 'nmt')

        if not student_name or course_type not in dict(TutorStudentRequest.COURSE_CHOICES):
            messages.error(request, "Будь ласка, заповніть усі поля форми.")
            return redirect('cabinet')

        student_req, created = TutorStudentRequest.objects.get_or_create(
            user=request.user,
            defaults={'real_name': student_name, 'course': course_type}
        )

        if created:
            course_display = dict(TutorStudentRequest.COURSE_CHOICES).get(course_type, course_type)
            messages.success(request, "Заявку успішно надіслано! Очікуйте на підтвердження.")
            msg = f"🙋‍♂️ <b>Нова заявка на статус учня!</b>\n\nУчень: <b>{html.escape(student_name)}</b>\nКлас/Курс: <b>{course_display}</b>\nEmail: {html.escape(request.user.email)}\n\nЧекає на твоє підтвердження в адмінці."
            send_telegram_notification(msg)

        elif student_req.status == 'pending':
            student_req.real_name = student_name
            student_req.course = course_type
            student_req.save()
            messages.info(request, "Вашу заявку оновлено. Вона вже розглядається.")

        elif student_req.status == 'approved':
            messages.info(request, "Ви вже є підтвердженим учнем.")

    return redirect('cabinet')


# ==========================================
# ВІДГУКИ
# ==========================================
def parse_rating(value):
    rating = to_int(value)
    return rating if rating in dict(Review.RATING_CHOICES) else None


@login_required
@post_required('cabinet')
def submit_review(request):
    rating = parse_rating(request.POST.get('rating', 5))
    text = request.POST.get('text', '').strip()
    reviewer_name = request.POST.get('reviewer_name', '').strip()[:100]
    material_id = request.POST.get('material_id')
    back_url = safe_back_url(request)

    if not text or not reviewer_name:
        messages.error(request, "Будь ласка, введіть своє ім'я та текст відгуку.")
        return redirect(back_url)
    if rating is None:
        messages.error(request, "Оберіть оцінку від 1 до 5.")
        return redirect(back_url)

    if rate_limit_exceeded(f'review:user:{request.user.pk}', limit=5, window=60 * 60):
        messages.error(request, "Ви вже надіслали кілька відгуків. Спробуйте пізніше.")
        return redirect(back_url)

    review = Review(
        user=request.user,
        reviewer_name=reviewer_name,
        rating=rating,
        text=text
    )

    material_title = "Загальний відгук (про заняття)"
    if material_id:
        material = get_object_or_404(StudyMaterial, id=to_int(material_id))
        review.material = material
        material_title = f"Матеріал: {material.title}"

    review.save()

    msg = (f"⭐️ <b>Новий відгук!</b>\n\nВід: {html.escape(reviewer_name)} ({html.escape(request.user.email)})\n"
           f"Оцінка: {'⭐' * rating}\nЩодо: {html.escape(material_title)}\n\n<i>«{html.escape(text)}»</i>\n\n"
           f"Перевір та схвали його в адмінці.")
    send_telegram_notification(msg)

    messages.success(request, "Дякуємо за ваш відгук! Він з'явиться на сайті після перевірки модератором.")
    return redirect(back_url)


@login_required(login_url='/login/')
def view_student_presentation(request, presentation_id):
    presentation = get_object_or_404(StudentPresentation, id=presentation_id)

    if presentation.student != request.user and not request.user.is_staff:
        raise Http404("У вас немає доступу до цієї презентації.")

    context = {
        'material': presentation,
        'is_personal': True
    }
    return render(request, 'materials/reader.html', context)


@login_required
def view_attempt_details(request, attempt_id):
    attempt = get_object_or_404(PracticeAttempt, id=attempt_id)

    if attempt.user != request.user and not is_teacher(request.user):
        raise Http404("У вас немає доступу до цієї статистики.")

    saved_answers = attempt.answers_json
    if not saved_answers:
        messages.info(request, "Цей тест був пройдений до оновлення системи. Деталі не збережено.")
        return redirect('cabinet')

    questions = questions_in_order(parse_id_list(saved_answers.get('question_ids', '')))

    mode = saved_answers.get('mode')
    if mode in practice.PROFILES:
        questions_by_id = {q.id: q for q in questions}
        results = practice.build_results(questions_by_id, saved_answers.get('history') or [], mode)[0]
        return render(request, 'materials/practice_school_results.html',
                      school_results_context(request, attempt, results))

    results_data = []
    for q in questions:
        q_result = {
            'question': q, 'type': q.question_type, 'is_correct': False,
            'user_answer': None, 'correct_answer': None, 'points_earned': 0, 'max_points': 0
        }

        if q.question_type == 'CHOICE':
            q_result['max_points'] = 1
            q_result['correct_answer'] = next((opt for opt in q.options.all() if opt.is_correct), None)
            user_ans = saved_answers.get('q_choice', {}).get(str(q.id))
            opt = find_option(q, user_ans)
            if opt:
                q_result['user_answer'] = opt
                if opt.is_correct:
                    q_result['points_earned'] = 1
                    q_result['is_correct'] = True

        elif q.question_type == 'MATCH':
            q_result['max_points'] = 3
            q_result['matches'] = []
            match_points = 0
            for item in q.match_items.all():
                user_match = saved_answers.get('q_match', {}).get(str(q.id), {}).get(str(item.id))
                user_opt = find_option(q, user_match)
                is_match_correct = user_opt is not None and user_opt.id == item.correct_option_id
                if is_match_correct:
                    match_points += 1
                q_result['matches'].append({
                    'item': item, 'user_option': user_opt,
                    'correct_option': item.correct_option, 'is_correct': is_match_correct
                })
            q_result['points_earned'] = match_points
            q_result['is_correct'] = (match_points == 3)

        elif q.question_type == 'SHORT':
            q_result['max_points'] = 2
            q_result['correct_answer'] = q.correct_short_answer
            user_ans = saved_answers.get('q_short', {}).get(str(q.id))
            q_result['user_answer'] = user_ans
            if user_ans:
                if short_answer_matches(user_ans, q.correct_short_answer):
                    q_result['points_earned'] = 2
                    q_result['is_correct'] = True

        results_data.append(q_result)

    context = {
        'material': attempt.material,
        'total_score': attempt.score,
        'max_score': attempt.max_score,
        'results_data': results_data,
    }
    return render(request, 'materials/practice_results.html', context)


@login_required
def report_question_error(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except ValueError:
            data = None
        if not isinstance(data, dict):
            return JsonResponse({'status': 'error', 'message': 'Некоректні дані'}, status=400)
        try:
            question_id = to_int(data.get('question_id'))
            message = str(data.get('message') or '').strip()[:2000]
            if not message:
                return JsonResponse({'status': 'error', 'message': 'Опишіть помилку'}, status=400)

            if rate_limit_exceeded(f'question-error:user:{request.user.pk}', limit=20, window=60 * 60):
                return JsonResponse({'status': 'error', 'message': 'Забагато скарг. Спробуйте пізніше.'}, status=429)

            question = get_object_or_404(Question, id=question_id)

            QuestionError.objects.create(
                question=question,
                user=request.user,
                message=message
            )

            msg = f"🚨 <b>СКАРГА НА ЗАВДАННЯ!</b>\n\n"
            msg += f"<b>ID Завдання:</b> {question.id}\n"
            msg += f"<b>Учень:</b> {html.escape(request.user.email)}\n\n"
            msg += f"<b>Що не так:</b> <i>{html.escape(message)}</i>\n\n"
            msg += f"Зайди в адмінку (розділ 'Скарги на завдання'), щоб виправити."

            send_telegram_notification(msg)

            return JsonResponse({'status': 'success'})
        except Http404:
            return JsonResponse({'status': 'error', 'message': 'Завдання не знайдено'}, status=404)
        except Exception:
            logger.exception("Помилка збереження скарги на завдання")
            return JsonResponse({'status': 'error', 'message': 'Не вдалося надіслати скаргу'}, status=400)
    return JsonResponse({'status': 'invalid method'}, status=405)


def parent_dashboard_view(request, parent_token):
    student_request = get_object_or_404(TutorStudentRequest, parent_token=parent_token, status='approved')

    presentations = StudentPresentation.objects.filter(student=student_request.user).order_by('-created_at')

    context = {
        'student': student_request,
        'presentations': presentations,
    }

    if student_request.course == 'nmt':
        attempts = (PracticeAttempt.objects.filter(user=student_request.user).select_related('material')
                    .defer('material__html_content').order_by('-created_at'))
        context['attempts'] = attempts
        context['is_nmt'] = True
        passed = list(parent_viewable_materials(student_request))

        def topic_number(material):
            match = re.match(r'^(\d+)', material.title)
            return int(match.group(1)) if match else 99999

        context['passed_materials'] = sorted(passed, key=topic_number)
    else:
        reports = StudentReport.objects.filter(student=student_request).order_by('-date')
        context['reports'] = reports
        context['is_nmt'] = False
        context['training'] = practice.topic_progress(
            PracticeAttempt.objects.filter(user=student_request.user).select_related('material')
            .defer('material__html_content'))
        diagnostic = next((a for a in PracticeAttempt.objects.filter(user=student_request.user)
                           .select_related('material').defer('material__html_content').order_by('-created_at')
                           if (a.answers_json or {}).get('kind') == 'diagnostic'), None)
        if diagnostic:
            context['diagnostic'] = diagnostic
            context['diagnostic_rows'] = topic_rows(diagnostic.answers_json.get('topic_map') or {})

    return render(request, 'materials/parent_dashboard.html', context)


def parent_viewable_materials(student_request):
    return (StudyMaterial.objects.filter(attempts__user_id=student_request.user_id)
            .filter(Q(is_published=True) | Q(id__in=student_request.user.purchased_materials.values('id')))
            .exclude(html_content__isnull=True).exclude(html_content='')
            .exclude(title=DIAGNOSTIC_MATERIAL_TITLE).distinct())


def parent_view_material(request, parent_token, material_id):
    student_request = get_object_or_404(TutorStudentRequest, parent_token=parent_token, status='approved',
                                        course='nmt')
    material = get_object_or_404(parent_viewable_materials(student_request), id=material_id)

    response = render(request, 'materials/reader.html', {
        'material': material,
        'is_personal': True,
        'back_url': reverse('parent_dashboard', args=[parent_token]),
    })
    response['Referrer-Policy'] = 'no-referrer'
    return response


def parent_view_presentation(request, parent_token, presentation_id):
    student_request = get_object_or_404(TutorStudentRequest, parent_token=parent_token, status='approved')
    presentation = get_object_or_404(StudentPresentation, id=presentation_id, student=student_request.user)

    context = {
        'material': presentation,
        'is_personal': True,
        'back_url': reverse('parent_dashboard', args=[parent_token]),
    }
    response = render(request, 'materials/reader.html', context)
    response['Referrer-Policy'] = 'no-referrer'
    return response


@login_required
@post_required('cabinet')
def add_quick_report(request):
    if not is_teacher(request.user):
        return redirect('cabinet')

    student = get_object_or_404(TutorStudentRequest, id=to_int(request.POST.get('student_id')))
    form = StudentReportForm(request.POST)
    if form.is_valid():
        report = form.save(commit=False)
        report.student = student
        report.save()
        messages.success(request, f"✅ Звіт для {student.real_name} успішно надіслано на дашборд!")
    else:
        errors = '; '.join(err for field_errors in form.errors.values() for err in field_errors)
        messages.error(request, f"Звіт не збережено: {errors}")
    return redirect('cabinet')


@login_required
@post_required('cabinet')
def add_nmt_score(request):
    if not is_teacher(request.user):
        return redirect('cabinet')

    student_req = get_object_or_404(TutorStudentRequest, id=to_int(request.POST.get('student_id')))
    material = get_object_or_404(StudyMaterial, id=to_int(request.POST.get('material_id')))
    score = to_int(request.POST.get('score'))
    max_score = to_int(request.POST.get('max_score', 18))

    if score is None or max_score is None or max_score <= 0 or not 0 <= score <= max_score:
        messages.error(request, "Бал має бути числом від 0 до максимуму, а максимум — більшим за 0.")
        return redirect('cabinet')

    PracticeAttempt.objects.create(
        user=student_req.user,
        material=material,
        score=score,
        max_score=max_score,
        answers_json={'note': 'Спільна робота на уроці (демонстрація екрана)'}
    )
    messages.success(request, f"✅ Результат роботи на уроці для {student_req.real_name} успішно додано!")
    return redirect('cabinet')


def submit_parent_review(request, parent_token):
    if request.method == 'POST':
        student_req = get_object_or_404(TutorStudentRequest, parent_token=parent_token, status='approved')

        rating = parse_rating(request.POST.get('rating', 5))
        text = request.POST.get('text', '').strip()
        reviewer_name = request.POST.get('reviewer_name', '').strip()[:100]

        if not text or not reviewer_name or rating is None:
            messages.error(request, "Будь ласка, введіть своє ім'я, оцінку та текст відгуку.")
            return redirect('parent_dashboard', parent_token=parent_token)

        if rate_limit_exceeded(f'parent-review:{student_req.pk}', limit=3, window=60 * 60):
            messages.error(request, "Ви вже надіслали кілька відгуків. Спробуйте пізніше.")
            return redirect('parent_dashboard', parent_token=parent_token)

        Review.objects.create(
            user=student_req.user,
            reviewer_name=reviewer_name,
            rating=rating,
            text=text
        )

        msg = f"⭐️ <b>Новий відгук від батьків!</b>\n\n"
        msg += f"Від: <b>{html.escape(reviewer_name)}</b> <i>(Батьки учня: {html.escape(student_req.real_name)})</i>\n"
        msg += f"Оцінка: {'⭐' * rating}\n\n"
        msg += f"<i>«{html.escape(text)}»</i>\n\n"
        msg += f"Зайди в адмінку, щоб схвалити публікацію на головній сторінці."

        send_telegram_notification(msg)

        messages.success(request, "Щиро дякуємо за ваш відгук! Ваша думка дуже важлива для нас.")

    return redirect('parent_dashboard', parent_token=parent_token)
SPRINT_MIN_QUESTIONS = 4
SPRINT_POOL = 40


@require_GET
def math_sprint_game(request):
  """Ігровий тренажер 'Математичний Спринт (60 секунд)'."""
  import random
  from django.shortcuts import render
  from .games import game_materials, topics_with_enough
  from .models import Question

  # Гра без нагород. Доступні теми залежать від ролі користувача
  available_materials, access_label = game_materials(request.user)

  # Спринт тренує швидкість у простих діях: беремо легкі завдання без рисунка, середні — лише якщо легких мало
  sprint_qs = Question.objects.filter(
      Q(svg_code__isnull=True) | Q(svg_code__regex=r'^\s*$'),
      Q(image__isnull=True) | Q(image=''),
      question_type='CHOICE', difficulty__lte=2,
  )

  # У списку лише теми, де вистачає завдань для гри
  available_materials = topics_with_enough(sprint_qs, available_materials, SPRINT_MIN_QUESTIONS)

  selected_material = None
  material_id = request.GET.get('material_id')
  if material_id and material_id.isdigit():
    selected_material = next((m for m in available_materials if m.id == int(material_id)), None)

  # Без доступних тем — лише усний рахунок, ніколи не весь банк (там і платні теми)
  scope = [selected_material] if selected_material else available_materials
  questions_list = []
  if scope:
    by_level = {}
    for q_id, level in sprint_qs.filter(materials__in=scope).values_list('id', 'difficulty').distinct():
      by_level.setdefault(level, set()).add(q_id)
    easy, medium = list(by_level.get(1, ())), list(by_level.get(2, ()))
    sampled_ids = random.sample(easy, min(len(easy), SPRINT_POOL))
    if len(sampled_ids) < SPRINT_POOL:
      sampled_ids += random.sample(medium, min(len(medium), SPRINT_POOL - len(sampled_ids)))

    scope_ids = {m.id for m in scope}
    qs = Question.objects.filter(id__in=sampled_ids).prefetch_related('options', 'materials')
    for q in qs:
      # Перевірка — у браузері (без нагород); id потрібні, щоб записати помилку в «Роботу над помилками»
      opts = [{'id': o.id, 'text': o.body, 'is_correct': o.is_correct} for o in q.options.all()]
      if len(opts) < 2 or sum(o['is_correct'] for o in opts) != 1:
        continue
      lesson = next((m for m in q.materials.all() if m.id in scope_ids), None)
      questions_list.append({
          'id': q.id,
          'text': q.text,
          'options': opts,
          'lesson_title': lesson.title if lesson else '',
          'lesson_url': reverse('material_detail', args=[lesson.id]) if lesson else '',
      })

  return render(
      request,
      'materials/math_sprint.html',
      {
          'available_materials': available_materials,
          'selected_material': selected_material,
          'access_label': access_label,
          'questions_list': questions_list,
          'autostart': request.GET.get('autostart') == '1',
      },
  )
