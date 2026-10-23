TOPIC_NAME = "2.1. Вектор. Модуль і напрям вектора"
COURSE = "Геометрія (7-9 класи)"
GRADE = "9 клас"

TASKS = [
    # ==========================================
    # СХОДИНКА 1 — БАЗОВИЙ
    # ==========================================
    # --- Моделювання ---
    {
        "type": "GROUP", "difficulty": 1, "skill": "MODEL",
        "text": r"Розподіліть величини: скалярні чи векторні?",
        "groups": ["скалярні", "векторні"],
        "items": [("маса", 0), ("швидкість", 1), ("час", 0), ("сила", 1), ("площа", 0), ("переміщення", 1)],
        "solution": r"Векторна величина має напрям: швидкість, сила, переміщення. Маса, час, площа задаються одним числом.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "MODEL",
        "text": r"У вектора $\overrightarrow{KM}$ початок — точка …",
        "options": [(r"$K$", True), (r"$M$", False), ("середина відрізка $KM$", False), ("у вектора немає початку", False)],
        "solution": r"У записі $\overrightarrow{KM}$ першою пишуть початок, другою — кінець.",
    },
    {
        "type": "TF", "difficulty": 1, "skill": "MODEL",
        "text": r"Правда чи ні?",
        "statements": [(r"Модуль вектора $\overrightarrow{AB}$ дорівнює довжині відрізка $AB$", True),
                       (r"Вектори $\overrightarrow{AB}$ і $\overrightarrow{BA}$ рівні", False),
                       (r"Модуль нульового вектора дорівнює $0$", True)],
        "solution": r"$|\overrightarrow{AB}| = AB$. $\overrightarrow{AB}$ і $\overrightarrow{BA}$ протилежно напрямлені, тому не рівні. У нульового вектора початок і кінець збігаються.",
    },
    {
        "type": "COORD", "difficulty": 1, "skill": "MODEL",
        "text": r"Від точки $O(0;\,0)$ відклали вектор $\vec a(3;\,-2)$. Позначте його кінець.",
        "xmin": -5, "xmax": 5, "ymin": -5, "ymax": 5, "step": 1, "answer": [3, -2],
        "solution": r"Кінець = початок + координати вектора: $(0 + 3;\,0 - 2) = (3;\,-2)$.",
    },
    {
        "type": "MATCH", "difficulty": 1, "skill": "MODEL",
        "text": r"$ABCD$ — квадрат. Установіть відповідність між парою векторів (1–3) та їхнім взаємним розміщенням (А–Г).",
        "options": ["А) рівні", "Б) протилежно напрямлені", "В) неколінеарні", "Г) співнапрямлені, але не рівні"],
        "matches": [(r"1. $\overrightarrow{AB}$ і $\overrightarrow{DC}$", "А) рівні"),
                    (r"2. $\overrightarrow{AB}$ і $\overrightarrow{CD}$", "Б) протилежно напрямлені"),
                    (r"3. $\overrightarrow{AB}$ і $\overrightarrow{AD}$", "В) неколінеарні")],
        "solution": r"$AB \parallel DC$, напрям від $A$ до $B$ такий самий, як від $D$ до $C$ — рівні. $\overrightarrow{CD}$ напрямлений навпаки. $AB \perp AD$ — неколінеарні.",
    },
    # --- Розв'язування ---
    {
        "type": "FIELDS", "difficulty": 1, "skill": "SOLVE",
        "text": r"$A(2;\,1)$, $B(5;\,7)$. Знайдіть координати вектора $\overrightarrow{AB}$.",
        "fields": [(r"$x =$", "3"), (r"$y =$", "6")],
        "solution": r"Кінець мінус початок: $(5 - 2;\,7 - 1) = (3;\,6)$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"Знайдіть модуль вектора $\vec a(6;\,8)$.",
        "answer": "10",
        "solution": r"$|\vec a| = \sqrt{6^2 + 8^2} = \sqrt{100} = 10$.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "SOLVE",
        "text": r"$M(-1;\,4)$, $N(3;\,1)$. Знайдіть координати вектора $\overrightarrow{NM}$.",
        "options": [(r"$(-4;\,3)$", True), (r"$(4;\,-3)$", False), (r"$(2;\,5)$", False), (r"$(-4;\,-3)$", False)],
        "solution": r"Початок $N$, кінець $M$: $(-1 - 3;\,4 - 1) = (-4;\,3)$. Варіант $(4;\,-3)$ — це $\overrightarrow{MN}$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"Знайдіть модуль вектора $\vec b(-5;\,0)$.",
        "answer": "5",
        "solution": r"$\sqrt{(-5)^2 + 0^2} = 5$. Модуль не буває від'ємним.",
    },
    {
        "type": "MULTI", "difficulty": 1, "skill": "SOLVE",
        "text": r"Які з векторів мають модуль $5$?",
        "options": [(r"$(3;\,4)$", True), (r"$(-4;\,-3)$", True), (r"$(0;\,5)$", True), (r"$(2;\,3)$", False), (r"$(1;\,4)$", False)],
        "solution": r"$\sqrt{9 + 16} = 5$, $\sqrt{16 + 9} = 5$, $\sqrt{0 + 25} = 5$. $\sqrt{4 + 9} = \sqrt{13}$, $\sqrt{1 + 16} = \sqrt{17}$.",
    },
    # --- Аналіз результатів ---
    {
        "type": "ERROR", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Учень шукав координати вектора $\overrightarrow{AB}$, $A(4;\,-1)$, $B(1;\,3)$. У якому кроці помилка?",
        "steps": [r"Початок вектора — $A$, кінець — $B$", r"$\overrightarrow{AB}(4 - 1;\,-1 - 3)$", r"$\overrightarrow{AB}(3;\,-4)$"],
        "wrong": 1,
        "solution": r"Від координат кінця віднімають координати початку: $(1 - 4;\,3 - (-1)) = (-3;\,4)$.",
    },
    {
        "type": "TF", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [(r"Якщо $|\vec a| = |\vec b|$, то $\vec a = \vec b$", False),
                       (r"Якщо $\vec a = \vec b$, то $|\vec a| = |\vec b|$", True),
                       (r"Рівні вектори мають рівні координати", True)],
        "solution": r"Вектори $(3;\,4)$ і $(4;\,3)$ мають модуль $5$, але не рівні. Рівні вектори мають рівні модулі й рівні координати.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Учень: «$|\vec a(3;\,-4)| = 3 - 4 = -1$». Яка правильна відповідь?",
        "options": [(r"$5$", True), (r"$1$", False), (r"$7$", False), (r"$25$", False)],
        "solution": r"$|\vec a| = \sqrt{3^2 + (-4)^2} = \sqrt{25} = 5$. Модуль — довжина, від'ємним бути не може.",
    },
    {
        "type": "GROUP", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Порівняйте з вектором $\vec a(2;\,-1)$. Розподіліть вектори.",
        "groups": [r"дорівнює $\vec a$", r"не дорівнює $\vec a$"],
        "items": [(r"$\overrightarrow{AB}$, $A(0;\,0)$, $B(2;\,-1)$", 0), (r"$\overrightarrow{CD}$, $C(1;\,3)$, $D(3;\,2)$", 0),
                  (r"$(-2;\,1)$", 1), (r"$(1;\,-2)$", 1), (r"$\overrightarrow{KL}$, $K(5;\,5)$, $L(3;\,6)$", 1)],
        "solution": r"$\overrightarrow{AB}(2;\,-1)$, $\overrightarrow{CD}(2;\,-1)$ — рівні $\vec a$. $(-2;\,1)$ — протилежний; $(1;\,-2)$ — інший; $\overrightarrow{KL}(-2;\,1)$ — протилежний.",
    },
    {
        "type": "MULTI", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Які твердження про нульовий вектор правильні?",
        "options": [("Його початок і кінець збігаються", True), (r"Його модуль дорівнює $0$", True),
                    ("Він колінеарний будь-якому вектору", True), (r"Його координати $(1;\,1)$", False), ("Він має напрям уздовж осі $Ox$", False)],
        "solution": r"$\vec 0 = \overrightarrow{AA}$, координати $(0;\,0)$, модуль $0$, конкретного напряму не має; за домовленістю колінеарний будь-якому вектору.",
    },

    # ==========================================
    # СХОДИНКА 2 — СЕРЕДНІЙ
    # ==========================================
    # --- Моделювання ---
    {
        "type": "COORD", "difficulty": 2, "skill": "MODEL",
        "text": r"Від точки $M(-2;\,3)$ відклали вектор $\vec a(4;\,-5)$. Позначте кінець вектора.",
        "xmin": -5, "xmax": 5, "ymin": -5, "ymax": 5, "step": 1, "answer": [2, -2],
        "solution": r"$(-2 + 4;\,3 - 5) = (2;\,-2)$.",
    },
    {
        "type": "MATCH", "difficulty": 2, "skill": "MODEL",
        "text": r"$ABCDEF$ — правильний шестикутник, $O$ — його центр. Установіть відповідність між вектором (1–3) та рівним йому вектором (А–Д).",
        "options": [r"А) $\overrightarrow{OC}$", r"Б) $\overrightarrow{FE}$", r"В) $\overrightarrow{DC}$", r"Г) $\overrightarrow{OA}$", r"Д) $\overrightarrow{CB}$"],
        "matches": [(r"1. $\overrightarrow{AB}$", r"А) $\overrightarrow{OC}$"),
                    (r"2. $\overrightarrow{OD}$", r"Б) $\overrightarrow{FE}$"),
                    (r"3. $\overrightarrow{EO}$", r"В) $\overrightarrow{DC}$")],
        "solution": r"Шестикутник складається з шести правильних трикутників. $ABCO$ — ромб: $\overrightarrow{AB} = \overrightarrow{OC}$. $OFED$ — ромб: $\overrightarrow{OD} = \overrightarrow{FE}$. $DEOC$ — ромб: $\overrightarrow{EO} = \overrightarrow{DC}$. $\overrightarrow{OA}$ і $\overrightarrow{CB}$ рівні між собою, але жодному з даних векторів.",
    },
    {
        "type": "TF", "difficulty": 2, "skill": "MODEL",
        "text": r"$ABCD$ — паралелограм, $O$ — точка перетину діагоналей. Правда чи ні?",
        "statements": [(r"$\overrightarrow{AO} = \overrightarrow{OC}$", True),
                       (r"$\overrightarrow{BO} = \overrightarrow{OD}$", True),
                       (r"$\overrightarrow{AD} = \overrightarrow{CB}$", False),
                       (r"$|\overrightarrow{AC}| = |\overrightarrow{BD}|$ для будь-якого паралелограма", False)],
        "solution": r"Діагоналі паралелограма діляться навпіл, тож $\overrightarrow{AO} = \overrightarrow{OC}$, $\overrightarrow{BO} = \overrightarrow{OD}$. $\overrightarrow{AD} = \overrightarrow{BC}$, а $\overrightarrow{CB}$ — протилежний. Діагоналі рівні лише в прямокутника.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "MODEL",
        "text": r"$ABCD$ — паралелограм, $A(1;\,1)$, $B(4;\,2)$, $C(6;\,5)$. Знайдіть координати вершини $D$.",
        "options": [(r"$(3;\,4)$", True), (r"$(9;\,6)$", False), (r"$(-1;\,-2)$", False), (r"$(5;\,4)$", False)],
        "solution": r"$\overrightarrow{AD} = \overrightarrow{BC} = (2;\,3)$. $D = (1 + 2;\,1 + 3) = (3;\,4)$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "MODEL",
        "text": r"Сторона ромба $ABCD$ дорівнює $7$. Знайдіть модуль вектора $\overrightarrow{DC}$.",
        "answer": "7",
        "solution": r"$|\overrightarrow{DC}| = DC = 7$ — модуль вектора дорівнює довжині відрізка.",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"$A(-1;\,4)$, $B(5;\,-4)$. Знайдіть $|\overrightarrow{AB}|$.",
        "answer": "10",
        "solution": r"$\overrightarrow{AB}(6;\,-8)$, $|\overrightarrow{AB}| = \sqrt{36 + 64} = 10$.",
    },
    {
        "type": "FIELDS", "difficulty": 2, "skill": "SOLVE",
        "text": r"Вектор $\overrightarrow{AB}(-3;\,5)$, $B(2;\,1)$. Знайдіть координати точки $A$.",
        "fields": [(r"$x_A =$", "5"), (r"$y_A =$", "-4")],
        "solution": r"$2 - x_A = -3 \Rightarrow x_A = 5$; $\;1 - y_A = 5 \Rightarrow y_A = -4$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Знайдіть додатне значення $x$, при якому $|\vec a(x;\,12)| = 13$.",
        "answer": "5",
        "solution": r"$x^2 + 144 = 169 \Rightarrow x^2 = 25$, $x = \pm 5$. Додатне — $5$.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "SOLVE",
        "text": r"При яких $m$ і $n$ вектори $\vec a(m;\,3)$ і $\vec b(-2;\,n - 1)$ рівні?",
        "options": [(r"$m = -2$, $n = 4$", True), (r"$m = -2$, $n = 2$", False), (r"$m = 2$, $n = 4$", False), (r"$m = 3$, $n = -2$", False)],
        "solution": r"Рівні вектори мають рівні координати: $m = -2$, $n - 1 = 3 \Rightarrow n = 4$.",
    },
    {
        "type": "ORDER", "difficulty": 2, "skill": "SOLVE",
        "text": r"Розташуйте вектори в порядку зростання модулів.",
        "items": [r"$(1;\,-1)$", r"$(0;\,2)$", r"$(2;\,-2)$", r"$(-3;\,0)$", r"$(3;\,4)$"],
        "solution": r"Модулі: $\sqrt2 \approx 1{,}41$; $2$; $\sqrt8 \approx 2{,}83$; $3$; $5$.",
    },
    # --- Аналіз результатів ---
    {
        "type": "ERROR", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Учень шукав вершину $D$ паралелограма $ABCD$: $A(0;\,0)$, $B(3;\,1)$, $C(5;\,4)$. У якому кроці помилка?",
        "steps": [r"У паралелограмі $\overrightarrow{AD} = \overrightarrow{BC}$", r"$\overrightarrow{BC}(2;\,3)$", r"$D = A - \overrightarrow{BC} = (-2;\,-3)$"],
        "wrong": 2,
        "solution": r"Кінець = початок + вектор: $D = (0 + 2;\,0 + 3) = (2;\,3)$.",
    },
    {
        "type": "TF", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [(r"Якщо $\overrightarrow{AB} = \overrightarrow{CD}$, то $\overrightarrow{AC} = \overrightarrow{BD}$", True),
                       (r"Якщо $\overrightarrow{AB} = \overrightarrow{DC}$ і точки не лежать на одній прямій, то $ABCD$ — паралелограм", True),
                       (r"Протилежно напрямлені вектори завжди мають різні модулі", False)],
        "solution": r"$\overrightarrow{AB} = \overrightarrow{CD}$ означає $B - A = D - C$, тоді $C - A = D - B$. Друге — ознака паралелограма. $\overrightarrow{AB}$ і $\overrightarrow{BA}$ протилежно напрямлені й мають рівні модулі.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Які вектори співнапрямлені з вектором $\vec a(2;\,-3)$?",
        "options": [(r"$(4;\,-6)$", True), (r"$(-4;\,6)$", False), (r"$(3;\,-2)$", False), (r"$(2;\,3)$", False)],
        "solution": r"$(4;\,-6) = 2\,(2;\,-3)$ — той самий напрям. $(-4;\,6)$ — протилежний; інші неколінеарні.",
    },
    {
        "type": "MULTI", "difficulty": 2, "skill": "ANALYZE",
        "text": r"$A(1;\,2)$, $B(3;\,6)$, $C(-1;\,0)$, $D(1;\,4)$. Які твердження правильні?",
        "options": [(r"$\overrightarrow{AB} = \overrightarrow{CD}$", True), (r"$|\overrightarrow{AB}| = 2\sqrt5$", True),
                    (r"$\overrightarrow{AB} = \overrightarrow{DC}$", False), (r"$\overrightarrow{AC} = \overrightarrow{BD}$", True), (r"$|\overrightarrow{AC}| = 4$", False)],
        "solution": r"$\overrightarrow{AB}(2;\,4)$, $\overrightarrow{CD}(2;\,4)$ — рівні; $\overrightarrow{DC}(-2;\,-4)$. $|\overrightarrow{AB}| = \sqrt{20} = 2\sqrt5$. $\overrightarrow{AC}(-2;\,-2)$, $\overrightarrow{BD}(-2;\,-2)$. $|\overrightarrow{AC}| = 2\sqrt2$.",
    },
    {
        "type": "GROUP", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Розподіліть вектори відносно вектора $\vec a(1;\,2)$.",
        "groups": [r"співнапрямлені з $\vec a$", r"протилежно напрямлені", "неколінеарні"],
        "items": [(r"$(3;\,6)$", 0), (r"$(0{,}5;\,1)$", 0), (r"$(-2;\,-4)$", 1), (r"$(-1;\,-2)$", 1), (r"$(2;\,1)$", 2), (r"$(-1;\,2)$", 2)],
        "solution": r"Колінеарні — координати пропорційні: $(3;\,6) = 3\vec a$, $(0{,}5;\,1) = 0{,}5\vec a$ (додатний множник — співнапрямлені); $(-2;\,-4) = -2\vec a$, $(-1;\,-2) = -\vec a$ (від'ємний — протилежні). $(2;\,1)$, $(-1;\,2)$ — не пропорційні.",
    },

    # ==========================================
    # СХОДИНКА 3 — ПІДВИЩЕНИЙ
    # ==========================================
    # --- Моделювання ---
    {
        "type": "COORD", "difficulty": 3, "skill": "MODEL",
        "text": r"$ABCD$ — паралелограм, $A(-3;\,-1)$, $B(1;\,-2)$, $D(-2;\,3)$. Позначте вершину $C$.",
        "xmin": -5, "xmax": 5, "ymin": -5, "ymax": 5, "step": 1, "answer": [2, 2],
        "solution": r"$\overrightarrow{DC} = \overrightarrow{AB} = (4;\,-1)$. $C = (-2 + 4;\,3 - 1) = (2;\,2)$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"$ABCD$ — прямокутник, $AB = 6$, $BC = 8$, $O$ — точка перетину діагоналей. Знайдіть $|\overrightarrow{AO}|$.",
        "answer": "5",
        "solution": r"$AC = \sqrt{36 + 64} = 10$, діагоналі діляться навпіл: $|\overrightarrow{AO}| = 5$.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "MODEL",
        "text": r"Точки $A(1;\,1)$, $B(4;\,5)$, $C(8;\,2)$. Знайдіть точку $D$ таку, що $ABCD$ — паралелограм.",
        "options": [(r"$(5;\,-2)$", True), (r"$(11;\,6)$", False), (r"$(-3;\,4)$", False), (r"$(7;\,-2)$", False), (r"$(5;\,2)$", False)],
        "solution": r"$\overrightarrow{AD} = \overrightarrow{BC} = (4;\,-3)$, $D = (1 + 4;\,1 - 3) = (5;\,-2)$. $(11;\,6)$ — це четверта вершина паралелограма $ABDC$, а не $ABCD$.",
    },
    {
        "type": "TF", "difficulty": 3, "skill": "MODEL",
        "text": r"$ABC$ — рівносторонній трикутник зі стороною $4$, $M$ — середина $BC$. Правда чи ні?",
        "statements": [(r"$|\overrightarrow{AM}| = 2\sqrt3$", True),
                       (r"$\overrightarrow{BM} = \overrightarrow{MC}$", True),
                       (r"$|\overrightarrow{AB}| = |\overrightarrow{BC}|$, отже $\overrightarrow{AB} = \overrightarrow{BC}$", False),
                       (r"$\overrightarrow{MB}$ і $\overrightarrow{CB}$ співнапрямлені", True)],
        "solution": r"Медіана рівностороннього трикутника $\frac{4\sqrt3}{2} = 2\sqrt3$. $M$ — середина, тому $\overrightarrow{BM} = \overrightarrow{MC}$. $\overrightarrow{AB}$ і $\overrightarrow{BC}$ неколінеарні. $\overrightarrow{MB}$ і $\overrightarrow{CB}$ напрямлені до $B$ — співнапрямлені.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"Від точки $A(2;\,-1)$ відклали вектор $\overrightarrow{AB}$, рівний вектору $\overrightarrow{CD}$, де $C(-3;\,0)$, $D(1;\,3)$. Знайдіть суму координат точки $B$.",
        "answer": "8",
        "solution": r"$\overrightarrow{CD}(4;\,3)$, $B(2 + 4;\,-1 + 3) = (6;\,2)$. Сума $6 + 2 = 8$.",
    },
    # --- Розв'язування ---
    {
        "type": "FIELDS", "difficulty": 3, "skill": "SOLVE",
        "text": r"$|\vec a(x;\,-4)| = 5$. Знайдіть обидва значення $x$.",
        "fields": [(r"$x_1 =$", "3"), (r"$x_2 =$", "-3")],
        "solution": r"$x^2 + 16 = 25$, $x^2 = 9$, $x = \pm 3$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Вектор $\vec a(k - 1;\,k + 1)$ має модуль $\sqrt{20}$, $k \gt 0$. Знайдіть $k$.",
        "answer": "3",
        "solution": r"$(k - 1)^2 + (k + 1)^2 = 20 \Rightarrow 2k^2 + 2 = 20 \Rightarrow k^2 = 9$, $k = 3$.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "SOLVE",
        "text": r"Знайдіть периметр трикутника $ABC$, якщо $\overrightarrow{AB}(3;\,4)$, $\overrightarrow{AC}(3;\,-4)$.",
        "options": [(r"$18$", True), (r"$10$", False), (r"$14$", False), (r"$16$", False), (r"$13$", False)],
        "solution": r"$AB = AC = 5$. Нехай $A(0;\,0)$, тоді $B(3;\,4)$, $C(3;\,-4)$, $\overrightarrow{CB}(0;\,8)$, $BC = 8$. $P = 5 + 5 + 8 = 18$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"$A(1;\,3)$, $B(x;\,7)$. При якому від'ємному $x$ модуль $\overrightarrow{AB}$ дорівнює $5$?",
        "answer": "-2",
        "solution": r"$\overrightarrow{AB}(x - 1;\,4)$: $(x - 1)^2 + 16 = 25$, $x - 1 = \pm 3$, $x = 4$ або $x = -2$. Від'ємне — $-2$.",
    },
    {
        "type": "MULTI", "difficulty": 3, "skill": "SOLVE",
        "text": r"Від точки $P(1;\,1)$ відклали вектори $\vec a(3;\,4)$, $\vec b(-5;\,0)$, $\vec c(0;\,-5)$, $\vec d(4;\,-4)$. Кінці яких векторів лежать на колі з центром $P$ і радіусом $5$?",
        "options": [(r"$\vec a$", True), (r"$\vec b$", True), (r"$\vec c$", True), (r"$\vec d$", False)],
        "solution": r"Кінець лежить на колі, якщо модуль вектора дорівнює $5$: $|\vec a| = |\vec b| = |\vec c| = 5$, $|\vec d| = 4\sqrt2 \approx 5{,}66$.",
    },
    # --- Аналіз результатів ---
    {
        "type": "ERROR", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Учень розв'язував задачу: «$|\vec a(x;\,-6)| = 10$, знайдіть $x$». У якому кроці помилка?",
        "steps": [r"$\sqrt{x^2 + 36} = 10$", r"$x^2 + 36 = 100$", r"$x^2 = 64$", r"$x = 8$ — єдина відповідь"],
        "wrong": 3,
        "solution": r"$x^2 = 64$ має два розв'язки: $x = 8$ і $x = -8$. Вектори $(8;\,-6)$ і $(-8;\,-6)$ обидва мають модуль $10$.",
    },
    {
        "type": "TF", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [(r"Якщо $\vec a \uparrow\uparrow \vec b$ і $\vec b \uparrow\uparrow \vec c$, то $\vec a \uparrow\uparrow \vec c$", True),
                       (r"Якщо $\vec a \uparrow\downarrow \vec b$ і $\vec b \uparrow\downarrow \vec c$, то $\vec a \uparrow\downarrow \vec c$", False),
                       (r"Від даної точки можна відкласти лише один вектор, рівний даному", True)],
        "solution": r"Співнапрямленість передається. Два «протилежно» дають співнапрямлені: $\vec a \uparrow\uparrow \vec c$. Відкладання рівного вектора від точки — єдине.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Учень стверджує: «$\overrightarrow{AB} = \overrightarrow{DC}$, отже, $ABCD$ — паралелограм». Коли це може бути неправильно?",
        "options": [("Коли всі чотири точки лежать на одній прямій", True), ("Коли $ABCD$ — квадрат", False),
                    ("Ніколи — твердження завжди правильне", False), ("Коли $AB \\gt BC$", False)],
        "solution": r"Якщо точки на одній прямій, рівність векторів можлива, але «паралелограм» вироджується у відрізок. Для точок не на одній прямій $ABCD$ — паралелограм.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Скільки існує векторів з цілими координатами, модуль яких дорівнює $5$?",
        "answer": "12",
        "solution": r"$a_1^2 + a_2^2 = 25$: $(\pm 5;\,0)$, $(0;\,\pm 5)$ — 4 вектори; $(\pm 3;\,\pm 4)$ і $(\pm 4;\,\pm 3)$ — ще 8. Разом $12$.",
    },
    {
        "type": "MULTI", "difficulty": 3, "skill": "ANALYZE",
        "text": r"$ABCD$ — трапеція з основами $AD$ і $BC$, $AD = 2BC$. Які твердження правильні?",
        "options": [(r"$\overrightarrow{BC}$ і $\overrightarrow{AD}$ співнапрямлені", True), (r"$|\overrightarrow{AD}| = 2|\overrightarrow{CB}|$", True),
                    (r"$\overrightarrow{AB}$ і $\overrightarrow{DC}$ колінеарні", False), (r"$\overrightarrow{BC} = \overrightarrow{AD}$", False),
                    (r"$\overrightarrow{CB}$ і $\overrightarrow{AD}$ протилежно напрямлені", True)],
        "solution": r"Основи паралельні й «ідуть» в одному напрямку: $\overrightarrow{BC} \uparrow\uparrow \overrightarrow{AD}$, отже $\overrightarrow{CB} \uparrow\downarrow \overrightarrow{AD}$. Модулі: $AD = 2BC = 2CB$. Бічні сторони трапеції не паралельні. Рівності $\overrightarrow{BC} = \overrightarrow{AD}$ немає — різні модулі.",
    },

    # ==========================================
    # БОСИ
    # ==========================================
    {
        "type": "SHORT", "difficulty": 4, "skill": "SOLVE",
        "text": r"$A(-2;\,1)$, $B(1;\,5)$, $C(5;\,2)$. $ABCD$ — паралелограм. Знайдіть $|\overrightarrow{BD}|^2$.",
        "answer": "50",
        "solution": r"$\overrightarrow{AD} = \overrightarrow{BC} = (4;\,-3)$, $D(2;\,-2)$. $\overrightarrow{BD}(1;\,-7)$, $|\overrightarrow{BD}|^2 = 1 + 49 = 50$.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "MODEL",
        "text": r"Точки $A(0;\,0)$, $B(4;\,0)$, $C(4;\,3)$. Скільки існує точок $D$, для яких чотири точки $A$, $B$, $C$, $D$ є вершинами паралелограма (у будь-якому порядку)?",
        "answer": "3",
        "solution": r"Четверта вершина: $A + C - B = (0;\,3)$, $A + B - C = (0;\,-3)$, $B + C - A = (8;\,3)$. Три точки.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "SOLVE",
        "text": r"Вектор $\vec a$ співнапрямлений з вектором $\vec b(3;\,-4)$, а $|\vec a| = 15$. Знайдіть першу координату $\vec a$.",
        "answer": "9",
        "solution": r"$|\vec b| = 5$, $\vec a = 3\vec b = (9;\,-12)$ (множник додатний — співнапрямлені).",
    },
    {
        "type": "TF", "difficulty": 4, "skill": "ANALYZE",
        "text": r"$ABCD$ — ромб, $A(0;\,0)$, $B(3;\,4)$, $D(5;\,0)$. Правда чи ні?",
        "statements": [(r"$C(8;\,4)$", True), (r"$|\overrightarrow{AC}| = 4\sqrt5$", True),
                       (r"$|\overrightarrow{BD}| = 2\sqrt5$", True), (r"$\overrightarrow{AB} = \overrightarrow{CD}$", False)],
        "solution": r"$AB = AD = 5$ — справді ромб. $C = B + \overrightarrow{AD} = (8;\,4)$. $\overrightarrow{AC}(8;\,4)$, $\sqrt{80} = 4\sqrt5$. $\overrightarrow{BD}(2;\,-4)$, $\sqrt{20} = 2\sqrt5$. $\overrightarrow{CD}(-3;\,-4) = -\overrightarrow{AB}$.",
    },
    {
        "type": "CHOICE", "difficulty": 4, "skill": "MODEL",
        "text": r"$ABCDEF$ — правильний шестикутник зі стороною $2$. Знайдіть $|\overrightarrow{AD}|$ і $|\overrightarrow{AC}|$.",
        "options": [(r"$4$ і $2\sqrt3$", True), (r"$4$ і $4$", False), (r"$2\sqrt3$ і $4$", False), (r"$2$ і $2\sqrt3$", False), (r"$4$ і $3$", False)],
        "solution": r"$AD$ — велика діагональ, удвічі більша за сторону: $4$. $AC$ — мала діагональ: $\sqrt{2^2 + 2^2 - 2 \cdot 2 \cdot 2 \cos 120^\circ} = \sqrt{12} = 2\sqrt3$.",
    },

    # ==========================================
    # УЛЬТРА-БОСИ
    # ==========================================
    {
        "type": "SHORT", "difficulty": 5, "skill": "ANALYZE",
        "text": r"Скільки існує векторів з цілими координатами, модуль яких дорівнює $\sqrt{50}$?",
        "answer": "12",
        "solution": r"$a_1^2 + a_2^2 = 50$: $(\pm 1;\,\pm 7)$, $(\pm 7;\,\pm 1)$, $(\pm 5;\,\pm 5)$. По $4$ у кожній групі — $12$.",
    },
    {
        "type": "SHORT", "difficulty": 5, "skill": "SOLVE",
        "text": r"$A(1;\,2)$, $B(5;\,5)$. Точка $C$ лежить на осі $Ox$, а $\overrightarrow{AB} = \overrightarrow{CD}$, де точка $D$ лежить на прямій $y = x$. Знайдіть абсцису точки $C$.",
        "answer": "-1",
        "solution": r"$\overrightarrow{AB}(4;\,3)$. $C(c;\,0)$, $D(c + 4;\,3)$. $D$ на $y = x$: $c + 4 = 3$, $c = -1$.",
    },
]
