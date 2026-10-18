"""Шкільна практика (5–11 класи). Режим залежить від класу — як методичний профіль презентацій (docs/html_prompt.md):

* А (5–6 кл.) — «Тренажер»: завдання по одному, після помилки підказка і друга спроба;
* Б (7–9 кл.) — завдання по одному, після відповіді одразу розв'язання;
* В (10–11 кл.) — тест цілком, розбір у кінці.

Практика НМТ (матеріали курсу НМТ і матеріали без теми) лишається як була — у practice_session_view.

За кожним критерієм НУШ (моделювання, розв'язування, аналіз результатів) учень отримує окрему оцінку 1–12.
Правильні відповіді в сторінку не потрапляють: у покроковому режимі кожну відповідь перевіряє сервер
(practice_check_view), а спроби зберігаються в сесії, тож підсумок рахується з них, а не з того, що надішле браузер.
"""
import random

from django.db.models import Q
from django.utils.html import escape
from django.utils.safestring import mark_safe

from .games import record_game_answer, short_answer_matches
from .models import Question

PROFILES = {
    'A': {'size': 8, 'levels': (3, 3, 2), 'types': ('CHOICE', 'SHORT'), 'tries': 2, 'step_by_step': True,
          'title': 'Тренажер', 'button': '✏️ Тренажер'},
    'B': {'size': 10, 'levels': (4, 4, 2), 'types': ('CHOICE', 'SHORT', 'MATCH'), 'tries': 1, 'step_by_step': True,
          'title': 'Практика', 'button': '✏️ Практика'},
    'C': {'size': 12, 'levels': (4, 5, 3), 'types': ('CHOICE', 'SHORT', 'MATCH'), 'tries': 1, 'step_by_step': False,
          'title': 'Практика', 'button': '✏️ Практика'},
}
NMT_BUTTON = '🎯 Практика НМТ'

# Частка завдань на повторення попередніх тем того самого класу
REVIEW_SHARE = 0.2

POINTS = {'CHOICE': 2, 'SHORT': 2, 'MATCH': 3}
SKILLS = ('MODEL', 'SOLVE', 'ANALYZE')
SKILL_FIELDS = {'MODEL': 'nush_modeling', 'SOLVE': 'nush_solving', 'ANALYZE': 'nush_analysis'}
DEFAULT_HINT = 'Перечитай умову ще раз і перевір обчислення. Спробуй ще раз!'


def practice_profile(material):
    """'A', 'B' або 'C' для шкільної теми; None — практика НМТ."""
    if material.is_nmt:
        return None
    number = material.curriculum_grade.number or 0
    if 5 <= number <= 6:
        return 'A'
    if 7 <= number <= 9:
        return 'B'
    if 10 <= number <= 11:
        return 'C'
    return None


def practice_button_label(material):
    profile = practice_profile(material)
    return PROFILES[profile]['button'] if profile else NMT_BUTTON


def session_key(material):
    return f'school_practice_{material.id}'


# ---------- Добір завдань ----------

def question_pools(material, profile):
    """(завдання теми, завдання попередніх тем цього класу для повторення)."""
    topic = material.curriculum_topic
    chapter = topic.chapter
    base = (Question.objects.filter(question_type__in=PROFILES[profile]['types'])
            .prefetch_related('options', 'match_items'))
    own = list(base.filter(Q(curriculum_topic=topic) | Q(materials=material)).distinct())
    own_ids = {q.id for q in own}
    earlier = (Q(curriculum_topic__chapter__order__lt=chapter.order)
               | Q(curriculum_topic__chapter__order=chapter.order, curriculum_topic__order__lt=topic.order))
    review = [q for q in base.filter(earlier, curriculum_topic__chapter__grade=chapter.grade, difficulty__lte=2)
              if q.id not in own_ids]
    return own, review


def pick_balanced(pool, count, seen_ids):
    """Спершу ще не бачені завдання; у межах цього — по черзі з різних критеріїв, щоб були оцінки за всі три."""
    picked = []
    for group in ([q for q in pool if q.id not in seen_ids], [q for q in pool if q.id in seen_ids]):
        by_skill = {}
        for q in random.sample(group, len(group)):
            by_skill.setdefault(q.nush_skill, []).append(q)
        queues = [by_skill[s] for s in random.sample(sorted(by_skill), len(by_skill))]
        while len(picked) < count and any(queues):
            for queue in queues:
                if queue and len(picked) < count:
                    picked.append(queue.pop())
    return picked


def level_quotas(levels, total):
    quotas = list(levels)
    while sum(quotas) > total:
        quotas[quotas.index(max(quotas))] -= 1
    return quotas


def select_questions(material, profile, seen_ids):
    cfg = PROFILES[profile]
    own, review = question_pools(material, profile)
    n_review = min(len(review), round(cfg['size'] * REVIEW_SHARE))
    n_own = cfg['size'] - n_review

    picked = []
    for level, quota in zip((1, 2, 3), level_quotas(cfg['levels'], n_own)):
        picked += pick_balanced([q for q in own if q.difficulty == level], quota, seen_ids)
    # Якщо якогось рівня бракує — добираємо з решти завдань теми
    rest = [q for q in own if q not in picked]
    picked += pick_balanced(rest, n_own - len(picked), seen_ids)
    picked += pick_balanced(review, cfg['size'] - len(picked), seen_ids)

    random.shuffle(picked)
    picked.sort(key=lambda q: q.difficulty)  # від легшого до складнішого
    return picked


# ---------- Перевірка і оцінювання ----------

def answer_from_post(question, post):
    """Відповідь на одне завдання з форми тесту (режим В) — у тому ж вигляді, що й у покроковому режимі."""
    if question.question_type == 'MATCH':
        return {str(m.id): post.get(f'match_{m.id}', '') for m in question.match_items.all()}
    return post.get(f'q_{question.id}', '')


def clean_answer(question, raw):
    if question.question_type == 'MATCH':
        raw = raw if isinstance(raw, dict) else {}
        return {str(m.id): str(raw.get(str(m.id)) or '') for m in question.match_items.all()}
    return str(raw if raw is not None else '').strip()[:100]


def answer_points(question, answer):
    """Бали за одну спробу: варіант і коротка відповідь — 0 або 2, відповідність — по 1 за кожну пару."""
    if question.question_type == 'CHOICE':
        correct = next((o for o in question.options.all() if o.is_correct), None)
        return POINTS['CHOICE'] if correct and answer == str(correct.id) else 0
    if question.question_type == 'MATCH':
        return sum(1 for m in question.match_items.all() if answer.get(str(m.id)) == str(m.correct_option_id))
    return POINTS['SHORT'] if short_answer_matches(answer, question.correct_short_answer) else 0


def correct_answer(question):
    """Що показати як правильну відповідь (у сторінку потрапляє лише після останньої спроби)."""
    if question.question_type == 'CHOICE':
        correct = next((o for o in question.options.all() if o.is_correct), None)
        return {'option_id': str(correct.id) if correct else None}
    if question.question_type == 'MATCH':
        return {'pairs': {str(m.id): str(m.correct_option_id) for m in question.match_items.all()}}
    return {'answer': question.correct_short_answer}


def earned_points(question, tries, profile):
    """Зараховується перша спроба; у тренажері (А) правильна друга спроба дає половину балів."""
    if not tries:
        return 0
    max_points = POINTS[question.question_type]
    earned = answer_points(question, tries[0])
    if PROFILES[profile]['tries'] > 1 and earned < max_points and len(tries) > 1:
        if answer_points(question, tries[1]) == max_points:
            earned = max(earned, max_points // 2)
    return earned


def is_finished(question, tries, profile):
    if not tries:
        return False
    return len(tries) >= PROFILES[profile]['tries'] or answer_points(question, tries[-1]) == POINTS[question.question_type]


def nush_grade(earned, maximum):
    """Частка балів → оцінка 1–12 (0 балів — 1, усі бали — 12)."""
    if not maximum:
        return None
    return max(1, min(12, int(12 * earned / maximum + 0.5)))


def option_text(question, option_id):
    return next((o.body for o in question.options.all() if str(o.id) == str(option_id)), '')


def describe_answer(question, answer):
    """Відповідь учня для сторінки результатів. Тексти варіантів пише вчитель (у них бувають формули й теги),
    а коротку відповідь — учень, тож її екрануємо."""
    if question.question_type == 'CHOICE':
        return mark_safe(option_text(question, answer) or '—')
    if question.question_type == 'MATCH':
        texts = {str(o.id): o.text for o in question.options.all()}
        return mark_safe('; '.join(f'{m.text} → {texts.get(answer.get(str(m.id)), "—")}'
                                   for m in question.match_items.all()))
    return escape(answer) if answer else '—'


def describe_correct(question):
    if question.question_type == 'CHOICE':
        return mark_safe(option_text(question, correct_answer(question)['option_id']))
    if question.question_type == 'MATCH':
        return mark_safe('; '.join(f'{m.text} → {m.correct_option.text}' for m in question.match_items.all()))
    return mark_safe(question.correct_short_answer or '')


def build_results(questions, tries_by_id, profile):
    """Підсумок спроби: [(завдання, бали, …)], сума балів, максимум і оцінки за критеріями."""
    results, total, maximum = [], 0, 0
    by_skill = {skill: [0, 0] for skill in SKILLS}
    for q in questions:
        tries = [clean_answer(q, t) for t in tries_by_id.get(str(q.id), [])]
        max_points = POINTS[q.question_type]
        earned = earned_points(q, tries, profile)
        total += earned
        maximum += max_points
        skill = q.nush_skill if q.nush_skill in by_skill else 'SOLVE'
        by_skill[skill][0] += earned
        by_skill[skill][1] += max_points
        results.append({
            'question': q, 'earned': earned, 'max_points': max_points,
            'is_correct': earned == max_points, 'answered': bool(tries),
            'answers': [describe_answer(q, t) for t in tries],
            'correct_text': describe_correct(q),
        })
    grades = {SKILL_FIELDS[s]: nush_grade(e, m) for s, (e, m) in by_skill.items()}
    return results, total, maximum, grades


def record_mistakes(user, question, tries):
    """Для «Роботи над помилками»: завдання з помилкою в першій спробі стає помилкою учня."""
    if tries:
        record_game_answer(user, question,
                           answer_points(question, clean_answer(question, tries[0])) == POINTS[question.question_type])
