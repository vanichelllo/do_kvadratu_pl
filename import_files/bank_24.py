TOPIC_NAME = "24. Побудова графіків функцій шляхом геометричних перетворень"
TASKS = [
    # ==========================================
    # ТЕСТОВІ ЗАВДАННЯ (CHOICE) З ГРАФІКАМИ - 5 шт.
    # ==========================================
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"На рисунку зображено графік функції $y = f(x)$. Яка з наведених формул задає цю функцію?",
        "svg_code": r"""
<svg viewBox="-5 -5 10 10" width="100%" height="250px" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <marker id="arrDark1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4" markerHeight="4" orient="auto-start-reverse"><path d="M 0 1 L 10 5 L 0 9 z" fill="#7f8c8d" /></marker>
    </defs>
    <line x1="-5" y1="0" x2="5" y2="0" stroke="#7f8c8d" stroke-width="0.05" marker-end="url(#arrDark1)"/>
    <line x1="0" y1="5" x2="0" y2="-5" stroke="#7f8c8d" stroke-width="0.05" marker-end="url(#arrDark1)"/>
    <text x="4.5" y="-0.3" font-size="0.4" font-family="sans-serif" fill="#7f8c8d">x</text>
    <text x="0.2" y="-4.5" font-size="0.4" font-family="sans-serif" fill="#7f8c8d">y</text>
    <text x="-0.2" y="0.4" font-size="0.3" font-family="sans-serif">0</text>
    <line x1="1" y1="-0.1" x2="1" y2="0.1" stroke="#333" stroke-width="0.03"/>
    <text x="1" y="0.5" font-size="0.3" font-family="sans-serif" text-anchor="middle">1</text>
    <line x1="-0.1" y1="-1" x2="0.1" y2="-1" stroke="#333" stroke-width="0.03"/>
    <text x="-0.3" y="-0.9" font-size="0.3" font-family="sans-serif" text-anchor="end">1</text>

    <path d="M 0 -3 Q 2 5 4 -3" fill="none" stroke="#3498db" stroke-width="0.08"/>
    <circle cx="2" cy="1" r="0.08" fill="#e74c3c"/>
    <line x1="2" y1="0" x2="2" y2="1" stroke="#e74c3c" stroke-width="0.03" stroke-dasharray="0.1,0.1"/>
    <line x1="0" y1="1" x2="2" y2="1" stroke="#e74c3c" stroke-width="0.03" stroke-dasharray="0.1,0.1"/>
    <text x="2" y="-0.2" font-size="0.3" font-family="sans-serif" text-anchor="middle">2</text>
    <text x="-0.2" y="1.1" font-size="0.3" font-family="sans-serif" text-anchor="end">-1</text>
</svg>
        """,
        "options": [
            (r"А) $y = (x+2)^2 - 1$", False),
            (r"Б) $y = (x-2)^2 + 1$", False),
            (r"В) $y = x^2 - 2$", False),
            (r"Г) $y = (x-2)^2 - 1$", True),
            (r"Д) $y = (x+2)^2 + 1$", False)
        ],
        "topic_tags": ["24. Побудова графіків функцій шляхом геометричних перетворень", "12. Квадратична функція"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"Яка з наведених функцій відповідає графіку, зображеному на рисунку?",
        "svg_code": r"""
<svg viewBox="-5 -5 10 10" width="100%" height="250px" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <marker id="arrDark2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4" markerHeight="4" orient="auto-start-reverse"><path d="M 0 1 L 10 5 L 0 9 z" fill="#7f8c8d" /></marker>
    </defs>
    <line x1="-5" y1="0" x2="5" y2="0" stroke="#7f8c8d" stroke-width="0.05" marker-end="url(#arrDark2)"/>
    <line x1="0" y1="5" x2="0" y2="-5" stroke="#7f8c8d" stroke-width="0.05" marker-end="url(#arrDark2)"/>
    <text x="4.5" y="-0.3" font-size="0.4" font-family="sans-serif" fill="#7f8c8d">x</text>
    <text x="0.2" y="-4.5" font-size="0.4" font-family="sans-serif" fill="#7f8c8d">y</text>
    <text x="-0.2" y="0.4" font-size="0.3" font-family="sans-serif">0</text>
    <line x1="1" y1="-0.1" x2="1" y2="0.1" stroke="#333" stroke-width="0.03"/>
    <text x="1" y="0.5" font-size="0.3" font-family="sans-serif" text-anchor="middle">1</text>
    <line x1="-0.1" y1="-1" x2="0.1" y2="-1" stroke="#333" stroke-width="0.03"/>
    <text x="-0.3" y="-0.9" font-size="0.3" font-family="sans-serif" text-anchor="end">1</text>

    <path d="M -3 0 L -2.8 -0.447 L -2 -1 L -1 -1.414 L 0 -1.732 L 1 -2 L 2 -2.236 L 3 -2.449 L 4 -2.645 L 5 -2.828" fill="none" stroke="#27ae60" stroke-width="0.08"/>
    <circle cx="-3" cy="0" r="0.08" fill="#27ae60"/>
    <line x1="-3" y1="-0.1" x2="-3" y2="0.1" stroke="#333" stroke-width="0.03"/>
    <text x="-3" y="0.5" font-size="0.3" font-family="sans-serif" text-anchor="middle">-3</text>
</svg>
        """,
        "options": [
            (r"А) $y = \sqrt{x} + 3$", False),
            (r"Б) $y = \sqrt{x} - 3$", False),
            (r"В) $y = \sqrt{x - 3}$", False),
            (r"Г) $y = \sqrt{x + 3}$", True),
            (r"Д) $y = -\sqrt{x + 3}$", False)
        ],
        "topic_tags": ["24. Побудова графіків функцій шляхом геометричних перетворень", "11. Функції та їх властивості"]
    },
    {
        "type": "CHOICE",
        "difficulty": 3,
        "text": r"На рисунку зображено графік функції, утворений геометричними перетвореннями параболи. Вкажіть формулу, якою він задається.",
        "svg_code": r"""
<svg viewBox="-5 -5 10 10" width="100%" height="250px" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <marker id="arrDark3" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4" markerHeight="4" orient="auto-start-reverse"><path d="M 0 1 L 10 5 L 0 9 z" fill="#7f8c8d" /></marker>
    </defs>
    <line x1="-5" y1="0" x2="5" y2="0" stroke="#7f8c8d" stroke-width="0.05" marker-end="url(#arrDark3)"/>
    <line x1="0" y1="5" x2="0" y2="-5" stroke="#7f8c8d" stroke-width="0.05" marker-end="url(#arrDark3)"/>
    <text x="4.5" y="-0.3" font-size="0.4" font-family="sans-serif" fill="#7f8c8d">x</text>
    <text x="0.2" y="-4.5" font-size="0.4" font-family="sans-serif" fill="#7f8c8d">y</text>
    <text x="-0.2" y="0.4" font-size="0.3" font-family="sans-serif">0</text>
    <line x1="1" y1="-0.1" x2="1" y2="0.1" stroke="#333" stroke-width="0.03"/>
    <text x="1" y="0.5" font-size="0.3" font-family="sans-serif" text-anchor="middle">1</text>
    <line x1="-0.1" y1="-1" x2="0.1" y2="-1" stroke="#333" stroke-width="0.03"/>
    <text x="-0.3" y="-0.9" font-size="0.3" font-family="sans-serif" text-anchor="end">1</text>

    <path d="M -3 -5 Q -2.5 -1.25 -2 0 Q 0 -8 2 0 Q 2.5 -1.25 3 -5" fill="none" stroke="#8e44ad" stroke-width="0.08"/>
    <line x1="-2" y1="-0.1" x2="-2" y2="0.1" stroke="#333" stroke-width="0.03"/>
    <text x="-2" y="0.5" font-size="0.3" font-family="sans-serif" text-anchor="middle">-2</text>
    <line x1="2" y1="-0.1" x2="2" y2="0.1" stroke="#333" stroke-width="0.03"/>
    <text x="2" y="0.5" font-size="0.3" font-family="sans-serif" text-anchor="middle">2</text>
    <line x1="-0.1" y1="-4" x2="0.1" y2="-4" stroke="#333" stroke-width="0.03"/>
    <text x="-0.3" y="-3.9" font-size="0.3" font-family="sans-serif" text-anchor="end">4</text>
</svg>
        """,
        "options": [
            (r"А) $y = x^2 - 4$", False),
            (r"Б) $y = x^2 + 4$", False),
            (r"В) $y = |x^2 - 4|$", True),
            (r"Г) $y = |x^2| - 4$", False),
            (r"Д) $y = -|x^2 - 4|$", False)
        ],
        "topic_tags": ["24. Побудова графіків функцій шляхом геометричних перетворень",
                       "6. Лінійні рівняння. Лінійні рівняння з модулем"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"Червоною лінією зображено графік функції $y = f(x)$, а синьою — графік функції $y = g(x)$. Виразіть $g(x)$ через $f(x)$.",
        "svg_code": r"""
<svg viewBox="-5 -5 10 10" width="100%" height="250px" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <marker id="arrDark4" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4" markerHeight="4" orient="auto-start-reverse"><path d="M 0 1 L 10 5 L 0 9 z" fill="#7f8c8d" /></marker>
    </defs>
    <line x1="-5" y1="0" x2="5" y2="0" stroke="#7f8c8d" stroke-width="0.05" marker-end="url(#arrDark4)"/>
    <line x1="0" y1="5" x2="0" y2="-5" stroke="#7f8c8d" stroke-width="0.05" marker-end="url(#arrDark4)"/>

    <path d="M -2.5 -4.25 Q 0 6 2.5 -4.25" fill="none" stroke="#e74c3c" stroke-width="0.08"/>
    <text x="2" y="-3.5" font-size="0.4" font-family="sans-serif" fill="#e74c3c">f(x)</text>

    <path d="M -2.5 4.25 Q 0 -6 2.5 4.25" fill="none" stroke="#3498db" stroke-width="0.08"/>
    <text x="2" y="3.8" font-size="0.4" font-family="sans-serif" fill="#3498db">g(x)</text>
</svg>
        """,
        "options": [
            (r"А) $g(x) = f(-x)$", False),
            (r"Б) $g(x) = -f(x)$", True),
            (r"В) $g(x) = |f(x)|$", False),
            (r"Г) $g(x) = f(x) - 2$", False),
            (r"Д) $g(x) = 2f(x)$", False)
        ],
        "topic_tags": ["24. Побудова графіків функцій шляхом геометричних перетворень"]
    },
    {
        "type": "CHOICE",
        "difficulty": 1,
        "text": r"Яка з наведених формул відповідає зображеному графіку?",
        "svg_code": r"""
<svg viewBox="-6 -5 10 10" width="100%" height="250px" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <marker id="arrDark5" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4" markerHeight="4" orient="auto-start-reverse"><path d="M 0 1 L 10 5 L 0 9 z" fill="#7f8c8d" /></marker>
    </defs>
    <line x1="-6" y1="0" x2="4" y2="0" stroke="#7f8c8d" stroke-width="0.05" marker-end="url(#arrDark5)"/>
    <line x1="0" y1="5" x2="0" y2="-5" stroke="#7f8c8d" stroke-width="0.05" marker-end="url(#arrDark5)"/>

    <polyline points="-6,-3 -3,0 0,-3 2,-5" fill="none" stroke="#e67e22" stroke-width="0.08"/>
    <line x1="-3" y1="-0.1" x2="-3" y2="0.1" stroke="#333" stroke-width="0.03"/>
    <text x="-3" y="0.5" font-size="0.3" font-family="sans-serif" text-anchor="middle">-3</text>
    <line x1="-0.1" y1="-3" x2="0.1" y2="-3" stroke="#333" stroke-width="0.03"/>
    <text x="-0.3" y="-2.9" font-size="0.3" font-family="sans-serif" text-anchor="end">3</text>
</svg>
        """,
        "options": [
            (r"А) $y = |x| + 3$", False),
            (r"Б) $y = |x - 3|$", False),
            (r"В) $y = |x| - 3$", False),
            (r"Г) $y = -|x + 3|$", False),
            (r"Д) $y = |x + 3|$", True)
        ],
        "topic_tags": ["24. Побудова графіків функцій шляхом геометричних перетворень",
                       "6. Лінійні рівняння. Лінійні рівняння з модулем"]
    },

    # ==========================================
    # ЗАВДАННЯ НА ВІДПОВІДНІСТЬ (MATCH) - 2 шт.
    # ==========================================
    {
        "type": "MATCH",
        "difficulty": 1,
        "text": r"Узгодьте функцію (1–3) із геометричним перетворенням (А–Д), яке потрібно застосувати до графіка базової функції $y = x^2$ для її побудови.",
        "svg_code": "",
        "options": [
            r"А) Зсув вправо на 3 одиниці",
            r"Б) Зсув вліво на 3 одиниці",
            r"В) Зсув вгору на 3 одиниці",
            r"Г) Зсув вниз на 3 одиниці",
            r"Д) Відображення відносно осі Ox"
        ],
        "matches": [
            (r"1. $y = (x-3)^2$", r"А) Зсув вправо на 3 одиниці"),
            (r"2. $y = x^2 - 3$", r"Г) Зсув вниз на 3 одиниці"),
            (r"3. $y = (x+3)^2$", r"Б) Зсув вліво на 3 одиниці")
        ],
        "topic_tags": ["24. Побудова графіків функцій шляхом геометричних перетворень"]
    },
    {
        "type": "MATCH",
        "difficulty": 2,
        "text": r"Узгодьте формулу перетворення (1–3) із відповідним наслідком для графіка $y = f(x)$ (А–Д).",
        "svg_code": "",
        "options": [
            r"А) Симетрія відносно осі Ox (низ і верх міняються місцями)",
            r"Б) Симетрія відносно осі Oy (ліво і право міняються місцями)",
            r"В) Частини графіка під віссю Ox відображаються вгору",
            r"Г) Графік розтягується вдвічі вздовж осі Oy",
            r"Д) Графік стискається вдвічі вздовж осі Ox"
        ],
        "matches": [
            (r"1. $y = -f(x)$", r"А) Симетрія відносно осі Ox (низ і верх міняються місцями)"),
            (r"2. $y = f(-x)$", r"Б) Симетрія відносно осі Oy (ліво і право міняються місцями)"),
            (r"3. $y = |f(x)|$", r"В) Частини графіка під віссю Ox відображаються вгору")
        ],
        "topic_tags": ["24. Побудова графіків функцій шляхом геометричних перетворень"]
    },

    # ==========================================
    # КОРОТКА ВІДПОВІДЬ (SHORT) - 1 шт (Але з графіком)
    # ==========================================
    {
        "type": "SHORT",
        "difficulty": 3,
        "text": r"На рисунку зображено графік функції $y = f(x)$. Користуючись графіком, знайдіть значення виразу $f(-3) + f(0) + f(2)$.",
        "svg_code": r"""
<svg viewBox="-5 -5 10 10" width="100%" height="250px" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <marker id="arrDark6" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4" markerHeight="4" orient="auto-start-reverse"><path d="M 0 1 L 10 5 L 0 9 z" fill="#7f8c8d" /></marker>
    </defs>
    <line x1="-5" y1="0" x2="5" y2="0" stroke="#7f8c8d" stroke-width="0.05" marker-end="url(#arrDark6)"/>
    <line x1="0" y1="5" x2="0" y2="-5" stroke="#7f8c8d" stroke-width="0.05" marker-end="url(#arrDark6)"/>

    <polyline points="-4,2 -2,-2 1,-2 4,1 5,1" fill="none" stroke="#344e86" stroke-width="0.08"/>
    <circle cx="-4" cy="2" r="0.08" fill="#344e86"/>
    <circle cx="-2" cy="-2" r="0.08" fill="#344e86"/>
    <circle cx="1" cy="-2" r="0.08" fill="#344e86"/>
    <circle cx="4" cy="1" r="0.08" fill="#344e86"/>
    <circle cx="5" cy="1" r="0.08" fill="#344e86"/>

    <text x="-4" y="0.5" font-size="0.3" font-family="sans-serif" text-anchor="middle">-4</text>
    <text x="-3" y="0.5" font-size="0.3" font-family="sans-serif" text-anchor="middle">-3</text>
    <text x="-2" y="0.5" font-size="0.3" font-family="sans-serif" text-anchor="middle">-2</text>
    <text x="2" y="0.5" font-size="0.3" font-family="sans-serif" text-anchor="middle">2</text>
    <text x="4" y="0.5" font-size="0.3" font-family="sans-serif" text-anchor="middle">4</text>
    <text x="-0.2" y="-1.9" font-size="0.3" font-family="sans-serif" text-anchor="end">2</text>
    <text x="-0.2" y="2.1" font-size="0.3" font-family="sans-serif" text-anchor="end">-2</text>
    <text x="-0.2" y="1.1" font-size="0.3" font-family="sans-serif" text-anchor="end">-1</text>

    <line x1="-3" y1="-0.1" x2="-3" y2="0.1" stroke="#333" stroke-width="0.03"/>
    <line x1="-2" y1="-0.1" x2="-2" y2="0.1" stroke="#333" stroke-width="0.03"/>
    <line x1="2" y1="-0.1" x2="2" y2="0.1" stroke="#333" stroke-width="0.03"/>
    <line x1="4" y1="-0.1" x2="4" y2="0.1" stroke="#333" stroke-width="0.03"/>

    <line x1="-3" y1="0" x2="-3" y2="0" stroke="#7f8c8d" stroke-dasharray="0.1,0.1" stroke-width="0.02"/>
    <line x1="2" y1="0" x2="2" y2="-0.95" stroke="#7f8c8d" stroke-dasharray="0.1,0.1" stroke-width="0.03"/>
    <line x1="0" y1="-1" x2="2" y2="-1" stroke="#7f8c8d" stroke-dasharray="0.1,0.1" stroke-width="0.03"/>
</svg>
        """,
        "answer": "3",
        "topic_tags": ["24. Побудова графіків функцій шляхом геометричних перетворень", "11. Функції та їх властивості"]
    }
]