TOPIC_NAME = "10. Ірраціональні рівняння"
TASKS = [
    # ==========================================
    # ТЕСТОВІ ЗАВДАННЯ (CHOICE) - 15 шт.
    # ==========================================
    {
        "type": "CHOICE",
        "difficulty": 1,
        "text": r"Знайдіть корінь рівняння $\sqrt{x - 4} = 3$.",
        "svg_code": "",
        "options": [
            (r"А) $7$", False),
            (r"Б) $13$", True),
            (r"В) $1$", False),
            (r"Г) $9$", False),
            (r"Д) $5$", False)
        ],
        "topic_tags": ["10. Ірраціональні рівняння"]
    },
    {
        "type": "CHOICE",
        "difficulty": 1,
        "text": r"Розв'яжіть рівняння $\sqrt{2x + 7} = -4$.",
        "svg_code": "",
        "options": [
            (r"А) $4,5$", False),
            (r"Б) $4$", False),
            (r"В) $-11,5$", False),
            (r"Г) $9$", False),
            (r"Д) Коренів немає", True)
        ],
        "topic_tags": ["10. Ірраціональні рівняння", "9. Корені та їх властивості"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"Яка з наведених систем є рівносильною рівнянню $\sqrt{x^2 - 3x} = x - 1$?",
        "svg_code": "",
        "options": [
            (r"А) $x^2 - 3x = (x - 1)^2$", False),
            (r"Б) $\begin{cases} x^2 - 3x = (x - 1)^2 \\ x^2 - 3x \geq 0 \end{cases}$", False),
            (r"В) $\begin{cases} x^2 - 3x = (x - 1)^2 \\ x - 1 \geq 0 \end{cases}$", True),
            (r"Г) $\begin{cases} x^2 - 3x = x - 1 \\ x - 1 \geq 0 \end{cases}$", False),
            (r"Д) $\begin{cases} x^2 - 3x = (x - 1)^2 \\ x \geq 0 \end{cases}$", False)
        ],
        "topic_tags": ["10. Ірраціональні рівняння"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"Знайдіть корінь рівняння $\sqrt{x + 2} = x$. Обов'язково виконайте перевірку!",
        "svg_code": "",
        "options": [
            (r"А) $2$", True),
            (r"Б) $-1$", False),
            (r"В) $2; -1$", False),
            (r"Г) $0$", False),
            (r"Д) Коренів немає", False)
        ],
        "topic_tags": ["10. Ірраціональні рівняння", "7. Квадратні рівняння"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"Розв'яжіть рівняння $\sqrt{x^2 - x - 2} = \sqrt{x - 5}$.",
        "svg_code": "",
        "options": [
            (r"А) $1; -3$", False),
            (r"Б) $1$", False),
            (r"В) $-3$", False),
            (r"Г) $3$", False),
            (r"Д) Коренів немає", True)
        ],
        "topic_tags": ["10. Ірраціональні рівняння"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"Знайдіть суму коренів рівняння $\sqrt{(x - 4)^2} = 5$. Зверніть увагу на прихований модуль!",
        "svg_code": "",
        "options": [
            (r"А) $9$", False),
            (r"Б) $-1$", False),
            (r"В) $8$", True),
            (r"Г) $10$", False),
            (r"Д) $4$", False)
        ],
        "topic_tags": ["10. Ірраціональні рівняння", "9. Корені та їх властивості",
                       "6. Лінійні рівняння. Лінійні рівняння з модулем"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"Скільки дійсних коренів має рівняння $(x + 4)\sqrt{x - 2} = 0$?",
        "svg_code": "",
        "options": [
            (r"А) Один", True),
            (r"Б) Два", False),
            (r"В) Три", False),
            (r"Г) Жодного", False),
            (r"Д) Безліч", False)
        ],
        "topic_tags": ["10. Ірраціональні рівняння"]
    },
    {
        "type": "CHOICE",
        "difficulty": 1,
        "text": r"Розв'яжіть рівняння $\sqrt[3]{x^2 - 1} = 2$.",
        "svg_code": "",
        "options": [
            (r"А) $3$", False),
            (r"Б) $-3$", False),
            (r"В) $-3; 3$", True),
            (r"Г) $9$", False),
            (r"Д) $\sqrt{5}; -\sqrt{5}$", False)
        ],
        "topic_tags": ["10. Ірраціональні рівняння", "9. Корені та їх властивості"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"Знайдіть суму коренів рівняння $x - 6\sqrt{x} + 5 = 0$. (Використайте заміну $t = \sqrt{x}$).",
        "svg_code": "",
        "options": [
            (r"А) $6$", False),
            (r"Б) $26$", True),
            (r"В) $-6$", False),
            (r"Г) $5$", False),
            (r"Д) $15$", False)
        ],
        "topic_tags": ["10. Ірраціональні рівняння", "7. Квадратні рівняння"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"Укажіть область допустимих значень (ОДЗ) виразу $\sqrt{4 - x} + \frac{1}{\sqrt{x + 1}}$.",
        "svg_code": "",
        "options": [
            (r"А) $[-1; 4]$", False),
            (r"Б) $(-1; 4]$", True),
            (r"В) $[-1; 4)$", False),
            (r"Г) $(-\infty; 4]$", False),
            (r"Д) $(-1; +\infty)$", False)
        ],
        "topic_tags": ["10. Ірраціональні рівняння"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"Знайдіть корінь рівняння $\frac{\sqrt{x} - 3}{x - 9} = 0$.",
        "svg_code": "",
        "options": [
            (r"А) $3$", False),
            (r"Б) $9$", False),
            (r"В) $-3$", False),
            (r"Г) $81$", False),
            (r"Д) Коренів немає", True)
        ],
        "topic_tags": ["10. Ірраціональні рівняння", "8. Дробово-раціональні рівняння"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"Розв'яжіть рівняння $\sqrt{x^2 - 2x - 3} = -x$.",
        "svg_code": "",
        "options": [
            (r"А) $-1,5$", True),
            (r"Б) $1,5$", False),
            (r"В) $-3$", False),
            (r"Г) $3$", False),
            (r"Д) Коренів немає", False)
        ],
        "topic_tags": ["10. Ірраціональні рівняння"]
    },
    {
        "type": "CHOICE",
        "difficulty": 1,
        "text": r"Розв'яжіть рівняння $\sqrt{x}\sqrt{x - 3} = 0$.",
        "svg_code": "",
        "options": [
            (r"А) $0$", False),
            (r"Б) $3$", False),
            (r"В) $0; 3$", True),
            (r"Г) $-3; 0$", False),
            (r"Д) Коренів немає", False)
        ],
        "topic_tags": ["10. Ірраціональні рівняння"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"При яких значеннях параметра $a$ рівняння $\sqrt{x - 2} = a - 3$ має хоча б один дійсний корінь?",
        "svg_code": "",
        "options": [
            (r"А) $a \geq 2$", False),
            (r"Б) $a \geq 3$", True),
            (r"В) $a < 3$", False),
            (r"Г) $a \in \mathbb{R}$", False),
            (r"Д) $a \geq 0$", False)
        ],
        "topic_tags": ["10. Ірраціональні рівняння"]
    },
    {
        "type": "CHOICE",
        "difficulty": 3,
        "text": r"Знайдіть найбільший корінь рівняння $\sqrt{x^2 + 5x + 1} = \sqrt{x^2 - 3x + 9}$.",
        "svg_code": "",
        "options": [
            (r"А) $0$", False),
            (r"Б) $1$", True),
            (r"В) $2$", False),
            (r"Г) $3$", False),
            (r"Д) $-1$", False)
        ],
        "topic_tags": ["10. Ірраціональні рівняння"]
    },

    # ==========================================
    # ЗАВДАННЯ НА ВІДПОВІДНІСТЬ (MATCH) - 5 шт.
    # ==========================================
    {
        "type": "MATCH",
        "difficulty": 1,
        "text": r"Узгодьте рівняння (1–3) із множиною його дійсних коренів (А–Д).",
        "svg_code": "",
        "options": [
            r"А) $\{16\}$",
            r"Б) $\{-64\}$",
            r"В) $\{-16\}$",
            r"Г) $\{-16; 16\}$",
            r"Д) $\varnothing$ (коренів немає)"
        ],
        "matches": [
            (r"1. $\sqrt{x} = 4$", r"А) $\{16\}$"),
            (r"2. $\sqrt{x} = -4$", r"Д) $\varnothing$ (коренів немає)"),
            (r"3. $\sqrt[3]{x} = -4$", r"Б) $\{-64\}$")
        ],
        "topic_tags": ["10. Ірраціональні рівняння"]
    },
    {
        "type": "MATCH",
        "difficulty": 2,
        "text": r"Узгодьте рівняння (1–3) із відповідною обов'язковою умовою (ОДЗ або обмеженням), необхідною для його розв'язання (А–Д).",
        "svg_code": "",
        "options": [
            r"А) $g(x) \geq 0$",
            r"Б) $f(x) \geq 0$ або $g(x) \geq 0$",
            r"В) $x \in \mathbb{R}$ (умов немає)",
            r"Г) $g(x) \neq 0$",
            r"Д) $f(x) > 0$"
        ],
        "matches": [
            (r"1. $\sqrt{f(x)} = g(x)$", r"А) $g(x) \geq 0$"),
            (r"2. $\sqrt{f(x)} = \sqrt{g(x)}$", r"Б) $f(x) \geq 0$ або $g(x) \geq 0$"),
            (r"3. $\sqrt[3]{f(x)} = g(x)$", r"В) $x \in \mathbb{R}$ (умов немає)")
        ],
        "topic_tags": ["10. Ірраціональні рівняння"]
    },
    {
        "type": "MATCH",
        "difficulty": 2,
        "text": r"Узгодьте рівняння (1–3) із кількістю його дійсних коренів (А–Д).",
        "svg_code": "",
        "options": [
            r"А) $0$",
            r"Б) $1$",
            r"В) $2$",
            r"Г) $3$",
            r"Д) Безліч"
        ],
        "matches": [
            (r"1. $(x - 2)\sqrt{x + 1} = 0$", r"В) $2$"),
            (r"2. $(x + 2)\sqrt{x - 1} = 0$", r"Б) $1$"),
            (r"3. $\sqrt{x^2 + 1} = -2$", r"А) $0$")
        ],
        "topic_tags": ["10. Ірраціональні рівняння"]
    },
    {
        "type": "MATCH",
        "difficulty": 2,
        "text": r"Узгодьте рівняння з прихованим модулем (1–3) із його розв'язками (А–Д).",
        "svg_code": "",
        "options": [
            r"А) $2$",
            r"Б) $\{-1; 5\}$",
            r"В) $\varnothing$ (коренів немає)",
            r"Г) $\{5\}$",
            r"Д) $\{-5; 1\}$"
        ],
        "matches": [
            (r"1. $\sqrt{(x - 2)^2} = 3$", r"Б) $\{-1; 5\}$"),
            (r"2. $\sqrt{x^2 - 4x + 4} = 0$", r"А) $2$"),
            (r"3. $\sqrt{(x - 2)^2} = -3$", r"В) $\varnothing$ (коренів немає)")
        ],
        "topic_tags": ["10. Ірраціональні рівняння", "6. Лінійні рівняння. Лінійні рівняння з модулем",
                       "9. Корені та їх властивості"]
    },
    {
        "type": "MATCH",
        "difficulty": 2,
        "text": r"Узгодьте ірраціональне рівняння (1–3) із заміною змінної, яку найдоцільніше використати для його розв'язання (А–Д).",
        "svg_code": "",
        "options": [
            r"А) $t = x^2$",
            r"Б) $t = \sqrt{x}$",
            r"В) $t = \sqrt{x^2 - 5x}$",
            r"Г) $t = \sqrt[3]{x}$",
            r"Д) $t = \sqrt{x - 5}$"
        ],
        "matches": [
            (r"1. $x - 5\sqrt{x} + 4 = 0$", r"Б) $t = \sqrt{x}$"),
            (r"2. $x^2 - 5x + \sqrt{x^2 - 5x} = 2$", r"В) $t = \sqrt{x^2 - 5x}$"),
            (r"3. $\sqrt[3]{x^2} - 5\sqrt[3]{x} = 0$", r"Г) $t = \sqrt[3]{x}$")
        ],
        "topic_tags": ["10. Ірраціональні рівняння"]
    },

    # ==========================================
    # КОРОТКА ВІДПОВІДЬ (SHORT) - 5 шт.
    # ВСІ МАЮТЬ РІВЕНЬ СКЛАДНОСТІ 3
    # ==========================================
    {
        "type": "SHORT",
        "difficulty": 3,
        "text": r"Знайдіть суму коренів рівняння $(x^2 - 6x - 7)\sqrt{x - 2} = 0$. Уважно перевірте ОДЗ!",
        "svg_code": "",
        "answer": "9",
        "topic_tags": ["10. Ірраціональні рівняння", "7. Квадратні рівняння"]
    },
    {
        "type": "SHORT",
        "difficulty": 3,
        "text": r"Знайдіть корінь рівняння $\sqrt{3x^2 - 8x + 5} = 1 - x$. Якщо рівняння має кілька коренів, запишіть у відповідь їхню суму.",
        "svg_code": "",
        "answer": "1",
        "topic_tags": ["10. Ірраціональні рівняння", "7. Квадратні рівняння"]
    },
    {
        "type": "SHORT",
        "difficulty": 3,
        "text": r"Використовуючи метод заміни змінної, розв'яжіть рівняння $x^2 - 2x - \sqrt{x^2 - 2x + 4} = 2$. У відповідь запишіть добуток його дійсних коренів.",
        "svg_code": "",
        "answer": "-5",
        "topic_tags": ["10. Ірраціональні рівняння", "7. Квадратні рівняння"]
    },
    {
        "type": "SHORT",
        "difficulty": 3,
        "text": r"Знайдіть суму коренів рівняння $\sqrt{x^2 - 12x + 36} + \sqrt{x^2} = 10$. <br><br><i>Підказка: Згорніть вираз під першим коренем у повний квадрат і пригадайте геометричний зміст модуля (сума відстаней від точки $x$ до точок $6$ та $0$).</i>",
        "svg_code": r"""<svg viewBox="0 0 400 120" width="100%" height="120" xmlns="http://www.w3.org/2000/svg">
            <line x1="20" y1="80" x2="380" y2="80" stroke="#333" stroke-width="2" marker-end="url(#arrDark)"/>
            <text x="385" y="85" font-size="14" font-family="sans-serif">x</text>

            <circle cx="120" cy="80" r="5" fill="#2c3e50"/>
            <text x="120" y="110" font-size="16" font-weight="bold" fill="#2c3e50" text-anchor="middle">0</text>

            <circle cx="280" cy="80" r="5" fill="#2c3e50"/>
            <text x="280" y="110" font-size="16" font-weight="bold" fill="#2c3e50" text-anchor="middle">6</text>

            <circle cx="200" cy="80" r="5" fill="#e74c3c"/>
            <text x="200" y="110" font-size="16" font-weight="bold" fill="#e74c3c" text-anchor="middle">x</text>

            <path d="M 120 70 Q 160 20 200 70" fill="none" stroke="#3498db" stroke-width="2" stroke-dasharray="5,5"/>
            <path d="M 200 70 Q 240 20 280 70" fill="none" stroke="#27ae60" stroke-width="2" stroke-dasharray="5,5"/>

            <text x="160" y="40" font-size="14" font-weight="bold" fill="#3498db" text-anchor="middle">|x|</text>
            <text x="240" y="40" font-size="14" font-weight="bold" fill="#27ae60" text-anchor="middle">|x - 6|</text>
        </svg>""",
        "answer": "6",
        "topic_tags": ["10. Ірраціональні рівняння", "9. Корені та їх властивості",
                       "6. Лінійні рівняння. Лінійні рівняння з модулем"]
    },
    {
        "type": "SHORT",
        "difficulty": 3,
        "text": r"Розв'яжіть дробово-ірраціональне рівняння $\frac{x^2 - 16}{\sqrt{3 - x}} = 0$. У відповідь запишіть знайдений корінь.",
        "svg_code": "",
        "answer": "-4",
        "topic_tags": ["10. Ірраціональні рівняння", "8. Дробово-раціональні рівняння"]
    }
]