TOPIC_NAME = "2.4. Розв'язування квадратних нерівностей"
COURSE = "Алгебра (7-9 класи)"
GRADE = "9 клас"

TASKS = [
    # ==========================================
    # СХОДИНКА 1 — БАЗОВИЙ
    # ==========================================
    # --- Моделювання ---
    {
        "type": "MULTI", "difficulty": 1, "skill": "MODEL",
        "text": r"Які з нерівностей квадратні?",
        "options": [(r"$x^2 - 4 \gt 0$", True), (r"$2x^2 + x \le 3$", True), (r"$-x^2 \lt 0$", True), (r"$3x - 1 \gt 0$", False), (r"$\frac{1}{x^2} \gt 1$", False)],
        "hint": r"Квадратна: $ax^2 + bx + c$ порівнюємо з нулем (або зводиться до цього), $a \ne 0$.",
        "solution": r"Перші три зводяться до $ax^2 + bx + c \vee 0$. $3x - 1 \gt 0$ — лінійна; з $\frac{1}{x^2}$ — дробова.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "MODEL",
        "text": r"$a \gt 0$, $D \gt 0$, нулі $x_1 \lt x_2$. На якому проміжку $ax^2 + bx + c \lt 0$?",
        "options": [(r"$(x_1;\,x_2)$", True), (r"$(-\infty;\,x_1) \cup (x_2;\,+\infty)$", False), (r"$\mathbb{R}$", False), (r"$\varnothing$", False)],
        "hint": r"Гілки вгору — між нулями парабола під віссю.",
        "solution": r"Між нулями графік нижче від осі $Ox$.",
    },
    {
        "type": "GROUP", "difficulty": 1, "skill": "MODEL",
        "text": r"Чи є число розв'язком нерівності $x^2 - 4 \gt 0$?",
        "groups": [r"Розв'язок", r"Не розв'язок"],
        "items": [(r"$x = 3$", 0), (r"$x = 0$", 1), (r"$x = -5$", 0), (r"$x = 2$", 1), (r"$x = 1$", 1)],
        "hint": r"Підставте: $x^2 - 4$ має бути додатним.",
        "solution": r"$9 - 4 \gt 0$, $25 - 4 \gt 0$ ✓. $0 - 4$, $1 - 4$ — від'ємні; при $x = 2$ вираз $= 0$, а нерівність строга.",
    },
    {
        "type": "MATCH", "difficulty": 1, "skill": "MODEL",
        "text": r"$y = (x - 1)(x - 3)$. Установіть відповідність між нерівністю (1–3) та її розв'язком (А–Д).",
        "options": [r"А) $(-\infty;\,1) \cup (3;\,+\infty)$", r"Б) $(1;\,3)$", r"В) $[1;\,3]$", r"Г) $(-\infty;\,1] \cup [3;\,+\infty)$", r"Д) $\varnothing$"],
        "matches": [(r"1. $y \gt 0$", r"А) $(-\infty;\,1) \cup (3;\,+\infty)$"), (r"2. $y \lt 0$", r"Б) $(1;\,3)$"), (r"3. $y \le 0$", r"В) $[1;\,3]$")],
        "hint": r"Нулі $1$ і $3$, гілки вгору.",
        "solution": r"$\gt 0$ — зовні нулів; $\lt 0$ — між; $\le 0$ — між разом з нулями.",
    },
    {
        "type": "TF", "difficulty": 1, "skill": "MODEL",
        "text": r"Нерівність $x^2 + 1 \gt 0$. Правда чи ні?",
        "statements": [
            (r"Вона виконується при всіх $x$", True),
            (r"$x = 0$ — її розв'язок", True),
            (r"Нерівність $x^2 + 1 \lt 0$ має розв'язки", False),
        ],
        "hint": r"$x^2 \ge 0$, тож $x^2 + 1 \ge 1$.",
        "solution": r"$x^2 + 1 \ge 1 \gt 0$ завжди; тому $x^2 + 1 \lt 0$ розв'язків не має.",
    },
    # --- Розв'язування ---
    {
        "type": "CHOICE", "difficulty": 1, "skill": "SOLVE",
        "text": r"Розв'яжіть нерівність $x^2 - 16 \le 0$.",
        "options": [(r"$[-4;\,4]$", True), (r"$(-4;\,4)$", False), (r"$(-\infty;\,-4] \cup [4;\,+\infty)$", False), (r"$(-\infty;\,4]$", False)],
        "hint": r"Нулі $\pm 4$, нерівність нестрога.",
        "solution": r"Між нулями разом з нулями: $[-4;\,4]$.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "SOLVE",
        "text": r"Розв'яжіть нерівність $x^2 - 3x \gt 0$.",
        "options": [(r"$(-\infty;\,0) \cup (3;\,+\infty)$", True), (r"$(0;\,3)$", False), (r"$(3;\,+\infty)$", False), (r"$[0;\,3]$", False)],
        "hint": r"$x(x - 3) = 0$: нулі $0$ і $3$.",
        "solution": r"Гілки вгору, $\gt 0$ — зовні нулів.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"Скільки цілих розв'язків має нерівність $x^2 - 4 \lt 0$?",
        "answer": "3",
        "hint": r"Розв'язок — $(-2;\,2)$.",
        "solution": r"$-1$, $0$, $1$ — три.",
    },
    {
        "type": "FIELDS", "difficulty": 1, "skill": "SOLVE",
        "text": r"Розв'язок нерівності $(x - 2)(x - 7) \lt 0$ — проміжок $(a;\,b)$. Знайдіть $a$ і $b$.",
        "fields": [(r"$a =$", "2"), (r"$b =$", "7")],
        "hint": r"Нулі $2$ і $7$, гілки вгору.",
        "solution": r"Між нулями: $(2;\,7)$.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "SOLVE",
        "text": r"Розв'яжіть нерівність $x^2 \ge 25$.",
        "options": [(r"$(-\infty;\,-5] \cup [5;\,+\infty)$", True), (r"$[5;\,+\infty)$", False), (r"$[-5;\,5]$", False), (r"$(-\infty;\,-5) \cup (5;\,+\infty)$", False)],
        "hint": r"$x^2 - 25 \ge 0$: нулі $\pm 5$.",
        "solution": r"Зовні нулів разом з нулями.",
    },
    # --- Аналіз ---
    {
        "type": "ERROR", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Петро розв'язує $x^2 - 9 \gt 0$. У якому кроці помилка?",
        "steps": [r"Нулі: $x = \pm 3$", r"$a = 1 \gt 0$ — гілки вгору", r"Відповідь: $(-3;\,3)$"],
        "wrong": 2,
        "hint": r"Де парабола з гілками вгору над віссю?",
        "solution": r"$\gt 0$ — зовні нулів: $(-\infty;\,-3) \cup (3;\,+\infty)$.",
    },
    {
        "type": "MULTI", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Які числа є розв'язками нерівності $x^2 - 5x + 4 \le 0$?",
        "options": [(r"$1$", True), (r"$2$", True), (r"$4$", True), (r"$0$", False), (r"$5$", False)],
        "hint": r"Нулі $1$ і $4$; розв'язок $[1;\,4]$.",
        "solution": r"$[1;\,4]$ містить $1$, $2$, $4$. $0$ і $5$ — зовні.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Оля: «$x^2 \gt 9$, отже, $x \gt 3$». Як правильно?",
        "options": [(r"$x \lt -3$ або $x \gt 3$", True), (r"$x \gt 3$", False), (r"$-3 \lt x \lt 3$", False), (r"$x \gt \pm 3$", False)],
        "hint": r"Чи задовольняє нерівність $x = -4$?",
        "solution": r"$(-4)^2 = 16 \gt 9$. Нулі $\pm 3$, гілки вгору: зовні нулів.",
    },
    {
        "type": "TF", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [
            (r"Нерівність $x^2 \le 0$ має єдиний розв'язок $x = 0$", True),
            (r"Нерівність $x^2 \lt 0$ не має розв'язків", True),
            (r"$x^2 \gt 0$ при всіх $x$", False),
        ],
        "hint": r"А при $x = 0$?",
        "solution": r"$x^2 \ge 0$, рівність лише при $x = 0$. Тому $x^2 \gt 0$ — при $x \ne 0$.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Розв'яжіть нерівність $-x^2 + 1 \gt 0$.",
        "options": [(r"$(-1;\,1)$", True), (r"$(-\infty;\,-1) \cup (1;\,+\infty)$", False), (r"$\mathbb{R}$", False), (r"$\varnothing$", False)],
        "hint": r"Гілки вниз — парабола над віссю між нулями.",
        "solution": r"Нулі $\pm 1$; $a \lt 0$: $\gt 0$ між нулями.",
    },
    # ==========================================
    # СХОДИНКА 2 — СЕРЕДНІЙ
    # ==========================================
    # --- Моделювання ---
    {
        "type": "ORDER", "difficulty": 2, "skill": "MODEL",
        "text": r"Розташуйте кроки розв'язання нерівності $x^2 - 2x - 8 \lt 0$.",
        "items": [
            r"Нулі: $x^2 - 2x - 8 = 0$, $x = -2$, $x = 4$",
            r"Точки $-2$ і $4$ порожні (нерівність строга)",
            r"$a = 1 \gt 0$ — гілки вгору",
            r"$y \lt 0$ між нулями: $(-2;\,4)$",
        ],
        "hint": r"Нулі → точки → напрям гілок → проміжки.",
        "solution": r"Алгоритм з уроку.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "MODEL",
        "text": r"Висота м'яча — $h(t) = -5t^2 + 30t$ м. Скільки секунд м'яч перебував вище за $25$ м?",
        "answer": "4",
        "hint": r"$-5t^2 + 30t \gt 25 \iff t^2 - 6t + 5 \lt 0$.",
        "solution": r"Нулі $1$ і $5$: $1 \lt t \lt 5$ — тривалість $4$ с.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "MODEL",
        "text": r"Периметр прямокутника — $20$ см, площа більша за $21$ см². У яких межах може бути одна зі сторін $x$?",
        "options": [(r"$3 \lt x \lt 7$", True), (r"$0 \lt x \lt 10$", False), (r"$x \gt 7$", False), (r"$x \lt 3$ або $x \gt 7$", False)],
        "hint": r"Сторони $x$ і $10 - x$: $x(10 - x) \gt 21$.",
        "solution": r"$x^2 - 10x + 21 \lt 0$: нулі $3$ і $7$, розв'язок $(3;\,7)$.",
    },
    {
        "type": "FIELDS", "difficulty": 2, "skill": "MODEL",
        "text": r"Область визначення функції $y = \sqrt{x^2 - 4x}$ — $(-\infty;\,a] \cup [b;\,+\infty)$. Знайдіть $a$ і $b$.",
        "fields": [(r"$a =$", "0"), (r"$b =$", "4")],
        "hint": r"Підкореневий вираз невід'ємний: $x^2 - 4x \ge 0$.",
        "solution": r"$x(x - 4) \ge 0$: зовні нулів $0$ і $4$, разом з ними.",
    },
    {
        "type": "TF", "difficulty": 2, "skill": "MODEL",
        "text": r"Функція $y = -x^2 + 6x - 5$ (нулі $1$ і $5$). Правда чи ні?",
        "statements": [
            (r"$y \gt 0$ на $(1;\,5)$", True),
            (r"$y \lt 0$ на $(-\infty;\,1) \cup (5;\,+\infty)$", True),
            (r"$y \ge 0$ на $(-\infty;\,1] \cup [5;\,+\infty)$", False),
        ],
        "hint": r"Гілки вниз.",
        "solution": r"Над віссю — між нулями: $y \ge 0$ на $[1;\,5]$.",
    },
    # --- Розв'язування ---
    {
        "type": "CHOICE", "difficulty": 2, "skill": "SOLVE",
        "text": r"Розв'яжіть нерівність $x^2 - 7x + 10 \ge 0$.",
        "options": [(r"$(-\infty;\,2] \cup [5;\,+\infty)$", True), (r"$[2;\,5]$", False), (r"$(-\infty;\,2) \cup (5;\,+\infty)$", False), (r"$(-\infty;\,-5] \cup [-2;\,+\infty)$", False)],
        "hint": r"Нулі $2$ і $5$.",
        "solution": r"Гілки вгору: зовні нулів разом з ними.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "SOLVE",
        "text": r"Розв'яжіть нерівність $-x^2 + 3x + 4 \gt 0$.",
        "options": [(r"$(-1;\,4)$", True), (r"$(-\infty;\,-1) \cup (4;\,+\infty)$", False), (r"$(-4;\,1)$", False), (r"$[-1;\,4]$", False)],
        "hint": r"Помножте на $-1$: $x^2 - 3x - 4 \lt 0$.",
        "solution": r"Нулі $-1$ і $4$; між нулями.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Скільки цілих розв'язків має нерівність $x^2 - x - 12 \le 0$?",
        "answer": "8",
        "hint": r"Нулі $-3$ і $4$.",
        "solution": r"$[-3;\,4]$: $-3, -2, \ldots, 4$ — вісім чисел.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "SOLVE",
        "text": r"Розв'яжіть нерівність $x^2 - 4x + 4 \le 0$.",
        "options": [(r"$\{2\}$", True), (r"$\varnothing$", False), (r"$\mathbb{R}$", False), (r"$(-\infty;\,2]$", False)],
        "hint": r"$(x - 2)^2 \le 0$.",
        "solution": r"Квадрат не від'ємний, тож лише $(x - 2)^2 = 0$: $x = 2$.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "SOLVE",
        "text": r"Розв'яжіть нерівність $x^2 + 2x + 5 \gt 0$.",
        "options": [(r"$\mathbb{R}$", True), (r"$\varnothing$", False), (r"$(-\infty;\,-1) \cup (-1;\,+\infty)$", False), (r"$(-5;\,+\infty)$", False)],
        "hint": r"$D = 4 - 20 \lt 0$.",
        "solution": r"Нулів немає, $a \gt 0$ — парабола цілком над віссю.",
    },
    # --- Аналіз ---
    {
        "type": "ERROR", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Іра розв'язує $-x^2 + 4x \gt 0$. У якому кроці помилка?",
        "steps": [r"$-x^2 + 4x = 0$: $x = 0$, $x = 4$", r"$a \gt 0$ — гілки вгору", r"Відповідь: $(-\infty;\,0) \cup (4;\,+\infty)$"],
        "wrong": 1,
        "hint": r"Чому дорівнює $a$?",
        "solution": r"$a = -1 \lt 0$ — гілки вниз; $\gt 0$ між нулями: $(0;\,4)$.",
    },
    {
        "type": "MULTI", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Які нерівності виконуються при всіх $x$?",
        "options": [(r"$x^2 + 1 \gt 0$", True), (r"$x^2 - 2x + 1 \ge 0$", True), (r"$-x^2 - 3 \lt 0$", True), (r"$x^2 - 1 \gt 0$", False), (r"$x^2 + x \ge 0$", False)],
        "hint": r"$x^2 - 2x + 1 = (x - 1)^2$.",
        "solution": r"Квадрат невід'ємний; $-x^2 - 3 \le -3$. А $x^2 - 1 \gt 0$ хибне при $x = 0$; $x^2 + x \ge 0$ хибне при $x = -\frac{1}{2}$.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Скільки розв'язків має нерівність $x^2 + 6x + 9 \lt 0$?",
        "options": [(r"Жодного", True), (r"Один", False), (r"Два", False), (r"Безліч", False)],
        "hint": r"$x^2 + 6x + 9 = (x + 3)^2$.",
        "solution": r"$(x + 3)^2 \ge 0$, тож $\lt 0$ — ніколи.",
    },
    {
        "type": "GROUP", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Розподіліть нерівності: мають розв'язки чи ні?",
        "groups": [r"Є розв'язки", r"Розв'язків немає"],
        "items": [(r"$x^2 + 4 \lt 0$", 1), (r"$x^2 - 4 \lt 0$", 0), (r"$(x - 1)^2 \lt 0$", 1), (r"$(x - 1)^2 \le 0$", 0), (r"$-x^2 - 1 \gt 0$", 1)],
        "hint": r"$(x - 1)^2 \le 0$ при $x = 1$.",
        "solution": r"$x^2 - 4 \lt 0$ на $(-2;\,2)$; $(x - 1)^2 \le 0$ при $x = 1$. Решта — розв'язків немає.",
    },
    {
        "type": "TF", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [
            (r"Якщо $a \gt 0$ і $D \lt 0$, розв'язок $ax^2 + bx + c \ge 0$ — усі $x$", True),
            (r"Якщо $a \lt 0$ і $D \lt 0$, нерівність $ax^2 + bx + c \ge 0$ розв'язків не має", True),
            (r"Якщо $a \gt 0$ і $D = 0$, розв'язок $ax^2 + bx + c \gt 0$ — усі $x$", False),
        ],
        "hint": r"При $D = 0$ є одна точка, де вираз дорівнює нулю.",
        "solution": r"При $D = 0$, $a \gt 0$: $\gt 0$ — усі $x$, крім $x_0 = -\frac{b}{2a}$.",
    },
    # ==========================================
    # СХОДИНКА 3 — ПІДВИЩЕНИЙ
    # ==========================================
    # --- Моделювання ---
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"Знайдіть довжину проміжку, на якому функція $y = x^2 - 6x + 8$ набуває від'ємних значень.",
        "answer": "2",
        "hint": r"Нулі $2$ і $4$.",
        "solution": r"$y \lt 0$ на $(2;\,4)$ — довжина $2$.",
    },
    {
        "type": "FIELDS", "difficulty": 3, "skill": "MODEL",
        "text": r"Область визначення функції $y = \sqrt{9 - x^2}$ — відрізок $[a;\,b]$. Знайдіть $a$ і $b$.",
        "fields": [(r"$a =$", "-3"), (r"$b =$", "3")],
        "hint": r"$9 - x^2 \ge 0$.",
        "solution": r"$x^2 \le 9$: $[-3;\,3]$.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "MODEL",
        "text": r"При яких $m$ рівняння $x^2 + mx + 4 = 0$ має два різні корені?",
        "options": [(r"$m \lt -4$ або $m \gt 4$", True), (r"$-4 \lt m \lt 4$", False), (r"$m \gt 4$", False), (r"$m \ne 0$", False)],
        "hint": r"$D = m^2 - 16 \gt 0$.",
        "solution": r"$m^2 \gt 16$: $m \lt -4$ або $m \gt 4$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"Знайдіть найменше натуральне $n$, при якому $n^2 \gt 5n + 14$.",
        "answer": "8",
        "hint": r"$n^2 - 5n - 14 \gt 0$: нулі $-2$ і $7$.",
        "solution": r"$n \lt -2$ або $n \gt 7$; найменше натуральне — $8$.",
    },
    {
        "type": "TF", "difficulty": 3, "skill": "MODEL",
        "text": r"Розв'язок нерівності $x^2 + px + q \lt 0$ — проміжок $(-2;\,5)$. Правда чи ні?",
        "statements": [
            (r"Нулі $x^2 + px + q$ — числа $-2$ і $5$", True),
            (r"$p = -3$", True),
            (r"$q = -10$", True),
            (r"$x = 0$ не є розв'язком", False),
        ],
        "hint": r"$x^2 + px + q = (x + 2)(x - 5)$.",
        "solution": r"$(x + 2)(x - 5) = x^2 - 3x - 10$. $0 \in (-2;\,5)$ — розв'язок.",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Скільки цілих розв'язків має нерівність $2x^2 - 5x - 3 \le 0$?",
        "answer": "4",
        "hint": r"$D = 49$, нулі $-\frac{1}{2}$ і $3$.",
        "solution": r"$\left[-\frac{1}{2};\,3\right]$: $0, 1, 2, 3$ — чотири.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "SOLVE",
        "text": r"Розв'яжіть нерівність $x(x + 4) \ge 5$.",
        "options": [(r"$(-\infty;\,-5] \cup [1;\,+\infty)$", True), (r"$[-5;\,1]$", False), (r"$(-\infty;\,-4] \cup [0;\,+\infty)$", False), (r"$[1;\,+\infty)$", False)],
        "hint": r"Перенесіть $5$ вліво: $x^2 + 4x - 5 \ge 0$.",
        "solution": r"$(x + 5)(x - 1) \ge 0$: зовні нулів $-5$ і $1$.",
    },
    {
        "type": "FIELDS", "difficulty": 3, "skill": "SOLVE",
        "text": r"Розв'язок нерівності $-2x^2 + 8 \ge 0$ — відрізок $[a;\,b]$. Знайдіть $a$ і $b$.",
        "fields": [(r"$a =$", "-2"), (r"$b =$", "2")],
        "hint": r"$x^2 \le 4$.",
        "solution": r"$-2x^2 \ge -8 \iff x^2 \le 4$: $[-2;\,2]$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Знайдіть суму цілих розв'язків нерівності $x^2 - 3x - 10 \lt 0$.",
        "answer": "9",
        "hint": r"Нулі $-2$ і $5$.",
        "solution": r"$(-2;\,5)$: $-1 + 0 + 1 + 2 + 3 + 4 = 9$.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "SOLVE",
        "text": r"Розв'яжіть нерівність $(x - 1)^2 \gt 4$.",
        "options": [(r"$(-\infty;\,-1) \cup (3;\,+\infty)$", True), (r"$(-1;\,3)$", False), (r"$(3;\,+\infty)$", False), (r"$(-\infty;\,-3) \cup (1;\,+\infty)$", False)],
        "hint": r"$x - 1 \gt 2$ або $x - 1 \lt -2$.",
        "solution": r"$x \gt 3$ або $x \lt -1$. Або: $x^2 - 2x - 3 \gt 0$, нулі $-1$ і $3$.",
    },
    # --- Аналіз ---
    {
        "type": "ERROR", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Максим розв'язує $x^2 \lt 3x$. У якому кроці помилка?",
        "steps": [r"$x^2 \lt 3x$", r"Ділимо обидві частини на $x$: $x \lt 3$", r"Відповідь: $(-\infty;\,3)$"],
        "wrong": 1,
        "hint": r"Чи можна ділити нерівність на $x$, знак якого невідомий?",
        "solution": r"$x^2 - 3x \lt 0$, $x(x - 3) \lt 0$: $(0;\,3)$. При $x \lt 0$ ділення змінило б знак.",
    },
    {
        "type": "MULTI", "difficulty": 3, "skill": "ANALYZE",
        "text": r"При яких $c$ нерівність $x^2 + 2x + c \gt 0$ виконується при всіх $x$?",
        "options": [(r"$c = 2$", True), (r"$c = 5$", True), (r"$c = 1{,}5$", True), (r"$c = 1$", False), (r"$c = 0$", False)],
        "hint": r"Потрібно $D = 4 - 4c \lt 0$.",
        "solution": r"$c \gt 1$. При $c = 1$: $(x + 1)^2 \gt 0$ хибне при $x = -1$.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Розв'яжіть нерівність $x^2 \le x$.",
        "options": [(r"$[0;\,1]$", True), (r"$(-\infty;\,1]$", False), (r"$[1;\,+\infty)$", False), (r"$(-\infty;\,0] \cup [1;\,+\infty)$", False)],
        "hint": r"$x^2 - x \le 0$.",
        "solution": r"$x(x - 1) \le 0$: між нулями $0$ і $1$ разом з ними.",
    },
    {
        "type": "TF", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [
            (r"$-x^2 + 2x - 1 \ge 0$ має єдиний розв'язок $x = 1$", True),
            (r"$-x^2 + 2x - 1 \gt 0$ розв'язків не має", True),
            (r"$x^2 - 2x + 1 \gt 0 \iff x \ne 1$", True),
            (r"$x^2 - 2x + 1 \lt 0$ при $x = 1$", False),
        ],
        "hint": r"$-x^2 + 2x - 1 = -(x - 1)^2$.",
        "solution": r"$-(x - 1)^2 \le 0$, рівність при $x = 1$. $(x - 1)^2 = 0$ при $x = 1$ — не менше за нуль.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Знайдіть найбільший цілий розв'язок нерівності $x^2 + 3x - 18 \lt 0$.",
        "answer": "2",
        "hint": r"Нулі $-6$ і $3$.",
        "solution": r"$(-6;\,3)$: найбільше ціле — $2$ ($3$ не входить).",
    },
    # ==========================================
    # БОСИ
    # ==========================================
    {
        "type": "SHORT", "difficulty": 4, "skill": "MODEL",
        "text": r"При ціні квитка $100 + 10k$ грн на концерт приходить $500 - 25k$ глядачів ($k$ — ціле, $0 \le k \le 20$). Скільки значень $k$ дають виторг не менший за $55\,000$ грн?",
        "answer": "5",
        "solution": r"$(100 + 10k)(500 - 25k) \ge 55\,000 \iff k^2 - 10k + 20 \le 0$. Нулі $5 \pm \sqrt{5} \approx 2{,}76$ і $7{,}24$: $k = 3, 4, 5, 6, 7$.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "MODEL",
        "text": r"Одна сторона прямокутника на $3$ м більша за другу, а площа — не менша за $40$ м². Яка найменша можлива довжина меншої сторони (у м)?",
        "answer": "5",
        "solution": r"$x(x + 3) \ge 40 \iff x^2 + 3x - 40 \ge 0 \iff (x + 8)(x - 5) \ge 0$. При $x \gt 0$: $x \ge 5$.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "SOLVE",
        "text": r"Скільки цілих чисел з проміжку $[-5;\,5]$ входять до області визначення функції $y = \sqrt{x^2 - x - 6} + \frac{1}{\sqrt{5 - x}}$?",
        "answer": "6",
        "solution": r"$x^2 - x - 6 \ge 0 \iff x \le -2$ або $x \ge 3$; $5 - x \gt 0 \iff x \lt 5$. Цілі: $-5, -4, -3, -2, 3, 4$ — шість.",
    },
    {
        "type": "FIELDS", "difficulty": 4, "skill": "SOLVE",
        "text": r"Розв'язок нерівності $x^2 + bx + c \le 0$ — відрізок $[-1;\,6]$. Знайдіть $b$ і $c$.",
        "fields": [(r"$b =$", "-5"), (r"$c =$", "-6")],
        "solution": r"$x^2 + bx + c = (x + 1)(x - 6) = x^2 - 5x - 6$.",
    },
    {
        "type": "TF", "difficulty": 4, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [
            (r"Якщо $a \gt 0$ і $c \lt 0$, то $ax^2 + bx + c \lt 0$ має розв'язки", True),
            (r"Якщо $a \lt 0$ і $D \lt 0$, то $ax^2 + bx + c \lt 0$ при всіх $x$", True),
            (r"$x^2 + bx + 1 \gt 0$ при всіх $x$ для будь-якого $b$", False),
            (r"Якщо $x = 0$ — розв'язок $ax^2 + bx + c \gt 0$, то $c \gt 0$", True),
        ],
        "solution": r"При $x = 0$ вираз дорівнює $c \lt 0$ — розв'язок є. $a \lt 0$, $D \lt 0$ — парабола під віссю. При $b = 3$: $D = 5 \gt 0$, є від'ємні значення. Підстановка $x = 0$ дає $c \gt 0$.",
    },
    # ==========================================
    # УЛЬТРА
    # ==========================================
    {
        "type": "SHORT", "difficulty": 5, "skill": "SOLVE",
        "text": r"При скількох цілих значеннях $m$ рівняння $x^2 - 2mx + m + 6 = 0$ не має коренів?",
        "answer": "4",
        "solution": r"$\frac{D}{4} = m^2 - m - 6 \lt 0 \iff (m - 3)(m + 2) \lt 0 \iff -2 \lt m \lt 3$: $m = -1, 0, 1, 2$.",
    },
    {
        "type": "SHORT", "difficulty": 5, "skill": "MODEL",
        "text": r"Сума двох чисел дорівнює $10$, а їх добуток не менший за $21$. Скільки цілих значень може набувати одне з цих чисел?",
        "answer": "5",
        "solution": r"$x(10 - x) \ge 21 \iff x^2 - 10x + 21 \le 0 \iff 3 \le x \le 7$: $3, 4, 5, 6, 7$.",
    },
]
