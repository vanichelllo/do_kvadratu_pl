TOPIC_NAME = "2.7. Розкладання многочлена на множники. Винесення спільного множника за дужки"
COURSE = "Алгебра (7-9 класи)"
GRADE = "7 клас"

TASKS = [
    # ===== СХОДИНКА 1 =====
    # --- Моделювання ---
    {
        "type": "CHOICE", "difficulty": 1, "skill": "MODEL",
        "text": r"Яка рівність є розкладанням на множники?",
        "options": [(r"$5x + 5y = 5(x + y)$", True), (r"$5(x + y) = 5x + 5y$", False), (r"$x^2 + x = x^2 + x$", False), (r"$x(x + 1) = x^2 + x$", False)],
        "hint": "Розкладання — перетворення суми в добуток.",
        "solution": r"Лише в першій рівності сума записана як добуток.",
    },
    {
        "type": "FIELDS", "difficulty": 1, "skill": "MODEL",
        "text": r"Знайдіть спільний множник виразу $6a + 9b$ і вираз у дужках: $6a + 9b = 3(\ldots)$. Укажіть коефіцієнти при $a$ і $b$ у дужках.",
        "fields": [("При $a$:", "2"), ("При $b$:", "3")],
        "hint": "Поділіть кожен член на $3$.",
        "solution": r"$6a + 9b = 3(2a + 3b)$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "MODEL",
        "text": r"Обчисліть зручним способом: $47 \cdot 13 + 47 \cdot 87$.",
        "answer": "4700",
        "hint": "Винесіть $47$ за дужки.",
        "solution": r"$47(13 + 87) = 47 \cdot 100 = 4700$.",
    },
    {
        "type": "TF", "difficulty": 1, "skill": "MODEL",
        "text": r"Правда чи ні?",
        "statements": [(r"Спільний множник $4x^2 + 8x$ — це $4x$", True), (r"Спільний множник $x^3 + x^2$ — це $x^3$", False), (r"$ab + a = a(b + 1)$", True)],
        "hint": "Змінну беремо з найменшим показником.",
        "solution": r"$x^3 + x^2 = x^2(x + 1)$: найменший степінь — $x^2$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "MODEL",
        "text": r"Обчисліть зручним способом: $2{,}5 \cdot 17 - 2{,}5 \cdot 7$.",
        "answer": "25",
        "hint": "Винесіть $2{,}5$.",
        "solution": r"$2{,}5(17 - 7) = 25$.",
    },
    # --- Розв'язування ---
    {
        "type": "CHOICE", "difficulty": 1, "skill": "SOLVE",
        "text": r"Розкладіть на множники: $8x - 12$.",
        "options": [(r"$4(2x - 3)$", True), (r"$4(2x - 12)$", False), (r"$2(4x - 12)$", False), (r"$4(2x + 3)$", False)],
        "hint": "НСД$(8, 12) = 4$.",
        "solution": r"$8x - 12 = 4(2x - 3)$. $2(4x - 6)$ — теж добуток, але множник не найбільший.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "SOLVE",
        "text": r"Розкладіть на множники: $x^2 - 7x$.",
        "options": [(r"$x(x - 7)$", True), (r"$x(x - 7x)$", False), (r"$7(x^2 - x)$", False), (r"$x^2(1 - 7)$", False)],
        "hint": "Спільний множник — $x$.",
        "solution": r"$x^2 - 7x = x(x - 7)$.",
    },
    {
        "type": "FIELDS", "difficulty": 1, "skill": "SOLVE",
        "text": r"$10a^2 + 15a = 5a(\ldots)$. Укажіть вираз у дужках: коефіцієнт при $a$ і вільний член.",
        "fields": [("При $a$:", "2"), ("Вільний член:", "3")],
        "hint": "$10a^2 : 5a$ і $15a : 5a$.",
        "solution": r"$10a^2 + 15a = 5a(2a + 3)$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"$3y^2 + 3y = 3y(y + k)$. Знайдіть $k$.",
        "answer": "1",
        "hint": "$3y : 3y = ?$",
        "solution": r"$3y : 3y = 1$: $3y(y + 1)$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"Розв'яжіть рівняння $x^2 - 4x = 0$. Укажіть ненульовий корінь.",
        "answer": "4",
        "hint": "$x(x - 4) = 0$.",
        "solution": r"$x = 0$ або $x = 4$.",
    },
    # --- Аналіз ---
    {
        "type": "ERROR", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Оля розкладала $5x^2 + 5x$. У якому кроці помилка?",
        "steps": [r"Спільний множник — $5x$", r"$5x^2 : 5x = x$, $\;5x : 5x = 0$", r"$5x(x + 0) = 5x \cdot x$"],
        "wrong": 1,
        "hint": "Скільки буде $5x : 5x$?",
        "solution": r"$5x : 5x = 1$: $5x(x + 1)$.",
    },
    {
        "type": "MULTI", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Які розкладання правильні?",
        "options": [(r"$4a + 4 = 4(a + 1)$", True), (r"$a^2 + 3a = a(a + 3)$", True), (r"$6x - 3 = 3(2x - 3)$", False), (r"$2b^2 - b = b(2b - 1)$", True)],
        "hint": "Розкрийте дужки й порівняйте.",
        "solution": r"$3(2x - 3) = 6x - 9 \ne 6x - 3$; має бути $3(2x - 1)$.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Тарас: «$12x + 18 = 2(6x + 9)$ — розкладання завершено». Чи правий він?",
        "options": [(r"Ні, можна винести $6$: $6(2x + 3)$", True), (r"Так", False), (r"Ні, треба $3(4x + 6)$", False), (r"Ні, рівність хибна", False)],
        "hint": "Чи є в дужках ще спільний множник?",
        "solution": r"$6x + 9 = 3(2x + 3)$, тож найбільший спільний множник — $6$.",
    },
    {
        "type": "GROUP", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Розподіліть многочлени за спільним множником.",
        "groups": [r"$3x$", r"$x^2$"],
        "items": [(r"$6x^2 + 3x$", 0), (r"$x^3 - x^2$", 1), (r"$9x - 3x^2$", 0), (r"$x^4 + 2x^2$", 1), (r"$3x^3 + 12x$", 0), (r"$5x^2 + x^3$", 1)],
        "hint": "Знайдіть НСД коефіцієнтів і найменший степінь $x$.",
        "solution": r"$3x(2x + 1)$, $3x(3 - x)$, $3x(x^2 + 4)$; $x^2(x - 1)$, $x^2(x^2 + 2)$, $x^2(5 + x)$.",
    },
    {
        "type": "TF", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Перевірте розкриттям дужок. Правда чи ні?",
        "statements": [(r"$7a - 7b = 7(a - b)$", True), (r"$-2x - 4 = -2(x - 2)$", False), (r"$x^2y + xy^2 = xy(x + y)$", True)],
        "hint": "$-2 \\cdot (-2) = 4$.",
        "solution": r"$-2(x - 2) = -2x + 4$; правильно $-2(x + 2)$.",
    },

    # ===== СХОДИНКА 2 =====
    # --- Моделювання ---
    {
        "type": "SHORT", "difficulty": 2, "skill": "MODEL",
        "text": r"Обчисліть: $0{,}73 \cdot 54 + 0{,}73 \cdot 46$.",
        "answer": "73",
        "solution": r"$0{,}73 \cdot 100 = 73$.",
    },
    {
        "type": "FIELDS", "difficulty": 2, "skill": "MODEL",
        "text": r"$12a^3b^2 - 18a^2b^3 = k\,a^m b^n(2a - 3b)$. Знайдіть $k$, $m$, $n$.",
        "fields": [("$k$:", "6"), ("$m$:", "2"), ("$n$:", "2")],
        "solution": r"НСД $6$, $a^2$, $b^2$: $6a^2b^2(2a - 3b)$.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "MODEL",
        "text": r"Площа прямокутника $3x^2 + 6x$, одна сторона $3x$. Яка друга сторона?",
        "options": [(r"$x + 2$", True), (r"$x + 6$", False), (r"$3x + 2$", False), (r"$x^2 + 2$", False)],
        "solution": r"$3x^2 + 6x = 3x(x + 2)$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "MODEL",
        "text": r"Обчисліть: $17^2 + 17 \cdot 83$.",
        "answer": "1700",
        "solution": r"$17(17 + 83) = 1700$.",
    },
    {
        "type": "TF", "difficulty": 2, "skill": "MODEL",
        "text": r"Правда чи ні?",
        "statements": [(r"$a(x - y) + b(x - y) = (x - y)(a + b)$", True), (r"$b - a = -(a - b)$", True), (r"$3(a - b) - c(b - a) = (a - b)(3 - c)$", False)],
        "solution": r"$-c(b - a) = c(a - b)$, тож $(a - b)(3 + c)$.",
    },
    # --- Розв'язування ---
    {
        "type": "CHOICE", "difficulty": 2, "skill": "SOLVE",
        "text": r"Розкладіть на множники: $4m^3 - 6m^2 + 2m$.",
        "options": [(r"$2m(2m^2 - 3m + 1)$", True), (r"$2m(2m^2 - 3m)$", False), (r"$m(4m^2 - 6m + 2)$", False), (r"$2m^2(2m - 3 + 1)$", False), (r"$2(2m^3 - 3m^2 + m)$", False)],
        "solution": r"Ділимо кожен член на $2m$: $2m^2$, $-3m$, $1$.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "SOLVE",
        "text": r"Розкладіть на множники: $x(a + 3) - 2(a + 3)$.",
        "options": [(r"$(a + 3)(x - 2)$", True), (r"$(a + 3)(x + 2)$", False), (r"$x - 2(a + 3)$", False), (r"$2x(a + 3)$", False)],
        "solution": r"Спільний множник — $(a + 3)$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Розв'яжіть рівняння $3x^2 + 12x = 0$. Укажіть ненульовий корінь.",
        "answer": "-4",
        "solution": r"$3x(x + 4) = 0$: $x = 0$ або $x = -4$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Знайдіть значення виразу $a^2b + ab^2$, якщо $ab = 5$, $a + b = 4$.",
        "answer": "20",
        "solution": r"$ab(a + b) = 5 \cdot 4 = 20$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Розв'яжіть рівняння $x^2 = 9x$. Скільки коренів?",
        "answer": "2",
        "solution": r"$x(x - 9) = 0$: $0$ і $9$ — два корені.",
    },
    # --- Аналіз ---
    {
        "type": "ERROR", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Тарас розв'язував $x^2 = 5x$. У якому кроці помилка?",
        "steps": [r"Поділимо обидві частини на $x$", r"$x = 5$", r"Відповідь: $5$"],
        "wrong": 0,
        "solution": r"Ділити на $x$ не можна ($x$ може бути $0$). $x(x - 5) = 0$: $x = 0$ або $x = 5$.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Розкладіть з від'ємним спільним множником: $-4x^2 - 8x$.",
        "options": [(r"$-4x(x + 2)$", True), (r"$-4x(x - 2)$", False), (r"$-4x(-x - 2)$", False), (r"$4x(x + 2)$", False), (r"$-4(x^2 - 2x)$", False)],
        "solution": r"$-4x^2 : (-4x) = x$, $-8x : (-4x) = 2$.",
    },
    {
        "type": "MULTI", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Які вирази дорівнюють $5a - 5b$?",
        "options": [(r"$5(a - b)$", True), (r"$-5(b - a)$", True), (r"$5(b - a)$", False), (r"$-5(a - b)$", False)],
        "solution": r"$-5(b - a) = -5b + 5a$ ✓.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Доведіть, що $7^5 - 7^4$ ділиться на $6$: знайдіть частку $(7^5 - 7^4) : 6$.",
        "answer": "2401",
        "solution": r"$7^4(7 - 1) = 6 \cdot 7^4$; частка $7^4 = 2401$.",
    },
    {
        "type": "TF", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [(r"$x^5 + x^3$ ділиться на $x^3$ при $x \ne 0$", True), (r"$n^2 + n$ — завжди парне для натурального $n$", True), (r"$x^2 + 2x$ дорівнює нулю лише при $x = 0$", False)],
        "solution": r"$x^3(x^2 + 1)$; $n(n + 1)$ — добуток сусідніх чисел, один парний; $x(x + 2) = 0$ і при $x = -2$.",
    },

    # ===== СХОДИНКА 3 =====
    # --- Моделювання ---
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"Обчисліть: $\dfrac{3^{10} - 3^{8}}{3^8}$.",
        "answer": "8",
        "solution": r"$3^8(3^2 - 1) : 3^8 = 8$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"Обчисліть: $2^{15} - 2^{14} - 2^{13}$, поділене на $2^{13}$.",
        "answer": "1",
        "solution": r"$2^{13}(4 - 2 - 1) = 2^{13}$; частка $1$.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "MODEL",
        "text": r"Сума трьох послідовних натуральних чисел $n$, $n + 1$, $n + 2$ завжди ділиться на:",
        "options": [(r"$3$", True), (r"$2$", False), (r"$6$", False), (r"$5$", False), (r"$9$", False)],
        "solution": r"$3n + 3 = 3(n + 1)$.",
    },
    {
        "type": "FIELDS", "difficulty": 3, "skill": "MODEL",
        "text": r"$a^{n+2} + a^{n} = a^n(a^k + 1)$. Знайдіть $k$ і значення виразу при $a = 2$, $n = 3$.",
        "fields": [("$k$:", "2"), ("Значення:", "40")],
        "solution": r"$a^n \cdot a^2 = a^{n+2}$, $k = 2$; $8 \cdot 5 = 40$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"Знайдіть значення виразу $x^2y + xy^2 - xy$, якщо $x + y = 6$, $xy = 4$.",
        "answer": "20",
        "solution": r"$xy(x + y - 1) = 4 \cdot 5 = 20$.",
    },
    # --- Розв'язування ---
    {
        "type": "CHOICE", "difficulty": 3, "skill": "SOLVE",
        "text": r"Розкладіть на множники: $5a(b - 2) - 3(2 - b)$.",
        "options": [(r"$(b - 2)(5a + 3)$", True), (r"$(b - 2)(5a - 3)$", False), (r"$(2 - b)(5a + 3)$", False), (r"$(b - 2) \cdot 2a$", False), (r"$5a - 3(b - 2)$", False)],
        "solution": r"$-3(2 - b) = 3(b - 2)$: $(b - 2)(5a + 3)$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Розв'яжіть рівняння $x(x - 3) - 2(x - 3) = 0$. Укажіть більший корінь.",
        "answer": "3",
        "solution": r"$(x - 3)(x - 2) = 0$: $3$ і $2$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Розв'яжіть рівняння $6x^2 = 2x$. Укажіть ненульовий корінь (звичайним дробом, наприклад 2/5).",
        "answer": "1/3",
        "solution": r"$2x(3x - 1) = 0$: $x = \dfrac13 \approx 0{,}33$.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "SOLVE",
        "text": r"Розкладіть на множники: $(x - 1)^2 + 3(x - 1)$.",
        "options": [(r"$(x - 1)(x + 2)$", True), (r"$(x - 1)(x + 3)$", False), (r"$(x - 1)(x - 4)$", False), (r"$4(x - 1)$", False), (r"$(x - 1)^2(x + 2)$", False)],
        "solution": r"$(x - 1)(x - 1 + 3) = (x - 1)(x + 2)$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Розв'яжіть рівняння $(2x - 1)(x + 4) = 3(x + 4)$. Укажіть корінь, відмінний від $-4$.",
        "answer": "2",
        "solution": r"$(x + 4)(2x - 1 - 3) = 0$: $x = -4$ або $2x = 4$, $x = 2$.",
    },
    # --- Аналіз ---
    {
        "type": "ERROR", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Оля розкладала $2a(x - y) - (y - x)$. У якому кроці помилка?",
        "steps": [r"$-(y - x) = (x - y)$", r"$= 2a(x - y) + (x - y)$", r"$= (x - y) \cdot 2a$"],
        "wrong": 2,
        "solution": r"Залишається $1$: $(x - y)(2a + 1)$.",
    },
    {
        "type": "TF", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Для будь-якого натурального $n$ правда чи ні?",
        "statements": [(r"$5^{n+1} - 5^n$ ділиться на $4$", True), (r"$n^3 + n^2$ ділиться на $n + 1$", True), (r"$2^{n+3} - 2^n$ ділиться на $5$", False)],
        "solution": r"$5^n \cdot 4$; $n^2(n + 1)$; $2^n(8 - 1) = 7 \cdot 2^n$ — ділиться на $7$, а не на $5$.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "ANALYZE",
        "text": r"При якому $a$ рівняння $x^2 + ax = 0$ має лише один корінь?",
        "options": [(r"$a = 0$", True), (r"$a = 1$", False), (r"при будь-якому", False), (r"$a = -1$", False), (r"такого $a$ немає", False)],
        "solution": r"$x(x + a) = 0$: корені $0$ і $-a$ збігаються лише при $a = 0$.",
    },
    {
        "type": "MULTI", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Які вирази діляться на $11$ при будь-якому натуральному $n$?",
        "options": [(r"$12^n \cdot 12 - 12^n$", True), (r"$10^{n+1} + 10^n$", True), (r"$3^{n+2} + 3^n$", False), (r"$6^{n+1} + 5 \cdot 6^n$", True)],
        "solution": r"$12^n \cdot 11$; $10^n \cdot 11$; $3^n \cdot 10$; $6^n(6 + 5) = 11 \cdot 6^n$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Скільки коренів має рівняння $x^3 - 4x^2 = 0$?",
        "answer": "2",
        "solution": r"$x^2(x - 4) = 0$: $x = 0$ або $x = 4$ — два корені.",
    },

    # ===== БОСИ =====
    {
        "type": "SHORT", "difficulty": 4, "skill": "MODEL",
        "text": r"Обчисліть: $\dfrac{2^{20} + 2^{19}}{2^{19} - 2^{18}}$.",
        "answer": "6",
        "solution": r"$\dfrac{2^{19}(2 + 1)}{2^{18}(2 - 1)} = 2 \cdot 3 = 6$.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "MODEL",
        "text": r"Обчисліть: $\dfrac{2025^2 + 2025}{2026}$.",
        "answer": "2025",
        "solution": r"$\dfrac{2025(2025 + 1)}{2026} = 2025$.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "SOLVE",
        "text": r"Розв'яжіть рівняння $x^3 = 9x$. Скільки коренів?",
        "answer": "3",
        "solution": r"$x(x^2 - 9) = 0$: $x = 0$ або $x^2 = 9$, $x = \pm 3$ — три корені.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "SOLVE",
        "text": r"Знайдіть значення $a^2b - ab^2$, якщо $a - b = 3$, $ab = -2$.",
        "answer": "-6",
        "solution": r"$ab(a - b) = -2 \cdot 3 = -6$.",
    },
    {
        "type": "TF", "difficulty": 4, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [(r"$81^7 - 27^9 - 9^{13}$ ділиться на $45$", True), (r"$10^{n} - 1$ ділиться на $9$ для будь-якого натурального $n$", True), (r"$2^{100} + 2^{99}$ ділиться на $5$", False)],
        "solution": r"$3^{28} - 3^{27} - 3^{26} = 3^{26}(9 - 3 - 1) = 5 \cdot 3^{26}$, ділиться на $5 \cdot 9$. $10^n - 1 = 99\ldots9$. $2^{99} \cdot 3$ — не ділиться на $5$.",
    },
    {
        "type": "SHORT", "difficulty": 5, "skill": "SOLVE",
        "text": r"Розв'яжіть рівняння $(x - 2)^2 = 3(x - 2)$ і знайдіть суму його коренів.",
        "answer": "7",
        "solution": r"$(x - 2)(x - 2 - 3) = 0$ (не ділимо на $x - 2$!): $x = 2$ або $x = 5$; сума $7$.",
    },
    {
        "type": "SHORT", "difficulty": 5, "skill": "ANALYZE",
        "text": r"Знайдіть найменше натуральне $n \gt 1$, для якого $n^2 - n$ ділиться на $12$.",
        "answer": "4",
        "solution": r"$n(n - 1)$: $n = 2$: $2$; $3$: $6$; $4$: $12$ ✓.",
    },
]
