TOPIC_NAME = "3.3. Геометрична прогресія"
COURSE = "Алгебра (7-9 класи)"
GRADE = "9 клас"

TASKS = [
    # ===== СХОДИНКА 1 =====
    # --- Моделювання ---
    {
        "type": "MULTI", "difficulty": 1, "skill": "MODEL",
        "text": r"Які послідовності — геометричні прогресії?",
        "options": [(r"$2, 6, 18, 54, \ldots$", True), (r"$64, 32, 16, 8, \ldots$", True), (r"$1, -1, 1, -1, \ldots$", True), (r"$2, 4, 6, 8, \ldots$", False), (r"$0, 0, 0, \ldots$", False)],
        "hint": "Відношення сусідніх членів має бути сталим і ненульовим.",
        "solution": r"$q = 3$, $\dfrac12$, $-1$. $2, 4, 6$ — арифметична; нулі не допускаються.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "MODEL",
        "text": r"Знайдіть знаменник прогресії $5, 20, 80, \ldots$",
        "answer": "4",
        "hint": "$q = \\dfrac{b_2}{b_1}$.",
        "solution": r"$20 : 5 = 4$.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "MODEL",
        "text": r"Яка формула $n$-го члена геометричної прогресії?",
        "options": [(r"$b_n = b_1 q^{n-1}$", True), (r"$b_n = b_1 q^n$", False), (r"$b_n = b_1 + (n - 1)q$", False), (r"$b_n = nq$", False)],
        "hint": "Від $b_1$ до $b_n$ — $n - 1$ множень.",
        "solution": r"$b_n = b_1 q^{n-1}$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "MODEL",
        "text": r"Кількість бактерій подвоюється щогодини. Спочатку їх $100$. Скільки їх буде через $3$ години?",
        "answer": "800",
        "hint": "$100 \\cdot 2^3$.",
        "solution": r"$800$.",
    },
    {
        "type": "MATCH", "difficulty": 1, "skill": "MODEL",
        "text": r"Установіть відповідність між прогресією (1–3) та знаменником (А–Д).",
        "options": [r"А) $2$", r"Б) $-2$", r"В) $\dfrac12$", r"Г) $3$", r"Д) $-\dfrac12$"],
        "matches": [(r"1. $3; 6; 12$", r"А) $2$"), (r"2. $8; -4; 2$", r"Д) $-\dfrac12$"), (r"3. $1; -2; 4$", r"Б) $-2$")],
        "hint": "Ділимо другий член на перший.",
        "solution": r"$6 : 3 = 2$; $-4 : 8 = -\dfrac12$; $-2 : 1 = -2$.",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"$b_1 = 4$, $q = 2$. Знайдіть $b_5$.",
        "answer": "64",
        "hint": "$4 \\cdot 2^4$.",
        "solution": r"$64$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"$b_1 = 81$, $q = \dfrac{1}{3}$. Знайдіть $b_4$.",
        "answer": "3",
        "hint": "$81 \\cdot \\left(\\dfrac13\\right)^3$.",
        "solution": r"$81 : 27 = 3$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"$b_1 = 1$, $q = 2$. Знайдіть $S_6$.",
        "answer": "63",
        "hint": "$\\dfrac{2^6 - 1}{2 - 1}$.",
        "solution": r"$63$.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "SOLVE",
        "text": r"$b_3 = 9$, $b_5 = 81$, усі члени додатні. Знайдіть $b_4$.",
        "options": [(r"$27$", True), (r"$45$", False), (r"$36$", False), (r"$729$", False)],
        "hint": "$b_4^2 = b_3 b_5$.",
        "solution": r"$b_4^2 = 729$, $b_4 = 27$. $45$ — середнє арифметичне.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"$b_1 = -2$, $q = -3$. Знайдіть $b_3$.",
        "answer": "-18",
        "hint": "$-2 \\cdot 9$.",
        "solution": r"$-2 \cdot (-3)^2 = -18$.",
    },
    # --- Аналіз ---
    {
        "type": "ERROR", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Оля шукала $b_4$ для $b_1 = 5$, $q = 2$. У якому кроці помилка?",
        "steps": [r"$b_4 = b_1 q^4$", r"$= 5 \cdot 16 = 80$"],
        "wrong": 0,
        "hint": "Скільки множень від $b_1$ до $b_4$?",
        "solution": r"$b_4 = b_1q^3 = 40$.",
    },
    {
        "type": "TF", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [(r"$q = \dfrac{b_2}{b_1}$", True), (r"Член геометричної прогресії може дорівнювати $0$", False), (r"При $q \lt 0$ знаки членів чергуються", True)],
        "hint": "Згадайте означення.",
        "solution": r"Члени ненульові; від'ємний $q$ змінює знак на кожному кроці.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Тарас: «$3, 6, 9, 12$ — геометрична прогресія». Чи правий він?",
        "options": [(r"Ні: $6 : 3 \ne 9 : 6$; це арифметична", True), (r"Так, $q = 3$", False), (r"Так, $q = 2$", False), (r"Ні: члени мають спадати", False)],
        "hint": "Перевірте відношення.",
        "solution": r"$2 \ne 1{,}5$.",
    },
    {
        "type": "GROUP", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Арифметична чи геометрична прогресія?",
        "groups": ["арифметична", "геометрична"],
        "items": [(r"$2, 5, 8, 11$", 0), (r"$2, 6, 18, 54$", 1), (r"$10, 7, 4, 1$", 0), (r"$100, 10, 1, 0{,}1$", 1), (r"$-3, -1, 1, 3$", 0), (r"$5, -10, 20, -40$", 1)],
        "hint": "$+d$ чи $\\times q$?",
        "solution": r"Різниці $3, -3, 2$; знаменники $3, \dfrac{1}{10}, -2$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Скільки членів прогресії $2, 4, 8, \ldots$ менші за $100$?",
        "answer": "6",
        "hint": "Випишіть члени.",
        "solution": r"$2, 4, 8, 16, 32, 64$ — $6$; $128 \gt 100$.",
    },

    # ===== СХОДИНКА 2 =====
    # --- Моделювання ---
    {
        "type": "FIELDS", "difficulty": 2, "skill": "MODEL",
        "text": r"$b_2 = 10$, $b_4 = 40$, $q \gt 0$. Знайдіть $b_1$ і $q$.",
        "fields": [("$b_1$:", "5"), ("$q$:", "2")],
        "solution": r"$q^2 = 4$, $q = 2$; $b_1 = 5$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "MODEL",
        "text": r"Ціна товару щороку щороку множиться на $0{,}9$. Початкова ціна $1000$ грн. Яка ціна через $2$ роки?",
        "answer": "810",
        "solution": r"$1000 \cdot 0{,}81 = 810$ грн.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "MODEL",
        "text": r"М'яч падає з висоти $16$ м і щоразу відскакує на половину попередньої висоти. На яку висоту він підскочить після $3$-го удару?",
        "answer": "2",
        "solution": r"$16 \cdot \left(\dfrac12\right)^3 = 2$ м.",
    },
    {
        "type": "EXPR", "difficulty": 2, "skill": "MODEL",
        "text": r"Запишіть формулу $n$-го члена прогресії $3, 6, 12, \ldots$",
        "answer": "3*2^(n-1)", "vars": ["n"],
        "solution": r"$b_n = 3 \cdot 2^{n-1}$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "MODEL",
        "text": r"Між числами $2$ і $162$ вставте три числа, щоб вийшла зростаюча геометрична прогресія. Знайдіть середнє з вставлених.",
        "answer": "18",
        "solution": r"$162 = 2q^4$, $q = 3$: $2, 6, 18, 54, 162$.",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"$b_1 = 2$, $q = 3$. Знайдіть $S_5$.",
        "answer": "242",
        "solution": r"$\dfrac{2(243 - 1)}{2} = 242$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"$b_4 = 24$, $q = 2$. Знайдіть $b_1$.",
        "answer": "3",
        "solution": r"$b_1 = 24 : 8 = 3$.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "SOLVE",
        "text": r"$b_1 = 1$, $q = -2$. Знайдіть $S_4$.",
        "options": [(r"$-5$", True), (r"$15$", False), (r"$5$", False), (r"$-15$", False), (r"$-8$", False)],
        "solution": r"$1 - 2 + 4 - 8 = -5$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Знайдіть номер члена $1536$ у прогресії $3, 6, 12, \ldots$",
        "answer": "10",
        "solution": r"$3 \cdot 2^{n-1} = 1536$, $2^{n-1} = 512 = 2^9$, $n = 10$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"$b_1 = 64$, $q = \dfrac12$. Знайдіть $S_4$.",
        "answer": "120",
        "solution": r"$64 + 32 + 16 + 8 = 120$.",
    },
    # --- Аналіз ---
    {
        "type": "ERROR", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Тарас: «$b_1 = 2$, $b_3 = 18$. Знайти $q$». У якому кроці помилка?",
        "steps": [r"$b_3 = b_1q^2$", r"$q^2 = 9$", r"$q = 3$ — єдина відповідь"],
        "wrong": 2,
        "solution": r"$q = \pm 3$ — дві прогресії.",
    },
    {
        "type": "TF", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [(r"Добуток членів, рівновіддалених від кінців, однаковий: $b_1b_n = b_2b_{n-1}$", True), (r"Якщо $b_n$ — геометрична, то $b_n^2$ — теж геометрична", True), (r"Якщо $b_n$ — геометрична, то $b_n + 1$ — теж геометрична", False)],
        "solution": r"$b_1 \cdot b_1q^{n-1} = b_1q \cdot b_1q^{n-2}$. Квадрати — знаменник $q^2$. $2, 4, 8 \to 3, 5, 9$ — ні.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Числа $x - 1$, $x + 1$, $2x + 2$ — послідовні члени геометричної прогресії. Знайдіть $x$.",
        "options": [(r"$3$", True), (r"$-1$", False), (r"$1$", False), (r"$2$", False), (r"$5$", False)],
        "solution": r"$(x + 1)^2 = (x - 1)(2x + 2) = 2(x - 1)(x + 1)$ ⟹ $x + 1 = 2(x - 1)$ ($x \ne -1$), $x = 3$: $2, 4, 8$.",
    },
    {
        "type": "MULTI", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Прогресія $b_1 = 1$, $q = -1$. Що правильно?",
        "options": [(r"$S_{10} = 0$", True), (r"$S_{11} = 1$", True), (r"$b_{100} = -1$", True), (r"$S_{10} = 10$", False)],
        "solution": r"$1, -1, 1, -1, \ldots$: парні суми — $0$, непарні — $1$; $b_{100} = (-1)^{99} = -1$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Скільки членів прогресії $\dfrac{1}{4}, \dfrac{1}{2}, 1, \ldots$ не перевищують $100$?",
        "answer": "9",
        "solution": r"$\dfrac14 \cdot 2^{n-1} \le 100$ ⟹ $2^{n-1} \le 400$ ⟹ $n - 1 \le 8$ ($256$). $n = 9$.",
    },

    # ===== СХОДИНКА 3 =====
    # --- Моделювання ---
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"Вклад $10\,000$ грн щороку зростає в $1{,}1$ раза. Скільки гривень буде через $3$ роки?",
        "answer": "13310",
        "solution": r"$10\,000 \cdot 1{,}331 = 13\,310$ грн.",
    },
    {
        "type": "FIELDS", "difficulty": 3, "skill": "MODEL",
        "text": r"Сума першого і третього членів геометричної прогресії $20$, а сума другого і четвертого — $40$. Знайдіть $b_1$ і $q$.",
        "fields": [("$b_1$:", "4"), ("$q$:", "2")],
        "solution": r"$b_1q(1 + q^2) = 40$, $b_1(1 + q^2) = 20$ ⟹ $q = 2$, $b_1 = 4$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"Сторони трикутника утворюють геометричну прогресію, менша сторона $4$, більша $9$. Знайдіть середню сторону.",
        "answer": "6",
        "solution": r"$b^2 = 4 \cdot 9 = 36$, $b = 6$.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "MODEL",
        "text": r"Квадрат зі стороною $8$ поділили на $4$ квадрати і один з них знову на $4$, і так далі. Яка сторона квадрата після $4$-го поділу?",
        "options": [(r"$0{,}5$", True), (r"$1$", False), (r"$2$", False), (r"$0{,}25$", False), (r"$4$", False)],
        "solution": r"Сторона щоразу ділиться на $2$: $8 \cdot \left(\dfrac12\right)^4 = 0{,}5$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"$b_1 + b_2 + b_3 = 26$, $q = 3$. Знайдіть $b_1$.",
        "answer": "2",
        "solution": r"$b_1(1 + 3 + 9) = 26$, $b_1 = 2$.",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"$b_2 = -6$, $b_5 = 48$. Знайдіть $S_5$.",
        "answer": "33",
        "solution": r"$q^3 = -8$, $q = -2$, $b_1 = 3$. $S_5 = \dfrac{3((-2)^5 - 1)}{-3} = \dfrac{3 \cdot (-33)}{-3} = 33$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Скільки перших членів прогресії $1, 2, 4, \ldots$ треба взяти, щоб сума дорівнювала $255$?",
        "answer": "8",
        "solution": r"$2^n - 1 = 255$, $n = 8$.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "SOLVE",
        "text": r"$b_1 b_5 = 36$, усі члени додатні. Знайдіть $b_3$.",
        "options": [(r"$6$", True), (r"$18$", False), (r"$36$", False), (r"$\pm 6$", False), (r"$3$", False)],
        "solution": r"$b_1b_5 = b_3^2$; $b_3 = 6$ (додатні).",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"$b_1 = 3$, $S_3 = 21$, $q \gt 0$. Знайдіть $q$.",
        "answer": "2",
        "solution": r"$3(1 + q + q^2) = 21$, $q^2 + q - 6 = 0$, $q = 2$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"У зростаючій прогресії $b_1 + b_4 = 27$, $b_2 b_3 = 72$. Знайдіть $b_1$.",
        "answer": "3",
        "solution": r"$b_2b_3 = b_1b_4 = 72$; $b_1$ і $b_4$ — корені $t^2 - 27t + 72 = 0$: $3$ і $24$; зростає ⟹ $b_1 = 3$ ($q = 2$).",
    },
    # --- Аналіз ---
    {
        "type": "TF", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [(r"Прогресія з $b_1 \lt 0$, $q \gt 1$ спадає", True), (r"Прогресія з $0 \lt q \lt 1$ і $b_1 \gt 0$ спадає", True), (r"Будь-яка геометрична прогресія монотонна", False)],
        "solution": r"$-1, -2, -4$ — спадає. $8, 4, 2$ — спадає. При $q \lt 0$ — не монотонна.",
    },
    {
        "type": "ERROR", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Оля шукала $S_4$, якщо $b_1 = 5$, $q = 3$. У якому кроці помилка?",
        "steps": [r"$S_4 = \dfrac{b_1(q^4 - 1)}{q - 1}$", r"$= \dfrac{5(81 - 1)}{3 - 1}$", r"$= \dfrac{5 \cdot 80}{2} = 400$"],
        "wrong": 2,
        "solution": r"$\dfrac{400}{2} = 200$.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Числа $a$, $b$, $c$ утворюють і арифметичну, і геометричну прогресії. Що можна стверджувати?",
        "options": [(r"$a = b = c$", True), (r"$b = 0$", False), (r"$a + c = 0$", False), (r"$c = 2a$", False), (r"таких чисел немає", False)],
        "solution": r"$2b = a + c$ і $b^2 = ac$ ⟹ $(a + c)^2 = 4ac$ ⟹ $(a - c)^2 = 0$ ⟹ $a = c = b$.",
    },
    {
        "type": "MULTI", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Геометрична прогресія з $b_1 = 2$, $b_3 = 8$. Якими можуть бути $b_2$ і $S_3$?",
        "options": [(r"$b_2 = 4$, $S_3 = 14$", True), (r"$b_2 = -4$, $S_3 = 6$", True), (r"$b_2 = 5$, $S_3 = 15$", False), (r"$b_2 = 4$, $S_3 = 6$", False)],
        "solution": r"$q = \pm 2$: $2, 4, 8$ або $2, -4, 8$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Знайдіть найменше $n$, для якого $S_n$ прогресії $1, 3, 9, \ldots$ перевищує $1000$.",
        "answer": "7",
        "solution": r"$S_n = \dfrac{3^n - 1}{2}$: $S_6 = 364$, $S_7 = 1093$.",
    },

    # ===== БОСИ =====
    {
        "type": "SHORT", "difficulty": 4, "skill": "MODEL",
        "text": r"Три числа утворюють геометричну прогресію з сумою $21$ і добутком $216$, прогресія зростає. Знайдіть найбільше число.",
        "answer": "12",
        "solution": r"$b^3 = 216$ ⟹ $b = 6$; $\dfrac6q + 6 + 6q = 21$ ⟹ $2q^2 - 5q + 2 = 0$, $q = 2$: $3, 6, 12$.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "MODEL",
        "text": r"Листок паперу товщиною $0{,}1$ мм складають навпіл $10$ разів. Яка товщина пачки (у мм)?",
        "answer": "102,4",
        "solution": r"$0{,}1 \cdot 2^{10} = 102{,}4$ мм.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "SOLVE",
        "text": r"$S_3 = 13$, $S_6 = 364$. Знайдіть $q$.",
        "answer": "3",
        "solution": r"$S_6 = S_3(1 + q^3)$ ⟹ $1 + q^3 = 28$, $q = 3$.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "SOLVE",
        "text": r"Обчисліть $1 + 2 + 4 + \ldots + 512$.",
        "answer": "1023",
        "solution": r"$2^0 + \ldots + 2^9 = 2^{10} - 1 = 1023$.",
    },
    {
        "type": "TF", "difficulty": 4, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [(r"$b_1 b_2 \cdots b_n = (b_1 b_n)^{n/2}$ для додатних членів", True), (r"Числа $2^{b_n}$ для арифметичної $b_n$ утворюють геометричну прогресію", True), (r"Сума геометричної прогресії завжди зростає зі зростанням $n$", False)],
        "solution": r"Пари $b_kb_{n+1-k} = b_1b_n$. $2^{b_{n+1}} : 2^{b_n} = 2^d$. При $q \lt 0$ або від'ємних членах сума може спадати.",
    },
    {
        "type": "SHORT", "difficulty": 5, "skill": "SOLVE",
        "text": r"Сума трьох чисел, що утворюють арифметичну прогресію, $15$. Якщо до них додати $1$, $1$ і $4$, вийде геометрична прогресія. Знайдіть більше з початкових чисел (прогресія зростає).",
        "answer": "8",
        "solution": r"$5 - d$, $5$, $5 + d$; $6 - d$, $6$, $9 + d$: $36 = (6 - d)(9 + d)$ ⟹ $d^2 + 3d - 18 = 0$, $d = 3$ (зростає): $2, 5, 8$; перевірка $3, 6, 12$. Більше — $8$.",
    },
    {
        "type": "SHORT", "difficulty": 5, "skill": "ANALYZE",
        "text": r"Скільки існує зростаючих геометричних прогресій з натуральних чисел, у яких $b_1 = 1$ і $b_4 = 1000$?",
        "answer": "1",
        "solution": r"$q^3 = 1000$, $q = 10$ — одна.",
    },
]
