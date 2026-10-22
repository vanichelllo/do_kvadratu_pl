"""Ігри-тренажери: «Пари» (відповідності), «Без варіантів» (коротка відповідь) і «Робота над помилками».

Відповіді перевіряє сервер (game_answer), тож у сторінку правильні відповіді не потрапляють. Нагород немає;
для учня, що увійшов, кожна відповідь оновлює список його помилок (GameMistake)."""
import json
import random
import re
from fractions import Fraction

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET, require_POST

from .models import GameMistake, Question, StudyMaterial
from .teachers import licensed_grade_ids


def game_materials(user):
    """Теми, завдання з яких можна давати в іграх цьому користувачеві, і підпис для списку тем."""
    if user.is_authenticated and (user.is_staff or user.is_superuser):
        return StudyMaterial.objects.filter(is_bundle=False), 'Повний доступ викладача'
    # Як у практиці: безкоштовна тема — лише опублікована, куплена — завжди; репетитор — класи своєї підписки
    free = Q(is_free=True, is_published=True)
    if user.is_authenticated:
        licensed = Q(curriculum_topic__chapter__grade_id__in=licensed_grade_ids(user) or [])
        return (StudyMaterial.objects.filter(free | licensed | Q(id__in=user.purchased_materials.values('id')),
                                             is_bundle=False),
                'Ваші відкриті та безкоштовні теми')
    return StudyMaterial.objects.filter(free, is_bundle=False), 'Безкоштовні демо-теми'


def topics_with_enough(questions, materials, minimum):
    """Лише теми, де для гри є щонайменше minimum завдань, — щоб гра не підміняла тему чимось іншим."""
    counts = dict(questions.filter(materials__in=materials).values('materials')
                  .annotate(n=Count('id', distinct=True)).values_list('materials', 'n'))
    return [m for m in materials if counts.get(m.id, 0) >= minimum]


def pick_material(request, materials):
    material_id = request.GET.get('material_id', '')
    return next((m for m in materials if material_id.isdigit() and m.id == int(material_id)), None)


def sample_by_difficulty(questions, size):
    """Спершу легші завдання; складніші добираємо, лише якщо легших замало."""
    by_level = {}
    for q_id, level in questions.values_list('id', 'difficulty').distinct():
        by_level.setdefault(level, []).append(q_id)
    picked = []
    for level in sorted(by_level):
        ids = by_level[level]
        picked += random.sample(ids, min(len(ids), size - len(picked)))
        if len(picked) >= size:
            break
    return picked


def question_payload(question, lesson=None):
    """Завдання для сторінки гри — без позначок правильності."""
    data = {'id': question.id, 'type': question.question_type, 'text': question.text,
            'svg': question.svg_code or '', 'image': question.image.url if question.image else '',
            'lesson_title': lesson.title if lesson else '',
            'lesson_url': lesson.get_absolute_url() if lesson else ''}
    if question.question_type == 'CHOICE':
        data['options'] = [{'id': o.id, 'text': o.body} for o in question.options.all()]
    elif question.question_type == 'MATCH':
        data['options'] = [{'id': o.id, 'text': o.text} for o in question.options.all()]
        data['items'] = [{'id': m.id, 'text': m.text} for m in question.match_items.all()]
    return data


def payload_list(question_ids, lessons_from):
    lesson_ids = {m.id for m in lessons_from}
    questions = (Question.objects.filter(id__in=question_ids)
                 .prefetch_related('options', 'match_items', 'materials'))
    result = []
    for q in questions:
        lesson = next((m for m in q.materials.all() if m.id in lesson_ids), None)
        result.append(question_payload(q, lesson))
    random.shuffle(result)
    return result


# Мішане число «2 3/5» (ціла частина, пробіл, дріб) — це 2 + 3/5, а не 23/5
MIXED_NUMBER = re.compile(r'^\s*([-−]?)\s*(\d+)\s+(\d+)\s*/\s*(\d+)\s*$')


def _number(text):
    mixed = MIXED_NUMBER.match(text)
    if mixed:
        sign, whole, num, den = mixed.groups()
        if int(den) == 0:
            return None
        value = int(whole) + Fraction(int(num), int(den))
        return -value if sign else value
    text = text.strip().replace(' ', '').replace(',', '.').replace('−', '-')
    try:
        return Fraction(text)
    except (ValueError, ZeroDivisionError):
        return None


# Одиниці виміру, які учні дописують до числа: «5 см», «12 кг», «30 %» — та сама відповідь, що й «5»
UNIT_SUFFIX = re.compile(r'^\s*(.*?\d)\s*(?:мм|см|дм|км|м|мг|кг|г|т|мл|л|с|хв|год|грн|коп|шт|%|°)\.?[²³23]?\s*$')


def short_answer_matches(answer, correct):
    """«0,5», «0.50» і «1/2» — та сама відповідь; «5 см» зараховується як «5»; нечислові — порівнюємо як текст."""
    answer, correct = str(answer or '').strip(), str(correct or '').strip()
    if not answer:
        return False
    a, c = _number(answer), _number(correct)
    if a is None and c is not None:
        unit = UNIT_SUFFIX.match(answer)
        a = _number(unit.group(1)) if unit else None
    if a is not None and c is not None:
        return a == c
    return answer.replace(',', '.').replace(' ', '').lower() == correct.replace(',', '.').replace(' ', '').lower()


def record_game_answer(user, question, is_correct):
    """Помилка — завдання потрапляє в «Роботу над помилками»; правильні відповіді поспіль його звідти прибирають."""
    if not user.is_authenticated:
        return
    if not is_correct:
        mistake, created = GameMistake.objects.get_or_create(user=user, question=question)
        if not created:
            mistake.correct_streak = 0
            mistake.save(update_fields=['correct_streak', 'updated_at'])
        return
    mistake = GameMistake.objects.filter(user=user, question=question).first()
    if mistake:
        mistake.correct_streak += 1
        if mistake.correct_streak >= GameMistake.MASTERED_STREAK:
            mistake.delete()
        else:
            mistake.save(update_fields=['correct_streak', 'updated_at'])


def check_answer(question, data):
    """(чи правильно, що показати як правильну відповідь)."""
    if question.question_type == 'CHOICE':
        correct = next((o for o in question.options.all() if o.is_correct), None)
        chosen = str(data.get('option_id', ''))
        return (correct is not None and chosen == str(correct.id)), {'option_id': correct.id if correct else None}
    if question.question_type == 'MATCH':
        pairs = {str(k): str(v) for k, v in (data.get('pairs') or {}).items()}
        expected = {str(m.id): str(m.correct_option_id) for m in question.match_items.all()}
        return pairs == expected, {'pairs': expected}
    return short_answer_matches(data.get('answer'), question.correct_short_answer), \
        {'answer': question.correct_short_answer}


@require_POST
def game_answer(request):
    try:
        data = json.loads(request.body)
        question_id = int(data.get('question_id'))
    except (ValueError, TypeError, json.JSONDecodeError):
        return JsonResponse({'error': 'bad request'}, status=400)
    question = get_object_or_404(Question.objects.prefetch_related('options', 'match_items'), id=question_id)

    # Відповідь видаємо лише на завдання, яке учень може бачити: з доступної теми або зі своїх помилок
    materials, _ = game_materials(request.user)
    allowed = question.materials.filter(id__in=materials.values('id')).exists() or (
        request.user.is_authenticated and GameMistake.objects.filter(user=request.user, question=question).exists())
    if not allowed:
        raise Http404

    is_correct, solution = check_answer(question, data)
    record_game_answer(request.user, question, is_correct)
    return JsonResponse({'correct': is_correct, **solution})


GAMES = {
    'pairs': {
        'title': '🧩 Пари',
        'intro': "З'єднай кожну умову (1–3) з відповіддю (А–Д): натисни умову, потім відповідь. "
                 "Так виглядають завдання на відповідність у НМТ.",
        'round': 5, 'minimum': 2,
    },
    'input': {
        'title': '✍️ Без варіантів',
        'intro': 'Варіантів немає — введи відповідь сам. Вгадати не вийде, тож це чесна перевірка вміння. '
                 'Дробову відповідь пиши через кому або крапку.',
        'round': 10, 'minimum': 3,
    },
}


def _round_page(request, mode, questions):
    game = GAMES[mode]
    all_materials, access_label = game_materials(request.user)
    materials = topics_with_enough(questions, all_materials, game['minimum'])
    selected = pick_material(request, materials)
    scope = [selected] if selected else materials
    items = payload_list(sample_by_difficulty(questions.filter(materials__in=scope), game['round']),
                         scope) if scope else []
    return render(request, 'materials/game_round.html', {
        'game': game, 'mode': mode, 'questions': items, 'available_materials': materials,
        'selected_material': selected, 'access_label': access_label,
    })


@require_GET
def game_pairs(request):
    return _round_page(request, 'pairs', Question.objects.filter(question_type='MATCH'))


@require_GET
def game_input(request):
    return _round_page(request, 'input', Question.objects.filter(question_type='SHORT'))


@require_GET
@login_required
def game_mistakes(request):
    mistakes = request.user.game_mistakes.all()
    total = mistakes.count()
    ids = list(mistakes.values_list('question_id', flat=True)[:10])
    return render(request, 'materials/game_round.html', {
        'game': {'title': '🔁 Робота над помилками',
                 'intro': 'Тут завдання, у яких ти помилявся в практиці та іграх. Завдання зникає зі списку, '
                          f'коли відповіси на нього правильно {GameMistake.MASTERED_STREAK} рази поспіль '
                          '(у різних раундах).'},
        'mode': 'mistakes', 'questions': payload_list(ids, game_materials(request.user)[0]), 'mistakes_total': total,
    })


@require_GET
def game_hub(request):
    mistakes_total = request.user.game_mistakes.count() if request.user.is_authenticated else 0
    return render(request, 'materials/game_hub.html', {'mistakes_total': mistakes_total})
