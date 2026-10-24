TOPIC_NAME = "1.8. Функція y = k/x та її графік"
COURSE = "Алгебра (7-9 класи)"
GRADE = "8 клас"

TASKS = [
    # ===== СХОДИНКА 1 =====
    # --- Моделювання ---
    {
        "type": "CHOICE", "difficulty": 1, "skill": "MODEL",
        "text": r"Яка формула задає обернену пропорційність?",
        "options": [(r"$y = \dfrac{8}{x}$", True), (r"$y = 8x$", False), (r"$y = \dfrac{x}{8}$", False), (r"$y = x + 8$", False)],
        "hint": "Змінна $x$ — у знаменнику.",
        "solution": r"$y = \dfrac{k}{x}$ з $k = 8$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "MODEL",
        "text": r"Площа прямокутника $24$ см², довжина $6$ см. Знайдіть ширину (у см).",
        "answer": "4",
        "hint": "$b = \\dfrac{24}{a}$.",
        "solution": r"$24 : 6 = 4$ см.",
    },
    {
        "type": "TF", "difficulty": 1, "skill": "MODEL",
        "text": r"Правда чи ні?",
        "statements": [(r"Графік $y = \dfrac{k}{x}$ — гіпербола", True), (r"Графік $y = \dfrac{3}{x}$ перетинає вісь $Ox$", False), (r"Для $y = \dfrac{k}{x}$ добуток $xy = k$", True)],
        "hint": "Чи може $\\dfrac{3}{x}$ дорівнювати нулю?",
        "solution": r"$\dfrac3x \ne 0$ — графік не перетинає осей.",
    },
    {
        "type": "MATCH", "difficulty": 1, "skill": "MODEL",
        "text": r"Установіть відповідність між функцією (1–3) та чвертями, де лежить її графік (А–Д).",
        "options": [r"А) I і III", r"Б) II і IV", r"В) I і II", r"Г) III і IV", r"Д) лише I"],
        "matches": [(r"1. $y = \dfrac{2}{x}$", r"А) I і III"), (r"2. $y = -\dfrac{2}{x}$", r"Б) II і IV"), (r"3. $y = \dfrac{-7}{x}$", r"Б) II і IV")],
        "hint": "Дивимось на знак $k$.",
        "solution": r"$k \gt 0$ — I і III; $k \lt 0$ — II і IV.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "MODEL",
        "text": r"Відстань $90$ км велосипедист проїхав за $t$ год зі швидкістю $v$. Знайдіть $v$ при $t = 6$ (км/год).",
        "answer": "15",
        "hint": "$v = \\dfrac{90}{t}$.",
        "solution": r"$90 : 6 = 15$ км/год.",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"$y = \dfrac{12}{x}$. Знайдіть $y(-3)$.",
        "answer": "-4",
        "hint": "$12 : (-3)$.",
        "solution": r"$\dfrac{12}{-3} = -4$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"$y = \dfrac{12}{x}$. При якому $x$ значення функції дорівнює $3$?",
        "answer": "4",
        "hint": "$\\dfrac{12}{x} = 3$.",
        "solution": r"$x = 12 : 3 = 4$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"Графік $y = \dfrac{k}{x}$ проходить через точку $(2; 5)$. Знайдіть $k$.",
        "answer": "10",
        "hint": "$k = xy$.",
        "solution": r"$k = 2 \cdot 5 = 10$.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "SOLVE",
        "text": r"Яка точка належить графіку $y = \dfrac{6}{x}$?",
        "options": [(r"$(-2; -3)$", True), (r"$(2; -3)$", False), (r"$(6; 6)$", False), (r"$(3; 3)$", False)],
        "hint": "Перевірте: $xy = 6$?",
        "solution": r"$(-2)(-3) = 6$ ✓.",
    },
    {
        "type": "FIELDS", "difficulty": 1, "skill": "SOLVE",
        "text": r"Заповніть таблицю для $y = \dfrac{-8}{x}$: значення при $x = 2$ і $x = -4$.",
        "fields": [("$y(2)$:", "-4"), ("$y(-4)$:", "2")],
        "hint": "Ділимо $-8$ на $x$.",
        "solution": r"$-8 : 2 = -4$; $-8 : (-4) = 2$.",
    },
    # --- Аналіз ---
    {
        "type": "ERROR", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Оля шукала $k$, якщо графік $y = \dfrac{k}{x}$ проходить через $(-4; 3)$. У якому кроці помилка?",
        "steps": [r"$3 = \dfrac{k}{-4}$", r"$k = 3 : (-4) = -0{,}75$"],
        "wrong": 1,
        "hint": "Щоб знайти ділене, множимо.",
        "solution": r"$k = 3 \cdot (-4) = -12$.",
    },
    {
        "type": "MULTI", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Які твердження про $y = \dfrac{5}{x}$ правильні?",
        "options": [(r"при $x \gt 0$ значення додатні", True), (r"графік у I і III чвертях", True), (r"$y(0) = 0$", False), (r"$y(1) = 5$", True)],
        "hint": "Чи можна ділити на $0$?",
        "solution": r"$x = 0$ не входить в область визначення.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Тарас: «Графік $y = \dfrac{4}{x}$ проходить через початок координат». Чи правий він?",
        "options": [(r"Ні, $x \ne 0$", True), (r"Так", False), (r"Так, бо $y(0) = 4$", False), (r"Ні, бо $y(0) = 0$", False)],
        "hint": "Підставте $x = 0$.",
        "solution": r"На нуль ділити не можна — точки з $x = 0$ на графіку немає.",
    },
    {
        "type": "GROUP", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Чи належить точка графіку $y = \dfrac{12}{x}$?",
        "groups": ["належить", "не належить"],
        "items": [(r"$(3; 4)$", 0), (r"$(-6; -2)$", 0), (r"$(24; 0{,}5)$", 0), (r"$(2; -6)$", 1), (r"$(4; 4)$", 1), (r"$(-3; 4)$", 1)],
        "hint": "Перевірте $xy = 12$.",
        "solution": r"$12$, $12$, $12$ — належать; $-12$, $16$, $-12$ — ні.",
    },
    {
        "type": "TF", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Для $y = -\dfrac{6}{x}$ правда чи ні?",
        "statements": [(r"$y(2) = -3$", True), (r"$y(-2) = -3$", False), (r"графік у II і IV чвертях", True)],
        "hint": "$-6 : (-2) = 3$.",
        "solution": r"$y(-2) = 3$. $k = -6 \lt 0$.",
    },

    # ===== СХОДИНКА 2 =====
    # --- Моделювання ---
    {
        "type": "SHORT", "difficulty": 2, "skill": "MODEL",
        "text": r"$6$ робітників виконують роботу за $10$ днів. За скільки днів виконають її $15$ робітників з тією самою продуктивністю?",
        "answer": "4",
        "solution": r"Кількість робітників і днів — обернено пропорційні: $6 \cdot 10 = 15 \cdot t$, $t = 4$.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "MODEL",
        "text": r"Яка залежність є оберненою пропорційністю?",
        "options": [(r"час руху від швидкості при сталій відстані", True), (r"вартість від кількості товару", False), (r"периметр квадрата від сторони", False), (r"площа квадрата від сторони", False)],
        "solution": r"$t = \dfrac{s}{v}$; інші — пряма пропорційність або квадрат.",
    },
    {
        "type": "EXPR", "difficulty": 2, "skill": "MODEL",
        "text": r"Графік оберненої пропорційності проходить через $(-3; 4)$. Запишіть формулу функції (вираз для $y$, дробом через «/»).",
        "answer": "-12/x", "vars": ["x"],
        "solution": r"$k = -12$: $y = -\dfrac{12}{x}$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "MODEL",
        "text": r"Об'єм коробки $360$ см³, висота $5$ см. Площа дна $S$ — функція від висоти. Знайдіть $S$ (у см²).",
        "answer": "72",
        "solution": r"$S = \dfrac{360}{h} = 72$ см².",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "MODEL",
        "text": r"Сторони прямокутника $x$ і $y$, площа $18$. Знайдіть $y$, якщо $x$ збільшили втричі від $2$ до $6$ (тобто $x = 6$).",
        "answer": "3",
        "solution": r"$y = \dfrac{18}{6} = 3$ — зменшилося втричі (з $9$).",
    },
    # --- Розв'язування ---
    {
        "type": "FIELDS", "difficulty": 2, "skill": "SOLVE",
        "text": r"Знайдіть точки перетину графіків $y = \dfrac{8}{x}$ і $y = 2x$: абсциси (менша, більша).",
        "fields": [("Менша:", "-2"), ("Більша:", "2")],
        "solution": r"$\dfrac8x = 2x$ ⟹ $x^2 = 4$, $x = \pm 2$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Графік $y = \dfrac{k}{x}$ проходить через $(0{,}5; -8)$. Знайдіть $y(2)$.",
        "answer": "-2",
        "solution": r"$k = -4$; $y(2) = -2$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Знайдіть найбільше значення функції $y = \dfrac{6}{x}$ на відрізку $[2; 6]$.",
        "answer": "3",
        "solution": r"$k \gt 0$, функція спадає при $x \gt 0$: найбільше при $x = 2$: $3$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Знайдіть найменше значення функції $y = -\dfrac{12}{x}$ на відрізку $[1; 4]$.",
        "answer": "-12",
        "solution": r"$k \lt 0$ — зростає: найменше при $x = 1$: $-12$.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "SOLVE",
        "text": r"Графіки $y = \dfrac{k}{x}$ і $y = 3$ перетинаються в точці з абсцисою $-2$. Знайдіть $k$.",
        "options": [(r"$-6$", True), (r"$6$", False), (r"$-1{,}5$", False), (r"$1$", False)],
        "solution": r"$\dfrac{k}{-2} = 3$, $k = -6$.",
    },
    # --- Аналіз ---
    {
        "type": "ERROR", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Тарас: «$y = \dfrac{3}{x}$ спадає, тож $y(-1) \gt y(1)$». У якому кроці помилка?",
        "steps": [r"$k = 3 \gt 0$ — функція спадає на кожному з проміжків $x \lt 0$, $x \gt 0$", r"$-1 \lt 1$, отже, $y(-1) \gt y(1)$"],
        "wrong": 1,
        "solution": r"$-1$ і $1$ — у різних проміжках; $y(-1) = -3 \lt y(1) = 3$.",
    },
    {
        "type": "TF", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [(r"Графік $y = \dfrac{k}{x}$ симетричний відносно початку координат", True), (r"Якщо $x$ збільшити вдвічі, $y$ зменшиться вдвічі", True), (r"$y = \dfrac{k}{x}$ при $k \lt 0$ спадає", False)],
        "solution": r"$(x; y) \to (-x; -y)$ — теж на графіку. $k \lt 0$ — зростає на кожному проміжку.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Точки $A(2; a)$ і $B(5; b)$ лежать на графіку $y = \dfrac{10}{x}$. Порівняйте $a$ і $b$.",
        "options": [(r"$a \gt b$", True), (r"$a \lt b$", False), (r"$a = b$", False), (r"не можна порівняти", False)],
        "solution": r"$a = 5$, $b = 2$; функція спадає при $x \gt 0$.",
    },
    {
        "type": "MULTI", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Які прямі не мають спільних точок з графіком $y = \dfrac{1}{x}$?",
        "options": [(r"$y = 0$", True), (r"$x = 0$", True), (r"$y = -x$", True), (r"$y = x$", False), (r"$y = 1$", False)],
        "solution": r"$\dfrac1x = -x$ ⟹ $x^2 = -1$ — розв'язків немає. $y = x$: $(\pm1; \pm1)$; $y = 1$: $(1; 1)$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Скільки точок з цілими координатами має графік $y = \dfrac{6}{x}$?",
        "answer": "8",
        "solution": r"$x$ — дільник $6$ (зі знаком): $\pm1, \pm2, \pm3, \pm6$ — $8$ точок.",
    },

    # ===== СХОДИНКА 3 =====
    # --- Моделювання ---
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"Басейн наповнюють $4$ однакові труби за $9$ год. Скільки потрібно труб, щоб наповнити його за $6$ год?",
        "answer": "6",
        "solution": r"$4 \cdot 9 = n \cdot 6$, $n = 6$.",
    },
    {
        "type": "EXPR", "difficulty": 3, "skill": "MODEL",
        "text": r"Графік $y = \dfrac{k}{x}$ проходить через точку $(a; 2a)$, $a \ne 0$. Запишіть $k$ через $a$.",
        "answer": "2a^2", "vars": ["a"],
        "solution": r"$k = a \cdot 2a = 2a^2$.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "MODEL",
        "text": r"Гіпербола $y = \dfrac{k}{x}$ і пряма $y = -x + 5$ перетинаються в точці з абсцисою $1$. Знайдіть другу точку перетину.",
        "options": [(r"$(4; 1)$", True), (r"$(1; 4)$ — єдина", False), (r"$(-4; 9)$", False), (r"$(5; 0)$", False), (r"$(2; 3)$", False)],
        "solution": r"$y(1) = 4$, $k = 4$. $\dfrac4x = 5 - x$ ⟹ $x^2 - 5x + 4 = 0$, $(x - 1)(x - 4) = 0$: друга точка $(4; 1)$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"Точки $A(-2; y_1)$ і $B(x_2; 3)$ лежать на одній гіперболі $y = \dfrac{k}{x}$, $y_1 = -9$. Знайдіть $x_2$.",
        "answer": "6",
        "solution": r"$k = (-2)(-9) = 18$; $x_2 = 18 : 3 = 6$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"Прямокутник зі сторонами $x$ і $y$ має площу $20$. На скільки відсотків зменшиться $y$, якщо $x$ збільшити на $25\%$?",
        "answer": "20",
        "solution": r"$x' = 1{,}25x$, $y' = \dfrac{20}{1{,}25x} = 0{,}8y$ — менше на $20\%$.",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Розв'яжіть графічно рівняння $\dfrac{3}{x} = x - 2$ — знайдіть додатний корінь.",
        "answer": "3",
        "solution": r"$x^2 - 2x - 3 = 0$: $(x - 3)(x + 1) = 0$; додатний $3$ (перевірка: $1 = 1$ ✓).",
    },
    {
        "type": "FIELDS", "difficulty": 3, "skill": "SOLVE",
        "text": r"Знайдіть найменше і найбільше значення $y = \dfrac{-6}{x}$ на відрізку $[-3; -1]$.",
        "fields": [("Найменше:", "2"), ("Найбільше:", "6")],
        "solution": r"$k \lt 0$ — зростає на $x \lt 0$: $y(-3) = 2$, $y(-1) = 6$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Гіпербола $y = \dfrac{k}{x}$ проходить через $(2; 6)$ і $(m; -4)$. Знайдіть $m$.",
        "answer": "-3",
        "solution": r"$k = 12$, $m = \dfrac{12}{-4} = -3$.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "SOLVE",
        "text": r"Яка множина значень $y = \dfrac{4}{x}$ при $x \in [1; 4]$?",
        "options": [(r"$[1; 4]$", True), (r"$[4; 16]$", False), (r"$[0; 4]$", False), (r"$(0; +\infty)$", False), (r"$\left[\dfrac14; 1\right]$", False)],
        "solution": r"Функція спадає: від $y(1) = 4$ до $y(4) = 1$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Скільки розв'язків має рівняння $\dfrac{2}{x} = x + 1$?",
        "answer": "2",
        "solution": r"$x^2 + x - 2 = 0$: $(x + 2)(x - 1) = 0$ — два корені $-2$ і $1$.",
    },
    # --- Аналіз ---
    {
        "type": "TF", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [(r"Будь-яка пряма $y = kx$ з $k \gt 0$ перетинає гіперболу $y = \dfrac{1}{x}$ у двох точках", True),
                       (r"Пряма $y = 2$ перетинає будь-яку гіперболу $y = \dfrac{k}{x}$ рівно в одній точці", True),
                       (r"Гіперболи $y = \dfrac{2}{x}$ і $y = \dfrac{3}{x}$ мають спільну точку", False)],
        "solution": r"$kx = \dfrac1x$ ⟹ $x^2 = \dfrac1k$ — два корені. $\dfrac{k}{x} = 2$, $x = \dfrac{k}{2}$ — один. $\dfrac2x = \dfrac3x$ — неможливо.",
    },
    {
        "type": "ERROR", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Оля шукала множину значень $y = \dfrac{6}{x}$ при $x \in [-3; 2]$, $x \ne 0$. У якому кроці помилка?",
        "steps": [r"$y(-3) = -2$, $y(2) = 3$", r"Функція спадає", r"Множина значень $[-2; 3]$"],
        "wrong": 2,
        "solution": r"Проміжок містить $0$, функція має дві вітки: при $x \in [-3; 0)$: $y \le -2$; при $x \in (0; 2]$: $y \ge 3$. Отже, $(-\infty; -2] \cup [3; +\infty)$.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "ANALYZE",
        "text": r"При яких $k$ графік $y = \dfrac{k}{x}$ не перетинає пряму $y = x$?",
        "options": [(r"$k \lt 0$", True), (r"$k \gt 0$", False), (r"$k = 1$", False), (r"при будь-яких", False), (r"таких $k$ немає", False)],
        "solution": r"$x^2 = k$ не має розв'язків при $k \lt 0$.",
    },
    {
        "type": "GROUP", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Скільки спільних точок має гіпербола $y = \dfrac{4}{x}$ з прямою?",
        "groups": ["жодної", "одну", "дві"],
        "items": [(r"$y = -x$", 0), (r"$y = 1$", 1), (r"$y = x$", 2), (r"$x = 2$", 1), (r"$y = 0$", 0), (r"$y = 4x$", 2)],
        "solution": r"$x^2 = -4$ — немає; $y = 1$: $x = 4$; $x^2 = 4$; $x = 2$: $y = 2$; $y = 0$ — немає; $x^2 = 1$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Скільки точок з натуральними координатами має графік $y = \dfrac{24}{x}$?",
        "answer": "8",
        "solution": r"$x$ — натуральний дільник $24$: $1, 2, 3, 4, 6, 8, 12, 24$.",
    },

    # ===== БОСИ =====
    {
        "type": "SHORT", "difficulty": 4, "skill": "MODEL",
        "text": r"Точка $M$ лежить на гіперболі $y = \dfrac{12}{x}$ у I чверті. З неї опущено перпендикуляри на осі. Знайдіть площу утвореного прямокутника.",
        "answer": "12",
        "solution": r"Сторони — $x$ і $y$, площа $xy = 12$ для будь-якої точки.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "MODEL",
        "text": r"Гіпербола $y = \dfrac{k}{x}$ і пряма $y = 2x - 3$ перетинаються в точці з абсцисою $2$. Знайдіть абсцису другої точки перетину.",
        "answer": "-0,5",
        "solution": r"$y(2) = 1$, $k = 2$. $\dfrac2x = 2x - 3$ ⟹ $2x^2 - 3x - 2 = 0$ ⟹ $(x - 2)(2x + 1) = 0$, $x = -0{,}5$.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "SOLVE",
        "text": r"Скільки розв'язків має рівняння $\dfrac{4}{x} = |x|$?",
        "answer": "1",
        "solution": r"$x \gt 0$: $x^2 = 4$, $x = 2$. $x \lt 0$: ліва частина від'ємна, права додатна — немає.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "SOLVE",
        "text": r"Знайдіть найменше значення функції $y = \dfrac{12}{x}$ на відрізку $[2; 6]$, помножене на найбільше значення на тому самому відрізку.",
        "answer": "12",
        "solution": r"Найменше $y(6) = 2$, найбільше $y(2) = 6$; добуток $12$.",
    },
    {
        "type": "TF", "difficulty": 4, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [(r"Пряма $y = -x + 4$ дотикається до гіперболи $y = \dfrac{4}{x}$ (одна спільна точка)", True), (r"Пряма $y = -x + 5$ перетинає $y = \dfrac{4}{x}$ у двох точках", True), (r"Пряма $y = -x + 3$ перетинає $y = \dfrac{4}{x}$", False)],
        "solution": r"$\dfrac4x = -x + b$ ⟹ $x^2 - bx + 4 = 0$. $b = 4$: $(x - 2)^2 = 0$ — одна точка. $b = 5$: $(x - 1)(x - 4) = 0$ — дві. $b = 3$: $x^2 - 3x + 4 = (x - 1{,}5)^2 + 1{,}75 \gt 0$ — жодної.",
    },
    {
        "type": "SHORT", "difficulty": 5, "skill": "SOLVE",
        "text": r"Пряма, що проходить через початок координат, перетинає гіперболу $y = \dfrac{8}{x}$ у точках $A$ і $B$, абсциса $A$ дорівнює $2$. Знайдіть довжину $AB$, піднесену до квадрата.",
        "answer": "80",
        "solution": r"$A(2; 4)$, $B(-2; -4)$ (симетрія). $AB^2 = 4^2 + 8^2 = 80$.",
    },
    {
        "type": "SHORT", "difficulty": 5, "skill": "MODEL",
        "text": r"Точки $A(1; 6)$ і $B(3; 2)$ лежать на гіперболі $y = \dfrac{6}{x}$. Знайдіть площу трикутника $OAB$ ($O$ — початок координат).",
        "answer": "8",
        "solution": r"Площа $OAB$ = площа трапеції під $AB$ між $x = 1$ і $x = 3$ (бо трикутники $O$-$A$-$x_A$ і $O$-$B$-$x_B$ мають однакову площу $3$): $\dfrac{(6 + 2)}{2} \cdot 2 = 8$.",
    },
]
