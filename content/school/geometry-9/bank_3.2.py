TOPIC_NAME = "3.2. Теорема синусів"
COURSE = "Геометрія (7-9 класи)"
GRADE = "9 клас"

TASKS = [
    # ==========================================
    # СХОДИНКА 1 — БАЗОВИЙ
    # ==========================================
    # --- Моделювання ---
    {
        "type": "CHOICE", "difficulty": 1, "skill": "MODEL",
        "text": r"Запишіть теорему синусів для сторін $BC$ і $AC$ трикутника $ABC$.",
        "options": [(r"$\dfrac{BC}{\sin A} = \dfrac{AC}{\sin B}$", True), (r"$\dfrac{BC}{\sin B} = \dfrac{AC}{\sin A}$", False),
                    (r"$\dfrac{BC}{\sin C} = \dfrac{AC}{\sin C}$", False), (r"$BC \cdot \sin A = AC \cdot \sin B$", False)],
        "solution": r"Кожна сторона ділиться на синус протилежного кута: $BC$ — проти $A$, $AC$ — проти $B$.",
    },
    {
        "type": "MATCH", "difficulty": 1, "skill": "MODEL",
        "text": r"$R$ — радіус кола, описаного навколо трикутника зі сторонами $a$, $b$, $c$ і протилежними кутами $\alpha$, $\beta$, $\gamma$. Установіть відповідність.",
        "options": [r"А) $2R$", r"Б) $2R\sin\beta$", r"В) $\dfrac{c}{2R}$", r"Г) $R\sin\beta$", r"Д) $\dfrac{2R}{c}$"],
        "matches": [(r"1. $\dfrac{a}{\sin\alpha}$", r"А) $2R$"), (r"2. $b$", r"Б) $2R\sin\beta$"), (r"3. $\sin\gamma$", r"В) $\dfrac{c}{2R}$")],
        "solution": r"$\frac{a}{\sin\alpha} = \frac{b}{\sin\beta} = \frac{c}{\sin\gamma} = 2R$, звідки $b = 2R\sin\beta$, $\sin\gamma = \frac{c}{2R}$.",
    },
    {
        "type": "TF", "difficulty": 1, "skill": "MODEL",
        "text": r"Правда чи ні?",
        "statements": [("Теорема синусів справджується і для тупокутного трикутника", True),
                       (r"$\dfrac{a}{\sin\alpha} = R$, де $R$ — радіус описаного кола", False),
                       (r"$\sin 150^\circ = \sin 30^\circ$", True)],
        "solution": r"Теорема справджується для будь-якого трикутника. Відношення дорівнює $2R$, а не $R$. $\sin(180^\circ - \alpha) = \sin\alpha$.",
    },
    {
        "type": "GROUP", "difficulty": 1, "skill": "MODEL",
        "text": r"Яку теорему зручно застосувати? Розподіліть задачі.",
        "groups": ["Теорема синусів", "Теорема косинусів"],
        "items": [("Дано сторону і два кути — знайти іншу сторону", 0), ("Дано дві сторони і кут між ними — знайти третю сторону", 1),
                  ("Дано три сторони — знайти кут", 1), ("Дано сторону і протилежний кут — знайти радіус описаного кола", 0),
                  ("Дано дві сторони і кут між ними — визначити вид трикутника", 1), ("Дано два кути і сторону між ними — знайти сторону", 0)],
        "solution": r"Синусів — коли є пара «сторона і протилежний кут» (або два кути, бо третій знаходимо). Косинусів — дві сторони і кут між ними, або три сторони.",
    },
    {
        "type": "FIELDS", "difficulty": 1, "skill": "MODEL",
        "text": r"У трикутнику сторона $a = 6$, протилежний кут $\alpha = 30^\circ$. Знайдіть:",
        "fields": [(r"$\dfrac{a}{\sin\alpha} =$", "12"), (r"$R =$", "6")],
        "solution": r"$\frac{6}{\frac12} = 12 = 2R$, отже $R = 6$.",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"У трикутнику $ABC$: $BC = 10$, $\angle A = 30^\circ$. Знайдіть радіус описаного кола.",
        "answer": "10",
        "solution": r"$2R = \frac{BC}{\sin A} = \frac{10}{\frac12} = 20$, $R = 10$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"У трикутнику $ABC$: $\angle A = 45^\circ$, $\angle B = 30^\circ$, $BC = 6\sqrt2$. Знайдіть $AC$.",
        "answer": "6",
        "solution": r"$\frac{AC}{\sin B} = \frac{BC}{\sin A}$: $AC = \frac{6\sqrt2 \cdot \frac12}{\frac{\sqrt2}{2}} = 6$.",
    },
    {
        "type": "FIELDS", "difficulty": 1, "skill": "SOLVE",
        "text": r"Радіус кола, описаного навколо трикутника, дорівнює $4$. Знайдіть сторону, що лежить проти кута:",
        "fields": [(r"$30^\circ$:", "4"), (r"$90^\circ$:", "8")],
        "solution": r"$a = 2R\sin\alpha$: $8 \cdot \frac12 = 4$; $\;8 \cdot 1 = 8$.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "SOLVE",
        "text": r"У трикутнику $ABC$: $\angle A = 60^\circ$, $\angle B = 45^\circ$, $BC = 3\sqrt6$. Знайдіть $AC$.",
        "options": [(r"$6$", True), (r"$9$", False), (r"$3\sqrt3$", False), (r"$4\sqrt3$", False)],
        "solution": r"$AC = \frac{BC \cdot \sin B}{\sin A} = \frac{3\sqrt6 \cdot \frac{\sqrt2}{2}}{\frac{\sqrt3}{2}} = 3\sqrt6 \cdot \frac{\sqrt2}{\sqrt3} = 3 \cdot 2 = 6$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"Радіус описаного кола дорівнює $5$, а сторона трикутника — $5$. Знайдіть (у градусах) гострий кут, що лежить проти цієї сторони.",
        "answer": "30",
        "solution": r"$\sin\alpha = \frac{a}{2R} = \frac{5}{10} = \frac12$. Гострий кут — $30^\circ$ (тупий був би $150^\circ$).",
    },
    # --- Аналіз результатів ---
    {
        "type": "ERROR", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Сторона трикутника $8$, протилежний кут $30^\circ$. Учень шукав радіус описаного кола. У якому кроці помилка?",
        "steps": [r"$\dfrac{8}{\sin 30^\circ} = 2R$", r"$\dfrac{8}{\frac12} = 16$", r"$R = 16$"],
        "wrong": 2,
        "solution": r"$16 = 2R$ — це діаметр, отже $R = 8$.",
    },
    {
        "type": "TF", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [("Проти більшої сторони трикутника лежить більший кут", True),
                       (r"Якщо $\sin\alpha = \sin\beta$, то обов'язково $\alpha = \beta$", False),
                       (r"Синус будь-якого кута трикутника додатний", True)],
        "solution": r"$\sin\alpha = \sin\beta$ і при $\beta = 180^\circ - \alpha$. Кути трикутника від $0^\circ$ до $180^\circ$ — синус додатний.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Петро: «$\sin 120^\circ = -\dfrac{\sqrt3}{2}$». Чи правий він?",
        "options": [(r"Ні: $\sin 120^\circ = \sin 60^\circ = \dfrac{\sqrt3}{2}$", True), ("Так", False),
                    (r"Ні: $\sin 120^\circ = \dfrac12$", False), (r"Ні: $\sin 120^\circ = -\dfrac12$", False)],
        "solution": r"$\sin(180^\circ - \alpha) = \sin\alpha$, тож синус тупого кута додатний. Від'ємний — косинус: $\cos 120^\circ = -\frac12$.",
    },
    {
        "type": "MULTI", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Для яких кутів $\varphi$ виконується $\sin\varphi = \frac12$?",
        "options": [(r"$30^\circ$", True), (r"$150^\circ$", True), (r"$60^\circ$", False), (r"$120^\circ$", False), (r"$45^\circ$", False)],
        "solution": r"$\sin 30^\circ = \frac12$ і $\sin 150^\circ = \sin 30^\circ$. $\sin 60^\circ = \sin 120^\circ = \frac{\sqrt3}{2}$.",
    },
    {
        "type": "ORDER", "difficulty": 1, "skill": "ANALYZE",
        "text": r"У трикутнику $ABC$: $\angle A = 40^\circ$, $\angle B = 60^\circ$, $\angle C = 80^\circ$. Розташуйте сторони від найменшої до найбільшої.",
        "items": [r"$BC$", r"$AC$", r"$AB$"],
        "solution": r"Більший кут — проти більшої сторони: $BC$ — проти $40^\circ$, $AC$ — проти $60^\circ$, $AB$ — проти $80^\circ$.",
    },

    # ==========================================
    # СХОДИНКА 2 — СЕРЕДНІЙ
    # ==========================================
    # --- Моделювання ---
    {
        "type": "SHORT", "difficulty": 2, "skill": "MODEL",
        "text": r"Щоб знайти відстань до човна $C$, на березі відміряли $AB = 40$ м і виміряли кути: $\angle A = 30^\circ$, $\angle B = 120^\circ$. Знайдіть відстань $BC$ (у метрах).",
        "answer": "40",
        "solution": r"$\angle C = 180^\circ - 30^\circ - 120^\circ = 30^\circ$. $\frac{BC}{\sin 30^\circ} = \frac{AB}{\sin 30^\circ}$, тож $BC = AB = 40$ м (трикутник рівнобедрений).",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "MODEL",
        "text": r"Знайдіть радіус кола, описаного навколо правильного трикутника зі стороною $6$.",
        "options": [(r"$2\sqrt3$", True), (r"$3$", False), (r"$6$", False), (r"$3\sqrt3$", False), (r"$\sqrt3$", False)],
        "solution": r"$2R = \frac{6}{\sin 60^\circ} = \frac{12}{\sqrt3} = 4\sqrt3$, $R = 2\sqrt3$.",
    },
    {
        "type": "TF", "difficulty": 2, "skill": "MODEL",
        "text": r"Правда чи ні?",
        "statements": [("Щоб знайти радіус описаного кола, досить знати одну сторону і протилежний їй кут", True),
                       ("Щоб знайти радіус описаного кола, досить знати дві сторони", False),
                       (r"У прямокутному трикутнику $2R$ дорівнює гіпотенузі", True)],
        "solution": r"$2R = \frac{a}{\sin\alpha}$. Дві сторони без кута трикутник не визначають. Гіпотенуза лежить проти $90^\circ$: $\frac{c}{\sin 90^\circ} = c$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "MODEL",
        "text": r"У трикутнику кути $\alpha = 30^\circ$ і $\beta = 90^\circ$. Знайдіть відношення $\dfrac{a}{b}$ протилежних їм сторін.",
        "answer": "0,5",
        "solution": r"$\frac{a}{b} = \frac{\sin\alpha}{\sin\beta} = \frac{\frac12}{1} = 0{,}5$. (Катет проти $30^\circ$ — половина гіпотенузи.)",
    },
    {
        "type": "MATCH", "difficulty": 2, "skill": "MODEL",
        "text": r"Кути трикутника — $30^\circ$, $60^\circ$, $90^\circ$, радіус описаного кола $R = 5$. Установіть відповідність між стороною (1–3) та її довжиною (А–Д).",
        "options": [r"А) $5$", r"Б) $5\sqrt3$", r"В) $10$", r"Г) $2{,}5$", r"Д) $10\sqrt3$"],
        "matches": [(r"1. проти кута $30^\circ$", r"А) $5$"), (r"2. проти кута $60^\circ$", r"Б) $5\sqrt3$"), (r"3. проти кута $90^\circ$", r"В) $10$")],
        "solution": r"$a = 2R\sin\alpha = 10\sin\alpha$: $10 \cdot \frac12 = 5$; $10 \cdot \frac{\sqrt3}{2} = 5\sqrt3$; $10 \cdot 1 = 10$.",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"У трикутнику $ABC$: $\angle A = 45^\circ$, $\angle B = 60^\circ$, $AC = 2\sqrt6$. Знайдіть $BC$.",
        "answer": "4",
        "solution": r"$\frac{BC}{\sin A} = \frac{AC}{\sin B}$: $BC = \frac{2\sqrt6 \cdot \frac{\sqrt2}{2}}{\frac{\sqrt3}{2}} = 2\sqrt6 \cdot \frac{\sqrt2}{\sqrt3} = 4$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Радіус кола, описаного навколо трикутника $ABC$, дорівнює $6$, $\angle C = 150^\circ$. Знайдіть $AB$.",
        "answer": "6",
        "solution": r"$AB = 2R\sin C = 12 \cdot \sin 150^\circ = 12 \cdot \frac12 = 6$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"У трикутнику $ABC$: $BC = 6\sqrt3$, $AC = 6$, $\angle A = 60^\circ$. Знайдіть $\angle B$ (у градусах).",
        "answer": "30",
        "solution": r"$\sin B = \frac{AC \cdot \sin A}{BC} = \frac{6 \cdot \frac{\sqrt3}{2}}{6\sqrt3} = \frac12$: $30^\circ$ або $150^\circ$. $AC \lt BC$, тож $\angle B \lt \angle A = 60^\circ$: $\angle B = 30^\circ$.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "SOLVE",
        "text": r"Сторона трикутника дорівнює $10$, а протилежний кут — $45^\circ$. Знайдіть радіус описаного кола.",
        "options": [(r"$5\sqrt2$", True), (r"$10\sqrt2$", False), (r"$10$", False), (r"$5$", False)],
        "solution": r"$2R = \frac{10}{\frac{\sqrt2}{2}} = 10\sqrt2$, $R = 5\sqrt2$. ($10\sqrt2$ — це діаметр.)",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Радіус кола, описаного навколо трикутника $ABC$, дорівнює $3$, $\angle A = 150^\circ$. Знайдіть $BC$.",
        "answer": "3",
        "solution": r"$BC = 2R\sin A = 6 \cdot \frac12 = 3$.",
    },
    # --- Аналіз результатів ---
    {
        "type": "ERROR", "difficulty": 2, "skill": "ANALYZE",
        "text": r"У трикутнику $ABC$: $BC = 8$, $\angle A = 30^\circ$, $\angle B = 45^\circ$. Учень шукав $AC$. У якому кроці помилка?",
        "steps": [r"$\dfrac{AC}{\sin A} = \dfrac{BC}{\sin B}$", r"$AC = \dfrac{8 \cdot \frac12}{\frac{\sqrt2}{2}}$", r"$AC = 4\sqrt2$"],
        "wrong": 0,
        "solution": r"$AC$ лежить проти кута $B$, а $BC$ — проти $A$: $\frac{AC}{\sin B} = \frac{BC}{\sin A}$, $AC = \frac{8 \cdot \frac{\sqrt2}{2}}{\frac12} = 8\sqrt2$.",
    },
    {
        "type": "TF", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Чи правильний висновок?",
        "statements": [(r"$\dfrac{a}{\sin\alpha} = 12$, отже $R = 6$", True),
                       (r"$\sin\beta = 0{,}5$, отже $\beta = 30^\circ$", False),
                       (r"Сторона проти кута $90^\circ$ дорівнює $2R$", True)],
        "solution": r"$2R = 12$. Синус $0{,}5$ має і кут $150^\circ$ — висновок неповний. $a = 2R\sin 90^\circ = 2R$.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "ANALYZE",
        "text": r"$BC = 3$, $AC = 6$, $\angle A = 30^\circ$. Скільки існує трикутників $ABC$ з такими даними?",
        "options": [("Один", True), ("Жодного", False), ("Два", False), ("Безліч", False)],
        "solution": r"$\sin B = \frac{6 \cdot \frac12}{3} = 1$, $\angle B = 90^\circ$ — єдиний кут. Трикутник один (прямокутний).",
    },
    {
        "type": "MULTI", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Які рівності правильні для будь-якого трикутника $ABC$ з радіусом описаного кола $R$?",
        "options": [(r"$\dfrac{BC}{\sin A} = \dfrac{AC}{\sin B}$", True), (r"$BC = 2R\sin A$", True), (r"$BC \cdot \sin B = AC \cdot \sin A$", True),
                    (r"$\dfrac{AB}{\sin A} = \dfrac{BC}{\sin C}$", False), (r"$\dfrac{BC}{\sin B} = 2R$", False)],
        "solution": r"Сторона ділиться на синус протилежного кута. Третя рівність — перехресне множення першої. У хибних сторону поділено на синус прилеглого кута.",
    },
    {
        "type": "TF", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [(r"У трикутнику з кутами $40^\circ$, $60^\circ$, $80^\circ$ найбільша сторона лежить проти кута $80^\circ$", True),
                       (r"Якщо $a \gt b$, то $\alpha \gt \beta$", True),
                       (r"Якщо $\alpha = 2\beta$, то $a = 2b$", False)],
        "solution": r"Більша сторона — проти більшого кута, і навпаки. Але сторони пропорційні синусам, а не кутам: при $\beta = 30^\circ$, $\alpha = 60^\circ$ $\frac{a}{b} = \sqrt3$.",
    },

    # ==========================================
    # СХОДИНКА 3 — ПІДВИЩЕНИЙ
    # ==========================================
    # --- Моделювання ---
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"Основа рівнобедреного трикутника дорівнює $6\sqrt3$, кут при вершині — $120^\circ$. Знайдіть радіус описаного кола.",
        "answer": "6",
        "solution": r"Основа лежить проти кута $120^\circ$: $2R = \frac{6\sqrt3}{\frac{\sqrt3}{2}} = 12$, $R = 6$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"Корабель іде прямим курсом. З точки $A$ маяк $M$ видно під кутом $30^\circ$ до курсу, а через $10$ км, з точки $B$, — під кутом $60^\circ$ до курсу. Знайдіть відстань $BM$ (у км).",
        "answer": "10",
        "solution": r"У $\triangle ABM$: $\angle A = 30^\circ$, $\angle ABM = 180^\circ - 60^\circ = 120^\circ$, $\angle M = 30^\circ$. Кути при $A$ і $M$ рівні, тож $BM = AB = 10$ км (і за теоремою синусів $\frac{BM}{\sin 30^\circ} = \frac{AB}{\sin 30^\circ}$).",
    },
    {
        "type": "MATCH", "difficulty": 3, "skill": "MODEL",
        "text": r"Установіть відповідність між даними трикутника (1–3) та радіусом описаного кола (А–Д).",
        "options": [r"А) $6$", r"Б) $3$", r"В) $4$", r"Г) $12$", r"Д) $2\sqrt3$"],
        "matches": [(r"1. $a = 6$, $\alpha = 30^\circ$", r"А) $6$"), (r"2. $a = 6$, $\alpha = 90^\circ$", r"Б) $3$"),
                    (r"3. $a = 4\sqrt3$, $\alpha = 120^\circ$", r"В) $4$")],
        "solution": r"$R = \frac{a}{2\sin\alpha}$: $\frac{6}{1} = 6$; $\frac{6}{2} = 3$; $\frac{4\sqrt3}{\sqrt3} = 4$.",
    },
    {
        "type": "TF", "difficulty": 3, "skill": "MODEL",
        "text": r"Треба знайти відстані від точок $A$ і $B$ до недоступної точки $C$. Правда чи ні?",
        "statements": [(r"Досить виміряти відрізок $AB$ і кути $CAB$ та $CBA$", True),
                       ("Досить виміряти лише кути трикутника $ABC$", False),
                       (r"Якщо обидва виміряні кути по $45^\circ$, то $C$ лежить на серединному перпендикулярі до $AB$", True)],
        "solution": r"Сторона і два кути визначають трикутник. Самі кути визначають лише форму — розмір невідомий. При рівних кутах $CA = CB$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"Знайдіть сторону правильного трикутника, вписаного в коло радіуса $4\sqrt3$.",
        "answer": "12",
        "solution": r"$a = 2R\sin 60^\circ = 8\sqrt3 \cdot \frac{\sqrt3}{2} = 12$.",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"У трикутнику $ABC$: $AB = 8\sqrt2$, $\angle C = 135^\circ$. Знайдіть радіус описаного кола.",
        "answer": "8",
        "solution": r"$\sin 135^\circ = \frac{\sqrt2}{2}$. $2R = \frac{8\sqrt2}{\frac{\sqrt2}{2}} = 16$, $R = 8$.",
    },
    {
        "type": "FIELDS", "difficulty": 3, "skill": "SOLVE",
        "text": r"У трикутнику $ABC$: $BC = 6$, $AC = 6\sqrt3$, $\angle A = 30^\circ$. Знайдіть усі можливі значення $\angle B$ (у градусах).",
        "fields": [(r"$\angle B_1 =$", "60"), (r"$\angle B_2 =$", "120")], "unordered": True,
        "solution": r"$\sin B = \frac{6\sqrt3 \cdot \frac12}{6} = \frac{\sqrt3}{2}$: $60^\circ$ або $120^\circ$. $AC \gt BC$, тож $\angle B \gt 30^\circ$ в обох випадках, і $30^\circ + 120^\circ \lt 180^\circ$. Обидва трикутники існують.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"У трикутнику $ABC$: $\angle A = 45^\circ$, $\angle C = 105^\circ$, $BC = 4\sqrt2$. Знайдіть $AC$.",
        "answer": "4",
        "solution": r"$\angle B = 180^\circ - 45^\circ - 105^\circ = 30^\circ$. $AC = \frac{BC \cdot \sin B}{\sin A} = \frac{4\sqrt2 \cdot \frac12}{\frac{\sqrt2}{2}} = 4$.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "SOLVE",
        "text": r"У трикутнику $ABC$: $\angle A = 120^\circ$, $BC = 6\sqrt3$. Знайдіть радіус описаного кола.",
        "options": [(r"$6$", True), (r"$12$", False), (r"$3\sqrt3$", False), (r"$9$", False), (r"$6\sqrt3$", False)],
        "solution": r"$2R = \frac{6\sqrt3}{\sin 120^\circ} = \frac{6\sqrt3}{\frac{\sqrt3}{2}} = 12$, $R = 6$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"У трикутнику $a : b = \sqrt2 : 1$, $\beta = 30^\circ$, кут $\alpha$ гострий. Знайдіть $\alpha$ (у градусах).",
        "answer": "45",
        "solution": r"$\sin\alpha = \frac{a}{b}\sin\beta = \sqrt2 \cdot \frac12 = \frac{\sqrt2}{2}$; гострий кут — $45^\circ$.",
    },
    # --- Аналіз результатів ---
    {
        "type": "ERROR", "difficulty": 3, "skill": "ANALYZE",
        "text": r"У трикутнику $ABC$: $AC = 6$, $BC = 6\sqrt3$, $\angle A = 60^\circ$. Учень шукав $\angle B$. У якому кроці помилка?",
        "steps": [r"$\sin B = \dfrac{AC \cdot \sin A}{BC} = \dfrac12$", r"$\angle B = 30^\circ$ або $\angle B = 150^\circ$", r"Відповідь: $30^\circ$ або $150^\circ$"],
        "wrong": 2,
        "solution": r"$150^\circ$ не підходить: $60^\circ + 150^\circ \gt 180^\circ$ (та й проти меншої сторони $AC$ кут менший за $60^\circ$). Відповідь: $30^\circ$.",
    },
    {
        "type": "GROUP", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Дано $a$, $b$ і кут $\alpha$ проти сторони $a$. Скільки існує трикутників?",
        "groups": ["Жодного", "Один", "Два"],
        "items": [(r"$a = 2$, $b = 6$, $\alpha = 30^\circ$", 0), (r"$a = 3$, $b = 6$, $\alpha = 30^\circ$", 1), (r"$a = 4$, $b = 6$, $\alpha = 30^\circ$", 2),
                  (r"$a = 8$, $b = 6$, $\alpha = 30^\circ$", 1), (r"$a = 6$, $b = 6$, $\alpha = 30^\circ$", 1), (r"$a = 5$, $b = 8$, $\alpha = 30^\circ$", 2)],
        "solution": r"$\sin\beta = \frac{b\sin\alpha}{a} = \frac{b}{2a}$: $1{,}5$ — немає; $1$ — один ($90^\circ$); $0{,}75$ і $0{,}8$ при $b \gt a$ — два ($\beta$ і $180^\circ - \beta$, обидва більші за $30^\circ$); при $b \le a$ кут $\beta \le \alpha$, тож лише гострий — один.",
    },
    {
        "type": "TF", "difficulty": 3, "skill": "ANALYZE",
        "text": r"$R$ — радіус описаного кола, $a$ — сторона, $\alpha$ — протилежний кут. Чи правильний висновок?",
        "statements": [(r"$a = 2R$, отже $\alpha = 90^\circ$", True), (r"$a = R$, отже $\alpha = 30^\circ$", False),
                       (r"$\frac{a}{\sin\alpha} = \frac{b}{\sin\beta}$ і $a = b$, отже $\alpha = \beta$", True)],
        "solution": r"$\sin\alpha = 1$ — лише $90^\circ$. $\sin\alpha = \frac12$ — $30^\circ$ або $150^\circ$. При $a = b$ $\sin\alpha = \sin\beta$; $\alpha + \beta = 180^\circ$ неможливо, тож $\alpha = \beta$.",
    },
    {
        "type": "MULTI", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Радіус кола, описаного навколо трикутника, дорівнює $5$. Якою може бути довжина сторони трикутника?",
        "options": [(r"$10$", True), (r"$5$", True), (r"$8$", True), (r"$12$", False), (r"$11$", False)],
        "solution": r"$a = 10\sin\alpha$, а $0 \lt \sin\alpha \le 1$: сторона може бути будь-якою з $(0;\,10]$. $11$ і $12$ — більші за діаметр.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "ANALYZE",
        "text": r"У трикутнику $ABC$: $\angle A = 30^\circ$, $BC = 5$, $AB = 10$. Знайдіть $\angle C$.",
        "options": [(r"$90^\circ$", True), (r"$30^\circ$", False), (r"$60^\circ$", False), (r"$150^\circ$", False), (r"$45^\circ$", False)],
        "solution": r"$\sin C = \frac{AB \cdot \sin A}{BC} = \frac{10 \cdot \frac12}{5} = 1$, $\angle C = 90^\circ$. (Катет $BC$ проти $30^\circ$ — половина гіпотенузи $AB$.)",
    },

    # ==========================================
    # БОСИ
    # ==========================================
    {
        "type": "SHORT", "difficulty": 4, "skill": "MODEL",
        "text": r"Сторони трикутника — $5$, $5$ і $5\sqrt3$. Знайдіть радіус описаного кола.",
        "answer": "5",
        "solution": r"Найбільший кут (проти $5\sqrt3$) за теоремою косинусів: $\cos\gamma = \frac{25 + 25 - 75}{50} = -\frac12$, $\gamma = 120^\circ$. Тоді $2R = \frac{5\sqrt3}{\frac{\sqrt3}{2}} = 10$, $R = 5$.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "MODEL",
        "text": r"У трикутнику $ABC$: $AB = 6$, $\angle C = 30^\circ$. Яку найбільшу довжину може мати сторона $AC$?",
        "answer": "12",
        "solution": r"$2R = \frac{AB}{\sin C} = 12$. $AC = 2R\sin B = 12\sin B \le 12$, і $12$ досягається при $\angle B = 90^\circ$ (тоді $\angle A = 60^\circ$ — трикутник існує).",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "SOLVE",
        "text": r"Діагональ $BD$ паралелограма $ABCD$ дорівнює $6$, а $\angle A = 150^\circ$. Знайдіть радіус кола, описаного навколо трикутника $ABD$.",
        "answer": "6",
        "solution": r"У $\triangle ABD$ сторона $BD$ лежить проти кута $A$: $2R = \frac{6}{\sin 150^\circ} = \frac{6}{\frac12} = 12$, $R = 6$.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "SOLVE",
        "text": r"Кути трикутника відносяться як $1 : 2 : 3$, а найбільша сторона дорівнює $12$. Знайдіть найменшу сторону.",
        "answer": "6",
        "solution": r"Кути $30^\circ$, $60^\circ$, $90^\circ$. $\frac{a}{\sin 30^\circ} = \frac{12}{\sin 90^\circ}$, $a = 6$.",
    },
    {
        "type": "TF", "difficulty": 4, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [(r"Сторона, що лежить проти кута $30^\circ$, дорівнює радіусу описаного кола", True),
                       ("Сторона трикутника не може бути більшою за діаметр описаного кола", True),
                       (r"Якщо два кути трикутника — $30^\circ$ і $45^\circ$, то протилежні їм сторони відносяться як $1 : \sqrt2$", True),
                       (r"Умова $\sin\beta = 0{,}9$ завжди дає два різні трикутники", False)],
        "solution": r"$a = 2R \cdot \frac12 = R$. $a = 2R\sin\alpha \le 2R$. $\frac{\sin 30^\circ}{\sin 45^\circ} = \frac{1}{\sqrt2}$. Тупий кут може не вміститися (якщо вже є великий кут або сторона $b$ менша) — тоді трикутник один.",
    },

    # ==========================================
    # УЛЬТРА-БОСИ
    # ==========================================
    {
        "type": "SHORT", "difficulty": 5, "skill": "SOLVE",
        "text": r"Знайдіть радіус кола, описаного навколо трикутника зі сторонами $13$, $14$, $15$.",
        "answer": "65/8",
        "solution": r"Кут проти сторони $14$: $\cos\beta = \frac{169 + 225 - 196}{2 \cdot 13 \cdot 15} = \frac{198}{390} = \frac{33}{65}$. $\sin\beta = \sqrt{1 - \frac{1089}{4225}} = \frac{56}{65}$. $2R = \frac{14}{\frac{56}{65}} = \frac{65}{4}$, $R = \frac{65}{8} = 8{,}125$.",
    },
    {
        "type": "CHOICE", "difficulty": 5, "skill": "MODEL",
        "text": r"Вершину вежі з точки $A$ видно під кутом $30^\circ$ до горизонту, а з точки $B$, на $50$ м ближчої до вежі, — під кутом $60^\circ$. Знайдіть висоту вежі.",
        "options": [(r"$25\sqrt3$ м", True), (r"$50$ м", False), (r"$25$ м", False), (r"$50\sqrt3$ м", False), (r"$100$ м", False)],
        "solution": r"$T$ — вершина. У $\triangle ABT$: $\angle A = 30^\circ$, $\angle ABT = 180^\circ - 60^\circ = 120^\circ$, $\angle T = 30^\circ$, тож $BT = AB = 50$ м. Висота — катет проти $60^\circ$ у прямокутному трикутнику з гіпотенузою $BT$: $h = 50\sin 60^\circ = 25\sqrt3$ м.",
    },
]
