TOPIC_NAME = "2.1. Властивості функцій (зростання, спадання, нулі, проміжки знакосталості)"
COURSE = "Алгебра (7-9 класи)"
GRADE = "9 клас"

TASKS = [
    # ==========================================
    # СХОДИНКА 1 — БАЗОВИЙ
    # ==========================================
    # --- Моделювання ---
    {
        "type": "CHOICE", "difficulty": 1, "skill": "MODEL",
        "text": r"На рисунку — графік функції $y = f(x)$, заданої на проміжку $[-5;\,5]$. Скільки нулів має функція?",
        "svg_code": '<svg xmlns="http://www.w3.org/2000/svg" width="340" height="290" viewBox="0 0 340 290" fill="none" stroke="currentColor" stroke-width="1" font-family="sans-serif"><line x1="20" y1="270" x2="20" y2="20" stroke-opacity="0.18"/><line x1="45" y1="270" x2="45" y2="20" stroke-opacity="0.18"/><line x1="70" y1="270" x2="70" y2="20" stroke-opacity="0.18"/><line x1="95" y1="270" x2="95" y2="20" stroke-opacity="0.18"/><line x1="120" y1="270" x2="120" y2="20" stroke-opacity="0.18"/><line x1="145" y1="270" x2="145" y2="20" stroke-opacity="0.18"/><line x1="170" y1="270" x2="170" y2="20" stroke-opacity="0.18"/><line x1="195" y1="270" x2="195" y2="20" stroke-opacity="0.18"/><line x1="220" y1="270" x2="220" y2="20" stroke-opacity="0.18"/><line x1="245" y1="270" x2="245" y2="20" stroke-opacity="0.18"/><line x1="270" y1="270" x2="270" y2="20" stroke-opacity="0.18"/><line x1="295" y1="270" x2="295" y2="20" stroke-opacity="0.18"/><line x1="320" y1="270" x2="320" y2="20" stroke-opacity="0.18"/><line x1="20" y1="270" x2="320" y2="270" stroke-opacity="0.18"/><line x1="20" y1="245" x2="320" y2="245" stroke-opacity="0.18"/><line x1="20" y1="220" x2="320" y2="220" stroke-opacity="0.18"/><line x1="20" y1="195" x2="320" y2="195" stroke-opacity="0.18"/><line x1="20" y1="170" x2="320" y2="170" stroke-opacity="0.18"/><line x1="20" y1="145" x2="320" y2="145" stroke-opacity="0.18"/><line x1="20" y1="120" x2="320" y2="120" stroke-opacity="0.18"/><line x1="20" y1="95" x2="320" y2="95" stroke-opacity="0.18"/><line x1="20" y1="70" x2="320" y2="70" stroke-opacity="0.18"/><line x1="20" y1="45" x2="320" y2="45" stroke-opacity="0.18"/><line x1="20" y1="20" x2="320" y2="20" stroke-opacity="0.18"/><line x1="12" y1="145" x2="332" y2="145" stroke-width="1.8"/><line x1="170" y1="262" x2="170" y2="8" stroke-width="1.8"/><path d="M332 145 l-9 -4 v8 z" fill="currentColor" stroke="none"/><path d="M170 8 l-4 9 h8 z" fill="currentColor" stroke="none"/><text x="326" y="163" fill="currentColor" stroke="none" font-size="13" font-style="italic">x</text><text x="178" y="18" fill="currentColor" stroke="none" font-size="13" font-style="italic">y</text><text x="160" y="160" fill="currentColor" stroke="none" font-size="13">0</text><text x="195" y="160" fill="currentColor" stroke="none" font-size="13" text-anchor="middle">1</text><text x="176" y="125" fill="currentColor" stroke="none" font-size="13">1</text><polyline points="45,195 120,45 220,245 295,95" stroke-width="3" stroke-linejoin="round"/><circle cx="45" cy="195" r="4" fill="currentColor" stroke="none"/><circle cx="295" cy="95" r="4" fill="currentColor" stroke="none"/></svg>',
        "options": [(r"$3$", True), (r"$2$", False), (r"$4$", False), (r"$1$", False)],
        "hint": r"Нуль — абсциса точки перетину графіка з віссю $Ox$.",
        "solution": r"Графік перетинає вісь $Ox$ у точках з абсцисами $-4$, $0$, $4$ — три нулі.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "MODEL",
        "text": r"Що означає «функція $f$ зростає на проміжку»?",
        "options": [(r"Для будь-яких $x_1 \lt x_2$ з проміжку $f(x_1) \lt f(x_2)$", True),
                    (r"Для будь-яких $x_1 \lt x_2$ з проміжку $f(x_1) \gt f(x_2)$", False),
                    (r"$f(x) \gt 0$ на цьому проміжку", False),
                    (r"Графік лежить вище осі $Ox$", False)],
        "hint": r"Більшому аргументу — …",
        "solution": r"Зростає — більшому значенню $x$ відповідає більше значення функції. Додатність — це знакосталість, а не зростання.",
    },
    {
        "type": "GROUP", "difficulty": 1, "skill": "MODEL",
        "text": r"Розподіліть лінійні функції: зростають чи спадають на $\mathbb{R}$?",
        "groups": [r"Зростає на $\mathbb{R}$", r"Спадає на $\mathbb{R}$"],
        "items": [(r"$y = 3x - 1$", 0), (r"$y = -2x + 5$", 1), (r"$y = 0{,}5x$", 0), (r"$y = 4 - x$", 1), (r"$y = \frac{x}{3} + 2$", 0)],
        "hint": r"Дивіться на знак кутового коефіцієнта $k$.",
        "solution": r"$k \gt 0$: $3$, $0{,}5$, $\frac{1}{3}$ — зростають. $k \lt 0$: $-2$, $-1$ — спадають.",
    },
    {
        "type": "MATCH", "difficulty": 1, "skill": "MODEL",
        "text": r"Установіть відповідність між поняттям (1–3) та його описом (А–Д).",
        "options": [r"А) розв'язки рівняння $f(x) = 0$", r"Б) графік лежить вище осі $Ox$", r"В) з $x_1 \lt x_2$ випливає $f(x_1) \lt f(x_2)$",
                    r"Г) з $x_1 \lt x_2$ випливає $f(x_1) \gt f(x_2)$", r"Д) графік лежить нижче осі $Ox$"],
        "matches": [("1. Нулі функції", r"А) розв'язки рівняння $f(x) = 0$"),
                    (r"2. Проміжок, де $f(x) \gt 0$", r"Б) графік лежить вище осі $Ox$"),
                    ("3. Функція зростає", r"В) з $x_1 \lt x_2$ випливає $f(x_1) \lt f(x_2)$")],
        "hint": r"Знак функції — положення графіка відносно $Ox$; монотонність — порівняння значень.",
        "solution": r"Нулі — $f(x) = 0$; $f(x) \gt 0$ — графік вище $Ox$; зростання — більшому $x$ більше $f(x)$.",
    },
    {
        "type": "TF", "difficulty": 1, "skill": "MODEL",
        "text": r"Функція $y = 2x - 6$. Правда чи ні?",
        "statements": [
            (r"$x = 3$ — нуль функції", True),
            (r"Точка $(0;\,-6)$ — нуль функції", False),
            (r"Графік перетинає вісь $Ox$ у точці $(3;\,0)$", True),
        ],
        "hint": r"Нуль — це значення $x$, при якому $y = 0$.",
        "solution": r"$2x - 6 = 0 \Rightarrow x = 3$. Точка $(0;\,-6)$ — перетин з віссю $Oy$, а нуль — число, не точка.",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"Знайдіть нуль функції $y = 3x - 12$.",
        "answer": "4",
        "hint": r"Розв'яжіть рівняння $3x - 12 = 0$.",
        "solution": r"$3x = 12$, $x = 4$.",
    },
    {
        "type": "FIELDS", "difficulty": 1, "skill": "SOLVE",
        "text": r"Знайдіть нулі функції $y = x^2 - 16$.",
        "fields": [(r"$x_1 =$", "-4"), (r"$x_2 =$", "4")],
        "unordered": True,
        "hint": r"$x^2 = 16$ має два корені.",
        "solution": r"$x^2 = 16$, $x = -4$ або $x = 4$.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "SOLVE",
        "text": r"На якому проміжку функція $y = 5 - x$ набуває додатних значень?",
        "options": [(r"$(-\infty;\,5)$", True), (r"$(5;\,+\infty)$", False), (r"$(-\infty;\,5]$", False), (r"$(-5;\,+\infty)$", False)],
        "hint": r"Розв'яжіть нерівність $5 - x \gt 0$.",
        "solution": r"$5 - x \gt 0 \Rightarrow x \lt 5$. У нулі $x = 5$ значення не додатне — дужка кругла.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "SOLVE",
        "text": r"За графіком функції $y = f(x)$ укажіть проміжок спадання.",
        "svg_code": '<svg xmlns="http://www.w3.org/2000/svg" width="340" height="290" viewBox="0 0 340 290" fill="none" stroke="currentColor" stroke-width="1" font-family="sans-serif"><line x1="20" y1="270" x2="20" y2="20" stroke-opacity="0.18"/><line x1="45" y1="270" x2="45" y2="20" stroke-opacity="0.18"/><line x1="70" y1="270" x2="70" y2="20" stroke-opacity="0.18"/><line x1="95" y1="270" x2="95" y2="20" stroke-opacity="0.18"/><line x1="120" y1="270" x2="120" y2="20" stroke-opacity="0.18"/><line x1="145" y1="270" x2="145" y2="20" stroke-opacity="0.18"/><line x1="170" y1="270" x2="170" y2="20" stroke-opacity="0.18"/><line x1="195" y1="270" x2="195" y2="20" stroke-opacity="0.18"/><line x1="220" y1="270" x2="220" y2="20" stroke-opacity="0.18"/><line x1="245" y1="270" x2="245" y2="20" stroke-opacity="0.18"/><line x1="270" y1="270" x2="270" y2="20" stroke-opacity="0.18"/><line x1="295" y1="270" x2="295" y2="20" stroke-opacity="0.18"/><line x1="320" y1="270" x2="320" y2="20" stroke-opacity="0.18"/><line x1="20" y1="270" x2="320" y2="270" stroke-opacity="0.18"/><line x1="20" y1="245" x2="320" y2="245" stroke-opacity="0.18"/><line x1="20" y1="220" x2="320" y2="220" stroke-opacity="0.18"/><line x1="20" y1="195" x2="320" y2="195" stroke-opacity="0.18"/><line x1="20" y1="170" x2="320" y2="170" stroke-opacity="0.18"/><line x1="20" y1="145" x2="320" y2="145" stroke-opacity="0.18"/><line x1="20" y1="120" x2="320" y2="120" stroke-opacity="0.18"/><line x1="20" y1="95" x2="320" y2="95" stroke-opacity="0.18"/><line x1="20" y1="70" x2="320" y2="70" stroke-opacity="0.18"/><line x1="20" y1="45" x2="320" y2="45" stroke-opacity="0.18"/><line x1="20" y1="20" x2="320" y2="20" stroke-opacity="0.18"/><line x1="12" y1="145" x2="332" y2="145" stroke-width="1.8"/><line x1="170" y1="262" x2="170" y2="8" stroke-width="1.8"/><path d="M332 145 l-9 -4 v8 z" fill="currentColor" stroke="none"/><path d="M170 8 l-4 9 h8 z" fill="currentColor" stroke="none"/><text x="326" y="163" fill="currentColor" stroke="none" font-size="13" font-style="italic">x</text><text x="178" y="18" fill="currentColor" stroke="none" font-size="13" font-style="italic">y</text><text x="160" y="160" fill="currentColor" stroke="none" font-size="13">0</text><text x="195" y="160" fill="currentColor" stroke="none" font-size="13" text-anchor="middle">1</text><text x="176" y="125" fill="currentColor" stroke="none" font-size="13">1</text><polyline points="45,195 120,45 220,245 295,95" stroke-width="3" stroke-linejoin="round"/><circle cx="45" cy="195" r="4" fill="currentColor" stroke="none"/><circle cx="295" cy="95" r="4" fill="currentColor" stroke="none"/></svg>',
        "options": [(r"$[-2;\,2]$", True), (r"$[-4;\,4]$", False), (r"$[-5;\,-2]$", False), (r"$[2;\,5]$", False), (r"$[-4;\,0]$", False)],
        "hint": r"Читаємо графік зліва направо: де він іде вниз?",
        "solution": r"Від $x = -2$ до $x = 2$ графік іде вниз — спадає на $[-2;\,2]$. На $[-5;\,-2]$ і $[2;\,5]$ — зростає.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"Скільки нулів має функція $y = x^2 + 1$?",
        "answer": "0",
        "hint": r"Чи може $x^2 + 1$ дорівнювати нулю?",
        "solution": r"$x^2 \ge 0$, тож $x^2 + 1 \ge 1 \gt 0$ — нулів немає.",
    },
    # --- Аналіз результатів ---
    {
        "type": "ERROR", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Оля шукала нуль функції $y = 2x + 10$. У якому кроці помилка?",
        "steps": [r"$2x + 10 = 0$", r"$2x = -10$", r"$x = 5$"],
        "wrong": 2,
        "hint": r"Перевірте знак після ділення.",
        "solution": r"$x = -10 : 2 = -5$. Перевірка: $2 \cdot (-5) + 10 = 0$ ✓.",
    },
    {
        "type": "MULTI", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Які функції спадають на $\mathbb{R}$?",
        "options": [(r"$y = -3x + 1$", True), (r"$y = 2x - 7$", False), (r"$y = -x$", True), (r"$y = 5$", False), (r"$y = 4 - 0{,}5x$", True)],
        "hint": r"Спадає, якщо $k \lt 0$.",
        "solution": r"$k = -3$, $-1$, $-0{,}5$ — спадають. $y = 2x - 7$ зростає, $y = 5$ — стала (не зростає й не спадає).",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Петро каже: «Нуль функції $y = 4x - 8$ — це $y = -8$». Яка відповідь правильна?",
        "options": [(r"$x = 2$", True), (r"$(0;\,-8)$", False), (r"$x = -2$", False), (r"$x = 8$", False)],
        "hint": r"Нуль функції — значення $x$, а не $y$.",
        "solution": r"$4x - 8 = 0 \Rightarrow x = 2$. $-8$ — значення функції при $x = 0$.",
    },
    {
        "type": "TF", "difficulty": 1, "skill": "ANALYZE",
        "text": r"За графіком функції $y = f(x)$. Правда чи ні?",
        "svg_code": '<svg xmlns="http://www.w3.org/2000/svg" width="340" height="290" viewBox="0 0 340 290" fill="none" stroke="currentColor" stroke-width="1" font-family="sans-serif"><line x1="20" y1="270" x2="20" y2="20" stroke-opacity="0.18"/><line x1="45" y1="270" x2="45" y2="20" stroke-opacity="0.18"/><line x1="70" y1="270" x2="70" y2="20" stroke-opacity="0.18"/><line x1="95" y1="270" x2="95" y2="20" stroke-opacity="0.18"/><line x1="120" y1="270" x2="120" y2="20" stroke-opacity="0.18"/><line x1="145" y1="270" x2="145" y2="20" stroke-opacity="0.18"/><line x1="170" y1="270" x2="170" y2="20" stroke-opacity="0.18"/><line x1="195" y1="270" x2="195" y2="20" stroke-opacity="0.18"/><line x1="220" y1="270" x2="220" y2="20" stroke-opacity="0.18"/><line x1="245" y1="270" x2="245" y2="20" stroke-opacity="0.18"/><line x1="270" y1="270" x2="270" y2="20" stroke-opacity="0.18"/><line x1="295" y1="270" x2="295" y2="20" stroke-opacity="0.18"/><line x1="320" y1="270" x2="320" y2="20" stroke-opacity="0.18"/><line x1="20" y1="270" x2="320" y2="270" stroke-opacity="0.18"/><line x1="20" y1="245" x2="320" y2="245" stroke-opacity="0.18"/><line x1="20" y1="220" x2="320" y2="220" stroke-opacity="0.18"/><line x1="20" y1="195" x2="320" y2="195" stroke-opacity="0.18"/><line x1="20" y1="170" x2="320" y2="170" stroke-opacity="0.18"/><line x1="20" y1="145" x2="320" y2="145" stroke-opacity="0.18"/><line x1="20" y1="120" x2="320" y2="120" stroke-opacity="0.18"/><line x1="20" y1="95" x2="320" y2="95" stroke-opacity="0.18"/><line x1="20" y1="70" x2="320" y2="70" stroke-opacity="0.18"/><line x1="20" y1="45" x2="320" y2="45" stroke-opacity="0.18"/><line x1="20" y1="20" x2="320" y2="20" stroke-opacity="0.18"/><line x1="12" y1="145" x2="332" y2="145" stroke-width="1.8"/><line x1="170" y1="262" x2="170" y2="8" stroke-width="1.8"/><path d="M332 145 l-9 -4 v8 z" fill="currentColor" stroke="none"/><path d="M170 8 l-4 9 h8 z" fill="currentColor" stroke="none"/><text x="326" y="163" fill="currentColor" stroke="none" font-size="13" font-style="italic">x</text><text x="178" y="18" fill="currentColor" stroke="none" font-size="13" font-style="italic">y</text><text x="160" y="160" fill="currentColor" stroke="none" font-size="13">0</text><text x="195" y="160" fill="currentColor" stroke="none" font-size="13" text-anchor="middle">1</text><text x="176" y="125" fill="currentColor" stroke="none" font-size="13">1</text><polyline points="45,195 120,45 220,245 295,95" stroke-width="3" stroke-linejoin="round"/><circle cx="45" cy="195" r="4" fill="currentColor" stroke="none"/><circle cx="295" cy="95" r="4" fill="currentColor" stroke="none"/></svg>',
        "statements": [
            (r"$f(x) \gt 0$ на проміжку $(-4;\,0)$", True),
            (r"Функція зростає на $[-5;\,-2]$", True),
            (r"Найбільше значення функції дорівнює $5$", False),
        ],
        "hint": r"Найбільше значення — це $y$ найвищої точки графіка.",
        "solution": r"На $(-4;\,0)$ графік вище $Ox$ ✓. На $[-5;\,-2]$ іде вгору ✓. Найвища точка $(-2;\,4)$ — найбільше значення $4$, а $5$ — кінець області визначення.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Ярина: «Функція $y = \frac{1}{x}$ спадає на всій області визначення». Чи права вона?",
        "options": [(r"Ні: спадає на $(-\infty;\,0)$ і на $(0;\,+\infty)$ окремо", True), ("Так", False), ("Ні: вона зростає", False), ("Ні: вона стала", False)],
        "hint": r"Порівняйте $f(-1)$ і $f(1)$.",
        "solution": r"$-1 \lt 1$, а $f(-1) = -1 \lt f(1) = 1$ — на всій $D$ не спадає. Спадає на кожному з проміжків окремо.",
    },

    # ==========================================
    # СХОДИНКА 2 — СЕРЕДНІЙ
    # ==========================================
    # --- Моделювання ---
    {
        "type": "FIELDS", "difficulty": 2, "skill": "MODEL",
        "text": r"На рисунку — графік функції $y = g(x)$, заданої на $[-3;\,4]$. Знайдіть нулі функції.",
        "svg_code": '<svg xmlns="http://www.w3.org/2000/svg" width="340" height="290" viewBox="0 0 340 290" fill="none" stroke="currentColor" stroke-width="1" font-family="sans-serif"><line x1="20" y1="270" x2="20" y2="20" stroke-opacity="0.18"/><line x1="45" y1="270" x2="45" y2="20" stroke-opacity="0.18"/><line x1="70" y1="270" x2="70" y2="20" stroke-opacity="0.18"/><line x1="95" y1="270" x2="95" y2="20" stroke-opacity="0.18"/><line x1="120" y1="270" x2="120" y2="20" stroke-opacity="0.18"/><line x1="145" y1="270" x2="145" y2="20" stroke-opacity="0.18"/><line x1="170" y1="270" x2="170" y2="20" stroke-opacity="0.18"/><line x1="195" y1="270" x2="195" y2="20" stroke-opacity="0.18"/><line x1="220" y1="270" x2="220" y2="20" stroke-opacity="0.18"/><line x1="245" y1="270" x2="245" y2="20" stroke-opacity="0.18"/><line x1="270" y1="270" x2="270" y2="20" stroke-opacity="0.18"/><line x1="295" y1="270" x2="295" y2="20" stroke-opacity="0.18"/><line x1="320" y1="270" x2="320" y2="20" stroke-opacity="0.18"/><line x1="20" y1="270" x2="320" y2="270" stroke-opacity="0.18"/><line x1="20" y1="245" x2="320" y2="245" stroke-opacity="0.18"/><line x1="20" y1="220" x2="320" y2="220" stroke-opacity="0.18"/><line x1="20" y1="195" x2="320" y2="195" stroke-opacity="0.18"/><line x1="20" y1="170" x2="320" y2="170" stroke-opacity="0.18"/><line x1="20" y1="145" x2="320" y2="145" stroke-opacity="0.18"/><line x1="20" y1="120" x2="320" y2="120" stroke-opacity="0.18"/><line x1="20" y1="95" x2="320" y2="95" stroke-opacity="0.18"/><line x1="20" y1="70" x2="320" y2="70" stroke-opacity="0.18"/><line x1="20" y1="45" x2="320" y2="45" stroke-opacity="0.18"/><line x1="20" y1="20" x2="320" y2="20" stroke-opacity="0.18"/><line x1="12" y1="145" x2="332" y2="145" stroke-width="1.8"/><line x1="170" y1="262" x2="170" y2="8" stroke-width="1.8"/><path d="M332 145 l-9 -4 v8 z" fill="currentColor" stroke="none"/><path d="M170 8 l-4 9 h8 z" fill="currentColor" stroke="none"/><text x="326" y="163" fill="currentColor" stroke="none" font-size="13" font-style="italic">x</text><text x="178" y="18" fill="currentColor" stroke="none" font-size="13" font-style="italic">y</text><text x="160" y="160" fill="currentColor" stroke="none" font-size="13">0</text><text x="195" y="160" fill="currentColor" stroke="none" font-size="13" text-anchor="middle">1</text><text x="176" y="125" fill="currentColor" stroke="none" font-size="13">1</text><polyline points="95,195 170,45 270,245" stroke-width="3" stroke-linejoin="round"/><circle cx="95" cy="195" r="4" fill="currentColor" stroke="none"/><circle cx="270" cy="245" r="4" fill="currentColor" stroke="none"/></svg>',
        "fields": [(r"$x_1 =$", "-2"), (r"$x_2 =$", "2")],
        "unordered": True,
        "hint": r"Шукайте точки, де графік перетинає вісь $Ox$.",
        "solution": r"Графік перетинає $Ox$ у точках $(-2;\,0)$ і $(2;\,0)$: нулі $-2$ і $2$.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "MODEL",
        "text": r"За графіком функції $y = g(x)$ укажіть проміжок зростання.",
        "svg_code": '<svg xmlns="http://www.w3.org/2000/svg" width="340" height="290" viewBox="0 0 340 290" fill="none" stroke="currentColor" stroke-width="1" font-family="sans-serif"><line x1="20" y1="270" x2="20" y2="20" stroke-opacity="0.18"/><line x1="45" y1="270" x2="45" y2="20" stroke-opacity="0.18"/><line x1="70" y1="270" x2="70" y2="20" stroke-opacity="0.18"/><line x1="95" y1="270" x2="95" y2="20" stroke-opacity="0.18"/><line x1="120" y1="270" x2="120" y2="20" stroke-opacity="0.18"/><line x1="145" y1="270" x2="145" y2="20" stroke-opacity="0.18"/><line x1="170" y1="270" x2="170" y2="20" stroke-opacity="0.18"/><line x1="195" y1="270" x2="195" y2="20" stroke-opacity="0.18"/><line x1="220" y1="270" x2="220" y2="20" stroke-opacity="0.18"/><line x1="245" y1="270" x2="245" y2="20" stroke-opacity="0.18"/><line x1="270" y1="270" x2="270" y2="20" stroke-opacity="0.18"/><line x1="295" y1="270" x2="295" y2="20" stroke-opacity="0.18"/><line x1="320" y1="270" x2="320" y2="20" stroke-opacity="0.18"/><line x1="20" y1="270" x2="320" y2="270" stroke-opacity="0.18"/><line x1="20" y1="245" x2="320" y2="245" stroke-opacity="0.18"/><line x1="20" y1="220" x2="320" y2="220" stroke-opacity="0.18"/><line x1="20" y1="195" x2="320" y2="195" stroke-opacity="0.18"/><line x1="20" y1="170" x2="320" y2="170" stroke-opacity="0.18"/><line x1="20" y1="145" x2="320" y2="145" stroke-opacity="0.18"/><line x1="20" y1="120" x2="320" y2="120" stroke-opacity="0.18"/><line x1="20" y1="95" x2="320" y2="95" stroke-opacity="0.18"/><line x1="20" y1="70" x2="320" y2="70" stroke-opacity="0.18"/><line x1="20" y1="45" x2="320" y2="45" stroke-opacity="0.18"/><line x1="20" y1="20" x2="320" y2="20" stroke-opacity="0.18"/><line x1="12" y1="145" x2="332" y2="145" stroke-width="1.8"/><line x1="170" y1="262" x2="170" y2="8" stroke-width="1.8"/><path d="M332 145 l-9 -4 v8 z" fill="currentColor" stroke="none"/><path d="M170 8 l-4 9 h8 z" fill="currentColor" stroke="none"/><text x="326" y="163" fill="currentColor" stroke="none" font-size="13" font-style="italic">x</text><text x="178" y="18" fill="currentColor" stroke="none" font-size="13" font-style="italic">y</text><text x="160" y="160" fill="currentColor" stroke="none" font-size="13">0</text><text x="195" y="160" fill="currentColor" stroke="none" font-size="13" text-anchor="middle">1</text><text x="176" y="125" fill="currentColor" stroke="none" font-size="13">1</text><polyline points="95,195 170,45 270,245" stroke-width="3" stroke-linejoin="round"/><circle cx="95" cy="195" r="4" fill="currentColor" stroke="none"/><circle cx="270" cy="245" r="4" fill="currentColor" stroke="none"/></svg>',
        "options": [(r"$[-3;\,0]$", True), (r"$[-2;\,2]$", False), (r"$[0;\,4]$", False), (r"$[-3;\,4]$", False), (r"$[-2;\,4]$", False)],
        "hint": r"Зростання — графік іде вгору зліва направо.",
        "solution": r"Від $x = -3$ до $x = 0$ графік іде вгору: зростає на $[-3;\,0]$, далі спадає.",
    },
    {
        "type": "MATCH", "difficulty": 2, "skill": "MODEL",
        "text": r"За графіком функції $y = f(x)$ установіть відповідність між властивістю (1–3) та відповіддю (А–Д).",
        "svg_code": '<svg xmlns="http://www.w3.org/2000/svg" width="340" height="290" viewBox="0 0 340 290" fill="none" stroke="currentColor" stroke-width="1" font-family="sans-serif"><line x1="20" y1="270" x2="20" y2="20" stroke-opacity="0.18"/><line x1="45" y1="270" x2="45" y2="20" stroke-opacity="0.18"/><line x1="70" y1="270" x2="70" y2="20" stroke-opacity="0.18"/><line x1="95" y1="270" x2="95" y2="20" stroke-opacity="0.18"/><line x1="120" y1="270" x2="120" y2="20" stroke-opacity="0.18"/><line x1="145" y1="270" x2="145" y2="20" stroke-opacity="0.18"/><line x1="170" y1="270" x2="170" y2="20" stroke-opacity="0.18"/><line x1="195" y1="270" x2="195" y2="20" stroke-opacity="0.18"/><line x1="220" y1="270" x2="220" y2="20" stroke-opacity="0.18"/><line x1="245" y1="270" x2="245" y2="20" stroke-opacity="0.18"/><line x1="270" y1="270" x2="270" y2="20" stroke-opacity="0.18"/><line x1="295" y1="270" x2="295" y2="20" stroke-opacity="0.18"/><line x1="320" y1="270" x2="320" y2="20" stroke-opacity="0.18"/><line x1="20" y1="270" x2="320" y2="270" stroke-opacity="0.18"/><line x1="20" y1="245" x2="320" y2="245" stroke-opacity="0.18"/><line x1="20" y1="220" x2="320" y2="220" stroke-opacity="0.18"/><line x1="20" y1="195" x2="320" y2="195" stroke-opacity="0.18"/><line x1="20" y1="170" x2="320" y2="170" stroke-opacity="0.18"/><line x1="20" y1="145" x2="320" y2="145" stroke-opacity="0.18"/><line x1="20" y1="120" x2="320" y2="120" stroke-opacity="0.18"/><line x1="20" y1="95" x2="320" y2="95" stroke-opacity="0.18"/><line x1="20" y1="70" x2="320" y2="70" stroke-opacity="0.18"/><line x1="20" y1="45" x2="320" y2="45" stroke-opacity="0.18"/><line x1="20" y1="20" x2="320" y2="20" stroke-opacity="0.18"/><line x1="12" y1="145" x2="332" y2="145" stroke-width="1.8"/><line x1="170" y1="262" x2="170" y2="8" stroke-width="1.8"/><path d="M332 145 l-9 -4 v8 z" fill="currentColor" stroke="none"/><path d="M170 8 l-4 9 h8 z" fill="currentColor" stroke="none"/><text x="326" y="163" fill="currentColor" stroke="none" font-size="13" font-style="italic">x</text><text x="178" y="18" fill="currentColor" stroke="none" font-size="13" font-style="italic">y</text><text x="160" y="160" fill="currentColor" stroke="none" font-size="13">0</text><text x="195" y="160" fill="currentColor" stroke="none" font-size="13" text-anchor="middle">1</text><text x="176" y="125" fill="currentColor" stroke="none" font-size="13">1</text><polyline points="45,195 120,45 220,245 295,95" stroke-width="3" stroke-linejoin="round"/><circle cx="45" cy="195" r="4" fill="currentColor" stroke="none"/><circle cx="295" cy="95" r="4" fill="currentColor" stroke="none"/></svg>',
        "options": [r"А) $-4;\ 0;\ 4$", r"Б) $[-2;\,2]$", r"В) $[-5;\,-4) \cup (0;\,4)$", r"Г) $(-4;\,0) \cup (4;\,5]$", r"Д) $[-4;\,4]$"],
        "matches": [("1. Нулі функції", r"А) $-4;\ 0;\ 4$"), ("2. Проміжок спадання", r"Б) $[-2;\,2]$"),
                    (r"3. Проміжки, де $f(x) \lt 0$", r"В) $[-5;\,-4) \cup (0;\,4)$")],
        "hint": r"$f(x) \lt 0$ — графік нижче осі $Ox$.",
        "solution": r"Нулі $-4, 0, 4$. Спадає на $[-2;\,2]$. Нижче $Ox$ — на $[-5;\,-4)$ і $(0;\,4)$; Г — це проміжки, де $f(x) \gt 0$, Д — множина значень.",
    },
    {
        "type": "ORDER", "difficulty": 2, "skill": "MODEL",
        "text": r"Розташуйте кроки дослідження функції $f(x) = 3x + 6$ у правильному порядку.",
        "items": [
            r"$D(f) = \mathbb{R}$",
            r"Нуль: $3x + 6 = 0$, $x = -2$",
            r"$f(x) \gt 0$ при $x \gt -2$, $\;f(x) \lt 0$ при $x \lt -2$",
            r"$k = 3 \gt 0$ — зростає на $\mathbb{R}$",
        ],
        "hint": r"Область визначення → нулі → знак → монотонність.",
        "solution": r"Це алгоритм дослідження: $D(f)$, нулі, знак, монотонність.",
    },
    {
        "type": "GROUP", "difficulty": 2, "skill": "MODEL",
        "text": r"За графіком функції $y = g(x)$ визначте знак $g(x)$ у кожній точці.",
        "svg_code": '<svg xmlns="http://www.w3.org/2000/svg" width="340" height="290" viewBox="0 0 340 290" fill="none" stroke="currentColor" stroke-width="1" font-family="sans-serif"><line x1="20" y1="270" x2="20" y2="20" stroke-opacity="0.18"/><line x1="45" y1="270" x2="45" y2="20" stroke-opacity="0.18"/><line x1="70" y1="270" x2="70" y2="20" stroke-opacity="0.18"/><line x1="95" y1="270" x2="95" y2="20" stroke-opacity="0.18"/><line x1="120" y1="270" x2="120" y2="20" stroke-opacity="0.18"/><line x1="145" y1="270" x2="145" y2="20" stroke-opacity="0.18"/><line x1="170" y1="270" x2="170" y2="20" stroke-opacity="0.18"/><line x1="195" y1="270" x2="195" y2="20" stroke-opacity="0.18"/><line x1="220" y1="270" x2="220" y2="20" stroke-opacity="0.18"/><line x1="245" y1="270" x2="245" y2="20" stroke-opacity="0.18"/><line x1="270" y1="270" x2="270" y2="20" stroke-opacity="0.18"/><line x1="295" y1="270" x2="295" y2="20" stroke-opacity="0.18"/><line x1="320" y1="270" x2="320" y2="20" stroke-opacity="0.18"/><line x1="20" y1="270" x2="320" y2="270" stroke-opacity="0.18"/><line x1="20" y1="245" x2="320" y2="245" stroke-opacity="0.18"/><line x1="20" y1="220" x2="320" y2="220" stroke-opacity="0.18"/><line x1="20" y1="195" x2="320" y2="195" stroke-opacity="0.18"/><line x1="20" y1="170" x2="320" y2="170" stroke-opacity="0.18"/><line x1="20" y1="145" x2="320" y2="145" stroke-opacity="0.18"/><line x1="20" y1="120" x2="320" y2="120" stroke-opacity="0.18"/><line x1="20" y1="95" x2="320" y2="95" stroke-opacity="0.18"/><line x1="20" y1="70" x2="320" y2="70" stroke-opacity="0.18"/><line x1="20" y1="45" x2="320" y2="45" stroke-opacity="0.18"/><line x1="20" y1="20" x2="320" y2="20" stroke-opacity="0.18"/><line x1="12" y1="145" x2="332" y2="145" stroke-width="1.8"/><line x1="170" y1="262" x2="170" y2="8" stroke-width="1.8"/><path d="M332 145 l-9 -4 v8 z" fill="currentColor" stroke="none"/><path d="M170 8 l-4 9 h8 z" fill="currentColor" stroke="none"/><text x="326" y="163" fill="currentColor" stroke="none" font-size="13" font-style="italic">x</text><text x="178" y="18" fill="currentColor" stroke="none" font-size="13" font-style="italic">y</text><text x="160" y="160" fill="currentColor" stroke="none" font-size="13">0</text><text x="195" y="160" fill="currentColor" stroke="none" font-size="13" text-anchor="middle">1</text><text x="176" y="125" fill="currentColor" stroke="none" font-size="13">1</text><polyline points="95,195 170,45 270,245" stroke-width="3" stroke-linejoin="round"/><circle cx="95" cy="195" r="4" fill="currentColor" stroke="none"/><circle cx="270" cy="245" r="4" fill="currentColor" stroke="none"/></svg>',
        "groups": [r"$g(x) \gt 0$", r"$g(x) \lt 0$"],
        "items": [(r"$x = -3$", 1), (r"$x = -1$", 0), (r"$x = 0$", 0), (r"$x = 1$", 0), (r"$x = 3$", 1), (r"$x = 4$", 1)],
        "hint": r"Знак додатний між нулями $-2$ і $2$.",
        "solution": r"$g(x) \gt 0$ на $(-2;\,2)$: $x = -1, 0, 1$. Решта точок — де графік нижче $Ox$.",
    },
    # --- Розв'язування ---
    {
        "type": "FIELDS", "difficulty": 2, "skill": "SOLVE",
        "text": r"Знайдіть нулі функції $y = x^2 - 4x$.",
        "fields": [(r"$x_1 =$", "0"), (r"$x_2 =$", "4")],
        "unordered": True,
        "hint": r"Винесіть $x$ за дужки.",
        "solution": r"$x(x - 4) = 0$: $x = 0$ або $x = 4$.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "SOLVE",
        "text": r"Укажіть усі значення $x$, при яких функція $y = \sqrt{x} - 3$ набуває від'ємних значень.",
        "options": [(r"$[0;\,9)$", True), (r"$(-\infty;\,9)$", False), (r"$(0;\,9)$", False), (r"$[0;\,3)$", False), (r"$(9;\,+\infty)$", False)],
        "hint": r"Не забудьте про область визначення кореня.",
        "solution": r"$D = [0;\,+\infty)$. $\sqrt{x} \lt 3 \Rightarrow 0 \le x \lt 9$. При $x = 0$: $y = -3 \lt 0$ — нуль входить.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Знайдіть суму нулів функції $y = (x - 3)(x + 5)$.",
        "answer": "-2",
        "hint": r"Добуток дорівнює нулю, коли один із множників — нуль.",
        "solution": r"Нулі $3$ і $-5$; сума $-2$.",
    },
    {
        "type": "TF", "difficulty": 2, "skill": "SOLVE",
        "text": r"Функція $y = -2x + 6$. Правда чи ні?",
        "statements": [
            (r"$y \ge 0$ на $(-\infty;\,3]$", True),
            (r"$y \lt 0$ на $(-\infty;\,3)$", False),
            ("Функція зростає", False),
        ],
        "hint": r"Розв'яжіть $-2x + 6 \ge 0$; подивіться на знак $k$.",
        "solution": r"$-2x \ge -6 \Rightarrow x \le 3$. Від'ємна при $x \gt 3$. $k = -2 \lt 0$ — спадає.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Скільки натуральних значень $x$, при яких функція $y = 7 - 2x$ набуває додатних значень?",
        "answer": "3",
        "hint": r"$7 - 2x \gt 0$.",
        "solution": r"$x \lt 3{,}5$: натуральні $1, 2, 3$ — три.",
    },
    # --- Аналіз результатів ---
    {
        "type": "ERROR", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Максим досліджував функцію $y = 4 - 2x$. У якому кроці помилка?",
        "steps": [r"Нуль: $4 - 2x = 0$, $x = 2$", r"$y \gt 0$ при $x \gt 2$", r"$k = -2 \lt 0$ — функція спадає"],
        "wrong": 1,
        "hint": r"Підставте, наприклад, $x = 3$.",
        "solution": r"$4 - 2x \gt 0 \Rightarrow x \lt 2$. При $x = 3$: $y = -2 \lt 0$.",
    },
    {
        "type": "TF", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Функція $y = x^2$. Правда чи ні?",
        "statements": [
            (r"Спадає на $(-\infty;\,0]$", True),
            (r"Зростає на $\mathbb{R}$", False),
            (r"$y \ge 0$ при всіх $x$", True),
            ("Має два нулі", False),
        ],
        "hint": r"Згадайте параболу $y = x^2$.",
        "solution": r"Парабола спадає до вершини й зростає після неї. $x^2 \ge 0$. Нуль один: $x = 0$.",
    },
    {
        "type": "MULTI", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Які функції зростають на проміжку $(0;\,+\infty)$?",
        "options": [(r"$y = x^2$", True), (r"$y = \sqrt{x}$", True), (r"$y = \frac{2}{x}$", False), (r"$y = -\frac{3}{x}$", True), (r"$y = -x$", False)],
        "hint": r"$y = \frac{k}{x}$ при $k \lt 0$ зростає на кожному проміжку.",
        "solution": r"$x^2$ і $\sqrt{x}$ зростають при $x \gt 0$; $-\frac{3}{x}$ — бо $k = -3 \lt 0$. $\frac{2}{x}$ і $-x$ спадають.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Тарас: «Функція $y = x^2 - 9$ додатна на $(-3;\,3)$». Що правильно?",
        "options": [(r"Ні: $y \gt 0$ на $(-\infty;\,-3) \cup (3;\,+\infty)$, а на $(-3;\,3)$ $y \lt 0$", True), ("Так, він правий", False),
                    (r"Ні: $y \gt 0$ при всіх $x$", False), (r"Ні: $y \gt 0$ лише на $(3;\,+\infty)$", False)],
        "hint": r"Обчисліть $y(0)$.",
        "solution": r"$y(0) = -9 \lt 0$, тож на $(-3;\,3)$ функція від'ємна. $y(4) = 7 \gt 0$, $y(-4) = 7 \gt 0$.",
    },
    {
        "type": "GROUP", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Чи має функція нулі? Розподіліть.",
        "groups": ["Має нулі", "Не має нулів"],
        "items": [(r"$y = x^2 + 4$", 1), (r"$y = \sqrt{x} + 1$", 1), (r"$y = 2x - 1$", 0), (r"$y = x^2 - x$", 0), (r"$y = \frac{1}{x}$", 1), (r"$y = |x| - 2$", 0)],
        "hint": r"Спробуйте розв'язати рівняння $y = 0$.",
        "solution": r"Нулі: $\frac{1}{2}$; $0$ і $1$; $\pm 2$. $x^2 + 4 \ge 4$, $\sqrt{x} + 1 \ge 1$, $\frac{1}{x} \ne 0$ — нулів немає.",
    },

    # ==========================================
    # СХОДИНКА 3 — СКЛАДНИЙ
    # ==========================================
    # --- Моделювання ---
    {
        "type": "FIELDS", "difficulty": 3, "skill": "MODEL",
        "text": r"За графіком функції $y = f(x)$ знайдіть:",
        "svg_code": '<svg xmlns="http://www.w3.org/2000/svg" width="340" height="290" viewBox="0 0 340 290" fill="none" stroke="currentColor" stroke-width="1" font-family="sans-serif"><line x1="20" y1="270" x2="20" y2="20" stroke-opacity="0.18"/><line x1="45" y1="270" x2="45" y2="20" stroke-opacity="0.18"/><line x1="70" y1="270" x2="70" y2="20" stroke-opacity="0.18"/><line x1="95" y1="270" x2="95" y2="20" stroke-opacity="0.18"/><line x1="120" y1="270" x2="120" y2="20" stroke-opacity="0.18"/><line x1="145" y1="270" x2="145" y2="20" stroke-opacity="0.18"/><line x1="170" y1="270" x2="170" y2="20" stroke-opacity="0.18"/><line x1="195" y1="270" x2="195" y2="20" stroke-opacity="0.18"/><line x1="220" y1="270" x2="220" y2="20" stroke-opacity="0.18"/><line x1="245" y1="270" x2="245" y2="20" stroke-opacity="0.18"/><line x1="270" y1="270" x2="270" y2="20" stroke-opacity="0.18"/><line x1="295" y1="270" x2="295" y2="20" stroke-opacity="0.18"/><line x1="320" y1="270" x2="320" y2="20" stroke-opacity="0.18"/><line x1="20" y1="270" x2="320" y2="270" stroke-opacity="0.18"/><line x1="20" y1="245" x2="320" y2="245" stroke-opacity="0.18"/><line x1="20" y1="220" x2="320" y2="220" stroke-opacity="0.18"/><line x1="20" y1="195" x2="320" y2="195" stroke-opacity="0.18"/><line x1="20" y1="170" x2="320" y2="170" stroke-opacity="0.18"/><line x1="20" y1="145" x2="320" y2="145" stroke-opacity="0.18"/><line x1="20" y1="120" x2="320" y2="120" stroke-opacity="0.18"/><line x1="20" y1="95" x2="320" y2="95" stroke-opacity="0.18"/><line x1="20" y1="70" x2="320" y2="70" stroke-opacity="0.18"/><line x1="20" y1="45" x2="320" y2="45" stroke-opacity="0.18"/><line x1="20" y1="20" x2="320" y2="20" stroke-opacity="0.18"/><line x1="12" y1="145" x2="332" y2="145" stroke-width="1.8"/><line x1="170" y1="262" x2="170" y2="8" stroke-width="1.8"/><path d="M332 145 l-9 -4 v8 z" fill="currentColor" stroke="none"/><path d="M170 8 l-4 9 h8 z" fill="currentColor" stroke="none"/><text x="326" y="163" fill="currentColor" stroke="none" font-size="13" font-style="italic">x</text><text x="178" y="18" fill="currentColor" stroke="none" font-size="13" font-style="italic">y</text><text x="160" y="160" fill="currentColor" stroke="none" font-size="13">0</text><text x="195" y="160" fill="currentColor" stroke="none" font-size="13" text-anchor="middle">1</text><text x="176" y="125" fill="currentColor" stroke="none" font-size="13">1</text><polyline points="45,195 120,45 220,245 295,95" stroke-width="3" stroke-linejoin="round"/><circle cx="45" cy="195" r="4" fill="currentColor" stroke="none"/><circle cx="295" cy="95" r="4" fill="currentColor" stroke="none"/></svg>',
        "fields": [("Найбільше значення функції:", "4"), ("Найменше значення функції:", "-4"), (r"Кількість цілих $x$, при яких $f(x) \gt 0$:", "4")],
        "hint": r"$f(x) \gt 0$ на $(-4;\,0)$ і $(4;\,5]$.",
        "solution": r"Найвища точка $(-2;\,4)$, найнижча $(2;\,-4)$. Цілі $x$ з $f(x) \gt 0$: $-3, -2, -1$ і $5$ — чотири.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"Лінійна функція $y = kx + 3$ має нуль $x = 6$. Знайдіть $k$.",
        "answer": "-0.5",
        "hint": r"Підставте $x = 6$, $y = 0$.",
        "solution": r"$6k + 3 = 0 \Rightarrow k = -0{,}5$. Функція спадає ($k \lt 0$).",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "MODEL",
        "text": r"Яка функція має область визначення $[0;\,+\infty)$, зростає на ній і має нуль $x = 4$?",
        "options": [(r"$y = \sqrt{x} - 2$", True), (r"$y = \sqrt{x} - 4$", False), (r"$y = x - 4$", False), (r"$y = \sqrt{x - 4}$", False), (r"$y = 2 - \sqrt{x}$", False)],
        "hint": r"Перевірте кожну умову окремо.",
        "solution": r"$\sqrt{4} - 2 = 0$ ✓, $D = [0;\,+\infty)$ ✓, зростає ✓. $\sqrt{x} - 4$ має нуль $16$; $x - 4$ визначена на $\mathbb{R}$; $\sqrt{x - 4}$ — на $[4;\,+\infty)$; $2 - \sqrt{x}$ спадає.",
    },
    {
        "type": "MATCH", "difficulty": 3, "skill": "MODEL",
        "text": r"Установіть відповідність між функцією (1–3) та проміжками, на яких вона додатна (А–Д).",
        "options": [r"А) $(2;\,+\infty)$", r"Б) $(-\infty;\,2)$", r"В) $(-\infty;\,-2) \cup (2;\,+\infty)$", r"Г) $(-2;\,2)$", r"Д) $(-\infty;\,+\infty)$"],
        "matches": [(r"1. $y = 2x - 4$", r"А) $(2;\,+\infty)$"), (r"2. $y = 4 - 2x$", r"Б) $(-\infty;\,2)$"),
                    (r"3. $y = x^2 - 4$", r"В) $(-\infty;\,-2) \cup (2;\,+\infty)$")],
        "hint": r"Знайдіть нулі й перевірте знак у пробній точці.",
        "solution": r"1) $2x \gt 4$, $x \gt 2$. 2) $x \lt 2$. 3) Нулі $\pm 2$; $y(0) = -4 \lt 0$, тож додатна за межами $[-2;\,2]$.",
    },
    {
        "type": "POINT", "difficulty": 3, "skill": "MODEL",
        "text": r"Позначте на прямій нуль функції $y = 2x + 3$.",
        "min": -4, "max": 4, "step": 0.5, "answer": -1.5,
        "hint": r"Розв'яжіть $2x + 3 = 0$.",
        "solution": r"$2x = -3$, $x = -1{,}5$.",
    },
    # --- Розв'язування ---
    {
        "type": "FIELDS", "difficulty": 3, "skill": "SOLVE",
        "text": r"Знайдіть нулі функції $y = x^2 - 2x - 8$.",
        "fields": [(r"$x_1 =$", "-2"), (r"$x_2 =$", "4")],
        "unordered": True,
        "hint": r"Розв'яжіть квадратне рівняння (дискримінант або теорема Вієта).",
        "solution": r"$x_1 + x_2 = 2$, $x_1 x_2 = -8$: $x = -2$ або $x = 4$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Скільки цілих значень $x$, при яких функція $y = (x - 1)(x - 5)$ набуває від'ємних значень?",
        "answer": "3",
        "hint": r"Добуток від'ємний, коли множники різних знаків.",
        "solution": r"Між нулями $1$ і $5$ множники різних знаків: $y \lt 0$ на $(1;\,5)$. Цілі: $2, 3, 4$.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "SOLVE",
        "text": r"Укажіть усі значення $x$, при яких функція $y = \sqrt{x + 4} - 1$ набуває від'ємних значень.",
        "options": [(r"$[-4;\,-3)$", True), (r"$(-\infty;\,-3)$", False), (r"$(-4;\,-3)$", False), (r"$[-4;\,-3]$", False), (r"$(-3;\,+\infty)$", False)],
        "hint": r"$\sqrt{x + 4} \lt 1$ і $x + 4 \ge 0$.",
        "solution": r"$0 \le x + 4 \lt 1 \Rightarrow -4 \le x \lt -3$. При $x = -4$: $y = -1 \lt 0$ — входить.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Знайдіть суму нулів функції $y = |x - 3| - 2$.",
        "answer": "6",
        "hint": r"$|x - 3| = 2$ має два розв'язки.",
        "solution": r"$x - 3 = 2$ або $x - 3 = -2$: $x = 5$ або $x = 1$; сума $6$.",
    },
    {
        "type": "FIELDS", "difficulty": 3, "skill": "SOLVE",
        "text": r"Функція $y = \frac{6}{x} - 2$.",
        "fields": [("Нуль функції:", "3"), (r"Кількість цілих $x$, при яких $y \gt 0$:", "2")],
        "hint": r"$\frac{6}{x} \gt 2$ можливе лише при $x \gt 0$.",
        "solution": r"$\frac{6}{x} = 2 \Rightarrow x = 3$. При $x \lt 0$: $y \lt 0$. При $x \gt 0$: $\frac{6}{x} \gt 2 \iff x \lt 3$. $y \gt 0$ на $(0;\,3)$: $x = 1, 2$.",
    },
    # --- Аналіз результатів ---
    {
        "type": "ERROR", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Сашко шукав, де $y = \sqrt{x} - 2$ від'ємна. У якому кроці помилка?",
        "steps": [r"$D(y) = [0;\,+\infty)$", r"$\sqrt{x} \lt 2 \Rightarrow x \lt 4$", r"Відповідь: $(-\infty;\,4)$"],
        "wrong": 2,
        "hint": r"Чи визначена функція при $x = -1$?",
        "solution": r"Треба врахувати $D(y)$: $0 \le x \lt 4$, відповідь $[0;\,4)$.",
    },
    {
        "type": "TF", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [
            (r"Якщо $f(1) \lt f(3)$, то $f$ зростає на $[1;\,3]$", False),
            (r"Функція $y = kx + b$ з $k \lt 0$ має рівно один нуль", True),
            (r"Якщо $f$ зростає на $[0;\,5]$, то $f(2) \lt f(4)$", True),
        ],
        "hint": r"Дві точки ще не визначають поведінку між ними.",
        "solution": r"Функція може спершу спадати, а потім зростати, і все одно $f(1) \lt f(3)$: наприклад, $f(x) = (x - 1{,}5)^2$: $f(1) = 0{,}25 \lt f(3) = 2{,}25$, але на $[1;\,1{,}5]$ спадає. Рівняння $kx + b = 0$ при $k \ne 0$ має єдиний корінь. Зростання: $2 \lt 4 \Rightarrow f(2) \lt f(4)$.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Функція $f$ зростає на $\mathbb{R}$. Порівняйте $f(-3)$ і $f(-5)$.",
        "options": [(r"$f(-3) \gt f(-5)$", True), (r"$f(-3) \lt f(-5)$", False), (r"$f(-3) = f(-5)$", False), ("Порівняти неможливо", False)],
        "hint": r"Яке з чисел $-3$ і $-5$ більше?",
        "solution": r"$-5 \lt -3$, а функція зростає: $f(-5) \lt f(-3)$.",
    },
    {
        "type": "MULTI", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Функція $f$ спадає на $\mathbb{R}$, $f(2) = 0$. Які твердження правильні?",
        "options": [(r"$f(0) \gt 0$", True), (r"$f(5) \lt 0$", True), (r"$f(1) \lt 0$", False), (r"$f(-1) \lt f(1)$", False), (r"$x = 2$ — єдиний нуль функції", True)],
        "hint": r"Ліворуч від $2$ значення більші за $f(2)$, праворуч — менші.",
        "solution": r"$0 \lt 2 \Rightarrow f(0) \gt f(2) = 0$; $5 \gt 2 \Rightarrow f(5) \lt 0$; $f(1) \gt 0$; $f(-1) \gt f(1)$. Спадна функція кожне значення набуває лише раз — нуль єдиний.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Скільки нулів має функція $y = \frac{x^2 - 4}{x - 2}$?",
        "answer": "1",
        "hint": r"Не забудьте про область визначення.",
        "solution": r"$x^2 - 4 = 0$ при $x = \pm 2$, але $x = 2$ не входить у $D$ (знаменник $0$). Нуль один: $x = -2$.",
    },

    # ==========================================
    # БОСИ — після опанування теми
    # ==========================================
    {
        "type": "SHORT", "difficulty": 4, "skill": "MODEL",
        "text": r"Лінійна функція $y = kx + b$ має нуль $x = -2$, а її графік перетинає вісь $Oy$ у точці $(0;\,4)$. Знайдіть $y(3)$.",
        "answer": "10",
        "solution": r"$b = 4$; $-2k + 4 = 0 \Rightarrow k = 2$. $y = 2x + 4$, $y(3) = 10$.",
    },
    {
        "type": "FIELDS", "difficulty": 4, "skill": "MODEL",
        "text": r"За графіком функції $y = f(x)$ знайдіть кількість розв'язків кожного рівняння.",
        "svg_code": '<svg xmlns="http://www.w3.org/2000/svg" width="340" height="290" viewBox="0 0 340 290" fill="none" stroke="currentColor" stroke-width="1" font-family="sans-serif"><line x1="20" y1="270" x2="20" y2="20" stroke-opacity="0.18"/><line x1="45" y1="270" x2="45" y2="20" stroke-opacity="0.18"/><line x1="70" y1="270" x2="70" y2="20" stroke-opacity="0.18"/><line x1="95" y1="270" x2="95" y2="20" stroke-opacity="0.18"/><line x1="120" y1="270" x2="120" y2="20" stroke-opacity="0.18"/><line x1="145" y1="270" x2="145" y2="20" stroke-opacity="0.18"/><line x1="170" y1="270" x2="170" y2="20" stroke-opacity="0.18"/><line x1="195" y1="270" x2="195" y2="20" stroke-opacity="0.18"/><line x1="220" y1="270" x2="220" y2="20" stroke-opacity="0.18"/><line x1="245" y1="270" x2="245" y2="20" stroke-opacity="0.18"/><line x1="270" y1="270" x2="270" y2="20" stroke-opacity="0.18"/><line x1="295" y1="270" x2="295" y2="20" stroke-opacity="0.18"/><line x1="320" y1="270" x2="320" y2="20" stroke-opacity="0.18"/><line x1="20" y1="270" x2="320" y2="270" stroke-opacity="0.18"/><line x1="20" y1="245" x2="320" y2="245" stroke-opacity="0.18"/><line x1="20" y1="220" x2="320" y2="220" stroke-opacity="0.18"/><line x1="20" y1="195" x2="320" y2="195" stroke-opacity="0.18"/><line x1="20" y1="170" x2="320" y2="170" stroke-opacity="0.18"/><line x1="20" y1="145" x2="320" y2="145" stroke-opacity="0.18"/><line x1="20" y1="120" x2="320" y2="120" stroke-opacity="0.18"/><line x1="20" y1="95" x2="320" y2="95" stroke-opacity="0.18"/><line x1="20" y1="70" x2="320" y2="70" stroke-opacity="0.18"/><line x1="20" y1="45" x2="320" y2="45" stroke-opacity="0.18"/><line x1="20" y1="20" x2="320" y2="20" stroke-opacity="0.18"/><line x1="12" y1="145" x2="332" y2="145" stroke-width="1.8"/><line x1="170" y1="262" x2="170" y2="8" stroke-width="1.8"/><path d="M332 145 l-9 -4 v8 z" fill="currentColor" stroke="none"/><path d="M170 8 l-4 9 h8 z" fill="currentColor" stroke="none"/><text x="326" y="163" fill="currentColor" stroke="none" font-size="13" font-style="italic">x</text><text x="178" y="18" fill="currentColor" stroke="none" font-size="13" font-style="italic">y</text><text x="160" y="160" fill="currentColor" stroke="none" font-size="13">0</text><text x="195" y="160" fill="currentColor" stroke="none" font-size="13" text-anchor="middle">1</text><text x="176" y="125" fill="currentColor" stroke="none" font-size="13">1</text><polyline points="45,195 120,45 220,245 295,95" stroke-width="3" stroke-linejoin="round"/><circle cx="45" cy="195" r="4" fill="currentColor" stroke="none"/><circle cx="295" cy="95" r="4" fill="currentColor" stroke="none"/></svg>',
        "fields": [(r"$f(x) = 2$:", "3"), (r"$f(x) = -3$:", "2"), (r"$f(x) = 4$:", "1")],
        "solution": r"Проводимо горизонтальні прямі. $y = 2$ перетинає графік у точках з $x = -3$, $x = -1$ і в кінці $x = 5$ — три. $y = -3$: $x = 1{,}5$ і $x = 2{,}5$ — дві (ліва частина не опускається нижче $-2$). $y = 4$ — лише вершина $x = -2$.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "SOLVE",
        "text": r"Скільки цілих значень $x$, при яких функція $y = \frac{x - 4}{x + 1}$ набуває від'ємних значень?",
        "answer": "4",
        "solution": r"Дріб від'ємний, коли чисельник і знаменник різних знаків: $\begin{cases} x - 4 \lt 0, \\ x + 1 \gt 0 \end{cases} \Rightarrow -1 \lt x \lt 4$ (друга система $x \gt 4$, $x \lt -1$ розв'язків не має). Цілі: $0, 1, 2, 3$.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "SOLVE",
        "text": r"Скільки цілих значень $x$, при яких функція $y = \sqrt{x + 3} - \sqrt{5 - x}$ набуває додатних значень?",
        "answer": "4",
        "solution": r"$D = [-3;\,5]$. $y \gt 0 \iff \sqrt{x + 3} \gt \sqrt{5 - x} \iff x + 3 \gt 5 - x \iff x \gt 1$. Отже, $(1;\,5]$: $x = 2, 3, 4, 5$.",
    },
    {
        "type": "TF", "difficulty": 4, "skill": "ANALYZE",
        "text": r"Лінійна функція $f$ така, що $f(-1) = 5$, $f(3) = -3$. Правда чи ні?",
        "statements": [
            (r"$f$ спадає на $\mathbb{R}$", True),
            (r"Нуль функції $x = 1{,}5$", True),
            (r"$f(x) \gt 0$ при $x \lt 1{,}5$", True),
            (r"$f(0) = 2$", False),
        ],
        "solution": r"$k = \frac{-3 - 5}{3 - (-1)} = -2$, $b = 5 + k = 3$: $f(x) = -2x + 3$. Спадає; нуль $1{,}5$; додатна ліворуч від нуля; $f(0) = 3$.",
    },

    # ==========================================
    # УЛЬТРА-БОСИ
    # ==========================================
    {
        "type": "SHORT", "difficulty": 5, "skill": "SOLVE",
        "text": r"Функція $f$ зростає на $\mathbb{R}$. Скільки натуральних розв'язків має нерівність $f(2x - 1) \lt f(x + 4)$?",
        "answer": "4",
        "solution": r"Для зростаючої функції $f(a) \lt f(b) \iff a \lt b$. Тож $2x - 1 \lt x + 4$, $x \lt 5$: натуральні $1, 2, 3, 4$.",
    },
    {
        "type": "SHORT", "difficulty": 5, "skill": "SOLVE",
        "text": r"Функція $y = |x - 1| + |x - 5|$. При скількох цілих $x$ вона набуває свого найменшого значення?",
        "answer": "5",
        "solution": r"$|x - 1| + |x - 5|$ — сума відстаней від $x$ до $1$ і до $5$ на числовій прямій. Вона не менша за $4$ і дорівнює $4$ при $1 \le x \le 5$ (поза відрізком — більша). Цілі: $1, 2, 3, 4, 5$.",
    },
]
