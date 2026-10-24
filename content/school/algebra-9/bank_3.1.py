TOPIC_NAME = "3.1. Числові послідовності"
COURSE = "Алгебра (7-9 класи)"
GRADE = "9 клас"

TASKS = [
    # ===== СХОДИНКА 1 =====
    # --- Моделювання ---
    {
        "type": "CHOICE", "difficulty": 1, "skill": "MODEL",
        "text": r"Послідовність задано описом: «натуральні числа, кратні $5$, у порядку зростання». Яка формула $n$-го члена?",
        "options": [(r"$a_n = 5n$", True), (r"$a_n = n + 5$", False), (r"$a_n = 5^n$", False), (r"$a_n = \dfrac{n}{5}$", False)],
        "hint": "Випишіть перші члени: $5, 10, 15, \\ldots$",
        "solution": r"$5, 10, 15, \ldots$ — це $5 \cdot 1, 5 \cdot 2, 5 \cdot 3$: $a_n = 5n$.",
    },
    {
        "type": "FIELDS", "difficulty": 1, "skill": "MODEL",
        "text": r"Запишіть перші три члени послідовності $a_n = 2n + 3$.",
        "fields": [("$a_1$:", "5"), ("$a_2$:", "7"), ("$a_3$:", "9")],
        "hint": "Підставте $n = 1, 2, 3$.",
        "solution": r"$2 + 3 = 5$, $4 + 3 = 7$, $6 + 3 = 9$.",
    },
    {
        "type": "MATCH", "difficulty": 1, "skill": "MODEL",
        "text": r"Установіть відповідність між послідовністю (1–3) та формулою її $n$-го члена (А–Д).",
        "options": [r"А) $a_n = n^2$", r"Б) $a_n = 2n$", r"В) $a_n = 2n - 1$", r"Г) $a_n = 10^n$", r"Д) $a_n = n + 10$"],
        "matches": [(r"1. $1, 3, 5, 7, \ldots$", r"В) $a_n = 2n - 1$"), (r"2. $1, 4, 9, 16, \ldots$", r"А) $a_n = n^2$"),
                    (r"3. $10, 100, 1000, \ldots$", r"Г) $a_n = 10^n$")],
        "hint": "Перевірте кожну формулу при $n = 1$ і $n = 2$.",
        "solution": r"Непарні числа — $2n - 1$; квадрати — $n^2$; степені десяти — $10^n$.",
    },
    {
        "type": "TF", "difficulty": 1, "skill": "MODEL",
        "text": r"Правда чи ні?",
        "statements": [(r"Номер члена послідовності — натуральне число", True), (r"Послідовність двоцифрових чисел нескінченна", False),
                       (r"Послідовність можна задати рекурентною формулою", True)],
        "hint": "Скільки є двоцифрових чисел?",
        "solution": r"Двоцифрових чисел $90$ — послідовність скінченна. Решта — правда.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "MODEL",
        "text": r"$a_1 = 7$, $a_{n+1} = a_n + 4$. Знайдіть $a_2$.",
        "answer": "11",
        "hint": "Підставте $n = 1$: $a_2 = a_1 + 4$.",
        "solution": r"$a_2 = 7 + 4 = 11$.",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"$a_n = 5n - 8$. Знайдіть $a_{10}$.",
        "answer": "42",
        "hint": "Підставте $n = 10$.",
        "solution": r"$5 \cdot 10 - 8 = 42$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"$b_n = n^2 + n$. Знайдіть $b_4$.",
        "answer": "20",
        "hint": "$16 + 4$.",
        "solution": r"$4^2 + 4 = 20$.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "SOLVE",
        "text": r"$a_n = \dfrac{12}{n}$. Знайдіть $a_3$.",
        "options": [(r"$4$", True), (r"$36$", False), (r"$9$", False), (r"$\dfrac{1}{4}$", False)],
        "hint": "$12 : 3$.",
        "solution": r"$a_3 = 12 : 3 = 4$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"$x_1 = 2$, $x_{n+1} = 3x_n$. Знайдіть $x_3$.",
        "answer": "18",
        "hint": "Спершу $x_2$, потім $x_3$.",
        "solution": r"$x_2 = 6$, $x_3 = 18$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"Яким за номером членом послідовності $a_n = 3n + 2$ є число $32$?",
        "answer": "10",
        "hint": "Розв'яжіть $3n + 2 = 32$.",
        "solution": r"$3n = 30$, $n = 10$.",
    },
    # --- Аналіз ---
    {
        "type": "TF", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Чи є число членом послідовності $a_n = 4n$?",
        "statements": [(r"$40$", True), (r"$42$", False), (r"$0$", False), (r"$4$", True)],
        "hint": "$n = \\dfrac{a_n}{4}$ має бути натуральним.",
        "solution": r"$40 = a_{10}$, $4 = a_1$. $42 : 4 = 10{,}5$ — ні; $0$ дає $n = 0$ — не натуральне.",
    },
    {
        "type": "ERROR", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Оля шукала $a_3$ для $a_n = (n + 1)^2$. У якому кроці помилка?",
        "steps": [r"Підставимо $n = 3$", r"$(3 + 1)^2 = 3^2 + 1$", r"$= 10$"],
        "wrong": 1,
        "hint": "Спершу додавання в дужках.",
        "solution": r"$(3 + 1)^2 = 4^2 = 16$.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Тарас: «$a_{2{,}5}$ — це член між $a_2$ і $a_3$». Чи правий він?",
        "options": [(r"Ні, номер має бути натуральним", True), (r"Так", False), (r"Так, якщо послідовність нескінченна", False), (r"Ні, бо $a_{2{,}5} = 0$", False)],
        "hint": "Якими можуть бути номери членів?",
        "solution": r"Номери — натуральні числа, $a_{2{,}5}$ не існує.",
    },
    {
        "type": "GROUP", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Розподіліть послідовності: скінченні чи нескінченні?",
        "groups": ["скінченна", "нескінченна"],
        "items": [(r"дні тижня за номером", 0), (r"парні натуральні числа", 1), (r"двоцифрові числа", 0),
                  (r"$a_n = \dfrac{1}{n}$", 1), (r"дільники числа $12$", 0), (r"степені двійки", 1)],
        "hint": "Чи можна перелічити всі члени?",
        "solution": r"Дні тижня ($7$), двоцифрові ($90$), дільники $12$ ($6$) — скінченні. Інші — нескінченні.",
    },
    {
        "type": "MULTI", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Які формули задають послідовність $3, 6, 9, 12, \ldots$?",
        "options": [(r"$a_n = 3n$", True), (r"$a_1 = 3,\; a_{n+1} = a_n + 3$", True), (r"$a_n = n + 3$", False), (r"$a_1 = 3,\; a_{n+1} = 2a_n$", False)],
        "hint": "Перевірте перші три члени.",
        "solution": r"$3n$: $3, 6, 9$ ✓. Рекурентна з $+3$ ✓. $n + 3$: $4, 5, 6$. $2a_n$: $3, 6, 12$.",
    },

    # ===== СХОДИНКА 2 =====
    # --- Моделювання ---
    {
        "type": "EXPR", "difficulty": 2, "skill": "MODEL",
        "text": r"Знайдіть формулу $n$-го члена: $\dfrac{1}{3}, \dfrac{2}{4}, \dfrac{3}{5}, \dfrac{4}{6}, \ldots$ (дробом через «/»).",
        "answer": "n/(n+2)", "vars": ["n"],
        "solution": r"Чисельник — $n$, знаменник — $n + 2$: $a_n = \dfrac{n}{n + 2}$.",
    },
    {
        "type": "EXPR", "difficulty": 2, "skill": "MODEL",
        "text": r"Знайдіть формулу $n$-го члена: $2, 5, 10, 17, 26, \ldots$",
        "answer": "n^2+1", "vars": ["n"],
        "solution": r"Це квадрати, збільшені на $1$: $a_n = n^2 + 1$.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "MODEL",
        "text": r"Знайдіть формулу $n$-го члена: $-1, 1, -1, 1, \ldots$",
        "options": [(r"$a_n = (-1)^n$", True), (r"$a_n = (-1)^{n+1}$", False), (r"$a_n = -n$", False), (r"$a_n = 1 - n$", False), (r"$a_n = -1$", False)],
        "solution": r"$(-1)^1 = -1$, $(-1)^2 = 1$ ✓. $(-1)^{n+1}$ починається з $1$.",
    },
    {
        "type": "FIELDS", "difficulty": 2, "skill": "MODEL",
        "text": r"Задайте рекурентно послідовність $5, 15, 45, 135, \ldots$: $a_1 = ?$, $a_{n+1} = k \cdot a_n$. Знайдіть $a_1$ і $k$.",
        "fields": [("$a_1$:", "5"), ("$k$:", "3")],
        "solution": r"Кожен наступний утричі більший: $a_1 = 5$, $a_{n+1} = 3a_n$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "MODEL",
        "text": r"У залі в першому ряду $20$ місць, а в кожному наступному — на $2$ більше. Скільки місць у $15$-му ряду?",
        "answer": "48",
        "solution": r"$a_n = 20 + 2(n - 1)$; $a_{15} = 20 + 28 = 48$.",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"$a_1 = 1$, $a_{n+1} = 2a_n + 1$. Знайдіть $a_5$.",
        "answer": "31",
        "solution": r"$1, 3, 7, 15, 31$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Скільки членів послідовності $a_n = 4n - 3$ менші за $50$?",
        "answer": "13",
        "solution": r"$4n - 3 \lt 50$, $n \lt 13{,}25$: $n = 1, \ldots, 13$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"$a_n = n^2 - 6n$. Знайдіть номер члена, що дорівнює $16$.",
        "answer": "8",
        "solution": r"$n^2 - 6n - 16 = 0$, $n = 8$ або $n = -2$; натуральний лише $8$.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "SOLVE",
        "text": r"$a_n = \dfrac{n + 1}{n}$. Знайдіть $a_{n+1}$.",
        "options": [(r"$\dfrac{n + 2}{n + 1}$", True), (r"$\dfrac{n + 1}{n} + 1$", False), (r"$\dfrac{n + 2}{n}$", False), (r"$\dfrac{n + 1}{n + 1}$", False), (r"$\dfrac{n}{n + 1}$", False)],
        "solution": r"Замість $n$ підставляємо $n + 1$: $\dfrac{(n + 1) + 1}{n + 1} = \dfrac{n + 2}{n + 1}$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"$c_1 = 10$, $c_{n+1} = c_n - n$. Знайдіть $c_5$.",
        "answer": "0",
        "solution": r"$c_2 = 9$, $c_3 = 7$, $c_4 = 4$, $c_5 = 0$.",
    },
    # --- Аналіз ---
    {
        "type": "ERROR", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Тарас перевіряв, чи є $50$ членом послідовності $a_n = 3n + 4$. У якому кроці помилка?",
        "steps": [r"$3n + 4 = 50$", r"$3n = 46$, $n = 15\dfrac{1}{3}$", r"Отже, $50$ — член послідовності з номером $15$"],
        "wrong": 2,
        "solution": r"$n$ не натуральне, тож $50$ не є членом послідовності ($a_{15} = 49$, $a_{16} = 52$).",
    },
    {
        "type": "TF", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Послідовність $a_n = 20 - 3n$. Правда чи ні?",
        "statements": [(r"Кожен наступний член на $3$ менший за попередній", True), (r"Додатних членів — $6$", True),
                       (r"$a_7 = 1$", False), (r"Число $-1$ — член послідовності", True)],
        "solution": r"$a_{n+1} - a_n = -3$. $20 - 3n \gt 0$ при $n \le 6$. $a_7 = -1$. $-1 = a_7$.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Який з чисел є членом послідовності $a_n = n^2 + 2n$?",
        "options": [(r"$48$", True), (r"$50$", False), (r"$30$", False), (r"$10$", False), (r"$20$", False)],
        "solution": r"$n^2 + 2n = n(n + 2)$: $3, 8, 15, 24, 35, 48$. $48 = a_6$.",
    },
    {
        "type": "MULTI", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Які послідовності мають усі члени додатні?",
        "options": [(r"$a_n = \dfrac{1}{n}$", True), (r"$a_n = n^2 - n + 1$", True), (r"$a_n = 10 - n$", False), (r"$a_n = (-1)^n n$", False), (r"$a_n = 2^n$", True)],
        "solution": r"$\dfrac1n \gt 0$; $n^2 - n + 1 = n(n - 1) + 1 \ge 1$; $2^n \gt 0$. $a_{10} = 0$ для $10 - n$; $(-1)^1 \cdot 1 = -1$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Знайдіть найменший член послідовності $a_n = n^2 - 8n + 5$.",
        "answer": "-11",
        "solution": r"$a_n = (n - 4)^2 - 11$, найменше при $n = 4$: $-11$.",
    },

    # ===== СХОДИНКА 3 =====
    # --- Моделювання ---
    {
        "type": "CHOICE", "difficulty": 3, "skill": "MODEL",
        "text": r"Знайдіть формулу $n$-го члена: $1, -\dfrac{1}{2}, \dfrac{1}{3}, -\dfrac{1}{4}, \ldots$",
        "options": [(r"$a_n = \dfrac{(-1)^{n+1}}{n}$", True), (r"$a_n = \dfrac{(-1)^{n}}{n}$", False), (r"$a_n = -\dfrac{1}{n}$", False),
                    (r"$a_n = \dfrac{(-1)^{n+1}}{n + 1}$", False), (r"$a_n = (-1)^{n} n$", False)],
        "solution": r"Модуль — $\dfrac1n$, знак чергується, починаючи з $+$: $a_n = \dfrac{(-1)^{n+1}}{n}$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"Бактерія ділиться навпіл щогодини. О 8:00 була одна бактерія. Скільки бактерій буде о 14:00?",
        "answer": "64",
        "solution": r"$b_1 = 1$ (8:00), $b_{n+1} = 2b_n$. 14:00 — це $b_7 = 2^6 = 64$.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "MODEL",
        "text": r"Фігури з точок: $1$, $3$, $6$, $10$, … (трикутні числа). Яка формула $n$-го члена?",
        "options": [(r"$\dfrac{n(n + 1)}{2}$", True), (r"$n^2 - 1$", False), (r"$2n - 1$", False), (r"$\dfrac{n^2}{2}$", False), (r"$n(n - 1)$", False)],
        "solution": r"$n$-та фігура — $1 + 2 + \ldots + n = \dfrac{n(n + 1)}{2}$. Перевірка: $1, 3, 6, 10$ ✓.",
    },
    {
        "type": "FIELDS", "difficulty": 3, "skill": "MODEL",
        "text": r"$a_n = pn + q$, $a_2 = 7$, $a_5 = 16$. Знайдіть $p$ і $q$.",
        "fields": [("$p$:", "3"), ("$q$:", "1")],
        "solution": r"$2p + q = 7$, $5p + q = 16$: $3p = 9$, $p = 3$, $q = 1$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"Сума перших $n$ членів деякої послідовності дорівнює $S_n = n^2 + 3n$. Знайдіть $a_5$.",
        "answer": "12",
        "solution": r"$a_5 = S_5 - S_4 = 40 - 28 = 12$.",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Скільки членів послідовності $a_n = \dfrac{60}{n}$ є натуральними числами?",
        "answer": "12",
        "solution": r"$n$ має бути дільником $60$: $1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 60$ — $12$ дільників.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"$a_1 = 2$, $a_{n+1} = \dfrac{1}{1 - a_n}$. Знайдіть $a_{100}$.",
        "answer": "2",
        "solution": r"$a_2 = -1$, $a_3 = \dfrac12$, $a_4 = 2$ — період $3$. $100 = 3 \cdot 33 + 1$, тож $a_{100} = a_1 = 2$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Скільки членів послідовності $a_n = n^2 - 10n$ від'ємні?",
        "answer": "9",
        "solution": r"$n(n - 10) \lt 0$ при $0 \lt n \lt 10$: $n = 1, \ldots, 9$.",
    },
    {
        "type": "FIELDS", "difficulty": 3, "skill": "SOLVE",
        "text": r"$a_1 = 1$, $a_2 = 1$, $a_{n+2} = a_{n+1} + a_n$ (послідовність Фібоначчі). Знайдіть $a_8$ і $a_{10}$.",
        "fields": [("$a_8$:", "21"), ("$a_{10}$:", "55")],
        "solution": r"$1, 1, 2, 3, 5, 8, 13, 21, 34, 55$.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "SOLVE",
        "text": r"$a_n = \dfrac{2n + 7}{n}$. Скільки членів послідовності — цілі числа?",
        "options": [(r"$2$", True), (r"$1$", False), (r"$7$", False), (r"$3$", False), (r"безліч", False)],
        "solution": r"$a_n = 2 + \dfrac{7}{n}$: ціле при $n = 1$ і $n = 7$.",
    },
    # --- Аналіз ---
    {
        "type": "TF", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [(r"Послідовність $a_n = \dfrac{n}{n + 1}$ зростає", True), (r"Усі члени $a_n = \dfrac{n}{n + 1}$ менші за $1$", True),
                       (r"Послідовність $a_n = (-2)^n$ зростає", False), (r"Послідовність $a_n = 5$ — нескінченна", True)],
        "solution": r"$\dfrac{n}{n+1} = 1 - \dfrac{1}{n + 1}$ — зростає і $\lt 1$. $(-2)^n$: $-2, 4, -8$ — не зростає. Стала послідовність має нескінченно багато членів.",
    },
    {
        "type": "ERROR", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Оля шукала $a_{n+1} - a_n$ для $a_n = n^2$. У якому кроці помилка?",
        "steps": [r"$a_{n+1} = n^2 + 1$", r"$a_{n+1} - a_n = n^2 + 1 - n^2$", r"$= 1$"],
        "wrong": 0,
        "solution": r"$a_{n+1} = (n + 1)^2 = n^2 + 2n + 1$, тому різниця $2n + 1$.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Яка з послідовностей має найбільший член?",
        "options": [(r"$a_n = 10n - n^2$", True), (r"$a_n = 2n + 1$", False), (r"$a_n = n^2$", False), (r"$a_n = 3^n$", False), (r"$a_n = n$", False)],
        "solution": r"$10n - n^2 = 25 - (n - 5)^2 \le 25$ — найбільший $a_5 = 25$. Решта зростають необмежено.",
    },
    {
        "type": "MULTI", "difficulty": 3, "skill": "ANALYZE",
        "text": r"$a_1 = 3$, $a_{n+1} = a_n^2 - 2a_n$. Що правильно?",
        "options": [(r"$a_2 = 3$", True), (r"усі члени дорівнюють $3$", True), (r"$a_3 = 9$", False), (r"послідовність зростає", False)],
        "solution": r"$a_2 = 9 - 6 = 3$, і далі так само — стала послідовність.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Знайдіть найбільший член послідовності $a_n = -n^2 + 7n + 3$.",
        "answer": "15",
        "solution": r"Вершина параболи при $n = 3{,}5$: найближчі натуральні $3$ і $4$. $a_3 = a_4 = -9 + 21 + 3 = 15$.",
    },

    # ===== БОСИ =====
    {
        "type": "SHORT", "difficulty": 4, "skill": "MODEL",
        "text": r"Сума перших $n$ членів послідовності $S_n = 2n^2 - n$. Знайдіть $a_{10}$.",
        "answer": "37",
        "solution": r"$a_{10} = S_{10} - S_9 = 190 - 153 = 37$.",
    },
    {
        "type": "EXPR", "difficulty": 4, "skill": "MODEL",
        "text": r"Знайдіть формулу $n$-го члена: $\dfrac{1}{2}, \dfrac{1}{6}, \dfrac{1}{12}, \dfrac{1}{20}, \ldots$ (дробом через «/»).",
        "answer": "1/(n(n+1))", "vars": ["n"],
        "solution": r"$2 = 1 \cdot 2$, $6 = 2 \cdot 3$, $12 = 3 \cdot 4$: $a_n = \dfrac{1}{n(n + 1)}$.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "SOLVE",
        "text": r"$a_1 = 1$, $a_{n+1} = a_n + 2n + 1$. Знайдіть $a_{20}$.",
        "answer": "400",
        "solution": r"$1, 4, 9, 16, \ldots$ — це $n^2$ (бо $(n + 1)^2 = n^2 + 2n + 1$). $a_{20} = 400$.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "SOLVE",
        "text": r"Скільки членів послідовності $a_n = \dfrac{n^2 + 24}{n}$ є цілими числами?",
        "answer": "8",
        "solution": r"$a_n = n + \dfrac{24}{n}$: $n$ — дільник $24$: $1, 2, 3, 4, 6, 8, 12, 24$.",
    },
    {
        "type": "TF", "difficulty": 4, "skill": "ANALYZE",
        "text": r"Послідовність $a_n = \dfrac{3n - 1}{n + 2}$. Правда чи ні?",
        "statements": [(r"Усі члени менші за $3$", True), (r"Послідовність зростає", True), (r"Є член, що дорівнює $3$", False), (r"$a_1 = \dfrac{2}{3}$", True)],
        "solution": r"$a_n = 3 - \dfrac{7}{n + 2}$: менше за $3$ і зростає. Члена $3$ немає, бо $\dfrac{7}{n + 2} \ne 0$. $a_1 = \dfrac{2}{3}$.",
    },
    {
        "type": "SHORT", "difficulty": 5, "skill": "SOLVE",
        "text": r"$a_1 = 1$, $a_{n+1} = \dfrac{a_n}{1 + a_n}$. Знайдіть $a_{2025}$ і запишіть відповідь як $\dfrac{1}{k}$ — укажіть $k$.",
        "answer": "2025",
        "solution": r"$\dfrac{1}{a_{n+1}} = \dfrac{1 + a_n}{a_n} = \dfrac{1}{a_n} + 1$. Тому $\dfrac{1}{a_n} = n$, $a_{2025} = \dfrac{1}{2025}$.",
    },
    {
        "type": "SHORT", "difficulty": 5, "skill": "ANALYZE",
        "text": r"Скільки членів послідовності $a_n = n^2 - 20n + 90$ менші за $10$?",
        "answer": "9",
        "solution": r"$(n - 10)^2 - 10 \lt 10$ ⟹ $(n - 10)^2 \lt 20$. Цілі $n - 10$ від $-4$ до $4$ ($5^2 = 25 \gt 20$): $n = 6, \ldots, 14$ — $9$ членів.",
    },
]
