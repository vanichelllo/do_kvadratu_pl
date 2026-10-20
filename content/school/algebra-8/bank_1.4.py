TOPIC_NAME = "1.4. Множення і ділення раціональних дробів"
COURSE = "Алгебра (7-9 класи)"
GRADE = "8 клас"

TASKS = [
    # ==========================================
    # СХОДИНКА 1 — БАЗОВИЙ
    # ==========================================
    # --- Моделювання ---
    {
        "type": "CHOICE", "difficulty": 1, "skill": "MODEL",
        "text": r"Як поділити дріб $\frac{a}{b}$ на дріб $\frac{c}{d}$?",
        "options": [(r"Помножити $\frac{a}{b}$ на $\frac{d}{c}$", True), (r"Помножити $\frac{b}{a}$ на $\frac{c}{d}$", False), (r"Додати $\frac{a}{b}$ і $\frac{d}{c}$", False), (r"Помножити $\frac{a}{b}$ на $\frac{c}{d}$", False)],
        "hint": r"Обертаємо дільник — другий дріб.",
        "solution": r"$\frac{a}{b} : \frac{c}{d} = \frac{a}{b} \cdot \frac{d}{c} = \frac{ad}{bc}$.",
    },
    {
        "type": "EXPR", "difficulty": 1, "skill": "MODEL",
        "text": r"Прямокутник має сторони $\frac{a}{2}$ і $\frac{4}{a}$. Запишіть вираз для його площі.",
        "answer": "2", "vars": ["a"],
        "hint": r"Площа — добуток сторін.",
        "solution": r"$\frac{a}{2} \cdot \frac{4}{a} = \frac{4a}{2a} = 2$.",
    },
    {
        "type": "TF", "difficulty": 1, "skill": "MODEL",
        "text": r"Правда чи ні?",
        "statements": [
            (r"$\frac{a}{b} \cdot \frac{c}{d} = \frac{ac}{bd}$", True),
            (r"$\left(\frac{x}{y}\right)^2 = \frac{x^2}{y}$", False),
            (r"$\frac{x}{3} : \frac{x}{6} = 2$ при $x \ne 0$", True),
        ],
        "hint": r"У степінь підносять і чисельник, і знаменник.",
        "solution": r"Правило множення ✓. $\left(\frac{x}{y}\right)^2 = \frac{x^2}{y^2}$. $\frac{x}{3} \cdot \frac{6}{x} = 2$ ✓.",
    },
    {
        "type": "MATCH", "difficulty": 1, "skill": "MODEL",
        "text": r"Установіть відповідність між дією (1–3) та результатом (А–Д).",
        "options": [r"А) $\frac{x^2}{4}$", r"Б) $\frac{1}{2}$", r"В) $2$", r"Г) $\frac{2}{x^2}$", r"Д) $\frac{x}{4}$"],
        "matches": [(r"1. $\frac{x}{2} \cdot \frac{x}{2}$", r"А) $\frac{x^2}{4}$"),
                    (r"2. $\frac{x}{2} : x$", r"Б) $\frac{1}{2}$"),
                    (r"3. $x : \frac{x}{2}$", r"В) $2$")],
        "hint": r"Ділення на $x$ — множення на $\frac{1}{x}$.",
        "solution": r"1) $\frac{x^2}{4}$. 2) $\frac{x}{2} \cdot \frac{1}{x} = \frac{1}{2}$. 3) $x \cdot \frac{2}{x} = 2$ (усе при $x \ne 0$).",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "MODEL",
        "text": r"Знайдіть значення $\frac{x^2}{y} \cdot \frac{y^2}{x}$ при $x = 3$, $y = 2$.",
        "answer": "6",
        "hint": r"Спершу спростіть: вийде $xy$.",
        "solution": r"$\frac{x^2 y^2}{xy} = xy = 6$.",
    },
    # --- Розв'язування ---
    {
        "type": "EXPR", "difficulty": 1, "skill": "SOLVE",
        "text": r"Спростіть $\frac{3x}{y^2} \cdot \frac{y}{6x^2}$.",
        "answer": "1/(2xy)", "vars": ["x", "y"],
        "hint": r"Скоротіть на $3$, $x$ і $y$.",
        "solution": r"$\frac{3xy}{6x^2 y^2} = \frac{1}{2xy}$.",
    },
    {
        "type": "EXPR", "difficulty": 1, "skill": "SOLVE",
        "text": r"Спростіть $\frac{4a}{5} : \frac{2a}{15}$.",
        "answer": "6", "vars": ["a"],
        "hint": r"Помножте на $\frac{15}{2a}$.",
        "solution": r"$\frac{4a \cdot 15}{5 \cdot 2a} = \frac{60a}{10a} = 6$ при $a \ne 0$.",
    },
    {
        "type": "EXPR", "difficulty": 1, "skill": "SOLVE",
        "text": r"Піднесіть до степеня: $\left(\frac{2x}{y}\right)^3$.",
        "answer": "8x^3/y^3", "vars": ["x", "y"],
        "hint": r"$(2x)^3 = 8x^3$.",
        "solution": r"$\frac{(2x)^3}{y^3} = \frac{8x^3}{y^3}$.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "SOLVE",
        "text": r"Спростіть $\frac{a^2}{b} : \frac{a}{b^2}$.",
        "options": [(r"$ab$", True), (r"$\frac{a}{b}$", False), (r"$\frac{a^3}{b^3}$", False), (r"$\frac{b}{a}$", False)],
        "hint": r"Помножте на $\frac{b^2}{a}$.",
        "solution": r"$\frac{a^2 \cdot b^2}{b \cdot a} = ab$.",
    },
    {
        "type": "EXPR", "difficulty": 1, "skill": "SOLVE",
        "text": r"Спростіть $\frac{x + 1}{x} \cdot \frac{x^2}{x + 1}$.",
        "answer": "x", "vars": ["x"],
        "hint": r"Скоротіть $x + 1$ і $x$.",
        "solution": r"$\frac{(x + 1) x^2}{x(x + 1)} = x$ при $x \ne 0$, $x \ne -1$.",
    },
    # --- Аналіз ---
    {
        "type": "ERROR", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Петро ділив $\frac{3}{x} : \frac{6}{x^2}$. У якому кроці помилка?",
        "steps": [r"$\frac{x}{3} \cdot \frac{6}{x^2}$", r"$= \frac{6x}{3x^2}$", r"$= \frac{2}{x}$"],
        "wrong": 0,
        "hint": r"Який дріб треба перевертати?",
        "solution": r"Обертаємо дільник: $\frac{3}{x} \cdot \frac{x^2}{6} = \frac{x}{2}$.",
    },
    {
        "type": "MULTI", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Які рівності правильні (при допустимих значеннях змінних)?",
        "options": [(r"$\frac{a}{b} \cdot \frac{b}{a} = 1$", True), (r"$\frac{a}{b} : \frac{a}{b} = 1$", True), (r"$\left(-\frac{a}{b}\right)^2 = -\frac{a^2}{b^2}$", False), (r"$\frac{a + 1}{b} \cdot \frac{b}{a} = 1$", False)],
        "hint": r"Парний степінь «з'їдає» мінус.",
        "solution": r"Перші два правильні. $\left(-\frac{a}{b}\right)^2 = \frac{a^2}{b^2}$. $\frac{a + 1}{a} \ne 1$.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "ANALYZE",
        "text": r"При яких $x$ має зміст вираз $\frac{1}{x} : \frac{x - 2}{x}$?",
        "options": [(r"$x \ne 0$ і $x \ne 2$", True), (r"лише $x \ne 0$", False), (r"лише $x \ne 2$", False), (r"при будь-яких $x$", False)],
        "hint": r"Дільник не може дорівнювати нулю.",
        "solution": r"Знаменники: $x \ne 0$; дільник $\frac{x - 2}{x} \ne 0$, тож $x \ne 2$.",
    },
    {
        "type": "TF", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [
            (r"$\left(-\frac{a}{b}\right)^3 = -\frac{a^3}{b^3}$", True),
            (r"$\frac{x}{y} : x = \frac{1}{y}$ при $x \ne 0$", True),
            (r"$\frac{x}{y} : y = \frac{x}{1}$", False),
        ],
        "hint": r"Ділення на $y$ — множення на $\frac{1}{y}$.",
        "solution": r"Непарний степінь ✓. $\frac{x}{y} \cdot \frac{1}{x} = \frac{1}{y}$ ✓. $\frac{x}{y} \cdot \frac{1}{y} = \frac{x}{y^2}$.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Який вираз обернений до дробу $\frac{x - 3}{x + 1}$?",
        "options": [(r"$\frac{x + 1}{x - 3}$", True), (r"$\frac{3 - x}{x + 1}$", False), (r"$-\frac{x - 3}{x + 1}$", False), (r"$\frac{x + 3}{x - 1}$", False)],
        "hint": r"Обернений дріб — переставити чисельник і знаменник.",
        "solution": r"$\frac{x - 3}{x + 1} \cdot \frac{x + 1}{x - 3} = 1$.",
    },

    # ==========================================
    # СХОДИНКА 2 — СЕРЕДНІЙ
    # ==========================================
    # --- Моделювання ---
    {
        "type": "EXPR", "difficulty": 2, "skill": "MODEL",
        "text": r"Сторони прямокутника — $\frac{x^2 - 1}{x}$ і $\frac{x}{x + 1}$. Запишіть спрощений вираз для площі.",
        "answer": "x-1", "vars": ["x"],
        "solution": r"$\frac{(x - 1)(x + 1) \cdot x}{x(x + 1)} = x - 1$.",
    },
    {
        "type": "EXPR", "difficulty": 2, "skill": "MODEL",
        "text": r"Площа прямокутника — $\frac{a^2 - 4}{a}$, одна сторона — $\frac{a + 2}{a}$. Запишіть вираз для другої сторони.",
        "answer": "a-2", "vars": ["a"],
        "solution": r"$\frac{a^2 - 4}{a} : \frac{a + 2}{a} = \frac{(a - 2)(a + 2) \cdot a}{a(a + 2)} = a - 2$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "MODEL",
        "text": r"Знайдіть значення виразу $\frac{x^2 - 4}{x + 3} \cdot \frac{x + 3}{x - 2}$ при $x = 98$.",
        "answer": "100",
        "solution": r"Вираз дорівнює $x + 2$ (при $x \ne -3$, $x \ne 2$): $98 + 2 = 100$.",
    },
    {
        "type": "MATCH", "difficulty": 2, "skill": "MODEL",
        "text": r"Установіть відповідність між виразом (1–3) та спрощеним виглядом (А–Д).",
        "options": [r"А) $\frac{a + b}{a}$", r"Б) $a - b$", r"В) $\frac{1}{a - b}$", r"Г) $a + b$", r"Д) $\frac{a}{a + b}$"],
        "matches": [(r"1. $\frac{a^2 - b^2}{a} \cdot \frac{1}{a - b}$", r"А) $\frac{a + b}{a}$"),
                    (r"2. $\frac{a^2 - b^2}{a + b}$", r"Б) $a - b$"),
                    (r"3. $\frac{a + b}{a^2 - b^2}$", r"В) $\frac{1}{a - b}$")],
        "solution": r"$a^2 - b^2 = (a - b)(a + b)$. 1) $\frac{a + b}{a}$. 2) $a - b$. 3) $\frac{1}{a - b}$.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "MODEL",
        "text": r"Автомобіль проїхав $\frac{s}{2}$ км за $\frac{t}{3}$ год. Яка його швидкість (км/год)?",
        "options": [(r"$\frac{3s}{2t}$", True), (r"$\frac{st}{6}$", False), (r"$\frac{2s}{3t}$", False), (r"$\frac{2t}{3s}$", False)],
        "solution": r"$v = \frac{s}{2} : \frac{t}{3} = \frac{s}{2} \cdot \frac{3}{t} = \frac{3s}{2t}$.",
    },
    # --- Розв'язування ---
    {
        "type": "EXPR", "difficulty": 2, "skill": "SOLVE",
        "text": r"Спростіть $\frac{x^2 - 25}{3x} : \frac{x + 5}{6x^2}$.",
        "answer": "2x(x-5)", "vars": ["x"],
        "solution": r"$\frac{(x - 5)(x + 5)}{3x} \cdot \frac{6x^2}{x + 5} = 2x(x - 5)$.",
    },
    {
        "type": "EXPR", "difficulty": 2, "skill": "SOLVE",
        "text": r"Спростіть $\frac{a^2 - 9}{a^2 + 2a} : \frac{a - 3}{a}$.",
        "answer": "(a+3)/(a+2)", "vars": ["a"],
        "solution": r"$\frac{(a - 3)(a + 3)}{a(a + 2)} \cdot \frac{a}{a - 3} = \frac{a + 3}{a + 2}$.",
    },
    {
        "type": "EXPR", "difficulty": 2, "skill": "SOLVE",
        "text": r"Спростіть $\frac{x - y}{x^2} \cdot \frac{x}{y - x}$.",
        "answer": "-1/x", "vars": ["x", "y"],
        "solution": r"$y - x = -(x - y)$: $\frac{(x - y)x}{-x^2(x - y)} = -\frac{1}{x}$.",
    },
    {
        "type": "EXPR", "difficulty": 2, "skill": "SOLVE",
        "text": r"Спростіть $\left(-\frac{2x^2}{3y}\right)^3 \cdot \frac{9y^4}{4x^5}$.",
        "answer": "-2xy/3", "vars": ["x", "y"],
        "solution": r"$-\frac{8x^6}{27y^3} \cdot \frac{9y^4}{4x^5} = -\frac{72x^6y^4}{108x^5y^3} = -\frac{2xy}{3}$.",
    },
    {
        "type": "EXPR", "difficulty": 2, "skill": "SOLVE",
        "text": r"Спростіть $\frac{5a + 5b}{a^2} \cdot \frac{a^3}{a^2 - b^2}$.",
        "answer": "5a/(a-b)", "vars": ["a", "b"],
        "solution": r"$\frac{5(a + b) \cdot a^3}{a^2 (a - b)(a + b)} = \frac{5a}{a - b}$.",
    },
    # --- Аналіз ---
    {
        "type": "ERROR", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Оля спрощувала $\frac{x^2 - 9}{x} \cdot \frac{x}{x + 3}$. У якому кроці помилка?",
        "steps": [r"$x^2 - 9 = (x - 3)^2$", r"$\frac{(x - 3)^2 \cdot x}{x(x + 3)}$", r"$= \frac{(x - 3)^2}{x + 3}$"],
        "wrong": 0,
        "solution": r"$x^2 - 9 = (x - 3)(x + 3)$ — різниця квадратів. Тоді вираз дорівнює $x - 3$.",
    },
    {
        "type": "TF", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Правда чи ні (при допустимих значеннях змінних)?",
        "statements": [
            (r"$\frac{a}{b} : \frac{c}{d} = \frac{a}{b} \cdot \frac{d}{c}$", True),
            (r"$\left(\frac{2a}{b^2}\right)^2 = \frac{4a^2}{b^4}$", True),
            (r"$\frac{x - 1}{x} \cdot \frac{x}{1 - x} = 1$", False),
            (r"$\frac{a^2}{b} : a^2 = \frac{1}{b}$", True),
        ],
        "solution": r"Правило ✓. $\frac{4a^2}{b^4}$ ✓. $\frac{x - 1}{1 - x} = -1$. $\frac{a^2}{b} \cdot \frac{1}{a^2} = \frac{1}{b}$ ✓.",
    },
    {
        "type": "GROUP", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Розподіліть вирази за значенням (при допустимих значеннях змінних).",
        "groups": [r"Дорівнює $1$", r"Дорівнює $-1$"],
        "items": [(r"$\frac{a - b}{a} \cdot \frac{a}{a - b}$", 0), (r"$\frac{a - b}{a} \cdot \frac{a}{b - a}$", 1), (r"$\left(\frac{x}{y}\right)^2 : \frac{x^2}{y^2}$", 0), (r"$\left(-\frac{x}{y}\right)^3 : \frac{x^3}{y^3}$", 1), (r"$\frac{x^2 - 1}{x + 1} : (x - 1)$", 0)],
        "solution": r"Скорочуємо: $1$; $\frac{a - b}{b - a} = -1$; $1$; непарний степінь дає $-1$; $\frac{(x - 1)(x + 1)}{(x + 1)(x - 1)} = 1$.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Учень записав: $\frac{x + 2}{x + 5} \cdot \frac{x}{2} = \frac{x(x + 1)}{x + 5}$. Яку помилку він зробив?",
        "options": [(r"«Скоротив» $2$ у сумі $x + 2$", True), ("Помилився в знаку", False), ("Неправильно перемножив знаменники", False), ("Помилки немає", False)],
        "solution": r"Скорочувати можна лише множники. Правильно: $\frac{x(x + 2)}{2(x + 5)}$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Скільки значень $x$ не входять в ОДЗ виразу $\frac{x}{x - 1} : \frac{x + 2}{x - 3}$?",
        "answer": "3",
        "solution": r"$x \ne 1$, $x \ne 3$ (знаменники) і $x \ne -2$ (дільник не нуль) — три значення.",
    },

    # ==========================================
    # СХОДИНКА 3 — ВИСОКИЙ
    # ==========================================
    # --- Моделювання ---
    {
        "type": "EXPR", "difficulty": 3, "skill": "MODEL",
        "text": r"Об'єм прямокутного паралелепіпеда — $\frac{a^3 - a}{2}$, а площа основи — $\frac{a^2 + a}{4}$. Запишіть спрощений вираз для висоти.",
        "answer": "2(a-1)", "vars": ["a"],
        "solution": r"$h = \frac{a(a - 1)(a + 1)}{2} : \frac{a(a + 1)}{4} = \frac{a(a - 1)(a + 1) \cdot 4}{2 \cdot a(a + 1)} = 2(a - 1)$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"Знайдіть значення $\frac{a^2 - b^2}{ab} : \frac{a + b}{b^2}$ при $a = 2$, $b = 6$.",
        "answer": "-12",
        "solution": r"Вираз дорівнює $\frac{(a - b) b}{a}$: $\frac{(2 - 6) \cdot 6}{2} = -12$.",
    },
    {
        "type": "EXPR", "difficulty": 3, "skill": "MODEL",
        "text": r"Робітник виготовляє $\frac{n}{t}$ деталей за годину. Скільки годин він витратить на $\frac{n^2}{2}$ деталей?",
        "answer": "n*t/2", "vars": ["n", "t"],
        "solution": r"$\frac{n^2}{2} : \frac{n}{t} = \frac{n^2 t}{2n} = \frac{nt}{2}$.",
    },
    {
        "type": "MATCH", "difficulty": 3, "skill": "MODEL",
        "text": r"Установіть відповідність між виразом (1–3) та його значенням при $x = 3$ (А–Д).",
        "options": [r"А) $4$", r"Б) $-\frac{1}{3}$", r"В) $-3$", r"Г) $6$", r"Д) $\frac{3}{4}$"],
        "matches": [(r"1. $\frac{x^2 - 1}{x} : \frac{x - 1}{x}$", r"А) $4$"),
                    (r"2. $\frac{x - 2}{x^2} \cdot \frac{x}{2 - x}$", r"Б) $-\frac{1}{3}$"),
                    (r"3. $\frac{2x^2}{x - 1} : \frac{x}{x - 1}$", r"Г) $6$")],
        "solution": r"1) $\frac{(x - 1)(x + 1)}{x} \cdot \frac{x}{x - 1} = x + 1 = 4$. 2) $\frac{x - 2}{2 - x} \cdot \frac{1}{x} = -\frac{1}{x} = -\frac{1}{3}$. 3) $\frac{2x^2}{x - 1} \cdot \frac{x - 1}{x} = 2x = 6$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"Знайдіть значення $\left(\frac{x}{y}\right)^3 \cdot \left(\frac{y^2}{x}\right)^2$ при $x = 5$, $y = 0{,}2$.",
        "answer": "1",
        "solution": r"$\frac{x^3}{y^3} \cdot \frac{y^4}{x^2} = xy = 5 \cdot 0{,}2 = 1$.",
    },
    # --- Розв'язування ---
    {
        "type": "EXPR", "difficulty": 3, "skill": "SOLVE",
        "text": r"Спростіть $\left(\frac{a - b}{a}\right)^2 : \frac{b^2 - a^2}{a^3}$.",
        "answer": "a(b-a)/(a+b)", "vars": ["a", "b"],
        "solution": r"$\frac{(a - b)^2}{a^2} \cdot \frac{a^3}{(b - a)(b + a)} = \frac{a(b - a)}{a + b}$, бо $(a - b)^2 = (b - a)^2$.",
    },
    {
        "type": "EXPR", "difficulty": 3, "skill": "SOLVE",
        "text": r"Спростіть $\frac{x^2 - 6x + 9}{x^2 - 9} \cdot \frac{x + 3}{x}$.",
        "answer": "(x-3)/x", "vars": ["x"],
        "solution": r"$\frac{(x - 3)^2}{(x - 3)(x + 3)} \cdot \frac{x + 3}{x} = \frac{x - 3}{x}$.",
    },
    {
        "type": "EXPR", "difficulty": 3, "skill": "SOLVE",
        "text": r"Спростіть $\frac{a^2 + ab}{b} : \frac{a^2 - b^2}{b^2}$.",
        "answer": "ab/(a-b)", "vars": ["a", "b"],
        "solution": r"$\frac{a(a + b)}{b} \cdot \frac{b^2}{(a - b)(a + b)} = \frac{ab}{a - b}$.",
    },
    {
        "type": "EXPR", "difficulty": 3, "skill": "SOLVE",
        "text": r"Спростіть $\frac{3x - 6}{x + 4} : \frac{x^2 - 4}{2x + 8}$.",
        "answer": "6/(x+2)", "vars": ["x"],
        "solution": r"$\frac{3(x - 2)}{x + 4} \cdot \frac{2(x + 4)}{(x - 2)(x + 2)} = \frac{6}{x + 2}$.",
    },
    {
        "type": "FIELDS", "difficulty": 3, "skill": "SOLVE",
        "text": r"Вираз $\frac{x^3}{y^2} \cdot \left(\frac{y}{x}\right)^4 : \frac{y}{x^2}$ дорівнює $x^m y^k$. Знайдіть:",
        "fields": [("$m =$", "1"), ("$k =$", "1")],
        "solution": r"$\frac{x^3}{y^2} \cdot \frac{y^4}{x^4} \cdot \frac{x^2}{y} = x^{3 - 4 + 2} y^{4 - 2 - 1} = xy$.",
    },
    # --- Аналіз ---
    {
        "type": "ERROR", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Сашко спрощував $\frac{a^2 - 4}{a} : \frac{2 - a}{a^2}$. У якому кроці помилка?",
        "steps": [r"$\frac{(a - 2)(a + 2)}{a} \cdot \frac{a^2}{2 - a}$", r"Скорочуємо $a - 2$ і $2 - a$ як однакові", r"$= a(a + 2)$"],
        "wrong": 1,
        "solution": r"$2 - a = -(a - 2)$, тож після скорочення лишається мінус: $-a(a + 2)$.",
    },
    {
        "type": "TF", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [
            (r"Добуток раціонального дробу і оберненого до нього дорівнює $1$ (де обидва мають зміст)", True),
            (r"Частка двох дробів завжди має ту саму ОДЗ, що й ділене", False),
            (r"$\left(\frac{a}{b}\right)^{2} : \left(\frac{a}{b}\right)^{3} = \frac{b}{a}$", True),
            (r"$\frac{x^2 - 1}{x - 1} = x + 1$ при будь-якому $x$", False),
        ],
        "solution": r"$\frac{a}{b} \cdot \frac{b}{a} = 1$ ✓. У частки додається умова «дільник $\ne 0$». $\frac{a^2}{b^2} \cdot \frac{b^3}{a^3} = \frac{b}{a}$ ✓. При $x = 1$ ліва частина не має змісту.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "ANALYZE",
        "text": r"При якому $k$ рівність $\frac{x^2 - 4}{kx} \cdot \frac{3x}{x + 2} = x - 2$ є тотожністю (при допустимих $x$)?",
        "options": [("3", True), ("1", False), ("-3", False), ("2", False), ("такого $k$ немає", False)],
        "solution": r"Ліва частина: $\frac{(x - 2)(x + 2) \cdot 3x}{kx(x + 2)} = \frac{3(x - 2)}{k}$. Дорівнює $x - 2$, коли $k = 3$.",
    },
    {
        "type": "MULTI", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Які вирази тотожно рівні $\frac{a}{b}$ (при допустимих значеннях)?",
        "options": [(r"$\frac{a^2}{b} : b$", False), (r"$\frac{a^3}{b^2} : \frac{a^2}{b}$", True), (r"$\frac{a}{b^2} \cdot b$", True), (r"$\left(\frac{a}{b}\right)^2 \cdot \frac{b}{a}$", True), (r"$\frac{a + 1}{b + 1}$", False)],
        "solution": r"$\frac{a^2}{b} : b = \frac{a^2}{b^2}$ — ні. $\frac{a^3}{b^2} \cdot \frac{b}{a^2} = \frac{a}{b}$ ✓; $\frac{ab}{b^2} = \frac{a}{b}$ ✓; $\frac{a^2}{b^2} \cdot \frac{b}{a} = \frac{a}{b}$ ✓. Останній — ні: при $a = 1$, $b = 2$ маємо $\frac{2}{3} \ne \frac{1}{2}$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Обчисліть $\frac{1}{2} \cdot \frac{2}{3} \cdot \frac{3}{4} \cdot \ldots \cdot \frac{99}{100}$. Відповідь запишіть десятковим дробом.",
        "answer": "0,01",
        "solution": r"Кожен знаменник скорочується з наступним чисельником: лишається $\frac{1}{100} = 0{,}01$.",
    },

    # ==========================================
    # БОСИ
    # ==========================================
    {
        "type": "SHORT", "difficulty": 4, "skill": "MODEL",
        "text": r"Знайдіть значення $\frac{x^2 - y^2}{x^2 + xy} \cdot \frac{x}{x - y}$ при $x = 1{,}7$, $y = 2{,}3$.",
        "answer": "1",
        "solution": r"$\frac{(x - y)(x + y)}{x(x + y)} \cdot \frac{x}{x - y} = 1$ при всіх допустимих $x$, $y$ — значення не залежить від чисел.",
    },
    {
        "type": "EXPR", "difficulty": 4, "skill": "MODEL",
        "text": r"Басейн об'ємом $\frac{v^2}{3}$ м³ наповнюють зі швидкістю $\frac{v}{6t}$ м³/год. Запишіть спрощений вираз для часу наповнення (у год).",
        "answer": "2v*t", "vars": ["v", "t"],
        "solution": r"$\frac{v^2}{3} : \frac{v}{6t} = \frac{v^2 \cdot 6t}{3v} = 2vt$.",
    },
    {
        "type": "EXPR", "difficulty": 4, "skill": "SOLVE",
        "text": r"Спростіть $\frac{x^2 - 4}{x^2 + 4x + 4} : \frac{x - 2}{x^2 + 2x}$.",
        "answer": "x", "vars": ["x"],
        "solution": r"$\frac{(x - 2)(x + 2)}{(x + 2)^2} \cdot \frac{x(x + 2)}{x - 2} = x$ при $x \ne 0$, $\pm 2$.",
    },
    {
        "type": "EXPR", "difficulty": 4, "skill": "SOLVE",
        "text": r"Спростіть $\frac{a^3 - 8}{a^2 - 4} \cdot \frac{a + 2}{a^2 + 2a + 4}$.",
        "answer": "1", "vars": ["a"],
        "solution": r"$a^3 - 8 = (a - 2)(a^2 + 2a + 4)$: $\frac{(a - 2)(a^2 + 2a + 4)(a + 2)}{(a - 2)(a + 2)(a^2 + 2a + 4)} = 1$.",
    },
    {
        "type": "TF", "difficulty": 4, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [
            (r"$\frac{2}{1} \cdot \frac{3}{2} \cdot \frac{4}{3} \cdot \ldots \cdot \frac{n + 1}{n} = n + 1$", True),
            (r"Якщо $\frac{a}{b} \cdot \frac{c}{d} = 1$, то $\frac{c}{d}$ — обернений до $\frac{a}{b}$", True),
            (r"$\left(\frac{a}{b}\right)^n \cdot \left(\frac{b}{a}\right)^n = 1$ при $a, b \ne 0$", True),
            (r"Частка $\frac{a}{b} : \frac{c}{d}$ має зміст, якщо $b \ne 0$ і $d \ne 0$", False),
        ],
        "solution": r"Скорочується все, крім $n + 1$ ✓. Добуток $1$ — означення оберненого ✓. $\left(\frac{a}{b} \cdot \frac{b}{a}\right)^n = 1$ ✓. Потрібно ще $c \ne 0$.",
    },

    # ==========================================
    # УЛЬТРА-БОСИ
    # ==========================================
    {
        "type": "SHORT", "difficulty": 5, "skill": "SOLVE",
        "text": r"Обчисліть $\left(1 - \frac{1}{4}\right)\left(1 - \frac{1}{9}\right)\left(1 - \frac{1}{16}\right) \cdots \left(1 - \frac{1}{100}\right)$. Відповідь запишіть десятковим дробом.",
        "answer": "0,55",
        "solution": r"$1 - \frac{1}{n^2} = \frac{(n - 1)(n + 1)}{n \cdot n}$. Добуток для $n = 2, \ldots, 10$: $\frac{1 \cdot 2 \cdots 9}{2 \cdot 3 \cdots 10} \cdot \frac{3 \cdot 4 \cdots 11}{2 \cdot 3 \cdots 10} = \frac{1}{10} \cdot \frac{11}{2} = \frac{11}{20} = 0{,}55$.",
    },
    {
        "type": "SHORT", "difficulty": 5, "skill": "MODEL",
        "text": r"Відомо, що $\frac{a}{b} = 3$. Знайдіть значення $\frac{a^2 - b^2}{ab} : \frac{a + b}{b}$.",
        "answer": "2/3",
        "solution": r"Вираз: $\frac{(a - b)(a + b)}{ab} \cdot \frac{b}{a + b} = \frac{a - b}{a} = 1 - \frac{b}{a} = 1 - \frac{1}{3} = \frac{2}{3}$.",
    },
]
