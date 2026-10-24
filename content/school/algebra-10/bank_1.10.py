TOPIC_NAME = "1.10. Метод інтервалів"
COURSE = "Алгебра і початки аналізу (10-11 класи)"
GRADE = "10 клас"

TASKS = [
    # ===== СХОДИНКА 1 =====
    # --- Моделювання ---
    {
        "type": "ORDER", "difficulty": 1, "skill": "MODEL",
        "text": r"Упорядкуйте кроки методу інтервалів.",
        "items": [r"Перенести все в ліву частину", r"Розкласти на множники", r"Знайти нулі та точки, де вираз не визначений", r"Визначити знаки на інтервалах", r"Записати відповідь"],
        "hint": "Спершу — вигляд $f(x) \\vee 0$.",
        "solution": r"Вигляд $f(x) \vee 0$ → множники → точки → знаки → відповідь.",
    },
    {
        "type": "TF", "difficulty": 1, "skill": "MODEL",
        "text": r"Правда чи ні?",
        "statements": [(r"На інтервалі між сусідніми нулями знак $(x - 1)(x - 3)$ не змінюється", True), (r"Нуль знаменника в нестрогій нерівності зафарбовуємо", False), (r"Знак $(x - 2)^2$ при переході через $2$ не змінюється", True)],
        "hint": "На нуль ділити не можна.",
        "solution": r"Нулі знаменника завжди виколоті.",
    },
    {
        "type": "FIELDS", "difficulty": 1, "skill": "MODEL",
        "text": r"Знайдіть точки, які позначаємо на прямій для нерівності $(x - 7)(x + 4) \ge 0$ (менша, більша).",
        "fields": [("Менша:", "-4"), ("Більша:", "7")],
        "hint": "Нулі множників.",
        "solution": r"$x - 7 = 0$, $x + 4 = 0$: $-4$ і $7$.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "MODEL",
        "text": r"Які знаки має $(x - 1)(x - 5)$ на інтервалах $(-\infty; 1)$, $(1; 5)$, $(5; +\infty)$?",
        "options": [(r"$+, -, +$", True), (r"$-, +, -$", False), (r"$+, +, -$", False), (r"$-, -, +$", False)],
        "hint": "Пробна точка $x = 0$.",
        "solution": r"$x = 0$: $5 \gt 0$; $x = 2$: $-3$; $x = 6$: $5$.",
    },
    {
        "type": "GROUP", "difficulty": 1, "skill": "MODEL",
        "text": r"Нерівність $\dfrac{(x - 1)(x + 2)}{x - 3} \ge 0$. Як позначити точки?",
        "groups": ["зафарбована", "виколота"],
        "items": [(r"$x = 1$", 0), (r"$x = -2$", 0), (r"$x = 3$", 1)],
        "hint": "Знаменник не може бути нулем.",
        "solution": r"Нулі чисельника — зафарбовані (нестрога), нуль знаменника — виколотий.",
    },
    # --- Розв'язування ---
    {
        "type": "CHOICE", "difficulty": 1, "skill": "SOLVE",
        "text": r"Розв'яжіть: $(x - 2)(x + 3) \gt 0$.",
        "options": [(r"$(-\infty; -3) \cup (2; +\infty)$", True), (r"$(-3; 2)$", False), (r"$(-\infty; -2) \cup (3; +\infty)$", False), (r"$[-3; 2]$", False)],
        "hint": "Знаки $+, -, +$.",
        "solution": r"Крайні інтервали: $(-\infty; -3) \cup (2; +\infty)$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"Скільки цілих розв'язків має нерівність $(x - 1)(x - 6) \lt 0$?",
        "answer": "4",
        "hint": "Розв'язок — $(1; 6)$.",
        "solution": r"$2, 3, 4, 5$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"Знайдіть найменший цілий розв'язок нерівності $\dfrac{x - 3}{x + 1} \ge 0$, що більший за $-1$.",
        "answer": "3",
        "hint": "Розв'язки: $(-\\infty; -1) \\cup [3; +\\infty)$.",
        "solution": r"Праворуч від $-1$ розв'язки — $[3; +\infty)$; найменший цілий $3$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"Скільки цілих розв'язків має $x(x - 4) \le 0$?",
        "answer": "5",
        "hint": "$[0; 4]$.",
        "solution": r"$0, 1, 2, 3, 4$.",
    },
    {
        "type": "MULTI", "difficulty": 1, "skill": "SOLVE",
        "text": r"Які числа є розв'язками $(x + 2)(x - 3) \le 0$?",
        "options": [(r"$-2$", True), (r"$0$", True), (r"$3$", True), (r"$4$", False), (r"$-3$", False)],
        "hint": "Розв'язок — $[-2; 3]$.",
        "solution": r"$[-2; 3]$ містить $-2$, $0$, $3$.",
    },
    # --- Аналіз ---
    {
        "type": "ERROR", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Оля розв'язувала $\dfrac{x + 1}{x - 2} \le 0$. У якому кроці помилка?",
        "steps": [r"Точки $-1$ і $2$", r"Знаки: $+, -, +$", r"Відповідь: $[-1; 2]$"],
        "wrong": 2,
        "hint": "Чи може знаменник дорівнювати нулю?",
        "solution": r"$x = 2$ — виколота: $[-1; 2)$.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Тарас: «$\dfrac{1}{x} \gt 1$ ⟺ $1 \gt x$». Чи правий він?",
        "options": [(r"Ні: множити на $x$ можна лише при $x \gt 0$", True), (r"Так", False), (r"Ні: треба $x \gt 1$", False), (r"Так, бо $x \ne 0$", False)],
        "hint": "Перевірте $x = -1$.",
        "solution": r"$x = -1$: $1 \gt -1$, але $\dfrac{1}{-1} = -1 \lt 1$. Правильна відповідь $(0; 1)$.",
    },
    {
        "type": "TF", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Для $(x - 3)^2 \gt 0$ правда чи ні?",
        "statements": [(r"Розв'язки — усі $x$, крім $3$", True), (r"$x = 3$ — розв'язок", False), (r"Нерівність не має розв'язків", False)],
        "hint": "Квадрат додатний, якщо основа $\\ne 0$.",
        "solution": r"$(x - 3)^2 \gt 0$ ⟺ $x \ne 3$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Скільки розв'язків має нерівність $(x + 1)^2 \le 0$?",
        "answer": "1",
        "hint": "Квадрат не буває від'ємним.",
        "solution": r"Лише $x = -1$.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Нерівність $(2 - x)(x + 5) \gt 0$ рівносильна нерівності…",
        "options": [(r"$(x - 2)(x + 5) \lt 0$", True), (r"$(x - 2)(x + 5) \gt 0$", False), (r"$(x + 2)(x + 5) \gt 0$", False), (r"$(x - 2)(x - 5) \gt 0$", False)],
        "hint": "$2 - x = -(x - 2)$.",
        "solution": r"Винесли $-1$ — знак нерівності змінився.",
    },

    # ===== СХОДИНКА 2 =====
    # --- Моделювання ---
    {
        "type": "FIELDS", "difficulty": 2, "skill": "MODEL",
        "text": r"Розв'язок нерівності $\dfrac{x - 5}{x + 3} \lt 0$ — інтервал $(a; b)$. Знайдіть $a$ і $b$.",
        "fields": [("$a$:", "-3"), ("$b$:", "5")],
        "solution": r"Знаки $+, -, +$; «$\lt 0$» — $(-3; 5)$.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "MODEL",
        "text": r"Знайдіть область визначення функції $y = \sqrt{\dfrac{x + 2}{4 - x}}$.",
        "options": [(r"$[-2; 4)$", True), (r"$[-2; 4]$", False), (r"$(-\infty; -2] \cup (4; +\infty)$", False), (r"$(-2; 4)$", False), (r"$\mathbb{R}$", False)],
        "solution": r"$\dfrac{x + 2}{4 - x} \ge 0$ ⟺ $\dfrac{x + 2}{x - 4} \le 0$: $[-2; 4)$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "MODEL",
        "text": r"При яких значеннях $x$ вираз $\dfrac{x^2 - 9}{x}$ від'ємний? Знайдіть кількість цілих таких $x$ на відрізку $[-5; 5]$.",
        "answer": "4",
        "solution": r"$\dfrac{(x - 3)(x + 3)}{x} \lt 0$: знаки $-, +, -, +$ на $(-\infty; -3)$, $(-3; 0)$, $(0; 3)$, $(3; \infty)$. На $[-5; 5]$: $-5, -4, 1, 2$ — $4$ числа.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "MODEL",
        "text": r"Знайдіть суму цілих розв'язків нерівності $(x + 2)(x - 4) \le 0$.",
        "answer": "7",
        "solution": r"$[-2; 4]$: $-2 - 1 + 0 + 1 + 2 + 3 + 4 = 7$.",
    },
    {
        "type": "MATCH", "difficulty": 2, "skill": "MODEL",
        "text": r"Установіть відповідність між нерівністю (1–3) та множиною розв'язків (А–Д).",
        "options": [r"А) $(-1; 2)$", r"Б) $(-\infty; -1) \cup (2; +\infty)$", r"В) $[-1; 2)$", r"Г) $(-1; 2]$", r"Д) $\varnothing$"],
        "matches": [(r"1. $(x + 1)(x - 2) \lt 0$", r"А) $(-1; 2)$"), (r"2. $\dfrac{x + 1}{x - 2} \le 0$", r"В) $[-1; 2)$"), (r"3. $\dfrac{x - 2}{x + 1} \le 0$", r"Г) $(-1; 2]$")],
        "solution": r"Нулі знаменника виколоті; нулі чисельника при «$\le$» зафарбовані.",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Скільки цілих розв'язків має $x(x - 3)(x + 2) \lt 0$ на відрізку $[-5; 5]$?",
        "answer": "5",
        "solution": r"Знаки (справа): $+$ на $(3; \infty)$, $-$ на $(0; 3)$, $+$ на $(-2; 0)$, $-$ на $(-\infty; -2)$. Цілі: $-5, -4, -3, 1, 2$.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "SOLVE",
        "text": r"Розв'яжіть: $\dfrac{x^2 - 4}{x + 5} \ge 0$.",
        "options": [(r"$(-5; -2] \cup [2; +\infty)$", True), (r"$[-5; -2] \cup [2; +\infty)$", False), (r"$(-\infty; -5) \cup [-2; 2]$", False), (r"$[-2; 2]$", False), (r"$[2; +\infty)$", False)],
        "solution": r"Точки $-5$ (виколота), $-2$, $2$. Знаки справа: $+, -, +, -$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Знайдіть найбільший цілий розв'язок нерівності $\dfrac{3x - 12}{x + 1} \lt 0$.",
        "answer": "3",
        "solution": r"$(-1; 4)$; найбільший цілий $3$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Скільки цілих розв'язків має $\dfrac{x + 4}{x - 1} \le 2$ на відрізку $[-10; 10]$?",
        "answer": "11",
        "solution": r"$\dfrac{x + 4 - 2x + 2}{x - 1} = \dfrac{6 - x}{x - 1} \le 0$ ⟺ $\dfrac{x - 6}{x - 1} \ge 0$: $(-\infty; 1) \cup [6; +\infty)$. На $[-10; 10]$: $-10..0$ — $11$ чисел і $6..10$ — $5$. Разом $16$?",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Знайдіть довжину проміжку розв'язків нерівності $(x + 3)(x - 5) \le 0$.",
        "answer": "8",
        "solution": r"$[-3; 5]$, довжина $8$.",
    },
    # --- Аналіз ---
    {
        "type": "ERROR", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Тарас розв'язував $(x - 1)^2(x - 4) \lt 0$. У якому кроці помилка?",
        "steps": [r"Точки $1$ і $4$, обидві виколоті", r"Знаки справа наліво: $+, -, +$", r"Відповідь: $(1; 4)$"],
        "wrong": 1,
        "solution": r"Через $x = 1$ (квадрат) знак не змінюється: $+, -, -$. Відповідь $(-\infty; 1) \cup (1; 4)$.",
    },
    {
        "type": "TF", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [(r"$\dfrac{x - 2}{x + 1} \ge 0$ і $(x - 2)(x + 1) \ge 0$ мають однакові розв'язки", False), (r"$\dfrac{x - 2}{x + 1} \gt 0$ і $(x - 2)(x + 1) \gt 0$ мають однакові розв'язки", True), (r"$x^2 + 1 \gt 0$ для всіх $x$", True)],
        "solution": r"У нестрогій нерівності $x = -1$ входить у другу, але не в першу. Для строгих — однаково.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Нерівність $\dfrac{x^2 + 4}{x - 3} \lt 0$ рівносильна…",
        "options": [(r"$x \lt 3$", True), (r"$x \gt 3$", False), (r"$x \ne 3$", False), (r"$-2 \lt x \lt 2$", False), (r"не має розв'язків", False)],
        "solution": r"$x^2 + 4 \gt 0$ завжди, тож знак — від знаменника: $x - 3 \lt 0$.",
    },
    {
        "type": "MULTI", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Які числа є розв'язками $\dfrac{(x - 2)^2}{x + 3} \le 0$?",
        "options": [(r"$2$", True), (r"$-4$", True), (r"$-3$", False), (r"$0$", False), (r"$-10$", True)],
        "solution": r"Розв'язки: $(-\infty; -3) \cup \{2\}$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Скільки цілих чисел НЕ є розв'язками нерівності $(x + 2)(x - 3) \gt 0$?",
        "answer": "6",
        "solution": r"Не розв'язки: $[-2; 3]$ — $-2, -1, 0, 1, 2, 3$.",
    },

    # ===== СХОДИНКА 3 =====
    # --- Моделювання ---
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"Знайдіть кількість цілих $x$ з області визначення $y = \sqrt{\dfrac{9 - x^2}{x + 1}}$.",
        "answer": "5",
        "solution": r"$\dfrac{(3 - x)(3 + x)}{x + 1} \ge 0$ ⟺ $\dfrac{(x - 3)(x + 3)}{x + 1} \le 0$: $(-\infty; -3] \cup (-1; 3]$. Цілих на $(-1; 3]$: $0, 1, 2, 3$ — і нескінченно багато зліва! Обмежимося $x \ge -3$: $-3, 0, 1, 2, 3$ — $5$.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "MODEL",
        "text": r"При яких $x$ значення функції $f(x) = \dfrac{2x - 1}{x + 2}$ не менші за $1$?",
        "options": [(r"$(-\infty; -2) \cup [3; +\infty)$", True), (r"$[3; +\infty)$", False), (r"$(-2; 3]$", False), (r"$(-\infty; -2] \cup [3; +\infty)$", False), (r"$(-\infty; 3]$", False)],
        "solution": r"$\dfrac{2x - 1 - x - 2}{x + 2} = \dfrac{x - 3}{x + 2} \ge 0$.",
    },
    {
        "type": "FIELDS", "difficulty": 3, "skill": "MODEL",
        "text": r"Розв'язок $\dfrac{x^2 - 5x + 6}{x - 1} \le 0$: $(-\infty; a) \cup [b; c]$. Знайдіть $a$, $b$, $c$.",
        "fields": [("$a$:", "1"), ("$b$:", "2"), ("$c$:", "3")],
        "solution": r"$\dfrac{(x - 2)(x - 3)}{x - 1} \le 0$: знаки справа $+, -, +, -$; «$\le$»: $(-\infty; 1) \cup [2; 3]$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"Знайдіть суму цілих розв'язків нерівності $\dfrac{(x + 1)^2(x - 5)}{x - 1} \le 0$.",
        "answer": "13",
        "solution": r"Точки $-1$ (квадрат), $1$ (виколота), $5$. Знаки: $(5; \infty)$ $+$, $(1; 5)$ $-$, $(-1; 1)$ $+$, лівіше $+$. Розв'язки: $\{-1\} \cup (1; 5]$. Цілі: $-1, 2, 3, 4, 5$, сума $13$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"Сума довжин проміжків, що утворюють розв'язок $(x + 4)(x + 1)(x - 2)(x - 3) \lt 0$.",
        "answer": "4",
        "solution": r"Знаки справа: $+, -, +, -, +$. Розв'язки: $(-4; -1) \cup (2; 3)$: довжини $3 + 1 = 4$.",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Знайдіть кількість цілих розв'язків нерівності $\dfrac{x^2 - 16}{x^2 - 2x} \le 0$.",
        "answer": "5",
        "solution": r"$\dfrac{(x - 4)(x + 4)}{x(x - 2)} \le 0$: точки $-4, 0, 2, 4$. Знаки справа $+, -, +, -, +$. Розв'язки $[-4; 0) \cup (2; 4]$: $-4, -3, -2, -1, 3, 4$ — $6$?",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "SOLVE",
        "text": r"Розв'яжіть: $\dfrac{1}{x - 1} \gt \dfrac{1}{x + 1}$.",
        "options": [(r"$(-\infty; -1) \cup (1; +\infty)$", True), (r"$(-1; 1)$", False), (r"$\mathbb{R}$", False), (r"$(1; +\infty)$", False), (r"$\varnothing$", False)],
        "solution": r"$\dfrac{(x + 1) - (x - 1)}{(x - 1)(x + 1)} = \dfrac{2}{(x - 1)(x + 1)} \gt 0$ ⟺ $(x - 1)(x + 1) \gt 0$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Знайдіть найменший натуральний розв'язок нерівності $\dfrac{x - 10}{x - 3} \gt 2$.",
        "answer": "4",
        "solution": r"$\dfrac{x - 10 - 2x + 6}{x - 3} = \dfrac{-x - 4}{x - 3} \gt 0$ ⟺ $\dfrac{x + 4}{x - 3} \lt 0$: $(-4; 3)$. Натуральні: $1, 2$ — найменший $1$?",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Скільки цілих розв'язків має $(x^2 - 1)(x^2 - 9) \le 0$?",
        "answer": "6",
        "solution": r"Точки $\pm1$, $\pm3$; знаки справа $+, -, +, -, +$. Розв'язки $[-3; -1] \cup [1; 3]$: $-3, -2, -1, 1, 2, 3$.",
    },
    {
        "type": "FIELDS", "difficulty": 3, "skill": "SOLVE",
        "text": r"Розв'язок $\dfrac{x(x - 4)}{(x - 2)^2} \le 0$: $[a; 2) \cup (2; b]$. Знайдіть $a$ і $b$.",
        "fields": [("$a$:", "0"), ("$b$:", "4")],
        "solution": r"$(x - 2)^2 \gt 0$ при $x \ne 2$, тож знак — від $x(x - 4)$: $[0; 4]$, без $2$.",
    },
    # --- Аналіз ---
    {
        "type": "TF", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [(r"$\dfrac{f(x)}{g(x)} \ge 0$ ⟺ $f(x)g(x) \ge 0$ і $g(x) \ne 0$", True), (r"Метод інтервалів годиться для $\dfrac{x^2 + 1}{x} \gt 0$", True), (r"$(x - a)^{2}(x - b) \ge 0$ завжди має розв'язок $x = a$", True), (r"Якщо нерівність строга, то кінці проміжків завжди зафарбовані", False)],
        "solution": r"Добуток і частка мають однаковий знак. Строга нерівність — кінці виколоті.",
    },
    {
        "type": "ERROR", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Оля розв'язувала $\dfrac{x + 2}{x - 3} \ge 1$. У якому кроці помилка?",
        "steps": [r"Помножимо на $x - 3$: $x + 2 \ge x - 3$", r"$2 \ge -3$ — правильно завжди", r"Відповідь: $x \ne 3$"],
        "wrong": 0,
        "solution": r"Множити на $x - 3$ не можна. $\dfrac{5}{x - 3} \ge 0$ ⟺ $x \gt 3$.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "ANALYZE",
        "text": r"При якому $a$ нерівність $(x - a)(x - 2) \le 0$ має рівно один розв'язок?",
        "options": [(r"$a = 2$", True), (r"$a = 0$", False), (r"$a = -2$", False), (r"при будь-якому", False), (r"такого $a$ немає", False)],
        "solution": r"$(x - 2)^2 \le 0$ ⟺ $x = 2$. Інакше — відрізок між $a$ і $2$.",
    },
    {
        "type": "MULTI", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Які нерівності мають розв'язок $(-\infty; -1) \cup (3; +\infty)$?",
        "options": [(r"$(x + 1)(x - 3) \gt 0$", True), (r"$\dfrac{x - 3}{x + 1} \gt 0$", True), (r"$(x + 1)(3 - x) \lt 0$", True), (r"$\dfrac{x + 1}{x - 3} \ge 0$", False)],
        "solution": r"Остання включає $x = -1$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Скільки цілих $x$ задовольняють $\dfrac{x^2}{x - 2} \le 0$ і $x \ge -3$?",
        "answer": "5",
        "solution": r"$(-\infty; 2)$, бо $x^2 \ge 0$ (і $x = 0$ — розв'язок). Цілі від $-3$ до $1$: $5$.",
    },

    # ===== БОСИ =====
    {
        "type": "SHORT", "difficulty": 4, "skill": "MODEL",
        "text": r"Знайдіть кількість цілих розв'язків системи $\begin{cases} (x - 1)(x - 7) \lt 0 \\ \dfrac{x - 4}{x - 2} \ge 0 \end{cases}$.",
        "answer": "3",
        "solution": r"Перша: $(1; 7)$. Друга: $(-\infty; 2) \cup [4; \infty)$. Перетин: $(1; 2) \cup [4; 7)$: цілі $4, 5, 6$.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "MODEL",
        "text": r"Знайдіть суму цілих $x$ з відрізка $[-5; 5]$, для яких $\dfrac{x^3 - x}{x + 3} \ge 0$.",
        "answer": "11",
        "solution": r"$\dfrac{x(x - 1)(x + 1)}{x + 3} \ge 0$; точки $-3$ (вик.), $-1, 0, 1$. Знаки справа: $+, -, +, -, +$. Розв'язки: $(-\infty; -3) \cup [-1; 0] \cup [1; \infty)$. Цілі на $[-5; 5]$: $-5, -4, -1, 0, 1, 2, 3, 4, 5$; сума $5$.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "SOLVE",
        "text": r"Скільки цілих розв'язків має нерівність $\dfrac{(x - 3)^2(x + 2)}{(x - 5)(x + 4)} \le 0$ на відрізку $[-6; 6]$?",
        "answer": "8",
        "solution": r"Точки: $-4$ (вик.), $-2$, $3$ (квадрат), $5$ (вик.). Знаки справа: $+$ $(5; \infty)$, $-$ $(3; 5)$, $-$ $(-2; 3)$, $+$ $(-4; -2)$, $-$ $(-\infty; -4)$. Розв'язки: $(-\infty; -4) \cup [-2; 5)$. Цілі на $[-6; 6]$: $-6, -5, -2, -1, 0, 1, 2, 3, 4$ — $9$?",
    },
    {
        "type": "CHOICE", "difficulty": 4, "skill": "SOLVE",
        "text": r"Розв'яжіть: $\dfrac{2}{x} \le x - 1$.",
        "options": [(r"$[-1; 0) \cup [2; +\infty)$", True), (r"$[2; +\infty)$", False), (r"$(-\infty; -1] \cup (0; 2]$", False), (r"$[-1; 2]$", False), (r"$(0; 2]$", False)],
        "solution": r"$\dfrac{x^2 - x - 2}{x} \ge 0$ ⟺ $\dfrac{(x - 2)(x + 1)}{x} \ge 0$: знаки справа $+, -, +, -$: $[-1; 0) \cup [2; \infty)$.",
    },
    {
        "type": "TF", "difficulty": 4, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [(r"$\dfrac{x - 1}{x - 1} \ge 1$ має розв'язок $x \ne 1$", True), (r"$x^4 - x^2 \lt 0$ ⟺ $0 \lt |x| \lt 1$", True), (r"$\dfrac{1}{x^2} \gt 0$ для всіх $x$", False)],
        "solution": r"$1 \ge 1$ при $x \ne 1$. $x^2(x^2 - 1) \lt 0$ ⟺ $x \ne 0$, $x^2 \lt 1$. $\dfrac{1}{x^2}$ не визначено при $x = 0$.",
    },
    {
        "type": "SHORT", "difficulty": 5, "skill": "SOLVE",
        "text": r"При яких цілих $a$ нерівність $\dfrac{x - a}{x - 2} \le 0$ має рівно $3$ цілі розв'язки? Укажіть суму таких $a$.",
        "answer": "4",
        "solution": r"Якщо $a \gt 2$: $(2; a]$ — цілі $3, \ldots, a$: $a - 2 = 3$, $a = 5$. Якщо $a \lt 2$: $[a; 2)$ — цілі $a, \ldots, 1$: $2 - a = 3$, $a = -1$. Сума $4$.",
    },
    {
        "type": "SHORT", "difficulty": 5, "skill": "ANALYZE",
        "text": r"Знайдіть кількість цілих розв'язків нерівності $\dfrac{(x^2 - 4)(x - 6)^2}{x^2 - 25} \le 0$.",
        "answer": "7",
        "solution": r"Точки $\pm 5$ (вик.), $\pm 2$, $6$ (квадрат). Знаки справа: $+$ $(6;\infty)$, $+$ $(5; 6)$, $-$ $(2; 5)$, $+$ $(-2; 2)$, $-$ $(-5; -2)$, $+$ $(-\infty; -5)$. Розв'язки: $(-5; -2] \cup [2; 5) \cup \{6\}$. Цілі: $-4, -3, -2, 2, 3, 4, 6$ — $7$.",
    },
]
