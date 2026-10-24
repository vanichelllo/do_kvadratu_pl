TOPIC_NAME = "1.6. Центральні та вписані кути"
COURSE = "Геометрія (7-9 класи)"
GRADE = "8 клас"

TASKS = [
    # ===== СХОДИНКА 1 =====
    # --- Моделювання ---
    {
        "type": "CHOICE", "difficulty": 1, "skill": "MODEL",
        "text": r"$O$ — центр кола, $A$, $B$, $C$ — точки кола. Який кут є вписаним?",
        "options": [(r"$\angle ACB$", True), (r"$\angle AOB$", False), (r"$\angle OAB$", False), (r"$\angle AOC$", False)],
        "hint": "Вершина вписаного кута лежить на колі, а сторони перетинають коло.",
        "solution": r"$\angle ACB$: вершина $C$ на колі, сторони $CA$ і $CB$ — хорди. $\angle AOB$, $\angle AOC$ — центральні.",
    },
    {
        "type": "TF", "difficulty": 1, "skill": "MODEL",
        "text": r"Правда чи ні?",
        "statements": [(r"Вершина центрального кута — центр кола", True), (r"Градусна міра всього кола — $180^\circ$", False),
                       (r"Дуга вимірюється центральним кутом, що на неї спирається", True)],
        "hint": "Скільки градусів у повному колі?",
        "solution": r"Повне коло — $360^\circ$. Решта — означення.",
    },
    {
        "type": "MATCH", "difficulty": 1, "skill": "MODEL",
        "text": r"Установіть відповідність між дугою (1–3) та вписаним кутом, що на неї спирається (А–Д).",
        "options": [r"А) $30^\circ$", r"Б) $45^\circ$", r"В) $90^\circ$", r"Г) $60^\circ$", r"Д) $120^\circ$"],
        "matches": [(r"1. $60^\circ$", r"А) $30^\circ$"), (r"2. $180^\circ$", r"В) $90^\circ$"), (r"3. $90^\circ$", r"Б) $45^\circ$")],
        "hint": "Вписаний кут — половина дуги.",
        "solution": r"$60 : 2 = 30$, $180 : 2 = 90$, $90 : 2 = 45$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "MODEL",
        "text": r"Коло поділили на $6$ рівних дуг. Скільки градусів у кожній дузі?",
        "answer": "60",
        "hint": "Усе коло — $360^\\circ$.",
        "solution": r"$360^\circ : 6 = 60^\circ$.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "MODEL",
        "text": r"Під яким кутом видно діаметр кола з будь-якої іншої точки кола?",
        "options": [(r"$90^\circ$", True), (r"$180^\circ$", False), (r"$45^\circ$", False), (r"залежить від точки", False)],
        "hint": "Діаметр стягує півколо — $180^\\circ$.",
        "solution": r"Вписаний кут, що спирається на півколо: $180^\circ : 2 = 90^\circ$.",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"Центральний кут $AOB = 84^\circ$. Знайдіть вписаний кут $ACB$, що спирається на дугу $AB$ (у градусах).",
        "answer": "42",
        "hint": "Вписаний — половина центрального на ту саму дугу.",
        "solution": r"$84^\circ : 2 = 42^\circ$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"Вписаний кут дорівнює $35^\circ$. Знайдіть центральний кут, що спирається на ту саму дугу (у градусах).",
        "answer": "70",
        "hint": "Центральний удвічі більший.",
        "solution": r"$2 \cdot 35^\circ = 70^\circ$.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "SOLVE",
        "text": r"Вписаний кут спирається на дугу $130^\circ$. Чому він дорівнює?",
        "options": [(r"$65^\circ$", True), (r"$130^\circ$", False), (r"$260^\circ$", False), (r"$50^\circ$", False)],
        "hint": "Половина дуги.",
        "solution": r"$130^\circ : 2 = 65^\circ$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"Дуга $AB$ дорівнює $100^\circ$. Знайдіть другу дугу $AB$ (що доповнює її до кола), у градусах.",
        "answer": "260",
        "hint": "Дві дуги разом — усе коло.",
        "solution": r"$360^\circ - 100^\circ = 260^\circ$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"$AB$ — діаметр, $C$ — точка кола, $\angle CAB = 40^\circ$. Знайдіть $\angle ABC$ (у градусах).",
        "answer": "50",
        "hint": "$\\angle ACB = 90^\\circ$.",
        "solution": r"$\angle ACB = 90^\circ$, $\angle ABC = 90^\circ - 40^\circ = 50^\circ$.",
    },
    # --- Аналіз ---
    {
        "type": "ERROR", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Оля шукала вписаний кут, що спирається на дугу $70^\circ$. У якому кроці помилка?",
        "steps": [r"Вписаний кут пов'язаний з дугою, на яку спирається", r"Він удвічі більший за дугу", r"Відповідь: $140^\circ$"],
        "wrong": 1,
        "hint": "Більший чи менший за дугу вписаний кут?",
        "solution": r"Вписаний кут — половина дуги: $35^\circ$.",
    },
    {
        "type": "TF", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [(r"Вписані кути, що спираються на одну дугу, рівні", True), (r"Вписаний кут може дорівнювати $200^\circ$", False),
                       (r"Центральний кут удвічі більший за вписаний, що спирається на ту саму дугу", True)],
        "hint": "Дуга менша за $360^\\circ$, тож вписаний кут менший за $180^\\circ$.",
        "solution": r"Вписаний кут — половина дуги ($\lt 360^\circ$), тому він менший за $180^\circ$.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Тарас: «Кут $ACB$ спирається на діаметр, тому дорівнює $180^\circ$». Чи правий він?",
        "options": [(r"Ні, кут дорівнює $90^\circ$", True), (r"Так", False), (r"Ні, $45^\circ$", False), (r"Ні, $360^\circ$", False)],
        "hint": "$180^\\circ$ — це дуга, а кут — її половина.",
        "solution": r"Діаметр стягує дугу $180^\circ$, вписаний кут — $90^\circ$.",
    },
    {
        "type": "GROUP", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Вписаний кут спирається на дугу. Яким він буде?",
        "groups": ["гострий", "прямий", "тупий"],
        "items": [(r"дуга $100^\circ$", 0), (r"дуга $180^\circ$", 1), (r"дуга $240^\circ$", 2), (r"дуга $170^\circ$", 0), (r"дуга $300^\circ$", 2), (r"півколо", 1)],
        "hint": "Порівняйте дугу з $180^\\circ$.",
        "solution": r"Кут: $50^\circ$, $90^\circ$, $120^\circ$, $85^\circ$, $150^\circ$, $90^\circ$.",
    },
    {
        "type": "MULTI", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Точки $C$ і $D$ лежать на колі по один бік від хорди $AB$. Що правильно?",
        "options": [(r"$\angle ACB = \angle ADB$", True), (r"обидва кути — половина однієї дуги", True), (r"$\angle ACB = 2\angle ADB$", False), (r"$\angle ACB + \angle ADB = 180^\circ$", False)],
        "hint": "Вони спираються на одну дугу.",
        "solution": r"Обидва кути спираються на ту саму дугу $AB$, тому рівні.",
    },

    # ===== СХОДИНКА 2 =====
    # --- Моделювання ---
    {
        "type": "FIELDS", "difficulty": 2, "skill": "MODEL",
        "text": r"Точки $A$, $B$, $C$ ділять коло на дуги $AB$, $BC$, $CA$ у відношенні $1 : 2 : 3$. Знайдіть ці дуги (у градусах).",
        "fields": [(r"$\buildrel\frown\over{AB}$:", "60"), (r"$\buildrel\frown\over{BC}$:", "120"), (r"$\buildrel\frown\over{CA}$:", "180")],
        "solution": r"$6x = 360^\circ$, $x = 60^\circ$: $60^\circ$, $120^\circ$, $180^\circ$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "MODEL",
        "text": r"Хорда $AB$ стягує дугу $80^\circ$. Під яким кутом видно $AB$ з точки $C$ на більшій дузі (у градусах)?",
        "answer": "40",
        "solution": r"Кут $ACB$ спирається на дугу $80^\circ$, що не містить $C$: $40^\circ$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "MODEL",
        "text": r"Хорда $AB$ стягує дугу $80^\circ$. Під яким кутом видно $AB$ з точки $C$ на меншій дузі (у градусах)?",
        "answer": "140",
        "solution": r"Тепер кут спирається на більшу дугу: $360 - 80 = 280^\circ$, кут $140^\circ$.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "MODEL",
        "text": r"Хорда дорівнює радіусу кола. Який центральний кут на неї спирається?",
        "options": [(r"$60^\circ$", True), (r"$30^\circ$", False), (r"$90^\circ$", False), (r"$120^\circ$", False)],
        "solution": r"$\triangle AOB$ має сторони $R$, $R$, $R$ — рівносторонній: $\angle AOB = 60^\circ$.",
    },
    {
        "type": "EXPR", "difficulty": 2, "skill": "MODEL",
        "text": r"Центральний кут дорівнює $x$ градусів. Запишіть вписаний кут, що спирається на іншу дугу з тими самими кінцями (вершина на меншій дузі).",
        "answer": "(360-x)/2", "vars": ["x"],
        "solution": r"Інша дуга — $360 - x$, вписаний кут — $\dfrac{360 - x}{2} = 180 - \dfrac{x}{2}$.",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"$O$ — центр кола, $\angle OAB = 20^\circ$ ($A$, $B$ — точки кола). Знайдіть центральний кут $AOB$ (у градусах).",
        "answer": "140",
        "solution": r"$OA = OB$, тож $\angle OBA = 20^\circ$, $\angle AOB = 180 - 40 = 140^\circ$.",
    },
    {
        "type": "FIELDS", "difficulty": 2, "skill": "SOLVE",
        "text": r"Дуги $AB$, $BC$, $CA$ кола дорівнюють $100^\circ$, $120^\circ$, $140^\circ$. Знайдіть кути $\triangle ABC$.",
        "fields": [(r"$\angle A$:", "60"), (r"$\angle B$:", "70"), (r"$\angle C$:", "50")],
        "solution": r"$\angle A = \dfrac{\buildrel\frown\over{BC}}{2} = 60^\circ$, $\angle B = \dfrac{\buildrel\frown\over{CA}}{2} = 70^\circ$, $\angle C = \dfrac{\buildrel\frown\over{AB}}{2} = 50^\circ$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"$AB$ — діаметр, $C$ — точка кола, $\angle ABC = 2\angle BAC$. Знайдіть $\angle BAC$ (у градусах).",
        "answer": "30",
        "solution": r"$\angle C = 90^\circ$: $x + 2x = 90^\circ$, $x = 30^\circ$.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "SOLVE",
        "text": r"Вписаний кут $ACB = 50^\circ$, $O$ — центр. Знайдіть $\angle OAB$.",
        "options": [(r"$40^\circ$", True), (r"$50^\circ$", False), (r"$80^\circ$", False), (r"$25^\circ$", False)],
        "solution": r"$\angle AOB = 100^\circ$; $\triangle AOB$ рівнобедрений: $\angle OAB = (180 - 100) : 2 = 40^\circ$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Точки $A$ і $B$ ділять коло на дуги, одна з яких на $40^\circ$ більша за іншу. Знайдіть вписаний кут, що спирається на меншу дугу (у градусах).",
        "answer": "80",
        "solution": r"$x + x + 40 = 360$, $x = 160^\circ$. Вписаний кут — $80^\circ$.",
    },
    # --- Аналіз ---
    {
        "type": "ERROR", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Тарас: «$\angle AOB = 120^\circ$, $C$ лежить на меншій дузі $AB$. Знайти $\angle ACB$». У якому кроці помилка?",
        "steps": [r"$\angle ACB$ спирається на дугу $AB$ величиною $120^\circ$", r"$\angle ACB = 120^\circ : 2$", r"$\angle ACB = 60^\circ$"],
        "wrong": 0,
        "solution": r"Точка $C$ на меншій дузі, тож кут спирається на більшу дугу $240^\circ$: $\angle ACB = 120^\circ$.",
    },
    {
        "type": "TF", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [(r"Якщо вписаний кут прямий, то він спирається на діаметр", True),
                       (r"Вписаний кут, що спирається на дугу, меншу за півколо, — гострий", True),
                       (r"Два вписані кути, що спираються на рівні хорди, завжди рівні", False)],
        "solution": r"Прямий кут — дуга $180^\circ$, тобто діаметр. Дуга $\lt 180^\circ$ — кут $\lt 90^\circ$. Рівна хорда стягує дві дуги — кути можуть бути $\alpha$ і $180^\circ - \alpha$.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Точки $C$ і $D$ лежать на колі по різні боки від хорди $AB$, $\angle ACB = 70^\circ$. Чому дорівнює $\angle ADB$?",
        "options": [(r"$110^\circ$", True), (r"$70^\circ$", False), (r"$140^\circ$", False), (r"$35^\circ$", False), (r"$20^\circ$", False)],
        "solution": r"Кути спираються на дві дуги, що разом $360^\circ$: $\angle ADB = 180^\circ - 70^\circ = 110^\circ$.",
    },
    {
        "type": "MULTI", "difficulty": 2, "skill": "ANALYZE",
        "text": r"$\angle AOB = 80^\circ$ ($O$ — центр). Якими можуть бути вписані кути з кінцями сторін в $A$ і $B$?",
        "options": [(r"$40^\circ$", True), (r"$140^\circ$", True), (r"$80^\circ$", False), (r"$160^\circ$", False), (r"$100^\circ$", False)],
        "solution": r"Вершина на більшій дузі — $40^\circ$, на меншій — $\dfrac{280^\circ}{2} = 140^\circ$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Вписаний кут на $36^\circ$ менший за центральний, що спирається на ту саму дугу. Знайдіть вписаний кут (у градусах).",
        "answer": "36",
        "solution": r"$2x - x = 36^\circ$, $x = 36^\circ$.",
    },

    # ===== СХОДИНКА 3 =====
    # --- Моделювання ---
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"Кути $\triangle ABC$ відносяться як $2 : 3 : 4$. Трикутник вписано в коло. Знайдіть найбільшу з дуг $AB$, $BC$, $CA$ (у градусах).",
        "answer": "160",
        "solution": r"Кути $40^\circ$, $60^\circ$, $80^\circ$. Дуги — подвоєні кути: $80^\circ$, $120^\circ$, $160^\circ$.",
    },
    {
        "type": "FIELDS", "difficulty": 3, "skill": "MODEL",
        "text": r"Хорда $AB$ ділить коло на дві дуги у відношенні $5 : 7$. Знайдіть вписані кути, що спираються на хорду $AB$ (меншу і більшу величини, у градусах).",
        "fields": [("Менший:", "75"), ("Більший:", "105")],
        "solution": r"Дуги: $150^\circ$ і $210^\circ$. Кути — половини: $75^\circ$ і $105^\circ$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"Сторона $AB$ трикутника, вписаного в коло, дорівнює радіусу. Знайдіть $\angle C$, якщо він гострий (у градусах).",
        "answer": "30",
        "solution": r"$\triangle AOB$ рівносторонній: $\angle AOB = 60^\circ$. Гострий $\angle C = 30^\circ$ (тупий був би $150^\circ$).",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "MODEL",
        "text": r"Точка $C$ на колі з діаметром $AB$, $\buildrel\frown\over{AC} = 70^\circ$ (дуга, що не містить $B$). Знайдіть $\angle CAB$.",
        "options": [(r"$55^\circ$", True), (r"$35^\circ$", False), (r"$70^\circ$", False), (r"$110^\circ$", False), (r"$20^\circ$", False)],
        "solution": r"Дуга $BC$ (без $A$) $= 180 - 70 = 110^\circ$. $\angle CAB$ спирається на неї: $55^\circ$.",
    },
    {
        "type": "EXPR", "difficulty": 3, "skill": "MODEL",
        "text": r"$O$ — центр кола, $\angle OAB = t$ градусів. Запишіть вписаний кут $ACB$ ($C$ на більшій дузі).",
        "answer": "90-t", "vars": ["t"],
        "solution": r"$\angle AOB = 180 - 2t$, $\angle ACB = \dfrac{180 - 2t}{2} = 90 - t$.",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Хорди $AC$ і $BD$ кола перетинаються в точці $M$. $\buildrel\frown\over{AB} = 60^\circ$, $\buildrel\frown\over{CD} = 100^\circ$ (дуги, що не містять інших точок). Знайдіть $\angle AMB$ (у градусах).",
        "answer": "80",
        "solution": r"$\angle ACB = 30^\circ$ (на дугу $AB$), $\angle DBC = 50^\circ$ (на дугу $CD$). $\angle AMB$ — зовнішній для $\triangle BMC$: $30 + 50 = 80^\circ$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"$AB$ — діаметр, $C$, $D$ — точки кола по різні боки від $AB$, $\angle CAB = 32^\circ$. Знайдіть $\angle ADC$ (у градусах).",
        "answer": "58",
        "solution": r"$\angle ABC = 90 - 32 = 58^\circ$. $\angle ADC$ і $\angle ABC$ спираються на дугу $AC$ (з одного боку) — рівні: $58^\circ$.",
    },
    {
        "type": "FIELDS", "difficulty": 3, "skill": "SOLVE",
        "text": r"Рівнобедрений $\triangle ABC$ ($AB = BC$) вписано в коло, $\angle B = 40^\circ$. Знайдіть дуги $AC$ і $AB$, що не містять третьої вершини (у градусах).",
        "fields": [(r"$\buildrel\frown\over{AC}$:", "80"), (r"$\buildrel\frown\over{AB}$:", "140")],
        "solution": r"$\buildrel\frown\over{AC} = 2\angle B = 80^\circ$. $\angle C = 70^\circ$, $\buildrel\frown\over{AB} = 140^\circ$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Вершини $\triangle ABC$ лежать на колі з центром $O$, $\angle BOC = 110^\circ$, $\angle AOC = 150^\circ$ (центр усередині трикутника). Знайдіть $\angle C$ (у градусах).",
        "answer": "50",
        "solution": r"$\angle AOB = 360 - 110 - 150 = 100^\circ$. $\angle C = 100 : 2 = 50^\circ$.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "SOLVE",
        "text": r"Вписаний $\angle ABC = 25^\circ$, $O$ — центр, $B$ і $O$ по один бік від $AC$. Знайдіть $\angle OCA$.",
        "options": [(r"$65^\circ$", True), (r"$25^\circ$", False), (r"$50^\circ$", False), (r"$40^\circ$", False), (r"$130^\circ$", False)],
        "solution": r"$\angle AOC = 50^\circ$, $\triangle AOC$ рівнобедрений: $\angle OCA = (180 - 50) : 2 = 65^\circ$.",
    },
    # --- Аналіз ---
    {
        "type": "TF", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Трикутник вписано в коло. Правда чи ні?",
        "statements": [(r"Якщо центр кола лежить на стороні, трикутник прямокутний", True),
                       (r"Якщо трикутник тупокутний, центр кола лежить поза ним", True),
                       (r"Більшій стороні відповідає більша дуга", True),
                       (r"Центр кола завжди всередині трикутника", False)],
        "solution": r"Центр на стороні — сторона є діаметром, протилежний кут $90^\circ$. Тупий кут спирається на дугу $\gt 180^\circ$ — центр зовні. Більший кут — більша дуга, а проти більшого кута більша сторона.",
    },
    {
        "type": "ERROR", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Оля: «Дуги $AB : BC : CA = 3 : 4 : 5$. Знайти $\angle A$». У якому кроці помилка?",
        "steps": [r"$12x = 360^\circ$, $x = 30^\circ$", r"Дуги: $90^\circ$, $120^\circ$, $150^\circ$", r"$\angle A$ спирається на дугу $AB$: $\angle A = 45^\circ$"],
        "wrong": 2,
        "solution": r"$\angle A$ спирається на дугу $BC$ (протилежну вершині $A$): $\angle A = 60^\circ$.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Скільки існує точок $C$ на колі, з яких діаметр $AB$ видно під кутом $90^\circ$?",
        "options": [(r"усі точки кола, крім $A$ і $B$", True), (r"лише дві", False), (r"одна", False), (r"жодної", False), (r"чотири", False)],
        "solution": r"Будь-який вписаний кут, що спирається на діаметр, прямий.",
    },
    {
        "type": "MULTI", "difficulty": 3, "skill": "ANALYZE",
        "text": r"У трикутник $ABC$, вписаний у коло, $\angle A = 80^\circ$. Що правильно?",
        "options": [(r"дуга $BC$ без точки $A$ — $160^\circ$", True), (r"центр кола і $A$ — по один бік від $BC$", True),
                    (r"$\angle BOC = 160^\circ$", True), (r"$\angle BOC = 40^\circ$", False), (r"сторона $BC$ — діаметр", False)],
        "solution": r"$\buildrel\frown\over{BC} = 160^\circ \lt 180^\circ$ — центр з того ж боку, що й $A$. $\angle BOC = 160^\circ$. Діаметр — лише при $90^\circ$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Діагоналі квадрата $ABCD$ — діаметри кола, описаного навколо нього. Під яким кутом видно сторону $AB$ з точки $M$ на дузі $CD$ (у градусах)?",
        "answer": "45",
        "solution": r"Кожна сторона стягує дугу $90^\circ$. $M$ на дузі $CD$ — кут спирається на дугу $AB$ $90^\circ$: $45^\circ$.",
    },

    # ===== БОСИ =====
    {
        "type": "SHORT", "difficulty": 4, "skill": "MODEL",
        "text": r"Точки $A$, $B$, $C$, $D$ послідовно лежать на колі й ділять його на дуги $AB : BC : CD : DA = 2 : 3 : 5 : 8$. Знайдіть кут між хордами $AC$ і $BD$ (менший, у градусах).",
        "answer": "70",
        "solution": r"$18x = 360^\circ$, $x = 20^\circ$: дуги $40^\circ$, $60^\circ$, $100^\circ$, $160^\circ$. Нехай $M$ — точка перетину. $\angle AMB$ — зовнішній для $\triangle BMC$: $\angle AMB = \angle ACB + \angle DBC = \dfrac{40}{2} + \dfrac{100}{2} = 70^\circ$.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "MODEL",
        "text": r"Сторона $AB$ вписаного $\triangle ABC$ стягує дугу $100^\circ$, сторона $BC$ — дугу $110^\circ$ (дуги, що не містять третьої вершини). Знайдіть найбільший кут трикутника (у градусах).",
        "answer": "75",
        "solution": r"Дуга $CA = 360 - 210 = 150^\circ$. Кути: $\angle C = 50^\circ$, $\angle A = 55^\circ$, $\angle B = 75^\circ$.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "SOLVE",
        "text": r"У колі з центром $O$ проведено діаметр $AB$ і хорду $AC$, $\angle BAC = 25^\circ$. Знайдіть $\angle OCB$ (у градусах).",
        "answer": "65",
        "solution": r"$\angle BOC = 2 \cdot 25 = 50^\circ$, $\triangle OBC$ рівнобедрений: $\angle OCB = (180 - 50) : 2 = 65^\circ$.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "SOLVE",
        "text": r"$ABCDEF$ — правильний шестикутник, вписаний у коло. Знайдіть $\angle ADB$ (у градусах).",
        "answer": "30",
        "solution": r"Кожна сторона стягує дугу $60^\circ$. $\angle ADB$ спирається на дугу $AB$: $30^\circ$.",
    },
    {
        "type": "TF", "difficulty": 4, "skill": "ANALYZE",
        "text": r"Точка $M$ лежить усередині кола з діаметром $AB$. Правда чи ні?",
        "statements": [(r"$\angle AMB \gt 90^\circ$", True), (r"Для точки поза колом $\angle AMB \lt 90^\circ$", True), (r"$\angle AMB$ може дорівнювати $90^\circ$", False)],
        "solution": r"Продовжимо $AM$ до перетину з колом у $K$: $\angle AKB = 90^\circ$, а $\angle AMB$ — зовнішній для $\triangle MKB$, тому більший за $90^\circ$. Для точки поза колом аналогічно кут менший.",
    },
    {
        "type": "SHORT", "difficulty": 5, "skill": "SOLVE",
        "text": r"Хорди $AB$ і $CD$ кола продовжили до перетину в точці $M$ поза колом. Дуги $AC$ і $BD$, що лежать між ними, дорівнюють $40^\circ$ і $120^\circ$ ($M$ ближче до $A$ і $C$). Знайдіть $\angle AMC$ (у градусах).",
        "answer": "40",
        "solution": r"$\angle ADC = 20^\circ$ (на дугу $AC$), $\angle DAB = 60^\circ$ (на дугу $BD$). $\angle DAB$ — зовнішній для $\triangle AMD$: $\angle AMD = 60 - 20 = 40^\circ$.",
    },
    {
        "type": "SHORT", "difficulty": 5, "skill": "ANALYZE",
        "text": r"Гострокутний $\triangle ABC$ вписано в коло з центром $O$, $\angle A = 70^\circ$. Знайдіть $\angle OBC$ (у градусах).",
        "answer": "20",
        "solution": r"$\angle BOC = 2 \cdot 70 = 140^\circ$ (центр усередині гострокутного трикутника). $\triangle BOC$ рівнобедрений: $\angle OBC = (180 - 140) : 2 = 20^\circ$.",
    },
]
