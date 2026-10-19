TOPIC_NAME = "2.3. Паралельні прямі. Ознаки паралельності"
COURSE = "Геометрія (7-9 класи)"
GRADE = "7 клас"

# Нумерація кутів на малюнках — як в уроці: при прямій a — 1 (угорі ліворуч від c), 2 (угорі праворуч),
# 3 (унизу ліворуч), 4 (унизу праворуч); при прямій b — 5, 6, 7, 8 так само.
# Відповідні: 1 і 5, 2 і 6, 3 і 7, 4 і 8. Внутрішні різносторонні: 3 і 6, 4 і 5. Внутрішні односторонні: 3 і 5, 4 і 6.

TASKS = [
    # ==========================================
    # СХОДИНКА 1 — БАЗОВИЙ
    # ==========================================
    # --- Моделювання ---
    {
        "type": "CHOICE", "difficulty": 1, "skill": "MODEL",
        "text": r"Прямі $a$ і $b$ перетнуто січною $c$ (див. малюнок). Який кут є відповідним до $\angle 2$?",
        "svg_code": '<svg xmlns="http://www.w3.org/2000/svg" width="360" height="260" viewBox="0 0 360 260" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" font-family="sans-serif"><line x1="14.0" y1="75.0" x2="346.0" y2="75.0"/><line x1="14.0" y1="185.0" x2="346.0" y2="185.0"/><line x1="125.9" y1="246.0" x2="234.1" y2="14.0"/><circle cx="205.6" cy="75.0" r="3.5" fill="currentColor" stroke="none"/><circle cx="154.4" cy="185.0" r="3.5" fill="currentColor" stroke="none"/><text x="334.0" y="68.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">a</text><text x="334.0" y="178.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">b</text><text x="240.8" y="36.4" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">c</text><text x="194.9" y="63.1" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">1</text><text x="222.5" y="69.3" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">2</text><text x="188.8" y="90.7" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">3</text><text x="216.4" y="96.9" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">4</text><text x="143.6" y="173.1" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">5</text><text x="171.2" y="179.3" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">6</text><text x="137.5" y="200.7" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">7</text><text x="165.1" y="206.9" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">8</text></svg>',
        "options": [(r"$\angle 6$", True), (r"$\angle 3$", False), (r"$\angle 5$", False), (r"$\angle 7$", False), (r"$\angle 8$", False)],
        "hint": r"Відповідні кути розташовані однаково: один при $a$, другий при $b$, з того самого боку від $c$ і від своєї прямої.",
        "solution": r"$\angle 2$ лежить над прямою $a$ праворуч від $c$. При прямій $b$ так само розташований $\angle 6$. ($\angle 3$ — вертикальний до $\angle 2$, а не відповідний.)",
    },
    {
        "type": "GROUP", "difficulty": 1, "skill": "MODEL",
        "text": r"Розподіліть пари кутів (див. малюнок) за видом.",
        "svg_code": '<svg xmlns="http://www.w3.org/2000/svg" width="360" height="260" viewBox="0 0 360 260" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" font-family="sans-serif"><line x1="14.0" y1="75.0" x2="346.0" y2="75.0"/><line x1="14.0" y1="185.0" x2="346.0" y2="185.0"/><line x1="125.9" y1="246.0" x2="234.1" y2="14.0"/><circle cx="205.6" cy="75.0" r="3.5" fill="currentColor" stroke="none"/><circle cx="154.4" cy="185.0" r="3.5" fill="currentColor" stroke="none"/><text x="334.0" y="68.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">a</text><text x="334.0" y="178.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">b</text><text x="240.8" y="36.4" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">c</text><text x="194.9" y="63.1" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">1</text><text x="222.5" y="69.3" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">2</text><text x="188.8" y="90.7" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">3</text><text x="216.4" y="96.9" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">4</text><text x="143.6" y="173.1" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">5</text><text x="171.2" y="179.3" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">6</text><text x="137.5" y="200.7" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">7</text><text x="165.1" y="206.9" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">8</text></svg>',
        "groups": ["Відповідні", "Внутрішні різносторонні", "Внутрішні односторонні"],
        "items": [(r"$\angle 1$ і $\angle 5$", 0), (r"$\angle 3$ і $\angle 6$", 1), (r"$\angle 4$ і $\angle 6$", 2),
                  (r"$\angle 4$ і $\angle 8$", 0), (r"$\angle 4$ і $\angle 5$", 1), (r"$\angle 3$ і $\angle 5$", 2)],
        "hint": r"Внутрішні кути лежать між прямими $a$ і $b$. Далі дивіться: з одного чи з різних боків від січної $c$.",
        "solution": r"Відповідні: $1$ і $5$, $4$ і $8$. Внутрішні кути — $3, 4, 5, 6$: по різні боки від $c$ — $3$ і $6$, $4$ і $5$ (різносторонні); з одного боку — $3$ і $5$, $4$ і $6$ (односторонні).",
    },
    {
        "type": "TF", "difficulty": 1, "skill": "MODEL",
        "text": r"Правда чи ні (за малюнком)?",
        "svg_code": '<svg xmlns="http://www.w3.org/2000/svg" width="360" height="260" viewBox="0 0 360 260" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" font-family="sans-serif"><line x1="14.0" y1="75.0" x2="346.0" y2="75.0"/><line x1="14.0" y1="185.0" x2="346.0" y2="185.0"/><line x1="125.9" y1="246.0" x2="234.1" y2="14.0"/><circle cx="205.6" cy="75.0" r="3.5" fill="currentColor" stroke="none"/><circle cx="154.4" cy="185.0" r="3.5" fill="currentColor" stroke="none"/><text x="334.0" y="68.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">a</text><text x="334.0" y="178.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">b</text><text x="240.8" y="36.4" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">c</text><text x="194.9" y="63.1" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">1</text><text x="222.5" y="69.3" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">2</text><text x="188.8" y="90.7" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">3</text><text x="216.4" y="96.9" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">4</text><text x="143.6" y="173.1" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">5</text><text x="171.2" y="179.3" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">6</text><text x="137.5" y="200.7" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">7</text><text x="165.1" y="206.9" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">8</text></svg>',
        "statements": [
            (r"$\angle 3$ і $\angle 6$ лежать між прямими $a$ і $b$", True),
            (r"$\angle 1$ і $\angle 5$ лежать з одного боку від січної $c$", True),
            (r"$\angle 4$ і $\angle 5$ — внутрішні односторонні кути", False),
            (r"$\angle 2$ — внутрішній кут", False),
        ],
        "hint": r"Внутрішні кути — ті, що між $a$ і $b$: $\angle 3$, $\angle 4$, $\angle 5$, $\angle 6$.",
        "solution": r"$\angle 3$ і $\angle 6$ — внутрішні, так. $\angle 1$ і $\angle 5$ — обидва ліворуч від $c$, так. $\angle 4$ і $\angle 5$ — по різні боки від $c$, тобто різносторонні. $\angle 2$ лежить над прямою $a$, поза смугою між $a$ і $b$ — він зовнішній.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "MODEL",
        "text": r"Відомо, що $\angle 3 = \angle 6$ (див. малюнок). На яку ознаку треба послатися, щоб довести, що $a \parallel b$?",
        "svg_code": '<svg xmlns="http://www.w3.org/2000/svg" width="360" height="260" viewBox="0 0 360 260" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" font-family="sans-serif"><line x1="14.0" y1="75.0" x2="346.0" y2="75.0"/><line x1="14.0" y1="185.0" x2="346.0" y2="185.0"/><line x1="125.9" y1="246.0" x2="234.1" y2="14.0"/><circle cx="205.6" cy="75.0" r="3.5" fill="currentColor" stroke="none"/><circle cx="154.4" cy="185.0" r="3.5" fill="currentColor" stroke="none"/><text x="334.0" y="68.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">a</text><text x="334.0" y="178.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">b</text><text x="240.8" y="36.4" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">c</text><text x="194.9" y="63.1" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">1</text><text x="222.5" y="69.3" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">2</text><text x="188.8" y="90.7" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">3</text><text x="216.4" y="96.9" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">4</text><text x="143.6" y="173.1" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">5</text><text x="171.2" y="179.3" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">6</text><text x="137.5" y="200.7" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">7</text><text x="165.1" y="206.9" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">8</text></svg>',
        "options": [
            (r"Внутрішні різносторонні кути рівні", True),
            (r"Відповідні кути рівні", False),
            (r"Сума внутрішніх односторонніх кутів дорівнює $180^\circ$", False),
            (r"Вертикальні кути рівні", False),
            (r"Дві прямі, перпендикулярні до третьої, паралельні", False),
        ],
        "hint": r"Визначте, яку пару утворюють $\angle 3$ і $\angle 6$.",
        "solution": r"$\angle 3$ і $\angle 6$ лежать між $a$ і $b$ по різні боки від $c$ — це внутрішні різносторонні кути. Вони рівні, тож $a \parallel b$ за ознакою.",
    },
    {
        "type": "MULTI", "difficulty": 1, "skill": "MODEL",
        "text": r"Які з умов гарантують, що $a \parallel b$ (див. малюнок)? Позначте всі правильні.",
        "svg_code": '<svg xmlns="http://www.w3.org/2000/svg" width="360" height="260" viewBox="0 0 360 260" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" font-family="sans-serif"><line x1="14.0" y1="75.0" x2="346.0" y2="75.0"/><line x1="14.0" y1="185.0" x2="346.0" y2="185.0"/><line x1="125.9" y1="246.0" x2="234.1" y2="14.0"/><circle cx="205.6" cy="75.0" r="3.5" fill="currentColor" stroke="none"/><circle cx="154.4" cy="185.0" r="3.5" fill="currentColor" stroke="none"/><text x="334.0" y="68.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">a</text><text x="334.0" y="178.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">b</text><text x="240.8" y="36.4" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">c</text><text x="194.9" y="63.1" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">1</text><text x="222.5" y="69.3" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">2</text><text x="188.8" y="90.7" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">3</text><text x="216.4" y="96.9" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">4</text><text x="143.6" y="173.1" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">5</text><text x="171.2" y="179.3" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">6</text><text x="137.5" y="200.7" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">7</text><text x="165.1" y="206.9" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">8</text></svg>',
        "options": [
            (r"$\angle 1 = \angle 5$", True),
            (r"$\angle 4 = \angle 5$", True),
            (r"$\angle 3 + \angle 5 = 180^\circ$", True),
            (r"$\angle 3 = \angle 5$", False),
            (r"$\angle 2 = \angle 3$", False),
        ],
        "hint": r"Для кожної умови визначте вид пари кутів і пригадайте відповідну ознаку.",
        "solution": r"$1$ і $5$ — відповідні (рівні — ознака). $4$ і $5$ — внутрішні різносторонні (рівні — ознака). $3$ і $5$ — внутрішні односторонні: ознака — сума $180^\circ$, а не рівність. $\angle 2 = \angle 3$ завжди (вертикальні) — про пряму $b$ це нічого не каже.",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"Яким має бути $\angle 5$ (див. малюнок), щоб $a \parallel b$? Відповідь дайте в градусах.",
        "svg_code": '<svg xmlns="http://www.w3.org/2000/svg" width="360" height="260" viewBox="0 0 360 260" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" font-family="sans-serif"><path d="M160.0 75.0 L140.0 75.0 A20 20 0 0 0 166.8 93.8 Z" fill="currentColor" fill-opacity="0.18" stroke="none"/><path d="M200.0 185.0 L193.2 166.2 A20 20 0 0 0 180.0 185.0 Z" fill="currentColor" fill-opacity="0.18" stroke="none"/><line x1="14.0" y1="75.0" x2="346.0" y2="75.0"/><line x1="14.0" y1="185.0" x2="346.0" y2="185.0"/><line x1="222.2" y1="246.0" x2="137.8" y2="14.0"/><circle cx="160.0" cy="75.0" r="3.5" fill="currentColor" stroke="none"/><circle cx="200.0" cy="185.0" r="3.5" fill="currentColor" stroke="none"/><text x="334.0" y="68.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">a</text><text x="334.0" y="178.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">b</text><text x="129.7" y="35.7" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">c</text><text x="140.5" y="107.9" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">110°</text><text x="172.2" y="170.5" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">5</text></svg>',
        "answer": "70",
        "hint": r"Кут $110^\circ$ і $\angle 5$ лежать між $a$ і $b$ з одного боку від $c$ — це внутрішні односторонні кути.",
        "solution": r"Для внутрішніх односторонніх кутів ознака — сума $180^\circ$: $\angle 5 = 180^\circ - 110^\circ = 70^\circ$.",
    },
    {
        "type": "FIELDS", "difficulty": 1, "skill": "SOLVE",
        "text": r"Якими мають бути кути $5$ і $6$ (див. малюнок), щоб $a \parallel b$? Відповіді дайте в градусах.",
        "svg_code": '<svg xmlns="http://www.w3.org/2000/svg" width="360" height="260" viewBox="0 0 360 260" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" font-family="sans-serif"><path d="M205.6 75.0 L197.2 93.1 A20 20 0 0 0 225.6 75.0 Z" fill="currentColor" fill-opacity="0.18" stroke="none"/><path d="M154.4 185.0 L162.8 166.9 A20 20 0 0 0 134.4 185.0 Z" fill="currentColor" fill-opacity="0.18" stroke="none"/><path d="M154.4 185.0 L174.4 185.0 A20 20 0 0 0 162.8 166.9 Z" fill="currentColor" fill-opacity="0.18" stroke="none"/><line x1="14.0" y1="75.0" x2="346.0" y2="75.0"/><line x1="14.0" y1="185.0" x2="346.0" y2="185.0"/><line x1="125.9" y1="246.0" x2="234.1" y2="14.0"/><circle cx="205.6" cy="75.0" r="3.5" fill="currentColor" stroke="none"/><circle cx="154.4" cy="185.0" r="3.5" fill="currentColor" stroke="none"/><text x="334.0" y="68.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">a</text><text x="334.0" y="178.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">b</text><text x="240.8" y="36.4" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">c</text><text x="223.9" y="108.7" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">115°</text><text x="136.1" y="161.3" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">5</text><text x="183.0" y="171.7" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">6</text></svg>',
        "fields": [(r"$\angle 5 =$", "115"), (r"$\angle 6 =$", "65")],
        "hint": r"З кутом $115^\circ$ кут $5$ утворює пару внутрішніх різносторонніх кутів, а кут $6$ — внутрішніх односторонніх.",
        "solution": r"Різносторонні мають бути рівні: $\angle 5 = 115^\circ$. Односторонні в сумі $180^\circ$: $\angle 6 = 180^\circ - 115^\circ = 65^\circ$.",
    },
    {
        "type": "ORDER", "difficulty": 1, "skill": "SOLVE",
        "text": r"Розташуйте кроки доведення паралельності прямих $a$ і $b$ у правильному порядку.",
        "items": [
            r"Знайти січну, при якій дано кути",
            r"Визначити вид пари кутів (за потреби перейти до вертикального чи суміжного кута)",
            r"Перевірити рівність кутів або суму $180^\circ$",
            r"Послатися на ознаку й записати $a \parallel b$",
        ],
        "hint": r"Спершу треба зрозуміти, про які кути йдеться, і лише потім щось перевіряти.",
        "solution": r"Січна → вид пари кутів → перевірка умови ознаки → висновок $a \parallel b$.",
    },
    {
        "type": "MULTI", "difficulty": 1, "skill": "SOLVE",
        "text": r"Один із кутів при прямій $a$ дорівнює $70^\circ$ (див. малюнок). Яка з рівностей для кутів при прямій $b$ гарантує, що $a \parallel b$? Позначте всі правильні.",
        "svg_code": '<svg xmlns="http://www.w3.org/2000/svg" width="360" height="260" viewBox="0 0 360 260" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" font-family="sans-serif"><path d="M200.0 75.0 L180.0 75.0 A20 20 0 0 0 193.2 93.8 Z" fill="currentColor" fill-opacity="0.18" stroke="none"/><line x1="14.0" y1="75.0" x2="346.0" y2="75.0"/><line x1="14.0" y1="185.0" x2="346.0" y2="185.0"/><line x1="137.8" y1="246.0" x2="222.2" y2="14.0"/><circle cx="200.0" cy="75.0" r="3.5" fill="currentColor" stroke="none"/><circle cx="160.0" cy="185.0" r="3.5" fill="currentColor" stroke="none"/><text x="334.0" y="68.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">a</text><text x="334.0" y="178.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">b</text><text x="230.3" y="35.7" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">c</text><text x="188.5" y="63.6" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">1</text><text x="216.4" y="68.5" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">2</text><text x="172.2" y="99.5" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">70°</text><text x="211.5" y="96.4" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">4</text><text x="148.5" y="173.6" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">5</text><text x="176.4" y="178.5" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">6</text><text x="143.6" y="201.5" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">7</text><text x="171.5" y="206.4" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">8</text></svg>',
        "options": [
            (r"$\angle 6 = 70^\circ$", True),
            (r"$\angle 5 = 110^\circ$", True),
            (r"$\angle 7 = 70^\circ$", True),
            (r"$\angle 5 = 70^\circ$", False),
            (r"$\angle 6 = 110^\circ$", False),
        ],
        "hint": r"Кут $70^\circ$ стоїть на місці $\angle 3$. Знайдіть кути, що утворюють з ним відомі пари.",
        "solution": r"Кут $70^\circ$ (на місці $\angle 3$) з $\angle 6$ — внутрішні різносторонні: потрібно $70^\circ$. З $\angle 5$ — внутрішні односторонні: потрібно $180^\circ - 70^\circ = 110^\circ$. З $\angle 7$ — відповідні: потрібно $70^\circ$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"Пряма $c$ перпендикулярна до прямої $a$ і перетинає пряму $b$. Яким має бути кут між прямими $b$ і $c$, щоб $a \parallel b$? Відповідь дайте в градусах.",
        "answer": "90",
        "hint": r"Пригадайте наслідок з ознак паралельності про дві прямі, перпендикулярні до третьої.",
        "solution": r"Якщо $b \perp c$, то $a$ і $b$ перпендикулярні до однієї прямої $c$, отже, $a \parallel b$. Кут має бути $90^\circ$.",
    },
    # --- Аналіз результатів ---
    {
        "type": "TF", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [
            (r"Паралельні прямі не мають спільних точок", True),
            (r"Через точку поза прямою можна провести дві різні прямі, паралельні їй", False),
            (r"Дві прямі, перпендикулярні до третьої прямої, паралельні", True),
            (r"Якщо два відрізки не перетинаються, то вони лежать на паралельних прямих", False),
        ],
        "hint": r"Пригадайте означення паралельних прямих і аксіому паралельності.",
        "solution": r"Паралельні прямі за означенням не перетинаються — так. За аксіомою через точку поза прямою проходить лише одна паралельна — ні. Наслідок з ознак — так. Відрізки можуть не перетинатися, а їхні прямі перетнуться далі — ні.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Внутрішні односторонні кути при прямих $a$, $b$ і січній $c$ дорівнюють $70^\circ$ і $70^\circ$. Сашко каже: «Кути рівні — отже, $a \parallel b$». Чи правий він?",
        "options": [
            (r"Ні: для односторонніх кутів ознака вимагає суми $180^\circ$, а $70^\circ + 70^\circ = 140^\circ$", True),
            (r"Так: рівність кутів — ознака паралельності", False),
            (r"Так: обидва кути гострі", False),
            (r"Ні: ознака стосується лише відповідних кутів", False),
        ],
        "hint": r"Яка умова в ознаці саме для внутрішніх односторонніх кутів?",
        "solution": r"Рівність потрібна для відповідних і для різносторонніх кутів. Для односторонніх ознака — сума $180^\circ$, а тут $140^\circ$. Висновок Сашка не обґрунтований.",
    },
    {
        "type": "ERROR", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Іра перевіряє, чи можна стверджувати, що $a \parallel b$, якщо $\angle 3 = 100^\circ$, $\angle 5 = 80^\circ$ (див. малюнок). У якому кроці перша помилка?",
        "svg_code": '<svg xmlns="http://www.w3.org/2000/svg" width="360" height="260" viewBox="0 0 360 260" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" font-family="sans-serif"><line x1="14.0" y1="75.0" x2="346.0" y2="75.0"/><line x1="14.0" y1="185.0" x2="346.0" y2="185.0"/><line x1="125.9" y1="246.0" x2="234.1" y2="14.0"/><circle cx="205.6" cy="75.0" r="3.5" fill="currentColor" stroke="none"/><circle cx="154.4" cy="185.0" r="3.5" fill="currentColor" stroke="none"/><text x="334.0" y="68.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">a</text><text x="334.0" y="178.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">b</text><text x="240.8" y="36.4" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">c</text><text x="194.9" y="63.1" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">1</text><text x="222.5" y="69.3" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">2</text><text x="188.8" y="90.7" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">3</text><text x="216.4" y="96.9" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">4</text><text x="143.6" y="173.1" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">5</text><text x="171.2" y="179.3" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">6</text><text x="137.5" y="200.7" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">7</text><text x="165.1" y="206.9" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">8</text></svg>',
        "steps": [
            r"$\angle 3$ і $\angle 5$ — внутрішні односторонні кути",
            r"$\angle 3 + \angle 5 = 100^\circ + 80^\circ = 180^\circ$",
            r"Для паралельності внутрішні односторонні кути мають бути рівними",
            r"Отже, ознака не виконується",
        ],
        "wrong": 2,
        "hint": r"Звірте третій крок з ознакою паралельності.",
        "solution": r"Для внутрішніх односторонніх кутів ознака — сума $180^\circ$, а не рівність. Сума справді $180^\circ$, тому $a \parallel b$.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Відрізки $AB$ і $CD$ на малюнку не мають спільних точок. Чи можна стверджувати, що прямі $AB$ і $CD$ паралельні?",
        "svg_code": '<svg xmlns="http://www.w3.org/2000/svg" width="360" height="200" viewBox="0 0 360 200" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" font-family="sans-serif"><line x1="30.0" y1="45.0" x2="220.0" y2="70.0"/><line x1="30.0" y1="160.0" x2="220.0" y2="130.0"/><circle cx="30.0" cy="45.0" r="3.5" fill="currentColor" stroke="none"/><circle cx="220.0" cy="70.0" r="3.5" fill="currentColor" stroke="none"/><circle cx="30.0" cy="160.0" r="3.5" fill="currentColor" stroke="none"/><circle cx="220.0" cy="130.0" r="3.5" fill="currentColor" stroke="none"/><text x="26.0" y="36.0" fill="currentColor" stroke="none" font-size="16" font-weight="700" text-anchor="middle">A</text><text x="226.0" y="61.0" fill="currentColor" stroke="none" font-size="16" font-weight="700" text-anchor="middle">B</text><text x="26.0" y="183.0" fill="currentColor" stroke="none" font-size="16" font-weight="700" text-anchor="middle">C</text><text x="226.0" y="153.0" fill="currentColor" stroke="none" font-size="16" font-weight="700" text-anchor="middle">D</text></svg>',
        "options": [
            (r"Ні: прямі можуть перетнутися за межами відрізків", True),
            (r"Так: у відрізків немає спільних точок", False),
            (r"Так, якщо відрізки мають однакову довжину", False),
            (r"Ні: паралельними бувають лише горизонтальні прямі", False),
        ],
        "hint": r"Паралельність — властивість прямих, а прямі нескінченні.",
        "solution": r"Прямі $AB$ і $CD$ продовжуються за точки $B$ і $D$ і можуть перетнутися (на малюнку — праворуч від них). Відсутність спільних точок у відрізків нічого не гарантує.",
    },
    {
        "type": "TF", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Чи можна за цими даними стверджувати, що $a \parallel b$ (див. малюнок)? «Так» — можна, «Ні» — не можна.",
        "svg_code": '<svg xmlns="http://www.w3.org/2000/svg" width="360" height="260" viewBox="0 0 360 260" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" font-family="sans-serif"><line x1="14.0" y1="75.0" x2="346.0" y2="75.0"/><line x1="14.0" y1="185.0" x2="346.0" y2="185.0"/><line x1="125.9" y1="246.0" x2="234.1" y2="14.0"/><circle cx="205.6" cy="75.0" r="3.5" fill="currentColor" stroke="none"/><circle cx="154.4" cy="185.0" r="3.5" fill="currentColor" stroke="none"/><text x="334.0" y="68.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">a</text><text x="334.0" y="178.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">b</text><text x="240.8" y="36.4" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">c</text><text x="194.9" y="63.1" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">1</text><text x="222.5" y="69.3" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">2</text><text x="188.8" y="90.7" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">3</text><text x="216.4" y="96.9" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">4</text><text x="143.6" y="173.1" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">5</text><text x="171.2" y="179.3" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">6</text><text x="137.5" y="200.7" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">7</text><text x="165.1" y="206.9" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">8</text></svg>',
        "statements": [
            (r"$\angle 1 = \angle 5 = 118^\circ$", True),
            (r"$\angle 4 = 110^\circ$, $\angle 6 = 75^\circ$", False),
            (r"$\angle 3 = \angle 6 = 63^\circ$", True),
            (r"$\angle 3 = 66^\circ$, $\angle 5 = 114^\circ$", True),
            (r"$\angle 2 = \angle 3 = 64^\circ$", False),
        ],
        "hint": r"Для кожної пари визначте її вид: відповідні, різносторонні чи односторонні.",
        "solution": r"$1$ і $5$ — відповідні, рівні — так. $4$ і $6$ — односторонні: $110^\circ + 75^\circ = 185^\circ \ne 180^\circ$ — ні. $3$ і $6$ — різносторонні, рівні — так. $3$ і $5$ — односторонні: $66^\circ + 114^\circ = 180^\circ$ — так. $2$ і $3$ — вертикальні, вони рівні завжди — ні.",
    },

    # ==========================================
    # СХОДИНКА 2 — СЕРЕДНІЙ
    # ==========================================
    # --- Моделювання ---
    {
        "type": "MATCH", "difficulty": 2, "skill": "MODEL",
        "text": r"Установіть відповідність між умовою (1–3) та твердженням (А–Д), на яке треба послатися, щоб довести $a \parallel b$ (див. малюнок).",
        "svg_code": '<svg xmlns="http://www.w3.org/2000/svg" width="360" height="260" viewBox="0 0 360 260" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" font-family="sans-serif"><line x1="14.0" y1="75.0" x2="346.0" y2="75.0"/><line x1="14.0" y1="185.0" x2="346.0" y2="185.0"/><line x1="125.9" y1="246.0" x2="234.1" y2="14.0"/><circle cx="205.6" cy="75.0" r="3.5" fill="currentColor" stroke="none"/><circle cx="154.4" cy="185.0" r="3.5" fill="currentColor" stroke="none"/><text x="334.0" y="68.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">a</text><text x="334.0" y="178.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">b</text><text x="240.8" y="36.4" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">c</text><text x="194.9" y="63.1" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">1</text><text x="222.5" y="69.3" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">2</text><text x="188.8" y="90.7" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">3</text><text x="216.4" y="96.9" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">4</text><text x="143.6" y="173.1" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">5</text><text x="171.2" y="179.3" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">6</text><text x="137.5" y="200.7" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">7</text><text x="165.1" y="206.9" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">8</text></svg>',
        "options": [
            r"А) внутрішні різносторонні кути рівні",
            r"Б) відповідні кути рівні",
            r"В) сума внутрішніх односторонніх кутів дорівнює $180^\circ$",
            r"Г) вертикальні кути рівні",
            r"Д) дві прямі, перпендикулярні до третьої, паралельні",
        ],
        "matches": [
            (r"1. $\angle 4 = \angle 5$", r"А) внутрішні різносторонні кути рівні"),
            (r"2. $\angle 3 + \angle 5 = 180^\circ$", r"В) сума внутрішніх односторонніх кутів дорівнює $180^\circ$"),
            (r"3. $\angle 2 = \angle 6$", r"Б) відповідні кути рівні"),
        ],
        "solution": r"$4$ і $5$ — внутрішні різносторонні; $3$ і $5$ — внутрішні односторонні; $2$ і $6$ — відповідні. «Вертикальні кути рівні» — не ознака паралельності, а наслідок Д тут не потрібен.",
    },
    {
        "type": "FIELDS", "difficulty": 2, "skill": "MODEL",
        "text": r"Внутрішні односторонні кути при прямих $a$, $b$ і січній $c$ відносяться як $2 : 3$. Якими мають бути ці кути, щоб $a \parallel b$? Відповіді дайте в градусах.",
        "fields": [(r"Менший кут:", "72"), (r"Більший кут:", "108")],
        "hint": r"Позначте кути $2x$ і $3x$. Якою має бути їхня сума?",
        "solution": r"Для паралельності $2x + 3x = 180^\circ$, $5x = 180^\circ$, $x = 36^\circ$. Кути: $72^\circ$ і $108^\circ$.",
    },
    {
        "type": "EXPR", "difficulty": 2, "skill": "MODEL",
        "text": r"$\angle 3$ і $\angle 5$ — внутрішні односторонні кути при прямих $a$, $b$ і січній $c$, $\angle 3 = x^\circ$. Запишіть вираз для величини $\angle 5$ (у градусах), при якій $a \parallel b$.",
        "answer": "180-x", "vars": ["x"],
        "hint": r"Яку умову ознака ставить для внутрішніх односторонніх кутів?",
        "solution": r"Потрібно $\angle 3 + \angle 5 = 180^\circ$, тобто $\angle 5 = 180 - x$ градусів.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "MODEL",
        "text": r"Один із внутрішніх односторонніх кутів на $40^\circ$ більший за інший. Менший кут позначили $x$. Яке рівняння дає кути, при яких $a \parallel b$?",
        "options": [
            (r"$x + (x + 40^\circ) = 180^\circ$", True),
            (r"$x = x + 40^\circ$", False),
            (r"$x + 40^\circ = 180^\circ$", False),
            (r"$x + (x + 40^\circ) = 90^\circ$", False),
            (r"$x + (x - 40^\circ) = 180^\circ$", False),
        ],
        "hint": r"Більший кут — $x + 40^\circ$. Що має виконуватися для односторонніх кутів?",
        "solution": r"Кути $x$ і $x + 40^\circ$; для паралельності їхня сума $180^\circ$: $x + (x + 40^\circ) = 180^\circ$ (тоді кути $70^\circ$ і $110^\circ$).",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "MODEL",
        "text": r"Столяр перевіряє, чи паралельні краї двох планок. Він кладе поперек обох планок лінійку і вимірює два кути між лінійкою та краями планок — обидва між планками з одного боку від лінійки. Один кут дорівнює $87^\circ$. Яким має бути другий, щоб краї були паралельні? Відповідь дайте в градусах.",
        "answer": "93",
        "hint": r"Лінійка — січна. Які це кути: відповідні, різносторонні чи односторонні?",
        "solution": r"Кути між планками з одного боку від лінійки — внутрішні односторонні. Їхня сума має бути $180^\circ$: $180^\circ - 87^\circ = 93^\circ$.",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Яким має бути $\angle 2$ (див. малюнок), щоб $a \parallel b$? Відповідь дайте в градусах.",
        "svg_code": '<svg xmlns="http://www.w3.org/2000/svg" width="360" height="260" viewBox="0 0 360 260" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" font-family="sans-serif"><path d="M209.2 75.0 L218.6 57.3 A20 20 0 0 0 189.2 75.0 Z" fill="currentColor" fill-opacity="0.18" stroke="none"/><path d="M150.8 185.0 L130.8 185.0 A20 20 0 0 0 141.4 202.7 Z" fill="currentColor" fill-opacity="0.18" stroke="none"/><line x1="14.0" y1="75.0" x2="346.0" y2="75.0"/><line x1="14.0" y1="185.0" x2="346.0" y2="185.0"/><line x1="118.3" y1="246.0" x2="241.7" y2="14.0"/><circle cx="209.2" cy="75.0" r="3.5" fill="currentColor" stroke="none"/><circle cx="150.8" cy="185.0" r="3.5" fill="currentColor" stroke="none"/><text x="334.0" y="68.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">a</text><text x="334.0" y="178.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">b</text><text x="247.5" y="36.7" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">c</text><text x="191.7" y="50.9" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">118°</text><text x="121.6" y="207.5" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">2</text></svg>',
        "answer": "62",
        "hint": r"Знайдіть при прямій $b$ кут, відповідний до кута $118^\circ$. Як він пов'язаний з $\angle 2$?",
        "solution": r"Кут, відповідний до кута $118^\circ$, лежить над прямою $b$ ліворуч від $c$; він суміжний з $\angle 2$. Щоб він дорівнював $118^\circ$, треба $\angle 2 = 180^\circ - 118^\circ = 62^\circ$.",
    },
    {
        "type": "GROUP", "difficulty": 2, "skill": "SOLVE",
        "text": r"Кут при прямій $a$ дорівнює $50^\circ$ (див. малюнок). Якими мають бути кути $5$, $6$, $7$, $8$, щоб $a \parallel b$? Розподіліть їх.",
        "svg_code": '<svg xmlns="http://www.w3.org/2000/svg" width="360" height="260" viewBox="0 0 360 260" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" font-family="sans-serif"><path d="M226.2 75.0 L246.2 75.0 A20 20 0 0 0 239.0 59.7 Z" fill="currentColor" fill-opacity="0.18" stroke="none"/><line x1="14.0" y1="75.0" x2="346.0" y2="75.0"/><line x1="14.0" y1="185.0" x2="346.0" y2="185.0"/><line x1="82.7" y1="246.0" x2="277.3" y2="14.0"/><circle cx="226.2" cy="75.0" r="3.5" fill="currentColor" stroke="none"/><circle cx="133.8" cy="185.0" r="3.5" fill="currentColor" stroke="none"/><text x="334.0" y="68.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">a</text><text x="334.0" y="178.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">b</text><text x="279.6" y="37.5" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">c</text><text x="257.0" y="65.6" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">50°</text><text x="125.4" y="171.9" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">5</text><text x="152.0" y="181.5" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">6</text><text x="115.7" y="198.5" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">7</text><text x="142.3" y="208.1" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">8</text></svg>',
        "groups": [r"$50^\circ$", r"$130^\circ$"],
        "items": [(r"$\angle 5$", 1), (r"$\angle 6$", 0), (r"$\angle 7$", 0), (r"$\angle 8$", 1)],
        "hint": r"Спершу знайдіть кут, відповідний до кута $50^\circ$, а решту — через вертикальні й суміжні кути.",
        "solution": r"Відповідний до $50^\circ$ кут $\angle 6 = 50^\circ$. Тоді $\angle 7 = \angle 6 = 50^\circ$ (вертикальні), $\angle 5 = \angle 8 = 180^\circ - 50^\circ = 130^\circ$ (суміжні з $\angle 6$).",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Кут $125^\circ$ і $\angle 8$ на малюнку — зовнішні різносторонні кути. Яким має бути $\angle 8$, щоб $a \parallel b$? Відповідь дайте в градусах.",
        "svg_code": '<svg xmlns="http://www.w3.org/2000/svg" width="360" height="260" viewBox="0 0 360 260" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" font-family="sans-serif"><path d="M218.5 75.0 L230.0 58.6 A20 20 0 0 0 198.5 75.0 Z" fill="currentColor" fill-opacity="0.18" stroke="none"/><path d="M141.5 185.0 L130.0 201.4 A20 20 0 0 0 161.5 185.0 Z" fill="currentColor" fill-opacity="0.18" stroke="none"/><line x1="14.0" y1="75.0" x2="346.0" y2="75.0"/><line x1="14.0" y1="185.0" x2="346.0" y2="185.0"/><line x1="98.8" y1="246.0" x2="261.2" y2="14.0"/><circle cx="218.5" cy="75.0" r="3.5" fill="currentColor" stroke="none"/><circle cx="141.5" cy="185.0" r="3.5" fill="currentColor" stroke="none"/><text x="334.0" y="68.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">a</text><text x="334.0" y="178.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">b</text><text x="265.0" y="37.3" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">c</text><text x="202.8" y="49.8" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">125°</text><text x="157.2" y="220.2" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">8</text></svg>',
        "answer": "125",
        "hint": r"Такої пари в ознаках немає. Перейдіть до вертикального кута.",
        "solution": r"Кут, вертикальний до кута $125^\circ$ (під прямою $a$ праворуч від $c$), теж дорівнює $125^\circ$. Він і $\angle 8$ — відповідні кути, тому потрібно $\angle 8 = 125^\circ$.",
    },
    {
        "type": "MULTI", "difficulty": 2, "skill": "SOLVE",
        "text": r"Кут при прямій $b$ дорівнює $74^\circ$ (див. малюнок). Яка з умов для кутів при прямій $a$ гарантує, що $a \parallel b$? Позначте всі правильні.",
        "svg_code": '<svg xmlns="http://www.w3.org/2000/svg" width="360" height="260" viewBox="0 0 360 260" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" font-family="sans-serif"><path d="M195.8 185.0 L190.3 165.8 A20 20 0 0 0 175.8 185.0 Z" fill="currentColor" fill-opacity="0.18" stroke="none"/><line x1="14.0" y1="75.0" x2="346.0" y2="75.0"/><line x1="14.0" y1="185.0" x2="346.0" y2="185.0"/><line x1="213.3" y1="246.0" x2="146.7" y2="14.0"/><circle cx="164.2" cy="75.0" r="3.5" fill="currentColor" stroke="none"/><circle cx="195.8" cy="185.0" r="3.5" fill="currentColor" stroke="none"/><text x="334.0" y="68.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">a</text><text x="334.0" y="178.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">b</text><text x="137.5" y="35.1" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">c</text><text x="148.3" y="68.0" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">1</text><text x="176.3" y="64.0" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">2</text><text x="152.2" y="96.0" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">3</text><text x="180.2" y="92.0" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">4</text><text x="168.6" y="169.5" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">74°</text></svg>',
        "options": [
            (r"$\angle 1 = 74^\circ$", True),
            (r"$\angle 4 = 74^\circ$", True),
            (r"$\angle 2 = 106^\circ$", True),
            (r"$\angle 3 = 74^\circ$", False),
            (r"$\angle 2 = 74^\circ$", False),
        ],
        "hint": r"Кут $74^\circ$ стоїть на місці $\angle 5$. $\angle 2$ у ознаки не входить, але він вертикальний до $\angle 3$.",
        "solution": r"$\angle 1$ і кут $74^\circ$ — відповідні, $\angle 4$ і він — внутрішні різносторонні: потрібно $74^\circ$. $\angle 3$ з ним — односторонні: потрібно $106^\circ$, а не $74^\circ$. $\angle 2 = \angle 3$ (вертикальні), тому $\angle 2 = 106^\circ$ дає $\angle 3 + 74^\circ = 180^\circ$ — так, а $\angle 2 = 74^\circ$ — ні.",
    },
    {
        "type": "ORDER", "difficulty": 2, "skill": "SOLVE",
        "text": r"Дано: $\angle 1 = 123^\circ$, $\angle 2 = 57^\circ$ (див. малюнок). Розташуйте кроки доведення того, що $a \parallel b$.",
        "svg_code": '<svg xmlns="http://www.w3.org/2000/svg" width="360" height="260" viewBox="0 0 360 260" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" font-family="sans-serif"><path d="M215.7 75.0 L204.8 91.8 A20 20 0 0 0 235.7 75.0 Z" fill="currentColor" fill-opacity="0.18" stroke="none"/><path d="M144.3 185.0 L124.3 185.0 A20 20 0 0 0 133.4 201.8 Z" fill="currentColor" fill-opacity="0.18" stroke="none"/><path d="M144.3 185.0 L133.4 201.8 A20 20 0 0 0 164.3 185.0 Z" fill="currentColor" fill-opacity="0.18" stroke="none"/><line x1="14.0" y1="75.0" x2="346.0" y2="75.0"/><line x1="14.0" y1="185.0" x2="346.0" y2="185.0"/><line x1="104.7" y1="246.0" x2="255.3" y2="14.0"/><circle cx="215.7" cy="75.0" r="3.5" fill="currentColor" stroke="none"/><circle cx="144.3" cy="185.0" r="3.5" fill="currentColor" stroke="none"/><text x="334.0" y="68.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">a</text><text x="334.0" y="178.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">b</text><text x="259.7" y="37.1" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">c</text><text x="231.9" y="109.9" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">1</text><text x="114.4" y="206.2" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">2</text><text x="160.5" y="219.9" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">3</text></svg>',
        "items": [
            r"$\angle 2$ і $\angle 3$ — суміжні кути",
            r"$\angle 3 = 180^\circ - 57^\circ = 123^\circ$",
            r"$\angle 1 = \angle 3$, і це відповідні кути",
            r"Отже, $a \parallel b$ за ознакою",
        ],
        "solution": r"$\angle 1$ і $\angle 2$ — не пара з ознак, тому переходимо до суміжного з $\angle 2$ кута $\angle 3 = 123^\circ$. $\angle 1$ і $\angle 3$ — відповідні й рівні, отже, $a \parallel b$.",
    },
    # --- Аналіз результатів ---
    {
        "type": "SHORT", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Внутрішні односторонні кути при прямих $a$, $b$ і січній $c$ рівні між собою. Якою має бути величина кожного з них, щоб $a \parallel b$? Відповідь дайте в градусах.",
        "answer": "90",
        "hint": r"Два рівні кути мають дати в сумі $180^\circ$.",
        "solution": r"Для паралельності $x + x = 180^\circ$, тож $x = 90^\circ$. Рівні односторонні кути дають паралельність лише тоді, коли вони прямі (тоді $a \perp c$ і $b \perp c$).",
    },
    {
        "type": "ERROR", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Тарас розв'язує задачу: «Внутрішні односторонні кути відносяться як $1 : 2$. Якими мають бути ці кути, щоб $a \parallel b$?» У якому кроці помилка?",
        "steps": [
            r"Нехай кути дорівнюють $x$ і $2x$",
            r"Для паралельності $x + 2x = 90^\circ$",
            r"$3x = 90^\circ$, $x = 30^\circ$",
            r"Кути: $30^\circ$ і $60^\circ$",
        ],
        "wrong": 1,
        "solution": r"Сума внутрішніх односторонніх кутів має бути $180^\circ$: $3x = 180^\circ$, $x = 60^\circ$. Кути: $60^\circ$ і $120^\circ$.",
    },
    {
        "type": "TF", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Правда чи ні? Кути — як на малюнку.",
        "svg_code": '<svg xmlns="http://www.w3.org/2000/svg" width="360" height="260" viewBox="0 0 360 260" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" font-family="sans-serif"><line x1="14.0" y1="75.0" x2="346.0" y2="75.0"/><line x1="14.0" y1="185.0" x2="346.0" y2="185.0"/><line x1="125.9" y1="246.0" x2="234.1" y2="14.0"/><circle cx="205.6" cy="75.0" r="3.5" fill="currentColor" stroke="none"/><circle cx="154.4" cy="185.0" r="3.5" fill="currentColor" stroke="none"/><text x="334.0" y="68.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">a</text><text x="334.0" y="178.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">b</text><text x="240.8" y="36.4" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">c</text><text x="194.9" y="63.1" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">1</text><text x="222.5" y="69.3" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">2</text><text x="188.8" y="90.7" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">3</text><text x="216.4" y="96.9" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">4</text><text x="143.6" y="173.1" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">5</text><text x="171.2" y="179.3" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">6</text><text x="137.5" y="200.7" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">7</text><text x="165.1" y="206.9" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">8</text></svg>',
        "statements": [
            (r"Якщо $\angle 1 = \angle 5$, то й $\angle 4 = \angle 5$", True),
            (r"Якщо $\angle 4 = \angle 5$, то $\angle 4 + \angle 6 = 180^\circ$", True),
            (r"Якщо $\angle 4 = \angle 6$, то $a \parallel b$", False),
            (r"Якщо $\angle 3$ і $\angle 5$ обидва тупі, то ознака паралельності для них не виконується", True),
        ],
        "solution": r"$\angle 4 = \angle 1$ (вертикальні), тому $\angle 4 = \angle 5$ — так. $\angle 5 + \angle 6 = 180^\circ$ (суміжні), тож при $\angle 4 = \angle 5$ маємо $\angle 4 + \angle 6 = 180^\circ$ — так. $4$ і $6$ — односторонні, для них потрібна сума $180^\circ$, а не рівність — ні. Два тупі кути в сумі більше за $180^\circ$ — так.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Внутрішні різносторонні кути при прямих $a$, $b$ і січній $c$ дорівнюють $52^\circ$ і $128^\circ$. Петро каже: «У сумі $180^\circ$ — отже, $a \parallel b$». Чи правий Петро?",
        "options": [
            (r"Ні: для різносторонніх кутів ознака вимагає рівності, а $52^\circ \ne 128^\circ$", True),
            (r"Так: сума $180^\circ$ — ознака паралельності", False),
            (r"Так: будь-які два кути із сумою $180^\circ$ дають паралельність", False),
            (r"Ні: внутрішні різносторонні кути мають у сумі давати $90^\circ$", False),
        ],
        "solution": r"Сума $180^\circ$ — ознака лише для внутрішніх односторонніх кутів. Для різносторонніх потрібна рівність, а $52^\circ \ne 128^\circ$, тож висновок Петра не обґрунтований.",
    },
    {
        "type": "MULTI", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Прямі $a$ і $b$ перпендикулярні до прямої $c$. Які твердження правильні? Позначте всі.",
        "options": [
            (r"$a \parallel b$", True),
            (r"Усі вісім кутів, які січна $c$ утворює з прямими $a$ і $b$, прямі", True),
            (r"Сума внутрішніх односторонніх кутів дорівнює $180^\circ$", True),
            (r"$a \perp b$", False),
            (r"Прямі $a$ і $b$ перетинаються в точці на прямій $c$", False),
        ],
        "solution": r"Дві прямі, перпендикулярні до третьої, паралельні — $a \parallel b$, тому вони не перетинаються і не перпендикулярні. Усі кути при $a$ і при $b$ — по $90^\circ$, тож односторонні дають $90^\circ + 90^\circ = 180^\circ$.",
    },

    # ==========================================
    # СХОДИНКА 3 — ПІДВИЩЕНИЙ
    # ==========================================
    # --- Моделювання ---
    {
        "type": "FIELDS", "difficulty": 3, "skill": "MODEL",
        "text": r"Внутрішні різносторонні кути при прямих $a$, $b$ і січній $c$ дорівнюють $(3x - 20)^\circ$ і $(x + 40)^\circ$. При якому $x$ можна стверджувати, що $a \parallel b$? Чому тоді дорівнює кожен із кутів?",
        "fields": [(r"$x =$", "30"), (r"Кожен кут (градусів):", "70")],
        "solution": r"Різносторонні кути мають бути рівні: $3x - 20 = x + 40$, $2x = 60$, $x = 30$. Кути: $3 \cdot 30 - 20 = 70^\circ$ і $30 + 40 = 70^\circ$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"Один із внутрішніх односторонніх кутів становить $80\%$ іншого. Яким має бути менший із цих кутів, щоб $a \parallel b$? Відповідь дайте в градусах.",
        "answer": "80",
        "solution": r"Нехай більший кут $x$, менший $0{,}8x$. Для паралельності $x + 0{,}8x = 180^\circ$, $1{,}8x = 180^\circ$, $x = 100^\circ$. Менший кут $0{,}8 \cdot 100^\circ = 80^\circ$.",
    },
    {
        "type": "MATCH", "difficulty": 3, "skill": "MODEL",
        "text": r"Установіть відповідність між умовою (1–3) та значенням $x$ (А–Д), при якому $a \parallel b$.",
        "options": [r"А) $20$", r"Б) $30$", r"В) $35$", r"Г) $60$", r"Д) $70$"],
        "matches": [
            (r"1. Внутрішні різносторонні кути: $2x^\circ$ і $(x + 35)^\circ$", r"В) $35$"),
            (r"2. Відповідні кути: $3x^\circ$ і $(2x + 20)^\circ$", r"А) $20$"),
            (r"3. Внутрішні односторонні кути: $x^\circ$ і $2x^\circ$", r"Г) $60$"),
        ],
        "solution": r"1) Рівні: $2x = x + 35$, $x = 35$. 2) Рівні: $3x = 2x + 20$, $x = 20$. 3) Сума $180^\circ$: $3x = 180$, $x = 60$.",
    },
    {
        "type": "EXPR", "difficulty": 3, "skill": "MODEL",
        "text": r"Один із внутрішніх односторонніх кутів на $d^\circ$ більший за інший. Запишіть вираз для меншого кута (у градусах), при якому $a \parallel b$.",
        "answer": "(180-d)/2", "vars": ["d"],
        "solution": r"Менший кут $x$, більший $x + d$. Для паралельності $x + x + d = 180$, звідки $x = \frac{180 - d}{2}$.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "MODEL",
        "text": r"Кути $1$ і $7$ (див. малюнок) не утворюють жодної пари з ознак паралельності. Яка умова для них гарантує, що $a \parallel b$?",
        "svg_code": '<svg xmlns="http://www.w3.org/2000/svg" width="360" height="260" viewBox="0 0 360 260" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" font-family="sans-serif"><line x1="14.0" y1="75.0" x2="346.0" y2="75.0"/><line x1="14.0" y1="185.0" x2="346.0" y2="185.0"/><line x1="125.9" y1="246.0" x2="234.1" y2="14.0"/><circle cx="205.6" cy="75.0" r="3.5" fill="currentColor" stroke="none"/><circle cx="154.4" cy="185.0" r="3.5" fill="currentColor" stroke="none"/><text x="334.0" y="68.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">a</text><text x="334.0" y="178.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">b</text><text x="240.8" y="36.4" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">c</text><text x="194.9" y="63.1" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">1</text><text x="222.5" y="69.3" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">2</text><text x="188.8" y="90.7" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">3</text><text x="216.4" y="96.9" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">4</text><text x="143.6" y="173.1" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">5</text><text x="171.2" y="179.3" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">6</text><text x="137.5" y="200.7" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">7</text><text x="165.1" y="206.9" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">8</text></svg>',
        "options": [
            (r"$\angle 1 + \angle 7 = 180^\circ$", True),
            (r"$\angle 1 = \angle 7$", False),
            (r"$\angle 1 + \angle 7 = 90^\circ$", False),
            (r"$\angle 1 - \angle 7 = 90^\circ$", False),
        ],
        "solution": r"$\angle 1 = \angle 4$ і $\angle 7 = \angle 6$ (вертикальні). $\angle 4$ і $\angle 6$ — внутрішні односторонні, для них ознака — сума $180^\circ$. Отже, потрібно $\angle 1 + \angle 7 = 180^\circ$.",
    },
    # --- Розв'язування ---
    {
        "type": "FIELDS", "difficulty": 3, "skill": "SOLVE",
        "text": r"Кут $1$ утричі більший за кут $2$ (див. малюнок). Якими мають бути кути $5$ і $6$, щоб $a \parallel b$? Відповіді дайте в градусах.",
        "svg_code": '<svg xmlns="http://www.w3.org/2000/svg" width="360" height="260" viewBox="0 0 360 260" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" font-family="sans-serif"><path d="M235.0 75.0 L249.1 60.9 A20 20 0 0 0 215.0 75.0 Z" fill="currentColor" fill-opacity="0.18" stroke="none"/><path d="M235.0 75.0 L255.0 75.0 A20 20 0 0 0 249.1 60.9 Z" fill="currentColor" fill-opacity="0.18" stroke="none"/><path d="M125.0 185.0 L139.1 170.9 A20 20 0 0 0 105.0 185.0 Z" fill="currentColor" fill-opacity="0.18" stroke="none"/><path d="M125.0 185.0 L145.0 185.0 A20 20 0 0 0 139.1 170.9 Z" fill="currentColor" fill-opacity="0.18" stroke="none"/><line x1="14.0" y1="75.0" x2="346.0" y2="75.0"/><line x1="14.0" y1="185.0" x2="346.0" y2="185.0"/><line x1="64.0" y1="246.0" x2="296.0" y2="14.0"/><circle cx="235.0" cy="75.0" r="3.5" fill="currentColor" stroke="none"/><circle cx="125.0" cy="185.0" r="3.5" fill="currentColor" stroke="none"/><text x="334.0" y="68.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">a</text><text x="334.0" y="178.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">b</text><text x="296.7" y="37.7" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">c</text><text x="222.0" y="48.6" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">1</text><text x="266.4" y="67.0" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">2</text><text x="112.0" y="158.6" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">5</text><text x="156.4" y="177.0" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">6</text></svg>',
        "fields": [(r"$\angle 5 =$", "135"), (r"$\angle 6 =$", "45")],
        "solution": r"$\angle 1$ і $\angle 2$ — суміжні: $3\angle 2 + \angle 2 = 180^\circ$, $\angle 2 = 45^\circ$, $\angle 1 = 135^\circ$. Відповідні кути мають бути рівні: $\angle 5 = \angle 1 = 135^\circ$, $\angle 6 = \angle 2 = 45^\circ$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Внутрішні односторонні кути при прямих $a$, $b$ і січній $c$ дорівнюють $(2x + 16)^\circ$ і $(3x - 1)^\circ$. Яким має бути більший із цих кутів, щоб $a \parallel b$? Відповідь дайте в градусах.",
        "answer": "98",
        "solution": r"$(2x + 16) + (3x - 1) = 180$, $5x + 15 = 180$, $x = 33$. Кути: $2 \cdot 33 + 16 = 82^\circ$ і $3 \cdot 33 - 1 = 98^\circ$. Більший — $98^\circ$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Кути $1$ і $7$ (див. малюнок) відносяться як $5 : 4$. Яким має бути $\angle 1$, щоб $a \parallel b$? Відповідь дайте в градусах.",
        "svg_code": '<svg xmlns="http://www.w3.org/2000/svg" width="360" height="260" viewBox="0 0 360 260" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" font-family="sans-serif"><line x1="14.0" y1="75.0" x2="346.0" y2="75.0"/><line x1="14.0" y1="185.0" x2="346.0" y2="185.0"/><line x1="125.9" y1="246.0" x2="234.1" y2="14.0"/><circle cx="205.6" cy="75.0" r="3.5" fill="currentColor" stroke="none"/><circle cx="154.4" cy="185.0" r="3.5" fill="currentColor" stroke="none"/><text x="334.0" y="68.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">a</text><text x="334.0" y="178.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">b</text><text x="240.8" y="36.4" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">c</text><text x="194.9" y="63.1" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">1</text><text x="222.5" y="69.3" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">2</text><text x="188.8" y="90.7" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">3</text><text x="216.4" y="96.9" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">4</text><text x="143.6" y="173.1" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">5</text><text x="171.2" y="179.3" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">6</text><text x="137.5" y="200.7" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">7</text><text x="165.1" y="206.9" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">8</text></svg>',
        "answer": "100",
        "solution": r"$\angle 1 = \angle 4$, $\angle 7 = \angle 6$ (вертикальні), а $\angle 4$ і $\angle 6$ — внутрішні односторонні. Тому для паралельності $\angle 1 + \angle 7 = 180^\circ$: $5x + 4x = 180^\circ$, $x = 20^\circ$, $\angle 1 = 100^\circ$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"$\angle 1 + \angle 4 = 250^\circ$ (див. малюнок). Яким має бути $\angle 6$, щоб $a \parallel b$? Відповідь дайте в градусах.",
        "svg_code": '<svg xmlns="http://www.w3.org/2000/svg" width="360" height="260" viewBox="0 0 360 260" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" font-family="sans-serif"><path d="M218.5 75.0 L230.0 58.6 A20 20 0 0 0 198.5 75.0 Z" fill="currentColor" fill-opacity="0.18" stroke="none"/><path d="M218.5 75.0 L207.0 91.4 A20 20 0 0 0 238.5 75.0 Z" fill="currentColor" fill-opacity="0.18" stroke="none"/><path d="M141.5 185.0 L161.5 185.0 A20 20 0 0 0 153.0 168.6 Z" fill="currentColor" fill-opacity="0.18" stroke="none"/><line x1="14.0" y1="75.0" x2="346.0" y2="75.0"/><line x1="14.0" y1="185.0" x2="346.0" y2="185.0"/><line x1="98.8" y1="246.0" x2="261.2" y2="14.0"/><circle cx="218.5" cy="75.0" r="3.5" fill="currentColor" stroke="none"/><circle cx="141.5" cy="185.0" r="3.5" fill="currentColor" stroke="none"/><text x="334.0" y="68.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">a</text><text x="334.0" y="178.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">b</text><text x="265.0" y="37.3" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">c</text><text x="202.8" y="49.8" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">1</text><text x="234.2" y="110.2" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">4</text><text x="171.6" y="174.3" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">6</text></svg>',
        "answer": "55",
        "solution": r"$\angle 1$ і $\angle 4$ — вертикальні, тож кожен $250^\circ : 2 = 125^\circ$. $\angle 4$ і $\angle 6$ — внутрішні односторонні: $\angle 6 = 180^\circ - 125^\circ = 55^\circ$.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "SOLVE",
        "text": r"Відомо, що $\angle 2 = 38^\circ$ і $\angle 6 = 38^\circ$ (див. малюнок). Скільки з восьми кутів дорівнюють $38^\circ$?",
        "svg_code": '<svg xmlns="http://www.w3.org/2000/svg" width="360" height="260" viewBox="0 0 360 260" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" font-family="sans-serif"><line x1="14.0" y1="75.0" x2="346.0" y2="75.0"/><line x1="14.0" y1="185.0" x2="346.0" y2="185.0"/><line x1="125.9" y1="246.0" x2="234.1" y2="14.0"/><circle cx="205.6" cy="75.0" r="3.5" fill="currentColor" stroke="none"/><circle cx="154.4" cy="185.0" r="3.5" fill="currentColor" stroke="none"/><text x="334.0" y="68.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">a</text><text x="334.0" y="178.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">b</text><text x="240.8" y="36.4" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">c</text><text x="194.9" y="63.1" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">1</text><text x="222.5" y="69.3" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">2</text><text x="188.8" y="90.7" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">3</text><text x="216.4" y="96.9" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">4</text><text x="143.6" y="173.1" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">5</text><text x="171.2" y="179.3" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">6</text><text x="137.5" y="200.7" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">7</text><text x="165.1" y="206.9" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">8</text></svg>',
        "options": [(r"$4$", True), (r"$2$", False), (r"$3$", False), (r"$6$", False), (r"$8$", False)],
        "solution": r"$\angle 3 = \angle 2 = 38^\circ$ і $\angle 7 = \angle 6 = 38^\circ$ (вертикальні). Решта кутів суміжні з ними: $\angle 1 = \angle 4 = \angle 5 = \angle 8 = 142^\circ$. Отже, $38^\circ$ мають $4$ кути.",
    },
    # --- Аналіз результатів ---
    {
        "type": "ERROR", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Даша доводить, що $a \parallel b$ (див. малюнок; $\angle 1 = \angle 2 = 47^\circ$). У якому кроці помилка?",
        "svg_code": '<svg xmlns="http://www.w3.org/2000/svg" width="360" height="260" viewBox="0 0 360 260" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" font-family="sans-serif"><path d="M110.0 80.0 L132.0 80.0 A22 22 0 0 0 125.0 63.9 Z" fill="currentColor" fill-opacity="0.18" stroke="none"/><path d="M250.0 189.8 L271.8 192.9 A22 22 0 0 0 267.1 176.0 Z" fill="currentColor" fill-opacity="0.18" stroke="none"/><line x1="14.0" y1="80.0" x2="346.0" y2="80.0"/><line x1="14.0" y1="156.7" x2="346.0" y2="203.3"/><line x1="14.0" y1="182.9" x2="171.5" y2="14.0"/><line x1="180.6" y1="246.0" x2="346.0" y2="112.1"/><circle cx="110.0" cy="80.0" r="3.5" fill="currentColor" stroke="none"/><circle cx="250.0" cy="189.8" r="3.5" fill="currentColor" stroke="none"/><text x="334.0" y="73.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">a</text><text x="335.9" y="194.8" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">b</text><text x="172.9" y="37.6" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">c</text><text x="344.9" y="135.8" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">d</text><text x="143.0" y="70.6" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">1</text><text x="284.7" y="185.2" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">2</text></svg>',
        "steps": [
            r"$\angle 1 = \angle 2 = 47^\circ$",
            r"$\angle 1$ і $\angle 2$ — відповідні кути",
            r"Отже, $a \parallel b$ за ознакою",
        ],
        "wrong": 1,
        "solution": r"$\angle 1$ утворений прямою $a$ і січною $c$, а $\angle 2$ — прямою $b$ і іншою січною $d$. Ознаки стосуються кутів при одній січній, тож ці кути не відповідні, і висновок не обґрунтований.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Відомо лише, що $\angle 1 = \angle 5$ (див. малюнок). Скільки з чотирьох пар відповідних кутів ($1$ і $5$, $2$ і $6$, $3$ і $7$, $4$ і $8$) тоді точно рівні?",
        "svg_code": '<svg xmlns="http://www.w3.org/2000/svg" width="360" height="260" viewBox="0 0 360 260" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" font-family="sans-serif"><line x1="14.0" y1="75.0" x2="346.0" y2="75.0"/><line x1="14.0" y1="185.0" x2="346.0" y2="185.0"/><line x1="125.9" y1="246.0" x2="234.1" y2="14.0"/><circle cx="205.6" cy="75.0" r="3.5" fill="currentColor" stroke="none"/><circle cx="154.4" cy="185.0" r="3.5" fill="currentColor" stroke="none"/><text x="334.0" y="68.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">a</text><text x="334.0" y="178.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">b</text><text x="240.8" y="36.4" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">c</text><text x="194.9" y="63.1" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">1</text><text x="222.5" y="69.3" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">2</text><text x="188.8" y="90.7" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">3</text><text x="216.4" y="96.9" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">4</text><text x="143.6" y="173.1" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">5</text><text x="171.2" y="179.3" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">6</text><text x="137.5" y="200.7" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">7</text><text x="165.1" y="206.9" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">8</text></svg>',
        "answer": "4",
        "solution": r"$\angle 4 = \angle 1$ і $\angle 8 = \angle 5$ (вертикальні), тож $\angle 4 = \angle 8$. $\angle 2 = 180^\circ - \angle 1$ і $\angle 6 = 180^\circ - \angle 5$ (суміжні), тож $\angle 2 = \angle 6$; а $\angle 3 = \angle 2$, $\angle 7 = \angle 6$. Рівні всі $4$ пари.",
    },
    {
        "type": "TF", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Перевірте твердження про кути на малюнку: правда чи ні?",
        "svg_code": '<svg xmlns="http://www.w3.org/2000/svg" width="360" height="260" viewBox="0 0 360 260" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" font-family="sans-serif"><line x1="14.0" y1="75.0" x2="346.0" y2="75.0"/><line x1="14.0" y1="185.0" x2="346.0" y2="185.0"/><line x1="125.9" y1="246.0" x2="234.1" y2="14.0"/><circle cx="205.6" cy="75.0" r="3.5" fill="currentColor" stroke="none"/><circle cx="154.4" cy="185.0" r="3.5" fill="currentColor" stroke="none"/><text x="334.0" y="68.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">a</text><text x="334.0" y="178.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">b</text><text x="240.8" y="36.4" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">c</text><text x="194.9" y="63.1" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">1</text><text x="222.5" y="69.3" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">2</text><text x="188.8" y="90.7" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">3</text><text x="216.4" y="96.9" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">4</text><text x="143.6" y="173.1" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">5</text><text x="171.2" y="179.3" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">6</text><text x="137.5" y="200.7" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">7</text><text x="165.1" y="206.9" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">8</text></svg>',
        "statements": [
            (r"Якщо $\angle 3 = \angle 6$, то й $\angle 1 = \angle 8$", True),
            (r"Якщо один із восьми кутів прямий, то всі вісім кутів прямі", False),
            (r"Якщо $\angle 1 = \angle 5$, то $\angle 3 + \angle 5 = 180^\circ$", True),
            (r"Якщо якийсь кут при прямій $a$ дорівнює якомусь куту при прямій $b$, то $a \parallel b$", False),
        ],
        "solution": r"$\angle 1 = 180^\circ - \angle 3$, $\angle 8 = \angle 5 = 180^\circ - \angle 6$ — так. Прямий кут при $a$ робить прямими лише чотири кути при $a$ — ні. $\angle 3 = 180^\circ - \angle 1 = 180^\circ - \angle 5$ — так. Рівність, наприклад, $\angle 3 = \angle 5$ паралельності не гарантує — ні.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Через точку $M$, що не лежить на прямій $a$, провели прямі $m$ і $n$, кожна з яких паралельна прямій $a$. Що можна стверджувати?",
        "options": [
            (r"Прямі $m$ і $n$ збігаються", True),
            (r"$m \parallel n$", False),
            (r"$m \perp n$", False),
            (r"$m$ і $n$ перетинаються в точці $M$ під гострим кутом", False),
            (r"Таких прямих можна провести скільки завгодно", False),
        ],
        "solution": r"За аксіомою паралельності через точку поза прямою проходить лише одна пряма, паралельна даній. Тому $m$ і $n$ — це одна й та сама пряма. Вони мають спільну точку $M$, тож паралельними (як дві різні прямі) не є.",
    },
    {
        "type": "MULTI", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Кути в цих умовах не утворюють пар з ознак напряму. Які з умов усе ж гарантують, що $a \parallel b$ (див. малюнок)? Позначте всі правильні.",
        "svg_code": '<svg xmlns="http://www.w3.org/2000/svg" width="360" height="260" viewBox="0 0 360 260" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" font-family="sans-serif"><line x1="14.0" y1="75.0" x2="346.0" y2="75.0"/><line x1="14.0" y1="185.0" x2="346.0" y2="185.0"/><line x1="125.9" y1="246.0" x2="234.1" y2="14.0"/><circle cx="205.6" cy="75.0" r="3.5" fill="currentColor" stroke="none"/><circle cx="154.4" cy="185.0" r="3.5" fill="currentColor" stroke="none"/><text x="334.0" y="68.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">a</text><text x="334.0" y="178.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">b</text><text x="240.8" y="36.4" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">c</text><text x="194.9" y="63.1" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">1</text><text x="222.5" y="69.3" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">2</text><text x="188.8" y="90.7" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">3</text><text x="216.4" y="96.9" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">4</text><text x="143.6" y="173.1" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">5</text><text x="171.2" y="179.3" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">6</text><text x="137.5" y="200.7" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">7</text><text x="165.1" y="206.9" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">8</text></svg>',
        "options": [
            (r"$\angle 1 = \angle 8$", True),
            (r"$\angle 2 = \angle 7$", True),
            (r"$\angle 2 + \angle 8 = 180^\circ$", True),
            (r"$\angle 2 + \angle 7 = 180^\circ$", False),
            (r"$\angle 1 = \angle 7$", False),
        ],
        "solution": r"Замінимо зовнішні кути вертикальними: $\angle 1 = \angle 4$, $\angle 2 = \angle 3$, $\angle 7 = \angle 6$, $\angle 8 = \angle 5$. Тоді $\angle 1 = \angle 8$ — це $\angle 4 = \angle 5$ (різносторонні рівні) — так; $\angle 2 = \angle 7$ — це $\angle 3 = \angle 6$ — так; $\angle 2 + \angle 8 = 180^\circ$ — це $\angle 3 + \angle 5 = 180^\circ$ — так. $\angle 2 + \angle 7 = 180^\circ$ — сума різносторонніх, $\angle 1 = \angle 7$ — рівність односторонніх: не ознаки.",
    },

    # ==========================================
    # ⚔️ БОСИ
    # ==========================================
    {
        "type": "SHORT", "difficulty": 4, "skill": "MODEL",
        "text": r"Промінь $AK$ — бісектриса кута $1$; він утворює з прямою $a$ кут $62^\circ$ (див. малюнок). Яким має бути $\angle 7$, щоб $a \parallel b$? Відповідь дайте в градусах.",
        "svg_code": '<svg xmlns="http://www.w3.org/2000/svg" width="360" height="260" viewBox="0 0 360 260" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" font-family="sans-serif"><path d="M217.1 75.0 L226.6 60.9 A17 17 0 0 0 200.1 75.0 Z" fill="currentColor" fill-opacity="0.18" stroke="none"/><line x1="14.0" y1="75.0" x2="346.0" y2="75.0"/><line x1="14.0" y1="185.0" x2="346.0" y2="185.0"/><line x1="101.8" y1="246.0" x2="258.2" y2="14.0"/><line x1="217.1" y1="75.0" x2="188.9" y2="22.0"/><circle cx="188.9" cy="22.0" r="3.5" fill="currentColor" stroke="none"/><circle cx="217.1" cy="75.0" r="3.5" fill="currentColor" stroke="none"/><circle cx="142.9" cy="185.0" r="3.5" fill="currentColor" stroke="none"/><text x="334.0" y="68.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">a</text><text x="334.0" y="178.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">b</text><text x="262.3" y="37.2" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">c</text><text x="225.1" y="55.3" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">1</text><text x="178.9" y="21.0" fill="currentColor" stroke="none" font-size="16" font-weight="700" text-anchor="middle">K</text><text x="176.0" y="55.3" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">62°</text><text x="123.5" y="200.3" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">7</text><text x="231.1" y="96.0" fill="currentColor" stroke="none" font-size="16" font-weight="700" text-anchor="middle">A</text><path d="M202.1 46.7 A32 32 0 0 0 185.1 75.0" stroke-width="1.8"/></svg>',
        "answer": "56",
        "solution": r"1) Бісектриса ділить кут навпіл: $\angle 1 = 2 \cdot 62^\circ = 124^\circ$. 2) Кут, суміжний з $\angle 1$ (над $a$ праворуч від $c$), дорівнює $180^\circ - 124^\circ = 56^\circ$; вертикальний до нього кут (під $a$ ліворуч від $c$) — теж $56^\circ$. 3) Цей кут і $\angle 7$ — відповідні. Тому для паралельності $\angle 7 = 56^\circ$.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "MODEL",
        "text": r"Пряма $t$ перетинає прямі $a$, $b$, $c$, $d$ (див. малюнок). Для скількох пар із цих чотирьох прямих можна за ознаками довести, що вони паралельні?",
        "svg_code": '<svg xmlns="http://www.w3.org/2000/svg" width="360" height="320" viewBox="0 0 360 320" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" font-family="sans-serif"><path d="M218.2 55.0 L236.2 55.0 A18 18 0 0 0 224.4 38.1 Z" fill="currentColor" fill-opacity="0.18" stroke="none"/><path d="M192.7 125.0 L174.7 125.0 A18 18 0 0 0 186.6 141.9 Z" fill="currentColor" fill-opacity="0.18" stroke="none"/><path d="M167.3 195.0 L173.4 178.1 A18 18 0 0 0 149.5 191.9 Z" fill="currentColor" fill-opacity="0.18" stroke="none"/><path d="M141.8 265.0 L135.6 281.9 A18 18 0 0 0 159.5 268.1 Z" fill="currentColor" fill-opacity="0.18" stroke="none"/><line x1="126.9" y1="306.0" x2="233.1" y2="14.0"/><line x1="14.0" y1="55.0" x2="346.0" y2="55.0"/><line x1="14.0" y1="125.0" x2="346.0" y2="125.0"/><line x1="14.0" y1="168.0" x2="346.0" y2="226.5"/><line x1="14.0" y1="242.5" x2="346.0" y2="301.0"/><circle cx="218.2" cy="55.0" r="3.5" fill="currentColor" stroke="none"/><circle cx="192.7" cy="125.0" r="3.5" fill="currentColor" stroke="none"/><circle cx="167.3" cy="195.0" r="3.5" fill="currentColor" stroke="none"/><circle cx="141.8" cy="265.0" r="3.5" fill="currentColor" stroke="none"/><text x="216.8" y="26.8" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">t</text><text x="334.0" y="48.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">a</text><text x="244.4" y="41.6" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">70°</text><text x="334.0" y="118.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">b</text><text x="166.5" y="148.4" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">70°</text><text x="336.4" y="217.6" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">c</text><text x="151.3" y="172.3" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">100°</text><text x="336.4" y="292.1" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">d</text><text x="157.8" y="297.7" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">100°</text></svg>',
        "answer": "2",
        "solution": r"Порівнюємо кути над кожною прямою праворуч від $t$. При $a$: $70^\circ$. При $b$: дано $70^\circ$ під $b$ ліворуч, вертикальний до нього кут над $b$ праворуч — $70^\circ$. При $c$: дано $100^\circ$ над $c$ ліворуч, суміжний кут над $c$ праворуч — $80^\circ$. При $d$: дано $100^\circ$ під $d$ праворуч, вертикальний до нього кут над $d$ ліворуч — $100^\circ$, суміжний з ним над $d$ праворуч — $80^\circ$. Відповідні кути рівні лише для $a$ і $b$ ($70^\circ$) та для $c$ і $d$ ($80^\circ$); для решти пар $70^\circ \ne 80^\circ$. Відповідь: $2$ пари.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "SOLVE",
        "text": r"$\angle 1 + \angle 2 + \angle 3 = 250^\circ$ (див. малюнок). Яким має бути $\angle 5$, щоб $a \parallel b$? Відповідь дайте в градусах.",
        "svg_code": '<svg xmlns="http://www.w3.org/2000/svg" width="360" height="260" viewBox="0 0 360 260" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" font-family="sans-serif"><line x1="14.0" y1="75.0" x2="346.0" y2="75.0"/><line x1="14.0" y1="185.0" x2="346.0" y2="185.0"/><line x1="137.8" y1="246.0" x2="222.2" y2="14.0"/><circle cx="200.0" cy="75.0" r="3.5" fill="currentColor" stroke="none"/><circle cx="160.0" cy="185.0" r="3.5" fill="currentColor" stroke="none"/><text x="334.0" y="68.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">a</text><text x="334.0" y="178.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">b</text><text x="230.3" y="35.7" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">c</text><text x="188.5" y="63.6" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">1</text><text x="216.4" y="68.5" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">2</text><text x="183.6" y="91.5" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">3</text><text x="148.5" y="173.6" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">5</text></svg>',
        "answer": "110",
        "solution": r"1) $\angle 1$ і $\angle 2$ — суміжні: $\angle 1 + \angle 2 = 180^\circ$. 2) Тоді $\angle 3 = 250^\circ - 180^\circ = 70^\circ$. 3) $\angle 3$ і $\angle 5$ — внутрішні односторонні, їхня сума має бути $180^\circ$: $\angle 5 = 180^\circ - 70^\circ = 110^\circ$.",
    },
    {
        "type": "FIELDS", "difficulty": 4, "skill": "SOLVE",
        "text": r"Кути $2$ і $5$ (див. малюнок) відносяться як $4 : 5$. Якими мають бути ці кути, щоб $a \parallel b$? Відповіді дайте в градусах.",
        "svg_code": '<svg xmlns="http://www.w3.org/2000/svg" width="360" height="260" viewBox="0 0 360 260" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" font-family="sans-serif"><path d="M189.7 75.0 L209.7 75.0 A20 20 0 0 0 193.2 55.3 Z" fill="currentColor" fill-opacity="0.18" stroke="none"/><path d="M170.3 185.0 L173.8 165.3 A20 20 0 0 0 150.3 185.0 Z" fill="currentColor" fill-opacity="0.18" stroke="none"/><line x1="14.0" y1="75.0" x2="346.0" y2="75.0"/><line x1="14.0" y1="185.0" x2="346.0" y2="185.0"/><line x1="159.5" y1="246.0" x2="200.5" y2="14.0"/><circle cx="189.7" cy="75.0" r="3.5" fill="currentColor" stroke="none"/><circle cx="170.3" cy="185.0" r="3.5" fill="currentColor" stroke="none"/><text x="334.0" y="68.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">a</text><text x="334.0" y="178.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">b</text><text x="211.2" y="34.1" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">c</text><text x="215.7" y="58.1" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">2</text><text x="148.4" y="164.0" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">5</text></svg>',
        "fields": [(r"$\angle 2 =$", "80"), (r"$\angle 5 =$", "100")],
        "solution": r"1) $\angle 2$ і $\angle 5$ — не пара з ознак. Кут, вертикальний до $\angle 2$ (під $a$ ліворуч від $c$), дорівнює $\angle 2$, і він з $\angle 5$ — внутрішні односторонні. 2) Тому для паралельності $\angle 2 + \angle 5 = 180^\circ$. 3) $4x + 5x = 180^\circ$, $x = 20^\circ$: $\angle 2 = 80^\circ$, $\angle 5 = 100^\circ$.",
    },
    {
        "type": "TF", "difficulty": 4, "skill": "ANALYZE",
        "text": r"Які умови гарантують паралельність прямих $a$ і $b$ (див. малюнок)? Правда чи ні?",
        "svg_code": '<svg xmlns="http://www.w3.org/2000/svg" width="360" height="260" viewBox="0 0 360 260" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" font-family="sans-serif"><line x1="14.0" y1="75.0" x2="346.0" y2="75.0"/><line x1="14.0" y1="185.0" x2="346.0" y2="185.0"/><line x1="125.9" y1="246.0" x2="234.1" y2="14.0"/><circle cx="205.6" cy="75.0" r="3.5" fill="currentColor" stroke="none"/><circle cx="154.4" cy="185.0" r="3.5" fill="currentColor" stroke="none"/><text x="334.0" y="68.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">a</text><text x="334.0" y="178.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">b</text><text x="240.8" y="36.4" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">c</text><text x="194.9" y="63.1" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">1</text><text x="222.5" y="69.3" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">2</text><text x="188.8" y="90.7" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">3</text><text x="216.4" y="96.9" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">4</text><text x="143.6" y="173.1" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">5</text><text x="171.2" y="179.3" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">6</text><text x="137.5" y="200.7" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">7</text><text x="165.1" y="206.9" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">8</text></svg>',
        "statements": [
            (r"Якщо $\angle 1 + \angle 6 = 180^\circ$, то $a \parallel b$", True),
            (r"Якщо $\angle 3 = \angle 8$, то $a \parallel b$", False),
            (r"Якщо $\angle 2 + \angle 4 = \angle 5 + \angle 7$, то $a \parallel b$", False),
            (r"Якщо всі чотири кути при прямій $a$ рівні між собою і $\angle 5 = 90^\circ$, то $a \parallel b$", True),
            (r"Якщо $\angle 1 = \angle 6$, то $a \parallel b$", False),
        ],
        "solution": r"1) $\angle 1 = 180^\circ - \angle 2$, тож умова означає $\angle 6 = \angle 2$ — відповідні рівні: так. 2) $\angle 8 = \angle 5$ (вертикальні), тож умова — $\angle 3 = \angle 5$, рівність односторонніх: не ознака. 3) $\angle 2 + \angle 4 = 180^\circ$ і $\angle 5 + \angle 7 = 180^\circ$ (суміжні) завжди — умова нічого не дає. 4) Чотири рівні кути при $a$ — по $90^\circ$, тож $\angle 1 = \angle 5 = 90^\circ$ — відповідні рівні: так. 5) $\angle 1 = \angle 4$, тож умова — $\angle 4 = \angle 6$, рівність односторонніх: не ознака.",
    },

    # ==========================================
    # 👑 УЛЬТРА-БОСИ
    # ==========================================
    {
        "type": "SHORT", "difficulty": 5, "skill": "MODEL",
        "text": r"Січна $c$ перетинає прямі $a$ і $b$ і не перпендикулярна до $a$ (див. малюнок). Розглянемо всі пари «кут при прямій $a$ — кут при прямій $b$» (наприклад, $\angle 1$ і $\angle 7$). Для скількох таких пар рівність цих двох кутів гарантує, що $a \parallel b$?",
        "svg_code": '<svg xmlns="http://www.w3.org/2000/svg" width="360" height="260" viewBox="0 0 360 260" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" font-family="sans-serif"><line x1="14.0" y1="75.0" x2="346.0" y2="75.0"/><line x1="14.0" y1="185.0" x2="346.0" y2="185.0"/><line x1="125.9" y1="246.0" x2="234.1" y2="14.0"/><circle cx="205.6" cy="75.0" r="3.5" fill="currentColor" stroke="none"/><circle cx="154.4" cy="185.0" r="3.5" fill="currentColor" stroke="none"/><text x="334.0" y="68.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">a</text><text x="334.0" y="178.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">b</text><text x="240.8" y="36.4" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">c</text><text x="194.9" y="63.1" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">1</text><text x="222.5" y="69.3" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">2</text><text x="188.8" y="90.7" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">3</text><text x="216.4" y="96.9" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">4</text><text x="143.6" y="173.1" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">5</text><text x="171.2" y="179.3" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">6</text><text x="137.5" y="200.7" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">7</text><text x="165.1" y="206.9" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">8</text></svg>',
        "answer": "8",
        "solution": r"Усього пар $4 \cdot 4 = 16$. При $a$ кути двох видів: $\angle 2 = \angle 3$ (позначимо $\alpha$) і $\angle 1 = \angle 4 = 180^\circ - \alpha$, причому $\alpha \ne 90^\circ$. При $b$ так само: $\angle 6 = \angle 7$ і $\angle 5 = \angle 8$. Рівність кута з $\{2, 3\}$ і кута з $\{6, 7\}$ означає $\angle 3 = \angle 6$ — ознака: $2 \cdot 2 = 4$ пари. Рівність кута з $\{1, 4\}$ і кута з $\{5, 8\}$ означає $\angle 4 = \angle 5$ — ознака: ще $4$ пари. Рівність «навхрест» (наприклад, $\angle 3 = \angle 5$) — це рівність односторонніх кутів; вона дає паралельність лише при $\alpha = 90^\circ$, що виключено. Відповідь: $8$.",
    },
    {
        "type": "SHORT", "difficulty": 5, "skill": "ANALYZE",
        "text": r"Прямі $a$, $b$, $c$ перетнуто січними $m$ і $n$ (див. малюнок). Скільки пар паралельних прямих серед $a$, $b$, $c$ можна обґрунтувати?",
        "svg_code": '<svg xmlns="http://www.w3.org/2000/svg" width="360" height="260" viewBox="0 0 360 260" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" font-family="sans-serif"><path d="M130.1 55.0 L148.1 55.0 A18 18 0 0 0 134.8 37.6 Z" fill="currentColor" fill-opacity="0.18" stroke="none"/><path d="M110.0 130.0 L114.7 112.6 A18 18 0 0 0 92.0 130.0 Z" fill="currentColor" fill-opacity="0.18" stroke="none"/><path d="M260.0 130.0 L278.0 130.0 A18 18 0 0 0 251.0 114.4 Z" fill="currentColor" fill-opacity="0.18" stroke="none"/><path d="M303.3 205.0 L285.3 205.0 A18 18 0 0 0 312.3 220.6 Z" fill="currentColor" fill-opacity="0.18" stroke="none"/><line x1="14.0" y1="55.0" x2="346.0" y2="55.0"/><line x1="14.0" y1="130.0" x2="346.0" y2="130.0"/><line x1="14.0" y1="205.0" x2="346.0" y2="205.0"/><line x1="78.9" y1="246.0" x2="141.1" y2="14.0"/><line x1="327.0" y1="246.0" x2="193.0" y2="14.0"/><circle cx="130.1" cy="55.0" r="3.5" fill="currentColor" stroke="none"/><circle cx="110.0" cy="130.0" r="3.5" fill="currentColor" stroke="none"/><circle cx="260.0" cy="130.0" r="3.5" fill="currentColor" stroke="none"/><circle cx="303.3" cy="205.0" r="3.5" fill="currentColor" stroke="none"/><text x="334.0" y="48.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">a</text><text x="334.0" y="123.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">b</text><text x="334.0" y="198.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">c</text><text x="69.5" y="237.0" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">m</text><text x="332.2" y="235.1" fill="currentColor" stroke="none" font-size="18" font-style="italic" font-weight="700" text-anchor="middle">n</text><text x="155.5" y="40.5" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">75°</text><text x="90.5" y="109.6" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">105°</text><text x="276.0" y="107.3" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">120°</text><text x="287.3" y="237.7" fill="currentColor" stroke="none" font-size="14" font-weight="700" text-anchor="middle">120°</text></svg>',
        "answer": "3",
        "solution": r"1) Січна $m$: при $a$ кут над $a$ праворуч від $m$ — $75^\circ$; при $b$ дано $105^\circ$ (над $b$ ліворуч), суміжний кут над $b$ праворуч — $75^\circ$. Відповідні кути рівні: $a \parallel b$. 2) Січна $n$: при $b$ кут над $b$ праворуч від $n$ — $120^\circ$; при $c$ дано $120^\circ$ під $c$ ліворуч, вертикальний до нього (над $c$ праворуч) — $120^\circ$. Відповідні рівні: $b \parallel c$. 3) Пастка: для $a$ і $c$ кутів не дано. Але якби $a$ і $c$ перетиналися в точці $M$, то через $M$ проходили б дві різні прямі, паралельні $b$, — це суперечить аксіомі паралельності. Отже, $a \parallel c$. Відповідь: $3$ пари.",
    },
]
