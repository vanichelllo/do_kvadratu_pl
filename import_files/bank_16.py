TOPIC_NAME = "16. Системи нерівностей"
TASKS = [
    # ==========================================
    # ТЕСТОВІ ЗАВДАННЯ (CHOICE) - 30 шт.
    # ==========================================
    {
        "type": "CHOICE",
        "difficulty": 1,
        "text": r"Знайдіть множину розв'язків системи нерівностей $\begin{cases} x > 2 \\ x > 5 \end{cases}$.",
        "svg_code": "",
        "options": [
            (r"А) $(2; 5)$", False),
            (r"Б) $(5; +\infty)$", True),
            (r"В) $(2; +\infty)$", False),
            (r"Г) $[5; +\infty)$", False),
            (r"Д) $\varnothing$", False)
        ],
        "topic_tags": ["16. Системи нерівностей", "13. Лінійні нерівності"]
    },
    {
        "type": "CHOICE",
        "difficulty": 1,
        "text": r"Знайдіть множину розв'язків системи нерівностей $\begin{cases} x \leq 3 \\ x < 7 \end{cases}$.",
        "svg_code": "",
        "options": [
            (r"А) $(-\infty; 3)$", False),
            (r"Б) $(-\infty; 3]$", True),
            (r"В) $(3; 7)$", False),
            (r"Г) $(-\infty; 7)$", False),
            (r"Д) $[3; 7)$", False)
        ],
        "topic_tags": ["16. Системи нерівностей", "13. Лінійні нерівності"]
    },
    {
        "type": "CHOICE",
        "difficulty": 1,
        "text": r"Розв'яжіть систему нерівностей $\begin{cases} x > 4 \\ x < 1 \end{cases}$.",
        "svg_code": "",
        "options": [
            (r"А) $(1; 4)$", False),
            (r"Б) $(-\infty; 1)$", False),
            (r"В) $(4; +\infty)$", False),
            (r"Г) $\varnothing$", True),
            (r"Д) $(-\infty; 1) \cup (4; +\infty)$", False)
        ],
        "topic_tags": ["16. Системи нерівностей"]
    },
    {
        "type": "CHOICE",
        "difficulty": 1,
        "text": r"Знайдіть розв'язок системи нерівностей $\begin{cases} x \geq 3 \\ x \leq 3 \end{cases}$.",
        "svg_code": "",
        "options": [
            (r"А) $(-\infty; +\infty)$", False),
            (r"Б) $\varnothing$", False),
            (r"В) $x = 3$", True),
            (r"Г) $(3; +\infty)$", False),
            (r"Д) $(-\infty; 3)$", False)
        ],
        "topic_tags": ["16. Системи нерівностей"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"Розв'яжіть систему нерівностей $\begin{cases} 2x \geq 4 \\ 3x \leq 15 \end{cases}$.",
        "svg_code": "",
        "options": [
            (r"А) $[2; 5)$", False),
            (r"Б) $(2; 5)$", False),
            (r"В) $[2; 5]$", True),
            (r"Г) $(-\infty; 2] \cup [5; +\infty)$", False),
            (r"Д) $(-\infty; 5]$", False)
        ],
        "topic_tags": ["16. Системи нерівностей", "13. Лінійні нерівності"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"Знайдіть найменший цілий розв'язок системи $\begin{cases} x > -2,5 \\ x < 4 \end{cases}$.",
        "svg_code": "",
        "options": [
            (r"А) $-3$", False),
            (r"Б) $-2$", True),
            (r"В) $-1$", False),
            (r"Г) $0$", False),
            (r"Д) Такого розв'язку немає", False)
        ],
        "topic_tags": ["16. Системи нерівностей", "1. Числові множини"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"Знайдіть найбільший цілий розв'язок системи $\begin{cases} x \geq 1 \\ x \leq 4,8 \end{cases}$.",
        "svg_code": "",
        "options": [
            (r"А) $3$", False),
            (r"Б) $4$", True),
            (r"В) $5$", False),
            (r"Г) $4,8$", False),
            (r"Д) Безліч", False)
        ],
        "topic_tags": ["16. Системи нерівностей", "1. Числові множини"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"Скільки цілих розв'язків має система нерівностей $\begin{cases} x > 0 \\ x < 5 \end{cases}$?",
        "svg_code": "",
        "options": [
            (r"А) $3$", False),
            (r"Б) $4$", True),
            (r"В) $5$", False),
            (r"Г) $6$", False),
            (r"Д) Безліч", False)
        ],
        "topic_tags": ["16. Системи нерівностей", "1. Числові множини"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"Знайдіть область визначення функції $f(x) = \sqrt{x - 1} + \sqrt{4 - x}$.",
        "svg_code": "",
        "options": [
            (r"А) $[1; 4]$", True),
            (r"Б) $(1; 4)$", False),
            (r"В) $[1; +\infty)$", False),
            (r"Г) $(-\infty; 4]$", False),
            (r"Д) $\varnothing$", False)
        ],
        "topic_tags": ["16. Системи нерівностей", "11. Функції та їх властивості"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"Знайдіть область визначення функції $y = \sqrt{x + 2} + \frac{1}{\sqrt{x - 1}}$.",
        "svg_code": "",
        "options": [
            (r"А) $[-2; 1]$", False),
            (r"Б) $(-2; 1)$", False),
            (r"В) $(1; +\infty)$", True),
            (r"Г) $[1; +\infty)$", False),
            (r"Д) $[-2; +\infty)$", False)
        ],
        "topic_tags": ["16. Системи нерівностей", "11. Функції та їх властивості"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"Розв'яжіть подвійну нерівність $1 < 2x - 1 < 5$.",
        "svg_code": "",
        "options": [
            (r"А) $(1; 2)$", False),
            (r"Б) $(1; 3)$", True),
            (r"В) $(0; 2)$", False),
            (r"Г) $[1; 3]$", False),
            (r"Д) $(2; 6)$", False)
        ],
        "topic_tags": ["16. Системи нерівностей", "13. Лінійні нерівності"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"Розв'яжіть систему нерівностей $\begin{cases} x > 3 \\ x \geq 3 \end{cases}$.",
        "svg_code": "",
        "options": [
            (r"А) $[3; +\infty)$", False),
            (r"Б) $(3; +\infty)$", True),
            (r"В) $x = 3$", False),
            (r"Г) $(-\infty; 3)$", False),
            (r"Д) $\varnothing$", False)
        ],
        "topic_tags": ["16. Системи нерівностей"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"Знайдіть суму цілих розв'язків нерівності $-1 \leq x \leq 2$.",
        "svg_code": "",
        "options": [
            (r"А) $0$", False),
            (r"Б) $1$", False),
            (r"В) $2$", True),
            (r"Г) $3$", False),
            (r"Д) $4$", False)
        ],
        "topic_tags": ["16. Системи нерівностей", "1. Числові множини"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"Розв'яжіть систему $\begin{cases} 3(x - 1) < 6 \\ 2x > -4 \end{cases}$.",
        "svg_code": "",
        "options": [
            (r"А) $(-2; 3)$", True),
            (r"Б) $[-2; 3]$", False),
            (r"В) $(-\infty; 3)$", False),
            (r"Г) $(-2; +\infty)$", False),
            (r"Д) $\varnothing$", False)
        ],
        "topic_tags": ["16. Системи нерівностей", "13. Лінійні нерівності"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"Розв'яжіть систему $\begin{cases} \frac{x}{2} > 1 \\ x \leq 4 \end{cases}$.",
        "svg_code": "",
        "options": [
            (r"А) $(2; 4)$", False),
            (r"Б) $[2; 4]$", False),
            (r"В) $(2; 4]$", True),
            (r"Г) $[2; 4)$", False),
            (r"Д) $(-\infty; 4]$", False)
        ],
        "topic_tags": ["16. Системи нерівностей"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"Розв'яжіть систему нерівностей $\begin{cases} x - 1 \geq 0 \\ -x > -5 \end{cases}$.",
        "svg_code": "",
        "options": [
            (r"А) $[1; 5]$", False),
            (r"Б) $(1; 5)$", False),
            (r"В) $[1; 5)$", True),
            (r"Г) $(1; 5]$", False),
            (r"Д) $(-\infty; 5)$", False)
        ],
        "topic_tags": ["16. Системи нерівностей", "13. Лінійні нерівності"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"Розв'яжіть подвійну нерівність $-3 \leq x + 2 \leq 3$.",
        "svg_code": "",
        "options": [
            (r"А) $[-5; 1]$", True),
            (r"Б) $(-5; 1)$", False),
            (r"В) $[-1; 5]$", False),
            (r"Г) $[-3; 3]$", False),
            (r"Д) $[-5; -1]$", False)
        ],
        "topic_tags": ["16. Системи нерівностей"]
    },
    {
        "type": "CHOICE",
        "difficulty": 3,
        "text": r"При яких значеннях параметра $a$ система $\begin{cases} 5x > 15 \\ x < a \end{cases}$ не має розв'язків?",
        "svg_code": "",
        "options": [
            (r"А) $a \geq 3$", False),
            (r"Б) $a \leq 3$", True),
            (r"В) $a < 3$", False),
            (r"Г) $a > 3$", False),
            (r"Д) $a = 0$", False)
        ],
        "topic_tags": ["16. Системи нерівностей"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"Яка з наведених систем нерівностей не має розв'язків?",
        "svg_code": "",
        "options": [
            (r"А) $\begin{cases} x \geq 0 \\ x \leq 0 \end{cases}$", False),
            (r"Б) $\begin{cases} x > 2 \\ x \geq 5 \end{cases}$", False),
            (r"В) $\begin{cases} x < 2 \\ x > 5 \end{cases}$", True),
            (r"Г) $\begin{cases} x < 5 \\ x > 2 \end{cases}$", False),
            (r"Д) $\begin{cases} x \leq 5 \\ x \leq 2 \end{cases}$", False)
        ],
        "topic_tags": ["16. Системи нерівностей"]
    },
    {
        "type": "CHOICE",
        "difficulty": 3,
        "text": r"Розв'яжіть систему $\begin{cases} x^2 \leq 4 \\ x > 0 \end{cases}$.",
        "svg_code": "",
        "options": [
            (r"А) $(0; 2]$", True),
            (r"Б) $[0; 2]$", False),
            (r"В) $[-2; 2]$", False),
            (r"Г) $(0; 4]$", False),
            (r"Д) $[-2; 0)$", False)
        ],
        "topic_tags": ["16. Системи нерівностей", "14. Квадратичні нерівності. Дробово-раціональні нерівності"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"Знайдіть область визначення функції $f(x) = \sqrt{x} + \sqrt{-x}$.",
        "svg_code": "",
        "options": [
            (r"А) $(-\infty; +\infty)$", False),
            (r"Б) $[0; +\infty)$", False),
            (r"В) $(-\infty; 0]$", False),
            (r"Г) $x = 0$", True),
            (r"Д) $\varnothing$", False)
        ],
        "topic_tags": ["16. Системи нерівностей", "11. Функції та їх властивості"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"Розв'яжіть систему $\begin{cases} \frac{x}{3} + \frac{x}{2} < 5 \\ x > 0 \end{cases}$.",
        "svg_code": "",
        "options": [
            (r"А) $(0; 5)$", False),
            (r"Б) $(0; 6)$", True),
            (r"В) $(0; +\infty)$", False),
            (r"Г) $(-\infty; 6)$", False),
            (r"Д) $[0; 6]$", False)
        ],
        "topic_tags": ["16. Системи нерівностей", "8. Дробово-раціональні рівняння"]
    },
    {
        "type": "CHOICE",
        "difficulty": 1,
        "text": r"Знайдіть довжину числового проміжку, який є розв'язком системи $\begin{cases} x \geq -2 \\ x \leq 5 \end{cases}$.",
        "svg_code": "",
        "options": [
            (r"А) $3$", False),
            (r"Б) $5$", False),
            (r"В) $7$", True),
            (r"Г) $8$", False),
            (r"Д) $10$", False)
        ],
        "topic_tags": ["16. Системи нерівностей"]
    },
    {
        "type": "CHOICE",
        "difficulty": 3,
        "text": r"Знайдіть найменший цілий розв'язок системи $\begin{cases} 3x - 2 \geq 4 \\ 5 - x \geq 0 \end{cases}$.",
        "svg_code": "",
        "options": [
            (r"А) $1$", False),
            (r"Б) $2$", True),
            (r"В) $3$", False),
            (r"Г) $4$", False),
            (r"Д) $5$", False)
        ],
        "topic_tags": ["16. Системи нерівностей", "1. Числові множини"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"Знайдіть середину проміжку, який є розв'язком подвійної нерівності $2 \leq x \leq 6$.",
        "svg_code": "",
        "options": [
            (r"А) $3$", False),
            (r"Б) $4$", True),
            (r"В) $5$", False),
            (r"Г) $2$", False),
            (r"Д) $6$", False)
        ],
        "topic_tags": ["16. Системи нерівностей"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"Скільки натуральних розв'язків має система $\begin{cases} x > -1 \\ x < 2 \end{cases}$?",
        "svg_code": "",
        "options": [
            (r"А) $0$", False),
            (r"Б) $1$", True),
            (r"В) $2$", False),
            (r"Г) $3$", False),
            (r"Д) Безліч", False)
        ],
        "topic_tags": ["16. Системи нерівностей", "1. Числові множини"]
    },
    {
        "type": "CHOICE",
        "difficulty": 3,
        "text": r"Обчисліть добуток усіх цілих розв'язків системи $\begin{cases} x \geq 2 \\ x \leq 5 \end{cases}$.",
        "svg_code": "",
        "options": [
            (r"А) $10$", False),
            (r"Б) $60$", False),
            (r"В) $120$", True),
            (r"Г) $20$", False),
            (r"Д) $0$", False)
        ],
        "topic_tags": ["16. Системи нерівностей", "1. Числові множини"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"Знайдіть область визначення функції $f(x) = \frac{\sqrt{x - 3}}{\sqrt{5 - x}}$.",
        "svg_code": "",
        "options": [
            (r"А) $[3; 5]$", False),
            (r"Б) $(3; 5)$", False),
            (r"В) $[3; 5)$", True),
            (r"Г) $(3; 5]$", False),
            (r"Д) $\varnothing$", False)
        ],
        "topic_tags": ["16. Системи нерівностей", "11. Функції та їх властивості"]
    },
    {
        "type": "CHOICE",
        "difficulty": 3,
        "text": r"Розв'яжіть систему $\begin{cases} 4(x - 2) \leq 3x \\ 5x > 10 \end{cases}$.",
        "svg_code": "",
        "options": [
            (r"А) $(2; 8]$", True),
            (r"Б) $[2; 8]$", False),
            (r"В) $(-\infty; 8]$", False),
            (r"Г) $(2; +\infty)$", False),
            (r"Д) $(-\infty; 2) \cup [8; +\infty)$", False)
        ],
        "topic_tags": ["16. Системи нерівностей", "13. Лінійні нерівності"]
    },
    {
        "type": "CHOICE",
        "difficulty": 1,
        "text": r"Використовуючи правило «менше меншого», розв'яжіть систему $\begin{cases} x < 5 \\ x < 10 \end{cases}$.",
        "svg_code": "",
        "options": [
            (r"А) $x < 10$", False),
            (r"Б) $x < 5$", True),
            (r"В) $x > 5$", False),
            (r"Г) $5 < x < 10$", False),
            (r"Д) $\varnothing$", False)
        ],
        "topic_tags": ["16. Системи нерівностей"]
    },

    # ==========================================
    # ЗАВДАННЯ НА ВІДПОВІДНІСТЬ (MATCH) - 4 шт.
    # ==========================================
    {
        "type": "MATCH",
        "difficulty": 1,
        "text": r"Узгодьте систему нерівностей (1–3) із множиною її розв'язків (А–Д).",
        "svg_code": "",
        "options": [
            r"А) $(5; +\infty)$",
            r"Б) $(-\infty; 1)$",
            r"В) $(1; 5)$",
            r"Г) $\varnothing$",
            r"Д) $(-\infty; 5)$"
        ],
        "matches": [
            (r"1. $\begin{cases} x > 1 \\ x > 5 \end{cases}$", r"А) $(5; +\infty)$"),
            (r"2. $\begin{cases} x < 1 \\ x < 5 \end{cases}$", r"Б) $(-\infty; 1)$"),
            (r"3. $\begin{cases} x > 1 \\ x < 5 \end{cases}$", r"В) $(1; 5)$")
        ],
        "topic_tags": ["16. Системи нерівностей"]
    },
    {
        "type": "MATCH",
        "difficulty": 2,
        "text": r"Узгодьте функцію (1–3) з її областю визначення (А–Д).",
        "svg_code": "",
        "options": [
            r"А) $[2; 6]$",
            r"Б) $(2; 6]$",
            r"В) $[2; 6)$",
            r"Г) $(2; 6)$",
            r"Д) $\varnothing$"
        ],
        "matches": [
            (r"1. $y = \sqrt{x - 2} + \sqrt{6 - x}$", r"А) $[2; 6]$"),
            (r"2. $y = \frac{1}{\sqrt{x - 2}} + \sqrt{6 - x}$", r"Б) $(2; 6]$"),
            (r"3. $y = \sqrt{x - 2} + \frac{1}{\sqrt{6 - x}}$", r"В) $[2; 6)$")
        ],
        "topic_tags": ["16. Системи нерівностей", "11. Функції та їх властивості"]
    },
    {
        "type": "MATCH",
        "difficulty": 2,
        "text": r"Узгодьте систему нерівностей (1–3) з кількістю її цілих розв'язків (А–Д).",
        "svg_code": "",
        "options": [
            r"А) $0$",
            r"Б) $1$",
            r"В) $2$",
            r"Г) $3$",
            r"Д) $4$"
        ],
        "matches": [
            (r"1. $\begin{cases} x \geq 0 \\ x \leq 2 \end{cases}$", r"Г) $3$"),
            (r"2. $\begin{cases} x > 0 \\ x < 2 \end{cases}$", r"Б) $1$"),
            (r"3. $\begin{cases} x \geq 0 \\ x < 2 \end{cases}$", r"В) $2$")
        ],
        "topic_tags": ["16. Системи нерівностей", "1. Числові множини"]
    },
    {
        "type": "MATCH",
        "difficulty": 2,
        "text": r"Узгодьте подвійну нерівність (1–3) із множиною її розв'язків (А–Д).",
        "svg_code": "",
        "options": [
            r"А) $[-1; 3]$",
            r"Б) $[0; 2]$",
            r"В) $(-2; 0)$",
            r"Г) $(-\infty; 2]$",
            r"Д) $[-2; 2]$"
        ],
        "matches": [
            (r"1. $-2 \leq x - 1 \leq 2$", r"А) $[-1; 3]$"),
            (r"2. $0 \leq 2x \leq 4$", r"Б) $[0; 2]$"),
            (r"3. $-1 < x + 1 < 1$", r"В) $(-2; 0)$")
        ],
        "topic_tags": ["16. Системи нерівностей"]
    },

    # ==========================================
    # КОРОТКА ВІДПОВІДЬ (SHORT) - 4 шт.
    # ==========================================
    {
        "type": "SHORT",
        "difficulty": 3,
        "text": r"Знайдіть суму всіх цілих розв'язків системи нерівностей $\begin{cases} 2(x - 1) \geq -4 \\ 3x - 5 < 7 \end{cases}$.",
        "svg_code": "",
        "answer": "5",
        "topic_tags": ["16. Системи нерівностей", "13. Лінійні нерівності", "1. Числові множини"]
    },
    {
        "type": "SHORT",
        "difficulty": 3,
        "text": r"Знайдіть добуток усіх цілих розв'язків, які належать області визначення функції $f(x) = \sqrt{x - 2} + \sqrt{5 - x}$.",
        "svg_code": "",
        "answer": "120",
        "topic_tags": ["16. Системи нерівностей", "11. Функції та їх властивості", "1. Числові множини"]
    },
    {
        "type": "SHORT",
        "difficulty": 3,
        "text": r"Знайдіть найменший цілий розв'язок системи нерівностей $\begin{cases} 4x - 3 > 5 \\ 2x - 12 \leq 0 \end{cases}$.",
        "svg_code": "",
        "answer": "3",
        "topic_tags": ["16. Системи нерівностей", "13. Лінійні нерівності"]
    },
    {
        "type": "SHORT",
        "difficulty": 3,
        "text": r"Скільки цілих розв'язків має система нерівностей $\begin{cases} x^2 \leq 9 \\ x > -1 \end{cases}$?",
        "svg_code": "",
        "answer": "4",
        "topic_tags": ["16. Системи нерівностей", "14. Квадратичні нерівності. Дробово-раціональні нерівності", "1. Числові множини"]
    }
]