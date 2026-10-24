TOPIC_NAME = "1.7. Степінь із цілим від'ємним показником"
COURSE = "Алгебра (7-9 класи)"
GRADE = "8 клас"

TASKS = [
    # ===== СХОДИНКА 1 =====
    # --- Моделювання ---
    {
        "type": "CHOICE", "difficulty": 1, "skill": "MODEL",
        "text": r"Як записати $\dfrac{1}{7^3}$ у вигляді степеня?",
        "options": [(r"$7^{-3}$", True), (r"$-7^3$", False), (r"$7^{\frac13}$", False), (r"$(-7)^3$", False)],
        "hint": "$a^{-n} = \\dfrac{1}{a^n}$.",
        "solution": r"За означенням $\dfrac{1}{7^3} = 7^{-3}$.",
    },
    {
        "type": "MATCH", "difficulty": 1, "skill": "MODEL",
        "text": r"Установіть відповідність між степенем (1–3) та його значенням (А–Д).",
        "options": [r"А) $\dfrac{1}{10}$", r"Б) $1$", r"В) $\dfrac{1}{100}$", r"Г) $-10$", r"Д) $0$"],
        "matches": [(r"1. $10^{-1}$", r"А) $\dfrac{1}{10}$"), (r"2. $10^{0}$", r"Б) $1$"), (r"3. $10^{-2}$", r"В) $\dfrac{1}{100}$")],
        "hint": "$10^{-n} = \\dfrac{1}{10^n}$, $a^0 = 1$.",
        "solution": r"$10^{-1} = 0{,}1$, $10^0 = 1$, $10^{-2} = 0{,}01$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "MODEL",
        "text": r"$0{,}001 = 10^n$. Знайдіть $n$.",
        "answer": "-3",
        "hint": "$0{,}001 = \\dfrac{1}{1000}$.",
        "solution": r"$0{,}001 = \dfrac{1}{10^3} = 10^{-3}$, $n = -3$.",
    },
    {
        "type": "TF", "difficulty": 1, "skill": "MODEL",
        "text": r"Правда чи ні?",
        "statements": [(r"$a^{-1} = \dfrac{1}{a}$ при $a \ne 0$", True), (r"$5^0 = 0$", False), (r"$0^{-2}$ не має змісту", True)],
        "hint": "Згадайте означення степенів з нульовим і від'ємним показником.",
        "solution": r"$a^{-1} = \dfrac{1}{a}$; $5^0 = 1$; $0^{-2} = \dfrac{1}{0^2}$ — ділення на нуль.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "MODEL",
        "text": r"Яким степенем числа $2$ є дріб $\dfrac{1}{32}$?",
        "options": [(r"$2^{-5}$", True), (r"$2^{5}$", False), (r"$2^{-16}$", False), (r"$-2^{5}$", False)],
        "hint": "$32 = 2^5$.",
        "solution": r"$\dfrac{1}{32} = \dfrac{1}{2^5} = 2^{-5}$.",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"Обчисліть: $5^{-2}$. Відповідь запишіть десятковим дробом.",
        "answer": "0,04",
        "hint": "$5^{-2} = \\dfrac{1}{25}$.",
        "solution": r"$5^{-2} = \dfrac{1}{25} = 0{,}04$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"Обчисліть: $\left(\dfrac{1}{3}\right)^{-2}$.",
        "answer": "9",
        "hint": "Дріб у від'ємному степені — перевертаємо.",
        "solution": r"$\left(\dfrac{1}{3}\right)^{-2} = 3^2 = 9$.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "SOLVE",
        "text": r"Спростіть: $a^{-4} \cdot a^{6}$.",
        "options": [(r"$a^{2}$", True), (r"$a^{-24}$", False), (r"$a^{10}$", False), (r"$a^{-10}$", False)],
        "hint": "При множенні степенів показники додаємо.",
        "solution": r"$a^{-4+6} = a^2$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"Обчисліть: $2^{-3} \cdot 2^{5}$.",
        "answer": "4",
        "hint": "Додайте показники.",
        "solution": r"$2^{-3+5} = 2^2 = 4$.",
    },
    {
        "type": "ORDER", "difficulty": 1, "skill": "SOLVE",
        "text": r"Розташуйте числа в порядку зростання.",
        "items": [r"$2^{-3}$", r"$2^{-1}$", r"$2^{0}$", r"$2^{2}$"],
        "hint": "Обчисліть кожне: $2^{-3} = \\dfrac{1}{8}$.",
        "solution": r"$\dfrac{1}{8} \lt \dfrac{1}{2} \lt 1 \lt 4$.",
    },
    # --- Аналіз ---
    {
        "type": "ERROR", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Оля обчислювала $3^{-2}$. У якому кроці помилка?",
        "steps": [r"$3^{-2} = -3^2$", r"$= -9$"],
        "wrong": 0,
        "hint": "Від'ємний показник — це не від'ємне число.",
        "solution": r"$3^{-2} = \dfrac{1}{3^2} = \dfrac{1}{9}$.",
    },
    {
        "type": "MULTI", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Які з виразів дорівнюють $\dfrac{1}{4}$?",
        "options": [(r"$4^{-1}$", True), (r"$2^{-2}$", True), (r"$\left(\dfrac{1}{2}\right)^{2}$", True), (r"$-4$", False), (r"$4^{0}$", False)],
        "hint": "Обчисліть кожен.",
        "solution": r"$4^{-1} = 2^{-2} = \left(\dfrac12\right)^2 = \dfrac14$; $4^0 = 1$.",
    },
    {
        "type": "TF", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [(r"$2^{-3}$ — додатне число", True), (r"$(-2)^{-2} = \dfrac{1}{4}$", True), (r"$10^{-2} \gt 10^{-1}$", False)],
        "hint": "$10^{-2} = 0{,}01$, $10^{-1} = 0{,}1$.",
        "solution": r"$2^{-3} = \dfrac18 \gt 0$; $(-2)^{-2} = \dfrac{1}{4}$; $0{,}01 \lt 0{,}1$.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Тарас каже: «$7^0 = 0$, бо нуль разів по сім — це нуль». Чи правий він?",
        "options": [(r"Ні, $7^0 = 1$", True), (r"Так", False), (r"Ні, $7^0 = 7$", False), (r"Ні, $7^0$ не має змісту", False)],
        "hint": "$7^0 = 7^{1-1} = 7 : 7$.",
        "solution": r"$a^0 = 1$ для $a \ne 0$: $7^0 = \dfrac{7^1}{7^1} = 1$.",
    },
    {
        "type": "GROUP", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Розподіліть числа: більші за $1$ чи менші за $1$?",
        "groups": ["більші за 1", "менші за 1"],
        "items": [(r"$3^{-2}$", 1), (r"$\left(\dfrac{1}{2}\right)^{-3}$", 0), (r"$10^{-1}$", 1), (r"$\left(\dfrac{2}{5}\right)^{-1}$", 0), (r"$2^{3}$", 0), (r"$\left(\dfrac{3}{4}\right)^{2}$", 1)],
        "hint": "Обчисліть кожне.",
        "solution": r"$\dfrac19$, $0{,}1$, $\dfrac{9}{16}$ — менші; $8$, $\dfrac52$, $8$ — більші.",
    },

    # ===== СХОДИНКА 2 =====
    # --- Моделювання ---
    {
        "type": "FIELDS", "difficulty": 2, "skill": "MODEL",
        "text": r"Запишіть число $0{,}00045$ у стандартному вигляді $a \cdot 10^n$ ($1 \le a \lt 10$).",
        "fields": [("$a$:", "4,5"), ("$n$:", "-4")],
        "solution": r"$0{,}00045 = 4{,}5 \cdot 0{,}0001 = 4{,}5 \cdot 10^{-4}$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "MODEL",
        "text": r"Діаметр бактерії $2 \cdot 10^{-6}$ м. Скільки таких бактерій уміститься впритул в ряд завдовжки $1$ мм ($10^{-3}$ м)?",
        "answer": "500",
        "solution": r"$\dfrac{10^{-3}}{2 \cdot 10^{-6}} = \dfrac{10^{3}}{2} = 500$.",
    },
    {
        "type": "EXPR", "difficulty": 2, "skill": "MODEL",
        "text": r"Запишіть без від'ємних показників: $x^{-2}y$ (дробом через «/»).",
        "answer": "y/x^2", "vars": ["x", "y"],
        "solution": r"$x^{-2}y = \dfrac{y}{x^2}$.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "MODEL",
        "text": r"Який вираз дорівнює $\dfrac{a^3}{b^{2}}$ (у вигляді добутку степенів)?",
        "options": [(r"$a^3 b^{-2}$", True), (r"$a^{-3} b^{2}$", False), (r"$a^3 b^2$", False), (r"$(ab)^{1}$", False)],
        "solution": r"$\dfrac{1}{b^2} = b^{-2}$, тож $\dfrac{a^3}{b^2} = a^3 b^{-2}$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "MODEL",
        "text": r"$\dfrac{1}{81} = 3^n$. Знайдіть $n$.",
        "answer": "-4",
        "solution": r"$81 = 3^4$, тож $\dfrac{1}{81} = 3^{-4}$.",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Обчисліть: $\left(\dfrac{2}{3}\right)^{-3}$. Відповідь — десятковим дробом.",
        "answer": "3,375",
        "solution": r"$\left(\dfrac{3}{2}\right)^3 = \dfrac{27}{8} = 3{,}375$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Обчисліть: $\dfrac{7^{-3} \cdot 7^{8}}{7^{3}}$.",
        "answer": "49",
        "solution": r"$7^{-3 + 8 - 3} = 7^2 = 49$.",
    },
    {
        "type": "EXPR", "difficulty": 2, "skill": "SOLVE",
        "text": r"Спростіть: $(x^{-2})^{3} \cdot x^{8}$.",
        "answer": "x^2", "vars": ["x"],
        "solution": r"$x^{-6} \cdot x^8 = x^2$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Обчисліть: $2^{-1} + 4^{-1} + 8^{0}$. Відповідь — десятковим дробом.",
        "answer": "1,75",
        "solution": r"$0{,}5 + 0{,}25 + 1 = 1{,}75$.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "SOLVE",
        "text": r"Спростіть: $\dfrac{a^{-2}}{a^{-5}}$.",
        "options": [(r"$a^3$", True), (r"$a^{-7}$", False), (r"$a^{-3}$", False), (r"$a^{10}$", False)],
        "solution": r"$a^{-2 - (-5)} = a^{3}$.",
    },
    # --- Аналіз ---
    {
        "type": "ERROR", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Тарас спрощував $\dfrac{x^{3}}{x^{-2}}$. У якому кроці помилка?",
        "steps": [r"$\dfrac{x^{3}}{x^{-2}} = x^{3 - (-2)}$", r"$= x^{1}$", r"$= x$"],
        "wrong": 1,
        "solution": r"$3 - (-2) = 5$: відповідь $x^5$.",
    },
    {
        "type": "TF", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [(r"$-2^{-2} = -\dfrac{1}{4}$", True), (r"$(-2)^{-3} = \dfrac{1}{8}$", False),
                       (r"$(ab)^{-1} = a^{-1}b^{-1}$ при $a, b \ne 0$", True), (r"$(a + b)^{-1} = a^{-1} + b^{-1}$", False)],
        "solution": r"$-2^{-2} = -\dfrac14$. $(-2)^{-3} = -\dfrac18$. $(ab)^{-1} = \dfrac{1}{ab}$ ✓. $\dfrac{1}{a + b} \ne \dfrac1a + \dfrac1b$ (напр., $a = b = 1$: $\dfrac12 \ne 2$).",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Яке число більше: $0{,}2^{-2}$ чи $5^{1}$?",
        "options": [(r"$0{,}2^{-2}$", True), (r"$5^{1}$", False), (r"вони рівні", False), (r"порівняти неможливо", False)],
        "solution": r"$0{,}2^{-2} = 5^2 = 25 \gt 5$.",
    },
    {
        "type": "MULTI", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Які вирази дорівнюють $a^{-6}$ ($a \ne 0$)?",
        "options": [(r"$(a^{-2})^{3}$", True), (r"$a^{-2} \cdot a^{-4}$", True), (r"$\dfrac{a^{2}}{a^{8}}$", True), (r"$a^{-2} \cdot a^{-3}$", False), (r"$(a^{3})^{-3}$", False)],
        "solution": r"$a^{-6}$, $a^{-6}$, $a^{-6}$; $a^{-5}$ і $a^{-9}$ — ні.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "ANALYZE",
        "text": r"При якому $n$ виконується $4^{n} = \dfrac{1}{64}$?",
        "answer": "-3",
        "solution": r"$64 = 4^3$, тож $\dfrac{1}{64} = 4^{-3}$.",
    },

    # ===== СХОДИНКА 3 =====
    # --- Моделювання ---
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"Маса атома водню близько $1{,}7 \cdot 10^{-24}$ г. Скільки грамів важать $10^{20}$ атомів? Відповідь — десятковим дробом.",
        "answer": "0,00017",
        "solution": r"$1{,}7 \cdot 10^{-24} \cdot 10^{20} = 1{,}7 \cdot 10^{-4} = 0{,}00017$ г.",
    },
    {
        "type": "FIELDS", "difficulty": 3, "skill": "MODEL",
        "text": r"Запишіть добуток $(3 \cdot 10^{-5}) \cdot (4 \cdot 10^{2})$ у стандартному вигляді $a \cdot 10^n$.",
        "fields": [("$a$:", "1,2"), ("$n$:", "-2")],
        "solution": r"$12 \cdot 10^{-3} = 1{,}2 \cdot 10^{-2}$.",
    },
    {
        "type": "EXPR", "difficulty": 3, "skill": "MODEL",
        "text": r"Запишіть без від'ємних показників: $\dfrac{a^{-1}}{b^{-2}}$ (дробом через «/»).",
        "answer": "b^2/a", "vars": ["a", "b"],
        "solution": r"$\dfrac{a^{-1}}{b^{-2}} = \dfrac{b^2}{a}$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"$8^{-2} = 2^n$. Знайдіть $n$.",
        "answer": "-6",
        "solution": r"$8^{-2} = (2^3)^{-2} = 2^{-6}$.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "MODEL",
        "text": r"Який вираз дорівнює $\left(\dfrac{a}{b}\right)^{-3}$ ($a, b \ne 0$)?",
        "options": [(r"$\dfrac{b^3}{a^3}$", True), (r"$-\dfrac{a^3}{b^3}$", False), (r"$\dfrac{a^{3}}{b^{3}}$", False), (r"$\dfrac{b}{a^3}$", False), (r"$\dfrac{-3a}{b}$", False)],
        "solution": r"$\left(\dfrac{a}{b}\right)^{-3} = \left(\dfrac{b}{a}\right)^{3} = \dfrac{b^3}{a^3}$.",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Обчисліть: $\dfrac{25^{-3} \cdot 5^{4}}{125^{-1}}$.",
        "answer": "5",
        "solution": r"$5^{-6} \cdot 5^4 : 5^{-3} = 5^{-6 + 4 + 3} = 5^{1} = 5$.",
    },
    {
        "type": "EXPR", "difficulty": 3, "skill": "SOLVE",
        "text": r"Спростіть: $(2a^{-3})^{-2} \cdot a^{-4}$.",
        "answer": "a^2/4", "vars": ["a"],
        "solution": r"$(2a^{-3})^{-2} = 2^{-2}a^{6} = \dfrac{a^6}{4}$; $\cdot a^{-4} = \dfrac{a^2}{4}$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Обчисліть: $\left(\dfrac{1}{2}\right)^{-2} \cdot 0{,}5^{3} + \left(-\dfrac{1}{3}\right)^{-1}$.",
        "answer": "-2,5",
        "solution": r"$4 \cdot 0{,}125 + (-3) = 0{,}5 - 3 = -2{,}5$.",
    },
    {
        "type": "EXPR", "difficulty": 3, "skill": "SOLVE",
        "text": r"Спростіть: $\dfrac{x^{-3} y^{2}}{x^{-5} y^{-1}}$.",
        "answer": "x^2y^3", "vars": ["x", "y"],
        "solution": r"$x^{-3 + 5} y^{2 + 1} = x^2 y^3$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Обчисліть: $\dfrac{3^{-4} \cdot 9^{3}}{27^{-1}}$.",
        "answer": "243",
        "solution": r"$3^{-4} \cdot 3^{6} \cdot 3^{3} = 3^{5} = 243$.",
    },
    # --- Аналіз ---
    {
        "type": "ERROR", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Оля спрощувала $(3x^{-2})^{-2}$. У якому кроці помилка?",
        "steps": [r"$(3x^{-2})^{-2} = 3 \cdot x^{4}$", r"$= 3x^4$"],
        "wrong": 0,
        "solution": r"Степінь добутку: кожен множник у степінь $-2$: $3^{-2}x^{4} = \dfrac{x^4}{9}$.",
    },
    {
        "type": "TF", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Правда чи ні (для $a \ne 0$)?",
        "statements": [(r"$a^{-2} \gt 0$ для будь-якого $a$", True), (r"Якщо $a \gt 1$, то $a^{-1} \lt 1$", True),
                       (r"$a^{-3}$ має той самий знак, що й $a$", True), (r"Якщо $0 \lt a \lt 1$, то $a^{-2} \lt a$", False)],
        "solution": r"$a^{-2} = \dfrac{1}{a^2} \gt 0$. При $a \gt 1$: $\dfrac1a \lt 1$. $\dfrac{1}{a^3}$ — знак $a$. При $a = 0{,}5$: $a^{-2} = 4 \gt 0{,}5$.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Порівняйте $a = 3^{-20}$ і $b = 9^{-9}$.",
        "options": [(r"$a \lt b$", True), (r"$a \gt b$", False), (r"$a = b$", False), (r"порівняти неможливо", False), (r"обидва від'ємні", False)],
        "solution": r"$b = 3^{-18}$. $3^{-20} = \dfrac{1}{3^{20}} \lt \dfrac{1}{3^{18}}$, тож $a \lt b$.",
    },
    {
        "type": "GROUP", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Розподіліть вирази за знаком.",
        "groups": ["додатні", "від'ємні"],
        "items": [(r"$(-3)^{-2}$", 0), (r"$(-3)^{-3}$", 1), (r"$-3^{-2}$", 1), (r"$(-0{,}5)^{-4}$", 0), (r"$-(-2)^{-2}$", 1), (r"$(-1)^{0}$", 0)],
        "solution": r"Парний показник — додатне; непарний при від'ємній основі — від'ємне; мінус перед степенем змінює знак. $(-1)^0 = 1$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Знайдіть $n$, якщо $2^{n} \cdot 4^{3} = \dfrac{1}{8}$.",
        "answer": "-9",
        "solution": r"$2^{n} \cdot 2^{6} = 2^{-3}$, $n + 6 = -3$, $n = -9$.",
    },

    # ===== БОСИ =====
    {
        "type": "SHORT", "difficulty": 4, "skill": "MODEL",
        "text": r"Об'єм краплі води $5 \cdot 10^{-2}$ мл. Скільки крапель у склянці об'ємом $2 \cdot 10^{2}$ мл?",
        "answer": "4000",
        "solution": r"$\dfrac{2 \cdot 10^{2}}{5 \cdot 10^{-2}} = 0{,}4 \cdot 10^{4} = 4000$.",
    },
    {
        "type": "EXPR", "difficulty": 4, "skill": "MODEL",
        "text": r"Запишіть вираз $(a^{-1} + b^{-1})^{-1}$ без від'ємних показників (дробом через «/»).",
        "answer": "ab/(a+b)", "vars": ["a", "b"],
        "solution": r"$a^{-1} + b^{-1} = \dfrac{a + b}{ab}$; обернене — $\dfrac{ab}{a + b}$.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "SOLVE",
        "text": r"Обчисліть: $\dfrac{2^{-3} + 2^{-4}}{2^{-5}}$.",
        "answer": "6",
        "solution": r"Помножимо чисельник і знаменник на $2^5$: $\dfrac{4 + 2}{1} = 6$.",
    },
    {
        "type": "EXPR", "difficulty": 4, "skill": "SOLVE",
        "text": r"Спростіть: $\dfrac{x^{-2} - 1}{x^{-1} - 1}$ ($x \ne 0$, $x \ne 1$).",
        "answer": "(1+x)/x", "vars": ["x"],
        "solution": r"$\dfrac{\frac{1 - x^2}{x^2}}{\frac{1 - x}{x}} = \dfrac{(1 - x)(1 + x)}{x^2} \cdot \dfrac{x}{1 - x} = \dfrac{1 + x}{x}$.",
    },
    {
        "type": "TF", "difficulty": 4, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [(r"$2^{-10} \lt 10^{-3}$", True), (r"$(0{,}1)^{-3} = 1000$", True), (r"$\left(\dfrac{1}{2}\right)^{-5} \lt 5^{2}$", False)],
        "solution": r"$2^{10} = 1024 \gt 1000$, тож $2^{-10} \lt 10^{-3}$. $0{,}1^{-3} = 10^3$. $2^5 = 32 \gt 25$.",
    },
    {
        "type": "SHORT", "difficulty": 5, "skill": "SOLVE",
        "text": r"Відомо, що $a + a^{-1} = 3$. Знайдіть $a^{2} + a^{-2}$.",
        "answer": "7",
        "solution": r"$(a + a^{-1})^2 = a^2 + 2 + a^{-2} = 9$, тож $a^2 + a^{-2} = 7$.",
    },
    {
        "type": "SHORT", "difficulty": 5, "skill": "ANALYZE",
        "text": r"Знайдіть значення $\dfrac{1}{1 + x^{-3}} + \dfrac{1}{1 + x^{3}}$ ($x \ne 0$, $x \ne -1$).",
        "answer": "1",
        "solution": r"$\dfrac{1}{1 + x^{-3}} = \dfrac{x^3}{x^3 + 1}$. Сума: $\dfrac{x^3 + 1}{x^3 + 1} = 1$.",
    },
]
