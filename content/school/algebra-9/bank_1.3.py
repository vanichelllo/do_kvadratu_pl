TOPIC_NAME = "1.3. Системи лінійних нерівностей"
COURSE = "Алгебра (7-9 класи)"
GRADE = "9 клас"

TASKS = [
    # ==========================================
    # СХОДИНКА 1 — БАЗОВИЙ
    # ==========================================
    # --- Моделювання ---
    {
        "type": "CHOICE", "difficulty": 1, "skill": "MODEL",
        "text": r"Яка система описує умову «число $x$ більше за $2$ і не більше за $7$»?",
        "options": [(r"$\begin{cases} x \gt 2, \\ x \le 7 \end{cases}$", True), (r"$\begin{cases} x \ge 2, \\ x \lt 7 \end{cases}$", False),
                    (r"$\begin{cases} x \gt 2, \\ x \ge 7 \end{cases}$", False), (r"$\begin{cases} x \lt 2, \\ x \le 7 \end{cases}$", False)],
        "hint": r"«Не більше» — це «менше або дорівнює».",
        "solution": r"«Більше за $2$» — $x \gt 2$; «не більше за $7$» — $x \le 7$. Обидві умови разом — система.",
    },
    {
        "type": "MATCH", "difficulty": 1, "skill": "MODEL",
        "text": r"Установіть відповідність між подвійною нерівністю (1–3) та проміжком (А–Д).",
        "options": [r"А) $(-1;\,3]$", r"Б) $[-1;\,3)$", r"В) $(-1;\,3)$", r"Г) $[-1;\,3]$", r"Д) $(-\infty;\,3]$"],
        "matches": [(r"1. $-1 \lt x \le 3$", r"А) $(-1;\,3]$"), (r"2. $-1 \le x \lt 3$", r"Б) $[-1;\,3)$"),
                    (r"3. $-1 \lt x \lt 3$", r"В) $(-1;\,3)$")],
        "hint": r"Нестрогий знак — квадратна дужка, строгий — кругла.",
        "solution": r"Кінець входить у проміжок, лише якщо знак нестрогий: 1 — А, 2 — Б, 3 — В.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "MODEL",
        "text": r"Знайдіть переріз проміжків $(1;\,+\infty) \cap (-\infty;\,5]$.",
        "options": [(r"$(1;\,5]$", True), (r"$[1;\,5]$", False), (r"$(1;\,+\infty)$", False), (r"$(-\infty;\,5]$", False), (r"$(-\infty;\,+\infty)$", False)],
        "hint": r"Переріз — спільна частина обох проміжків.",
        "solution": r"Спільні точки — більші за $1$ і не більші за $5$: $(1;\,5]$.",
    },
    {
        "type": "FIELDS", "difficulty": 1, "skill": "MODEL",
        "text": r"Периметр квадрата зі стороною $x$ см більший за $12$ см, але менший за $20$ см. Запишіть розв'язок у вигляді $a \lt x \lt b$.",
        "fields": [("$a =$", "3"), ("$b =$", "5")],
        "hint": r"Периметр квадрата — $4x$: $\;12 \lt 4x \lt 20$.",
        "solution": r"$12 \lt 4x \lt 20$; ділимо всі частини на $4$: $3 \lt x \lt 5$.",
    },
    {
        "type": "TF", "difficulty": 1, "skill": "MODEL",
        "text": r"Правда чи ні?",
        "statements": [
            (r"Число $3$ — розв'язок системи $\begin{cases} x \gt 1, \\ x \lt 4 \end{cases}$", True),
            (r"Число $4$ — розв'язок системи $\begin{cases} x \gt 1, \\ x \lt 4 \end{cases}$", False),
            (r"Число $1$ — розв'язок системи $\begin{cases} x \ge 1, \\ x \le 5 \end{cases}$", True),
        ],
        "hint": r"Число має задовольняти кожну нерівність системи.",
        "solution": r"$1 \lt 3 \lt 4$ ✓. $4 \lt 4$ — хибно. $1 \ge 1$ і $1 \le 5$ ✓.",
    },
    # --- Розв'язування ---
    {
        "type": "CHOICE", "difficulty": 1, "skill": "SOLVE",
        "text": r"Розв'яжіть систему $\begin{cases} x \ge -2, \\ x \lt 5. \end{cases}$",
        "options": [(r"$[-2;\,5)$", True), (r"$(-2;\,5)$", False), (r"$[-2;\,5]$", False), (r"$(-2;\,5]$", False), (r"$(-\infty;\,5)$", False)],
        "hint": r"Який із кінців входить у відповідь?",
        "solution": r"Спільна частина $[-2;\,+\infty)$ і $(-\infty;\,5)$ — $[-2;\,5)$: $-2$ входить, $5$ — ні.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "SOLVE",
        "text": r"Розв'яжіть систему $\begin{cases} x \gt 3, \\ x \gt 7. \end{cases}$",
        "options": [(r"$(7;\,+\infty)$", True), (r"$(3;\,+\infty)$", False), (r"$(3;\,7)$", False), ("Розв'язків немає", False)],
        "hint": r"«Більше за більше».",
        "solution": r"Число, більше за $7$, точно більше за $3$. Відповідь: $(7;\,+\infty)$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"Скільки цілих розв'язків має подвійна нерівність $-2 \lt x \le 3$?",
        "answer": "5",
        "hint": r"Випишіть їх: $-2$ не входить, $3$ входить.",
        "solution": r"$-1,\ 0,\ 1,\ 2,\ 3$ — $5$ розв'язків.",
    },
    {
        "type": "FIELDS", "difficulty": 1, "skill": "SOLVE",
        "text": r"Розв'яжіть систему $\begin{cases} 2x \gt 6, \\ x \le 8. \end{cases}$ Відповідь має вигляд $(a;\,b]$.",
        "fields": [("$a =$", "3"), ("$b =$", "8")],
        "hint": r"Розв'яжіть першу нерівність: поділіть на $2$.",
        "solution": r"$x \gt 3$ і $x \le 8$: $x \in (3;\,8]$.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "SOLVE",
        "text": r"Розв'яжіть систему $\begin{cases} x \lt 2, \\ x \gt 6. \end{cases}$",
        "options": [("Розв'язків немає", True), (r"$(2;\,6)$", False), (r"$(-\infty;\,2)$", False), (r"$(6;\,+\infty)$", False)],
        "hint": r"Чи буває число водночас менше за $2$ і більше за $6$?",
        "solution": r"Промені $(-\infty;\,2)$ і $(6;\,+\infty)$ не мають спільних точок — розв'язків немає.",
    },
    # --- Аналіз результатів ---
    {
        "type": "ERROR", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Оля розв'язувала систему $\begin{cases} x \gt -1, \\ x \le 4. \end{cases}$ У якому кроці помилка?",
        "steps": [r"Перша нерівність: $x \in (-1;\,+\infty)$", r"Друга нерівність: $x \in (-\infty;\,4]$", r"Переріз: $[-1;\,4]$"],
        "wrong": 2,
        "hint": r"Чи входить $-1$ у розв'язки першої нерівності?",
        "solution": r"Знак строгий, тож $-1$ не входить: відповідь $(-1;\,4]$.",
    },
    {
        "type": "MULTI", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Які числа є розв'язками системи $\begin{cases} x \ge -3, \\ x \lt 2? \end{cases}$",
        "options": [(r"$-3$", True), (r"$2$", False), (r"$0$", True), (r"$-4$", False), (r"$1{,}5$", True)],
        "hint": r"Перевірте кожне число в обох нерівностях.",
        "solution": r"Розв'язки — $[-3;\,2)$: $-3$, $0$, $1{,}5$ — так; $2$ не входить, $-4 \lt -3$.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Петро записав: система $\begin{cases} x \gt 5, \\ x \lt 2 \end{cases}$ має розв'язки $(2;\,5)$. Яка відповідь правильна?",
        "options": [("Розв'язків немає", True), (r"$(2;\,5)$", False), (r"Усі числа, крім $[2;\,5]$", False), (r"$x = 3{,}5$", False)],
        "hint": r"Візьміть, наприклад, $x = 3$: чи виконується $x \gt 5$?",
        "solution": r"Число не може бути одночасно більшим за $5$ і меншим за $2$ — розв'язків немає.",
    },
    {
        "type": "TF", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [
            (r"Система $\begin{cases} x \ge 3, \\ x \le 3 \end{cases}$ має єдиний розв'язок", True),
            (r"Система $\begin{cases} x \gt 3, \\ x \le 3 \end{cases}$ має розв'язок $x = 3$", False),
            (r"Подвійна нерівність $1 \lt x \lt 4$ рівносильна системі $\begin{cases} x \gt 1, \\ x \lt 4 \end{cases}$", True),
        ],
        "hint": r"Підставте $x = 3$ у кожну нерівність.",
        "solution": r"$x = 3$ задовольняє $x \ge 3$ і $x \le 3$, але не $x \gt 3$. Подвійна нерівність — це коротший запис системи.",
    },
    {
        "type": "GROUP", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Чи має система розв'язки? Розподіліть.",
        "groups": ["Має розв'язки", "Не має розв'язків"],
        "items": [(r"$\begin{cases} x \gt 1, \\ x \lt 4 \end{cases}$", 0), (r"$\begin{cases} x \lt 0, \\ x \gt 2 \end{cases}$", 1),
                  (r"$\begin{cases} x \ge 5, \\ x \le 5 \end{cases}$", 0), (r"$\begin{cases} x \gt 5, \\ x \lt 5 \end{cases}$", 1),
                  (r"$\begin{cases} x \gt -3, \\ x \gt 1 \end{cases}$", 0)],
        "hint": r"Позначте обидва проміжки на одній прямій.",
        "solution": r"$(1;\,4)$, $\{5\}$, $(1;\,+\infty)$ — є розв'язки. У двох інших системах проміжки не перетинаються.",
    },

    # ==========================================
    # СХОДИНКА 2 — СЕРЕДНІЙ
    # ==========================================
    # --- Моделювання ---
    {
        "type": "FIELDS", "difficulty": 2, "skill": "MODEL",
        "text": r"Ширина прямокутника $x$ см, а довжина на $3$ см більша. Периметр більший за $18$ см і менший за $30$ см. Запишіть розв'язок у вигляді $a \lt x \lt b$.",
        "fields": [("$a =$", "3"), ("$b =$", "6")],
        "hint": r"$P = 2(x + x + 3) = 4x + 6$.",
        "solution": r"$\begin{cases} 4x + 6 \gt 18, \\ 4x + 6 \lt 30 \end{cases} \Rightarrow \begin{cases} x \gt 3, \\ x \lt 6. \end{cases}$ Отже, $3 \lt x \lt 6$.",
    },
    {
        "type": "MATCH", "difficulty": 2, "skill": "MODEL",
        "text": r"Установіть відповідність між системою (1–3) та її розв'язками (А–Д).",
        "options": [r"А) $(5;\,+\infty)$", r"Б) $(-\infty;\,2)$", r"В) $(2;\,5)$", "Г) розв'язків немає", r"Д) $(2;\,+\infty)$"],
        "matches": [(r"1. $\begin{cases} x \gt 2, \\ x \gt 5 \end{cases}$", r"А) $(5;\,+\infty)$"),
                    (r"2. $\begin{cases} x \lt 2, \\ x \lt 5 \end{cases}$", r"Б) $(-\infty;\,2)$"),
                    (r"3. $\begin{cases} x \gt 2, \\ x \lt 5 \end{cases}$", r"В) $(2;\,5)$")],
        "hint": r"«Більше за більше», «менше за менше», «між».",
        "solution": r"1) $x \gt 5$; 2) $x \lt 2$; 3) $2 \lt x \lt 5$.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "MODEL",
        "text": r"Знайдіть область визначення функції $y = \sqrt{x - 1} + \sqrt{4 - x}$.",
        "options": [(r"$[1;\,4]$", True), (r"$(1;\,4)$", False), (r"$[1;\,+\infty)$", False), (r"$(-\infty;\,4]$", False), (r"$\varnothing$", False)],
        "hint": r"Обидва підкореневі вирази мають бути невід'ємні одночасно.",
        "solution": r"$\begin{cases} x - 1 \ge 0, \\ 4 - x \ge 0 \end{cases} \Rightarrow 1 \le x \le 4$.",
    },
    {
        "type": "ORDER", "difficulty": 2, "skill": "MODEL",
        "text": r"Розташуйте кроки розв'язання системи $\begin{cases} 5 - 2x \gt 1, \\ 3x + 2 \ge -4 \end{cases}$ у правильному порядку.",
        "items": [
            r"$5 - 2x \gt 1 \Rightarrow -2x \gt -4 \Rightarrow x \lt 2$",
            r"$3x + 2 \ge -4 \Rightarrow 3x \ge -6 \Rightarrow x \ge -2$",
            "Позначаємо обидва проміжки на одній координатній прямій",
            r"Відповідь: $[-2;\,2)$",
        ],
        "hint": r"Спершу кожна нерівність окремо, потім переріз.",
        "solution": r"$x \lt 2$ і $x \ge -2$: $x \in [-2;\,2)$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "MODEL",
        "text": r"У Тараса $200$ грн. Він купує пакет за $2$ грн і $x$ булочок по $18$ грн; булочок треба щонайменше $8$. Скільки є варіантів кількості булочок?",
        "answer": "4",
        "hint": r"$\begin{cases} 18x + 2 \le 200, \\ x \ge 8 \end{cases}$, $x$ — натуральне.",
        "solution": r"$18x \le 198 \Rightarrow x \le 11$. Отже, $8 \le x \le 11$: $8, 9, 10, 11$ — $4$ варіанти.",
    },
    # --- Розв'язування ---
    {
        "type": "FIELDS", "difficulty": 2, "skill": "SOLVE",
        "text": r"Розв'яжіть систему $\begin{cases} 4x + 1 \ge 9, \\ 2x - 3 \lt 7. \end{cases}$ Відповідь має вигляд $[a;\,b)$.",
        "fields": [("$a =$", "2"), ("$b =$", "5")],
        "hint": r"Розв'яжіть кожну нерівність окремо.",
        "solution": r"$4x \ge 8 \Rightarrow x \ge 2$; $\;2x \lt 10 \Rightarrow x \lt 5$. Відповідь: $[2;\,5)$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Скільки цілих розв'язків має нерівність $-5 \lt 3x + 1 \le 10$?",
        "answer": "5",
        "hint": r"Відніміть $1$ від усіх трьох частин, потім поділіть на $3$.",
        "solution": r"$-6 \lt 3x \le 9 \Rightarrow -2 \lt x \le 3$: $-1, 0, 1, 2, 3$ — $5$ розв'язків.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "SOLVE",
        "text": r"Розв'яжіть систему $\begin{cases} -2x \gt 4, \\ x + 5 \ge 0. \end{cases}$",
        "options": [(r"$[-5;\,-2)$", True), (r"$(-5;\,-2]$", False), (r"$(-\infty;\,-2)$", False), (r"$(-2;\,5]$", False), (r"$[-5;\,2)$", False)],
        "hint": r"Ділимо на від'ємне число — знак змінюється.",
        "solution": r"$x \lt -2$ і $x \ge -5$: $x \in [-5;\,-2)$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Знайдіть найменший цілий розв'язок системи $\begin{cases} 3x + 4 \gt 1, \\ x - 2 \le 3. \end{cases}$",
        "answer": "0",
        "hint": r"Перша нерівність дає $x \gt -1$.",
        "solution": r"$3x \gt -3 \Rightarrow x \gt -1$; $x \le 5$. Розв'язки $(-1;\,5]$, найменший цілий — $0$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Знайдіть найбільший цілий розв'язок нерівності $1 \le \frac{x + 3}{2} \lt 4$.",
        "answer": "4",
        "hint": r"Помножте всі частини на $2$.",
        "solution": r"$2 \le x + 3 \lt 8 \Rightarrow -1 \le x \lt 5$. Найбільший цілий — $4$.",
    },
    # --- Аналіз результатів ---
    {
        "type": "ERROR", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Сашко розв'язував систему $\begin{cases} -3x \le 6, \\ x \lt 1. \end{cases}$ У якому кроці помилка?",
        "steps": [r"$-3x \le 6 \Rightarrow x \le -2$", r"Переріз з $x \lt 1$: $x \le -2$", r"Відповідь: $(-\infty;\,-2]$"],
        "wrong": 0,
        "hint": r"На яке число ділимо в першому кроці?",
        "solution": r"Ділимо на $-3$ — знак змінюється: $x \ge -2$. Відповідь: $[-2;\,1)$.",
    },
    {
        "type": "TF", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Система $\begin{cases} x \gt a, \\ x \lt 3. \end{cases}$ Правда чи ні?",
        "statements": [
            (r"При $a = 1$ розв'язки — $(1;\,3)$", True),
            (r"При $a = 3$ розв'язків немає", True),
            (r"При $a = 5$ розв'язки — $(3;\,5)$", False),
        ],
        "hint": r"Розв'язки — «між», якщо $a \lt 3$.",
        "solution": r"При $a \lt 3$ розв'язки $(a;\,3)$. При $a \ge 3$ — жодного: число не може бути більшим за $a$ і меншим за $3$.",
    },
    {
        "type": "MULTI", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Для яких систем число $-2$ є розв'язком?",
        "options": [(r"$\begin{cases} x \ge -2, \\ x \lt 0 \end{cases}$", True), (r"$\begin{cases} x \gt -2, \\ x \lt 3 \end{cases}$", False),
                    (r"$\begin{cases} 2x \le -4, \\ x \gt -5 \end{cases}$", True), (r"$\begin{cases} -x \ge 2, \\ x \ge -2 \end{cases}$", True)],
        "hint": r"Підставте $x = -2$ в обидві нерівності кожної системи.",
        "solution": r"$-2 \gt -2$ — хибно, тож друга система не підходить. В інших обидві нерівності виконуються: $-4 \le -4$, $2 \ge 2$.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Знайдіть область визначення функції $y = \sqrt{x + 3} + \frac{1}{\sqrt{2 - x}}$.",
        "options": [(r"$[-3;\,2)$", True), (r"$[-3;\,2]$", False), (r"$(-3;\,2)$", False), (r"$(-\infty;\,2)$", False), (r"$[-3;\,+\infty)$", False)],
        "hint": r"Корінь у знаменнику не може дорівнювати нулю.",
        "solution": r"$x + 3 \ge 0$ і $2 - x \gt 0$ (строго — бо знаменник): $-3 \le x \lt 2$.",
    },
    {
        "type": "GROUP", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Скільки розв'язків має система? Розподіліть.",
        "groups": ["Проміжок розв'язків", "Єдиний розв'язок", "Немає розв'язків"],
        "items": [(r"$\begin{cases} x \ge 2, \\ x \le 2 \end{cases}$", 1), (r"$\begin{cases} 2x \gt 4, \\ x \lt 2 \end{cases}$", 2),
                  (r"$\begin{cases} x + 1 \ge 0, \\ x \le 3 \end{cases}$", 0), (r"$\begin{cases} x \ge 4, \\ 8 - 2x \ge 0 \end{cases}$", 1),
                  (r"$\begin{cases} -x \gt 1, \\ x \gt 0 \end{cases}$", 2), (r"$\begin{cases} x \gt 0, \\ x \lt 0{,}5 \end{cases}$", 0)],
        "hint": r"Спершу розв'яжіть кожну нерівність.",
        "solution": r"$[-1;\,3]$ і $(0;\,0{,}5)$ — проміжки. $x = 2$ і $x = 4$ ($x \ge 4$, $x \le 4$) — єдині. $x \gt 2$ і $x \lt 2$; $x \lt -1$ і $x \gt 0$ — немає.",
    },

    # ==========================================
    # СХОДИНКА 3 — СКЛАДНИЙ
    # ==========================================
    # --- Моделювання ---
    {
        "type": "FIELDS", "difficulty": 3, "skill": "MODEL",
        "text": r"Дві сторони трикутника — $5$ см і $8$ см, третя — $x$ см. Запишіть усі можливі $x$ у вигляді $a \lt x \lt b$ і знайдіть кількість цілих $x$.",
        "fields": [("$a =$", "3"), ("$b =$", "13"), ("Кількість цілих $x$:", "9")],
        "hint": r"Кожна сторона менша від суми двох інших.",
        "solution": r"$\begin{cases} x \lt 5 + 8, \\ 8 \lt 5 + x, \\ 5 \lt 8 + x \end{cases} \Rightarrow 3 \lt x \lt 13$. Цілі: $4, \ldots, 12$ — $9$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"Подвоєне натуральне число більше за $7$, а потроєне — менше за $20$. Скільки таких чисел?",
        "answer": "3",
        "hint": r"$\begin{cases} 2x \gt 7, \\ 3x \lt 20. \end{cases}$",
        "solution": r"$x \gt 3{,}5$ і $x \lt 6\frac{2}{3}$: натуральні $4, 5, 6$ — три числа.",
    },
    {
        "type": "MATCH", "difficulty": 3, "skill": "MODEL",
        "text": r"Установіть відповідність між функцією (1–3) та її областю визначення (А–Д).",
        "options": [r"А) $[2;\,5]$", r"Б) $[2;\,5)$", r"В) $(2;\,5]$", r"Г) $(2;\,5)$", r"Д) $[5;\,+\infty)$"],
        "matches": [(r"1. $y = \sqrt{x - 2} + \sqrt{5 - x}$", r"А) $[2;\,5]$"),
                    (r"2. $y = \sqrt{x - 2} + \frac{1}{\sqrt{5 - x}}$", r"Б) $[2;\,5)$"),
                    (r"3. $y = \frac{1}{\sqrt{x - 2}} + \sqrt{5 - x}$", r"В) $(2;\,5]$")],
        "hint": r"Корінь у знаменнику дає строгу нерівність.",
        "solution": r"1) $x \ge 2$, $x \le 5$. 2) $x \ge 2$, $x \lt 5$. 3) $x \gt 2$, $x \le 5$.",
    },
    {
        "type": "POINT", "difficulty": 3, "skill": "MODEL",
        "text": r"Позначте на прямій найменший цілий розв'язок системи $\begin{cases} 2x + 5 \gt 0, \\ x \lt 3. \end{cases}$",
        "min": -5, "max": 5, "step": 1, "answer": -2,
        "hint": r"$2x \gt -5$, тобто $x \gt -2{,}5$.",
        "solution": r"Розв'язки — $(-2{,}5;\,3)$. Найменше ціле, більше за $-2{,}5$, — це $-2$.",
    },
    {
        "type": "ORDER", "difficulty": 3, "skill": "MODEL",
        "text": r"Розташуйте системи за кількістю цілих розв'язків — від найменшої до найбільшої.",
        "items": [r"$\begin{cases} x \gt 0, \\ x \lt 1 \end{cases}$", r"$-1 \le x \le 1$", r"$\begin{cases} x \ge -2, \\ x \lt 3 \end{cases}$", r"$0 \lt 2x \le 14$"],
        "hint": r"Для кожної системи запишіть проміжок і полічіть цілі числа в ньому.",
        "solution": r"$(0;\,1)$ — $0$; $[-1;\,1]$ — $3$; $[-2;\,3)$ — $5$; $(0;\,7]$ — $7$.",
    },
    # --- Розв'язування ---
    {
        "type": "FIELDS", "difficulty": 3, "skill": "SOLVE",
        "text": r"Розв'яжіть систему $\begin{cases} \frac{x - 1}{2} \ge \frac{x + 1}{3}, \\ 3(x - 2) \lt 2x + 1. \end{cases}$ Відповідь має вигляд $[a;\,b)$.",
        "fields": [("$a =$", "5"), ("$b =$", "7")],
        "hint": r"Першу нерівність помножте на $6$.",
        "solution": r"$3(x - 1) \ge 2(x + 1) \Rightarrow x \ge 5$; $\;3x - 6 \lt 2x + 1 \Rightarrow x \lt 7$. Відповідь: $[5;\,7)$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Знайдіть суму цілих розв'язків системи $\begin{cases} 2(x + 3) \gt x + 4, \\ 5x - 1 \le 3x + 7. \end{cases}$",
        "answer": "9",
        "hint": r"Розкрийте дужки й зведіть подібні.",
        "solution": r"$2x + 6 \gt x + 4 \Rightarrow x \gt -2$; $\;2x \le 8 \Rightarrow x \le 4$. Цілі: $-1, 0, 1, 2, 3, 4$; сума $9$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Скільки цілих розв'язків має нерівність $-7 \le 1 - 2x \lt 5$?",
        "answer": "6",
        "hint": r"Після ділення на $-2$ обидва знаки змінюються.",
        "solution": r"$-8 \le -2x \lt 4 \Rightarrow 4 \ge x \gt -2$. Цілі: $-1, 0, 1, 2, 3, 4$ — $6$.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "SOLVE",
        "text": r"Розв'яжіть систему $\begin{cases} x \gt -1, \\ x \le 6, \\ 2x \lt 8. \end{cases}$",
        "options": [(r"$(-1;\,4)$", True), (r"$(-1;\,6]$", False), (r"$(4;\,6]$", False), (r"$[-1;\,4)$", False), (r"$(-1;\,4]$", False)],
        "hint": r"Розв'язок має задовольняти всі три нерівності.",
        "solution": r"$x \lt 4$ сильніша за $x \le 6$. Отже, $-1 \lt x \lt 4$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Скільки цілих чисел належить області визначення функції $y = \sqrt{6 - 3x} + \sqrt{x + 4}$?",
        "answer": "7",
        "hint": r"Обидва підкореневі вирази невід'ємні.",
        "solution": r"$6 - 3x \ge 0 \Rightarrow x \le 2$; $x \ge -4$. $D(y) = [-4;\,2]$: $7$ цілих чисел.",
    },
    # --- Аналіз результатів ---
    {
        "type": "ERROR", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Ярина розв'язувала нерівність $-1 \lt 3 - 2x \le 5$. У якому кроці помилка?",
        "steps": [r"Віднімаємо $3$: $-4 \lt -2x \le 2$", r"Ділимо на $-2$: $2 \lt x \le -1$", "Розв'язків немає"],
        "wrong": 1,
        "hint": r"Що буває зі знаками при діленні на від'ємне число?",
        "solution": r"Знаки змінюються: $2 \gt x \ge -1$, тобто $x \in [-1;\,2)$.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "ANALYZE",
        "text": r"При яких значеннях $a$ система $\begin{cases} x \le 4, \\ x \ge a \end{cases}$ має хоча б один розв'язок?",
        "options": [(r"$a \le 4$", True), (r"$a \lt 4$", False), (r"$a \ge 4$", False), (r"$a \gt 4$", False), (r"при будь-яких $a$", False)],
        "hint": r"Перевірте окремо $a = 4$.",
        "solution": r"Розв'язки — $[a;\,4]$, він не порожній при $a \le 4$. При $a = 4$ — єдиний розв'язок $x = 4$.",
    },
    {
        "type": "TF", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [
            ("Якщо кожна нерівність системи має розв'язки, то й система має розв'язки", False),
            (r"Система $\begin{cases} x \gt a, \\ x \gt b \end{cases}$ має розв'язки при будь-яких $a$ і $b$", True),
            (r"Нерівність $5 \lt x \lt 2$ не має розв'язків", True),
        ],
        "hint": r"Згадайте систему $\begin{cases} x \lt 2, \\ x \gt 6. \end{cases}$",
        "solution": r"$x \lt 2$ і $x \gt 6$ мають розв'язки окремо, а разом — ні. «Більше за більше» — завжди промінь. $5 \lt x \lt 2$ — це $x \gt 5$ і $x \lt 2$: розв'язків немає.",
    },
    {
        "type": "MULTI", "difficulty": 3, "skill": "ANALYZE",
        "text": r"При яких значеннях $a$ система $\begin{cases} x \gt a, \\ x \lt 2 \end{cases}$ має рівно три цілі розв'язки?",
        "options": [(r"$a = -2$", True), (r"$a = -1{,}5$", True), (r"$a = -1$", False), (r"$a = -3$", False), (r"$a = -1{,}9$", True)],
        "hint": r"Три найбільші цілі, менші за $2$: $1, 0, -1$.",
        "solution": r"Потрібно, щоб $-1 \gt a$, але $-2$ не входило: $-2 \le a \lt -1$. Підходять $-2$, $-1{,}9$, $-1{,}5$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Знайдіть найбільше ціле $a$, при якому система $\begin{cases} x \ge 3, \\ x \lt a \end{cases}$ не має розв'язків.",
        "answer": "3",
        "hint": r"Що буде при $a = 3$? А при $a = 4$?",
        "solution": r"При $a = 3$: $x \ge 3$ і $x \lt 3$ — розв'язків немає. При $a = 4$ є розв'язок $x = 3$. Відповідь: $3$.",
    },

    # ==========================================
    # БОСИ — після опанування теми
    # ==========================================
    {
        "type": "SHORT", "difficulty": 4, "skill": "MODEL",
        "text": r"Сума трьох послідовних натуральних чисел більша за $40$, але менша за $52$. Скільки існує таких трійок чисел?",
        "answer": "4",
        "solution": r"Числа $n$, $n + 1$, $n + 2$; сума $3n + 3$. $40 \lt 3n + 3 \lt 52 \Rightarrow 12\frac{1}{3} \lt n \lt 16\frac{1}{3}$. $n = 13, 14, 15, 16$ — $4$ трійки.",
    },
    {
        "type": "FIELDS", "difficulty": 4, "skill": "MODEL",
        "text": r"Сторони трикутника — $x$ см, $(x + 2)$ см і $10$ см, а його периметр менший за $30$ см. Запишіть усі можливі $x$ у вигляді $a \lt x \lt b$ і знайдіть кількість цілих $x$.",
        "fields": [("$a =$", "4"), ("$b =$", "9"), ("Кількість цілих $x$:", "4")],
        "solution": r"Нерівність трикутника: $x + (x + 2) \gt 10 \Rightarrow x \gt 4$ (дві інші виконуються завжди). Периметр: $2x + 12 \lt 30 \Rightarrow x \lt 9$. Отже, $4 \lt x \lt 9$: $x = 5, 6, 7, 8$.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "SOLVE",
        "text": r"Знайдіть суму цілих розв'язків системи $\begin{cases} \frac{2x - 1}{3} - \frac{x - 1}{2} \le 1, \\ 3 - 2(x + 1) \lt 7. \end{cases}$",
        "answer": "12",
        "solution": r"Множимо першу на $6$: $4x - 2 - 3x + 3 \le 6 \Rightarrow x \le 5$. Друга: $1 - 2x \lt 7 \Rightarrow x \gt -3$. Цілі $-2, \ldots, 5$; сума $12$.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "SOLVE",
        "text": r"Скільки цілих чисел належить області визначення функції $y = \frac{\sqrt{x + 5}}{x - 1} + \sqrt{8 - 2x}$?",
        "answer": "9",
        "solution": r"$\begin{cases} x + 5 \ge 0, \\ x - 1 \ne 0, \\ 8 - 2x \ge 0 \end{cases} \Rightarrow x \in [-5;\,1) \cup (1;\,4]$. Цілих на $[-5;\,4]$ — $10$, без $x = 1$ — $9$.",
    },
    {
        "type": "TF", "difficulty": 4, "skill": "ANALYZE",
        "text": r"Система $\begin{cases} x \gt a, \\ x \le 3. \end{cases}$ Правда чи ні?",
        "statements": [
            (r"При $a = 3$ розв'язків немає", True),
            (r"При $a = 0$ система має рівно $3$ цілі розв'язки", True),
            (r"При $a = -0{,}5$ система має рівно $3$ цілі розв'язки", False),
            (r"При $a = 2{,}9$ система має цілий розв'язок", True),
        ],
        "solution": r"Розв'язки — $(a;\,3]$. При $a = 3$ — порожньо. При $a = 0$: $1, 2, 3$. При $a = -0{,}5$: $0, 1, 2, 3$ — чотири. При $a = 2{,}9$ входить $x = 3$.",
    },

    # ==========================================
    # УЛЬТРА-БОСИ
    # ==========================================
    {
        "type": "SHORT", "difficulty": 5, "skill": "SOLVE",
        "text": r"При якому значенні $a$ система $\begin{cases} x \ge a, \\ 2x - a \le 6 \end{cases}$ має єдиний розв'язок?",
        "answer": "6",
        "solution": r"Друга нерівність: $x \le \frac{a + 6}{2}$. Розв'язки — $\left[a;\,\frac{a + 6}{2}\right]$. Єдиний розв'язок, коли кінці збігаються: $a = \frac{a + 6}{2} \Rightarrow a = 6$ (тоді $x = 6$).",
    },
    {
        "type": "SHORT", "difficulty": 5, "skill": "SOLVE",
        "text": r"Знайдіть суму цілих розв'язків системи $\begin{cases} |2x - 1| \le 7, \\ 3x - 4 \gt x. \end{cases}$",
        "answer": "7",
        "solution": r"$|2x - 1| \le 7 \iff -7 \le 2x - 1 \le 7 \iff -3 \le x \le 4$. Друга: $2x \gt 4 \Rightarrow x \gt 2$. Переріз $(2;\,4]$: цілі $3$ і $4$, сума $7$.",
    },
]
