TOPIC_NAME = "1.9. Обернена функція"
COURSE = "Алгебра і початки аналізу (10-11 класи)"
GRADE = "10 клас"

TASKS = [
    # ===== СХОДИНКА 1 =====
    # --- Моделювання ---
    {
        "type": "TF", "difficulty": 1, "skill": "MODEL",
        "text": r"Правда чи ні?",
        "statements": [(r"Зростаюча функція оборотна", True), (r"$y = x^2$ на $\mathbb{R}$ оборотна", False),
                       (r"Графіки взаємно обернених функцій симетричні відносно прямої $y = x$", True)],
        "hint": "Чи повторює значення $y = x^2$?",
        "solution": r"$(-1)^2 = 1^2$ — значення повторюється, тож $x^2$ на $\mathbb{R}$ необоротна.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "MODEL",
        "text": r"Точка $(2; 7)$ лежить на графіку оборотної функції $f$. Яка точка лежить на графіку оберненої функції?",
        "options": [(r"$(7; 2)$", True), (r"$(-2; -7)$", False), (r"$(2; -7)$", False), (r"$\left(\dfrac12; \dfrac17\right)$", False), (r"$(-7; 2)$", False)],
        "hint": "Координати міняються місцями.",
        "solution": r"$f(2) = 7$ ⟺ $g(7) = 2$: точка $(7; 2)$.",
    },
    {
        "type": "MATCH", "difficulty": 1, "skill": "MODEL",
        "text": r"Установіть відповідність між функцією (1–3) та оберненою до неї (А–Д).",
        "options": [r"А) $y = x - 5$", r"Б) $y = \dfrac{x}{4}$", r"В) $y = \dfrac{1}{4x}$", r"Г) $y = x^2,\; x \ge 0$", r"Д) $y = 5 - x$"],
        "matches": [(r"1. $y = 4x$", r"Б) $y = \dfrac{x}{4}$"), (r"2. $y = x + 5$", r"А) $y = x - 5$"), (r"3. $y = \sqrt{x}$", r"Г) $y = x^2,\; x \ge 0$")],
        "hint": "Обернена «скасовує» дію функції.",
        "solution": r"Множення на $4$ скасовує ділення на $4$; $+5$ — $-5$; корінь — квадрат при $x \ge 0$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "MODEL",
        "text": r"$f$ — оборотна, $f(3) = 10$. Знайдіть $g(10)$, де $g$ — обернена до $f$.",
        "answer": "3",
        "hint": "$f(a) = b$ ⟺ $g(b) = a$.",
        "solution": r"$g(10) = 3$.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "MODEL",
        "text": r"$D(f) = [0; 4]$, $E(f) = [1; 9]$, $f$ оборотна. Знайдіть область визначення оберненої функції.",
        "options": [(r"$[1; 9]$", True), (r"$[0; 4]$", False), (r"$[0; 9]$", False), (r"$[1; 4]$", False), (r"$\mathbb{R}$", False)],
        "hint": "Області міняються місцями.",
        "solution": r"$D(g) = E(f) = [1; 9]$.",
    },
    # --- Розв'язування ---
    {
        "type": "EXPR", "difficulty": 1, "skill": "SOLVE",
        "text": r"Знайдіть функцію, обернену до $y = 2x - 8$.",
        "answer": "x/2+4", "vars": ["x"],
        "hint": "Виразіть $x$ через $y$ і поміняйте позначення.",
        "solution": r"$x = \dfrac{y + 8}{2}$ ⟹ $g(x) = \dfrac{x}{2} + 4$.",
    },
    {
        "type": "EXPR", "difficulty": 1, "skill": "SOLVE",
        "text": r"Знайдіть функцію, обернену до $y = 5 - 3x$.",
        "answer": "(5-x)/3", "vars": ["x"],
        "hint": "$3x = 5 - y$.",
        "solution": r"$x = \dfrac{5 - y}{3}$ ⟹ $g(x) = \dfrac{5 - x}{3}$.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "SOLVE",
        "text": r"Знайдіть функцію, обернену до $y = x^3 + 1$.",
        "options": [(r"$y = \sqrt[3]{x - 1}$", True), (r"$y = \sqrt[3]{x} - 1$", False), (r"$y = \dfrac{1}{x^3 + 1}$", False), (r"$y = (x - 1)^3$", False), (r"$y = x^3 - 1$", False)],
        "hint": "$x^3 = y - 1$.",
        "solution": r"$x = \sqrt[3]{y - 1}$, $g(x) = \sqrt[3]{x - 1}$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"$f(x) = 4x + 1$. Знайдіть $g(9)$, де $g$ — обернена до $f$.",
        "answer": "2",
        "hint": "Розв'яжіть $4x + 1 = 9$.",
        "solution": r"$4x + 1 = 9$, $x = 2$.",
    },
    {
        "type": "EXPR", "difficulty": 1, "skill": "SOLVE",
        "text": r"Знайдіть функцію, обернену до $y = \dfrac{x}{3} + 1$.",
        "answer": "3x-3", "vars": ["x"],
        "hint": "$x = 3(y - 1)$.",
        "solution": r"$x = 3y - 3$ ⟹ $g(x) = 3x - 3$.",
    },
    # --- Аналіз ---
    {
        "type": "ERROR", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Оля шукала функцію, обернену до $y = 2x$. У якому кроці помилка?",
        "steps": [r"Обернена — це «один поділити на функцію»", r"$g(x) = \dfrac{1}{2x}$"],
        "wrong": 0,
        "hint": "Перевірте: $g(f(1))$ має дорівнювати $1$.",
        "solution": r"Обернена скасовує дію: $g(x) = \dfrac{x}{2}$. Для $\dfrac{1}{2x}$: $g(f(1)) = \dfrac14 \ne 1$.",
    },
    {
        "type": "MULTI", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Які функції оборотні?",
        "options": [(r"$y = 3x - 2$", True), (r"$y = x^3$", True), (r"$y = |x|$", False), (r"$y = x^2 + 1$", False), (r"$y = \sqrt{x}$", True)],
        "hint": "Монотонна на всій області визначення — оборотна.",
        "solution": r"$3x - 2$, $x^3$, $\sqrt{x}$ — зростають. $|x|$ і $x^2 + 1$ повторюють значення для $\pm x$.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Функція $f$ спадає. Якою є обернена функція?",
        "options": [(r"спадною", True), (r"зростаючою", False), (r"сталою", False), (r"може бути будь-якою", False), (r"не існує", False)],
        "hint": "Симетрія відносно $y = x$ зберігає характер монотонності.",
        "solution": r"Обернена має ту саму монотонність: спадає.",
    },
    {
        "type": "TF", "difficulty": 1, "skill": "ANALYZE",
        "text": r"$g$ — обернена до $f(x) = x + 7$. Правда чи ні?",
        "statements": [(r"$g(x) = x - 7$", True), (r"$g(f(5)) = 5$", True), (r"$g(0) = 7$", False)],
        "hint": "$g(0) = 0 - 7$.",
        "solution": r"$g(x) = x - 7$, $g(0) = -7$; $g(f(x)) = x$ завжди.",
    },
    {
        "type": "GROUP", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Розподіліть функції: оборотні чи ні?",
        "groups": ["оборотна", "необоротна"],
        "items": [(r"$y = -x$", 0), (r"$y = \dfrac{1}{x}$", 0), (r"$y = x^4$", 1), (r"$y = 7$", 1), (r"$y = x^2,\; x \le 0$", 0), (r"$y = (x - 1)^2$", 1)],
        "hint": "Чи є значення, яких функція набуває двічі?",
        "solution": r"$x^4$, $7$, $(x - 1)^2$ повторюють значення. $-x$, $\dfrac1x$, $x^2$ на $x \le 0$ — ні.",
    },

    # ===== СХОДИНКА 2 =====
    # --- Моделювання ---
    {
        "type": "CHOICE", "difficulty": 2, "skill": "MODEL",
        "text": r"На якому проміжку функція $y = (x - 3)^2$ оборотна?",
        "options": [(r"$[3; +\infty)$", True), (r"$\mathbb{R}$", False), (r"$[0; +\infty)$", False), (r"$[-3; +\infty)$", False), (r"$[1; 5]$", False)],
        "solution": r"Вершина при $x = 3$; на $[3; +\infty)$ функція зростає. На $[0; +\infty)$ і $[1; 5]$ є $x$ по обидва боки від $3$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "MODEL",
        "text": r"Температура в °F: $F = 1{,}8C + 32$. Виразіть $C$ через $F$ і знайдіть $C$ при $F = 77$.",
        "answer": "25",
        "solution": r"$C = \dfrac{F - 32}{1{,}8} = \dfrac{45}{1{,}8} = 25$.",
    },
    {
        "type": "EXPR", "difficulty": 2, "skill": "MODEL",
        "text": r"Знайдіть функцію, обернену до $y = x^2 + 2$, $x \ge 0$.",
        "answer": "sqrt(x-2)", "vars": ["x"],
        "solution": r"$x^2 = y - 2$, $x \ge 0$ ⟹ $x = \sqrt{y - 2}$; $g(x) = \sqrt{x - 2}$, $x \ge 2$.",
    },
    {
        "type": "MATCH", "difficulty": 2, "skill": "MODEL",
        "text": r"Функція $f$ оборотна. Установіть відповідність між властивістю $f$ (1–3) та властивістю оберненої $g$ (А–Д).",
        "options": [r"А) $D(g) = [2; 5]$", r"Б) $g$ спадає", r"В) графік $g$ проходить через $(0; 1)$", r"Г) $E(g) = [2; 5]$", r"Д) $g$ зростає"],
        "matches": [(r"1. $E(f) = [2; 5]$", r"А) $D(g) = [2; 5]$"), (r"2. $f$ спадає", r"Б) $g$ спадає"), (r"3. $f(1) = 0$", r"В) графік $g$ проходить через $(0; 1)$")],
        "solution": r"$D(g) = E(f)$; монотонність зберігається; $f(1) = 0$ ⟺ $g(0) = 1$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "MODEL",
        "text": r"Графік оборотної функції $f$ проходить через точки $(1; 4)$ і $(3; 8)$. Знайдіть $g(8) - g(4)$, де $g$ — обернена.",
        "answer": "2",
        "solution": r"$g(8) = 3$, $g(4) = 1$, різниця $2$.",
    },
    # --- Розв'язування ---
    {
        "type": "EXPR", "difficulty": 2, "skill": "SOLVE",
        "text": r"Знайдіть функцію, обернену до $y = \dfrac{1}{x - 2}$.",
        "answer": "1/x+2", "vars": ["x"],
        "solution": r"$x - 2 = \dfrac{1}{y}$, $x = \dfrac1y + 2$; $g(x) = \dfrac{1}{x} + 2$, $x \ne 0$.",
    },
    {
        "type": "EXPR", "difficulty": 2, "skill": "SOLVE",
        "text": r"Знайдіть функцію, обернену до $y = \sqrt{x + 1}$.",
        "answer": "x^2-1", "vars": ["x"],
        "solution": r"$x + 1 = y^2$, $y \ge 0$ ⟹ $g(x) = x^2 - 1$, $x \ge 0$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"$f(x) = x^3 + 2x$. Знайдіть $g(12)$, де $g$ — обернена до $f$.",
        "answer": "2",
        "solution": r"$f$ зростає; $f(2) = 8 + 4 = 12$, тож $g(12) = 2$.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "SOLVE",
        "text": r"Знайдіть функцію, обернену до $y = \dfrac{x + 1}{x}$.",
        "options": [(r"$y = \dfrac{1}{x - 1}$", True), (r"$y = \dfrac{x}{x + 1}$", False), (r"$y = x - 1$", False), (r"$y = \dfrac{1}{x} + 1$", False), (r"$y = \dfrac{x - 1}{x}$", False)],
        "solution": r"$y = 1 + \dfrac1x$ ⟹ $x = \dfrac{1}{y - 1}$. $g(x) = \dfrac{1}{x - 1}$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Розв'яжіть рівняння $x^5 + x = 34$.",
        "answer": "2",
        "solution": r"$x^5 + x$ зростає — корінь єдиний; $32 + 2 = 34$, $x = 2$.",
    },
    # --- Аналіз ---
    {
        "type": "ERROR", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Тарас шукав обернену до $f(x) = \sqrt{x}$. У якому кроці помилка?",
        "steps": [r"$y = \sqrt{x}$ ⟹ $x = y^2$", r"Міняємо позначення: $g(x) = x^2$", r"$D(g) = \mathbb{R}$"],
        "wrong": 2,
        "solution": r"$D(g) = E(f) = [0; +\infty)$: $g(x) = x^2$ лише при $x \ge 0$.",
    },
    {
        "type": "TF", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [(r"Функція $y = x$ обернена сама до себе", True), (r"Функція $y = \dfrac{1}{x}$ обернена сама до себе", True),
                       (r"Функція $y = -x + 3$ обернена сама до себе", True), (r"Функція $y = 2x$ обернена сама до себе", False)],
        "solution": r"$\dfrac1x$: $x = \dfrac1y$. $-x + 3$: $x = 3 - y$. Для $2x$ обернена — $\dfrac{x}{2}$.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Графіки $f$ і оберненої $g$ перетинаються в точці $(a; b)$, $f$ зростає. Що можна стверджувати?",
        "options": [(r"$a = b$", True), (r"$a = -b$", False), (r"$a = 0$", False), (r"$b = 0$", False), (r"нічого", False)],
        "solution": r"Для зростаючої $f$ спільні точки з $g$ лежать на $y = x$: $f(a) = a$.",
    },
    {
        "type": "MULTI", "difficulty": 2, "skill": "ANALYZE",
        "text": r"$f(x) = 2x + 1$, $g$ — обернена. Які рівності правильні?",
        "options": [(r"$g(f(3)) = 3$", True), (r"$f(g(3)) = 3$", True), (r"$g(3) = 7$", False), (r"$g(3) = 1$", True), (r"$f(3) \cdot g(3) = 1$", False)],
        "solution": r"$g(x) = \dfrac{x - 1}{2}$, $g(3) = 1$, $f(3) = 7$; $7 \cdot 1 = 7 \ne 1$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "ANALYZE",
        "text": r"$f(x) = 3x - 4$. Знайдіть абсцису точки перетину графіків $f$ і оберненої до неї функції.",
        "answer": "2",
        "solution": r"$f$ зростає, тож перетин на $y = x$: $3x - 4 = x$, $x = 2$.",
    },

    # ===== СХОДИНКА 3 =====
    # --- Моделювання ---
    {
        "type": "EXPR", "difficulty": 3, "skill": "MODEL",
        "text": r"Знайдіть функцію, обернену до $y = x^2 - 6x + 5$, $x \ge 3$.",
        "answer": "3+sqrt(x+4)", "vars": ["x"],
        "solution": r"$y = (x - 3)^2 - 4$, $x - 3 = \sqrt{y + 4}$; $g(x) = 3 + \sqrt{x + 4}$, $x \ge -4$.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "MODEL",
        "text": r"Знайдіть функцію, обернену до $y = x^2 - 6x + 5$, $x \le 3$.",
        "options": [(r"$y = 3 - \sqrt{x + 4}$", True), (r"$y = 3 + \sqrt{x + 4}$", False), (r"$y = \sqrt{x + 4} - 3$", False), (r"$y = 3 - \sqrt{x - 4}$", False), (r"оберненої немає", False)],
        "solution": r"$(x - 3)^2 = y + 4$, $x - 3 \le 0$ ⟹ $x = 3 - \sqrt{y + 4}$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"Таксі: $25$ грн посадка і $12$ грн за км. Поїздка коштувала $205$ грн. Скільки кілометрів проїхали?",
        "answer": "15",
        "solution": r"$C = 25 + 12s$ ⟹ $s = \dfrac{C - 25}{12} = \dfrac{180}{12} = 15$ км.",
    },
    {
        "type": "FIELDS", "difficulty": 3, "skill": "MODEL",
        "text": r"Функція $f(x) = ax + b$ обернена сама до себе і $f(0) = 4$. Знайдіть $a$ і $b$ ($a \ne 1$).",
        "fields": [("$a$:", "-1"), ("$b$:", "4")],
        "solution": r"$b = 4$. Обернена: $\dfrac{x - 4}{a}$; $\dfrac{x - 4}{a} = ax + 4$ для всіх $x$ ⟹ $a^2 = 1$, $a = -1$ (при $a = 1$: $x - 4 \ne x + 4$).",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"Графік оберненої до $f(x) = kx + 3$ функції проходить через точку $(11; 4)$. Знайдіть $k$.",
        "answer": "2",
        "solution": r"$g(11) = 4$ ⟺ $f(4) = 11$: $4k + 3 = 11$, $k = 2$.",
    },
    # --- Розв'язування ---
    {
        "type": "EXPR", "difficulty": 3, "skill": "SOLVE",
        "text": r"Знайдіть функцію, обернену до $y = \dfrac{3x - 1}{x + 2}$.",
        "answer": "(2x+1)/(3-x)", "vars": ["x"],
        "solution": r"$xy + 2y = 3x - 1$, $x(y - 3) = -1 - 2y$, $x = \dfrac{2y + 1}{3 - y}$; $g(x) = \dfrac{2x + 1}{3 - x}$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Розв'яжіть рівняння $x^3 + 3x - 4 = 0$.",
        "answer": "1",
        "solution": r"$x^3 + 3x$ зростає — корінь єдиний; $1 + 3 - 4 = 0$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Розв'яжіть рівняння $\sqrt{x - 1} + x = 7$.",
        "answer": "5",
        "solution": r"Ліва частина зростає — корінь єдиний. $\sqrt4 + 5 = 7$, $x = 5$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"$f(x) = \dfrac{x + 5}{x - 1}$, $g$ — обернена. Знайдіть $g(3)$.",
        "answer": "4",
        "solution": r"$\dfrac{x + 5}{x - 1} = 3$: $x + 5 = 3x - 3$, $x = 4$.",
    },
    {
        "type": "FIELDS", "difficulty": 3, "skill": "SOLVE",
        "text": r"$f(x) = x^2 + 4x$, $x \ge -2$. Знайдіть область визначення оберненої функції $D(g) = [m; +\infty)$ і $g(5)$.",
        "fields": [("$m$:", "-4"), ("$g(5)$:", "1")],
        "solution": r"$f = (x + 2)^2 - 4$, $E(f) = [-4; +\infty)$. $x^2 + 4x = 5$, $x = 1$ (корінь $-5 \lt -2$ не підходить).",
    },
    # --- Аналіз ---
    {
        "type": "TF", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [(r"Немонотонна функція може бути оборотною", True), (r"Періодична функція не може бути оборотною", True),
                       (r"Парна функція з $D(f) = \mathbb{R}$ необоротна", True), (r"Непарна функція завжди оборотна", False)],
        "solution": r"$\dfrac1x$ оборотна, але не монотонна на всій області. Періодична повторює значення. Парна: $f(-1) = f(1)$. $x^3 - x$ непарна, але $f(0) = f(1) = 0$.",
    },
    {
        "type": "ERROR", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Оля шукала обернену до $y = x^2 - 2x$, $x \le 1$. У якому кроці помилка?",
        "steps": [r"$y = (x - 1)^2 - 1$", r"$(x - 1)^2 = y + 1$", r"$x = 1 + \sqrt{y + 1}$", r"$g(x) = 1 + \sqrt{x + 1}$"],
        "wrong": 2,
        "solution": r"При $x \le 1$: $x - 1 \le 0$, тож $x = 1 - \sqrt{y + 1}$; $g(x) = 1 - \sqrt{x + 1}$.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Скільки розв'язків має рівняння $f(x) = g(x)$, де $f(x) = x^3$, $g$ — обернена до $f$?",
        "options": [(r"$3$", True), (r"$1$", False), (r"$2$", False), (r"$0$", False), (r"безліч", False)],
        "solution": r"$f$ зростає — розв'язки на $y = x$: $x^3 = x$, $x \in \{-1; 0; 1\}$.",
    },
    {
        "type": "MULTI", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Які функції обернені самі до себе?",
        "options": [(r"$y = \dfrac{4}{x}$", True), (r"$y = 6 - x$", True), (r"$y = \dfrac{x + 1}{x - 1}$", True), (r"$y = x^3$", False), (r"$y = \dfrac{x}{2}$", False)],
        "solution": r"$x = \dfrac4y$; $x = 6 - y$; $\dfrac{x + 1}{x - 1}$: $xy - y = x + 1$, $x = \dfrac{y + 1}{y - 1}$. Для $x^3$ обернена — $\sqrt[3]{x}$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "ANALYZE",
        "text": r"$f(x) = \dfrac{ax + 2}{x - 3}$ обернена сама до себе. Знайдіть $a$.",
        "answer": "3",
        "solution": r"Обернена до $\dfrac{ax + b}{cx + d}$ — $\dfrac{dx - b}{-cx + a}$; збіг при $d = -a$: $-3 = -a$, $a = 3$. Перевірка: $\dfrac{3x + 2}{x - 3}$ — $x = \dfrac{3y + 2}{y - 3}$ ✓.",
    },

    # ===== БОСИ =====
    {
        "type": "SHORT", "difficulty": 4, "skill": "MODEL",
        "text": r"$f(x) = x^3 + x + 1$, $g$ — обернена. Знайдіть $g(11) + g(3) + g(1)$.",
        "answer": "3",
        "solution": r"$f(2) = 11$, $f(1) = 3$, $f(0) = 1$ — сума $2 + 1 + 0 = 3$.",
    },
    {
        "type": "EXPR", "difficulty": 4, "skill": "MODEL",
        "text": r"Знайдіть функцію, обернену до $y = 2 - \sqrt{4 - x}$.",
        "answer": "4-(2-x)^2", "vars": ["x"],
        "solution": r"$\sqrt{4 - x} = 2 - y$ ($y \le 2$), $x = 4 - (2 - y)^2$. $g(x) = 4 - (2 - x)^2$, $x \le 2$.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "SOLVE",
        "text": r"Розв'яжіть рівняння $\sqrt{x + 3} = x - 3$ — знайдіть корінь.",
        "answer": "6",
        "solution": r"$x \ge 3$: $x + 3 = x^2 - 6x + 9$, $x^2 - 7x + 6 = 0$, $x = 6$ або $x = 1$ (не підходить, $1 \lt 3$).",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "SOLVE",
        "text": r"Розв'яжіть рівняння $(x - 1)^3 + 2x = 14$.",
        "answer": "3",
        "solution": r"Ліва частина — сума зростаючих функцій, тож корінь єдиний. Підбором: $(3 - 1)^3 + 6 = 14$, $x = 3$.",
    },
    {
        "type": "TF", "difficulty": 4, "skill": "ANALYZE",
        "text": r"$f$ зростає на $\mathbb{R}$, $g$ — обернена. Правда чи ні?",
        "statements": [(r"Рівняння $f(x) = g(x)$ рівносильне $f(x) = x$", True), (r"$f(f(x)) = x$ ⟺ $f(x) = x$", True), (r"Графіки $f$ і $g$ не можуть перетинатися", False)],
        "solution": r"Для зростаючої $f$: якщо $f(x) \gt x$, то $f(f(x)) \gt f(x) \gt x$; аналогічно для $\lt$. Отже, $f(f(x)) = x$ лише при $f(x) = x$. $f(x) = x$ — перетин є.",
    },
    {
        "type": "SHORT", "difficulty": 5, "skill": "SOLVE",
        "text": r"Розв'яжіть рівняння $x = \sqrt{2 + \sqrt{2 + x}}$ — знайдіть корінь.",
        "answer": "2",
        "solution": r"$f(t) = \sqrt{2 + t}$ зростає, рівняння: $f(f(x)) = x$ ⟺ $f(x) = x$: $\sqrt{2 + x} = x$, $x^2 - x - 2 = 0$, $x = 2$ ($x \ge 0$).",
    },
    {
        "type": "SHORT", "difficulty": 5, "skill": "ANALYZE",
        "text": r"Розв'яжіть рівняння $x^3 + 1 = 2\sqrt[3]{2x - 1}$ — знайдіть найбільший корінь.",
        "answer": "1",
        "solution": r"$f(x) = \dfrac{x^3 + 1}{2}$ і $g(x) = \sqrt[3]{2x - 1}$ — взаємно обернені, $f$ зростає. Рівняння $f(x) = g(x)$ ⟺ $f(x) = x$: $x^3 - 2x + 1 = 0$, $(x - 1)(x^2 + x - 1) = 0$: $x = 1$, $x = \dfrac{-1 \pm \sqrt5}{2}$. Найбільший — $1$ ($\dfrac{-1 + \sqrt5}{2} \approx 0{,}62$).",
    },
]
