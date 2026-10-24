TOPIC_NAME = "3.1. Перпендикулярність прямої та площини"
COURSE = "Геометрія (10-11 класи)"
GRADE = "10 клас"

TASKS = [
    # ===== СХОДИНКА 1 =====
    # --- Моделювання ---
    {
        "type": "CHOICE", "difficulty": 1, "skill": "MODEL",
        "text": r"$ABCDA_1B_1C_1D_1$ — куб. Яка пряма перпендикулярна до площини $(ABC)$?",
        "options": [(r"$CC_1$", True), (r"$AC$", False), (r"$A_1B$", False), (r"$B_1D_1$", False), (r"$AC_1$", False)],
        "hint": "Бічні ребра куба перпендикулярні до основи.",
        "solution": r"$CC_1 \perp CB$ і $CC_1 \perp CD$ — отже, $CC_1 \perp (ABC)$.",
    },
    {
        "type": "TF", "difficulty": 1, "skill": "MODEL",
        "text": r"Правда чи ні?",
        "statements": [(r"Перпендикулярні прямі у просторі можуть бути мимобіжними", True),
                       (r"Якщо $a \perp \alpha$, то $a$ перпендикулярна до кожної прямої площини $\alpha$", True),
                       (r"Через точку можна провести дві різні прямі, перпендикулярні до однієї площини", False)],
        "hint": "Згадайте властивості.",
        "solution": r"Мимобіжні можуть бути перпендикулярними ($AA_1 \perp BC$ у кубі). Пряма через точку, перпендикулярна до площини, єдина.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "MODEL",
        "text": r"Що достатньо перевірити, щоб довести $a \perp \alpha$?",
        "options": [(r"$a$ перпендикулярна до двох прямих площини $\alpha$, що перетинаються", True), (r"$a$ перпендикулярна до однієї прямої площини", False),
                    (r"$a$ перпендикулярна до двох паралельних прямих площини", False), (r"$a$ перетинає площину", False), (r"$a$ паралельна площині", False)],
        "hint": "Згадайте ознаку перпендикулярності прямої та площини.",
        "solution": r"Ознака: дві прямі площини, що перетинаються.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "MODEL",
        "text": r"Стовп висотою $8$ м стоїть вертикально. Від його основи до кілка на землі $6$ м. Яка довжина троса від верхівки стовпа до кілка (у м)?",
        "answer": "10",
        "hint": "Стовп перпендикулярний до будь-якої прямої на землі — трикутник прямокутний.",
        "solution": r"$\sqrt{64 + 36} = 10$ м.",
    },
    {
        "type": "MULTI", "difficulty": 1, "skill": "MODEL",
        "text": r"У кубі $ABCDA_1B_1C_1D_1$ які прямі перпендикулярні до $AA_1$?",
        "options": [(r"$AB$", True), (r"$BC$", True), (r"$B_1D_1$", True), (r"$BB_1$", False), (r"$A_1C$", False)],
        "hint": "$AA_1$ перпендикулярна до площин основ.",
        "solution": r"$AB$, $BC$, $B_1D_1$ лежать у площинах основ, а $AA_1 \perp$ основам. $BB_1 \parallel AA_1$; $A_1C$ — діагональ куба.",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"$SA \perp (ABC)$, $SA = 5$, $AB = 12$. Знайдіть $SB$.",
        "answer": "13",
        "hint": "$\\triangle SAB$ прямокутний з прямим кутом $A$.",
        "solution": r"$SB = \sqrt{25 + 144} = 13$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"$MA \perp (ABC)$, $MB = 17$, $AB = 15$. Знайдіть $MA$.",
        "answer": "8",
        "hint": "$MA^2 = MB^2 - AB^2$.",
        "solution": r"$\sqrt{289 - 225} = 8$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"Знайдіть кут між прямими $AA_1$ і $CD$ у кубі $ABCDA_1B_1C_1D_1$ (у градусах).",
        "answer": "90",
        "hint": "$AA_1 \\perp (ABC)$, а $CD$ лежить у цій площині.",
        "solution": r"$AA_1 \perp (ABC)$, $CD \subset (ABC)$ ⟹ $AA_1 \perp CD$: $90^\circ$.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "SOLVE",
        "text": r"Пряма $a \perp \alpha$, пряма $b \parallel a$. Що можна сказати про $b$?",
        "options": [(r"$b \perp \alpha$", True), (r"$b \parallel \alpha$", False), (r"$b \subset \alpha$", False), (r"нічого", False), (r"$b$ перетинає $\alpha$ під кутом $45^\circ$", False)],
        "hint": "Властивість паралельних прямих.",
        "solution": r"Якщо одна з паралельних прямих перпендикулярна до площини, то й друга.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"Знайдіть кут між мимобіжними прямими $AB$ і $CC_1$ у кубі (у градусах).",
        "answer": "90",
        "hint": "$CC_1 \\parallel BB_1$.",
        "solution": r"$CC_1 \parallel BB_1$, $BB_1 \perp AB$ ⟹ кут $90^\circ$.",
    },
    # --- Аналіз ---
    {
        "type": "TF", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Правда чи ні (у просторі)?",
        "statements": [(r"Дві прямі, перпендикулярні до однієї площини, паралельні", True),
                       (r"Дві прямі, перпендикулярні до однієї прямої, паралельні", False),
                       (r"Пряма, перпендикулярна до однієї з двох паралельних площин, перпендикулярна й до другої", True)],
        "hint": "Візьміть куб: $AB \\perp AA_1$ і $AD \\perp AA_1$.",
        "solution": r"$AB$ і $AD$ обидві $\perp AA_1$, але перетинаються. Решта — властивості.",
    },
    {
        "type": "ERROR", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Оля доводила $a \perp \alpha$. У якому кроці помилка?",
        "steps": [r"$b$ і $c$ лежать у площині $\alpha$, $b \parallel c$", r"$a \perp b$ і $a \perp c$", r"За ознакою $a \perp \alpha$"],
        "wrong": 2,
        "hint": "Які прямі потрібні в ознаці?",
        "solution": r"Ознака вимагає прямих, що перетинаються, а $b \parallel c$.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Тарас: «$AA_1$ і $BD$ у кубі не перетинаються, тож не можуть бути перпендикулярними». Чи правий він?",
        "options": [(r"Ні, вони мимобіжні й перпендикулярні", True), (r"Так", False), (r"Ні, вони перетинаються", False), (r"Ні, вони паралельні", False)],
        "hint": "$AA_1 \\perp (ABC)$.",
        "solution": r"$BD \subset (ABC)$, $AA_1 \perp (ABC)$ ⟹ $AA_1 \perp BD$, хоча прямі мимобіжні.",
    },
    {
        "type": "GROUP", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Куб $ABCDA_1B_1C_1D_1$. Чи перпендикулярна пряма до площини $(ABB_1)$?",
        "groups": ["перпендикулярна", "не перпендикулярна"],
        "items": [(r"$BC$", 0), (r"$AD$", 0), (r"$C_1B_1$", 0), (r"$AC$", 1), (r"$CC_1$", 1), (r"$BD_1$", 1)],
        "hint": "Перпендикулярні до грані $ABB_1A_1$ — ребра, що виходять з неї під прямим кутом.",
        "solution": r"$BC$, $AD$, $B_1C_1$ — ребра, перпендикулярні до грані. $AC$, $BD_1$ — похилі; $CC_1 \parallel BB_1$ лежить паралельно грані.",
    },
    {
        "type": "MULTI", "difficulty": 1, "skill": "ANALYZE",
        "text": r"$SA \perp (ABC)$. Які кути обов'язково прямі?",
        "options": [(r"$\angle SAB$", True), (r"$\angle SAC$", True), (r"$\angle SBA$", False), (r"$\angle ASC$", False)],
        "hint": "$SA$ перпендикулярна до прямих площини, що проходять через $A$.",
        "solution": r"$AB$ і $AC$ лежать у $(ABC)$ — кути при $A$ прямі.",
    },

    # ===== СХОДИНКА 2 =====
    # --- Моделювання ---
    {
        "type": "SHORT", "difficulty": 2, "skill": "MODEL",
        "text": r"Кінці відрізка $AB$ лежать по один бік від площини, $AA_1$ і $BB_1$ — перпендикуляри до площини, $AA_1 = 3$, $BB_1 = 7$, $A_1B_1 = 3$. Знайдіть $AB$.",
        "answer": "5",
        "solution": r"$AA_1 \parallel BB_1$ (обидві $\perp$ площині). $AA_1B_1B$ — прямокутна трапеція; $AB = \sqrt{3^2 + (7 - 3)^2} = 5$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "MODEL",
        "text": r"Кінці відрізка лежать по різні боки від площини на перпендикулярах завдовжки $2$ і $4$; відстань між основами перпендикулярів $8$. Знайдіть довжину відрізка.",
        "answer": "10",
        "solution": r"Різниця «висот» тепер — сума: $2 + 4 = 6$. $\sqrt{36 + 64} = 10$.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "MODEL",
        "text": r"У прямокутному паралелепіпеді $ABCDA_1B_1C_1D_1$ яка площина перпендикулярна до $BD$, якщо основа — квадрат?",
        "options": [(r"$(AA_1C_1)$", True), (r"$(ABB_1)$", False), (r"$(A_1B_1C_1)$", False), (r"$(BB_1D_1)$", False), (r"$(ADD_1)$", False)],
        "solution": r"$BD \perp AC$ (діагоналі квадрата) і $BD \perp AA_1$ ⟹ $BD \perp (AA_1C_1C)$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "MODEL",
        "text": r"Драбину завдовжки $5$ м приставили до вертикальної стіни; нижній кінець на $3$ м від стіни. На якій висоті верхній кінець (у м)?",
        "answer": "4",
        "solution": r"Стіна ⊥ землі, тож кут між стіною й землею вздовж драбини прямий: $\sqrt{25 - 9} = 4$ м.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "MODEL",
        "text": r"Знайдіть довжину діагоналі прямокутного паралелепіпеда з вимірами $2$, $3$, $6$.",
        "answer": "7",
        "solution": r"$AC^2 = 4 + 9 = 13$; $CC_1 \perp AC$: $AC_1 = \sqrt{13 + 36} = 7$.",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"$SA \perp (ABCD)$, $ABCD$ — квадрат зі стороною $3$, $SA = 4$. Знайдіть $SC^2$.",
        "answer": "34",
        "solution": r"$AC^2 = 18$, $SC^2 = 16 + 18 = 34$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Точка $S$ рівновіддалена від вершин правильного трикутника зі стороною $6\sqrt3$, $O$ — центр трикутника, $SO \perp (ABC)$, $SO = 8$. Знайдіть $SA$.",
        "answer": "10",
        "solution": r"$OA = R = \dfrac{a}{\sqrt3} = 6$. $SA = \sqrt{64 + 36} = 10$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Знайдіть кут між прямими $AD_1$ і $BC_1$ у кубі (у градусах).",
        "answer": "0",
        "solution": r"$AD_1 \parallel BC_1$ (протилежні сторони прямокутника $ABC_1D_1$) — кут $0^\circ$.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "SOLVE",
        "text": r"Знайдіть кут між мимобіжними прямими $AB_1$ і $BC_1$ у кубі.",
        "options": [(r"$60^\circ$", True), (r"$90^\circ$", False), (r"$45^\circ$", False), (r"$30^\circ$", False), (r"$0^\circ$", False)],
        "solution": r"$BC_1 \parallel AD_1$. Кут між $AB_1$ і $AD_1$: $\triangle AB_1D_1$ — рівносторонній (діагоналі граней), кут $60^\circ$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"$SA \perp (ABC)$, $\angle ACB = 90^\circ$, $AC = 3$, $BC = 4$, $SA = 12$. Знайдіть $SB$.",
        "answer": "13",
        "solution": r"$AB = 5$; $SB = \sqrt{144 + 25} = 13$.",
    },
    # --- Аналіз ---
    {
        "type": "ERROR", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Тарас: «$SA \perp (ABC)$, $SB = 10$, $SA = 6$. Знайти $AB$». У якому кроці помилка?",
        "steps": [r"$SA \perp AB$, бо $AB \subset (ABC)$", r"$AB = SB + SA = 16$"],
        "wrong": 1,
        "solution": r"$\triangle SAB$ прямокутний: $AB = \sqrt{100 - 36} = 8$.",
    },
    {
        "type": "TF", "difficulty": 2, "skill": "ANALYZE",
        "text": r"$ABCD$ — ромб, $O$ — точка перетину діагоналей, $SO \perp (ABC)$. Правда чи ні?",
        "statements": [(r"$AC \perp (SBD)$", True), (r"$SA = SC$", True), (r"$SA \perp (ABC)$", False), (r"$BD \perp SC$", True)],
        "solution": r"$AC \perp BD$, $AC \perp SO$ ⟹ $AC \perp (SBD)$. $\triangle SOA = \triangle SOC$. $BD \perp AC$, $BD \perp SO$ ⟹ $BD \perp (SAC) \ni SC$. $SA$ — похила.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "ANALYZE",
        "text": r"$a \perp b$, $b \perp c$ (у просторі). Яким може бути взаємне розміщення $a$ і $c$?",
        "options": [(r"будь-яким: паралельні, перетинаються або мимобіжні", True), (r"лише паралельні", False), (r"лише перпендикулярні", False), (r"лише мимобіжні", False), (r"лише перетинаються", False)],
        "solution": r"Куб: $AB \perp AA_1$, $AA_1 \perp DC$ ($AB \parallel DC$); $AA_1 \perp AD$ ($AB$ і $AD$ перетинаються); $AA_1 \perp B_1C_1$ ($AB$ і $B_1C_1$ мимобіжні).",
    },
    {
        "type": "MULTI", "difficulty": 2, "skill": "ANALYZE",
        "text": r"У правильній піраміді $SABCD$ ($O$ — центр квадрата, $SO \perp (ABC)$) які прямі перпендикулярні?",
        "options": [(r"$AC$ і $SO$", True), (r"$BD$ і $SA$", True), (r"$SO$ і $AB$", True), (r"$SA$ і $SC$", False)],
        "solution": r"$SO \perp$ всім прямим основи. $BD \perp (SAC)$ ⟹ $BD \perp SA$. $SA$ і $SC$ — не обов'язково.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Скільки прямих, перпендикулярних до даної площини, можна провести через точку, що не лежить у ній?",
        "answer": "1",
        "solution": r"Така пряма єдина.",
    },

    # ===== СХОДИНКА 3 =====
    # --- Моделювання ---
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"Відрізок $AB = 13$ не перетинає площину; його кінці на відстанях (перпендикулярах) $3$ і $8$ від неї. Знайдіть довжину проекції відрізка — відстань між основами перпендикулярів.",
        "answer": "12",
        "solution": r"$\sqrt{169 - (8 - 3)^2} = \sqrt{144} = 12$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"Перпендикуляри з кінців відрізка до площини дорівнюють $5$ і $11$. Знайдіть перпендикуляр із середини відрізка (кінці по один бік).",
        "answer": "8",
        "solution": r"Три перпендикуляри паралельні й лежать в одній площині — середня лінія трапеції: $\dfrac{5 + 11}{2} = 8$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"Перпендикуляри з кінців відрізка до площини дорівнюють $5$ і $11$, кінці по різні боки площини. Знайдіть перпендикуляр із середини відрізка.",
        "answer": "3",
        "solution": r"Беремо зі знаком: $\dfrac{11 + (-5)}{2} = 3$.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "MODEL",
        "text": r"У кубі з ребром $a$ знайдіть довжину діагоналі $AC_1$.",
        "options": [(r"$a\sqrt3$", True), (r"$a\sqrt2$", False), (r"$3a$", False), (r"$2a$", False), (r"$a\sqrt5$", False)],
        "solution": r"$CC_1 \perp AC$, $AC = a\sqrt2$: $AC_1 = \sqrt{2a^2 + a^2} = a\sqrt3$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"Точка $M$ віддалена від кожної вершини квадрата зі стороною $4\sqrt2$ на $5$. Знайдіть відстань від $M$ до центру квадрата $O$ ($MO \perp$ площині квадрата).",
        "answer": "3",
        "solution": r"$OA = \dfrac{4\sqrt2 \cdot \sqrt2}{2} = 4$. $MO = \sqrt{25 - 16} = 3$.",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"$SA \perp (ABC)$, $\triangle ABC$ правильний зі стороною $6$, $SA = 6$. Знайдіть $SM^2$, де $M$ — середина $BC$.",
        "answer": "63",
        "solution": r"$AM = 3\sqrt3$, $AM^2 = 27$. $SM^2 = 36 + 27 = 63$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Знайдіть кут між мимобіжними прямими $B_1D_1$ і $AC$ у кубі (у градусах).",
        "answer": "90",
        "solution": r"$B_1D_1 \parallel BD$, $BD \perp AC$ — кут $90^\circ$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Доведено, що $AC \perp (BB_1D_1)$ у кубі. Знайдіть кут між $AC$ і $BD_1$ (у градусах).",
        "answer": "90",
        "solution": r"$BD_1$ лежить у площині $(BB_1D_1D)$, а $AC \perp$ цій площині: $90^\circ$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"$ABCD$ — прямокутник, $AB = 6$, $BC = 8$, $SA \perp (ABC)$, $SA = 24$. Знайдіть $SC$.",
        "answer": "26",
        "solution": r"$AC = 10$; $SC = \sqrt{576 + 100} = 26$.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "SOLVE",
        "text": r"$SA \perp (ABC)$, $\angle ABC = 90^\circ$. Який кут обов'язково прямий?",
        "options": [(r"$\angle SBC$", True), (r"$\angle SCB$", False), (r"$\angle BSC$", False), (r"$\angle SCA$", False), (r"$\angle ASB$", False)],
        "solution": r"$BC \perp AB$ і $BC \perp SA$ ⟹ $BC \perp (SAB)$ ⟹ $BC \perp SB$: $\angle SBC = 90^\circ$.",
    },
    # --- Аналіз ---
    {
        "type": "TF", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [(r"Якщо пряма перпендикулярна до двох сторін трикутника, то вона перпендикулярна і до третьої", True),
                       (r"Якщо пряма перпендикулярна до двох діаметрів кола, то вона перпендикулярна до площини кола", True),
                       (r"Якщо пряма перпендикулярна до двох сторін трапеції, то вона перпендикулярна до площини трапеції", False)],
        "solution": r"Дві сторони трикутника перетинаються — ознака. Діаметри перетинаються. Дві основи трапеції паралельні — ознака не працює.",
    },
    {
        "type": "ERROR", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Оля доводила $BC \perp SB$, де $SA \perp (ABC)$, $\angle ABC = 90^\circ$. У якому кроці помилка?",
        "steps": [r"$BC \perp AB$ (за умовою)", r"Отже, $BC \perp SB$, бо $BC$ перпендикулярна до прямої $AB$ площини $(SAB)$", r"$\angle SBC = 90^\circ$"],
        "wrong": 1,
        "solution": r"Однієї прямої мало. Треба ще $BC \perp SA$ (бо $SA \perp (ABC)$); тоді $BC \perp (SAB)$ за ознакою і $BC \perp SB$.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Пряма $a$ перпендикулярна до прямих $b$ і $c$, які мимобіжні. Що можна стверджувати про $a$ і площину, що містить $b$ і паралельна $c$?",
        "options": [(r"$a$ перпендикулярна до неї", True), (r"$a$ паралельна їй", False), (r"$a$ лежить у ній", False), (r"нічого", False), (r"$a$ утворює з нею $45^\circ$", False)],
        "solution": r"У площині через $b$ є пряма $c' \parallel c$, що перетинає $b$; $a \perp c'$, $a \perp b$ ⟹ $a \perp$ площині.",
    },
    {
        "type": "MULTI", "difficulty": 3, "skill": "ANALYZE",
        "text": r"$SABC$ — тетраедр, $SA \perp (ABC)$, $AB = AC$, $M$ — середина $BC$. Що правильно?",
        "options": [(r"$BC \perp AM$", True), (r"$BC \perp (SAM)$", True), (r"$BC \perp SM$", True), (r"$SM \perp (ABC)$", False), (r"$SB = SC$", True)],
        "solution": r"$AM$ — медіана й висота рівнобедреного. $BC \perp AM$, $BC \perp SA$ ⟹ $BC \perp (SAM)$ ∋ $SM$. $SB = SC$ (рівні прямокутні трикутники). $SM$ — похила.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Скільки ребер куба перпендикулярні до діагоналі грані $AC$?",
        "answer": "4",
        "solution": r"$AA_1$, $BB_1$, $CC_1$, $DD_1$ — перпендикулярні до основи. Ребра основ — під $45^\circ$.",
    },

    # ===== БОСИ =====
    {
        "type": "SHORT", "difficulty": 4, "skill": "MODEL",
        "text": r"Точка $S$ віддалена від усіх вершин прямокутного трикутника з катетами $6$ і $8$ на $13$. Знайдіть відстань від $S$ до площини трикутника (довжину перпендикуляра).",
        "answer": "12",
        "solution": r"Основа перпендикуляра — центр описаного кола, середина гіпотенузи; $R = 5$. $\sqrt{169 - 25} = 12$.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "MODEL",
        "text": r"Діагоналі трьох граней прямокутного паралелепіпеда дорівнюють $\sqrt{13}$, $\sqrt{20}$, $5$. Знайдіть квадрат діагоналі паралелепіпеда.",
        "answer": "29",
        "solution": r"$a^2 + b^2 = 13$, $b^2 + c^2 = 20$, $a^2 + c^2 = 25$: сума $= 2(a^2 + b^2 + c^2) = 58$, $d^2 = 29$.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "SOLVE",
        "text": r"У кубі з ребром $2$ точка $M$ — середина $AA_1$. Знайдіть $MC_1^2$.",
        "answer": "9",
        "solution": r"$A_1C_1^2 = 8$, $MA_1 = 1$, $MA_1 \perp A_1C_1$: $MC_1^2 = 1 + 8 = 9$.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "SOLVE",
        "text": r"$SA \perp (ABC)$, $AB = BC = AC = 2$, $SA = 1$. Знайдіть $SM$, де $M$ — середина $BC$.",
        "answer": "2",
        "solution": r"$AM = \sqrt3$, $SM = \sqrt{1 + 3} = 2$.",
    },
    {
        "type": "TF", "difficulty": 4, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [(r"Існує тетраедр, у якому кожне ребро перпендикулярне до протилежного", True),
                       (r"У кубі $AC_1 \perp B_1D_1$", True), (r"У кубі $AC_1 \perp AB$", False)],
        "solution": r"Правильний тетраедр: $AB \perp CD$ (через середину). $B_1D_1 \perp A_1C_1$ і $B_1D_1 \perp AA_1$ ⟹ $B_1D_1 \perp (AA_1C_1) \ni AC_1$. Кут між $AC_1$ і $AB$ — гострий ($\cos = \dfrac{1}{\sqrt3}$).",
    },
    {
        "type": "SHORT", "difficulty": 5, "skill": "SOLVE",
        "text": r"У тетраедрі $SABC$ ребра $SA$, $SB$, $SC$ попарно перпендикулярні й дорівнюють $1$, $2$, $2$. Знайдіть квадрат площі грані $ABC$.",
        "answer": "6",
        "solution": r"$AB = AC = \sqrt5$, $BC = 2\sqrt2$. Висота з $A$ на $BC$: $\sqrt{5 - 2} = \sqrt3$. $S = \dfrac12 \cdot 2\sqrt2 \cdot \sqrt3 = \sqrt6$, $S^2 = 6$.",
    },
    {
        "type": "SHORT", "difficulty": 5, "skill": "ANALYZE",
        "text": r"Скільки існує площин, перпендикулярних до даної прямої, що проходять через дану точку?",
        "answer": "1",
        "solution": r"Через точку проходить єдина площина, перпендикулярна до даної прямої (вона утворена всіма прямими через точку, перпендикулярними до даної).",
    },
]
