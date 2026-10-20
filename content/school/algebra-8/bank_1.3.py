TOPIC_NAME = "1.3. Додавання і віднімання раціональних дробів"
COURSE = "Алгебра (7-9 класи)"
GRADE = "8 клас"

TASKS = [
    # ==========================================
    # СХОДИНКА 1 — БАЗОВИЙ
    # ==========================================
    # --- Моделювання ---
    {
        "type": "CHOICE", "difficulty": 1, "skill": "MODEL",
        "text": r"Як додати дроби з однаковими знаменниками $\frac{a}{c}$ і $\frac{b}{c}$?",
        "options": [(r"$\frac{a + b}{c}$", True), (r"$\frac{a + b}{2c}$", False), (r"$\frac{ab}{c}$", False), (r"$\frac{a + b}{c^2}$", False)],
        "hint": r"Знаменник залишається тим самим.",
        "solution": r"$\frac{a}{c} + \frac{b}{c} = \frac{a + b}{c}$ — додаємо чисельники, знаменник не змінюється.",
    },
    {
        "type": "EXPR", "difficulty": 1, "skill": "MODEL",
        "text": r"Перша труба наповнює басейн за $a$ год, друга — за $b$ год. Запишіть вираз для частини басейну, яку обидві труби наповнять разом за $1$ год.",
        "answer": "1/a+1/b", "vars": ["a", "b"],
        "hint": r"За $1$ год перша труба наповнює $\frac{1}{a}$ басейну.",
        "solution": r"Перша — $\frac{1}{a}$, друга — $\frac{1}{b}$; разом $\frac{1}{a} + \frac{1}{b} = \frac{a + b}{ab}$.",
    },
    {
        "type": "TF", "difficulty": 1, "skill": "MODEL",
        "text": r"Правда чи ні?",
        "statements": [
            (r"$\frac{x}{5} + \frac{2x}{5} = \frac{3x}{5}$", True),
            (r"$\frac{a}{b} + \frac{c}{b} = \frac{a + c}{2b}$", False),
            (r"$\frac{7}{y} - \frac{2}{y} = \frac{5}{y}$", True),
        ],
        "hint": r"Знаменники не додають.",
        "solution": r"Перший і третій правильні. У другому знаменник має лишитися $b$: $\frac{a + c}{b}$.",
    },
    {
        "type": "MATCH", "difficulty": 1, "skill": "MODEL",
        "text": r"Установіть відповідність між дробами (1–3) та їхнім найпростішим спільним знаменником (А–Д).",
        "options": [r"А) $6x$", r"Б) $x(x + 1)$", r"В) $x^2$", r"Г) $(x - 1)(x + 1)$", r"Д) $2x + 3x$"],
        "matches": [(r"1. $\frac{1}{2x}$ і $\frac{1}{3x}$", r"А) $6x$"),
                    (r"2. $\frac{1}{x}$ і $\frac{1}{x + 1}$", r"Б) $x(x + 1)$"),
                    (r"3. $\frac{1}{x - 1}$ і $\frac{1}{x + 1}$", r"Г) $(x - 1)(x + 1)$")],
        "hint": r"Спільний знаменник ділиться на кожен зі знаменників.",
        "solution": r"1) Ділиться на $2x$ і $3x$ — $6x$. 2) $x$ і $x + 1$ не мають спільних множників — $x(x + 1)$. 3) Так само — $(x - 1)(x + 1)$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "MODEL",
        "text": r"Перший майстер виконує роботу за $4$ год, другий — за $6$ год. Яку частину роботи вони виконають разом за $1$ год? Відповідь запишіть дробом.",
        "answer": "5/12",
        "hint": r"$\frac{1}{4} + \frac{1}{6}$; спільний знаменник $12$.",
        "solution": r"$\frac{1}{4} + \frac{1}{6} = \frac{3}{12} + \frac{2}{12} = \frac{5}{12}$.",
    },
    # --- Розв'язування ---
    {
        "type": "EXPR", "difficulty": 1, "skill": "SOLVE",
        "text": r"Спростіть $\frac{3a}{7} + \frac{2a}{7}$.",
        "answer": "5a/7", "vars": ["a"],
        "hint": r"Додайте чисельники.",
        "solution": r"$\frac{3a + 2a}{7} = \frac{5a}{7}$.",
    },
    {
        "type": "EXPR", "difficulty": 1, "skill": "SOLVE",
        "text": r"Спростіть $\frac{x + 5}{x} - \frac{5}{x}$.",
        "answer": "1", "vars": ["x"],
        "hint": r"Чисельник: $(x + 5) - 5$.",
        "solution": r"$\frac{x + 5 - 5}{x} = \frac{x}{x} = 1$ при $x \ne 0$.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "SOLVE",
        "text": r"Спростіть $\frac{1}{x} + \frac{1}{2x}$.",
        "options": [(r"$\frac{3}{2x}$", True), (r"$\frac{2}{3x}$", False), (r"$\frac{1}{x}$", False), (r"$\frac{2}{2x^2}$", False)],
        "hint": r"Спільний знаменник — $2x$.",
        "solution": r"$\frac{2}{2x} + \frac{1}{2x} = \frac{3}{2x}$.",
    },
    {
        "type": "EXPR", "difficulty": 1, "skill": "SOLVE",
        "text": r"Спростіть $\frac{a}{3} - \frac{a}{4}$.",
        "answer": "a/12", "vars": ["a"],
        "hint": r"Спільний знаменник $12$.",
        "solution": r"$\frac{4a}{12} - \frac{3a}{12} = \frac{a}{12}$.",
    },
    {
        "type": "EXPR", "difficulty": 1, "skill": "SOLVE",
        "text": r"Спростіть $\frac{2b - 1}{b - 3} - \frac{b + 2}{b - 3}$.",
        "answer": "1", "vars": ["b"],
        "hint": r"Відніміть чисельники в дужках: $(2b - 1) - (b + 2)$.",
        "solution": r"$\frac{2b - 1 - b - 2}{b - 3} = \frac{b - 3}{b - 3} = 1$ при $b \ne 3$.",
    },
    # --- Аналіз ---
    {
        "type": "ERROR", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Петро спрощував $\frac{x}{x - 1} - \frac{x + 1}{x - 1}$. У якому кроці помилка?",
        "steps": [r"Знаменники однакові", r"$\frac{x - x + 1}{x - 1}$", r"$= \frac{1}{x - 1}$"],
        "wrong": 1,
        "hint": r"Мінус перед дробом стосується всього чисельника.",
        "solution": r"$x - (x + 1) = x - x - 1 = -1$, тож результат $-\frac{1}{x - 1}$.",
    },
    {
        "type": "MULTI", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Які рівності правильні (при допустимих значеннях змінних)?",
        "options": [(r"$\frac{a}{2} + \frac{a}{2} = a$", True), (r"$\frac{1}{a} + \frac{1}{b} = \frac{2}{a + b}$", False), (r"$\frac{3}{x} - \frac{1}{x} = \frac{2}{x}$", True), (r"$\frac{x}{y} + \frac{y}{x} = 1$", False)],
        "hint": r"Перевірте контрприкладом: $a = b = 1$, $x = y = 1$.",
        "solution": r"Перша і третя правильні. $\frac{1}{1} + \frac{1}{1} = 2 \ne 1$; $\frac{1}{1} + \frac{1}{1} = 2 \ne 1$.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "ANALYZE",
        "text": r"При якому значенні $x$ вираз $\frac{1}{x} + \frac{1}{x - 4}$ не має змісту?",
        "options": [(r"$x = 0$ і $x = 4$", True), (r"лише $x = 0$", False), (r"лише $x = 4$", False), (r"$x = 2$", False)],
        "hint": r"Коли знаменник дорівнює нулю?",
        "solution": r"Знаменники $x$ і $x - 4$ дорівнюють нулю при $x = 0$ і $x = 4$.",
    },
    {
        "type": "TF", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [
            (r"$y - x = -(x - y)$", True),
            (r"$\frac{a}{b - a} = \frac{a}{a - b}$", False),
            (r"$\frac{a}{b - a} = -\frac{a}{a - b}$", True),
        ],
        "hint": r"Згадайте, як міняються знаки у протилежних виразах.",
        "solution": r"$b - a = -(a - b)$, тож $\frac{a}{b - a} = -\frac{a}{a - b}$. Друга рівність хибна: знак загубили.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Тарас записав $\frac{x + 3}{x} = 3$, «скоротивши» $x$. Чому так не можна?",
        "options": [("Скорочують лише множники, а не доданки", True), (r"Бо $x$ може дорівнювати $3$", False), ("Бо в чисельнику дві змінні", False), ("Так можна, помилки немає", False)],
        "hint": r"Перевірте при $x = 1$.",
        "solution": r"При $x = 1$: $\frac{4}{1} = 4 \ne 3$. Правильно: $\frac{x + 3}{x} = 1 + \frac{3}{x}$.",
    },

    # ==========================================
    # СХОДИНКА 2 — СЕРЕДНІЙ
    # ==========================================
    # --- Моделювання ---
    {
        "type": "EXPR", "difficulty": 2, "skill": "MODEL",
        "text": r"Човен пройшов $12$ км за течією зі швидкістю $v + 2$ км/год і повернувся проти течії зі швидкістю $v - 2$ км/год. Запишіть вираз для часу всієї поїздки (у год).",
        "answer": "12/(v+2)+12/(v-2)", "vars": ["v"],
        "hint": r"Час — це відстань, поділена на швидкість.",
        "solution": r"$\frac{12}{v + 2} + \frac{12}{v - 2} = \frac{12(v - 2) + 12(v + 2)}{v^2 - 4} = \frac{24v}{v^2 - 4}$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "MODEL",
        "text": r"Вираз для часу поїздки човна: $\frac{24v}{v^2 - 4}$ год. Скільки годин триває поїздка, якщо власна швидкість човна $v = 10$ км/год?",
        "answer": "2,5",
        "hint": r"Підставте $v = 10$.",
        "solution": r"$\frac{240}{100 - 4} = \frac{240}{96} = 2{,}5$ год. Перевірка: $\frac{12}{12} + \frac{12}{8} = 1 + 1{,}5$ ✓.",
    },
    {
        "type": "MATCH", "difficulty": 2, "skill": "MODEL",
        "text": r"Установіть відповідність між сумою (1–3) та її спрощеним виглядом (А–Д).",
        "options": [r"А) $\frac{a + b}{ab}$", r"Б) $\frac{2a}{a^2 - 1}$", r"В) $\frac{2}{a}$", r"Г) $\frac{1}{a(a + 1)}$", r"Д) $\frac{a^2 + b^2}{ab}$"],
        "matches": [(r"1. $\frac{1}{a} + \frac{1}{b}$", r"А) $\frac{a + b}{ab}$"),
                    (r"2. $\frac{1}{a - 1} + \frac{1}{a + 1}$", r"Б) $\frac{2a}{a^2 - 1}$"),
                    (r"3. $\frac{a}{b} + \frac{b}{a}$", r"Д) $\frac{a^2 + b^2}{ab}$")],
        "hint": r"Зведіть кожну суму до спільного знаменника.",
        "solution": r"1) $\frac{b + a}{ab}$. 2) $\frac{(a + 1) + (a - 1)}{(a - 1)(a + 1)} = \frac{2a}{a^2 - 1}$. 3) $\frac{a^2 + b^2}{ab}$.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "MODEL",
        "text": r"Який найпростіший спільний знаменник дробів $\frac{3}{x^2 - 4}$ і $\frac{1}{x + 2}$?",
        "options": [(r"$(x - 2)(x + 2)$", True), (r"$(x^2 - 4)(x + 2)$", False), (r"$x + 2$", False), (r"$x^2 + 2$", False)],
        "hint": r"Розкладіть $x^2 - 4$ на множники.",
        "solution": r"$x^2 - 4 = (x - 2)(x + 2)$ уже ділиться на $x + 2$, тому досить $(x - 2)(x + 2)$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "MODEL",
        "text": r"Знайдіть значення виразу $\frac{1}{x} - \frac{1}{x + 1}$ при $x = 4$. Відповідь запишіть дробом.",
        "answer": "1/20",
        "hint": r"Вираз дорівнює $\frac{1}{x(x + 1)}$.",
        "solution": r"$\frac{1}{4 \cdot 5} = \frac{1}{20}$. Перевірка: $\frac{1}{4} - \frac{1}{5} = \frac{5 - 4}{20}$ ✓.",
    },
    # --- Розв'язування ---
    {
        "type": "EXPR", "difficulty": 2, "skill": "SOLVE",
        "text": r"Спростіть $\frac{3}{x} - \frac{2}{x + 1}$.",
        "answer": "(x+3)/(x(x+1))", "vars": ["x"],
        "solution": r"$\frac{3(x + 1) - 2x}{x(x + 1)} = \frac{x + 3}{x(x + 1)}$.",
    },
    {
        "type": "EXPR", "difficulty": 2, "skill": "SOLVE",
        "text": r"Спростіть $\frac{2}{x - 3} - \frac{12}{x^2 - 9}$.",
        "answer": "2/(x+3)", "vars": ["x"],
        "solution": r"$\frac{2(x + 3) - 12}{(x - 3)(x + 3)} = \frac{2x - 6}{(x - 3)(x + 3)} = \frac{2}{x + 3}$.",
    },
    {
        "type": "EXPR", "difficulty": 2, "skill": "SOLVE",
        "text": r"Спростіть $\frac{a}{a - b} + \frac{b}{b - a}$.",
        "answer": "1", "vars": ["a", "b"],
        "solution": r"$\frac{b}{b - a} = -\frac{b}{a - b}$, тож $\frac{a - b}{a - b} = 1$ при $a \ne b$.",
    },
    {
        "type": "EXPR", "difficulty": 2, "skill": "SOLVE",
        "text": r"Спростіть $\frac{x}{2y} - \frac{y}{3x}$.",
        "answer": "(3x^2-2y^2)/(6xy)", "vars": ["x", "y"],
        "solution": r"Спільний знаменник $6xy$: $\frac{3x \cdot x - 2y \cdot y}{6xy} = \frac{3x^2 - 2y^2}{6xy}$.",
    },
    {
        "type": "FIELDS", "difficulty": 2, "skill": "SOLVE",
        "text": r"Подайте $\frac{5}{a} + \frac{3}{a^2}$ у вигляді дробу $\frac{pa + q}{a^2}$. Знайдіть:",
        "fields": [("$p =$", "5"), ("$q =$", "3")],
        "solution": r"$\frac{5a}{a^2} + \frac{3}{a^2} = \frac{5a + 3}{a^2}$: $p = 5$, $q = 3$.",
    },
    # --- Аналіз ---
    {
        "type": "ERROR", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Оля спрощувала $\frac{1}{x} + \frac{1}{x + 2}$. У якому кроці помилка?",
        "steps": [r"Спільний знаменник $x(x + 2)$", r"$\frac{1 + 1}{x(x + 2)}$", r"$= \frac{2}{x(x + 2)}$"],
        "wrong": 1,
        "hint": r"А додаткові множники?",
        "solution": r"Чисельники треба домножити: $\frac{(x + 2) + x}{x(x + 2)} = \frac{2x + 2}{x(x + 2)}$.",
    },
    {
        "type": "TF", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Правда чи ні (при допустимих значеннях змінних)?",
        "statements": [
            (r"$\frac{1}{n} - \frac{1}{n + 1} = \frac{1}{n(n + 1)}$", True),
            (r"$\frac{a}{b} - \frac{b}{a} = \frac{a - b}{ab}$", False),
            (r"$\frac{x}{x - 2} - \frac{2}{x - 2} = 1$", True),
            (r"$\frac{1}{a} + \frac{1}{a} = \frac{1}{2a}$", False),
        ],
        "solution": r"$\frac{(n + 1) - n}{n(n + 1)} = \frac{1}{n(n + 1)}$ ✓. $\frac{a}{b} - \frac{b}{a} = \frac{a^2 - b^2}{ab}$. $\frac{x - 2}{x - 2} = 1$ ✓. $\frac{1}{a} + \frac{1}{a} = \frac{2}{a}$.",
    },
    {
        "type": "GROUP", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Розподіліть вирази за значенням (при допустимих значеннях змінних).",
        "groups": [r"Дорівнює $1$", r"Дорівнює $-1$"],
        "items": [(r"$\frac{a}{a - b} - \frac{b}{a - b}$", 0), (r"$\frac{a}{b - a} + \frac{b}{a - b}$", 1), (r"$\frac{x + 1}{x} - \frac{1}{x}$", 0), (r"$\frac{3}{3 - y} + \frac{y}{y - 3}$", 0), (r"$\frac{x}{1 - x} + \frac{1}{x - 1}$", 1)],
        "solution": r"$\frac{a - b}{a - b} = 1$; $\frac{-a + b}{a - b} = -1$; $\frac{x}{x} = 1$; $\frac{3 - y}{3 - y} = 1$ (бо $\frac{y}{y - 3} = -\frac{y}{3 - y}$); $\frac{x - 1}{1 - x} = -1$.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Яка з рівностей є тотожністю?",
        "options": [(r"$\frac{1}{x} - \frac{1}{y} = \frac{y - x}{xy}$", True), (r"$\frac{1}{x} - \frac{1}{y} = \frac{x - y}{xy}$", False), (r"$\frac{1}{x} - \frac{1}{y} = \frac{1}{x - y}$", False), (r"$\frac{1}{x} - \frac{1}{y} = 0$", False)],
        "solution": r"$\frac{y}{xy} - \frac{x}{xy} = \frac{y - x}{xy}$. Інші спростовує $x = 1$, $y = 2$: $\frac{1}{2}$, а не $-\frac{1}{2}$, $-1$ чи $0$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Обчисліть $\frac{1}{1 \cdot 2} + \frac{1}{2 \cdot 3} + \frac{1}{3 \cdot 4}$. Відповідь запишіть дробом.",
        "answer": "3/4",
        "solution": r"$\frac{1}{n(n + 1)} = \frac{1}{n} - \frac{1}{n + 1}$: $\left(1 - \frac{1}{2}\right) + \left(\frac{1}{2} - \frac{1}{3}\right) + \left(\frac{1}{3} - \frac{1}{4}\right) = 1 - \frac{1}{4} = \frac{3}{4}$.",
    },

    # ==========================================
    # СХОДИНКА 3 — ВИСОКИЙ
    # ==========================================
    # --- Моделювання ---
    {
        "type": "EXPR", "difficulty": 3, "skill": "MODEL",
        "text": r"Перший робітник виконує завдання за $t$ год, а другий — на $3$ год довше. Запишіть спрощений вираз для частини завдання, яку вони виконають разом за $1$ год.",
        "answer": "(2t+3)/(t(t+3))", "vars": ["t"],
        "solution": r"$\frac{1}{t} + \frac{1}{t + 3} = \frac{t + 3 + t}{t(t + 3)} = \frac{2t + 3}{t(t + 3)}$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"Перший робітник виконує завдання за $6$ год, другий — за $3$ год. За скільки годин вони виконають завдання разом?",
        "answer": "2",
        "solution": r"Разом за $1$ год: $\frac{1}{6} + \frac{1}{3} = \frac{1}{6} + \frac{2}{6} = \frac{1}{2}$ завдання. Усе — за $2$ год.",
    },
    {
        "type": "EXPR", "difficulty": 3, "skill": "MODEL",
        "text": r"Автомобіль проїхав $120$ км зі швидкістю $v$ км/год і ще $60$ км зі швидкістю $2v$ км/год. Запишіть спрощений вираз для часу всієї поїздки.",
        "answer": "150/v", "vars": ["v"],
        "solution": r"$\frac{120}{v} + \frac{60}{2v} = \frac{120}{v} + \frac{30}{v} = \frac{150}{v}$.",
    },
    {
        "type": "MATCH", "difficulty": 3, "skill": "MODEL",
        "text": r"Установіть відповідність між виразом (1–3) та його значенням при $x = 2$ (А–Д).",
        "options": [r"А) $\frac{1}{2}$", r"Б) $\frac{5}{4}$", r"В) $1$", r"Г) $\frac{1}{6}$", r"Д) $2$"],
        "matches": [(r"1. $\frac{1}{x} - \frac{1}{x + 1}$", r"Г) $\frac{1}{6}$"),
                    (r"2. $\frac{x}{x + 2} + \frac{2}{x + 2}$", r"В) $1$"),
                    (r"3. $\frac{x + 1}{x} - \frac{1}{x^2}$", r"Б) $\frac{5}{4}$")],
        "solution": r"1) $\frac{1}{2} - \frac{1}{3} = \frac{1}{6}$. 2) $\frac{x + 2}{x + 2} = 1$. 3) $\frac{3}{2} - \frac{1}{4} = \frac{5}{4}$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"Сума двох чисел, обернених до сусідніх натуральних чисел $n$ і $n + 1$, дорівнює $\frac{9}{20}$. Знайдіть $n$.",
        "answer": "4",
        "solution": r"$\frac{1}{n} + \frac{1}{n + 1} = \frac{2n + 1}{n(n + 1)}$. При $n = 4$: $\frac{9}{20}$ ✓.",
    },
    # --- Розв'язування ---
    {
        "type": "EXPR", "difficulty": 3, "skill": "SOLVE",
        "text": r"Спростіть $\frac{x}{x - 2} - \frac{4}{x^2 - 2x}$.",
        "answer": "(x+2)/x", "vars": ["x"],
        "solution": r"$x^2 - 2x = x(x - 2)$: $\frac{x^2 - 4}{x(x - 2)} = \frac{(x - 2)(x + 2)}{x(x - 2)} = \frac{x + 2}{x}$.",
    },
    {
        "type": "EXPR", "difficulty": 3, "skill": "SOLVE",
        "text": r"Спростіть $\frac{1}{a - 1} - \frac{1}{a + 1} - \frac{2}{a^2 - 1}$.",
        "answer": "0", "vars": ["a"],
        "solution": r"Спільний знаменник $a^2 - 1$: $\frac{(a + 1) - (a - 1) - 2}{a^2 - 1} = \frac{0}{a^2 - 1} = 0$ при $a \ne \pm 1$.",
    },
    {
        "type": "EXPR", "difficulty": 3, "skill": "SOLVE",
        "text": r"Спростіть $\frac{a + 3}{a^2 - 3a} - \frac{a - 3}{a^2 + 3a}$.",
        "answer": "12/(a^2-9)", "vars": ["a"],
        "solution": r"Знаменники $a(a - 3)$ і $a(a + 3)$; спільний $a(a^2 - 9)$. Чисельник: $(a + 3)^2 - (a - 3)^2 = 12a$. Результат $\frac{12a}{a(a^2 - 9)} = \frac{12}{a^2 - 9}$.",
    },
    {
        "type": "EXPR", "difficulty": 3, "skill": "SOLVE",
        "text": r"Подайте у вигляді дробу: $x + 1 - \frac{x^2}{x - 1}$.",
        "answer": "-1/(x-1)", "vars": ["x"],
        "solution": r"$\frac{(x + 1)(x - 1) - x^2}{x - 1} = \frac{x^2 - 1 - x^2}{x - 1} = -\frac{1}{x - 1}$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Знайдіть значення виразу $\frac{a}{a - b} - \frac{b}{a + b}$ при $a = 3$, $b = 1$. Відповідь запишіть дробом.",
        "answer": "5/4",
        "solution": r"$\frac{3}{2} - \frac{1}{4} = \frac{6}{4} - \frac{1}{4} = \frac{5}{4}$.",
    },
    # --- Аналіз ---
    {
        "type": "ERROR", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Сашко спрощував $\frac{3}{x^2 - 4} + \frac{1}{x + 2}$. У якому кроці помилка?",
        "steps": [r"Спільний знаменник $(x - 2)(x + 2)$", r"$\frac{3 + (x + 2)}{(x - 2)(x + 2)}$", r"$= \frac{x + 5}{x^2 - 4}$"],
        "wrong": 1,
        "solution": r"Додатковий множник другого дробу — $x - 2$: $\frac{3 + (x - 2)}{(x - 2)(x + 2)} = \frac{x + 1}{x^2 - 4}$.",
    },
    {
        "type": "TF", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [
            (r"Сума двох дробів може бути цілим виразом", True),
            (r"$\frac{a}{b} + \frac{c}{d} = \frac{ad + bc}{bd}$ при $b \ne 0$, $d \ne 0$", True),
            (r"Вираз $\frac{1}{x - 1} + \frac{1}{1 - x}$ дорівнює $\frac{2}{x - 1}$", False),
            (r"ОДЗ виразу $\frac{1}{x} + \frac{1}{x^2 - 1}$ — усі $x$, крім $0$ і $\pm 1$", True),
        ],
        "solution": r"Наприклад, $\frac{x}{x - 1} - \frac{1}{x - 1} = 1$ ✓. Загальне правило ✓. $\frac{1}{1 - x} = -\frac{1}{x - 1}$, тож сума $0$. Знаменники $x$ і $(x - 1)(x + 1)$ ✓.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "ANALYZE",
        "text": r"При якому значенні $k$ рівність $\frac{2}{x} + \frac{k}{x + 1} = \frac{5x + 2}{x(x + 1)}$ є тотожністю?",
        "options": [("3", True), ("5", False), ("2", False), ("-3", False), ("такого $k$ немає", False)],
        "solution": r"Ліва частина: $\frac{2(x + 1) + kx}{x(x + 1)} = \frac{(2 + k)x + 2}{x(x + 1)}$. Потрібно $2 + k = 5$, $k = 3$.",
    },
    {
        "type": "MULTI", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Які вирази тотожно рівні $\frac{2}{x^2 - 1}$ (при допустимих $x$)?",
        "options": [(r"$\frac{1}{x - 1} - \frac{1}{x + 1}$", True), (r"$\frac{1}{x + 1} - \frac{1}{x - 1}$", False), (r"$\frac{2}{(x - 1)(x + 1)}$", True), (r"$\frac{1}{x - 1} + \frac{1}{x + 1}$", False), (r"$-\frac{2}{1 - x^2}$", True)],
        "solution": r"$\frac{(x + 1) - (x - 1)}{x^2 - 1} = \frac{2}{x^2 - 1}$ ✓; другий — з протилежним знаком; третій ✓; четвертий — $\frac{2x}{x^2 - 1}$; $1 - x^2 = -(x^2 - 1)$ ✓.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Обчисліть $\frac{1}{1 \cdot 2} + \frac{1}{2 \cdot 3} + \ldots + \frac{1}{9 \cdot 10}$. Відповідь запишіть десятковим дробом.",
        "answer": "0,9",
        "solution": r"Кожен доданок — $\frac{1}{n} - \frac{1}{n + 1}$; сума «складається»: $1 - \frac{1}{10} = 0{,}9$.",
    },

    # ==========================================
    # БОСИ
    # ==========================================
    {
        "type": "SHORT", "difficulty": 4, "skill": "MODEL",
        "text": r"Катер пройшов $15$ км за течією і $15$ км проти течії. Швидкість течії — $2$ км/год, власна швидкість катера — $8$ км/год. Скільки годин тривала поїздка?",
        "answer": "4",
        "solution": r"$\frac{15}{8 + 2} + \frac{15}{8 - 2} = 1{,}5 + 2{,}5 = 4$ год. Загальна формула: $\frac{15}{v + 2} + \frac{15}{v - 2} = \frac{30v}{v^2 - 4}$, при $v = 8$: $\frac{240}{60} = 4$ ✓.",
    },
    {
        "type": "EXPR", "difficulty": 4, "skill": "MODEL",
        "text": r"Три труби наповнюють басейн окремо за $a$, $2a$ і $3a$ год. Запишіть спрощений вираз для частини басейну, яку вони наповнять разом за $1$ год.",
        "answer": "11/(6a)", "vars": ["a"],
        "solution": r"$\frac{1}{a} + \frac{1}{2a} + \frac{1}{3a} = \frac{6 + 3 + 2}{6a} = \frac{11}{6a}$.",
    },
    {
        "type": "EXPR", "difficulty": 4, "skill": "SOLVE",
        "text": r"Спростіть $\frac{1}{x(x + 1)} + \frac{1}{(x + 1)(x + 2)} + \frac{1}{(x + 2)(x + 3)}$.",
        "answer": "3/(x(x+3))", "vars": ["x"],
        "solution": r"Кожен доданок: $\frac{1}{x} - \frac{1}{x + 1}$, $\frac{1}{x + 1} - \frac{1}{x + 2}$, $\frac{1}{x + 2} - \frac{1}{x + 3}$. Сума: $\frac{1}{x} - \frac{1}{x + 3} = \frac{3}{x(x + 3)}$.",
    },
    {
        "type": "EXPR", "difficulty": 4, "skill": "SOLVE",
        "text": r"Спростіть $\frac{4}{a^2 - 4} - \frac{1}{a - 2} + \frac{1}{a + 2}$.",
        "answer": "0", "vars": ["a"],
        "solution": r"$\frac{4 - (a + 2) + (a - 2)}{a^2 - 4} = \frac{0}{a^2 - 4} = 0$ при $a \ne \pm 2$.",
    },
    {
        "type": "TF", "difficulty": 4, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [
            (r"Для будь-якого $n \ge 1$: $\frac{1}{1 \cdot 2} + \ldots + \frac{1}{n(n + 1)} = \frac{n}{n + 1}$", True),
            (r"Існують додатні $a$ і $b$, для яких $\frac{1}{a} + \frac{1}{b} = \frac{1}{a + b}$", False),
            (r"$\frac{a}{b} + \frac{b}{a} \ge 2$ для всіх $a, b \gt 0$", True),
            (r"Різниця дробів $\frac{1}{n} - \frac{1}{n + 1}$ спадає зі зростанням натурального $n$", True),
        ],
        "solution": r"Сума «складається» до $1 - \frac{1}{n + 1}$ ✓. Рівність $\frac{a + b}{ab} = \frac{1}{a + b}$ дає $(a + b)^2 = ab$, але $(a + b)^2 = a^2 + 2ab + b^2 \gt ab$ для додатних. $\frac{a^2 + b^2}{ab} - 2 = \frac{(a - b)^2}{ab} \ge 0$ ✓. $\frac{1}{n(n + 1)}$ спадає ✓.",
    },

    # ==========================================
    # УЛЬТРА-БОСИ
    # ==========================================
    {
        "type": "SHORT", "difficulty": 5, "skill": "SOLVE",
        "text": r"Обчисліть $\frac{1}{1 \cdot 3} + \frac{1}{3 \cdot 5} + \frac{1}{5 \cdot 7} + \ldots + \frac{1}{19 \cdot 21}$. Відповідь запишіть дробом.",
        "answer": "10/21",
        "solution": r"$\frac{1}{n(n + 2)} = \frac{1}{2}\left(\frac{1}{n} - \frac{1}{n + 2}\right)$. Сума: $\frac{1}{2}\left(1 - \frac{1}{21}\right) = \frac{1}{2} \cdot \frac{20}{21} = \frac{10}{21}$.",
    },
    {
        "type": "SHORT", "difficulty": 5, "skill": "MODEL",
        "text": r"Двоє робітників разом виконують завдання за $4$ год. Перший сам виконав би його на $6$ год швидше, ніж другий. За скільки годин виконує завдання перший робітник сам?",
        "answer": "6",
        "solution": r"Нехай перший — за $t$ год, другий — за $t + 6$. Разом за годину: $\frac{1}{t} + \frac{1}{t + 6} = \frac{1}{4}$. Перевірка $t = 6$: $\frac{1}{6} + \frac{1}{12} = \frac{3}{12} = \frac{1}{4}$ ✓.",
    },
]
