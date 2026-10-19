TOPIC_NAME = "1.3. Властивості кореня n-го степеня"
COURSE = "Алгебра і початки аналізу (10-11 класи)"
GRADE = "10 клас"

TASKS = [
    # ==========================================
    # СХОДИНКА 1 — БАЗОВИЙ
    # ==========================================
    # --- Моделювання ---
    {
        "type": "CHOICE", "difficulty": 1, "skill": "MODEL",
        "text": r"Яка рівність правильна при $a \ge 0$, $b \ge 0$?",
        "options": [(r"$\sqrt[n]{ab} = \sqrt[n]{a} \cdot \sqrt[n]{b}$", True), (r"$\sqrt[n]{a + b} = \sqrt[n]{a} + \sqrt[n]{b}$", False),
                    (r"$\sqrt[n]{ab} = \sqrt[n]{a} + \sqrt[n]{b}$", False), (r"$\sqrt[n]{a - b} = \sqrt[n]{a} - \sqrt[n]{b}$", False)],
        "hint": r"Властивості є лише для добутку й частки.",
        "solution": r"Корінь з добутку невід'ємних множників дорівнює добутку коренів. Для суми й різниці такої властивості немає: $\sqrt{9 + 16} = 5 \ne 7$.",
    },
    {
        "type": "MATCH", "difficulty": 1, "skill": "MODEL",
        "text": r"Установіть відповідність між виразом (1–3) та його значенням (А–Д).",
        "options": [r"А) $2$", r"Б) $3$", r"В) $-2$", r"Г) $-3$", r"Д) $4$"],
        "matches": [(r"1. $\sqrt[3]{2} \cdot \sqrt[3]{4}$", r"А) $2$"), (r"2. $\sqrt[4]{81}$", r"Б) $3$"), (r"3. $\sqrt[5]{-32}$", r"В) $-2$")],
        "hint": r"Корінь непарного степеня з від'ємного числа — від'ємний.",
        "solution": r"$\sqrt[3]{8} = 2$; $3^4 = 81$; $(-2)^5 = -32$.",
    },
    {
        "type": "GROUP", "difficulty": 1, "skill": "MODEL",
        "text": r"Чи має зміст вираз? Розподіліть.",
        "groups": ["Має зміст", "Не має змісту"],
        "items": [(r"$\sqrt[4]{-16}$", 1), (r"$\sqrt[3]{-27}$", 0), (r"$\sqrt[6]{0}$", 0), (r"$\sqrt[4]{(-2)^2}$", 0), (r"$\sqrt{-1}$", 1)],
        "hint": r"Корінь парного степеня — лише з невід'ємного числа.",
        "solution": r"$\sqrt[4]{-16}$ і $\sqrt{-1}$ не мають змісту. $\sqrt[3]{-27} = -3$, $\sqrt[6]{0} = 0$, $\sqrt[4]{(-2)^2} = \sqrt[4]{4} = \sqrt{2}$.",
    },
    {
        "type": "TF", "difficulty": 1, "skill": "MODEL",
        "text": r"Правда чи ні?",
        "statements": [
            (r"$\sqrt[n]{a^n} = a$ при будь-якому $a$, якщо $n$ парне", False),
            (r"$\sqrt[3]{-8} = -2$", True),
            (r"$\sqrt[4]{16} = \pm 2$", False),
        ],
        "hint": r"Арифметичний корінь парного степеня — невід'ємне число.",
        "solution": r"При парному $n$: $\sqrt[n]{a^n} = |a|$. $(-2)^3 = -8$ ✓. $\sqrt[4]{16} = 2$ — лише невід'ємне значення.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "MODEL",
        "text": r"За яких умов правильна рівність $\sqrt[4]{\frac{a}{b}} = \frac{\sqrt[4]{a}}{\sqrt[4]{b}}$?",
        "options": [(r"$a \ge 0$, $b \gt 0$", True), (r"$a \ge 0$, $b \ge 0$", False), (r"будь-які $a$, $b \ne 0$", False), (r"$a \gt 0$, $b \ge 0$", False)],
        "hint": r"Обидва корені мають існувати, а знаменник — не дорівнювати нулю.",
        "solution": r"Корені четвертого степеня — з невід'ємних чисел, а $\sqrt[4]{b}$ у знаменнику — ненульовий: $a \ge 0$, $b \gt 0$.",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"Обчисліть $\sqrt[3]{25} \cdot \sqrt[3]{5}$.",
        "answer": "5",
        "hint": r"Корінь з добутку.",
        "solution": r"$\sqrt[3]{125} = 5$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"Обчисліть $\frac{\sqrt[4]{48}}{\sqrt[4]{3}}$.",
        "answer": "2",
        "hint": r"Корінь з частки.",
        "solution": r"$\sqrt[4]{48 : 3} = \sqrt[4]{16} = 2$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"Обчисліть $\sqrt[5]{(-3)^5}$.",
        "answer": "-3",
        "hint": r"Степінь непарний.",
        "solution": r"При непарному $n$: $\sqrt[n]{a^n} = a$, тож $-3$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"Обчисліть $\sqrt[4]{(-5)^4}$.",
        "answer": "5",
        "hint": r"Степінь парний — з'являється модуль.",
        "solution": r"$\sqrt[4]{(-5)^4} = |-5| = 5$.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "SOLVE",
        "text": r"Обчисліть $\sqrt[3]{\sqrt{64}}$.",
        "options": [(r"$2$", True), (r"$4$", False), (r"$8$", False), (r"$16$", False)],
        "hint": r"$\sqrt[k]{\sqrt[n]{a}} = \sqrt[nk]{a}$.",
        "solution": r"$\sqrt[6]{64} = 2$, бо $2^6 = 64$. Або: $\sqrt{64} = 8$, $\sqrt[3]{8} = 2$.",
    },
    # --- Аналіз результатів ---
    {
        "type": "ERROR", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Оля обчислювала $\sqrt[4]{(-3)^4}$. У якому кроці помилка?",
        "steps": [r"Показники кореня і степеня однакові — $4$", r"Тому $\sqrt[4]{(-3)^4} = -3$", r"Відповідь: $-3$"],
        "wrong": 1,
        "hint": r"Чи може корінь четвертого степеня бути від'ємним?",
        "solution": r"При парному $n$: $\sqrt[n]{a^n} = |a|$. $\sqrt[4]{81} = 3$.",
    },
    {
        "type": "MULTI", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Які рівності правильні?",
        "options": [(r"$\sqrt[3]{-8} = -2$", True), (r"$\sqrt{(-7)^2} = -7$", False), (r"$\sqrt[4]{16 \cdot 81} = 6$", True), (r"$\sqrt{9 + 16} = 7$", False), (r"$\sqrt[3]{2} \cdot \sqrt[3]{32} = 4$", True)],
        "hint": r"Перевірте модуль і чи не корінь із суми.",
        "solution": r"$\sqrt{(-7)^2} = 7$; $\sqrt{25} = 5$. $\sqrt[4]{16} \cdot \sqrt[4]{81} = 2 \cdot 3 = 6$ ✓; $\sqrt[3]{64} = 4$ ✓.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Петро записав: $\sqrt{-4} \cdot \sqrt{-9} = \sqrt{36} = 6$. Що правильно?",
        "options": [(r"Вираз $\sqrt{-4} \cdot \sqrt{-9}$ не має змісту", True), (r"Усе правильно: $6$", False), (r"Відповідь $-6$", False), (r"Відповідь $\pm 6$", False)],
        "hint": r"Чи існує $\sqrt{-4}$?",
        "solution": r"Квадратні корені з від'ємних чисел не існують. Властивість $\sqrt{ab} = \sqrt{a}\sqrt{b}$ — лише для $a, b \ge 0$.",
    },
    {
        "type": "TF", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [
            (r"$\sqrt[6]{a^6} = |a|$", True),
            (r"$\sqrt[5]{a^5} = |a|$", False),
            (r"$\sqrt[3]{a} \cdot \sqrt[3]{b} = \sqrt[3]{ab}$ при будь-яких $a$, $b$", True),
        ],
        "hint": r"Модуль з'являється лише для парного показника.",
        "solution": r"$6$ — парне: модуль. $5$ — непарне: $\sqrt[5]{a^5} = a$ (при $a = -1$ маємо $-1 \ne 1$). Для непарних коренів властивість добутку — без умов.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Яке з чисел більше: $\sqrt[3]{2}$ чи $\sqrt{2}$?",
        "options": [(r"$\sqrt{2}$", True), (r"$\sqrt[3]{2}$", False), ("Вони рівні", False), ("Порівняти неможливо", False)],
        "hint": r"Зведіть до кореня шостого степеня.",
        "solution": r"$\sqrt[3]{2} = \sqrt[6]{4}$, $\sqrt{2} = \sqrt[6]{8}$; $4 \lt 8$, тож $\sqrt{2}$ більше.",
    },

    # ==========================================
    # СХОДИНКА 2 — СЕРЕДНІЙ
    # ==========================================
    # --- Моделювання ---
    {
        "type": "FIELDS", "difficulty": 2, "skill": "MODEL",
        "text": r"Винесіть множник з-під знака кореня.",
        "fields": [(r"$\sqrt[3]{54} = a\sqrt[3]{2}$, $\;a =$", "3"), (r"$\sqrt[4]{48} = b\sqrt[4]{3}$, $\;b =$", "2")],
        "hint": r"$54 = 27 \cdot 2$, $48 = 16 \cdot 3$.",
        "solution": r"$\sqrt[3]{27 \cdot 2} = 3\sqrt[3]{2}$; $\sqrt[4]{16 \cdot 3} = 2\sqrt[4]{3}$.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "MODEL",
        "text": r"Внесіть множник під знак кореня: $-2\sqrt[4]{3}$.",
        "options": [(r"$-\sqrt[4]{48}$", True), (r"$\sqrt[4]{48}$", False), (r"$\sqrt[4]{-48}$", False), (r"$-\sqrt[4]{24}$", False), (r"$\sqrt[4]{-6}$", False)],
        "hint": r"Від'ємний множник під корінь парного степеня не вносять — мінус лишається.",
        "solution": r"$-2\sqrt[4]{3} = -\sqrt[4]{2^4 \cdot 3} = -\sqrt[4]{48}$. $\sqrt[4]{48} \gt 0$, а вихідний вираз від'ємний.",
    },
    {
        "type": "ORDER", "difficulty": 2, "skill": "MODEL",
        "text": r"Розташуйте числа від найменшого до найбільшого.",
        "items": [r"$\sqrt[3]{2}$", r"$\sqrt[6]{6}$", r"$\sqrt{2}$", r"$\sqrt[3]{3}$"],
        "hint": r"Зведіть усі корені до шостого степеня.",
        "solution": r"$\sqrt[6]{4} \lt \sqrt[6]{6} \lt \sqrt[6]{8} \lt \sqrt[6]{9}$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "MODEL",
        "text": r"Об'єми двох кубів — $54$ см³ і $16$ см³. У скільки разів ребро першого куба більше за ребро другого?",
        "answer": "1.5",
        "hint": r"Ребро куба — корінь кубічний з об'єму.",
        "solution": r"$\frac{\sqrt[3]{54}}{\sqrt[3]{16}} = \sqrt[3]{\frac{27}{8}} = \frac{3}{2} = 1{,}5$.",
    },
    {
        "type": "MATCH", "difficulty": 2, "skill": "MODEL",
        "text": r"Установіть відповідність між виразом (1–3) та його спрощеним виглядом (А–Д).",
        "options": [r"А) $2 - x$", r"Б) $x - 2$", r"В) $x + 2$", r"Г) $-x - 2$", r"Д) $(x - 2)^2$"],
        "matches": [(r"1. $\sqrt[4]{(x - 2)^4}$, якщо $x \lt 2$", r"А) $2 - x$"), (r"2. $\sqrt[3]{(x - 2)^3}$", r"Б) $x - 2$"),
                    (r"3. $\sqrt{(x + 2)^2}$, якщо $x \ge -2$", r"В) $x + 2$")],
        "hint": r"Парний показник — модуль; знак підмодульного виразу визначає умова.",
        "solution": r"1) $|x - 2| = 2 - x$, бо $x - 2 \lt 0$. 2) Непарний показник — без модуля. 3) $|x + 2| = x + 2$, бо $x + 2 \ge 0$.",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Спростіть: $\sqrt[4]{32} + \sqrt[4]{162} - 4\sqrt[4]{2} = k\sqrt[4]{2}$. Знайдіть $k$.",
        "answer": "1",
        "hint": r"$32 = 16 \cdot 2$, $162 = 81 \cdot 2$.",
        "solution": r"$2\sqrt[4]{2} + 3\sqrt[4]{2} - 4\sqrt[4]{2} = \sqrt[4]{2}$, $k = 1$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Обчисліть $\sqrt[3]{9} \cdot \sqrt[3]{24}$.",
        "answer": "6",
        "hint": r"$9 \cdot 24 = 216$.",
        "solution": r"$\sqrt[3]{216} = 6$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Обчисліть $\left(\sqrt[6]{27}\right)^2$.",
        "answer": "3",
        "hint": r"$\left(\sqrt[n]{a}\right)^k = \sqrt[n]{a^k}$, далі основна властивість.",
        "solution": r"$\sqrt[6]{27^2} = \sqrt[6]{3^6} = 3$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Знайдіть значення виразу $\sqrt[4]{(x + 1)^4} + x$, якщо $x \lt -1$.",
        "answer": "-1",
        "hint": r"$x + 1 \lt 0$.",
        "solution": r"$\sqrt[4]{(x + 1)^4} = |x + 1| = -x - 1$; $-x - 1 + x = -1$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Обчисліть $\sqrt[4]{17 - \sqrt{33}} \cdot \sqrt[4]{17 + \sqrt{33}}$.",
        "answer": "4",
        "hint": r"Різниця квадратів під коренем.",
        "solution": r"$\sqrt[4]{17^2 - 33} = \sqrt[4]{256} = 4$. Обидва підкореневі вирази додатні ($\sqrt{33} \lt 17$).",
    },
    # --- Аналіз результатів ---
    {
        "type": "ERROR", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Максим вносив множник під корінь: $-3\sqrt{2}$. У якому кроці помилка?",
        "steps": [r"Множник $-3$ від'ємний", r"$-3\sqrt{2} = \sqrt{(-3)^2 \cdot 2}$", r"$= \sqrt{18}$"],
        "wrong": 1,
        "hint": r"Ліва частина від'ємна, а квадратний корінь — ні.",
        "solution": r"Мінус лишається перед коренем: $-3\sqrt{2} = -\sqrt{9 \cdot 2} = -\sqrt{18}$.",
    },
    {
        "type": "TF", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [
            (r"$\sqrt[4]{x^8} = x^2$ при будь-якому $x$", True),
            (r"$\sqrt[6]{x^2} = \sqrt[3]{x}$ при будь-якому $x$", False),
            (r"$\sqrt{x^2} = x$ при $x \ge 0$", True),
        ],
        "hint": r"Перевірте друге твердження при $x = -1$.",
        "solution": r"$\sqrt[4]{(x^2)^4} = |x^2| = x^2$ ✓. При $x = -1$: $\sqrt[6]{1} = 1$, а $\sqrt[3]{-1} = -1$; правильно $\sqrt[6]{x^2} = \sqrt[3]{|x|}$. $|x| = x$ при $x \ge 0$ ✓.",
    },
    {
        "type": "MULTI", "difficulty": 2, "skill": "ANALYZE",
        "text": r"При яких значеннях $a$ рівність $\sqrt[4]{a^4} = a$ правильна?",
        "options": [(r"$a = 0$", True), (r"$a = 2$", True), (r"$a = -2$", False), (r"$a = 0{,}5$", True), (r"$a = -0{,}1$", False)],
        "hint": r"$\sqrt[4]{a^4} = |a|$.",
        "solution": r"$|a| = a$ лише при $a \ge 0$.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Спростіть $\sqrt{\left(1 - \sqrt{3}\right)^2} + 1$.",
        "options": [(r"$\sqrt{3}$", True), (r"$2 - \sqrt{3}$", False), (r"$2 + \sqrt{3}$", False), (r"$-\sqrt{3}$", False), (r"$2$", False)],
        "hint": r"Знак числа $1 - \sqrt{3}$?",
        "solution": r"$1 - \sqrt{3} \lt 0$, тож $\left|1 - \sqrt{3}\right| = \sqrt{3} - 1$; $\sqrt{3} - 1 + 1 = \sqrt{3}$. Відповідь Б — загубили модуль.",
    },
    {
        "type": "GROUP", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Визначте знак виразу.",
        "groups": ["Додатний", "Від'ємний"],
        "items": [(r"$\sqrt[3]{-5}$", 1), (r"$\sqrt[4]{5}$", 0), (r"$-\sqrt[4]{3}$", 1), (r"$\sqrt[3]{2 - 3}$", 1), (r"$\sqrt[6]{(-2)^6}$", 0)],
        "hint": r"Корінь парного степеня невід'ємний; непарного — того самого знака, що й підкореневий вираз.",
        "solution": r"$\sqrt[3]{-5} \lt 0$, $-\sqrt[4]{3} \lt 0$, $\sqrt[3]{-1} = -1$. $\sqrt[4]{5} \gt 0$, $\sqrt[6]{64} = 2$.",
    },

    # ==========================================
    # СХОДИНКА 3 — СКЛАДНИЙ
    # ==========================================
    # --- Моделювання ---
    {
        "type": "FIELDS", "difficulty": 3, "skill": "MODEL",
        "text": r"Винесіть множники: $\sqrt[3]{a^7 b^4} = a^m b^k \sqrt[3]{ab}$. Знайдіть $m$ і $k$.",
        "fields": [("$m =$", "2"), ("$k =$", "1")],
        "hint": r"$a^7 = (a^2)^3 \cdot a$.",
        "solution": r"$a^7 b^4 = (a^2 b)^3 \cdot ab$, корінь непарний — без модулів: $a^2 b\sqrt[3]{ab}$.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "MODEL",
        "text": r"Укажіть найбільше з чисел.",
        "options": [(r"$\sqrt[3]{4}$", True), (r"$\sqrt[4]{6}$", False), (r"$\sqrt[6]{15}$", False), (r"$\sqrt[12]{250}$", False), (r"$\sqrt{2}$", False)],
        "hint": r"Спільний показник — $12$.",
        "solution": r"$\sqrt[12]{256}$, $\sqrt[12]{216}$, $\sqrt[12]{225}$, $\sqrt[12]{250}$, $\sqrt[12]{64}$ — найбільше $\sqrt[3]{4}$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"У скільки разів ребро куба об'ємом $250$ см³ більше за ребро куба об'ємом $2$ см³?",
        "answer": "5",
        "hint": r"Корінь з частки.",
        "solution": r"$\frac{\sqrt[3]{250}}{\sqrt[3]{2}} = \sqrt[3]{125} = 5$.",
    },
    {
        "type": "MATCH", "difficulty": 3, "skill": "MODEL",
        "text": r"Нехай $a \lt 0$. Установіть відповідність між виразом (1–3) та його спрощеним виглядом (А–Д).",
        "options": [r"А) $-a$", r"Б) $a$", r"В) $0$", r"Г) $2a$", r"Д) $-2a$"],
        "matches": [(r"1. $\sqrt{a^2}$", r"А) $-a$"), (r"2. $\sqrt[3]{a^3}$", r"Б) $a$"), (r"3. $\sqrt[4]{a^4} + a$", r"В) $0$")],
        "hint": r"$|a| = -a$ при $a \lt 0$.",
        "solution": r"1) $|a| = -a$. 2) $a$. 3) $|a| + a = -a + a = 0$.",
    },
    {
        "type": "ORDER", "difficulty": 3, "skill": "MODEL",
        "text": r"Розташуйте кроки спрощення $\sqrt[4]{48} + \sqrt[4]{243} - \sqrt[4]{3}$.",
        "items": [
            r"$48 = 16 \cdot 3$, $\;243 = 81 \cdot 3$",
            r"$\sqrt[4]{48} = 2\sqrt[4]{3}$, $\;\sqrt[4]{243} = 3\sqrt[4]{3}$",
            r"$2\sqrt[4]{3} + 3\sqrt[4]{3} - \sqrt[4]{3}$",
            r"$4\sqrt[4]{3}$",
        ],
        "hint": r"Розклад → винесення → подібні доданки.",
        "solution": r"$\sqrt[4]{48} + \sqrt[4]{243} - \sqrt[4]{3} = 4\sqrt[4]{3}$.",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Обчисліть $\left(\sqrt[3]{3} \cdot \sqrt[6]{3}\right)^2$.",
        "answer": "3",
        "hint": r"$\sqrt[3]{3} = \sqrt[6]{9}$.",
        "solution": r"$\sqrt[6]{9} \cdot \sqrt[6]{3} = \sqrt[6]{27} = \sqrt{3}$; $(\sqrt{3})^2 = 3$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Обчисліть $\left(\sqrt[4]{3} - 1\right)\left(\sqrt[4]{3} + 1\right)\left(\sqrt{3} + 1\right)$.",
        "answer": "2",
        "hint": r"Двічі різниця квадратів.",
        "solution": r"$(\sqrt{3} - 1)(\sqrt{3} + 1) = 3 - 1 = 2$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Обчисліть $\sqrt[3]{\left(\sqrt{2} - 3\right)^3} + \sqrt{\left(\sqrt{2} - 3\right)^2}$.",
        "answer": "0",
        "hint": r"Перший корінь — непарного степеня, другий — парного.",
        "solution": r"$(\sqrt{2} - 3) + |\sqrt{2} - 3| = \sqrt{2} - 3 + 3 - \sqrt{2} = 0$.",
    },
    {
        "type": "FIELDS", "difficulty": 3, "skill": "SOLVE",
        "text": r"Знайдіть значення виразу $\sqrt[4]{x^4} + \sqrt[3]{x^3}$.",
        "fields": [(r"при $x = -5$:", "0"), (r"при $x = 5$:", "10")],
        "hint": r"$|x| + x$.",
        "solution": r"При $x \lt 0$: $-x + x = 0$; при $x \gt 0$: $2x = 10$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Обчисліть $\sqrt{7 + 4\sqrt{3}} - \sqrt{3}$.",
        "answer": "2",
        "hint": r"$7 + 4\sqrt{3} = \left(2 + \sqrt{3}\right)^2$.",
        "solution": r"$\left(2 + \sqrt{3}\right)^2 = 4 + 4\sqrt{3} + 3$ ✓. $\sqrt{7 + 4\sqrt{3}} = 2 + \sqrt{3}$, мінус $\sqrt{3}$ — $2$.",
    },
    # --- Аналіз результатів ---
    {
        "type": "ERROR", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Ярина спрощувала $\sqrt[4]{16a^4}$ при $a \lt 0$. У якому кроці помилка?",
        "steps": [r"$16a^4 = (2a)^4$", r"$\sqrt[4]{(2a)^4} = 2a$", r"Відповідь: $2a$"],
        "wrong": 1,
        "hint": r"Чи може результат бути від'ємним?",
        "solution": r"$\sqrt[4]{(2a)^4} = |2a| = -2a$, бо $a \lt 0$.",
    },
    {
        "type": "TF", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [
            (r"$\sqrt[nk]{a^k} = \sqrt[n]{a}$ при $a \ge 0$", True),
            (r"$\sqrt[6]{(-8)^2} = \sqrt[3]{-8}$", False),
            (r"$\sqrt[3]{-a} = -\sqrt[3]{a}$ при будь-якому $a$", True),
        ],
        "hint": r"Обчисліть обидві частини другої рівності.",
        "solution": r"Основна властивість — для $a \ge 0$. $\sqrt[6]{64} = 2$, а $\sqrt[3]{-8} = -2$. Корінь непарного степеня — непарна функція ✓.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Знайдіть область визначення виразу $\sqrt[4]{x - 2} \cdot \sqrt[4]{x + 3}$.",
        "options": [(r"$[2;\,+\infty)$", True), (r"$(-\infty;\,-3] \cup [2;\,+\infty)$", False), (r"$[-3;\,2]$", False), (r"$[-3;\,+\infty)$", False)],
        "hint": r"Кожен корінь окремо має існувати.",
        "solution": r"$x - 2 \ge 0$ і $x + 3 \ge 0$: $x \ge 2$. Варіант Б — область визначення $\sqrt[4]{(x - 2)(x + 3)}$, вона ширша.",
    },
    {
        "type": "MULTI", "difficulty": 3, "skill": "ANALYZE",
        "text": r"При яких $x$ рівність $\sqrt{(x - 1)(x - 4)} = \sqrt{x - 1} \cdot \sqrt{x - 4}$ правильна?",
        "options": [(r"$x = 5$", True), (r"$x = 4$", True), (r"$x = 0$", False), (r"$x = 1$", False), (r"$x = 10$", True)],
        "hint": r"Права частина існує лише при $x - 1 \ge 0$ і $x - 4 \ge 0$.",
        "solution": r"Потрібно $x \ge 4$. При $x = 0$ ліва частина $= 2$, а $\sqrt{-1}$ не існує. При $x = 1$ не існує $\sqrt{-3}$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Скільки цілих $x$, при яких одночасно $\sqrt[4]{(x - 3)^4} = 3 - x$ і $\sqrt[6]{(x + 2)^6} = x + 2$?",
        "answer": "6",
        "hint": r"$|t| = -t \iff t \le 0$; $|t| = t \iff t \ge 0$.",
        "solution": r"$x - 3 \le 0$ і $x + 2 \ge 0$: $-2 \le x \le 3$ — цілі $-2, \ldots, 3$, їх $6$.",
    },

    # ==========================================
    # БОСИ — після опанування теми
    # ==========================================
    {
        "type": "SHORT", "difficulty": 4, "skill": "MODEL",
        "text": r"Сторона одного квадрата дорівнює $\sqrt[4]{12}$, іншого — $\sqrt[4]{3}$. У скільки разів площа першого квадрата більша?",
        "answer": "2",
        "solution": r"$\frac{S_1}{S_2} = \left(\frac{\sqrt[4]{12}}{\sqrt[4]{3}}\right)^2 = \left(\sqrt[4]{4}\right)^2 = \sqrt{4} = 2$.",
    },
    {
        "type": "FIELDS", "difficulty": 4, "skill": "MODEL",
        "text": r"Знайдіть значення виразу $\sqrt[4]{(a - 5)^4} + \sqrt[3]{(a - 1)^3}$.",
        "fields": [(r"при $a = 0$:", "4"), (r"при $a = 3$:", "4"), (r"при $a = 6$:", "6")],
        "solution": r"Вираз дорівнює $|a - 5| + a - 1$. При $a \le 5$: $5 - a + a - 1 = 4$ (стала!). При $a = 6$: $1 + 5 = 6$.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "SOLVE",
        "text": r"Обчисліть $\sqrt[3]{20 + 14\sqrt{2}} + \sqrt[3]{20 - 14\sqrt{2}}$.",
        "answer": "4",
        "solution": r"$\left(2 + \sqrt{2}\right)^3 = 8 + 12\sqrt{2} + 12 + 2\sqrt{2} = 20 + 14\sqrt{2}$, аналогічно $\left(2 - \sqrt{2}\right)^3 = 20 - 14\sqrt{2}$. Сума $(2 + \sqrt{2}) + (2 - \sqrt{2}) = 4$.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "SOLVE",
        "text": r"Обчисліть $\left(\sqrt[3]{9} - \sqrt[3]{6} + \sqrt[3]{4}\right)\left(\sqrt[3]{3} + \sqrt[3]{2}\right)$.",
        "answer": "5",
        "solution": r"Нехай $u = \sqrt[3]{3}$, $v = \sqrt[3]{2}$: $(u^2 - uv + v^2)(u + v) = u^3 + v^3 = 3 + 2 = 5$.",
    },
    {
        "type": "TF", "difficulty": 4, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [
            (r"$\sqrt[4]{\left(1 - \sqrt{2}\right)^4} = \sqrt{2} - 1$", True),
            (r"$\sqrt[3]{\left(1 - \sqrt{2}\right)^3} = 1 - \sqrt{2}$", True),
            (r"$\sqrt{\left(\sqrt{3} - 2\right)^2} = \sqrt{3} - 2$", False),
            (r"$\sqrt[6]{(\pi - 4)^6} = 4 - \pi$", True),
        ],
        "solution": r"$1 - \sqrt{2} \lt 0$: парний корінь дає $\sqrt{2} - 1$, непарний — саме число. $\sqrt{3} - 2 \lt 0$, тож $\sqrt{(\sqrt{3} - 2)^2} = 2 - \sqrt{3}$. $\pi - 4 \lt 0$: $|\pi - 4| = 4 - \pi$.",
    },

    # ==========================================
    # УЛЬТРА-БОСИ
    # ==========================================
    {
        "type": "SHORT", "difficulty": 5, "skill": "SOLVE",
        "text": r"Обчисліть $\sqrt{6 + 2\sqrt{5}} - \sqrt{6 - 2\sqrt{5}}$.",
        "answer": "2",
        "solution": r"$6 \pm 2\sqrt{5} = \left(\sqrt{5} \pm 1\right)^2$. Отже, $\left(\sqrt{5} + 1\right) - \left|\sqrt{5} - 1\right| = \sqrt{5} + 1 - \sqrt{5} + 1 = 2$.",
    },
    {
        "type": "SHORT", "difficulty": 5, "skill": "SOLVE",
        "text": r"Скільки цілих $x$ задовольняють рівність $\sqrt[6]{(x - 1)^6} + \sqrt[4]{(x - 5)^4} = 4$?",
        "answer": "5",
        "solution": r"Рівність має вигляд $|x - 1| + |x - 5| = 4$ — сума відстаней від $x$ до $1$ і до $5$. Вона дорівнює $4$ саме при $1 \le x \le 5$: цілі $1, 2, 3, 4, 5$.",
    },
]
