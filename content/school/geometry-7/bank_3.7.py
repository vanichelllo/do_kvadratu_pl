TOPIC_NAME = "3.7. Медіана, бісектриса і висота трикутника"
COURSE = "Геометрія (7-9 класи)"
GRADE = "7 клас"

TASKS = [
    # ===== СХОДИНКА 1 =====
    # --- Моделювання ---
    {
        "type": "MATCH", "difficulty": 1, "skill": "MODEL",
        "text": r"Установіть відповідність між відрізком (1–3) та його властивістю (А–Д).",
        "options": [r"А) ділить протилежну сторону навпіл", r"Б) ділить кут навпіл", r"В) перпендикулярний до прямої протилежної сторони", r"Г) паралельний стороні", r"Д) дорівнює стороні"],
        "matches": [(r"1. медіана", r"А) ділить протилежну сторону навпіл"), (r"2. бісектриса", r"Б) ділить кут навпіл"), (r"3. висота", r"В) перпендикулярний до прямої протилежної сторони")],
        "hint": "Згадайте означення.",
        "solution": r"Медіана — до середини, бісектриса — кут навпіл, висота — під прямим кутом.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "MODEL",
        "text": r"Скільки медіан має трикутник?",
        "answer": "3",
        "hint": "З кожної вершини — одна.",
        "solution": r"$3$ — по одній з кожної вершини.",
    },
    {
        "type": "TF", "difficulty": 1, "skill": "MODEL",
        "text": r"Правда чи ні?",
        "statements": [(r"Медіана завжди лежить усередині трикутника", True), (r"Висота завжди лежить усередині трикутника", False), (r"У прямокутному трикутнику катет є висотою", True)],
        "hint": "Згадайте тупокутний трикутник.",
        "solution": r"Висота з вершини гострого кута тупокутного трикутника — поза ним.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "MODEL",
        "text": r"$BM$ — медіана $\triangle ABC$. Яка рівність правильна?",
        "options": [(r"$AM = MC$", True), (r"$\angle ABM = \angle MBC$", False), (r"$BM \perp AC$", False), (r"$AB = BC$", False)],
        "hint": "Медіана — до середини сторони.",
        "solution": r"$M$ — середина $AC$.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "MODEL",
        "text": r"$BH$ — висота $\triangle ABC$. Який кут прямий?",
        "options": [(r"$\angle BHA$", True), (r"$\angle ABH$", False), (r"$\angle ABC$", False), (r"$\angle BAH$", False)],
        "hint": "Висота перпендикулярна до прямої $AC$.",
        "solution": r"$BH \perp AC$ ⟹ $\angle BHA = 90^\circ$.",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"$BM$ — медіана $\triangle ABC$, $AC = 18$ см. Знайдіть $MC$ (у см).",
        "answer": "9",
        "hint": "Медіана ділить сторону навпіл.",
        "solution": r"$18 : 2 = 9$ см.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"$AL$ — бісектриса $\triangle ABC$, $\angle BAL = 35^\circ$. Знайдіть $\angle BAC$ (у градусах).",
        "answer": "70",
        "hint": "Бісектриса ділить кут навпіл.",
        "solution": r"$2 \cdot 35^\circ = 70^\circ$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"$BH$ — висота $\triangle ABC$, $\angle A = 55^\circ$. Знайдіть $\angle ABH$ (у градусах).",
        "answer": "35",
        "hint": "$\\triangle ABH$ — прямокутний.",
        "solution": r"$90^\circ - 55^\circ = 35^\circ$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"У рівнобедреному трикутнику з основою $16$ см проведено бісектрису до основи. На які відрізки вона ділить основу (довжина кожного, у см)?",
        "answer": "8",
        "hint": "Бісектриса до основи — і медіана.",
        "solution": r"$16 : 2 = 8$ см.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "SOLVE",
        "text": r"У рівнобедреному $\triangle ABC$ ($AB = BC$) $BM$ — медіана. Знайдіть $\angle BMC$.",
        "options": [(r"$90^\circ$", True), (r"$45^\circ$", False), (r"$60^\circ$", False), (r"$180^\circ$", False)],
        "hint": "Медіана до основи — і висота.",
        "solution": r"$BM \perp AC$.",
    },
    # --- Аналіз ---
    {
        "type": "ERROR", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Оля: «$BL$ — бісектриса $\triangle ABC$, $AC = 12$. Тоді $AL = 6$». У якому кроці помилка?",
        "steps": [r"Бісектриса ділить кут $B$ навпіл", r"Отже, вона ділить і сторону $AC$ навпіл", r"$AL = 6$"],
        "wrong": 1,
        "hint": "Що ділить навпіл сторону?",
        "solution": r"Сторону навпіл ділить медіана; бісектриса — лише в рівнобедреному до основи.",
    },
    {
        "type": "MULTI", "difficulty": 1, "skill": "ANALYZE",
        "text": r"У рівнобедреному $\triangle ABC$ ($AB = BC$) з вершини $B$ проведено відрізок до основи. Він може бути одночасно…",
        "options": [(r"медіаною і висотою", True), (r"бісектрисою і медіаною", True), (r"висотою і бісектрисою", True), (r"бічною стороною", False)],
        "hint": "Властивість рівнобедреного трикутника.",
        "solution": r"Бісектриса, медіана й висота до основи збігаються.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Тарас: «У будь-якому трикутнику медіана і висота збігаються». Чи правий він?",
        "options": [(r"Ні, лише в рівнобедреному (до основи)", True), (r"Так", False), (r"Так, у прямокутному", False), (r"Ні, вони ніколи не збігаються", False)],
        "hint": "Подумайте про різносторонній трикутник.",
        "solution": r"Якщо медіана й висота збігаються, трикутник рівнобедрений.",
    },
    {
        "type": "GROUP", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Що відомо про відрізок $BK$ у $\triangle ABC$ ($K$ на $AC$)?",
        "groups": ["медіана", "бісектриса", "висота"],
        "items": [(r"$AK = KC$", 0), (r"$\angle ABK = \angle KBC$", 1), (r"$\angle BKC = 90^\circ$", 2), (r"$K$ — середина $AC$", 0), (r"$BK \perp AC$", 2), (r"$\angle ABC = 2\angle ABK$", 1)],
        "hint": "Розпізнайте означення.",
        "solution": r"Середина — медіана; рівні кути — бісектриса; прямий кут — висота.",
    },
    {
        "type": "TF", "difficulty": 1, "skill": "ANALYZE",
        "text": r"У прямокутному $\triangle ABC$ ($\angle C = 90^\circ$) правда чи ні?",
        "statements": [(r"$AC$ — висота, проведена з $A$", True), (r"$BC$ — висота, проведена з $B$", True), (r"Висота з $C$ збігається з катетом", False)],
        "hint": "Висота з $C$ падає на гіпотенузу.",
        "solution": r"Катети — висоти з вершин гострих кутів; висота з $C$ — окремий відрізок до гіпотенузи.",
    },

    # ===== СХОДИНКА 2 =====
    # --- Моделювання ---
    {
        "type": "SHORT", "difficulty": 2, "skill": "MODEL",
        "text": r"Медіана $BM$ ділить $\triangle ABC$ на два трикутники. Периметри $\triangle ABM$ і $\triangle CBM$ — $24$ см і $30$ см, $AB = 8$ см. Знайдіть $BC$.",
        "answer": "14",
        "solution": r"$P_2 - P_1 = BC - AB$ (бо $AM = MC$, $BM$ спільна) $= 6$ ⟹ $BC = 14$ см.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "MODEL",
        "text": r"Периметр рівнобедреного трикутника $40$ см, бічна сторона $13$ см. Медіана до основи ділить її на відрізки — знайдіть довжину кожного (у см).",
        "answer": "7",
        "solution": r"Основа $40 - 26 = 14$; медіана ділить навпіл: $7$ см.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "MODEL",
        "text": r"У $\triangle ABC$ бісектриса $BL$ є висотою. Що можна стверджувати?",
        "options": [(r"$AB = BC$", True), (r"$AB = AC$", False), (r"$\angle B = 90^\circ$", False), (r"$AL = BL$", False), (r"нічого", False)],
        "solution": r"$\triangle ABL = \triangle CBL$ (катет $BL$ і гострий кут) ⟹ $AB = BC$.",
    },
    {
        "type": "FIELDS", "difficulty": 2, "skill": "MODEL",
        "text": r"$\triangle ABC$: $\angle A = 40^\circ$, $\angle C = 60^\circ$. Знайдіть кути, які утворює бісектриса $BL$ зі стороною $AC$ (менший, більший).",
        "fields": [("Менший:", "80"), ("Більший:", "100")],
        "solution": r"$\angle B = 80^\circ$, $\angle ABL = 40^\circ$. $\angle ALB = 180 - 40 - 40 = 100^\circ$, $\angle CLB = 80^\circ$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "MODEL",
        "text": r"У рівнобедреному $\triangle ABC$ ($AB = BC$) $\angle A = 65^\circ$, $BH$ — висота. Знайдіть $\angle ABH$ (у градусах).",
        "answer": "25",
        "solution": r"$90^\circ - 65^\circ = 25^\circ$ (і висота — бісектриса: $\angle B = 50^\circ$).",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"У $\triangle ABC$ $\angle A = 30^\circ$, $\angle C = 80^\circ$. Знайдіть кут між висотою $BH$ і бісектрисою $BL$ (у градусах).",
        "answer": "25",
        "solution": r"$\angle B = 70^\circ$, $\angle ABL = 35^\circ$, $\angle ABH = 60^\circ$; $60 - 35 = 25^\circ$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"У рівнобедреному $\triangle ABC$ з основою $AC$ медіана $BM = 6$ см, периметр $\triangle ABC$ — $36$ см. Знайдіть периметр $\triangle ABM$.",
        "answer": "24",
        "solution": r"$P_{ABM} = AB + AM + BM = \dfrac{P}{2} + BM = 18 + 6 = 24$ см.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "SOLVE",
        "text": r"У прямокутному $\triangle ABC$ ($\angle C = 90^\circ$) $\angle A = 30^\circ$, $CH$ — висота. Знайдіть $\angle BCH$.",
        "options": [(r"$30^\circ$", True), (r"$60^\circ$", False), (r"$45^\circ$", False), (r"$90^\circ$", False), (r"$15^\circ$", False)],
        "solution": r"$\angle B = 60^\circ$; у $\triangle BCH$: $90^\circ - 60^\circ = 30^\circ$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Бісектриса прямого кута прямокутного трикутника утворює з гіпотенузою кут $65^\circ$ (менший). Знайдіть менший гострий кут трикутника (у градусах).",
        "answer": "20",
        "solution": r"Бісектриса ділить прямий кут на $45^\circ$. У трикутнику з кутом $65^\circ$ третій кут $70^\circ$; у другому — $180 - 45 - 115 = 20^\circ$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Висота $BH$ ділить кут $B$ трикутника на кути $20^\circ$ і $40^\circ$. Знайдіть найменший кут трикутника (у градусах).",
        "answer": "50",
        "solution": r"$\angle A = 90 - 20 = 70^\circ$, $\angle C = 90 - 40 = 50^\circ$, $\angle B = 60^\circ$. Найменший — $50^\circ$.",
    },
    # --- Аналіз ---
    {
        "type": "ERROR", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Тарас: «$AB = BC$, $BM$ — медіана, $\angle ABC = 70^\circ$. Знайти $\angle BAM$». У якому кроці помилка?",
        "steps": [r"$BM$ — бісектриса, $\angle ABM = 35^\circ$", r"$BM$ — висота, $\angle BMA = 90^\circ$", r"$\angle BAM = 180^\circ - 35^\circ = 145^\circ$"],
        "wrong": 2,
        "solution": r"$\angle BAM = 180^\circ - 90^\circ - 35^\circ = 55^\circ$.",
    },
    {
        "type": "TF", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [(r"Якщо медіана трикутника є висотою, то трикутник рівнобедрений", True), (r"У рівносторонньому трикутнику кожна медіана є бісектрисою і висотою", True), (r"Бісектриса трикутника завжди ділить протилежну сторону навпіл", False)],
        "solution": r"Ознака рівнобедреного; у рівносторонньому кожна сторона — основа. Бісектриса ділить сторону навпіл лише в рівнобедреному (до основи).",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Висота $BH$ трикутника $ABC$ лежить поза трикутником. Що можна сказати про трикутник?",
        "options": [(r"він тупокутний", True), (r"він прямокутний", False), (r"він гострокутний", False), (r"він рівнобедрений", False), (r"такого не буває", False)],
        "solution": r"Основа висоти поза стороною — один з кутів при цій стороні тупий.",
    },
    {
        "type": "MULTI", "difficulty": 2, "skill": "ANALYZE",
        "text": r"У $\triangle ABC$ $AB = BC$, $BL$ — бісектриса, $AC = 10$. Що правильно?",
        "options": [(r"$AL = 5$", True), (r"$BL \perp AC$", True), (r"$\angle BAL = \angle BCL$", True), (r"$BL = 5$", False)],
        "solution": r"Бісектриса до основи — медіана і висота; кути при основі рівні. Довжина $BL$ невідома.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Скільки висот прямокутного трикутника лежить на його сторонах?",
        "answer": "2",
        "solution": r"Два катети; третя висота — до гіпотенузи.",
    },

    # ===== СХОДИНКА 3 =====
    # --- Моделювання ---
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"Периметр рівнобедреного трикутника $50$ см, а периметр одного з трикутників, на які його ділить медіана до основи, — $40$ см. Знайдіть медіану.",
        "answer": "15",
        "solution": r"$P_{ABM} = \dfrac{P}{2} + BM$ ⟹ $40 = 25 + BM$, $BM = 15$ см.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"Медіана $AM$ трикутника $ABC$ дорівнює половині $BC$. Знайдіть $\angle A$ (у градусах).",
        "answer": "90",
        "solution": r"$MA = MB = MC$ ⟹ $\triangle ABM$ і $\triangle ACM$ рівнобедрені: $\angle B + \angle C = \angle A$, а сума $180^\circ$ ⟹ $\angle A = 90^\circ$.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "MODEL",
        "text": r"$AA_1$ і $CC_1$ — висоти, проведені до бічних сторін рівнобедреного трикутника з основою $AC$. Що можна сказати про них?",
        "options": [(r"вони рівні", True), (r"вони перпендикулярні", False), (r"одна вдвічі більша", False), (r"вони паралельні", False), (r"нічого", False)],
        "solution": r"$\triangle AA_1C = \triangle CC_1A$ (спільна гіпотенуза $AC$, рівні кути при основі) ⟹ $AA_1 = CC_1$.",
    },
    {
        "type": "FIELDS", "difficulty": 3, "skill": "MODEL",
        "text": r"$AL$ — бісектриса $\triangle ABC$, $\angle ALC = 80^\circ$, $\angle C = 60^\circ$. Знайдіть $\angle A$ і $\angle B$.",
        "fields": [(r"$\angle A$:", "80"), (r"$\angle B$:", "40")],
        "solution": r"У $\triangle ALC$: $\angle LAC = 180 - 80 - 60 = 40^\circ$ ⟹ $\angle A = 80^\circ$, $\angle B = 180 - 80 - 60 = 40^\circ$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"У $\triangle ABC$ $\angle C = 90^\circ$, $\angle B = 60^\circ$, $CH$ — висота, $BH = 2$ см. Знайдіть $AH$ (у см).",
        "answer": "6",
        "solution": r"У $\triangle BCH$ $\angle BCH = 30^\circ$ ⟹ $BC = 4$. $AB = 2BC = 8$; $AH = 8 - 2 = 6$ см.",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"У $\triangle ABC$ $\angle A = 40^\circ$, $\angle B = 80^\circ$. $AL$ і $BK$ — бісектриси, $O$ — точка їх перетину. Знайдіть $\angle AOB$ (у градусах).",
        "answer": "120",
        "solution": r"$\angle OAB = 20^\circ$, $\angle OBA = 40^\circ$; $\angle AOB = 120^\circ$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"У гострокутному $\triangle ABC$ $\angle A = 60^\circ$, $\angle C = 50^\circ$. Висоти $AA_1$ і $CC_1$ перетинаються в $H$. Знайдіть $\angle AHC$ (у градусах).",
        "answer": "110",
        "solution": r"$\angle HAC = 90 - 50 = 40^\circ$, $\angle HCA = 90 - 60 = 30^\circ$; $\angle AHC = 110^\circ$.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "SOLVE",
        "text": r"У прямокутному трикутнику кут між бісектрисою і висотою, проведеними з вершини прямого кута, — $10^\circ$. Знайдіть більший гострий кут.",
        "options": [(r"$55^\circ$", True), (r"$45^\circ$", False), (r"$35^\circ$", False), (r"$80^\circ$", False), (r"$50^\circ$", False)],
        "solution": r"Висота утворює з катетом кут, рівний протилежному гострому; бісектриса — $45^\circ$. Менший гострий $35^\circ$, більший $55^\circ$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Медіана $BM$ рівнобедреного $\triangle ABC$ ($AB = BC$) утворює з бічною стороною кут $25^\circ$. Знайдіть кут при основі (у градусах).",
        "answer": "65",
        "solution": r"$BM$ — бісектриса і висота: $\angle A = 90 - 25 = 65^\circ$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"У рівнобедреному трикутнику кут при вершині $120^\circ$, висота до основи $6$ см. Знайдіть бічну сторону (у см).",
        "answer": "12",
        "solution": r"Кути при основі по $30^\circ$; висота — катет проти $30^\circ$: бічна сторона $12$ см.",
    },
    # --- Аналіз ---
    {
        "type": "TF", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [(r"Якщо медіана і бісектриса з однієї вершини збігаються, трикутник рівнобедрений", True), (r"Висоти тупокутного трикутника перетинаються всередині нього", False), (r"Три бісектриси трикутника перетинаються в одній точці всередині трикутника", True)],
        "solution": r"Ознака рівнобедреного. Висоти (їх прямі) тупокутного перетинаються поза ним. Бісектриси — всередині.",
    },
    {
        "type": "ERROR", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Оля: «$\angle A = 50^\circ$, $\angle C = 70^\circ$; кут між бісектрисою $BL$ і висотою $BH$». У якому кроці помилка?",
        "steps": [r"$\angle B = 60^\circ$, $\angle ABL = 30^\circ$", r"$\angle ABH = 90^\circ - 70^\circ = 20^\circ$", r"Відповідь: $30^\circ - 20^\circ = 10^\circ$"],
        "wrong": 1,
        "solution": r"$\angle ABH = 90^\circ - \angle A = 40^\circ$; відповідь $40 - 30 = 10^\circ$ випадково збіглася, але крок 2 хибний.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Висота $BH$ ділить кут $B$ трикутника $ABC$ на кути $30^\circ$ ($\angle ABH$) і $50^\circ$ ($\angle HBC$). Яка сторона трикутника найбільша?",
        "options": [(r"$AC$", True), (r"$AB$", False), (r"$BC$", False), (r"усі рівні", False), (r"не можна визначити", False)],
        "solution": r"$\angle A = 60^\circ$, $\angle C = 40^\circ$, $\angle B = 80^\circ$ — найбільший; проти нього — $AC$.",
    },
    {
        "type": "MULTI", "difficulty": 3, "skill": "ANALYZE",
        "text": r"У рівносторонньому $\triangle ABC$ $AM$ — медіана. Що правильно?",
        "options": [(r"$\angle BAM = 30^\circ$", True), (r"$AM \perp BC$", True), (r"$BM = \dfrac{AB}{2}$", True), (r"$AM = BM$", False)],
        "solution": r"Медіана — бісектриса і висота. $BM = \dfrac{BC}{2} = \dfrac{AB}{2}$; $AM \gt BM$ (катет проти більшого кута).",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "ANALYZE",
        "text": r"У рівносторонньому трикутнику зі стороною $10$ см висота ділить сторону на відрізки. Знайдіть довжину кожного (у см).",
        "answer": "5",
        "solution": r"Висота — медіана: $5$ см.",
    },

    # ===== БОСИ =====
    {
        "type": "SHORT", "difficulty": 4, "skill": "MODEL",
        "text": r"Медіана $BM$ ділить $\triangle ABC$ на два трикутники з периметрами $32$ см і $26$ см. Периметр $\triangle ABC$ — $48$ см. Знайдіть $BM$.",
        "answer": "5",
        "solution": r"$P_1 + P_2 = AB + BC + AC + 2BM = 48 + 2BM = 58$ ⟹ $BM = 5$ см.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "MODEL",
        "text": r"У $\triangle ABC$ бісектриса $AL$ дорівнює $LC$, а $\angle C = 32^\circ$. Знайдіть $\angle B$ (у градусах).",
        "answer": "84",
        "solution": r"$\triangle ALC$ рівнобедрений: $\angle LAC = 32^\circ$, $\angle A = 64^\circ$, $\angle B = 180 - 64 - 32 = 84^\circ$.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "SOLVE",
        "text": r"У $\triangle ABC$ $\angle C = 90^\circ$, $\angle A = 30^\circ$, бісектриса $BL = 8$ см. Знайдіть $AC$ (у см).",
        "answer": "12",
        "solution": r"$\angle B = 60^\circ$, $\angle CBL = 30^\circ$ ⟹ $CL = 4$. $\angle ABL = 30^\circ = \angle A$ ⟹ $AL = BL = 8$. $AC = 12$ см.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "SOLVE",
        "text": r"Висота рівнобедреного трикутника, проведена до бічної сторони, утворює з основою кут $24^\circ$. Знайдіть кут при вершині (у градусах).",
        "answer": "48",
        "solution": r"Кут при основі $90 - 24 = 66^\circ$; при вершині $180 - 132 = 48^\circ$.",
    },
    {
        "type": "TF", "difficulty": 4, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [(r"Якщо дві висоти трикутника рівні, то трикутник рівнобедрений", True), (r"Якщо дві медіани трикутника рівні, то трикутник рівнобедрений", True), (r"Будь-яка медіана менша за півсуму сторін, що виходять з тієї самої вершини", True), (r"Бісектриса завжди коротша за медіану, проведену з тієї самої вершини", False)],
        "solution": r"Рівні висоти — рівні прямокутні трикутники. Рівні медіани — теж рівнобедрений (доводиться подовженням медіан). Подвоєння медіани дає $2m \lt b + c$. У рівнобедреному з вершини бісектриса = медіана.",
    },
    {
        "type": "SHORT", "difficulty": 5, "skill": "SOLVE",
        "text": r"У $\triangle ABC$ бісектриса $BL$ і висота $AH$ перетинаються в точці $O$, $\angle AOB = 110^\circ$, $\angle C = 40^\circ$. Знайдіть $\angle ABC$ (у градусах).",
        "answer": "40",
        "solution": r"У $\triangle BOH$ ($\angle BHO = 90^\circ$): $\angle BOH = 180 - 110 = 70^\circ$ ⟹ $\angle OBH = 20^\circ$ ⟹ $\angle B = 40^\circ$.",
    },
    {
        "type": "SHORT", "difficulty": 5, "skill": "MODEL",
        "text": r"У $\triangle ABC$ медіана $AM$ перпендикулярна до бісектриси $BL$, $AB = 6$ см. Знайдіть $BC$ (у см).",
        "answer": "12",
        "solution": r"У $\triangle ABM$ бісектриса $BL$ є висотою ⟹ $\triangle ABM$ рівнобедрений: $BM = AB = 6$. $BC = 2BM = 12$ см.",
    },
]
