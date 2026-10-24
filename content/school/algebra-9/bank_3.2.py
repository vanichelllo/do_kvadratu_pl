TOPIC_NAME = "3.2. Арифметична прогресія"
COURSE = "Алгебра (7-9 класи)"
GRADE = "9 клас"

TASKS = [
    # ===== СХОДИНКА 1 =====
    # --- Моделювання ---
    {
        "type": "MULTI", "difficulty": 1, "skill": "MODEL",
        "text": r"Які послідовності — арифметичні прогресії?",
        "options": [(r"$3, 7, 11, 15, \ldots$", True), (r"$10, 8, 6, 4, \ldots$", True), (r"$2, 4, 8, 16, \ldots$", False), (r"$5, 5, 5, \ldots$", True), (r"$1, 4, 9, 16, \ldots$", False)],
        "hint": "Різниця сусідніх членів має бути сталою.",
        "solution": r"$d = 4$, $d = -2$, $d = 0$. У $2, 4, 8$ і $1, 4, 9$ різниці змінюються.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "MODEL",
        "text": r"Знайдіть різницю арифметичної прогресії $15, 11, 7, \ldots$",
        "answer": "-4",
        "hint": "$d = a_2 - a_1$.",
        "solution": r"$11 - 15 = -4$.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "MODEL",
        "text": r"Яка формула $n$-го члена арифметичної прогресії?",
        "options": [(r"$a_n = a_1 + (n - 1)d$", True), (r"$a_n = a_1 + nd$", False), (r"$a_n = a_1 \cdot d^{n-1}$", False), (r"$a_n = nd$", False)],
        "hint": "Від $a_1$ до $a_n$ — $n - 1$ кроків.",
        "solution": r"$a_n = a_1 + (n - 1)d$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "MODEL",
        "text": r"У першому ряду $12$ крісел, у кожному наступному — на $2$ більше. Скільки крісел у $8$-му ряду?",
        "answer": "26",
        "hint": "$a_8 = a_1 + 7d$.",
        "solution": r"$12 + 7 \cdot 2 = 26$.",
    },
    {
        "type": "MATCH", "difficulty": 1, "skill": "MODEL",
        "text": r"Установіть відповідність між прогресією (1–3) та її різницею (А–Д).",
        "options": [r"А) $3$", r"Б) $-3$", r"В) $0{,}5$", r"Г) $2$", r"Д) $-0{,}5$"],
        "matches": [(r"1. $1; 4; 7; \ldots$", r"А) $3$"), (r"2. $2; 1{,}5; 1; \ldots$", r"Д) $-0{,}5$"), (r"3. $-1; -4; -7; \ldots$", r"Б) $-3$")],
        "hint": "Від другого члена відніміть перший.",
        "solution": r"$4 - 1 = 3$; $1{,}5 - 2 = -0{,}5$; $-4 - (-1) = -3$.",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"$a_1 = 5$, $d = 4$. Знайдіть $a_{11}$.",
        "answer": "45",
        "hint": "$a_{11} = a_1 + 10d$.",
        "solution": r"$5 + 40 = 45$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"$a_1 = 3$, $a_{10} = 21$. Знайдіть $S_{10}$.",
        "answer": "120",
        "hint": "$S_n = \\dfrac{a_1 + a_n}{2} \\cdot n$.",
        "solution": r"$\dfrac{3 + 21}{2} \cdot 10 = 120$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"$a_4 = 10$, $a_6 = 18$. Знайдіть $a_5$.",
        "answer": "14",
        "hint": "Середнє арифметичне сусідніх.",
        "solution": r"$\dfrac{10 + 18}{2} = 14$.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "SOLVE",
        "text": r"$a_1 = 20$, $d = -3$. Знайдіть $a_6$.",
        "options": [(r"$5$", True), (r"$2$", False), (r"$35$", False), (r"$-18$", False)],
        "hint": "$a_6 = a_1 + 5d$.",
        "solution": r"$20 - 15 = 5$. Б — $6d$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"Знайдіть суму $1 + 2 + 3 + \ldots + 50$.",
        "answer": "1275",
        "hint": "$S_{50} = \\dfrac{1 + 50}{2} \\cdot 50$.",
        "solution": r"$51 \cdot 25 = 1275$.",
    },
    # --- Аналіз ---
    {
        "type": "ERROR", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Оля шукала $a_{12}$ для $a_1 = 2$, $d = 5$. У якому кроці помилка?",
        "steps": [r"$a_{12} = a_1 + 12d$", r"$= 2 + 60 = 62$"],
        "wrong": 0,
        "hint": "Скільки кроків від $a_1$ до $a_{12}$?",
        "solution": r"$a_{12} = a_1 + 11d = 57$.",
    },
    {
        "type": "TF", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [(r"Якщо $d \gt 0$, прогресія зростає", True), (r"У прогресії $10, 7, 4, \ldots$ $d = 3$", False), (r"Кожен член (крім першого) — середнє арифметичне сусідніх", True)],
        "hint": "$d = 7 - 10$.",
        "solution": r"$d = -3$ — прогресія спадає.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Тарас: «$5, 9, 13, 18$ — арифметична прогресія». Чи правий він?",
        "options": [(r"Ні: $18 - 13 = 5 \ne 4$", True), (r"Так, $d = 4$", False), (r"Так, $d = 5$", False), (r"Ні: члени мають спадати", False)],
        "hint": "Перевірте всі різниці.",
        "solution": r"Різниці $4, 4, 5$ — не сталі.",
    },
    {
        "type": "GROUP", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Прогресія зростає чи спадає?",
        "groups": ["зростає", "спадає"],
        "items": [(r"$a_1 = -5$, $d = 2$", 0), (r"$a_1 = 10$, $d = -1$", 1), (r"$-3, -1, 1, \ldots$", 0), (r"$7, 4, 1, \ldots$", 1), (r"$a_n = 3n - 8$", 0), (r"$a_n = 5 - 2n$", 1)],
        "hint": "Дивимося на знак $d$.",
        "solution": r"$d \gt 0$ — зростає: $2$, $2$, $3$. $d \lt 0$ — спадає: $-1$, $-3$, $-2$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Скільки членів у прогресії $3, 6, 9, \ldots, 60$?",
        "answer": "20",
        "hint": "$a_n = 3n$.",
        "solution": r"$3n = 60$, $n = 20$.",
    },

    # ===== СХОДИНКА 2 =====
    # --- Моделювання ---
    {
        "type": "FIELDS", "difficulty": 2, "skill": "MODEL",
        "text": r"$a_2 = 7$, $a_5 = 19$. Знайдіть $a_1$ і $d$.",
        "fields": [("$a_1$:", "3"), ("$d$:", "4")],
        "solution": r"$3d = 12$, $d = 4$; $a_1 = 7 - 4 = 3$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "MODEL",
        "text": r"Тіло за першу секунду падіння пролітає $4{,}9$ м, а за кожну наступну — на $9{,}8$ м більше. Скільки метрів воно пролетить за $5$-ту секунду?",
        "answer": "44,1",
        "solution": r"$4{,}9 + 4 \cdot 9{,}8 = 44{,}1$ м.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "MODEL",
        "text": r"Тарас у перший день пробіг $2$ км, а кожного наступного — на $0{,}5$ км більше. Скільки кілометрів він пробіг за $10$ днів?",
        "answer": "42,5",
        "solution": r"$S_{10} = \dfrac{2 \cdot 2 + 9 \cdot 0{,}5}{2} \cdot 10 = 42{,}5$ км.",
    },
    {
        "type": "EXPR", "difficulty": 2, "skill": "MODEL",
        "text": r"Запишіть формулу $n$-го члена прогресії $7, 4, 1, \ldots$",
        "answer": "10-3n", "vars": ["n"],
        "solution": r"$a_n = 7 - 3(n - 1) = 10 - 3n$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "MODEL",
        "text": r"Між числами $2$ і $17$ вставте $4$ числа так, щоб вийшла арифметична прогресія. Знайдіть різницю.",
        "answer": "3",
        "solution": r"Усього $6$ членів: $17 = 2 + 5d$, $d = 3$.",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"$a_1 = -10$, $d = 3$. Знайдіть $S_{12}$.",
        "answer": "78",
        "solution": r"$\dfrac{-20 + 11 \cdot 3}{2} \cdot 12 = \dfrac{13}{2} \cdot 12 = 78$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Чи є число $100$ членом прогресії $4, 10, 16, \ldots$? Якщо так, укажіть номер, якщо ні — запишіть $0$.",
        "answer": "17",
        "solution": r"$4 + 6(n - 1) = 100$, $n - 1 = 16$, $n = 17$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Знайдіть суму всіх натуральних чисел від $1$ до $99$, кратних $3$.",
        "answer": "1683",
        "solution": r"$3, 6, \ldots, 99$: $33$ члени, $S = \dfrac{3 + 99}{2} \cdot 33 = 1683$.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "SOLVE",
        "text": r"$a_3 + a_7 = 20$. Знайдіть $a_5$.",
        "options": [(r"$10$", True), (r"$20$", False), (r"$5$", False), (r"$40$", False), (r"не можна визначити", False)],
        "solution": r"$a_3 + a_7 = 2a_1 + 8d = 2a_5$, $a_5 = 10$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Знайдіть перший від'ємний член прогресії $50, 46, 42, \ldots$",
        "answer": "-2",
        "solution": r"$50 - 4(n - 1) \lt 0$ ⟹ $n \gt 13{,}5$, $n = 14$: $a_{14} = 50 - 52 = -2$.",
    },
    # --- Аналіз ---
    {
        "type": "ERROR", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Тарас рахував кількість членів прогресії $10, 15, \ldots, 95$. У якому кроці помилка?",
        "steps": [r"$d = 5$", r"$n = \dfrac{95 - 10}{5} = 17$", r"Відповідь: $17$ членів"],
        "wrong": 1,
        "solution": r"$95 = 10 + (n - 1) \cdot 5$ ⟹ $n - 1 = 17$, $n = 18$.",
    },
    {
        "type": "TF", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [(r"$a_1 + a_n = a_2 + a_{n-1}$", True), (r"Послідовність $a_n = 5n + 2$ — арифметична прогресія", True), (r"Послідовність $a_n = n^2$ — арифметична прогресія", False), (r"$S_n - S_{n-1} = a_n$", True)],
        "solution": r"Пари рівновіддалених членів мають однакову суму. $a_{n+1} - a_n = 5$ — стала; для $n^2$ — $2n + 1$, змінна.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Числа $x - 1$, $2x$, $x + 7$ — послідовні члени арифметичної прогресії. Знайдіть $x$.",
        "options": [(r"$3$", True), (r"$4$", False), (r"$6$", False), (r"$-3$", False), (r"$1$", False)],
        "solution": r"$2x = \dfrac{(x - 1) + (x + 7)}{2} = x + 3$, $x = 3$.",
    },
    {
        "type": "MULTI", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Яка формула задає арифметичну прогресію?",
        "options": [(r"$a_n = 2n - 5$", True), (r"$a_n = 7$", True), (r"$a_n = \dfrac{n}{3} + 1$", True), (r"$a_n = 2^n$", False), (r"$a_n = \dfrac{1}{n}$", False)],
        "solution": r"Лінійна формула $a_n = kn + b$ задає прогресію з $d = k$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "ANALYZE",
        "text": r"$S_n = n^2 + 2n$. Знайдіть різницю прогресії.",
        "answer": "2",
        "solution": r"$a_1 = S_1 = 3$, $a_2 = S_2 - S_1 = 8 - 3 = 5$, $d = 2$.",
    },

    # ===== СХОДИНКА 3 =====
    # --- Моделювання ---
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"Кути трикутника утворюють арифметичну прогресію. Знайдіть середній кут (у градусах).",
        "answer": "60",
        "solution": r"$(b - d) + b + (b + d) = 180$, $b = 60^\circ$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"Колоди складено так: у нижньому ряду $20$, у кожному наступному на $1$ менше, у верхньому — $8$. Скільки всього колод?",
        "answer": "182",
        "solution": r"$20, 19, \ldots, 8$: $13$ рядів, $S = \dfrac{20 + 8}{2} \cdot 13 = 182$.",
    },
    {
        "type": "FIELDS", "difficulty": 3, "skill": "MODEL",
        "text": r"$a_1 + a_5 = 14$, $a_2 \cdot a_4 = 45$, прогресія зростає. Знайдіть $a_1$ і $d$.",
        "fields": [("$a_1$:", "3"), ("$d$:", "2")],
        "solution": r"$a_3 = 7$; $(7 - d)(7 + d) = 45$, $d^2 = 4$, $d = 2$ (зростає); $a_1 = 3$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"Скільки перших членів прогресії $1, 5, 9, \ldots$ треба взяти, щоб сума дорівнювала $231$?",
        "answer": "11",
        "solution": r"$S_n = \dfrac{2 + 4(n - 1)}{2} n = n(2n - 1) = 231$; $n = 11$ ($11 \cdot 21 = 231$).",
    },
    {
        "type": "EXPR", "difficulty": 3, "skill": "MODEL",
        "text": r"Запишіть $S_n$ для прогресії $1, 3, 5, \ldots$ (суму перших $n$ непарних чисел).",
        "answer": "n^2", "vars": ["n"],
        "solution": r"$S_n = \dfrac{1 + (2n - 1)}{2} \cdot n = n^2$.",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"$a_5 = 8$. Знайдіть $S_9$.",
        "answer": "72",
        "solution": r"$S_9 = \dfrac{a_1 + a_9}{2} \cdot 9 = a_5 \cdot 9 = 72$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Знайдіть суму всіх двоцифрових чисел, які при діленні на $4$ дають остачу $1$.",
        "answer": "1210",
        "solution": r"$13, 17, \ldots, 97$: $n = \dfrac{97 - 13}{4} + 1 = 22$; $S = \dfrac{13 + 97}{2} \cdot 22 = 1210$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"$a_1 = 3$, $S_{10} = 165$. Знайдіть $d$.",
        "answer": "3",
        "solution": r"$\dfrac{6 + 9d}{2} \cdot 10 = 165$ ⟹ $6 + 9d = 33$, $d = 3$.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "SOLVE",
        "text": r"Знайдіть суму перших $20$ членів прогресії, у якій $a_6 + a_{15} = 30$.",
        "options": [(r"$300$", True), (r"$600$", False), (r"$150$", False), (r"$315$", False), (r"$30$", False)],
        "solution": r"$a_1 + a_{20} = a_6 + a_{15} = 30$; $S_{20} = 15 \cdot 20 = 300$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Знайдіть найбільшу суму перших членів прогресії $25, 22, 19, \ldots$",
        "answer": "117",
        "solution": r"Додатні члени: $25 - 3(n - 1) \gt 0$ ⟹ $n \le 9$ ($a_9 = 1$). $S_9 = \dfrac{25 + 1}{2} \cdot 9 = 117$.",
    },
    # --- Аналіз ---
    {
        "type": "TF", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [(r"Якщо $a_n$ — прогресія, то $2a_n + 1$ — теж прогресія", True), (r"Якщо $a_n$ — прогресія, то $a_n^2$ — теж прогресія", False), (r"Члени з парними номерами прогресії утворюють прогресію", True)],
        "solution": r"$2a_n + 1$: різниця $2d$. $a_n^2$: різниці $(2a_n + d)d$ змінні. Парні члени — різниця $2d$.",
    },
    {
        "type": "ERROR", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Оля шукала $S_{15}$, якщо $a_1 = 4$, $d = 2$. У якому кроці помилка?",
        "steps": [r"$a_{15} = 4 + 14 \cdot 2 = 32$", r"$S_{15} = (4 + 32) \cdot 15 = 540$"],
        "wrong": 1,
        "solution": r"Забули поділити на $2$: $S_{15} = 18 \cdot 15 = 270$.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "ANALYZE",
        "text": r"При якому $n$ сума перших $n$ членів прогресії $-14, -11, -8, \ldots$ найменша?",
        "options": [(r"$5$", True), (r"$4$", False), (r"$6$", False), (r"$10$", False), (r"$1$", False)],
        "solution": r"Сума спадає, поки додаємо від'ємні: $a_5 = -2$, $a_6 = 1$. Найменша — $S_5$.",
    },
    {
        "type": "MULTI", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Прогресія з $a_1 = 10$, $d = -2$. Що правильно?",
        "options": [(r"$a_6 = 0$", True), (r"$S_{11} = 0$", True), (r"$S_5 = S_6$", True), (r"$a_{10} = -10$", False)],
        "solution": r"$a_6 = 0$; $S_{11} = 11 a_6 = 0$; $S_6 = S_5 + 0$; $a_{10} = 10 - 18 = -8$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "ANALYZE",
        "text": r"$S_n = 3n^2 - n$. Знайдіть $a_{10}$.",
        "answer": "56",
        "solution": r"$S_{10} - S_9 = 290 - 234 = 56$.",
    },

    # ===== БОСИ =====
    {
        "type": "SHORT", "difficulty": 4, "skill": "MODEL",
        "text": r"Сторони прямокутного трикутника утворюють арифметичну прогресію з різницею $2$. Знайдіть гіпотенузу.",
        "answer": "10",
        "solution": r"$(a - 2)^2 + a^2 = (a + 2)^2$ ⟹ $a^2 = 8a$, $a = 8$: сторони $6, 8, 10$.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "MODEL",
        "text": r"Амфітеатр: у першому ряду $20$ місць, у кожному наступному на $3$ більше, усього $970$ місць. Скільки рядів?",
        "answer": "20",
        "solution": r"$\dfrac{40 + 3(n - 1)}{2} \cdot n = 970$ ⟹ $3n^2 + 37n - 1940 = 0$, $n = 20$ (другий корінь від'ємний). Перевірка: $\dfrac{20 + 77}{2} \cdot 20 = 970$ ✓.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "SOLVE",
        "text": r"$S_{10} = 100$, $S_{20} = 400$. Знайдіть $S_{30}$.",
        "answer": "900",
        "solution": r"$S_n = An^2 + Bn$: $100A + 10B = 100$, $400A + 20B = 400$ ⟹ $A = 1$, $B = 0$. $S_{30} = 900$.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "SOLVE",
        "text": r"Знайдіть суму всіх трицифрових чисел, кратних $7$.",
        "answer": "70336",
        "solution": r"$105, \ldots, 994$: $n = \dfrac{994 - 105}{7} + 1 = 128$; $S = \dfrac{105 + 994}{2} \cdot 128 = 70\,336$.",
    },
    {
        "type": "TF", "difficulty": 4, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [(r"Якщо $S_m = S_n$ ($m \ne n$), то $S_{m+n} = 0$", True), (r"Сума $a_1 + a_2 + \ldots + a_{2k+1} = (2k + 1)a_{k+1}$", True), (r"Якщо $a_1 \gt 0$ і $d \lt 0$, то всі суми $S_n \gt 0$", False)],
        "solution": r"$S_n = An^2 + Bn$; $S_m = S_n$ ⟹ $A(m + n) + B = 0$ ⟹ $S_{m+n} = 0$. Середній член. Із часом члени стають від'ємними, суми — теж.",
    },
    {
        "type": "SHORT", "difficulty": 5, "skill": "SOLVE",
        "text": r"$S_5 = 35$, $S_{10} - S_5 = 110$. Знайдіть $d$.",
        "answer": "3",
        "solution": r"$S_{10} = 145$. $5a_1 + 10d = 35$, $10a_1 + 45d = 145$ ⟹ $25d = 75$, $d = 3$ ($a_1 = 1$).",
    },
    {
        "type": "SHORT", "difficulty": 5, "skill": "ANALYZE",
        "text": r"Скільки існує зростаючих арифметичних прогресій з натуральних чисел, у яких $a_1 = 1$ і серед членів є число $100$?",
        "answer": "6",
        "solution": r"$1 + (n - 1)d = 100$ ⟹ $(n - 1)d = 99$; $d$ — натуральний дільник $99$: $1, 3, 9, 11, 33, 99$ — $6$ прогресій.",
    },
]
