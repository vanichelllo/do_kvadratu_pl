TOPIC_NAME = "1.5. Тотожні перетворення раціональних виразів"
COURSE = "Алгебра (7-9 класи)"
GRADE = "8 клас"

TASKS = [
    # ==========================================
    # СХОДИНКА 1 — БАЗОВИЙ
    # ==========================================
    # --- Моделювання ---
    {
        "type": "CHOICE", "difficulty": 1, "skill": "MODEL",
        "text": r"Яку дію виконують першою у виразі $\frac{a}{b} + \frac{c}{d} \cdot \frac{m}{n}$?",
        "options": [(r"Множення", True), (r"Додавання", False), (r"Зліва направо — спершу додавання", False), (r"Порядок не важливий", False)],
        "hint": r"Порядок дій — як із числами: множення раніше за додавання.",
        "solution": r"Спершу $\frac{c}{d} \cdot \frac{m}{n}$, потім додаємо $\frac{a}{b}$.",
    },
    {
        "type": "TF", "difficulty": 1, "skill": "MODEL",
        "text": r"Правда чи ні?",
        "statements": [
            (r"Рівність $\frac{x^2 - 1}{x - 1} = x + 1$ — тотожність при $x \ne 1$", True),
            (r"Рівність, правильна при $x = 2$, обов'язково є тотожністю", False),
            (r"Тотожне перетворення не змінює значення виразу при допустимих значеннях змінних", True),
        ],
        "hint": r"Тотожність — рівність, правильна при всіх допустимих значеннях.",
        "solution": r"$x^2 - 1 = (x - 1)(x + 1)$ — тотожність при $x \ne 1$. Одне число тотожність не доводить. Тотожне перетворення замінює вираз тотожно рівним.",
    },
    {
        "type": "ORDER", "difficulty": 1, "skill": "MODEL",
        "text": r"Розташуйте дії у порядку виконання у виразі $\left(\frac{1}{x} + 1\right) \cdot \frac{x}{x + 1} - 1$.",
        "items": [
            r"Додавання в дужках: $\frac{1}{x} + 1$",
            r"Множення на $\frac{x}{x + 1}$",
            r"Віднімання $1$",
        ],
        "hint": r"Дужки → множення → віднімання.",
        "solution": r"$\frac{x + 1}{x} \cdot \frac{x}{x + 1} = 1$, потім $1 - 1 = 0$ при $x \ne 0$, $x \ne -1$.",
    },
    {
        "type": "MATCH", "difficulty": 1, "skill": "MODEL",
        "text": r"Установіть відповідність між виразом (1–3) та тотожно рівним йому виразом (А–Д).",
        "options": [r"А) $a + b$", r"Б) $b - a$", r"В) $1$", r"Г) $a - b$", r"Д) $ab$"],
        "matches": [(r"1. $\left(\frac{1}{a} + \frac{1}{b}\right) \cdot ab$", r"А) $a + b$"),
                    (r"2. $\left(\frac{1}{a} - \frac{1}{b}\right) \cdot ab$", r"Б) $b - a$"),
                    (r"3. $\frac{1}{a} \cdot \frac{1}{b} \cdot ab$", r"В) $1$")],
        "hint": r"Розкрийте дужки: $\frac{1}{a} \cdot ab = b$, $\frac{1}{b} \cdot ab = a$.",
        "solution": r"1) $b + a$; 2) $b - a$; 3) $\frac{ab}{ab} = 1$ ($a \ne 0$, $b \ne 0$).",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "MODEL",
        "text": r"Як можна довести тотожність?",
        "options": [(r"Перетворити ліву частину так, щоб отримати праву", True), (r"Підставити $x = 1$ і перевірити", False),
                    (r"Підставити три різні числа", False), (r"Помножити обидві частини на $0$", False)],
        "hint": r"Підстановка перевіряє лише окремі значення.",
        "solution": r"Тотожність доводять перетвореннями: ліву частину до правої, обидві до одного виразу або різниця частин дорівнює $0$.",
    },
    # --- Розв'язування ---
    {
        "type": "EXPR", "difficulty": 1, "skill": "SOLVE",
        "text": r"Спростіть вираз $\left(1 + \frac{1}{x}\right) \cdot x$.",
        "answer": "x+1", "vars": ["x"],
        "hint": r"Розкрийте дужки: $1 \cdot x + \frac{1}{x} \cdot x$.",
        "solution": r"$x + 1$ при $x \ne 0$.",
    },
    {
        "type": "EXPR", "difficulty": 1, "skill": "SOLVE",
        "text": r"Спростіть вираз $\left(\frac{a}{b} - 1\right) \cdot b$.",
        "answer": "a-b", "vars": ["a", "b"],
        "hint": r"$\frac{a}{b} - 1 = \frac{a - b}{b}$.",
        "solution": r"$\frac{a - b}{b} \cdot b = a - b$ при $b \ne 0$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"Знайдіть значення виразу $\left(\frac{1}{x} + \frac{1}{2x}\right) \cdot x$ при $x = 17$.",
        "answer": "1.5",
        "hint": r"Спершу спростіть: спільний знаменник $2x$.",
        "solution": r"$\frac{2 + 1}{2x} \cdot x = \frac{3}{2} = 1{,}5$ — при будь-якому $x \ne 0$.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "SOLVE",
        "text": r"Спростіть вираз $\left(\frac{x}{x + 1} + \frac{1}{x + 1}\right) : \frac{1}{x}$.",
        "options": [(r"$x$", True), (r"$\frac{1}{x}$", False), (r"$1$", False), (r"$x + 1$", False)],
        "hint": r"У дужках знаменник спільний: $\frac{x + 1}{x + 1}$.",
        "solution": r"$\frac{x + 1}{x + 1} = 1$; $\;1 : \frac{1}{x} = x$ при $x \ne 0$, $x \ne -1$.",
    },
    {
        "type": "EXPR", "difficulty": 1, "skill": "SOLVE",
        "text": r"Спростіть вираз $\left(\frac{a}{a - 1} - \frac{1}{a - 1}\right) \cdot 5$.",
        "answer": "5", "vars": ["a"],
        "hint": r"Дроби з однаковим знаменником: $\frac{a - 1}{a - 1}$.",
        "solution": r"$\frac{a - 1}{a - 1} \cdot 5 = 5$ при $a \ne 1$.",
    },
    # --- Аналіз ---
    {
        "type": "ERROR", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Олег спрощує $\frac{x}{x + 1} - \frac{x - 1}{x + 1}$. У якому кроці помилка?",
        "steps": [r"Знаменник спільний: $x + 1$", r"Чисельник: $x - x - 1 = -1$", r"Відповідь: $-\frac{1}{x + 1}$"],
        "wrong": 1,
        "hint": r"Мінус перед дробом стосується всього чисельника $x - 1$.",
        "solution": r"$x - (x - 1) = x - x + 1 = 1$. Відповідь: $\frac{1}{x + 1}$.",
    },
    {
        "type": "MULTI", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Які рівності є тотожностями (при допустимих значеннях змінних)?",
        "options": [(r"$\frac{x^2 - 4}{x - 2} = x + 2$", True), (r"$\frac{x}{x} = 1$", True), (r"$\frac{a + b}{b} = a + 1$", False),
                    (r"$\frac{1}{a} + \frac{1}{b} = \frac{2}{a + b}$", False), (r"$\frac{a}{b} \cdot \frac{b}{a} = 1$", True)],
        "hint": r"Хибну рівність спростовує одне число: спробуйте $a = b = 1$ або $a = 2$, $b = 1$.",
        "solution": r"$\frac{a + b}{b} = \frac{a}{b} + 1$, а не $a + 1$ (при $a = 2$, $b = 2$: $2 \ne 3$). $\frac{1}{1} + \frac{1}{1} = 2 \ne 1 = \frac{2}{2}$.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Петро: «Рівність $\frac{1}{x} + 1 = \frac{2}{x}$ правильна при $x = 1$, отже, це тотожність». Хто правий?",
        "options": [(r"Петро помиляється: при $x = 2$ ліва частина $1{,}5$, а права $1$", True), (r"Петро правий: рівність правильна при $x = 1$", False),
                    (r"Петро правий: обидві частини мають знаменник $x$", False), (r"Петро помиляється, бо $x$ не може дорівнювати $1$", False)],
        "hint": r"Тотожність має виконуватися при всіх допустимих $x$. Спробуйте інше число.",
        "solution": r"При $x = 2$: $\frac{1}{2} + 1 = 1{,}5$, а $\frac{2}{2} = 1$. Одного контрприкладу досить, щоб спростувати тотожність.",
    },
    {
        "type": "TF", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Вираз $\frac{x}{x - 3} - \frac{3}{x - 3}$. Правда чи ні?",
        "statements": [
            (r"При $x \ne 3$ він тотожно дорівнює $1$", True),
            (r"При $x = 3$ він дорівнює $1$", False),
            (r"Його значення не залежить від $x$ (на ОДЗ)", True),
        ],
        "hint": r"$\frac{x - 3}{x - 3}$. А що при $x = 3$?",
        "solution": r"$\frac{x - 3}{x - 3} = 1$ при $x \ne 3$; при $x = 3$ знаменник $0$ — вираз не має змісту.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Знайдіть ОДЗ виразу $\frac{1}{x} : \frac{x - 5}{x}$.",
        "options": [(r"$x \ne 0$, $x \ne 5$", True), (r"$x \ne 0$", False), (r"$x \ne 5$", False), (r"$x$ — будь-яке число", False)],
        "hint": r"Знаменники не дорівнюють нулю, і дільник теж.",
        "solution": r"Знаменник $x \ne 0$; дільник $\frac{x - 5}{x} \ne 0$, тобто $x \ne 5$.",
    },
    # ==========================================
    # СХОДИНКА 2 — СЕРЕДНІЙ
    # ==========================================
    # --- Моделювання ---
    {
        "type": "MATCH", "difficulty": 2, "skill": "MODEL",
        "text": r"Розкрийте дужки й установіть відповідність між виразом (1–3) та його спрощеним виглядом (А–Д).",
        "options": [r"А) $a^2 + b^2$", r"Б) $a^2 - b^2$", r"В) $ab$", r"Г) $(a + b)^2$", r"Д) $2ab$"],
        "matches": [(r"1. $\left(\frac{a}{b} + \frac{b}{a}\right) \cdot ab$", r"А) $a^2 + b^2$"),
                    (r"2. $\left(\frac{a}{b} - \frac{b}{a}\right) \cdot ab$", r"Б) $a^2 - b^2$"),
                    (r"3. $\frac{a}{b} \cdot \frac{b}{a} \cdot ab$", r"В) $ab$")],
        "hint": r"$\frac{a}{b} \cdot ab = a^2$, $\;\frac{b}{a} \cdot ab = b^2$.",
        "solution": r"1) $a^2 + b^2$; 2) $a^2 - b^2$; 3) $1 \cdot ab = ab$.",
    },
    {
        "type": "ORDER", "difficulty": 2, "skill": "MODEL",
        "text": r"Розташуйте кроки доведення тотожності $\left(\frac{1}{x - 1} - \frac{1}{x + 1}\right) \cdot \frac{x^2 - 1}{2} = 1$.",
        "items": [
            r"Спільний знаменник у дужках: $(x - 1)(x + 1)$",
            r"Чисельник: $(x + 1) - (x - 1) = 2$",
            r"Множимо: $\frac{2}{x^2 - 1} \cdot \frac{x^2 - 1}{2}$",
            r"Скорочуємо: ліва частина дорівнює $1$ при $x \ne \pm 1$",
        ],
        "hint": r"Спершу дужки, потім множення.",
        "solution": r"$\frac{2}{(x - 1)(x + 1)} \cdot \frac{x^2 - 1}{2} = 1$ — ліва частина дорівнює правій.",
    },
    {
        "type": "EXPR", "difficulty": 2, "skill": "MODEL",
        "text": r"Сторони прямокутника — $1 + \frac{1}{a}$ і $\frac{a^2}{a + 1}$ ($a \gt 0$). Запишіть найпростіший вираз для його площі.",
        "answer": "a", "vars": ["a"],
        "hint": r"$1 + \frac{1}{a} = \frac{a + 1}{a}$.",
        "solution": r"$\frac{a + 1}{a} \cdot \frac{a^2}{a + 1} = a$.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "MODEL",
        "text": r"Велосипедист проїхав $s$ км зі швидкістю $v$ км/год, а назад — зі швидкістю $2v$ км/год. Яка його середня швидкість?",
        "options": [(r"$\frac{4v}{3}$", True), (r"$\frac{3v}{2}$", False), (r"$\frac{3v}{4}$", False), (r"$\frac{2v}{3}$", False)],
        "hint": r"Середня швидкість — весь шлях $2s$, поділений на весь час $\frac{s}{v} + \frac{s}{2v}$.",
        "solution": r"$\frac{s}{v} + \frac{s}{2v} = \frac{3s}{2v}$. $\;2s : \frac{3s}{2v} = \frac{4v}{3}$ — не середнє арифметичне $1{,}5v$.",
    },
    {
        "type": "GROUP", "difficulty": 2, "skill": "MODEL",
        "text": r"Розподіліть вирази: чому вони тотожно дорівнюють (на ОДЗ)?",
        "groups": [r"Тотожно дорівнює $1$", r"Тотожно дорівнює $x$"],
        "items": [(r"$\frac{x}{x - 1} - \frac{1}{x - 1}$", 0), (r"$\frac{x^2}{x + 1} + \frac{x}{x + 1}$", 1), (r"$\left(1 + \frac{1}{x}\right) \cdot \frac{x}{x + 1}$", 0),
                  (r"$\frac{x^2 - x}{x - 1}$", 1), (r"$\left(\frac{1}{x} + \frac{1}{x^2}\right) \cdot \frac{x^2}{x + 1}$", 0)],
        "hint": r"Спростіть кожен: розкладіть на множники й скоротіть.",
        "solution": r"$\frac{x - 1}{x - 1} = 1$; $\frac{x(x + 1)}{x + 1} = x$; $\frac{x + 1}{x} \cdot \frac{x}{x + 1} = 1$; $\frac{x(x - 1)}{x - 1} = x$; $\frac{x + 1}{x^2} \cdot \frac{x^2}{x + 1} = 1$.",
    },
    # --- Розв'язування ---
    {
        "type": "EXPR", "difficulty": 2, "skill": "SOLVE",
        "text": r"Спростіть вираз $\left(\frac{1}{a - b} + \frac{1}{a + b}\right) \cdot (a^2 - b^2)$.",
        "answer": "2a", "vars": ["a", "b"],
        "hint": r"Можна розкрити дужки: $\frac{a^2 - b^2}{a - b} = a + b$.",
        "solution": r"$(a + b) + (a - b) = 2a$ при $a \ne \pm b$.",
    },
    {
        "type": "EXPR", "difficulty": 2, "skill": "SOLVE",
        "text": r"Спростіть вираз $\left(\frac{x}{x - y} - \frac{y}{x + y}\right) : \frac{x^2 + y^2}{x - y}$.",
        "answer": "1/(x+y)", "vars": ["x", "y"],
        "hint": r"Дужки: $\frac{x(x + y) - y(x - y)}{(x - y)(x + y)}$.",
        "solution": r"Чисельник: $x^2 + xy - xy + y^2 = x^2 + y^2$. $\;\frac{x^2 + y^2}{(x - y)(x + y)} \cdot \frac{x - y}{x^2 + y^2} = \frac{1}{x + y}$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Знайдіть значення виразу $\left(1 - \frac{2}{a + 1}\right) : \frac{a - 1}{a^2 + a}$ при $a = 7$.",
        "answer": "7",
        "hint": r"Спершу спростіть: $1 - \frac{2}{a + 1} = \frac{a - 1}{a + 1}$.",
        "solution": r"$\frac{a - 1}{a + 1} \cdot \frac{a(a + 1)}{a - 1} = a$. При $a = 7$ — $7$.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "SOLVE",
        "text": r"Спростіть вираз $\left(x + 2 - \frac{4x}{x + 2}\right) : \frac{x^2 + 4}{x^2 - 4}$.",
        "options": [(r"$x - 2$", True), (r"$x + 2$", False), (r"$\frac{x^2 + 4}{x + 2}$", False), (r"$\frac{1}{x - 2}$", False)],
        "hint": r"$x + 2 = \frac{(x + 2)^2}{x + 2}$.",
        "solution": r"$\frac{(x + 2)^2 - 4x}{x + 2} = \frac{x^2 + 4}{x + 2}$. $\;\frac{x^2 + 4}{x + 2} \cdot \frac{(x - 2)(x + 2)}{x^2 + 4} = x - 2$.",
    },
    {
        "type": "EXPR", "difficulty": 2, "skill": "SOLVE",
        "text": r"Спростіть вираз $\left(\frac{2}{x} - \frac{1}{x + 1}\right) \cdot x(x + 1)$.",
        "answer": "x+2", "vars": ["x"],
        "hint": r"Розкрийте дужки: кожен дріб помножте на $x(x + 1)$.",
        "solution": r"$2(x + 1) - x = x + 2$ при $x \ne 0$, $x \ne -1$.",
    },
    # --- Аналіз ---
    {
        "type": "ERROR", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Ліна спрощує $\left(\frac{1}{a} + \frac{1}{b}\right) : \frac{1}{ab}$. У якому кроці помилка?",
        "steps": [r"$\frac{1}{a} + \frac{1}{b} = \frac{2}{a + b}$", r"$\frac{2}{a + b} \cdot ab$", r"$= \frac{2ab}{a + b}$"],
        "wrong": 0,
        "hint": r"Дроби додають через спільний знаменник, а не «чисельник до чисельника».",
        "solution": r"$\frac{1}{a} + \frac{1}{b} = \frac{a + b}{ab}$. Тоді $\frac{a + b}{ab} \cdot ab = a + b$.",
    },
    {
        "type": "MULTI", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Значення яких виразів не залежить від $x$ (на ОДЗ)?",
        "options": [(r"$\frac{x}{x - 2} - \frac{2}{x - 2}$", True), (r"$\left(1 + \frac{1}{x}\right) \cdot \frac{x}{x + 1}$", True), (r"$\frac{x^2 - 1}{x - 1} - x$", True),
                    (r"$\frac{x}{x + 1} \cdot (x + 1)$", False), (r"$\left(\frac{1}{x} - 1\right) \cdot x$", False)],
        "hint": r"Спростіть кожен і подивіться, чи лишилася змінна.",
        "solution": r"Перші три дорівнюють $1$. $\frac{x}{x + 1} \cdot (x + 1) = x$; $\left(\frac{1}{x} - 1\right) x = 1 - x$.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Знайдіть ОДЗ виразу $\left(\frac{1}{x - 1} + 1\right) : \frac{x}{x + 2}$.",
        "options": [(r"$x \ne 1$, $x \ne -2$, $x \ne 0$", True), (r"$x \ne 1$, $x \ne -2$", False), (r"$x \ne 1$, $x \ne 0$", False), (r"$x \ne 1$", False)],
        "hint": r"Усі знаменники $\ne 0$, і дільник $\frac{x}{x + 2} \ne 0$.",
        "solution": r"$x - 1 \ne 0$, $x + 2 \ne 0$, а ще дільник не нуль: $x \ne 0$.",
    },
    {
        "type": "TF", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Учень довів, що $\frac{x^2 - 9}{x - 3} = x + 3$. Правда чи ні?",
        "statements": [
            (r"Рівність правильна при $x = 3$", False),
            (r"Рівність правильна при $x = -3$", True),
            (r"Це тотожність на множині $x \ne 3$", True),
        ],
        "hint": r"При $x = 3$ знаменник дорівнює $0$. При $x = -3$: $\frac{0}{-6} = 0$.",
        "solution": r"При $x = 3$ ліва частина не має змісту. При $x = -3$ обидві частини дорівнюють $0$. Скорочення на $x - 3$ можливе лише при $x \ne 3$.",
    },
    {
        "type": "GROUP", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Розподіліть перетворення: правильні чи з помилкою?",
        "groups": [r"Тотожне перетворення", r"Помилка"],
        "items": [(r"$\frac{1}{a} + \frac{1}{b} = \frac{a + b}{ab}$", 0), (r"$\frac{a + b}{b} = a + 1$", 1), (r"$\frac{x^2 - 1}{x + 1} = x - 1$", 0),
                  (r"$\frac{a}{a + b} = \frac{1}{b}$", 1), (r"$-\frac{x - 1}{2} = \frac{1 - x}{2}$", 0)],
        "hint": r"Скорочувати можна лише спільні множники, а не доданки.",
        "solution": r"Помилки: «скоротили» $b$ у сумі $a + b$ і $a$ у сумі $a + b$. Інші — правильні: спільний знаменник, різниця квадратів, мінус у чисельник.",
    },
    # ==========================================
    # СХОДИНКА 3 — ПІДВИЩЕНИЙ
    # ==========================================
    # --- Моделювання ---
    {
        "type": "EXPR", "difficulty": 3, "skill": "MODEL",
        "text": r"Перший робітник виконує роботу за $a$ год, другий — за $b$ год. Запишіть вираз для часу (у годинах), за який вони виконають роботу разом.",
        "answer": "ab/(a+b)", "vars": ["a", "b"],
        "hint": r"За годину перший робить $\frac{1}{a}$ роботи, другий — $\frac{1}{b}$.",
        "solution": r"Разом за годину — $\frac{1}{a} + \frac{1}{b} = \frac{a + b}{ab}$ роботи. Час: $1 : \frac{a + b}{ab} = \frac{ab}{a + b}$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"Значення виразу $\frac{3a}{a - b} + \frac{3b}{b - a}$ не залежить від $a$ і $b$ (на ОДЗ). Знайдіть його.",
        "answer": "3",
        "hint": r"$b - a = -(a - b)$.",
        "solution": r"$\frac{3a}{a - b} - \frac{3b}{a - b} = \frac{3(a - b)}{a - b} = 3$ при $a \ne b$.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "MODEL",
        "text": r"Автомобіль їхав з міста в село зі швидкістю $a$ км/год, а назад — зі швидкістю $b$ км/год. Яка середня швидкість на всьому шляху?",
        "options": [(r"$\frac{2ab}{a + b}$", True), (r"$\frac{a + b}{2}$", False), (r"$\frac{ab}{a + b}$", False), (r"$\frac{2}{a + b}$", False), (r"$\frac{a + b}{ab}$", False)],
        "hint": r"Позначте відстань $s$. Час — $\frac{s}{a} + \frac{s}{b}$, шлях — $2s$.",
        "solution": r"$\frac{s}{a} + \frac{s}{b} = \frac{s(a + b)}{ab}$. $\;2s : \frac{s(a + b)}{ab} = \frac{2ab}{a + b}$ — $s$ скоротилося.",
    },
    {
        "type": "MATCH", "difficulty": 3, "skill": "MODEL",
        "text": r"Установіть відповідність між виразом (1–3) та його ОДЗ (А–Д).",
        "options": [r"А) $x \ne 0$, $x \ne 1$", r"Б) $x \ne -1$", r"В) $x \ne 1$, $x \ne -2$", r"Г) $x \ne -1$, $x \ne 2$", r"Д) $x \ne 1$"],
        "matches": [(r"1. $\frac{1}{x} : \frac{x - 1}{x}$", r"А) $x \ne 0$, $x \ne 1$"),
                    (r"2. $\frac{1}{x + 1} \cdot (x - 2)$", r"Б) $x \ne -1$"),
                    (r"3. $\frac{1}{x - 1} : \frac{x + 2}{x - 1}$", r"В) $x \ne 1$, $x \ne -2$")],
        "hint": r"Множник $(x - 2)$ — не знаменник і не дільник, обмежень не дає.",
        "solution": r"1) знаменник $x$ і дільник $\ne 0$; 2) лише $x + 1 \ne 0$; 3) знаменник $x - 1$ і дільник: $x + 2 \ne 0$.",
    },
    {
        "type": "TF", "difficulty": 3, "skill": "MODEL",
        "text": r"$A = \left(\frac{1}{x - 1} - \frac{1}{x + 1}\right) : \frac{2}{x^2 - 1}$. Правда чи ні?",
        "statements": [
            (r"$A = 1$ при всіх допустимих $x$", True),
            (r"ОДЗ: $x \ne \pm 1$", True),
            (r"$A(0) = -1$", False),
        ],
        "hint": r"Дужки: $\frac{(x + 1) - (x - 1)}{x^2 - 1}$.",
        "solution": r"$\frac{2}{x^2 - 1} : \frac{2}{x^2 - 1} = 1$, тому й $A(0) = 1$: $(-1 - 1) : (-2) = 1$.",
    },
    # --- Розв'язування ---
    {
        "type": "EXPR", "difficulty": 3, "skill": "SOLVE",
        "text": r"Спростіть вираз $\left(\frac{1}{x} - \frac{1}{y}\right) : \left(\frac{1}{x^2} - \frac{1}{y^2}\right)$.",
        "answer": "xy/(x+y)", "vars": ["x", "y"],
        "hint": r"$\frac{1}{x^2} - \frac{1}{y^2} = \frac{y^2 - x^2}{x^2 y^2} = \frac{(y - x)(y + x)}{x^2 y^2}$.",
        "solution": r"$\frac{y - x}{xy} \cdot \frac{x^2 y^2}{(y - x)(y + x)} = \frac{xy}{x + y}$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Знайдіть значення виразу $\left(\frac{x + 1}{x - 1} - \frac{x - 1}{x + 1}\right) \cdot \frac{x^2 - 1}{4x}$ при $x = 2025$.",
        "answer": "1",
        "hint": r"Не підставляйте одразу — спростіть.",
        "solution": r"$\frac{(x + 1)^2 - (x - 1)^2}{x^2 - 1} = \frac{4x}{x^2 - 1}$. $\;\frac{4x}{x^2 - 1} \cdot \frac{x^2 - 1}{4x} = 1$ при будь-якому допустимому $x$.",
    },
    {
        "type": "EXPR", "difficulty": 3, "skill": "SOLVE",
        "text": r"Спростіть вираз $\left(\frac{a}{a - 2} - \frac{4a}{a^2 - 4}\right) \cdot (a + 2)$.",
        "answer": "a", "vars": ["a"],
        "hint": r"Спільний знаменник у дужках — $(a - 2)(a + 2)$.",
        "solution": r"$\frac{a(a + 2) - 4a}{(a - 2)(a + 2)} = \frac{a^2 - 2a}{(a - 2)(a + 2)} = \frac{a}{a + 2}$. $\;\frac{a}{a + 2} \cdot (a + 2) = a$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Знайдіть значення виразу $\left(\frac{m}{n} - \frac{n}{m}\right) : \frac{m + n}{mn}$ при $m = 3{,}7$, $n = 1{,}7$.",
        "answer": "2",
        "hint": r"Спершу спростіть: $\frac{m^2 - n^2}{mn}$.",
        "solution": r"$\frac{(m - n)(m + n)}{mn} \cdot \frac{mn}{m + n} = m - n = 3{,}7 - 1{,}7 = 2$.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "SOLVE",
        "text": r"Спростіть вираз $1 - \dfrac{1}{1 - \frac{1}{x}}$.",
        "options": [(r"$\frac{1}{1 - x}$", True), (r"$\frac{1}{x - 1}$", False), (r"$\frac{x}{x - 1}$", False), (r"$-x$", False)],
        "hint": r"Знизу вгору: $1 - \frac{1}{x} = \frac{x - 1}{x}$, тоді $\frac{1}{\frac{x - 1}{x}} = \frac{x}{x - 1}$.",
        "solution": r"$1 - \frac{x}{x - 1} = \frac{x - 1 - x}{x - 1} = -\frac{1}{x - 1} = \frac{1}{1 - x}$ при $x \ne 0$, $x \ne 1$.",
    },
    # --- Аналіз ---
    {
        "type": "ERROR", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Саша спрощує $\frac{a}{a - b} + \frac{b}{b - a}$. У якому кроці помилка?",
        "steps": [r"Спільний знаменник: $a - b$, бо $b - a = -(a - b)$", r"$\frac{a}{a - b} + \frac{b}{b - a} = \frac{a + b}{a - b}$", r"Відповідь: $\frac{a + b}{a - b}$"],
        "wrong": 1,
        "hint": r"Коли міняємо знаменник $b - a$ на $a - b$, змінюється знак дробу.",
        "solution": r"$\frac{b}{b - a} = -\frac{b}{a - b}$, тож $\frac{a - b}{a - b} = 1$ при $a \ne b$.",
    },
    {
        "type": "MULTI", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Які вирази дорівнюють $\frac{x + 1}{x}$ при всіх $x$, для яких обидва вирази мають зміст?",
        "options": [(r"$1 + \frac{1}{x}$", True), (r"$\frac{x^2 + x}{x^2}$", True), (r"$\frac{x + 1}{x} \cdot \frac{x - 1}{x - 1}$", True),
                    (r"$\frac{x}{x + 1}$", False), (r"$\frac{1}{x} + x$", False)],
        "hint": r"Спростіть кожен; хибні спростуйте числом, наприклад $x = 1$.",
        "solution": r"$1 + \frac{1}{x} = \frac{x + 1}{x}$; $\frac{x(x + 1)}{x^2} = \frac{x + 1}{x}$; множник $\frac{x - 1}{x - 1} = 1$. $\frac{x}{x + 1}$ при $x = 1$ дає $\frac{1}{2} \ne 2$; $\frac{1}{x} + x$ при $x = 2$ дає $2{,}5 \ne 1{,}5$.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "ANALYZE",
        "text": r"При яких $x$ правильна рівність $\frac{x^2 - 4}{x + 2} \cdot \frac{1}{x - 2} = 1$?",
        "options": [(r"При $x \ne \pm 2$", True), (r"При $x \ne 2$", False), (r"При $x \ne -2$", False), (r"При всіх $x$", False)],
        "hint": r"Ліва частина має зміст лише тоді, коли обидва знаменники $\ne 0$.",
        "solution": r"$\frac{(x - 2)(x + 2)}{(x + 2)(x - 2)} = 1$, але лише при $x \ne -2$ і $x \ne 2$.",
    },
    {
        "type": "TF", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Розглянемо рівність $\frac{1}{x(x + 1)} = \frac{1}{x} - \frac{1}{x + 1}$. Правда чи ні?",
        "statements": [
            (r"Це тотожність (при $x \ne 0$, $x \ne -1$)", True),
            (r"Звідси $\frac{1}{1 \cdot 2} + \frac{1}{2 \cdot 3} + \frac{1}{3 \cdot 4} = \frac{3}{4}$", True),
            (r"При $x = 1$ обидві частини дорівнюють $1$", False),
        ],
        "hint": r"Зведіть праву частину до спільного знаменника.",
        "solution": r"$\frac{(x + 1) - x}{x(x + 1)} = \frac{1}{x(x + 1)}$ ✓. Сума: $\left(1 - \frac{1}{2}\right) + \left(\frac{1}{2} - \frac{1}{3}\right) + \left(\frac{1}{3} - \frac{1}{4}\right) = 1 - \frac{1}{4} = \frac{3}{4}$. При $x = 1$ обидві частини дорівнюють $\frac{1}{2}$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Скільки цілих значень $x$ не входять до ОДЗ виразу $\left(\frac{1}{x - 1} + \frac{1}{x + 1}\right) : \frac{x}{x^2 - 4}$?",
        "answer": "5",
        "hint": r"Знаменники: $x - 1$, $x + 1$, $x^2 - 4$. Дільник $\frac{x}{x^2 - 4} \ne 0$.",
        "solution": r"$x \ne \pm 1$, $x \ne \pm 2$ і дільник не нуль: $x \ne 0$. Разом $5$ цілих значень: $-2, -1, 0, 1, 2$.",
    },
    # ==========================================
    # БОСИ
    # ==========================================
    {
        "type": "SHORT", "difficulty": 4, "skill": "MODEL",
        "text": r"Перша бригада виконує роботу за $x$ днів, друга — за $2x$ днів. Разом вони виконують її за $8$ днів. За скільки днів виконає роботу перша бригада?",
        "answer": "12",
        "solution": r"Разом за день: $\frac{1}{x} + \frac{1}{2x} = \frac{3}{2x}$. Час разом $\frac{2x}{3} = 8$, $x = 12$.",
    },
    {
        "type": "EXPR", "difficulty": 4, "skill": "MODEL",
        "text": r"Першу половину шляху автомобіль їхав зі швидкістю $v$ км/год, другу — зі швидкістю $v + 10$ км/год. Запишіть вираз для середньої швидкості на всьому шляху.",
        "answer": "v(v+10)/(v+5)", "vars": ["v"],
        "solution": r"Половина шляху — $s$. Час: $\frac{s}{v} + \frac{s}{v + 10} = \frac{s(2v + 10)}{v(v + 10)}$. Середня швидкість: $2s : \frac{2s(v + 5)}{v(v + 10)} = \frac{v(v + 10)}{v + 5}$.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "SOLVE",
        "text": r"Знайдіть значення виразу $\left(\frac{a + b}{a - b} - \frac{a - b}{a + b}\right) : \frac{ab}{a^2 - b^2}$ при допустимих $a$ і $b$.",
        "answer": "4",
        "solution": r"$\frac{(a + b)^2 - (a - b)^2}{a^2 - b^2} = \frac{4ab}{a^2 - b^2}$. $\;\frac{4ab}{a^2 - b^2} \cdot \frac{a^2 - b^2}{ab} = 4$.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "SOLVE",
        "text": r"Відомо, що $x + \frac{1}{x} = 5$. Знайдіть $x^2 + \frac{1}{x^2}$.",
        "answer": "23",
        "solution": r"$\left(x + \frac{1}{x}\right)^2 = x^2 + 2 + \frac{1}{x^2} = 25$, тож $x^2 + \frac{1}{x^2} = 23$.",
    },
    {
        "type": "TF", "difficulty": 4, "skill": "ANALYZE",
        "text": r"Відомо, що $\frac{a}{b} = 2$. Правда чи ні?",
        "statements": [
            (r"$\frac{a + b}{b} = 3$", True),
            (r"$\frac{a - b}{a + b} = \frac{1}{3}$", True),
            (r"$\frac{b}{a} = 0{,}5$", True),
            (r"$\frac{a^2}{b^2} = 2$", False),
        ],
        "solution": r"$\frac{a + b}{b} = \frac{a}{b} + 1 = 3$. Поділимо чисельник і знаменник на $b$: $\frac{2 - 1}{2 + 1} = \frac{1}{3}$. $\frac{b}{a} = \frac{1}{2}$. $\frac{a^2}{b^2} = 2^2 = 4$.",
    },
    # ==========================================
    # УЛЬТРА
    # ==========================================
    {
        "type": "SHORT", "difficulty": 5, "skill": "SOLVE",
        "text": r"Обчисліть $\frac{1}{1 \cdot 2} + \frac{1}{2 \cdot 3} + \frac{1}{3 \cdot 4} + \ldots + \frac{1}{99 \cdot 100}$.",
        "answer": "0.99",
        "solution": r"$\frac{1}{n(n + 1)} = \frac{1}{n} - \frac{1}{n + 1}$. Сума «телескопічна»: $1 - \frac{1}{2} + \frac{1}{2} - \frac{1}{3} + \ldots - \frac{1}{100} = 1 - \frac{1}{100} = 0{,}99$.",
    },
    {
        "type": "SHORT", "difficulty": 5, "skill": "MODEL",
        "text": r"Відомо, що $a + b = 5$, $ab = 3$. Знайдіть $\frac{a}{b} + \frac{b}{a}$.",
        "answer": "19/3",
        "solution": r"$\frac{a}{b} + \frac{b}{a} = \frac{a^2 + b^2}{ab} = \frac{(a + b)^2 - 2ab}{ab} = \frac{25 - 6}{3} = \frac{19}{3}$.",
    },
]
