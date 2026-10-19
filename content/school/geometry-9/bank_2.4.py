TOPIC_NAME = "2.4. Скалярний добуток векторів"
COURSE = "Геометрія (7-9 класи)"
GRADE = "9 клас"

TASKS = [
    # ==========================================
    # СХОДИНКА 1 — БАЗОВИЙ
    # ==========================================
    # --- Моделювання ---
    {
        "type": "CHOICE", "difficulty": 1, "skill": "MODEL",
        "text": r"Що є результатом скалярного добутку двох векторів?",
        "options": [("Число", True), ("Вектор", False), ("Точка", False), ("Кут", False)],
        "hint": r"Згадайте: $\vec a \cdot \vec b = |\vec a|\,|\vec b| \cos\varphi$ — що тут перемножують?",
        "solution": r"Модулі й косинус — числа, тож і добуток — число.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "MODEL",
        "text": r"Яка формула задає скалярний добуток векторів $\vec a$ і $\vec b$, кут між якими $\varphi$?",
        "options": [(r"$|\vec a| \cdot |\vec b| \cdot \cos\varphi$", True), (r"$|\vec a| \cdot |\vec b| \cdot \sin\varphi$", False),
                    (r"$(|\vec a| + |\vec b|) \cos\varphi$", False), (r"$|\vec a| \cdot |\vec b|$", False)],
        "hint": r"Згадайте роботу сили: $A = F \cdot s \cdot \cos\varphi$.",
        "solution": r"$\vec a \cdot \vec b = |\vec a|\,|\vec b| \cos\varphi$. Без косинуса формула правильна лише для $\varphi = 0^\circ$.",
    },
    {
        "type": "GROUP", "difficulty": 1, "skill": "MODEL",
        "text": r"Кут між ненульовими векторами — $\varphi$. Яким буде знак скалярного добутку?",
        "groups": [r"$\vec a \cdot \vec b \gt 0$", r"$\vec a \cdot \vec b = 0$", r"$\vec a \cdot \vec b \lt 0$"],
        "items": [(r"$\varphi = 30^\circ$", 0), (r"$\varphi = 90^\circ$", 1), (r"$\varphi = 150^\circ$", 2), (r"$\varphi = 0^\circ$", 0), (r"$\varphi = 180^\circ$", 2), (r"$\varphi = 120^\circ$", 2)],
        "hint": r"Гострий кут — косинус додатний, прямий — нуль, тупий — від'ємний.",
        "solution": r"$0^\circ$ і $30^\circ$ — добуток додатний; $90^\circ$ — нуль; $120^\circ$, $150^\circ$, $180^\circ$ — від'ємний.",
    },
    {
        "type": "MATCH", "difficulty": 1, "skill": "MODEL",
        "text": r"Для векторів $\vec a(a_1;\,a_2)$ і $\vec b(b_1;\,b_2)$ установіть відповідність між записом (1–3) та його змістом (А–Д).",
        "options": ["А) скалярний добуток", "Б) скалярний квадрат вектора $\\vec a$", "В) умова перпендикулярності",
                    "Г) умова колінеарності", "Д) модуль вектора $\\vec a$"],
        "matches": [(r"1. $a_1 b_1 + a_2 b_2$", "А) скалярний добуток"), (r"2. $a_1^2 + a_2^2$", "Б) скалярний квадрат вектора $\\vec a$"),
                    (r"3. $a_1 b_1 + a_2 b_2 = 0$", "В) умова перпендикулярності")],
        "hint": r"Модуль — з коренем, колінеарність — пропорційні координати.",
        "solution": r"$a_1 b_1 + a_2 b_2$ — добуток; $a_1^2 + a_2^2 = \vec a^{\,2}$; добуток $0$ — вектори перпендикулярні.",
    },
    {
        "type": "TF", "difficulty": 1, "skill": "MODEL",
        "text": r"Правда чи ні?",
        "statements": [
            (r"Сила $20$ Н діє вздовж руху, тіло пройшло $5$ м — робота $100$ Дж", True),
            ("Якщо сила перпендикулярна до напрямку руху, її робота дорівнює нулю", True),
            ("Скалярний добуток не може бути від'ємним", False),
        ],
        "hint": r"$A = F \cdot s \cdot \cos\varphi$; $\cos 90^\circ = 0$.",
        "solution": r"$20 \cdot 5 \cdot 1 = 100$ ✓. $\cos 90^\circ = 0$ ✓. Для тупого кута $\cos\varphi \lt 0$ — добуток від'ємний.",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"Знайдіть скалярний добуток векторів $\vec a(2;\,3)$ і $\vec b(4;\,1)$.",
        "answer": "11",
        "hint": r"$a_1 b_1 + a_2 b_2$.",
        "solution": r"$2 \cdot 4 + 3 \cdot 1 = 8 + 3 = 11$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"$|\vec a| = 5$, $|\vec b| = 2$, кут між векторами $60^\circ$. Знайдіть $\vec a \cdot \vec b$.",
        "answer": "5",
        "hint": r"$\cos 60^\circ = \frac{1}{2}$.",
        "solution": r"$5 \cdot 2 \cdot \frac{1}{2} = 5$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"Знайдіть скалярний квадрат вектора $\vec a(3;\,-4)$.",
        "answer": "25",
        "hint": r"$\vec a^{\,2} = a_1^2 + a_2^2$.",
        "solution": r"$3^2 + (-4)^2 = 9 + 16 = 25$ (і $|\vec a| = 5$).",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "SOLVE",
        "text": r"Знайдіть кут між векторами $\vec a(1;\,2)$ і $\vec b(-2;\,1)$.",
        "options": [(r"$90^\circ$", True), (r"$0^\circ$", False), (r"$45^\circ$", False), (r"$180^\circ$", False)],
        "hint": r"Обчисліть скалярний добуток.",
        "solution": r"$1 \cdot (-2) + 2 \cdot 1 = 0$ — вектори перпендикулярні.",
    },
    {
        "type": "FIELDS", "difficulty": 1, "skill": "SOLVE",
        "text": r"Дано $\vec a(-1;\,3)$ і $\vec b(2;\,4)$. Обчисліть:",
        "fields": [(r"$\vec a \cdot \vec b =$", "10"), (r"$\vec b^{\,2} =$", "20")],
        "hint": r"Множимо відповідні координати й додаємо.",
        "solution": r"$-1 \cdot 2 + 3 \cdot 4 = 10$; $\;2^2 + 4^2 = 20$.",
    },
    # --- Аналіз результатів ---
    {
        "type": "ERROR", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Оля обчислювала $\vec a \cdot \vec b$ для $\vec a(4;\,1)$ і $\vec b(2;\,3)$. У якому кроці помилка?",
        "steps": [r"$\vec a \cdot \vec b = 4 \cdot 2 + 1 \cdot 3$", r"$= 8$ і $3$", r"$= (8;\,3)$"],
        "wrong": 2,
        "hint": r"Скалярний добуток — вектор чи число?",
        "solution": r"Добутки треба додати: $8 + 3 = 11$.",
    },
    {
        "type": "MULTI", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Які пари векторів перпендикулярні?",
        "options": [(r"$(2;\,1)$ і $(-1;\,2)$", True), (r"$(3;\,6)$ і $(1;\,2)$", False), (r"$(4;\,-2)$ і $(1;\,2)$", True), (r"$(1;\,1)$ і $(1;\,-1)$", True), (r"$(2;\,3)$ і $(3;\,2)$", False)],
        "hint": r"Перпендикулярні — скалярний добуток дорівнює $0$.",
        "solution": r"$-2 + 2 = 0$, $4 - 4 = 0$, $1 - 1 = 0$. $(3;\,6)$ і $(1;\,2)$ — колінеарні ($15$), $(2;\,3)$ і $(3;\,2)$ — $12$.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Петро: «Якщо $\vec a \cdot \vec b = 0$ для ненульових векторів, то вони колінеарні». Що правильно?",
        "options": [("Ні: вони перпендикулярні", True), ("Так", False), ("Ні: вони рівні", False), (r"Ні: кут між ними $180^\circ$", False)],
        "hint": r"При якому куті $\cos\varphi = 0$?",
        "solution": r"$|\vec a|\,|\vec b| \cos\varphi = 0$ при ненульових векторах лише якщо $\cos\varphi = 0$, тобто $\varphi = 90^\circ$.",
    },
    {
        "type": "TF", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [
            (r"Якщо $\vec a \cdot \vec b \gt 0$, то кут між векторами гострий або $0^\circ$", True),
            (r"Якщо $\vec a \cdot \vec b \lt 0$, то кут між векторами гострий", False),
            (r"$\vec a^{\,2} = |\vec a|^2$", True),
        ],
        "hint": r"Знак добутку — це знак $\cos\varphi$.",
        "solution": r"$\cos\varphi \gt 0$ — гострий кут або $0^\circ$; $\cos\varphi \lt 0$ — тупий або $180^\circ$. $\vec a \cdot \vec a = |\vec a|^2 \cos 0^\circ$.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Скалярний добуток векторів дорівнює $-6$. Яким є кут між ними?",
        "options": [(r"Тупим або $180^\circ$", True), ("Гострим", False), ("Прямим", False), (r"$0^\circ$", False)],
        "hint": r"Від'ємний добуток — від'ємний косинус.",
        "solution": r"$\cos\varphi \lt 0$, тож кут тупий або розгорнутий.",
    },

    # ==========================================
    # СХОДИНКА 2 — СЕРЕДНІЙ
    # ==========================================
    # --- Моделювання ---
    {
        "type": "SHORT", "difficulty": 2, "skill": "MODEL",
        "text": r"Санки тягнуть із силою $40$ Н під кутом $60^\circ$ до дороги. Яку роботу (у джоулях) виконає сила на шляху $5$ м?",
        "answer": "100",
        "hint": r"$A = F \cdot s \cdot \cos\varphi$.",
        "solution": r"$A = 40 \cdot 5 \cdot \frac{1}{2} = 100$ Дж.",
    },
    {
        "type": "FIELDS", "difficulty": 2, "skill": "MODEL",
        "text": r"$ABC$ — рівносторонній трикутник зі стороною $6$. Знайдіть:",
        "fields": [(r"$\overrightarrow{AB} \cdot \overrightarrow{AC} =$", "18"), (r"$\overrightarrow{AB}^{\,2} =$", "36")],
        "hint": r"Вектори виходять з точки $A$, кут між ними — кут трикутника.",
        "solution": r"$6 \cdot 6 \cdot \cos 60^\circ = 18$; $\;|\overrightarrow{AB}|^2 = 36$.",
    },
    {
        "type": "ORDER", "difficulty": 2, "skill": "MODEL",
        "text": r"Розташуйте кроки знаходження кута між векторами $\vec a(1;\,1)$ і $\vec b(0;\,3)$.",
        "items": [
            r"$\vec a \cdot \vec b = 1 \cdot 0 + 1 \cdot 3 = 3$",
            r"$|\vec a| = \sqrt{2}$, $\;|\vec b| = 3$",
            r"$\cos\varphi = \frac{3}{3\sqrt{2}} = \frac{\sqrt{2}}{2}$",
            r"$\varphi = 45^\circ$",
        ],
        "hint": r"Добуток → модулі → косинус → кут.",
        "solution": r"Кут між векторами — $45^\circ$.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "MODEL",
        "text": r"$ABCD$ — квадрат зі стороною $3$. Знайдіть $\overrightarrow{AB} \cdot \overrightarrow{AD}$.",
        "options": [(r"$0$", True), (r"$9$", False), (r"$3$", False), (r"$-9$", False)],
        "hint": r"Який кут між сторонами квадрата?",
        "solution": r"$AB \perp AD$, $\cos 90^\circ = 0$, тож добуток $0$.",
    },
    {
        "type": "GROUP", "difficulty": 2, "skill": "MODEL",
        "text": r"Яким є кут між векторами? Розподіліть пари.",
        "groups": ["Гострий", "Прямий", "Тупий"],
        "items": [(r"$(1;\,2)$ і $(3;\,1)$", 0), (r"$(2;\,-1)$ і $(1;\,2)$", 1), (r"$(-1;\,3)$ і $(2;\,1)$", 0),
                  (r"$(3;\,0)$ і $(-2;\,1)$", 2), (r"$(1;\,-1)$ і $(-2;\,1)$", 2), (r"$(2;\,2)$ і $(-1;\,1)$", 1)],
        "hint": r"Досить знака скалярного добутку (жодна пара не колінеарна).",
        "solution": r"Добутки: $5$, $0$, $1$, $-6$, $-3$, $0$. Додатний — гострий, нуль — прямий, від'ємний — тупий.",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"При якому $x$ вектори $\vec a(x;\,3)$ і $\vec b(6;\,-2)$ перпендикулярні?",
        "answer": "1",
        "hint": r"Прирівняйте скалярний добуток до нуля.",
        "solution": r"$6x - 6 = 0 \Rightarrow x = 1$.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "SOLVE",
        "text": r"Знайдіть кут між векторами $\vec a(1;\,0)$ і $\vec b(1;\,1)$.",
        "options": [(r"$45^\circ$", True), (r"$30^\circ$", False), (r"$60^\circ$", False), (r"$90^\circ$", False), (r"$0^\circ$", False)],
        "hint": r"$\cos\varphi = \frac{\vec a \cdot \vec b}{|\vec a|\,|\vec b|}$.",
        "solution": r"$\cos\varphi = \frac{1}{1 \cdot \sqrt{2}} = \frac{\sqrt{2}}{2}$, $\varphi = 45^\circ$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"$|\vec a| = 4$, $|\vec b| = 3$, $\vec a \cdot \vec b = 6$. Знайдіть кут між векторами (у градусах).",
        "answer": "60",
        "hint": r"Виразіть $\cos\varphi$ з формули скалярного добутку.",
        "solution": r"$\cos\varphi = \frac{6}{4 \cdot 3} = \frac{1}{2}$, $\varphi = 60^\circ$.",
    },
    {
        "type": "FIELDS", "difficulty": 2, "skill": "SOLVE",
        "text": r"Дано трикутник $A(1;\,2)$, $B(4;\,6)$, $C(5;\,-1)$.",
        "fields": [(r"$\overrightarrow{AB} \cdot \overrightarrow{AC} =$", "0"), (r"Кут $A$ (у градусах):", "90")],
        "hint": r"$\overrightarrow{AB}(3;\,4)$, $\overrightarrow{AC}(4;\,-3)$.",
        "solution": r"$3 \cdot 4 + 4 \cdot (-3) = 0$ — кут $A$ прямий.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Дано $\vec a(2;\,-1)$ і $\vec b(1;\,3)$. Знайдіть $(\vec a + \vec b) \cdot \vec a$.",
        "answer": "4",
        "hint": r"Спершу знайдіть координати $\vec a + \vec b$.",
        "solution": r"$\vec a + \vec b = (3;\,2)$; $\;3 \cdot 2 + 2 \cdot (-1) = 4$.",
    },
    # --- Аналіз результатів ---
    {
        "type": "ERROR", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Максим шукав кут між $\vec a(2;\,0)$ і $\vec b(1;\,\sqrt{3})$. У якому кроці помилка?",
        "steps": [r"$\vec a \cdot \vec b = 2 \cdot 1 + 0 \cdot \sqrt{3} = 2$", r"$|\vec a| = 2$, $\;|\vec b| = 1 + 3 = 4$", r"$\cos\varphi = \frac{2}{8} = \frac{1}{4}$"],
        "wrong": 1,
        "hint": r"Модуль — з коренем.",
        "solution": r"$|\vec b| = \sqrt{1 + 3} = 2$; $\cos\varphi = \frac{2}{4} = \frac{1}{2}$, $\varphi = 60^\circ$.",
    },
    {
        "type": "TF", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Вектор $\vec a(3;\,4)$. Правда чи ні?",
        "statements": [
            (r"$|\vec a| = 5$", True),
            (r"$\vec a^{\,2} = 7$", False),
            (r"$\vec a$ перпендикулярний до вектора $(4;\,-3)$", True),
        ],
        "hint": r"$\vec a^{\,2} = a_1^2 + a_2^2$.",
        "solution": r"$\sqrt{9 + 16} = 5$; $\vec a^{\,2} = 25$; $3 \cdot 4 + 4 \cdot (-3) = 0$ ✓.",
    },
    {
        "type": "MULTI", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Які вектори перпендикулярні до $\vec a(2;\,-3)$?",
        "options": [(r"$(3;\,2)$", True), (r"$(-3;\,-2)$", True), (r"$(6;\,4)$", True), (r"$(2;\,3)$", False), (r"$(-2;\,3)$", False)],
        "hint": r"Перевірте $2b_1 - 3b_2 = 0$.",
        "solution": r"$6 - 6 = 0$, $-6 + 6 = 0$, $12 - 12 = 0$. $(2;\,3)$: $4 - 9 = -5$. $(-2;\,3)$ — колінеарний $\vec a$.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "ANALYZE",
        "text": r"$ABC$ — рівносторонній трикутник зі стороною $2$. Знайдіть $\overrightarrow{AB} \cdot \overrightarrow{BC}$.",
        "options": [(r"$-2$", True), (r"$2$", False), (r"$0$", False), (r"$-4$", False), (r"$4$", False)],
        "hint": r"Чи виходять вектори з однієї точки? Замініть $\overrightarrow{AB} = -\overrightarrow{BA}$.",
        "solution": r"$\overrightarrow{AB} \cdot \overrightarrow{BC} = -\overrightarrow{BA} \cdot \overrightarrow{BC} = -2 \cdot 2 \cdot \frac{1}{2} = -2$. Кут між $\overrightarrow{AB}$ і $\overrightarrow{BC}$ — $120^\circ$, а не $60^\circ$.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Ярина вважає, що кут $B$ трикутника $ABC$ — це кут між векторами $\overrightarrow{AB}$ і $\overrightarrow{BC}$. Між якими векторами він насправді?",
        "options": [(r"$\overrightarrow{BA}$ і $\overrightarrow{BC}$", True), (r"$\overrightarrow{AB}$ і $\overrightarrow{BC}$", False), (r"$\overrightarrow{AB}$ і $\overrightarrow{AC}$", False), (r"$\overrightarrow{BC}$ і $\overrightarrow{CA}$", False)],
        "hint": r"Вектори мають виходити з вершини кута.",
        "solution": r"Кут $B$ — між векторами з початком у $B$: $\overrightarrow{BA}$ і $\overrightarrow{BC}$. Між $\overrightarrow{AB}$ і $\overrightarrow{BC}$ — $180^\circ - \angle B$.",
    },

    # ==========================================
    # СХОДИНКА 3 — СКЛАДНИЙ
    # ==========================================
    # --- Моделювання ---
    {
        "type": "FIELDS", "difficulty": 3, "skill": "MODEL",
        "text": r"$ABCD$ — квадрат зі стороною $4$. Знайдіть:",
        "fields": [(r"$\overrightarrow{AC} \cdot \overrightarrow{AB} =$", "16"), (r"$\overrightarrow{AC} \cdot \overrightarrow{BD} =$", "0"), (r"$\overrightarrow{AB} \cdot \overrightarrow{CD} =$", "-16")],
        "hint": r"Зручно ввести координати: $A(0;\,0)$, $B(4;\,0)$, $C(4;\,4)$, $D(0;\,4)$.",
        "solution": r"$\overrightarrow{AC}(4;\,4)$, $\overrightarrow{AB}(4;\,0)$: $16$. Діагоналі квадрата перпендикулярні: $0$. $\overrightarrow{AB}$ і $\overrightarrow{CD}$ протилежно напрямлені: $4 \cdot 4 \cdot (-1) = -16$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"Прямокутник $ABCD$: $A(0;\,0)$, $B(6;\,0)$, $D(0;\,4)$. Знайдіть $\overrightarrow{AC} \cdot \overrightarrow{BD}$.",
        "answer": "-20",
        "hint": r"$C(6;\,4)$.",
        "solution": r"$\overrightarrow{AC}(6;\,4)$, $\overrightarrow{BD}(-6;\,4)$: $-36 + 16 = -20$. Добуток від'ємний — кут між цими векторами тупий.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "MODEL",
        "text": r"Сила $\vec F(3;\,4)$ (у ньютонах) переміщує тіло з точки $A(1;\,1)$ у точку $B(5;\,2)$ (координати — у метрах). Яку роботу виконує сила?",
        "options": [(r"$16$ Дж", True), (r"$(12;\,4)$ Дж", False), (r"$25$ Дж", False), (r"$20$ Дж", False), (r"$8$ Дж", False)],
        "hint": r"Робота — скалярний добуток $\vec F$ і переміщення $\overrightarrow{AB}$.",
        "solution": r"$\overrightarrow{AB}(4;\,1)$; $A = 3 \cdot 4 + 4 \cdot 1 = 16$ Дж.",
    },
    {
        "type": "MATCH", "difficulty": 3, "skill": "MODEL",
        "text": r"Установіть відповідність між парою векторів (1–3) та кутом між ними (А–Д).",
        "options": [r"А) $0^\circ$", r"Б) $30^\circ$", r"В) $45^\circ$", r"Г) $60^\circ$", r"Д) $90^\circ$"],
        "matches": [(r"1. $(1;\,0)$ і $(0;\,5)$", r"Д) $90^\circ$"), (r"2. $(2;\,2)$ і $(3;\,0)$", r"В) $45^\circ$"),
                    (r"3. $(1;\,\sqrt{3})$ і $(2;\,0)$", r"Г) $60^\circ$")],
        "hint": r"Знайдіть косинус кута для кожної пари.",
        "solution": r"1) Добуток $0$. 2) $\cos\varphi = \frac{6}{2\sqrt{2} \cdot 3} = \frac{\sqrt{2}}{2}$. 3) $\cos\varphi = \frac{2}{2 \cdot 2} = \frac{1}{2}$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"Трикутник $A(0;\,0)$, $B(3;\,0)$, $C(0;\,4)$. Знайдіть косинус кута $B$.",
        "answer": "0.6",
        "hint": r"Кут $B$ — між $\overrightarrow{BA}$ і $\overrightarrow{BC}$.",
        "solution": r"$\overrightarrow{BA}(-3;\,0)$, $\overrightarrow{BC}(-3;\,4)$: $\cos B = \frac{9}{3 \cdot 5} = 0{,}6$.",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"$|\vec a| = 2$, $|\vec b| = 3$, кут між ними $60^\circ$. Знайдіть $(\vec a + \vec b)^2$.",
        "answer": "19",
        "hint": r"$(\vec a + \vec b)^2 = \vec a^{\,2} + 2\,\vec a \cdot \vec b + \vec b^{\,2}$.",
        "solution": r"$\vec a \cdot \vec b = 2 \cdot 3 \cdot \frac{1}{2} = 3$; $\;4 + 6 + 9 = 19$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"При якому додатному $x$ вектори $\vec a(x;\,2)$ і $\vec b(x;\,-8)$ перпендикулярні?",
        "answer": "4",
        "hint": r"$x^2 - 16 = 0$.",
        "solution": r"$x \cdot x + 2 \cdot (-8) = 0$, $x^2 = 16$; додатний корінь $x = 4$.",
    },
    {
        "type": "FIELDS", "difficulty": 3, "skill": "SOLVE",
        "text": r"Трикутник $A(0;\,0)$, $B(4;\,0)$, $C(2;\,2)$. Знайдіть кути (у градусах).",
        "fields": [(r"$\angle A =$", "45"), (r"$\angle C =$", "90")],
        "hint": r"Кут $A$ — між $\overrightarrow{AB}$ і $\overrightarrow{AC}$; кут $C$ — між $\overrightarrow{CA}$ і $\overrightarrow{CB}$.",
        "solution": r"$\cos A = \frac{8}{4 \cdot 2\sqrt{2}} = \frac{\sqrt{2}}{2}$: $45^\circ$. $\overrightarrow{CA}(-2;\,-2)$, $\overrightarrow{CB}(2;\,-2)$: $-4 + 4 = 0$ — $90^\circ$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Дано $\vec a(1;\,2)$ і $\vec b(3;\,-1)$. Знайдіть $\vec a \cdot (\vec a + 2\vec b)$.",
        "answer": "7",
        "hint": r"$\vec a + 2\vec b = (7;\,0)$.",
        "solution": r"$1 \cdot 7 + 2 \cdot 0 = 7$.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "SOLVE",
        "text": r"Знайдіть кут між векторами $\vec a(\sqrt{3};\,1)$ і $\vec b(0;\,2)$.",
        "options": [(r"$60^\circ$", True), (r"$30^\circ$", False), (r"$45^\circ$", False), (r"$90^\circ$", False), (r"$120^\circ$", False)],
        "hint": r"$|\vec a| = \sqrt{3 + 1}$.",
        "solution": r"$\vec a \cdot \vec b = 2$, $|\vec a| = |\vec b| = 2$: $\cos\varphi = \frac{1}{2}$, $\varphi = 60^\circ$. $30^\circ$ — сплутали з синусом.",
    },
    # --- Аналіз результатів ---
    {
        "type": "ERROR", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Сашко шукав $\overrightarrow{AB} \cdot \overrightarrow{BC}$ для рівностороннього трикутника зі стороною $4$. У якому кроці помилка?",
        "steps": [r"$|\overrightarrow{AB}| = |\overrightarrow{BC}| = 4$", r"Кут між $\overrightarrow{AB}$ і $\overrightarrow{BC}$ дорівнює $60^\circ$", r"$\overrightarrow{AB} \cdot \overrightarrow{BC} = 4 \cdot 4 \cdot \frac{1}{2} = 8$"],
        "wrong": 1,
        "hint": r"Чи виходять ці вектори з однієї точки?",
        "solution": r"Кут між ними $120^\circ$. Правильно: $-\overrightarrow{BA} \cdot \overrightarrow{BC} = -8$.",
    },
    {
        "type": "TF", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [
            (r"Якщо $\vec a \cdot \vec b = \vec a \cdot \vec c$ і $\vec a \ne \vec 0$, то $\vec b = \vec c$", False),
            (r"$\vec a \cdot \vec b = \vec b \cdot \vec a$", True),
            (r"$(2\vec a) \cdot \vec b = 2(\vec a \cdot \vec b)$", True),
            (r"$|\vec a \cdot \vec b| \le |\vec a| \cdot |\vec b|$", True),
        ],
        "hint": r"Спробуйте $\vec a(1;\,0)$, $\vec b(0;\,1)$, $\vec c(0;\,2)$.",
        "solution": r"У прикладі $\vec a \cdot \vec b = \vec a \cdot \vec c = 0$, але $\vec b \ne \vec c$. Решта — з формули в координатах і $|\cos\varphi| \le 1$.",
    },
    {
        "type": "MULTI", "difficulty": 3, "skill": "ANALYZE",
        "text": r"При яких $x$ кут між векторами $\vec a(x;\,1)$ і $\vec b(2;\,-4)$ тупий?",
        "options": [(r"$x = 0$", True), (r"$x = 1$", True), (r"$x = 2$", False), (r"$x = -0{,}5$", False), (r"$x = 3$", False), (r"$x = -3$", True)],
        "hint": r"Добуток від'ємний, але вектори не протилежно напрямлені.",
        "solution": r"$2x - 4 \lt 0 \Rightarrow x \lt 2$. При $x = -0{,}5$: $\vec a = -\frac{1}{4}\vec b$ — кут $180^\circ$, а не тупий. Підходять $0$, $1$, $-3$.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "ANALYZE",
        "text": r"$|\vec a| = 3$, $|\vec b| = 5$. Яке найбільше значення може мати $\vec a \cdot \vec b$?",
        "options": [(r"$15$", True), (r"$8$", False), (r"$0$", False), (r"$30$", False), (r"$34$", False)],
        "hint": r"Найбільше значення $\cos\varphi$.",
        "solution": r"$\vec a \cdot \vec b = 15\cos\varphi \le 15$; рівність — для співнапрямлених векторів.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Знайдіть найменше ціле $y$, при якому кут між векторами $\vec a(3;\,y)$ і $\vec b(1;\,2)$ гострий.",
        "answer": "-1",
        "hint": r"$3 + 2y \gt 0$, і вектори не співнапрямлені.",
        "solution": r"$y \gt -1{,}5$; найменше ціле $-1$: $\vec a(3;\,-1)$, $3 - 2 = 1 \gt 0$, вектори не колінеарні ✓.",
    },

    # ==========================================
    # БОСИ — після опанування теми
    # ==========================================
    {
        "type": "SHORT", "difficulty": 4, "skill": "MODEL",
        "text": r"$ABCD$ — ромб зі стороною $6$ і кутом $A = 60^\circ$. Знайдіть $\overrightarrow{AC} \cdot \overrightarrow{AB}$.",
        "answer": "54",
        "solution": r"$\overrightarrow{AC} = \overrightarrow{AB} + \overrightarrow{AD}$, тож $\overrightarrow{AC} \cdot \overrightarrow{AB} = \overrightarrow{AB}^{\,2} + \overrightarrow{AD} \cdot \overrightarrow{AB} = 36 + 6 \cdot 6 \cdot \frac{1}{2} = 54$.",
    },
    {
        "type": "FIELDS", "difficulty": 4, "skill": "MODEL",
        "text": r"Дано точки $A(1;\,3)$ і $B(5;\,1)$. Знайдіть абсциси точок $C$ на осі $Ox$, для яких $\angle ACB = 90^\circ$.",
        "fields": [(r"$x_1 =$", "2"), (r"$x_2 =$", "4")],
        "unordered": True,
        "solution": r"$C(x;\,0)$: $\overrightarrow{CA}(1 - x;\,3)$, $\overrightarrow{CB}(5 - x;\,1)$. $(1 - x)(5 - x) + 3 = 0 \Rightarrow x^2 - 6x + 8 = 0$, $x = 2$ або $x = 4$.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "SOLVE",
        "text": r"$|\vec a| = 2$, $|\vec b| = 3$, $|\vec a - \vec b| = \sqrt{7}$. Знайдіть кут між векторами $\vec a$ і $\vec b$ (у градусах).",
        "answer": "60",
        "solution": r"$(\vec a - \vec b)^2 = 4 - 2\,\vec a \cdot \vec b + 9 = 7 \Rightarrow \vec a \cdot \vec b = 3$. $\cos\varphi = \frac{3}{2 \cdot 3} = \frac{1}{2}$, $\varphi = 60^\circ$.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "SOLVE",
        "text": r"Дано $\vec a(1;\,2)$ і $\vec b(-3;\,1)$. При якому $k$ вектор $\vec a + k\vec b$ перпендикулярний до $\vec a$?",
        "answer": "5",
        "solution": r"$(\vec a + k\vec b) \cdot \vec a = \vec a^{\,2} + k\,\vec a \cdot \vec b = 5 + k(-3 + 2) = 5 - k = 0 \Rightarrow k = 5$. Перевірка: $(-14;\,7) \cdot (1;\,2) = 0$ ✓.",
    },
    {
        "type": "TF", "difficulty": 4, "skill": "ANALYZE",
        "text": r"Трикутник $A(0;\,0)$, $B(4;\,0)$, $C(1;\,3)$. Правда чи ні?",
        "statements": [
            (r"Кут $A$ гострий", True),
            (r"Кут $B$ гострий", True),
            (r"Кут $C$ тупий", False),
            ("Трикутник гострокутний", True),
        ],
        "solution": r"$\overrightarrow{AB} \cdot \overrightarrow{AC} = 4 \gt 0$; $\overrightarrow{BA}(-4;\,0) \cdot \overrightarrow{BC}(-3;\,3) = 12 \gt 0$; $\overrightarrow{CA}(-1;\,-3) \cdot \overrightarrow{CB}(3;\,-3) = 6 \gt 0$. Усі кути гострі.",
    },

    # ==========================================
    # УЛЬТРА-БОСИ
    # ==========================================
    {
        "type": "SHORT", "difficulty": 5, "skill": "SOLVE",
        "text": r"$|\vec a| = |\vec b| = 1$, кут між векторами $60^\circ$. Знайдіть $|2\vec a - 3\vec b|^2$.",
        "answer": "7",
        "solution": r"$|2\vec a - 3\vec b|^2 = 4\vec a^{\,2} - 12\,\vec a \cdot \vec b + 9\vec b^{\,2} = 4 - 12 \cdot \frac{1}{2} + 9 = 7$.",
    },
    {
        "type": "SHORT", "difficulty": 5, "skill": "SOLVE",
        "text": r"$ABCD$ — квадрат зі стороною $2$, точка $P$ лежить на стороні $CD$. Знайдіть найменше значення $\overrightarrow{PA} \cdot \overrightarrow{PB}$.",
        "answer": "3",
        "solution": r"$A(0;\,0)$, $B(2;\,0)$, $P(t;\,2)$, $0 \le t \le 2$. $\overrightarrow{PA}(-t;\,-2)$, $\overrightarrow{PB}(2 - t;\,-2)$: добуток $t^2 - 2t + 4 = (t - 1)^2 + 3 \ge 3$, рівність при $t = 1$ (середина $CD$).",
    },
]
