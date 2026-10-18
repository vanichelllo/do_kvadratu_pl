"""Шкільна практика (5–11 класи) «сходинками» — кожен учень іде у своєму темпі.

Три сходинки — це рівні складності завдань (1–3). Учень починає з першої. Дві правильні відповіді поспіль
з першої спроби піднімають на сходинку вище, дві помилки поспіль — опускають нижче. Практика закінчується,
коли учень пройшов третю сходинку (тему опановано), набралося MAX_TASKS завдань або учень сам натиснув
«Завершити». Незавершена практика зберігається (PracticeRun), її можна продовжити пізніше.

Режим залежить від класу — як методичний профіль презентацій (docs/html_prompt.md):
* А (5–6 кл.) — «Тренажер»: після помилки підказка і друга спроба;
* Б (7–9 кл.) і В (10–11 кл.) — одна спроба, після відповіді одразу розв'язання.
Практика НМТ (матеріали курсу НМТ і без теми) лишається як була — у practice_session_view.

Оцінка — окремо за кожним критерієм НУШ (моделювання, розв'язування, аналіз результатів) і залежить від того,
на якій сходинці учень упорався, а не від кількості розв'язаних завдань: найвища сходинка з правильною
відповіддю задає рівень (середній 4–6, достатній 7–9, високий 10–12), точність — оцінку в межах рівня.

Правильні відповіді в сторінку не потрапляють: кожну відповідь перевіряє сервер, а спроби зберігаються
в PracticeRun, тож підсумок рахується з них, а не з того, що надішле браузер.
"""
import random

from django.db.models import Q
from django.utils.html import escape
from django.utils.safestring import mark_safe

from .expr import expressions_equal
from .games import record_game_answer, short_answer_matches
from .models import PracticeAttempt, Question

CLASSIC_TYPES = ('CHOICE', 'SHORT', 'MATCH')
SCHOOL_TYPES = ('MULTI', 'TF', 'FIELDS', 'ERROR', 'ORDER', 'GROUP', 'EXPR', 'POINT', 'COORD')
ALL_TYPES = CLASSIC_TYPES + SCHOOL_TYPES

PROFILES = {
    'A': {'tries': 2, 'types': tuple(t for t in ALL_TYPES if t != 'MATCH'), 'title': 'Тренажер', 'button': '✏️ Тренажер'},
    'B': {'tries': 1, 'types': ALL_TYPES, 'title': 'Практика', 'button': '✏️ Практика'},
    'C': {'tries': 1, 'types': ALL_TYPES, 'title': 'Практика', 'button': '✏️ Практика'},
}
NMT_BUTTON = '🎯 Практика НМТ'

LEVELS = (1, 2, 3)
UP_STREAK = 2      # правильних поспіль, щоб піднятися на сходинку
DOWN_STREAK = 2    # помилок поспіль, щоб опуститися
MAX_TASKS = 20     # не більше завдань за один раз, щоб не втомлювати
REVIEW_EVERY = 5   # кожне 5-те завдання — повторення попередніх тем класу (якщо є)

SKILLS = ('MODEL', 'SOLVE', 'ANALYZE')
SKILL_FIELDS = {'MODEL': 'nush_modeling', 'SOLVE': 'nush_solving', 'ANALYZE': 'nush_analysis'}
LEVEL_BASE = {1: 4, 2: 7, 3: 10}   # нижня межа рівня НУШ для сходинки: середній, достатній, високий
DEFAULT_HINT = 'Перечитай умову ще раз і перевір обчислення. Спробуй ще раз!'

# Боси — необов'язковий виклик після «Тему опановано»: складність 4 — «Бос», 5 — «Ультра-бос» (лише після перемоги
# над босом). На оцінку й сходинки не впливають, поразка нічого не знижує; перемога дає трофей.
BOSS, ULTRA = 4, 5
BOSS_TRIES = {BOSS: 2, ULTRA: 1}
BOSS_NAMES = {BOSS: '⚔️ Бос', ULTRA: '👑 Ультра-бос'}
BOSS_HINT = 'Бос ще стоїть! Підказок не буде — перевір міркування й спробуй ще раз.'


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


def topic_kind(material):
    """'lesson', 'summary' (узагальнення розділу) або 'diagnostic' (діагностика за клас)."""
    return material.curriculum_topic.kind if material.curriculum_topic_id else 'lesson'


DIAGNOSTIC_MAX = 30   # завдань у діагностиці за клас


def practice_button_label(material):
    profile = practice_profile(material)
    return PROFILES[profile]['button'] if profile else NMT_BUTTON


# ---------- Сходинки ----------

def new_state(top_skills=(), kind='lesson', level=1):
    """top_skills — критерії, для яких у банку є завдання третьої сходинки: тему опановано, лише коли кожен
    з них розв'язано на третій сходинці (інакше сильний учень мав би оцінку лише за два критерії).
    level — сходинка, з якої почати (див. resume_level)."""
    return {'level': level, 'start_level': level, 'ok': 0, 'bad': 0, 'history': [], 'status': 'active',
            'top_skills': sorted(top_skills), 'kind': kind}


def resume_level(previous_state):
    """Тема йде кілька уроків і ДЗ: нова практика з тієї ж теми починається зі сходинки, на якій учень зупинився
    минулого разу (тему опановано — з третьої). Узагальнення й діагностика завжди починаються з початку."""
    if not previous_state or previous_state.get('kind', 'lesson') != 'lesson' or not previous_state.get('history'):
        return LEVELS[0]
    if previous_state.get('status') == 'mastered':
        return LEVELS[-1]
    return min(max(int(previous_state.get('level') or LEVELS[0]), LEVELS[0]), LEVELS[-1])


def max_tries(state, profile, entry=None):
    """Діагностика міряє, а не вчить: одна спроба навіть у тренажері 5–6 класів. Бос — 2 спроби, ультра-бос — 1."""
    if entry and entry.get('boss'):
        return BOSS_TRIES[entry['boss']]
    return 1 if state.get('kind') == 'diagnostic' else PROFILES[profile]['tries']


def current_entry(state):
    history = state.get('history') or []
    return history[-1] if history and not history[-1].get('done') else None


def question_pools(material, profile):
    """(завдання теми, завдання попередніх тем цього класу для повторення).
    Узагальнення бере завдання всіх тем розділу, діагностика — базові завдання всіх тем класу (без повторення)."""
    topic = material.curriculum_topic
    chapter = topic.chapter
    base = Question.objects.filter(question_type__in=PROFILES[profile]['types']).prefetch_related('options', 'match_items')
    if topic.kind == 'diagnostic':
        own = list(base.filter(curriculum_topic__chapter__grade=chapter.grade, curriculum_topic__kind='lesson',
                               difficulty__lte=2).select_related('curriculum_topic__chapter'))
        return own, []
    if topic.kind == 'summary':
        own = list(base.filter(Q(curriculum_topic__chapter=chapter) | Q(materials=material)).distinct())
    else:
        own = list(base.filter(Q(curriculum_topic=topic) | Q(materials=material)).distinct())
    own_ids = {q.id for q in own}
    earlier = (Q(curriculum_topic__chapter__order__lt=chapter.order)
               | Q(curriculum_topic__chapter__order=chapter.order, curriculum_topic__order__lt=topic.order))
    review = [q for q in base.filter(earlier, curriculum_topic__chapter__grade=chapter.grade) if q.id not in own_ids]
    return own, review


def pick(pool, history, seen_ids, level):
    """Спершу критерій, якого найменше було на цій сходинці (а за рівності — загалом), щоб критерії чергувались;
    серед них — ще не бачене учнем завдання."""
    def used(skill):
        return (sum(1 for e in history if e['skill'] == skill and e.get('difficulty', e['level']) == level),
                sum(1 for e in history if e['skill'] == skill))
    fewest = min(used(q.nush_skill) for q in pool)
    pool = [q for q in pool if used(q.nush_skill) == fewest]
    # В узагальненні розділу — ще й теми по черзі
    topic_used = {}
    for e in history:
        topic_used[e.get('topic')] = topic_used.get(e.get('topic'), 0) + 1
    rarest = min(topic_used.get(q.curriculum_topic_id, 0) for q in pool)
    pool = [q for q in pool if topic_used.get(q.curriculum_topic_id, 0) == rarest]
    unseen = [q for q in pool if q.id not in seen_ids]
    return random.choice(unseen or pool)


def top_skills(own):
    return {q.nush_skill for q in own if q.difficulty == LEVELS[-1]}


def next_question(state, own, review, seen_ids):
    """(завдання, чи це повторення попередньої теми) або (None, False), якщо завдань не лишилось."""
    used = {entry['qid'] for entry in state['history']}
    if state.get('plan') is not None:
        by_id = {q.id: q for q in own}
        return next(((by_id[i], False) for i in state['plan'] if i not in used and i in by_id), (None, False))
    level = state['level']
    if len(state['history']) % REVIEW_EVERY == REVIEW_EVERY - 1:
        old = [q for q in review if q.id not in used and q.difficulty <= level]
        if old:
            return pick(old, state['history'], seen_ids, level), True
    fresh = [q for q in own if q.id not in used and q.difficulty in LEVELS]   # боси — лише за викликом
    # Сходинка без нових завдань — беремо найближчу за складністю
    for distance in range(len(LEVELS)):
        for wanted in (level - distance, level + distance):
            pool = [q for q in fresh if q.difficulty == wanted]
            if pool:
                return pick(pool, state['history'], seen_ids, level), False
    return None, False


def start_task(state, question, review=False):
    # level — сходинка учня, difficulty — складність самого завдання (різняться, коли на сходинці скінчились завдання)
    entry = {'qid': question.id, 'level': state['level'], 'difficulty': question.difficulty,
             'skill': question.nush_skill, 'topic': question.curriculum_topic_id, 'tries': [], 'done': False}
    if review:
        entry['review_topic'] = question.curriculum_topic_id   # повторення попередньої теми
    if question.question_type == 'ORDER':
        perm = list(range(len(spec_of(question).get('items') or [])))
        while len(perm) > 1 and perm == sorted(perm):
            random.shuffle(perm)
        entry['perm'] = perm   # perm[позиція на екрані] = номер у правильному порядку
    state['history'].append(entry)
    return entry


def finish_task(state, question, entry):
    """Завдання завершене: рухаємо учня сходинками. Повертає, чи була перша спроба правильною.
    Завдання, розв'язане з підказкою вчителя на уроці, сходинок не рухає і в оцінку не йде."""
    entry['done'] = True
    if state.get('plan') is not None:   # діагностика: без сходинок, до кінця плану
        entry['first_ok'] = is_correct(question, entry['tries'][0])
        if len(state['history']) >= len(state['plan']):
            state['status'] = 'done'
        return entry['first_ok']
    if entry.get('assisted'):
        entry['first_ok'] = False
        if state['status'] == 'active' and len(state['history']) >= MAX_TASKS:
            state['status'] = 'limit'
        return False
    first_ok = entry['first_ok'] = is_correct(question, entry['tries'][0])
    if first_ok:
        state['ok'], state['bad'] = state['ok'] + 1, 0
        if state['ok'] >= UP_STREAK and state['level'] < LEVELS[-1]:
            state['ok'] = 0
            state['level'] += 1
        elif state['ok'] >= UP_STREAK:
            solved_on_top = {e['skill'] for e in state['history']
                             if e.get('difficulty') == LEVELS[-1] and e.get('done') and e.get('first_ok')}
            needed = set(state.get('top_skills') or [])
            if needed and needed <= solved_on_top:
                state['status'] = 'mastered'
    else:
        state['ok'], state['bad'] = 0, state['bad'] + 1
        if state['bad'] >= DOWN_STREAK and state['level'] > LEVELS[0]:
            state['bad'] = 0
            state['level'] -= 1
    if state['status'] == 'active' and len(state['history']) >= MAX_TASKS:
        state['status'] = 'limit'
    return first_ok


# ---------- Боси ----------

def next_boss(state):
    """Який бос зараз доступний: BOSS після опанування теми, ULTRA — після перемоги над босом; None — жодного."""
    if state.get('status') != 'mastered' or state.get('kind') == 'diagnostic' or current_entry(state):
        return None
    bosses = state.get('bosses') or {}
    if str(BOSS) not in bosses:
        return BOSS
    if bosses[str(BOSS)] == 'won' and str(ULTRA) not in bosses:
        return ULTRA
    return None


def boss_question(state, own, seen_ids, stage):
    used = {entry['qid'] for entry in state['history']}
    pool = [q for q in own if q.difficulty == stage and q.id not in used]
    return min(pool, key=lambda q: (q.id in seen_ids, random.random()), default=None)


def start_boss(state, question, stage):
    entry = start_task(state, question)
    entry['boss'] = stage
    return entry


def finish_boss(state, question, entry):
    """Бос завершений: перемога — якщо хоч одна спроба правильна. Сходинки й оцінка не змінюються."""
    entry['done'] = True
    won = any(is_correct(question, answer) for answer in entry['tries'])
    entry['first_ok'] = is_correct(question, entry['tries'][0])
    state.setdefault('bosses', {})[str(entry['boss'])] = 'won' if won else 'lost'
    return won


def boss_trophy(bosses):
    """Найвищий трофей за словником {'4': 'won'|'lost', '5': …}: ULTRA, BOSS або None."""
    bosses = bosses or {}
    return next((stage for stage in (ULTRA, BOSS) if bosses.get(str(stage)) == 'won'), None)


# ---------- Типи завдань ----------

def spec_of(question):
    return question.spec if isinstance(question.spec, dict) else {}


def max_points(question):
    return 3 if question.question_type == 'MATCH' else 2


def _number(value):
    try:
        number = float(str(value).replace(',', '.').replace('−', '-').strip())
    except (TypeError, ValueError):
        return None
    return number if abs(number) < 1e9 else None


def _int_list(raw, limit):
    if not isinstance(raw, list):
        return []
    values = []
    for item in raw[:50]:
        if isinstance(item, int) and not isinstance(item, bool) and 0 <= item < limit:
            values.append(item)
    return values


def clean_answer(question, raw, entry):
    """Відповідь учня в стабільному вигляді — так вона й зберігається в історії."""
    t, spec = question.question_type, spec_of(question)
    if t == 'MATCH':
        raw = raw if isinstance(raw, dict) else {}
        return {str(m.id): str(raw.get(str(m.id)) or '') for m in question.match_items.all()}
    if t == 'MULTI':
        return sorted(set(_int_list(raw, len(spec.get('options') or []))))
    if t == 'TF':
        raw = raw if isinstance(raw, list) else []
        return [raw[i] if i < len(raw) and isinstance(raw[i], bool) else None
                for i in range(len(spec.get('statements') or []))]
    if t == 'FIELDS':
        raw = raw if isinstance(raw, list) else []
        return [str(raw[i] if i < len(raw) and raw[i] is not None else '').strip()[:50]
                for i in range(len(spec.get('fields') or []))]
    if t == 'ERROR':
        values = _int_list([raw], len(spec.get('steps') or []))
        return values[0] if values else None
    if t == 'ORDER':
        # З екрана приходять позиції; зберігаємо номери в правильному порядку, щоб розбір не залежав від перемішування
        perm = entry.get('perm') or []
        positions = _int_list(raw, len(perm))
        return [perm[p] for p in positions] if sorted(positions) == list(range(len(perm))) else []
    if t == 'GROUP':
        groups = _int_list(raw, len(spec.get('groups') or []))
        return groups if len(groups) == len(spec.get('items') or []) else []
    if t == 'POINT':
        return _number(raw)
    if t == 'COORD':
        point = [_number(v) for v in raw] if isinstance(raw, list) and len(raw) == 2 else [None]
        return None if None in point else point
    return str(raw if raw is not None else '').strip()[:100]


def is_correct(question, answer):
    t, spec = question.question_type, spec_of(question)
    if t == 'CHOICE':
        correct = next((o for o in question.options.all() if o.is_correct), None)
        return bool(correct) and answer == str(correct.id)
    if t == 'SHORT':
        return short_answer_matches(answer, question.correct_short_answer)
    if t == 'MATCH':
        return all(answer.get(str(m.id)) == str(m.correct_option_id) for m in question.match_items.all())
    if t == 'MULTI':
        return answer == [i for i, (_, ok) in enumerate(spec.get('options') or []) if ok]
    if t == 'TF':
        return answer == [bool(ok) for _, ok in spec.get('statements') or []]
    if t == 'FIELDS':
        expected = [str(value) for _, value in spec.get('fields') or []]
        if len(answer) != len(expected):
            return False
        if spec.get('unordered'):
            remaining = list(expected)
            for value in answer:
                hit = next((e for e in remaining if short_answer_matches(value, e)), None)
                if hit is None:
                    return False
                remaining.remove(hit)
            return True
        return all(short_answer_matches(a, e) for a, e in zip(answer, expected))
    if t == 'ERROR':
        return answer is not None and answer == spec.get('wrong')
    if t == 'ORDER':
        return answer == list(range(len(spec.get('items') or [])))
    if t == 'GROUP':
        return answer == [group for _, group in spec.get('items') or []]
    if t == 'EXPR':
        return expressions_equal(answer, spec.get('answer', ''), spec.get('vars') or [])
    if t == 'POINT':
        tolerance = spec.get('tolerance', (spec.get('step') or 1) / 2 * 0.999)
        return answer is not None and abs(answer - float(spec.get('answer', 0))) <= tolerance
    if t == 'COORD':
        tolerance = spec.get('tolerance', 0.25)
        target = spec.get('answer') or [0, 0]
        return answer is not None and all(abs(a - float(b)) <= tolerance for a, b in zip(answer, target))
    return False


def answer_points(question, answer):
    """Бали за одну спробу: відповідність — по 1 за пару, решта — 2 за повністю правильну відповідь."""
    if question.question_type == 'MATCH':
        return sum(1 for m in question.match_items.all() if answer.get(str(m.id)) == str(m.correct_option_id))
    return 2 if is_correct(question, answer) else 0


def is_finished(question, tries, tries_allowed):
    return bool(tries) and (len(tries) >= tries_allowed or is_correct(question, tries[-1]))


def earned_points(question, tries, profile):
    """Зараховується перша спроба; у тренажері (А) правильна друга спроба дає половину балів."""
    if not tries:
        return 0
    earned = answer_points(question, tries[0])
    if PROFILES[profile]['tries'] > 1 and len(tries) > 1 and is_correct(question, tries[1]):
        earned = max(earned, max_points(question) // 2)
    return earned


def public_spec(question, entry):
    """Що потрібно сторінці, щоб показати завдання, — без правильних відповідей."""
    t, spec = question.question_type, spec_of(question)
    if t == 'MULTI':
        options = list(enumerate(text for text, _ in spec.get('options') or []))
        random.shuffle(options)
        return {'options': options}
    if t == 'TF':
        return {'statements': [text for text, _ in spec.get('statements') or []]}
    if t == 'FIELDS':
        return {'labels': [label for label, _ in spec.get('fields') or []]}
    if t == 'ERROR':
        return {'steps': spec.get('steps') or []}
    if t == 'ORDER':
        items = spec.get('items') or []
        return {'items': [items[i] for i in entry.get('perm') or []]}
    if t == 'GROUP':
        return {'groups': spec.get('groups') or [], 'items': [text for text, _ in spec.get('items') or []]}
    if t == 'EXPR':
        return {'vars': spec.get('vars') or []}
    if t == 'POINT':
        return {key: spec.get(key) for key in ('min', 'max', 'step')}
    if t == 'COORD':
        return {key: spec.get(key) for key in ('xmin', 'xmax', 'ymin', 'ymax', 'step')}
    return {}


def reveal(question, entry):
    """Правильна відповідь у тому ж вигляді, що й public_spec, — лише після останньої спроби."""
    t, spec = question.question_type, spec_of(question)
    if t == 'CHOICE':
        correct = next((o for o in question.options.all() if o.is_correct), None)
        return {'option_id': str(correct.id) if correct else None}
    if t == 'MATCH':
        return {'pairs': {str(m.id): str(m.correct_option_id) for m in question.match_items.all()}}
    if t == 'SHORT':
        return {'answer': question.correct_short_answer}
    if t == 'MULTI':
        return {'expected': [i for i, (_, ok) in enumerate(spec.get('options') or []) if ok]}
    if t == 'TF':
        return {'expected': [bool(ok) for _, ok in spec.get('statements') or []]}
    if t == 'FIELDS':
        return {'expected': [str(value) for _, value in spec.get('fields') or []]}
    if t == 'ERROR':
        return {'expected': spec.get('wrong')}
    if t == 'ORDER':
        perm = entry.get('perm') or []
        return {'expected': [perm.index(i) for i in range(len(perm))]}   # позиції на екрані в правильному порядку
    if t == 'GROUP':
        return {'expected': [group for _, group in spec.get('items') or []]}
    if t == 'EXPR':
        return {'answer': spec.get('answer', '')}
    if t in ('POINT', 'COORD'):
        return {'answer': spec.get('answer')}
    return {}


# ---------- Розбір відповідей ----------

def _fmt_number(value):
    return f'{value:g}'.replace('.', ',').replace('-', '−') if isinstance(value, (int, float)) else '—'


def describe(question, answer):
    """Відповідь текстом для сторінки результатів. Тексти завдання пише вчитель (у них бувають формули й теги),
    а введене учнем екрануємо."""
    t, spec = question.question_type, spec_of(question)
    if answer in (None, '', [], {}):
        return '—'
    if t == 'CHOICE':
        return mark_safe(next((o.body for o in question.options.all() if str(o.id) == str(answer)), '—'))
    if t == 'MATCH':
        texts = {str(o.id): o.text for o in question.options.all()}
        return mark_safe('; '.join(f'{m.text} → {texts.get(answer.get(str(m.id)), "—")}'
                                   for m in question.match_items.all()))
    if t == 'MULTI':
        options = spec.get('options') or []
        return mark_safe('; '.join(options[i][0] for i in answer if i < len(options)))
    if t == 'TF':
        words = {True: 'так', False: 'ні', None: '?'}
        return mark_safe('; '.join(f'{text} — {words[a]}' for (text, _), a in zip(spec.get('statements') or [], answer)))
    if t == 'FIELDS':
        return mark_safe('; '.join(f'{label} {escape(a) or "—"}' for (label, _), a in zip(spec.get('fields') or [], answer)))
    if t == 'ERROR':
        return f'крок {answer + 1}'
    if t == 'ORDER':
        items = spec.get('items') or []
        return mark_safe(' → '.join(items[i] for i in answer if i < len(items)))
    if t == 'GROUP':
        groups = spec.get('groups') or []
        return mark_safe('; '.join(f'{text} → {groups[g] if g < len(groups) else "?"}'
                                   for (text, _), g in zip(spec.get('items') or [], answer)))
    if t == 'POINT':
        return _fmt_number(answer)
    if t == 'COORD':
        return f'({_fmt_number(answer[0])}; {_fmt_number(answer[1])})'
    return escape(answer)


def describe_correct(question):
    t, spec = question.question_type, spec_of(question)
    if t == 'SHORT':
        return mark_safe(question.correct_short_answer or '')
    if t == 'EXPR':
        return mark_safe(spec.get('answer', ''))
    if t == 'MATCH':
        return mark_safe('; '.join(f'{m.text} → {m.correct_option.text}' for m in question.match_items.all()))
    if t == 'CHOICE':
        return describe(question, reveal(question, {})['option_id'])
    if t == 'FIELDS':
        return mark_safe('; '.join(f'{label} {value}' for label, value in spec.get('fields') or []))
    if t == 'ORDER':
        return describe(question, list(range(len(spec.get('items') or []))))
    if t == 'POINT':
        return _fmt_number(float(spec.get('answer', 0)))
    if t == 'COORD':
        return describe(question, [float(v) for v in spec.get('answer') or [0, 0]])
    return describe(question, reveal(question, {})['expected'])


# ---------- Підсумок ----------

def skill_grade(tasks):
    """tasks — [(складність завдання, правильно з першої спроби, правильно хоч з другої, хоч щось правильно)].
    None — завдань цього критерію не було."""
    if not tasks:
        return None
    top = max((level for level, _, solved, _ in tasks if solved), default=0)
    if top == 0:
        return 2 if any(partial for *_, partial in tasks) else 1   # початковий рівень
    accuracy = sum(1 for _, first, _, _ in tasks if first) / len(tasks)
    return min(12, LEVEL_BASE[top] + round(2 * accuracy))


def build_results(questions_by_id, history, profile):
    """Розбір спроби: завдання з балами, сума балів, максимум і оцінки за критеріями."""
    results, total, maximum = [], 0, 0
    by_skill = {skill: [] for skill in SKILLS}
    for entry in history:
        q = questions_by_id.get(entry['qid'])
        tries = entry.get('tries') or []
        if q is None or not tries:
            continue
        if entry.get('assisted'):
            results.append({'question': q, 'level': entry.get('difficulty', q.difficulty), 'earned': 0, 'max_points': 0,
                            'is_correct': False, 'assisted': True, 'answers': [describe(q, t) for t in tries],
                            'correct_text': describe_correct(q)})
            continue
        earned = earned_points(q, tries, profile)
        first = is_correct(q, tries[0])
        solved = any(is_correct(q, t) for t in tries)
        total += earned
        maximum += max_points(q)
        difficulty = entry.get('difficulty', q.difficulty)
        by_skill[entry['skill'] if entry['skill'] in by_skill else 'SOLVE'].append((difficulty, first, solved, earned > 0))
        results.append({
            'question': q, 'level': difficulty, 'earned': earned, 'max_points': max_points(q),
            'is_correct': earned == max_points(q), 'answers': [describe(q, t) for t in tries], 'correct_text': describe_correct(q),
        })
    grades = {SKILL_FIELDS[s]: skill_grade(tasks) for s, tasks in by_skill.items()}
    return results, total, maximum, grades


def record_mistake(user, question, first_ok):
    """«Робота над помилками» вміє лише класичні типи — нові туди не потрапляють."""
    if question.question_type in CLASSIC_TYPES:
        record_game_answer(user, question, first_ok)


# ---------- Для батьків: тренування — це рівень і динаміка, а не бали ----------

LEVEL_BANDS = ((3, 'початковий'), (6, 'середній'), (9, 'достатній'), (12, 'високий'))


def level_band(grade):
    """Номер рівня НУШ (0–3) для оцінки 1–12."""
    return next(i for i, (top, _) in enumerate(LEVEL_BANDS) if grade <= top)


def level_name(grade):
    return LEVEL_BANDS[level_band(grade)][1] if grade else None


def overall_grade(attempt):
    grades = [g for _, g in attempt.nush_grades if g]
    return round(sum(grades) / len(grades)) if grades else None


def topic_progress(attempts):
    """Тренування по темах: скільки разів, рівень на першій і останній спробі, рівні за критеріями зараз.
    Перша спроба — чесна відправна точка, далі показуємо, як рівень зріс."""
    by_material = {}
    for attempt in sorted(attempts, key=lambda a: a.created_at):
        if (attempt.answers_json or {}).get('mode') in PROFILES and overall_grade(attempt):
            by_material.setdefault(attempt.material_id, []).append(attempt)
    rows = []
    for items in by_material.values():
        first, last = items[0], items[-1]
        first_grade, last_grade = overall_grade(first), overall_grade(last)
        rows.append({
            'material': last.material, 'count': len(items), 'date': last.created_at,
            'first': level_name(first_grade), 'last': level_name(last_grade),
            'grew': level_band(last_grade) > level_band(first_grade),
            'fell': level_band(last_grade) < level_band(first_grade),
            'criteria': [(name, level_name(g)) for name, g in last.nush_grades if g],
            'mastered': any((a.answers_json or {}).get('status') == 'mastered' for a in items),
            'trophy': BOSS_NAMES.get(max((boss_trophy((a.answers_json or {}).get('bosses')) or 0 for a in items))),
        })
    rows.sort(key=lambda row: row['date'], reverse=True)
    return rows


# ---------- Сигнали: застряг, прогалини ----------

STUCK_AFTER = 8   # стільки завдань без жодного правильного вище першої сходинки — учень застряг


def is_stuck(history):
    """Учень довго не може піднятися з першої сходинки."""
    counted = [e for e in history if e.get('tries') and not e.get('assisted')]
    return len(counted) >= STUCK_AFTER and not any(e.get('first_ok') and e.get('difficulty', 1) >= 2 for e in counted)


def gap_topics(history):
    """Попередні теми, на завданнях повторення з яких учень помилився з першої спроби."""
    topics = []
    for e in history:
        topic = e.get('review_topic')
        if topic and e.get('tries') and not e.get('first_ok') and not e.get('assisted') and topic not in topics:
            topics.append(topic)
    return topics


def recalculate_attempts(question):
    """Після виправлення завдання (хибна правильна відповідь у банку) перерахувати бали й оцінки шкільних спроб,
    у яких воно траплялося. Шлях сходинками не змінюється — лише те, що зараховано. Повертає кількість спроб."""
    changed = 0
    candidates = PracticeAttempt.objects.filter(answers_json__question_ids__icontains=str(question.id))
    for attempt in candidates:
        saved = attempt.answers_json or {}
        history = saved.get('history') or []
        if saved.get('mode') not in PROFILES or not any(e.get('qid') == question.id for e in history):
            continue
        ids = {e['qid'] for e in history}
        questions_by_id = {q.id: q for q in Question.objects.filter(id__in=ids).prefetch_related('options', 'match_items')}
        _, total, maximum, grades = build_results(questions_by_id, history, saved['mode'])
        for entry in history:
            q = questions_by_id.get(entry['qid'])
            if q is not None and entry.get('tries') and not entry.get('assisted'):
                entry['first_ok'] = is_correct(q, entry['tries'][0])
        attempt.score, attempt.max_score = total, maximum
        for field, grade in grades.items():
            setattr(attempt, field, grade)
        attempt.save(update_fields=['score', 'max_score', 'answers_json', *grades])
        changed += 1
    return changed


# ---------- Діагностика за клас ----------

def diagnostic_plan(own, seen_ids):
    """По одному-два базових завдання з кожної теми класу в порядку програми (не більше DIAGNOSTIC_MAX)."""
    by_topic = {}
    for q in own:
        by_topic.setdefault(q.curriculum_topic, []).append(q)
    topics = sorted(by_topic, key=lambda t: (t.chapter.order, t.order))
    per_topic = 2 if len(topics) * 2 <= DIAGNOSTIC_MAX else 1
    plan = []
    for topic in topics[:DIAGNOSTIC_MAX]:
        pool = sorted(by_topic[topic], key=lambda q: (q.id in seen_ids, q.difficulty, random.random()))
        plan += [q.id for q in pool[:per_topic]]
    return plan[:DIAGNOSTIC_MAX]


def topic_map(history):
    """{тема: [правильно з першої спроби, усього]} — розклад узагальнення чи діагностики по темах."""
    result = {}
    for e in history:
        if e.get('tries') and not e.get('assisted') and e.get('topic'):
            row = result.setdefault(str(e['topic']), [0, 0])
            row[0] += 1 if e.get('first_ok') else 0
            row[1] += 1
    return result

