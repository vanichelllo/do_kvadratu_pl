TOPIC_NAME = "2.2. Перпендикулярні прямі"
COURSE = "Геометрія (7-9 класи)"
GRADE = "7 клас"

TASKS = [
    # ==========================================
    # СХОДИНКА 1 — БАЗОВИЙ
    # ==========================================
    # --- Моделювання ---
    {
        "type": "GROUP", "difficulty": 1, "skill": "MODEL",
        "text": r"Чи перпендикулярні ці прямі (або промені)? Розклади на групи.",
        "groups": ["Перпендикулярні", "Не перпендикулярні"],
        "items": [("Сусідні краї аркуша паперу", 0), ("Стрілки годинника о 3:00", 0),
                  ("Стрілки годинника о 6:00", 1), ("Стрілки годинника о 2:00", 1),
                  ("Горизонтальна й вертикальна лінії зошита в клітинку", 0),
                  (r"Дві дороги, що перетинаються під кутом $60^\circ$", 1)],
        "hint": r"Перпендикулярні — ті, що перетинаються під прямим кутом ($90^\circ$).",
        "solution": r"Прямий кут утворюють сусідні краї аркуша, лінії зошита і стрілки о 3:00 ($3 \cdot 30^\circ = 90^\circ$). "
                    r"О 6:00 стрілки утворюють $180^\circ$, о 2:00 — $60^\circ$; дороги — $60^\circ$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "MODEL",
        "text": r"На малюнку $AH \perp a$. Яка відстань від точки $A$ до прямої $a$ (у см)?",
        "svg_code": '<svg xmlns="http://www.w3.org/2000/svg" width="320" height="180" viewBox="0 0 320 180" fill="none" stroke="currentColor" stroke-width="2" font-family="sans-serif" font-size="16"><line x1="10" y1="140" x2="310" y2="140"/><text x="300" y="129" fill="currentColor" stroke="none" text-anchor="middle" font-style="italic">a</text><line x1="180" y1="40" x2="180" y2="140"/><line x1="180" y1="40" x2="255" y2="140"/><line x1="180" y1="40" x2="36.4" y2="140"/><path d="M180 128 L168 128 L168 140" stroke-width="1.5"/><circle cx="180" cy="40" r="3.5" fill="currentColor" stroke="none"/><circle cx="180" cy="140" r="3.5" fill="currentColor" stroke="none"/><circle cx="255" cy="140" r="3.5" fill="currentColor" stroke="none"/><circle cx="36.4" cy="140" r="3.5" fill="currentColor" stroke="none"/><text x="180" y="29" fill="currentColor" stroke="none" text-anchor="middle" font-style="italic">A</text><text x="168" y="163" fill="currentColor" stroke="none" text-anchor="middle" font-style="italic">H</text><text x="255" y="163" fill="currentColor" stroke="none" text-anchor="middle" font-style="italic">M</text><text x="36.4" y="163" fill="currentColor" stroke="none" text-anchor="middle" font-style="italic">K</text><text x="156" y="95" fill="currentColor" stroke="none" text-anchor="middle" font-size="14">4 см</text><text x="243.5" y="89" fill="currentColor" stroke="none" text-anchor="middle" font-size="14">5 см</text><text x="88.2" y="85" fill="currentColor" stroke="none" text-anchor="middle" font-size="14">7 см</text></svg>',
        "answer": "4",
        "hint": r"Відстань від точки до прямої — довжина перпендикуляра.",
        "solution": r"Перпендикуляр з $A$ до $a$ — відрізок $AH$, тож відстань дорівнює $AH = 4$ см. "
                    r"$AM$ і $AK$ не перпендикулярні до $a$ — вони довші.",
    },
    {
        "type": "ORDER", "difficulty": 1, "skill": "MODEL",
        "text": r"Треба знайти відстань від точки $A$ до прямої $a$ за допомогою косинця й лінійки. Розташуй кроки в правильному порядку.",
        "items": [r"Прикласти косинець однією стороною прямого кута до прямої $a$",
                  r"Пересунути косинець уздовж $a$, доки друга сторона прямого кута не пройде через точку $A$",
                  r"Провести вздовж цієї сторони пряму $b$",
                  r"Позначити точку $H$ перетину $b$ і $a$ та виміряти $AH$ лінійкою"],
        "hint": r"Спершу косинець прикладають до прямої, а вимірюють наприкінці.",
        "solution": r"Косинець — на пряму $a$, пересунути до точки $A$, провести $b \perp a$, "
                    r"знайти основу $H$ і виміряти перпендикуляр $AH$ — це і є відстань.",
    },
    {
        "type": "MULTI", "difficulty": 1, "skill": "MODEL",
        "text": r"На малюнку $AB \perp CD$, $O$ — точка їх перетину. Які з кутів прямі?",
        "svg_code": '<svg xmlns="http://www.w3.org/2000/svg" width="320" height="200" viewBox="0 0 320 200" fill="none" stroke="currentColor" stroke-width="2" font-family="sans-serif" font-size="16"><line x1="20" y1="100" x2="300" y2="100"/><line x1="160" y1="10" x2="160" y2="190"/><line x1="160" y1="100" x2="75.7" y2="29.3"/><path d="M174 100 L174 86 L160 86" stroke-width="1.5"/><circle cx="160" cy="100" r="3.5" fill="currentColor" stroke="none"/><text x="148" y="121" fill="currentColor" stroke="none" text-anchor="middle" font-style="italic">O</text><text x="20" y="89" fill="currentColor" stroke="none" text-anchor="middle" font-style="italic">A</text><text x="300" y="89" fill="currentColor" stroke="none" text-anchor="middle" font-style="italic">B</text><text x="174" y="19" fill="currentColor" stroke="none" text-anchor="middle" font-style="italic">C</text><text x="174" y="191" fill="currentColor" stroke="none" text-anchor="middle" font-style="italic">D</text><text x="66.5" y="26.6" fill="currentColor" stroke="none" text-anchor="middle" font-style="italic">K</text></svg>',
        "options": [(r"$\angle AOC$", True), (r"$\angle BOD$", True), (r"$\angle COB$", True),
                    (r"$\angle AOB$", False), (r"$\angle KOC$", False)],
        "hint": r"Якщо один із чотирьох кутів при перетині прямих прямий, то й інші три теж.",
        "solution": r"$AB \perp CD$, тому всі чотири кути $AOC$, $COB$, $BOD$, $DOA$ прямі. "
                    r"$\angle AOB = 180^\circ$ — розгорнутий, а $\angle KOC$ — лише частина прямого кута $AOC$.",
    },
    {
        "type": "MATCH", "difficulty": 1, "skill": "MODEL",
        "text": r"Установіть відповідність між описом (1–3) та терміном (А–Д).",
        "options": [r"А) відстань від точки до прямої", r"Б) основа перпендикуляра", r"В) кут між прямими",
                    r"Г) суміжні кути", r"Д) розгорнутий кут"],
        "matches": [(r"1. Довжина перпендикуляра, проведеного з точки до прямої", r"А) відстань від точки до прямої"),
                    (r"2. Точка, у якій перпендикуляр, проведений з точки до прямої, перетинає цю пряму", r"Б) основа перпендикуляра"),
                    (r"3. Той із чотирьох кутів при перетині двох прямих, що не більший за $90^\circ$", r"В) кут між прямими")],
        "hint": r"Пригадай означення з уроку: перпендикуляр $AH$, його основа $H$, кут між прямими.",
        "solution": r"Довжина перпендикуляра $AH$ — відстань від $A$ до прямої; $H$ — основа перпендикуляра; "
                    r"кут між прямими — той з утворених кутів, що не більший за $90^\circ$.",
    },
    # --- Розв'язування ---
    {
        "type": "CHOICE", "difficulty": 1, "skill": "SOLVE",
        "text": r"Один із кутів, що утворилися при перетині двох прямих, дорівнює $115^\circ$. Знайдіть кут між прямими.",
        "options": [(r"$115^\circ$", False), (r"$65^\circ$", True), (r"$25^\circ$", False),
                    (r"$57{,}5^\circ$", False), (r"$90^\circ$", False)],
        "hint": r"Знайди суміжний кут і вибери той, що не більший за $90^\circ$.",
        "solution": r"Суміжний кут: $180^\circ - 115^\circ = 65^\circ$. Утворилися кути $115^\circ$ і $65^\circ$ (кожен двічі). "
                    r"Кут між прямими не більший за $90^\circ$ — це $65^\circ$. "
                    r"($25^\circ = 115^\circ - 90^\circ$ і $57{,}5^\circ = 115^\circ : 2$ — дії без підстав.)",
    },
    {
        "type": "FIELDS", "difficulty": 1, "skill": "SOLVE",
        "text": r"Прямі перетинаються, $\angle 1 = 72^\circ$ (див. малюнок). Знайдіть кути (у градусах).",
        "svg_code": '<svg xmlns="http://www.w3.org/2000/svg" width="320" height="200" viewBox="0 0 320 200" fill="none" stroke="currentColor" stroke-width="2" font-family="sans-serif" font-size="16"><line x1="310" y1="100" x2="10" y2="100"/><line x1="192.4" y1="0.1" x2="127.6" y2="199.9"/><path d="M186 100 A26 26 0 0 0 168 75.3" stroke-width="1.5"/><circle cx="160" cy="100" r="3.5" fill="currentColor" stroke="none"/><text x="195.6" y="79.1" fill="currentColor" stroke="none" text-anchor="middle">1</text><text x="134.1" y="69.4" fill="currentColor" stroke="none" text-anchor="middle">2</text><text x="124.4" y="130.9" fill="currentColor" stroke="none" text-anchor="middle">3</text><text x="185.9" y="140.6" fill="currentColor" stroke="none" text-anchor="middle">4</text></svg>',
        "fields": [(r"$\angle 2$", "108"), (r"$\angle 3$", "72"), (r"$\angle 4$", "108"), ("Кут між прямими", "72")],
        "hint": r"$\angle 1$ і $\angle 2$ — суміжні, $\angle 1$ і $\angle 3$ — вертикальні.",
        "solution": r"$\angle 2 = 180^\circ - 72^\circ = 108^\circ$ (суміжні), $\angle 3 = \angle 1 = 72^\circ$, "
                    r"$\angle 4 = \angle 2 = 108^\circ$ (вертикальні). Кут між прямими — $72^\circ$, бо він не більший за $90^\circ$.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "SOLVE",
        "text": r"$AB \perp CD$, $O$ — точка їх перетину, $OK$ — бісектриса кута $AOC$. Знайдіть $\angle KOB$.",
        "options": [(r"$45^\circ$", False), (r"$90^\circ$", False), (r"$135^\circ$", True), (r"$180^\circ$", False)],
        "hint": r"$\angle AOC$ прямий, а $\angle KOB = \angle KOC + \angle COB$.",
        "solution": r"$\angle AOC = 90^\circ$, тож $\angle KOC = 90^\circ : 2 = 45^\circ$. "
                    r"$\angle COB = 90^\circ$, тому $\angle KOB = 45^\circ + 90^\circ = 135^\circ$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"$AH$ — перпендикуляр, проведений з точки $A$ до прямої $a$, $AH = 7$ см. Точка $B$ лежить на відрізку $AH$, $AB = 2$ см. "
                r"Знайдіть відстань від точки $B$ до прямої $a$ (у см).",
        "answer": "5",
        "hint": r"Відрізок $BH$ лежить на прямій $AH$, тож $BH \perp a$.",
        "solution": r"$BH$ — частина перпендикуляра $AH$, тому $BH \perp a$ і відстань від $B$ до $a$ дорівнює $BH$. "
                    r"$BH = AH - AB = 7 - 2 = 5$ (см).",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"На малюнку $AB \perp CD$, промінь $OM$ лежить усередині кута $BOC$, $\angle BOM = 28^\circ$. Знайдіть $\angle MOC$ (у градусах).",
        "svg_code": '<svg xmlns="http://www.w3.org/2000/svg" width="320" height="200" viewBox="0 0 320 200" fill="none" stroke="currentColor" stroke-width="2" font-family="sans-serif" font-size="16"><line x1="20" y1="110" x2="300" y2="110"/><line x1="130" y1="10" x2="130" y2="190"/><line x1="130" y1="110" x2="271.3" y2="34.9"/><path d="M116 110 L116 124 L130 124" stroke-width="1.5"/><path d="M176 110 A46 46 0 0 0 170.6 88.4" stroke-width="1.5"/><text x="197.9" y="98.1" fill="currentColor" stroke="none" text-anchor="middle" font-size="14">28°</text><circle cx="130" cy="110" r="3.5" fill="currentColor" stroke="none"/><text x="142" y="131" fill="currentColor" stroke="none" text-anchor="middle" font-style="italic">O</text><text x="20" y="99" fill="currentColor" stroke="none" text-anchor="middle" font-style="italic">A</text><text x="300" y="99" fill="currentColor" stroke="none" text-anchor="middle" font-style="italic">B</text><text x="144" y="19" fill="currentColor" stroke="none" text-anchor="middle" font-style="italic">C</text><text x="144" y="191" fill="currentColor" stroke="none" text-anchor="middle" font-style="italic">D</text><text x="281.9" y="34.3" fill="currentColor" stroke="none" text-anchor="middle" font-style="italic">M</text></svg>',
        "answer": "62",
        "hint": r"$\angle BOC$ — прямий.",
        "solution": r"$AB \perp CD$, тож $\angle BOC = 90^\circ$. $\angle MOC = 90^\circ - 28^\circ = 62^\circ$.",
    },
    # --- Аналіз ---
    {
        "type": "TF", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [("Якщо один із кутів, що утворилися при перетині двох прямих, прямий, то й решта три кути прямі", True),
                       (r"Кут між прямими може дорівнювати $120^\circ$", False),
                       ("Відстань від точки до прямої — це довжина перпендикуляра, проведеного з цієї точки до прямої", True),
                       ("Перпендикулярні відрізки завжди мають спільну точку", False)],
        "hint": r"Пригадай означення кута між прямими і перпендикулярних відрізків.",
        "solution": r"Суміжний з прямим кутом — теж $90^\circ$, вертикальні рівні, тож усі кути прямі. "
                    r"Кут між прямими не більший за $90^\circ$. Відрізки перпендикулярні, якщо лежать на перпендикулярних прямих, — "
                    r"самі відрізки можуть і не перетинатися.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "ANALYZE",
        "text": r"При перетині двох прямих утворилися кути $130^\circ$ і $50^\circ$. Хто правильно назвав кут між прямими?",
        "options": [(r"Петро: $130^\circ$ — більший із кутів", False), (r"Оля: $50^\circ$", True),
                    (r"Іра: $90^\circ$ — прямі ж перетинаються", False), (r"Марко: $180^\circ$ — сума кутів", False),
                    (r"Денис: $80^\circ$ — різниця кутів", False)],
        "hint": r"Кут між прямими не буває більшим за $90^\circ$.",
        "solution": r"Кут між прямими — той з утворених кутів, що не більший за $90^\circ$, тобто $50^\circ$. Права Оля.",
    },
    {
        "type": "ERROR", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Прямі $a$ і $b$ перетинаються, $\angle 1 = 40^\circ$ і $\angle 2 = 140^\circ$ — суміжні кути. "
                r"Саша робить висновок про прямі. У якому кроці помилка?",
        "steps": [r"$\angle 1 + \angle 2 = 40^\circ + 140^\circ = 180^\circ$",
                  r"Сума двох кутів дорівнює $180^\circ$, отже, $a \perp b$",
                  r"Відповідь: прямі $a$ і $b$ перпендикулярні"],
        "wrong": 1,
        "hint": r"Чи буває сума суміжних кутів іншою, ніж $180^\circ$?",
        "solution": r"Суміжні кути в сумі дають $180^\circ$ завжди, це не ознака перпендикулярності. "
                    r"Тут жоден кут не прямий ($40^\circ$ і $140^\circ$), тож прямі не перпендикулярні.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Прямі $a$ і $b$ перетинаються. Один із кутів виміряли транспортиром: $88^\circ$. Чи перпендикулярні прямі?",
        "svg_code": '<svg xmlns="http://www.w3.org/2000/svg" width="320" height="200" viewBox="0 0 320 200" fill="none" stroke="currentColor" stroke-width="2" font-family="sans-serif" font-size="16"><line x1="300" y1="100" x2="20" y2="100"/><line x1="163.2" y1="8.1" x2="156.8" y2="191.9"/><path d="M184 100 A24 24 0 0 0 160.8 76" stroke-width="1.5"/><text x="193.1" y="73" fill="currentColor" stroke="none" text-anchor="middle" font-size="14">88°</text><circle cx="160" cy="100" r="3.5" fill="currentColor" stroke="none"/><text x="300" y="89" fill="currentColor" stroke="none" text-anchor="middle" font-style="italic">a</text><text x="177.1" y="21.1" fill="currentColor" stroke="none" text-anchor="middle" font-style="italic">b</text></svg>',
        "options": [("Так: на малюнку кут виглядає прямим", False),
                    (r"Ні: перпендикулярні прямі утворюють кут рівно $90^\circ$", True),
                    (r"Так: $88^\circ$ — це майже $90^\circ$", False),
                    (r"Так: кут між прямими не більший за $90^\circ$", False),
                    ("Не можна визначити, не знаючи інших кутів", False)],
        "hint": r"Перпендикулярність визначає міра кута, а не вигляд малюнка.",
        "solution": r"Прямі перпендикулярні, лише якщо кут між ними дорівнює $90^\circ$. Тут кути $88^\circ$ і $92^\circ$ — "
                    r"прямі не перпендикулярні, хоч на око кут і схожий на прямий.",
    },
    {
        "type": "MULTI", "difficulty": 1, "skill": "ANALYZE",
        "text": r"На малюнку $AH \perp a$, точка $M$ лежить на прямій $a$. Які твердження правильні?",
        "svg_code": '<svg xmlns="http://www.w3.org/2000/svg" width="320" height="180" viewBox="0 0 320 180" fill="none" stroke="currentColor" stroke-width="2" font-family="sans-serif" font-size="16"><line x1="10" y1="140" x2="310" y2="140"/><text x="300" y="129" fill="currentColor" stroke="none" text-anchor="middle" font-style="italic">a</text><line x1="120" y1="40" x2="120" y2="140"/><line x1="120" y1="40" x2="250" y2="140"/><path d="M132 140 L132 128 L120 128" stroke-width="1.5"/><circle cx="120" cy="40" r="3.5" fill="currentColor" stroke="none"/><circle cx="120" cy="140" r="3.5" fill="currentColor" stroke="none"/><circle cx="250" cy="140" r="3.5" fill="currentColor" stroke="none"/><text x="120" y="29" fill="currentColor" stroke="none" text-anchor="middle" font-style="italic">A</text><text x="120" y="163" fill="currentColor" stroke="none" text-anchor="middle" font-style="italic">H</text><text x="250" y="163" fill="currentColor" stroke="none" text-anchor="middle" font-style="italic">M</text></svg>',
        "options": [(r"$AH$ — перпендикуляр, проведений з точки $A$ до прямої $a$", True),
                    (r"$H$ — основа перпендикуляра", True),
                    (r"Відстань від $A$ до прямої $a$ дорівнює $AM$", False),
                    (r"$AM \gt AH$", True),
                    (r"$AM \perp a$", False)],
        "hint": r"Найкоротший відрізок від точки до прямої — перпендикуляр.",
        "solution": r"$AH$ — перпендикуляр, $H$ — його основа, відстань від $A$ до $a$ — це $AH$. "
                    r"Будь-який інший відрізок $AM$ довший за $AH$ і не перпендикулярний до $a$.",
    },
    # ==========================================
    # СХОДИНКА 2 — СЕРЕДНІЙ
    # ==========================================
    # --- Моделювання ---
    {
        "type": "FIELDS", "difficulty": 2, "skill": "MODEL",
        "text": r"Точки $A$ і $B$ лежать на прямій, перпендикулярній до прямої $a$. Відстань від $A$ до $a$ — $2$ см, від $B$ до $a$ — $6$ см. "
                r"Знайдіть $AB$ (у см) у двох випадках.",
        "fields": [(r"$A$ і $B$ по один бік від $a$:", "4"), (r"$A$ і $B$ по різні боки від $a$:", "8")],
        "hint": r"Зроби два схематичні малюнки: пряма $AB$ перетинає $a$ в точці $H$, $AH = 2$, $BH = 6$.",
        "solution": r"Пряма $AB$ перетинає $a$ в точці $H$; $AH$ і $BH$ — перпендикуляри, $AH = 2$ см, $BH = 6$ см. "
                    r"По один бік: $AB = 6 - 2 = 4$ (см). По різні боки: $AB = 6 + 2 = 8$ (см).",
    },
    {
        "type": "COORD", "difficulty": 2, "skill": "MODEL",
        "text": r"Познач точку $H$ — основу перпендикуляра, проведеного з точки $A(4; -3)$ до осі абсцис.",
        "xmin": -5, "xmax": 5, "ymin": -5, "ymax": 5, "step": 1, "answer": [4, 0],
        "hint": r"Вісь ординат перпендикулярна до осі абсцис; перпендикуляр з $A$ йде вертикально.",
        "solution": r"Осі координат перпендикулярні, тож перпендикуляр з $A$ до осі абсцис іде вертикально: "
                    r"абсциса не змінюється, а ордината стає $0$. $H(4; 0)$, відстань $AH = 3$.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "MODEL",
        "text": r"О котрій із цих годин стрілки годинника лежать на перпендикулярних прямих?",
        "options": [("3:00", True), ("6:00", False), ("12:15", False), ("9:30", False), ("4:00", False)],
        "hint": r"Між сусідніми числами на циферблаті $360^\circ : 12 = 30^\circ$. Годинна стрілка теж рухається.",
        "solution": r"О 3:00: $3 \cdot 30^\circ = 90^\circ$ — прямий кут. О 6:00 — $180^\circ$, о 4:00 — $120^\circ$. "
                    r"О 12:15 годинна стрілка пройшла чверть поділки ($7{,}5^\circ$), тож кут $90^\circ - 7{,}5^\circ = 82{,}5^\circ$. "
                    r"О 9:30 годинна стрілка посередині між 9 і 10: $3{,}5 \cdot 30^\circ = 105^\circ$.",
    },
    {
        "type": "ORDER", "difficulty": 2, "skill": "MODEL",
        "text": r"Прямі $a$ і $b$ перетинаються, а суміжні кути $\angle 1$ і $\angle 2$ рівні. "
                r"Розташуй кроки доведення того, що $a \perp b$.",
        "items": [r"$\angle 1 + \angle 2 = 180^\circ$, бо кути суміжні",
                  r"$\angle 1 = \angle 2$, тому $2 \cdot \angle 1 = 180^\circ$",
                  r"$\angle 1 = 90^\circ$",
                  r"Один із кутів прямий, отже, $a \perp b$"],
        "hint": r"Почни з властивості суміжних кутів.",
        "solution": r"Сума суміжних кутів $180^\circ$; вони рівні, тож кожен $90^\circ$; один прямий кут — і прямі перпендикулярні.",
    },
    {
        "type": "EXPR", "difficulty": 2, "skill": "MODEL",
        "text": r"Прямі $m$ і $n$ не перпендикулярні, кут між ними дорівнює $x^\circ$. "
                r"Запиши суму двох тупих кутів, що утворилися при їх перетині (у градусах).",
        "answer": "360-2x", "vars": ["x"],
        "hint": r"Тупий кут — суміжний з кутом $x^\circ$.",
        "solution": r"Кут між прямими $x^\circ$ — гострий, суміжний з ним тупий кут $180 - x$. "
                    r"Тупих кутів два (вертикальні), їх сума $2(180 - x) = 360 - 2x$.",
    },
    # --- Розв'язування ---
    {
        "type": "CHOICE", "difficulty": 2, "skill": "SOLVE",
        "text": r"Два з кутів, що утворилися при перетині двох прямих, відносяться як $1 : 5$. Знайдіть кут між прямими.",
        "options": [(r"$30^\circ$", True), (r"$150^\circ$", False), (r"$60^\circ$", False),
                    (r"$36^\circ$", False), (r"$90^\circ$", False)],
        "solution": r"Нерівні кути при перетині — суміжні, бо вертикальні рівні. $x + 5x = 180^\circ$, $x = 30^\circ$. "
                    r"Кути $30^\circ$ і $150^\circ$, кут між прямими — $30^\circ$. ($60^\circ$ — якщо взяти $360^\circ$, $150^\circ$ — тупий кут.)",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Сума двох кутів, що утворилися при перетині двох прямих, дорівнює $200^\circ$. Знайдіть кут між прямими (у градусах).",
        "answer": "80",
        "solution": r"Суміжні кути в сумі дають $180^\circ$, тож ці два кути вертикальні й рівні: $200^\circ : 2 = 100^\circ$. "
                    r"Інші два кути по $80^\circ$, кут між прямими — $80^\circ$.",
    },
    {
        "type": "FIELDS", "difficulty": 2, "skill": "SOLVE",
        "text": r"На малюнку $\angle AOC = 64^\circ$, $OM$ — бісектриса кута $AOC$, $ON$ — бісектриса кута $COB$. Знайдіть кути (у градусах).",
        "svg_code": '<svg xmlns="http://www.w3.org/2000/svg" width="320" height="180" viewBox="0 0 320 180" fill="none" stroke="currentColor" stroke-width="2" font-family="sans-serif" font-size="16"><line x1="10" y1="150" x2="310" y2="150"/><line x1="160" y1="150" x2="98.6" y2="24.2"/><line x1="160" y1="150" x2="58.2" y2="86.4"/><line x1="160" y1="150" x2="223.6" y2="48.2"/><path d="M146.8 123 A30 30 0 0 0 130 150" stroke-width="1.5"/><text x="99.8" y="140" fill="currentColor" stroke="none" text-anchor="middle" font-size="14">64°</text><circle cx="160" cy="150" r="3.5" fill="currentColor" stroke="none"/><text x="160" y="173" fill="currentColor" stroke="none" text-anchor="middle" font-style="italic">O</text><text x="16" y="173" fill="currentColor" stroke="none" text-anchor="middle" font-style="italic">A</text><text x="304" y="173" fill="currentColor" stroke="none" text-anchor="middle" font-style="italic">B</text><text x="88.6" y="29.2" fill="currentColor" stroke="none" text-anchor="middle" font-style="italic">C</text><text x="48.1" y="85.1" fill="currentColor" stroke="none" text-anchor="middle" font-style="italic">M</text><text x="229.9" y="43.1" fill="currentColor" stroke="none" text-anchor="middle" font-style="italic">N</text></svg>',
        "fields": [(r"$\angle MOC$", "32"), (r"$\angle CON$", "58"), (r"$\angle MON$", "90")],
        "solution": r"$\angle MOC = 64^\circ : 2 = 32^\circ$. $\angle COB = 180^\circ - 64^\circ = 116^\circ$ (суміжні), "
                    r"$\angle CON = 116^\circ : 2 = 58^\circ$. $\angle MON = 32^\circ + 58^\circ = 90^\circ$ — бісектриси суміжних кутів перпендикулярні.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"$AB \perp CD$, $O$ — точка їх перетину. Промінь $OK$ лежить усередині кута $AOC$, $\angle AOK : \angle KOC = 1 : 2$. "
                r"Знайдіть $\angle KOB$ (у градусах).",
        "answer": "150",
        "solution": r"$\angle AOC = 90^\circ$, тож $\angle AOK = 90^\circ : 3 = 30^\circ$, $\angle KOC = 60^\circ$. "
                    r"$\angle KOB = \angle KOC + \angle COB = 60^\circ + 90^\circ = 150^\circ$ (або $180^\circ - 30^\circ$).",
    },
    {
        "type": "ORDER", "difficulty": 2, "skill": "SOLVE",
        "text": r"Для кожної пари прямих відомий один із кутів, що утворилися при їх перетині. Розташуй пари за зростанням кута між прямими.",
        "items": [r"$a$ і $b$: один із кутів $150^\circ$", r"$c$ і $d$: один із кутів $70^\circ$",
                  r"$e$ і $f$: один із кутів $100^\circ$", r"$m$ і $n$: один із кутів $90^\circ$"],
        "solution": r"Кути між прямими: $a, b$ — $180^\circ - 150^\circ = 30^\circ$; $c, d$ — $70^\circ$; "
                    r"$e, f$ — $180^\circ - 100^\circ = 80^\circ$; $m, n$ — $90^\circ$. Отже, $30^\circ \lt 70^\circ \lt 80^\circ \lt 90^\circ$.",
    },
    # --- Аналіз ---
    {
        "type": "GROUP", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Прямі $a$ і $b$ перетинаються. Чи гарантує кожна з умов, що $a \perp b$?",
        "groups": [r"Так, $a \perp b$", "Не гарантує"],
        "items": [(r"Один із кутів дорівнює $90^\circ$", 0), ("Два суміжні кути рівні", 0),
                  (r"Сума двох вертикальних кутів дорівнює $180^\circ$", 0),
                  (r"Сума двох суміжних кутів дорівнює $180^\circ$", 1), ("Два вертикальні кути рівні", 1),
                  (r"Один із кутів дорівнює $89^\circ$", 1)],
        "solution": r"Досить знайти один прямий кут. Рівні суміжні кути — по $90^\circ$; вертикальні рівні, тож із сумою $180^\circ$ — по $90^\circ$. "
                    r"Сума суміжних завжди $180^\circ$, а вертикальні рівні завжди — це нічого не гарантує; $89^\circ \ne 90^\circ$.",
    },
    {
        "type": "MULTI", "difficulty": 2, "skill": "ANALYZE",
        "text": r"З точки $A$ до прямої $a$ проведено перпендикуляр $AH = 4$ см. "
                r"Якою може бути довжина відрізка $AM$, де $M$ — точка прямої $a$, відмінна від $H$?",
        "options": [(r"$3$ см", False), (r"$4$ см", False), (r"$4{,}5$ см", True), (r"$6$ см", True), (r"$10$ см", True)],
        "solution": r"Перпендикуляр — найкоротший відрізок від точки до прямої, тож $AM \gt AH = 4$ см. "
                    r"Відсуваючи $M$ від $H$, можна отримати будь-яку довжину, більшу за $4$ см.",
    },
    {
        "type": "ERROR", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Один із кутів, що утворилися при перетині двох прямих, у $4$ рази більший за інший. Знайдіть кут між прямими. У якому кроці помилка?",
        "steps": [r"Нехай менший кут $x$, тоді більший — $4x$; ці кути суміжні: $x + 4x = 180^\circ$",
                  r"$5x = 180^\circ$, $x = 36^\circ$",
                  r"Більший кут: $4x = 144^\circ$",
                  r"Кут між прямими дорівнює $144^\circ$"],
        "wrong": 3,
        "solution": r"Кути $36^\circ$ і $144^\circ$ знайдено правильно, але кут між прямими не більший за $90^\circ$: це $36^\circ$.",
    },
    {
        "type": "TF", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [("Через точку прямої можна провести дві різні прямі, перпендикулярні до неї", False),
                       (r"Якщо відрізки $AB$ і $CD$ перпендикулярні, то прямі $AB$ і $CD$ перетинаються", True),
                       ("Бісектриси двох суміжних кутів перпендикулярні", True),
                       (r"Якщо кут між прямими дорівнює $90^\circ$, то прямі перпендикулярні", True)],
        "solution": r"Через точку прямої проходить лише одна перпендикулярна до неї пряма. "
                    r"Перпендикулярні відрізки лежать на перпендикулярних прямих, а такі прямі перетинаються (хоч самі відрізки — не обов'язково). "
                    r"Бісектриси суміжних кутів утворюють $\tfrac12 \cdot 180^\circ = 90^\circ$. Кут $90^\circ$ між прямими — це і є перпендикулярність.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Точка $A$ лежить поза прямою $a$. Андрій провів з $A$ три відрізки до точок прямої $a$ і виміряв їх: $5$ см, $6$ см і $4$ см. "
                r"Він каже: «Відстань від $A$ до $a$ дорівнює $4$ см». Чи правий він?",
        "options": [("Так: найкоротший із проведених відрізків і є відстанню", False),
                    (r"Не обов'язково: відстань — довжина перпендикуляра; вона не більша за $4$ см, а дорівнює $4$ см, лише якщо цей відрізок перпендикулярний до $a$", True),
                    (r"Ні: відстань — середнє значення, $5$ см", False),
                    (r"Ні: відстань — найдовший відрізок, $6$ см", False),
                    ("Так: усі відрізки від точки до прямої дорівнюють відстані", False)],
        "solution": r"Відстань — довжина перпендикуляра, а він найкоротший з усіх відрізків від $A$ до $a$. "
                    r"Тож відстань не більша за $4$ см; дорівнює $4$ см, лише якщо відрізок $4$ см — перпендикуляр.",
    },
    # ==========================================
    # СХОДИНКА 3 — ПІДВИЩЕНИЙ
    # ==========================================
    # --- Моделювання ---
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"Один із кутів, що утворилися при перетині двох прямих, на $30^\circ$ менший від суми двох суміжних з ним кутів. "
                r"Знайдіть кут між прямими (у градусах).",
        "answer": "70",
        "solution": r"Нехай кут $x$; кожен суміжний з ним дорівнює $180^\circ - x$. "
                    r"$x = 2(180^\circ - x) - 30^\circ$, $3x = 330^\circ$, $x = 110^\circ$. "
                    r"Кут тупий, тож кут між прямими $180^\circ - 110^\circ = 70^\circ$.",
    },
    {
        "type": "EXPR", "difficulty": 3, "skill": "MODEL",
        "text": r"$AB \perp CD$, $O$ — точка їх перетину. Промінь $OM$ лежить усередині кута $AOC$, $\angle AOM = x^\circ$, "
                r"$ON$ — бісектриса кута $MOC$. Вирази $\angle NOB$ (у градусах) через $x$.",
        "svg_code": '<svg xmlns="http://www.w3.org/2000/svg" width="320" height="200" viewBox="0 0 320 200" fill="none" stroke="currentColor" stroke-width="2" font-family="sans-serif" font-size="16"><line x1="20" y1="110" x2="310" y2="110"/><line x1="170" y1="10" x2="170" y2="190"/><path d="M184 110 L184 96 L170 96" stroke-width="1.5"/><line x1="170" y1="110" x2="81.9" y2="36.1"/><line x1="170" y1="110" x2="131.1" y2="26.6"/><path d="M139.4 84.3 A40 40 0 0 0 130 110" stroke-width="1.5"/><text x="113.6" y="94.5" fill="currentColor" stroke="none" text-anchor="middle" font-style="italic" font-size="14">x°</text><circle cx="170" cy="110" r="3.5" fill="currentColor" stroke="none"/><text x="182" y="131" fill="currentColor" stroke="none" text-anchor="middle" font-style="italic">O</text><text x="20" y="99" fill="currentColor" stroke="none" text-anchor="middle" font-style="italic">A</text><text x="310" y="99" fill="currentColor" stroke="none" text-anchor="middle" font-style="italic">B</text><text x="184" y="19" fill="currentColor" stroke="none" text-anchor="middle" font-style="italic">C</text><text x="184" y="191" fill="currentColor" stroke="none" text-anchor="middle" font-style="italic">D</text><text x="72.7" y="33.4" fill="currentColor" stroke="none" text-anchor="middle" font-style="italic">M</text><text x="126" y="20.7" fill="currentColor" stroke="none" text-anchor="middle" font-style="italic">N</text></svg>',
        "answer": "135-x/2", "vars": ["x"],
        "solution": r"$\angle MOC = 90 - x$, тож $\angle NOC = \tfrac12 (90 - x) = 45 - \tfrac{x}{2}$. "
                    r"$\angle NOB = \angle NOC + \angle COB = 45 - \tfrac{x}{2} + 90 = 135 - \tfrac{x}{2}$.",
    },
    {
        "type": "COORD", "difficulty": 3, "skill": "MODEL",
        "text": r"Дано точку $A(-3; 2)$. Точка $B$ лежить нижче від осі абсцис, відрізок $AB$ перпендикулярний до осі абсцис, "
                r"а відстань від $B$ до осі абсцис дорівнює $4$. Познач точку $B$.",
        "xmin": -5, "xmax": 5, "ymin": -5, "ymax": 5, "step": 1, "answer": [-3, -4],
        "solution": r"$AB$ перпендикулярний до осі абсцис, тобто вертикальний: абсциса $B$ така сама, $-3$. "
                    r"$B$ нижче від осі на відстані $4$, тож ордината $-4$. $B(-3; -4)$.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "MODEL",
        "text": r"Один із кутів, що утворилися при перетині двох прямих, на $50^\circ$ більший за інший. "
                r"Кут між прямими позначили $x$ (у градусах). Яке рівняння відповідає умові?",
        "options": [(r"$x + (x + 50) = 180$", True), (r"$x + (x + 50) = 360$", False), (r"$x + (x + 50) = 90$", False),
                    (r"$x + 50 = 90$", False), (r"$2x + 2(x + 50) = 180$", False)],
        "solution": r"Нерівні кути — суміжні (вертикальні рівні), тож їх сума $180^\circ$: $x + (x + 50) = 180$. "
                    r"Сума всіх чотирьох кутів — $360^\circ$, тобто $2x + 2(x + 50) = 360$, а не $180$.",
    },
    {
        "type": "MATCH", "difficulty": 3, "skill": "MODEL",
        "text": r"Установіть відповідність між умовою про кути, що утворилися при перетині двох прямих (1–3), та кутом між прямими (А–Д).",
        "options": [r"А) $45^\circ$", r"Б) $60^\circ$", r"В) $90^\circ$", r"Г) $120^\circ$", r"Д) $135^\circ$"],
        "matches": [(r"1. Один із кутів утричі більший за інший", r"А) $45^\circ$"),
                    (r"2. Сума двох із кутів дорівнює $240^\circ$", r"Б) $60^\circ$"),
                    (r"3. Сума трьох із кутів дорівнює $270^\circ$", r"В) $90^\circ$")],
        "solution": r"1) Суміжні: $x + 3x = 180^\circ$, $x = 45^\circ$. "
                    r"2) $240^\circ \ne 180^\circ$, тож це вертикальні кути по $120^\circ$, інші — по $60^\circ$. "
                    r"3) Четвертий кут $360^\circ - 270^\circ = 90^\circ$ — прямі перпендикулярні.",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Прямі $a$, $b$ і $c$ проходять через одну точку, $a \perp b$, кут між прямими $a$ і $c$ дорівнює $25^\circ$. "
                r"Знайдіть кут між прямими $b$ і $c$ (у градусах).",
        "svg_code": '<svg xmlns="http://www.w3.org/2000/svg" width="320" height="200" viewBox="0 0 320 200" fill="none" stroke="currentColor" stroke-width="2" font-family="sans-serif" font-size="16"><line x1="310" y1="100" x2="10" y2="100"/><line x1="160" y1="8" x2="160" y2="192"/><line x1="295.9" y1="36.6" x2="24.1" y2="163.4"/><path d="M160 86 L146 86 L146 100" stroke-width="1.5"/><path d="M210 100 A50 50 0 0 0 205.3 78.9" stroke-width="1.5"/><text x="232.2" y="89" fill="currentColor" stroke="none" text-anchor="middle" font-size="14">25°</text><circle cx="160" cy="100" r="3.5" fill="currentColor" stroke="none"/><text x="302" y="89" fill="currentColor" stroke="none" text-anchor="middle" font-style="italic">a</text><text x="174" y="17" fill="currentColor" stroke="none" text-anchor="middle" font-style="italic">b</text><text x="295.9" y="27.6" fill="currentColor" stroke="none" text-anchor="middle" font-style="italic">c</text></svg>',
        "answer": "65",
        "solution": r"Промінь прямої $c$ лежить усередині прямого кута між $a$ і $b$ і ділить його на $25^\circ$ і $90^\circ - 25^\circ = 65^\circ$. "
                    r"$65^\circ \le 90^\circ$, тож кут між $b$ і $c$ — $65^\circ$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"$AB \perp CD$, $O$ — точка їх перетину. Промінь $OK$ лежить усередині кута $BOC$, промінь $OM$ — усередині кута $BOD$, "
                r"$\angle KOM = 100^\circ$, $\angle KOB = 35^\circ$. Знайдіть $\angle MOD$ (у градусах).",
        "svg_code": '<svg xmlns="http://www.w3.org/2000/svg" width="320" height="200" viewBox="0 0 320 200" fill="none" stroke="currentColor" stroke-width="2" font-family="sans-serif" font-size="16"><line x1="20" y1="100" x2="300" y2="100"/><line x1="150" y1="10" x2="150" y2="190"/><path d="M150 86 L136 86 L136 100" stroke-width="1.5"/><line x1="150" y1="100" x2="264.7" y2="19.7"/><line x1="150" y1="100" x2="184.7" y2="174.3"/><circle cx="150" cy="100" r="3.5" fill="currentColor" stroke="none"/><text x="138" y="121" fill="currentColor" stroke="none" text-anchor="middle" font-style="italic">O</text><text x="20" y="89" fill="currentColor" stroke="none" text-anchor="middle" font-style="italic">A</text><text x="300" y="89" fill="currentColor" stroke="none" text-anchor="middle" font-style="italic">B</text><text x="164" y="19" fill="currentColor" stroke="none" text-anchor="middle" font-style="italic">C</text><text x="136" y="191" fill="currentColor" stroke="none" text-anchor="middle" font-style="italic">D</text><text x="274.5" y="17.8" fill="currentColor" stroke="none" text-anchor="middle" font-style="italic">K</text><text x="199.7" y="190.2" fill="currentColor" stroke="none" text-anchor="middle" font-style="italic">M</text></svg>',
        "answer": "25",
        "solution": r"Промінь $OB$ лежить між $OK$ і $OM$: $\angle BOM = 100^\circ - 35^\circ = 65^\circ$. "
                    r"$\angle BOD = 90^\circ$, тож $\angle MOD = 90^\circ - 65^\circ = 25^\circ$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Прямі $AB$ і $CD$ перетинаються в точці $O$, $OK$ — бісектриса кута $AOC$, $\angle KOB = 155^\circ$. "
                r"Знайдіть кут між прямими $AB$ і $CD$ (у градусах).",
        "answer": "50",
        "solution": r"$\angle AOK = 180^\circ - 155^\circ = 25^\circ$ (суміжні). $\angle AOC = 2 \cdot 25^\circ = 50^\circ$. "
                    r"Кути при перетині — $50^\circ$ і $130^\circ$, кут між прямими — $50^\circ$.",
    },
    {
        "type": "FIELDS", "difficulty": 3, "skill": "SOLVE",
        "text": r"$AH$ — перпендикуляр до прямої $a$, $AH = 6$ см. Точка $B$ лежить на промені $HA$, $AB = 2$ см. "
                r"Знайдіть відстань від точки $B$ до прямої $a$ (у см). Розгляньте обидва можливі випадки.",
        "fields": [("Менше значення:", "4"), ("Більше значення:", "8")],
        "solution": r"$B$ лежить на промені $HA$, тож $BH \perp a$ і відстань від $B$ до $a$ — це $BH$. "
                    r"Якщо $B$ між $H$ і $A$: $BH = 6 - 2 = 4$ (см). Якщо $A$ між $H$ і $B$: $BH = 6 + 2 = 8$ (см).",
    },
    {
        "type": "EXPR", "difficulty": 3, "skill": "SOLVE",
        "text": r"Прямі $AB$ і $CD$ перетинаються в точці $O$, $\angle AOC = x^\circ$, де $x \lt 90$. "
                r"Промінь $OK \perp AB$, точки $K$ і $C$ лежать по один бік від прямої $AB$. Вирази $\angle KOD$ (у градусах) через $x$.",
        "svg_code": '<svg xmlns="http://www.w3.org/2000/svg" width="320" height="200" viewBox="0 0 320 200" fill="none" stroke="currentColor" stroke-width="2" font-family="sans-serif" font-size="16"><line x1="15" y1="105" x2="305" y2="105"/><line x1="82.9" y1="13.1" x2="237.1" y2="196.9"/><line x1="160" y1="105" x2="160" y2="13"/><path d="M174 105 L174 91 L160 91" stroke-width="1.5"/><path d="M138.1 79 A34 34 0 0 0 126 105" stroke-width="1.5"/><text x="111.1" y="87.2" fill="currentColor" stroke="none" text-anchor="middle" font-style="italic" font-size="14">x°</text><circle cx="160" cy="105" r="3.5" fill="currentColor" stroke="none"/><text x="147" y="126" fill="currentColor" stroke="none" text-anchor="middle" font-style="italic">O</text><text x="19" y="94" fill="currentColor" stroke="none" text-anchor="middle" font-style="italic">A</text><text x="301" y="94" fill="currentColor" stroke="none" text-anchor="middle" font-style="italic">B</text><text x="70.9" y="18.1" fill="currentColor" stroke="none" text-anchor="middle" font-style="italic">C</text><text x="240.8" y="189.7" fill="currentColor" stroke="none" text-anchor="middle" font-style="italic">D</text><text x="174" y="22" fill="currentColor" stroke="none" text-anchor="middle" font-style="italic">K</text></svg>',
        "answer": "90+x", "vars": ["x"],
        "solution": r"$\angle BOD = \angle AOC = x$ (вертикальні). $\angle KOB = 90^\circ$, бо $OK \perp AB$. "
                    r"Промінь $OB$ лежить між $OK$ і $OD$, тож $\angle KOD = 90 + x$.",
    },
    # --- Аналіз ---
    {
        "type": "TF", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [(r"Якщо при перетині двох прямих сума двох вертикальних кутів дорівнює $180^\circ$, то прямі перпендикулярні", True),
                       (r"Якщо сума трьох кутів, що утворилися при перетині двох прямих, дорівнює $270^\circ$, то прямі перпендикулярні", True),
                       ("Якщо два з кутів, що утворилися при перетині двох прямих, рівні, то прямі перпендикулярні", False),
                       (r"Якщо $OA \perp OB$ і $OC \perp OB$, причому $A$ і $C$ лежать по різні боки від прямої $OB$, то точки $A$, $O$, $C$ лежать на одній прямій", True)],
        "solution": r"Вертикальні кути рівні: із сумою $180^\circ$ — по $90^\circ$. Четвертий кут $360^\circ - 270^\circ = 90^\circ$. "
                    r"Рівними є будь-які вертикальні кути — це нічого не гарантує. "
                    r"$\angle AOB + \angle BOC = 90^\circ + 90^\circ = 180^\circ$ — кут $AOC$ розгорнутий.",
    },
    {
        "type": "ERROR", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Сума трьох кутів, що утворилися при перетині двох прямих, дорівнює $250^\circ$. Знайдіть кут між прямими. У якому кроці помилка?",
        "steps": [r"Чотири кути — дві пари суміжних, їх сума $2 \cdot 180^\circ = 360^\circ$",
                  r"Четвертий кут: $360^\circ - 250^\circ = 110^\circ$",
                  r"Кут між прямими дорівнює $110^\circ$"],
        "wrong": 2,
        "solution": r"Четвертий кут $110^\circ$ знайдено правильно, але він тупий. Кути при перетині — $110^\circ$ і $70^\circ$, "
                    r"кут між прямими — $70^\circ$ (перевірка: $110^\circ + 70^\circ + 70^\circ = 250^\circ$).",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Промені $OA$, $OB$, $OC$, $OD$ ідуть навколо точки $O$ саме в такому порядку й утворюють чотири рівні кути "
                r"$AOB$, $BOC$, $COD$, $DOA$, які разом становлять $360^\circ$. Яке твердження правильне?",
        "options": [(r"Прямі $AC$ і $BD$ перпендикулярні", True), (r"Кожен із кутів дорівнює $45^\circ$", False),
                    (r"$\angle AOC = 90^\circ$", False),
                    (r"Промені $OA$ і $OC$ не обов'язково лежать на одній прямій", False),
                    ("Усі чотири промені лежать на одній прямій", False)],
        "solution": r"Кожен кут $360^\circ : 4 = 90^\circ$. $\angle AOB + \angle BOC = 180^\circ$ — тож $A$, $O$, $C$ на одній прямій; "
                    r"так само $B$, $O$, $D$. Прямі $AC$ і $BD$ утворюють прямий кут $AOB$, отже, $AC \perp BD$.",
    },
    {
        "type": "MULTI", "difficulty": 3, "skill": "ANALYZE",
        "text": r"$AH$ — перпендикуляр до прямої $a$, $AH = 5$ см, $M$ — точка прямої $a$, відмінна від $H$. Які твердження правильні?",
        "options": [(r"Може бути $AM = 5$ см", False), (r"Може бути $AM = 13$ см", True),
                    (r"Відстань від точки $M$ до прямої $AH$ дорівнює $MH$", True), (r"Може бути $AM \perp a$", False)],
        "solution": r"$AM$ — не перпендикуляр, тож $AM \gt AH = 5$ см (і $13$ см можливо). Якби $AM \perp a$, то відрізок $AH$ був би довшим за перпендикуляр $AM$, а $AH \lt AM$. "
                    r"$MH$ лежить на $a$, а $a \perp AH$, тому $MH$ — перпендикуляр з $M$ до прямої $AH$ і відстань дорівнює $MH$.",
    },
    {
        "type": "GROUP", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Два з чотирьох кутів, що утворилися при перетині двох прямих, дорівнюють… Чи можливо це?",
        "groups": ["Можливо", "Неможливо"],
        "items": [(r"$50^\circ$ і $130^\circ$", 0), (r"$70^\circ$ і $70^\circ$", 0), (r"$50^\circ$ і $140^\circ$", 1),
                  (r"$90^\circ$ і $80^\circ$", 1), (r"$120^\circ$ і $120^\circ$", 0), (r"$90^\circ$ і $90^\circ$", 0)],
        "solution": r"Будь-які два з кутів або вертикальні (рівні), або суміжні (у сумі $180^\circ$). "
                    r"$50^\circ$ і $140^\circ$ — ні рівні, ні в сумі $180^\circ$. Якщо один кут $90^\circ$, то всі чотири прямі, тож $80^\circ$ неможливо.",
    },
    # ==========================================
    # БОСИ (difficulty 4)
    # ==========================================
    {
        "type": "SHORT", "difficulty": 4, "skill": "MODEL",
        "text": r"Промені $OA$, $OC$, $OB$, $OD$ ідуть саме в такому порядку (див. малюнок), $\angle AOB = \angle COD = 90^\circ$, "
                r"а $\angle AOD$ у $4$ рази більший за $\angle COB$. Знайдіть $\angle AOD$ (у градусах).",
        "svg_code": '<svg xmlns="http://www.w3.org/2000/svg" width="320" height="190" viewBox="0 0 320 190" fill="none" stroke="currentColor" stroke-width="2" font-family="sans-serif" font-size="16"><line x1="160" y1="165" x2="300" y2="165"/><line x1="160" y1="165" x2="239.4" y2="55.8"/><line x1="160" y1="165" x2="160" y2="30"/><line x1="160" y1="165" x2="46.7" y2="82.7"/><path d="M194 165 A34 34 0 0 0 160 131" stroke-width="1.5"/><path d="M187 127.8 A46 46 0 0 0 122.8 138" stroke-width="1.5"/><circle cx="160" cy="165" r="3.5" fill="currentColor" stroke="none"/><text x="160" y="186" fill="currentColor" stroke="none" text-anchor="middle" font-style="italic">O</text><text x="312" y="160" fill="currentColor" stroke="none" text-anchor="middle" font-style="italic">A</text><text x="247" y="50.3" fill="currentColor" stroke="none" text-anchor="middle" font-style="italic">C</text><text x="160" y="22" fill="currentColor" stroke="none" text-anchor="middle" font-style="italic">B</text><text x="37" y="80.7" fill="currentColor" stroke="none" text-anchor="middle" font-style="italic">D</text></svg>',
        "answer": "144",
        "solution": r"Нехай $\angle COB = x$. Тоді $\angle AOC = 90^\circ - x$ (частина прямого кута $AOB$). "
                    r"$\angle AOD = \angle AOC + \angle COD = (90^\circ - x) + 90^\circ = 180^\circ - x$. "
                    r"За умовою $180^\circ - x = 4x$, звідки $x = 36^\circ$, а $\angle AOD = 4 \cdot 36^\circ = 144^\circ$.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "MODEL",
        "text": r"$AB \perp CD$, $O$ — точка їх перетину. Пряма $EF$ проходить через $O$, точка $E$ лежить усередині кута $BOC$, "
                r"і $\angle AOE$ у $5$ разів більший за $\angle EOB$. Знайдіть кут між прямими $EF$ і $CD$ (у градусах).",
        "answer": "60",
        "solution": r"$\angle AOE$ і $\angle EOB$ — суміжні: $\angle EOB = x$, $5x + x = 180^\circ$, $x = 30^\circ$. "
                    r"$\angle BOC = 90^\circ$, тож $\angle EOC = 90^\circ - 30^\circ = 60^\circ$. "
                    r"Прямі $EF$ і $CD$ утворюють кути $60^\circ$ і $120^\circ$, кут між ними — $60^\circ$.",
    },
    {
        "type": "FIELDS", "difficulty": 4, "skill": "SOLVE",
        "text": r"$\angle AOB$ і $\angle BOC$ — суміжні, $\angle AOB = 70^\circ$, $OK$ — бісектриса кута $AOB$. "
                r"Промінь $OM$ лежить усередині кута $BOC$, і $OM \perp OK$. Знайдіть кути (у градусах).",
        "fields": [(r"$\angle BOM$", "55"), (r"$\angle MOC$", "55")],
        "solution": r"$\angle KOB = 70^\circ : 2 = 35^\circ$. $OM \perp OK$, тож $\angle KOM = 90^\circ$ і "
                    r"$\angle BOM = 90^\circ - 35^\circ = 55^\circ$. $\angle BOC = 180^\circ - 70^\circ = 110^\circ$, "
                    r"$\angle MOC = 110^\circ - 55^\circ = 55^\circ$. Отже, $OM$ — бісектриса кута $BOC$.",
    },
    {
        "type": "FIELDS", "difficulty": 4, "skill": "SOLVE",
        "text": r"Точки $A$ і $B$ лежать на прямій, перпендикулярній до прямої $a$, на відстанях $3$ см і $5$ см від $a$. "
                r"$M$ — середина відрізка $AB$. Знайдіть відстань від $M$ до прямої $a$ (у см) — два можливі значення.",
        "fields": [("Менше значення:", "1"), ("Більше значення:", "4")],
        "solution": r"Пряма $AB$ перетинає $a$ в точці $H$; $M$ лежить на $AH$, тож відстань від $M$ до $a$ — це $MH$. "
                    r"По один бік: $AB = 5 - 3 = 2$, $AM = 1$, $MH = 3 + 1 = 4$ (см). "
                    r"По різні боки: $AB = 5 + 3 = 8$, $AM = 4$; $M$ лежить по той бік від $a$, що й $B$, і $MH = 4 - 3 = 1$ (см).",
    },
    {
        "type": "TF", "difficulty": 4, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [("Якщо при перетині двох прямих утворилися три рівні кути, то прямі перпендикулярні", True),
                       ("Якщо бісектриси двох кутів перпендикулярні, то ці кути суміжні", False),
                       (r"Якщо $OA \perp OB$ і $OC \perp OB$, то точки $A$, $O$, $C$ лежать на одній прямій", True),
                       (r"Кут між прямими може дорівнювати $90^\circ$, навіть якщо прямі не перпендикулярні", False)],
        "solution": r"1) Серед будь-яких трьох із чотирьох кутів є два суміжні; рівні суміжні кути — по $90^\circ$. "
                    r"2) Ні: наприклад, кути по $20^\circ$, бісектриси яких — промені $OK$ і $OL$, де $OK \perp OL$: ці кути не мають спільної сторони, тож не суміжні. "
                    r"3) Так: прямі $OA$ і $OC$ перпендикулярні до прямої $OB$ у точці $O$, а така пряма лише одна — вони збігаються "
                    r"(промені $OA$ і $OC$ або збігаються, або доповнюють один одного). "
                    r"4) Ні: кут $90^\circ$ між прямими — це й означає перпендикулярність.",
    },
    # ==========================================
    # УЛЬТРА-БОСИ (difficulty 5)
    # ==========================================
    {
        "type": "SHORT", "difficulty": 5, "skill": "MODEL",
        "text": r"Скільки разів від 0:00 до 12:00 (не враховуючи самих цих моментів) стрілки годинника лежать на перпендикулярних прямих?",
        "answer": "22",
        "solution": r"Хвилинна стрілка проходить $360^\circ$ за $60$ хв, тобто $6^\circ$ за хвилину, годинна — $30^\circ$ за $60$ хв, тобто $0{,}5^\circ$. "
                    r"Хвилинна «обганяє» годинну на $5{,}5^\circ$ щохвилини, і за $12$ годин ($720$ хв) — на $5{,}5 \cdot 720 = 3960^\circ = 11 \cdot 360^\circ$, "
                    r"тобто робить $11$ повних обертів відносно годинної. За кожен такий оберт кут між стрілками двічі буває прямим "
                    r"(хвилинна попереду на $90^\circ$ і на $270^\circ$). Отже, $11 \cdot 2 = 22$ рази.",
    },
    {
        "type": "SHORT", "difficulty": 5, "skill": "SOLVE",
        "text": r"Чотири різні прямі $a$, $b$, $c$, $d$ проходять через одну точку $O$, $a \perp c$, $b \perp d$, "
                r"кут між прямими $a$ і $b$ дорівнює $40^\circ$. Знайдіть кут між прямими $c$ і $d$ (у градусах).",
        "answer": "40",
        "solution": r"Відкладатимемо кути від променя прямої $a$ проти годинникової стрілки. Пряма $c \perp a$ йде під кутом $90^\circ$. "
                    r"Пряма $b$ утворює з $a$ кут $40^\circ$ — її промінь під кутом $40^\circ$ (або $140^\circ$, тобто $-40^\circ$). "
                    r"Тоді $d \perp b$ — під кутом $40^\circ + 90^\circ = 130^\circ$ (або $50^\circ$). "
                    r"Між $c$ ($90^\circ$) і $d$ — $130^\circ - 90^\circ = 40^\circ$ (або $90^\circ - 50^\circ = 40^\circ$). Відповідь: $40^\circ$.",
    },
]
