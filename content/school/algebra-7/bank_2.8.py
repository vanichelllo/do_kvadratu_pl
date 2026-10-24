TOPIC_NAME = "2.8. Розкладання многочлена на множники. Спосіб групування"
COURSE = "Алгебра (7-9 класи)"
GRADE = "7 клас"

TASKS = [
    # ===== СХОДИНКА 1 =====
    # --- Моделювання ---
    {
        "type": "CHOICE", "difficulty": 1, "skill": "MODEL",
        "text": r"Як згрупувати члени многочлена $ax + ay + 2x + 2y$?",
        "options": [(r"$(ax + ay) + (2x + 2y)$", True), (r"$(ax + 2y) + (ay + 2x)$", False), (r"$ax + (ay + 2x) + 2y$", False), (r"групувати не можна", False)],
        "hint": "У кожній групі має бути спільний множник.",
        "solution": r"$a(x + y) + 2(x + y)$ — однакові дужки.",
    },
    {
        "type": "FIELDS", "difficulty": 1, "skill": "MODEL",
        "text": r"$bx + by + 4x + 4y = (x + y)(b + k)$. Знайдіть $k$ і значення виразу при $x = 1$, $y = 2$, $b = 3$.",
        "fields": [("$k$:", "4"), ("Значення:", "21")],
        "hint": "$b(x + y) + 4(x + y)$.",
        "solution": r"$k = 4$; $(1 + 2)(3 + 4) = 21$.",
    },
    {
        "type": "TF", "difficulty": 1, "skill": "MODEL",
        "text": r"Правда чи ні?",
        "statements": [(r"$a(x + y) + 3(x + y) = (x + y)(a + 3)$", True), (r"$a(x + y) + 3(x + y)$ — уже добуток", False), (r"Групування — це двічі застосований розподільний закон", True)],
        "hint": "Добуток — коли останньою дією є множення.",
        "solution": r"$a(x + y) + 3(x + y)$ — сума двох доданків, треба винести $(x + y)$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "MODEL",
        "text": r"Обчисліть зручним способом: $7 \cdot 15 + 7 \cdot 5 + 3 \cdot 15 + 3 \cdot 5$.",
        "answer": "200",
        "hint": "$7(15 + 5) + 3(15 + 5)$.",
        "solution": r"$20 \cdot (7 + 3) = 200$.",
    },
    {
        "type": "MULTI", "difficulty": 1, "skill": "MODEL",
        "text": r"Які многочлени можна розкласти групуванням на $(x + 2)(y + 3)$?",
        "options": [(r"$xy + 3x + 2y + 6$", True), (r"$xy + 2y + 3x + 6$", True), (r"$xy + 6$", False), (r"$xy + 3x + 2y + 5$", False)],
        "hint": "Перемножте $(x + 2)(y + 3)$.",
        "solution": r"$(x + 2)(y + 3) = xy + 3x + 2y + 6$; порядок доданків не важливий.",
    },
    # --- Розв'язування ---
    {
        "type": "CHOICE", "difficulty": 1, "skill": "SOLVE",
        "text": r"Розкладіть на множники: $3a + 3b + ca + cb$.",
        "options": [(r"$(a + b)(3 + c)$", True), (r"$3c(a + b)$", False), (r"$(a + b)(3 + cb)$", False), (r"$(3 + c)(a - b)$", False)],
        "hint": "$3(a + b) + c(a + b)$.",
        "solution": r"$(a + b)(3 + c)$.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "SOLVE",
        "text": r"Розкладіть на множники: $x^2 + 4x + 3x + 12$.",
        "options": [(r"$(x + 4)(x + 3)$", True), (r"$(x + 4)(x + 12)$", False), (r"$x(x + 4) + 3$", False), (r"$(x + 3)(x + 12)$", False)],
        "hint": "$x(x + 4) + 3(x + 4)$.",
        "solution": r"$(x + 4)(x + 3)$.",
    },
    {
        "type": "FIELDS", "difficulty": 1, "skill": "SOLVE",
        "text": r"$x(a - b) + 5(a - b) = (a - b)(x + k)$. Знайдіть $k$.",
        "fields": [("$k$:", "5")],
        "hint": "Винесіть $(a - b)$.",
        "solution": r"$(a - b)(x + 5)$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"Знайдіть значення $ax + bx + ay + by$, якщо $a + b = 5$, $x + y = 4$.",
        "answer": "20",
        "hint": "$(a + b)(x + y)$.",
        "solution": r"$5 \cdot 4 = 20$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"Розв'яжіть рівняння $x(x - 4) + 3(x - 4) = 0$. Укажіть додатний корінь.",
        "answer": "4",
        "hint": "$(x - 4)(x + 3) = 0$.",
        "solution": r"$x = 4$ або $x = -3$.",
    },
    # --- Аналіз ---
    {
        "type": "ERROR", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Оля розкладала $mx + my + x + y$. У якому кроці помилка?",
        "steps": [r"$m(x + y) + (x + y)$", r"$= (x + y) \cdot m$"],
        "wrong": 1,
        "hint": "Що лишається від другої групи?",
        "solution": r"$(x + y) = 1 \cdot (x + y)$: $(x + y)(m + 1)$.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Тарас записав: $ax + ay + 2x + 2y = a(x + y) + 2(x + y)$ — і вважає, що розклав. Чи правий він?",
        "options": [(r"Ні, треба ще винести $(x + y)$", True), (r"Так", False), (r"Ні, групування неправильне", False), (r"Ні, треба винести $a$", False)],
        "hint": "Чи є запис добутком?",
        "solution": r"Остання дія — додавання; результат: $(x + y)(a + 2)$.",
    },
    {
        "type": "TF", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Перевірте розкриттям дужок. Правда чи ні?",
        "statements": [(r"$xy - x + 2y - 2 = (y - 1)(x + 2)$", True), (r"$ab + a + b + 1 = (a + 1)(b + 1)$", True), (r"$2x + 2y + xy + y^2 = (x + y)(2 + x)$", False)],
        "hint": "Розкрийте праві частини.",
        "solution": r"$(x + y)(2 + y) = 2x + 2y + xy + y^2$ — множник $(2 + y)$, не $(2 + x)$.",
    },
    {
        "type": "GROUP", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Який спільний множник з'явиться після групування?",
        "groups": [r"$(a + b)$", r"$(x - 3)$"],
        "items": [(r"$5a + 5b + ca + cb$", 0), (r"$x^2 - 3x + 2x - 6$", 1), (r"$ax + bx + 4a + 4b$", 0), (r"$xy - 3y + x - 3$", 1)],
        "hint": "Згрупуйте попарно.",
        "solution": r"$5(a + b) + c(a + b)$; $x(x - 3) + 2(x - 3)$; $x(a + b) + 4(a + b)$; $y(x - 3) + (x - 3)$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Скільки коренів має рівняння $(x - 1)(x + 6) = 0$?",
        "answer": "2",
        "hint": "Добуток дорівнює нулю, коли хоча б один множник — нуль.",
        "solution": r"$x = 1$ або $x = -6$.",
    },

    # ===== СХОДИНКА 2 =====
    # --- Моделювання ---
    {
        "type": "SHORT", "difficulty": 2, "skill": "MODEL",
        "text": r"Обчисліть: $48 \cdot 23 - 48 \cdot 13 + 52 \cdot 23 - 52 \cdot 13$.",
        "answer": "1000",
        "solution": r"$48(23 - 13) + 52(23 - 13) = 10 \cdot 100 = 1000$.",
    },
    {
        "type": "FIELDS", "difficulty": 2, "skill": "MODEL",
        "text": r"$x^3 - 2x^2 + 3x - 6 = (x - a)(x^2 + b)$. Знайдіть $a$ і $b$.",
        "fields": [("$a$:", "2"), ("$b$:", "3")],
        "solution": r"$x^2(x - 2) + 3(x - 2) = (x - 2)(x^2 + 3)$.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "MODEL",
        "text": r"Прямокутник має площу $ab + 3a + 2b + 6$. Якими можуть бути його сторони?",
        "options": [(r"$a + 2$ і $b + 3$", True), (r"$a + 3$ і $b + 2$", False), (r"$ab$ і $6$", False), (r"$a + b$ і $5$", False), (r"$a + 6$ і $b$", False)],
        "solution": r"$a(b + 3) + 2(b + 3) = (b + 3)(a + 2)$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "MODEL",
        "text": r"Знайдіть значення $a^2 - ab + 3a - 3b$, якщо $a - b = 2$, $a = 7$.",
        "answer": "20",
        "solution": r"$a(a - b) + 3(a - b) = (a - b)(a + 3) = 2 \cdot 10 = 20$.",
    },
    {
        "type": "TF", "difficulty": 2, "skill": "MODEL",
        "text": r"Многочлен $xy + 2x - 3y - 6$. Правда чи ні?",
        "statements": [(r"$= x(y + 2) - 3(y + 2)$", True), (r"$= (y + 2)(x - 3)$", True), (r"$= (y - 2)(x + 3)$", False)],
        "solution": r"$-3y - 6 = -3(y + 2)$. Перевірка: $(y + 2)(x - 3) = xy - 3y + 2x - 6$ ✓.",
    },
    # --- Розв'язування ---
    {
        "type": "CHOICE", "difficulty": 2, "skill": "SOLVE",
        "text": r"Розкладіть на множники: $ax - bx - ay + by$.",
        "options": [(r"$(a - b)(x - y)$", True), (r"$(a - b)(x + y)$", False), (r"$(a + b)(x - y)$", False), (r"$(a - b)(y - x)$", False), (r"$x(a - b) - y$", False)],
        "solution": r"$x(a - b) - y(a - b) = (a - b)(x - y)$.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "SOLVE",
        "text": r"Розкладіть на множники: $3x^2 - 6x + xy - 2y$.",
        "options": [(r"$(x - 2)(3x + y)$", True), (r"$(x - 2)(3x - y)$", False), (r"$(x + 2)(3x + y)$", False), (r"$3x(x - 2) + y$", False), (r"$(3x - 2)(x + y)$", False)],
        "solution": r"$3x(x - 2) + y(x - 2)$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Розв'яжіть рівняння $x^2 - 7x + 2x - 14 = 0$. Укажіть менший корінь.",
        "answer": "-2",
        "solution": r"$x(x - 7) + 2(x - 7) = (x - 7)(x + 2)$: $7$ і $-2$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Знайдіть значення $xy - 2x + 5y - 10$ при $x = 15$, $y = 2{,}4$.",
        "answer": "8",
        "solution": r"$(y - 2)(x + 5) = 0{,}4 \cdot 20 = 8$.",
    },
    {
        "type": "FIELDS", "difficulty": 2, "skill": "SOLVE",
        "text": r"$a^3 + a^2 + a + 1 = (a + 1)(a^2 + k)$. Знайдіть $k$ і значення многочлена при $a = 2$.",
        "fields": [("$k$:", "1"), ("Значення:", "15")],
        "solution": r"$a^2(a + 1) + (a + 1)$; $3 \cdot 5 = 15$.",
    },
    # --- Аналіз ---
    {
        "type": "ERROR", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Тарас розкладав $ax - ay - 3x + 3y$. У якому кроці помилка?",
        "steps": [r"$a(x - y) - 3(x + y)$", r"Однакових дужок немає — розкласти не можна"],
        "wrong": 0,
        "solution": r"$-3x + 3y = -3(x - y)$: $(x - y)(a - 3)$.",
    },
    {
        "type": "MULTI", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Які групування многочлена $ab + 2a + 3b + 6$ ведуть до мети?",
        "options": [(r"$(ab + 2a) + (3b + 6)$", True), (r"$(ab + 3b) + (2a + 6)$", True), (r"$(ab + 6) + (2a + 3b)$", False)],
        "solution": r"$a(b + 2) + 3(b + 2)$ або $b(a + 3) + 2(a + 3)$; третє — без спільних множників.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Чому дорівнює $2x - 2 + xy - y$ при $x = 1$?",
        "options": [(r"$0$ при будь-якому $y$", True), (r"$y$", False), (r"$2$", False), (r"$-y$", False), (r"залежить від $y$", False)],
        "solution": r"$(x - 1)(2 + y)$; при $x = 1$ — $0$.",
    },
    {
        "type": "TF", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [(r"Будь-який многочлен з чотирьох членів розкладається групуванням", False), (r"Іноді треба спробувати інше групування", True), (r"Перевірити розклад можна, перемноживши множники", True)],
        "solution": r"$x^2 + y^2 + x + 1$ не розкладається групуванням.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Скільки коренів має рівняння $x^3 + 2x^2 + x + 2 = 0$?",
        "answer": "1",
        "solution": r"$(x + 2)(x^2 + 1) = 0$; $x^2 + 1 \gt 0$, тож лише $x = -2$.",
    },

    # ===== СХОДИНКА 3 =====
    # --- Моделювання ---
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"Обчисліть: $12{,}5 \cdot 3{,}7 + 12{,}5 \cdot 6{,}3 - 2{,}5 \cdot 3{,}7 - 2{,}5 \cdot 6{,}3$.",
        "answer": "100",
        "solution": r"$(3{,}7 + 6{,}3)(12{,}5 - 2{,}5) = 10 \cdot 10 = 100$.",
    },
    {
        "type": "FIELDS", "difficulty": 3, "skill": "MODEL",
        "text": r"$x^3 + 3x^2 - 2x - 6 = (x + a)(x^2 + b)$. Знайдіть $a$ і $b$.",
        "fields": [("$a$:", "3"), ("$b$:", "-2")],
        "solution": r"$x^2(x + 3) - 2(x + 3) = (x + 3)(x^2 - 2)$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"Знайдіть значення $a^3 + a^2b - ab - b^2$, якщо $a + b = 3$, $a^2 - b = 4$.",
        "answer": "12",
        "solution": r"$a^2(a + b) - b(a + b) = (a + b)(a^2 - b) = 12$.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "MODEL",
        "text": r"Розкладіть на множники: $ax^2 + bx^2 - ay - by + a + b$.",
        "options": [(r"$(a + b)(x^2 - y + 1)$", True), (r"$(a + b)(x^2 - y)$", False), (r"$(a - b)(x^2 + y + 1)$", False), (r"$(a + b)(x^2 + y + 1)$", False), (r"$(x^2 - y)(a + b + 1)$", False)],
        "solution": r"$x^2(a + b) - y(a + b) + (a + b)$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"Обчисліть: $\dfrac{37 \cdot 63 + 37 \cdot 37}{63 \cdot 37 + 63 \cdot 63}$ і запишіть звичайним дробом (наприклад, 2/3).",
        "answer": "37/63",
        "solution": r"$\dfrac{37 \cdot 100}{63 \cdot 100} = \dfrac{37}{63}$.",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Розв'яжіть рівняння $x^3 - 5x^2 - x + 5 = 0$. Укажіть суму коренів.",
        "answer": "5",
        "solution": r"$x^2(x - 5) - (x - 5) = (x - 5)(x^2 - 1) = 0$: $5$, $1$, $-1$; сума $5$.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "SOLVE",
        "text": r"Розкладіть на множники: $x^2y - y + x^2 - 1$.",
        "options": [(r"$(x^2 - 1)(y + 1)$", True), (r"$(x^2 + 1)(y - 1)$", False), (r"$(x^2 - 1)y$", False), (r"$(x^2 - y)(1 + y)$", False), (r"$x^2(y + 1) - 1$", False)],
        "solution": r"$y(x^2 - 1) + (x^2 - 1)$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Розв'яжіть рівняння $2x^3 - x^2 - 8x + 4 = 0$. Укажіть найбільший корінь.",
        "answer": "2",
        "solution": r"$x^2(2x - 1) - 4(2x - 1) = (2x - 1)(x^2 - 4)$: $0{,}5$, $\pm 2$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Знайдіть значення $x^3 - 3x^2 + 4x - 12$ при $x = 3{,}1$.",
        "answer": "1,361",
        "solution": r"$(x - 3)(x^2 + 4) = 0{,}1 \cdot 13{,}61 = 1{,}361$.",
    },
    {
        "type": "FIELDS", "difficulty": 3, "skill": "SOLVE",
        "text": r"$ab - ac - b^2 + bc = (b - c)(a + kb)$. Знайдіть $k$.",
        "fields": [("$k$:", "-1")],
        "solution": r"$a(b - c) - b(b - c) = (b - c)(a - b)$.",
    },
    # --- Аналіз ---
    {
        "type": "ERROR", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Оля розв'язувала $x^3 - 4x^2 - 9x + 36 = 0$. У якому кроці помилка?",
        "steps": [r"$x^2(x - 4) - 9(x - 4) = 0$", r"$(x - 4)(x^2 - 9) = 0$", r"$x = 4$ або $x = 9$"],
        "wrong": 2,
        "solution": r"$x^2 = 9$ ⟹ $x = \pm 3$. Корені: $4$, $3$, $-3$.",
    },
    {
        "type": "TF", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [(r"$n^3 + n^2 + n + 1$ ділиться на $n + 1$ для натурального $n$", True), (r"$ab + a + b + 1$ при натуральних $a, b$ завжди складене", True), (r"$x^3 - x^2 + x - 1 = 0$ має три корені", False)],
        "solution": r"$(n + 1)(n^2 + 1)$; $(a + 1)(b + 1)$, обидва $\ge 2$; $(x - 1)(x^2 + 1) = 0$ — один корінь.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Розкладіть $x^2 - xy + 4x - 4y$ на множники і знайдіть значення виразу при $x = y$.",
        "options": [(r"$(x - y)(x + 4)$; $0$", True), (r"$(x + y)(x - 4)$; $0$", False), (r"$(x - y)(x + 4)$; $x + 4$", False), (r"$(x - y)(x - 4)$; $0$", False), (r"не розкладається", False)],
        "solution": r"$x(x - y) + 4(x - y)$; при $x = y$ — $0$.",
    },
    {
        "type": "MULTI", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Які числа є коренями рівняння $x^3 + x^2 - 4x - 4 = 0$?",
        "options": [(r"$-1$", True), (r"$2$", True), (r"$-2$", True), (r"$1$", False), (r"$4$", False)],
        "solution": r"$(x + 1)(x^2 - 4) = 0$: $-1$, $\pm 2$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "ANALYZE",
        "text": r"При якому $k$ многочлен $x^2 + kx + 3x + 3k$ дорівнює $(x + 3)(x + 5)$?",
        "answer": "5",
        "solution": r"$x(x + k) + 3(x + k) = (x + k)(x + 3)$ ⟹ $k = 5$.",
    },

    # ===== БОСИ =====
    {
        "type": "SHORT", "difficulty": 4, "skill": "MODEL",
        "text": r"Обчисліть: $\dfrac{2^{10} + 2^{7} + 2^{3} + 1}{2^{3} + 1}$.",
        "answer": "129",
        "solution": r"$2^7(2^3 + 1) + (2^3 + 1) = (2^3 + 1)(2^7 + 1)$; частка $129$.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "MODEL",
        "text": r"Знайдіть значення $xy + x + y$, якщо $(x + 1)(y + 1) = 20$.",
        "answer": "19",
        "solution": r"$xy + x + y + 1 = 20$ ⟹ $xy + x + y = 19$.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "SOLVE",
        "text": r"Розв'яжіть рівняння $x^3 + 2x^2 - 9x - 18 = 0$. Укажіть добуток коренів.",
        "answer": "18",
        "solution": r"$(x + 2)(x^2 - 9)$: $-2$, $3$, $-3$; добуток $18$.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "SOLVE",
        "text": r"Скільки пар натуральних чисел $(x; y)$ задовольняють $xy + x + y = 11$?",
        "answer": "4",
        "solution": r"$(x + 1)(y + 1) = 12$, обидва множники $\ge 2$: $2 \cdot 6$, $3 \cdot 4$, $4 \cdot 3$, $6 \cdot 2$. Пари: $(1; 5)$, $(2; 3)$, $(3; 2)$, $(5; 1)$ — $4$.",
    },
    {
        "type": "TF", "difficulty": 4, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [(r"$a^3 + a^2 + a + 1 \gt 0$ при $a \gt -1$", True), (r"$x^4 + x^3 + x + 1 = (x + 1)(x^3 + 1)$", True), (r"$x^3 - x^2 - x + 1 \ge 0$ при всіх $x$", False)],
        "solution": r"$(a + 1)(a^2 + 1)$. $x^3(x + 1) + (x + 1)$. $(x - 1)(x^2 - 1) = (x - 1)^2(x + 1)$ — від'ємне при $x \lt -1$.",
    },
    {
        "type": "SHORT", "difficulty": 5, "skill": "SOLVE",
        "text": r"Знайдіть значення $\dfrac{a^3 - a^2b + ab^2 - b^3}{a^2 + b^2}$ при $a = 2025$, $b = 2024$.",
        "answer": "1",
        "solution": r"$a^2(a - b) + b^2(a - b) = (a - b)(a^2 + b^2)$; частка $a - b = 1$.",
    },
    {
        "type": "SHORT", "difficulty": 5, "skill": "ANALYZE",
        "text": r"Скільки натуральних $n$, для яких $n^3 + 2n^2 + n + 2$ — просте число?",
        "answer": "0",
        "solution": r"$(n + 2)(n^2 + 1)$: обидва множники $\ge 2$ при натуральному $n$ ⟹ число складене завжди.",
    },
]
