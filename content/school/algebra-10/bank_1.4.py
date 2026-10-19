TOPIC_NAME = "1.4. Степінь з раціональним показником та його властивості"
COURSE = "Алгебра і початки аналізу (10-11 класи)"
GRADE = "10 клас"

TASKS = [
    # ==========================================
    # СХОДИНКА 1 — БАЗОВИЙ
    # ==========================================
    # --- Моделювання ---
    {
        "type": "CHOICE", "difficulty": 1, "skill": "MODEL",
        "text": r"Чому дорівнює $a^{\frac{m}{n}}$ при $a \gt 0$?",
        "options": [(r"$\sqrt[n]{a^m}$", True), (r"$\sqrt[m]{a^n}$", False), (r"$\frac{a^m}{n}$", False), (r"$\left(\sqrt[m]{a}\right)^n$", False)],
        "hint": r"Знаменник показника — показник кореня.",
        "solution": r"За означенням $a^{\frac{m}{n}} = \sqrt[n]{a^m}$: знаменник — показник кореня, чисельник — степінь.",
    },
    {
        "type": "MATCH", "difficulty": 1, "skill": "MODEL",
        "text": r"Нехай $a \gt 0$. Установіть відповідність між степенем (1–3) та коренем (А–Д).",
        "options": [r"А) $\sqrt{a}$", r"Б) $\sqrt[3]{a^2}$", r"В) $\frac{1}{\sqrt{a}}$", r"Г) $\sqrt{a^3}$", r"Д) $-\sqrt{a}$"],
        "matches": [(r"1. $a^{\frac{1}{2}}$", r"А) $\sqrt{a}$"), (r"2. $a^{\frac{2}{3}}$", r"Б) $\sqrt[3]{a^2}$"), (r"3. $a^{-\frac{1}{2}}$", r"В) $\frac{1}{\sqrt{a}}$")],
        "hint": r"Від'ємний показник — обернене число, а не від'ємне.",
        "solution": r"$a^{\frac{1}{2}} = \sqrt{a}$; $a^{\frac{2}{3}} = \sqrt[3]{a^2}$; $a^{-\frac{1}{2}} = \frac{1}{a^{\frac{1}{2}}} = \frac{1}{\sqrt{a}}$.",
    },
    {
        "type": "GROUP", "difficulty": 1, "skill": "MODEL",
        "text": r"Чи має зміст вираз? Розподіліть.",
        "groups": ["Має зміст", "Не має змісту"],
        "items": [(r"$8^{\frac{1}{3}}$", 0), (r"$(-8)^{\frac{1}{3}}$", 1), (r"$0^{\frac{1}{2}}$", 0), (r"$0^{-\frac{1}{2}}$", 1), (r"$5^{-\frac{2}{3}}$", 0)],
        "hint": r"Основа степеня з дробовим показником — додатна; $0^r$ — лише при $r \gt 0$.",
        "solution": r"При $a \lt 0$ степінь з дробовим показником не означають; $0^{-\frac{1}{2}} = \frac{1}{0^{\frac{1}{2}}}$ — ділення на нуль.",
    },
    {
        "type": "TF", "difficulty": 1, "skill": "MODEL",
        "text": r"Правда чи ні?",
        "statements": [
            (r"$4^{-\frac{1}{2}} = -2$", False),
            (r"$a^{\frac{2}{6}} = a^{\frac{1}{3}}$ при $a \gt 0$", True),
            (r"$(-27)^{\frac{1}{3}} = -3$", False),
        ],
        "hint": r"Від'ємний показник і від'ємна основа — дві різні пастки.",
        "solution": r"$4^{-\frac{1}{2}} = \frac{1}{2}$. Значення не залежить від запису дробу ✓. $(-27)^{\frac{1}{3}}$ не означено, хоча $\sqrt[3]{-27} = -3$.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "MODEL",
        "text": r"Яким числом має бути $8^{\frac{1}{3}}$, щоб виконувалась рівність $\left(8^{\frac{1}{3}}\right)^3 = 8^{\frac{1}{3} \cdot 3} = 8$?",
        "options": [(r"$2$", True), (r"$\frac{8}{3}$", False), (r"$24$", False), (r"$\frac{1}{24}$", False)],
        "hint": r"Куб якого числа дорівнює $8$?",
        "solution": r"$8^{\frac{1}{3}}$ — число, куб якого $8$: $\sqrt[3]{8} = 2$.",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"Обчисліть $81^{\frac{1}{4}}$.",
        "answer": "3",
        "hint": r"$81 = 3^4$.",
        "solution": r"$\sqrt[4]{81} = 3$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"Обчисліть $32^{\frac{3}{5}}$.",
        "answer": "8",
        "hint": r"$32 = 2^5$.",
        "solution": r"$(2^5)^{\frac{3}{5}} = 2^3 = 8$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"Обчисліть $9^{-\frac{1}{2}}$. Відповідь запишіть дробом, наприклад 1/5.",
        "answer": "1/3",
        "hint": r"$a^{-r} = \frac{1}{a^r}$.",
        "solution": r"$\frac{1}{9^{\frac{1}{2}}} = \frac{1}{3}$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"Обчисліть $2^{\frac{1}{2}} \cdot 2^{\frac{3}{2}}$.",
        "answer": "4",
        "hint": r"При множенні показники додаються.",
        "solution": r"$2^{\frac{1}{2} + \frac{3}{2}} = 2^2 = 4$.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "SOLVE",
        "text": r"Запишіть $5^{\frac{2}{3}}$ у вигляді кореня.",
        "options": [(r"$\sqrt[3]{25}$", True), (r"$\sqrt{125}$", False), (r"$\frac{10}{3}$", False), (r"$\sqrt[3]{10}$", False)],
        "hint": r"$a^{\frac{m}{n}} = \sqrt[n]{a^m}$.",
        "solution": r"$\sqrt[3]{5^2} = \sqrt[3]{25}$. $\sqrt{125} = 5^{\frac{3}{2}}$ — переплутали чисельник і знаменник.",
    },
    # --- Аналіз результатів ---
    {
        "type": "ERROR", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Оля обчислювала $25^{-\frac{1}{2}}$. У якому кроці помилка?",
        "steps": [r"$25^{\frac{1}{2}} = \sqrt{25} = 5$", r"$25^{-\frac{1}{2}} = -5$", r"Відповідь: $-5$"],
        "wrong": 1,
        "hint": r"Що означає від'ємний показник?",
        "solution": r"$25^{-\frac{1}{2}} = \frac{1}{25^{\frac{1}{2}}} = \frac{1}{5}$.",
    },
    {
        "type": "MULTI", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Які рівності правильні при $a \gt 0$, $b \gt 0$?",
        "options": [(r"$a^{\frac{1}{3}} \cdot a^{\frac{2}{3}} = a$", True), (r"$\left(a^{\frac{1}{2}}\right)^4 = a^2$", True), (r"$a^{\frac{1}{2}} + a^{\frac{1}{2}} = a$", False),
                    (r"$a^{\frac{3}{4}} : a^{\frac{1}{4}} = a^{\frac{1}{2}}$", True), (r"$(a + b)^{\frac{1}{2}} = a^{\frac{1}{2}} + b^{\frac{1}{2}}$", False)],
        "hint": r"Властивості — для добутку, частки й степеня, а не для суми.",
        "solution": r"$a^{1}$, $a^{2}$, $a^{\frac{1}{2}}$ ✓. $a^{\frac{1}{2}} + a^{\frac{1}{2}} = 2a^{\frac{1}{2}}$. Степінь суми не дорівнює сумі степенів.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Петро записав $a^{\frac{3}{5}} = \sqrt[3]{a^5}$. Як правильно?",
        "options": [(r"$\sqrt[5]{a^3}$", True), (r"$\sqrt[3]{a^5}$", False), (r"$a^{\frac{5}{3}}$", False), (r"$\frac{3a}{5}$", False)],
        "hint": r"Знаменник — показник кореня.",
        "solution": r"$a^{\frac{3}{5}} = \sqrt[5]{a^3}$; $\sqrt[3]{a^5} = a^{\frac{5}{3}}$ — інше число.",
    },
    {
        "type": "TF", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [
            (r"$(ab)^{\frac{1}{2}} = a^{\frac{1}{2}} b^{\frac{1}{2}}$ при $a, b \gt 0$", True),
            (r"$0^{-1} = 0$", False),
            (r"$1^{\frac{2}{7}} = 1$", True),
        ],
        "hint": r"Чи можна ділити на нуль?",
        "solution": r"Властивість степеня добутку ✓. $0^{-1} = \frac{1}{0}$ — не існує. $\sqrt[7]{1} = 1$ ✓.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Порівняйте $4^{\frac{1}{2}}$ і $8^{\frac{1}{3}}$.",
        "options": [("Вони рівні", True), (r"$4^{\frac{1}{2}}$ більше", False), (r"$8^{\frac{1}{3}}$ більше", False), ("Порівняти неможливо", False)],
        "hint": r"Обчисліть обидва числа.",
        "solution": r"$4^{\frac{1}{2}} = 2$ і $8^{\frac{1}{3}} = 2$.",
    },

    # ==========================================
    # СХОДИНКА 2 — СЕРЕДНІЙ
    # ==========================================
    # --- Моделювання ---
    {
        "type": "FIELDS", "difficulty": 2, "skill": "MODEL",
        "text": r"Запишіть як степінь з основою $2$: впишіть показник (дробом, наприклад 1/3).",
        "fields": [(r"$\sqrt[3]{4} = 2^{r}$, $\;r =$", "2/3"), (r"$\frac{1}{\sqrt{8}} = 2^{s}$, $\;s =$", "-3/2")],
        "hint": r"$4 = 2^2$, $8 = 2^3$.",
        "solution": r"$\sqrt[3]{2^2} = 2^{\frac{2}{3}}$; $\frac{1}{(2^3)^{\frac{1}{2}}} = 2^{-\frac{3}{2}}$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "MODEL",
        "text": r"Нехай $a \gt 0$. Запишіть $\sqrt{a} \cdot \sqrt[4]{a}$ як $a^r$. Знайдіть $r$ (дробом, наприклад 2/5).",
        "answer": "3/4",
        "hint": r"$\sqrt{a} = a^{\frac{1}{2}}$, $\sqrt[4]{a} = a^{\frac{1}{4}}$.",
        "solution": r"$a^{\frac{1}{2} + \frac{1}{4}} = a^{\frac{3}{4}}$.",
    },
    {
        "type": "ORDER", "difficulty": 2, "skill": "MODEL",
        "text": r"Розташуйте числа від найменшого до найбільшого.",
        "items": [r"$8^{-\frac{1}{3}}$", r"$16^{\frac{1}{4}}$", r"$27^{\frac{2}{3}}$", r"$32^{0{,}8}$"],
        "hint": r"Обчисліть кожне число.",
        "solution": r"$\frac{1}{2} \lt 2 \lt 9 \lt 16$.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "MODEL",
        "text": r"Площа грані куба дорівнює $2$ см². Чому дорівнює об'єм куба?",
        "options": [(r"$2^{\frac{3}{2}}$ см³", True), (r"$2^{\frac{2}{3}}$ см³", False), (r"$2^3$ см³", False), (r"$2^{\frac{1}{6}}$ см³", False), (r"$6$ см³", False)],
        "hint": r"Ребро — $2^{\frac{1}{2}}$ см.",
        "solution": r"$V = \left(2^{\frac{1}{2}}\right)^3 = 2^{\frac{3}{2}} = 2\sqrt{2}$ см³.",
    },
    {
        "type": "MATCH", "difficulty": 2, "skill": "MODEL",
        "text": r"Нехай $a \gt 0$. Установіть відповідність між виразом (1–3) та степенем (А–Д).",
        "options": [r"А) $a^{\frac{5}{6}}$", r"Б) $a^{\frac{1}{2}}$", r"В) $a^{\frac{1}{3}}$", r"Г) $a^{\frac{1}{6}}$", r"Д) $a^{2}$"],
        "matches": [(r"1. $a^{\frac{1}{2}} \cdot a^{\frac{1}{3}}$", r"А) $a^{\frac{5}{6}}$"), (r"2. $\left(a^{\frac{2}{3}}\right)^{\frac{3}{4}}$", r"Б) $a^{\frac{1}{2}}$"),
                    (r"3. $a^{\frac{5}{6}} : a^{\frac{1}{2}}$", r"В) $a^{\frac{1}{3}}$")],
        "hint": r"Множення — додаємо показники, степінь степеня — множимо, ділення — віднімаємо.",
        "solution": r"1) $\frac{1}{2} + \frac{1}{3} = \frac{5}{6}$. 2) $\frac{2}{3} \cdot \frac{3}{4} = \frac{1}{2}$. 3) $\frac{5}{6} - \frac{1}{2} = \frac{1}{3}$.",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Обчисліть $125^{\frac{2}{3}} - 4^{1{,}5}$.",
        "answer": "17",
        "hint": r"$1{,}5 = \frac{3}{2}$.",
        "solution": r"$(5^3)^{\frac{2}{3}} = 25$; $(2^2)^{\frac{3}{2}} = 8$; $25 - 8 = 17$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Обчисліть $0{,}25^{-\frac{1}{2}}$.",
        "answer": "2",
        "hint": r"$0{,}25 = \frac{1}{4}$.",
        "solution": r"$\left(\frac{1}{4}\right)^{-\frac{1}{2}} = 4^{\frac{1}{2}} = 2$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Обчисліть $\left(3^{\frac{1}{2}} \cdot 3^{\frac{1}{3}} \cdot 3^{\frac{1}{6}}\right)^2$.",
        "answer": "9",
        "hint": r"Додайте показники.",
        "solution": r"$\frac{1}{2} + \frac{1}{3} + \frac{1}{6} = 1$; $(3^1)^2 = 9$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Обчисліть $49^{0{,}5} - 8^{-\frac{2}{3}}$.",
        "answer": "6.75",
        "hint": r"$8^{\frac{2}{3}} = 4$.",
        "solution": r"$7 - \frac{1}{4} = 6{,}75$.",
    },
    {
        "type": "FIELDS", "difficulty": 2, "skill": "SOLVE",
        "text": r"Нехай $a = 16$. Обчисліть:",
        "fields": [(r"$a^{\frac{3}{4}} =$", "8"), (r"$a^{-\frac{1}{4}} =$", "0.5")],
        "hint": r"$16^{\frac{1}{4}} = 2$.",
        "solution": r"$2^3 = 8$; $\frac{1}{2} = 0{,}5$.",
    },
    # --- Аналіз результатів ---
    {
        "type": "ERROR", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Максим обчислював $\left(4^{\frac{1}{2}} + 9^{\frac{1}{2}}\right)^2$. У якому кроці помилка?",
        "steps": [r"$\left(4^{\frac{1}{2}} + 9^{\frac{1}{2}}\right)^2 = \left(4^{\frac{1}{2}}\right)^2 + \left(9^{\frac{1}{2}}\right)^2$", r"$= 4 + 9$", r"$= 13$"],
        "wrong": 0,
        "hint": r"Квадрат суми — це не сума квадратів.",
        "solution": r"$(2 + 3)^2 = 25$. Загублено подвоєний добуток: $4 + 2 \cdot 6 + 9 = 25$.",
    },
    {
        "type": "TF", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [
            (r"$(-8)^{\frac{1}{3}} = -2$", False),
            (r"$8^{-\frac{1}{3}} = \frac{1}{2}$", True),
            (r"Вираз $(-8)^{\frac{2}{6}}$ має зміст", False),
        ],
        "hint": r"Чому основа має бути додатною?",
        "solution": r"Для $a \lt 0$ степінь з дробовим показником не означають: інакше $(-8)^{\frac{1}{3}} = -2$, а $(-8)^{\frac{2}{6}} = \sqrt[6]{64} = 2$. $8^{-\frac{1}{3}} = \frac{1}{2}$ ✓.",
    },
    {
        "type": "MULTI", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Які числа дорівнюють $\frac{1}{2}$?",
        "options": [(r"$4^{-\frac{1}{2}}$", True), (r"$8^{-\frac{1}{3}}$", True), (r"$16^{-\frac{1}{4}}$", True), (r"$(-8)^{-\frac{1}{3}}$", False), (r"$2^{-2}$", False)],
        "hint": r"Від'ємний показник — обернене число.",
        "solution": r"$\frac{1}{2}$, $\frac{1}{2}$, $\frac{1}{2}$ ✓. $(-8)^{-\frac{1}{3}}$ не означено; $2^{-2} = \frac{1}{4}$.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Порівняйте $3^{\frac{1}{2}}$ і $5^{\frac{1}{3}}$.",
        "options": [(r"$3^{\frac{1}{2}} \gt 5^{\frac{1}{3}}$", True), (r"$3^{\frac{1}{2}} \lt 5^{\frac{1}{3}}$", False), ("Вони рівні", False), ("Порівняти неможливо", False)],
        "hint": r"Обидва числа додатні — піднесіть до степеня $6$.",
        "solution": r"$\left(3^{\frac{1}{2}}\right)^6 = 27$, $\left(5^{\frac{1}{3}}\right)^6 = 25$; $27 \gt 25$.",
    },
    {
        "type": "GROUP", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Більше чи менше за $1$? Розподіліть.",
        "groups": [r"Більше за $1$", r"Менше за $1$"],
        "items": [(r"$2^{\frac{1}{3}}$", 0), (r"$0{,}5^{\frac{1}{2}}$", 1), (r"$3^{-\frac{1}{2}}$", 1), (r"$\left(\frac{1}{4}\right)^{-\frac{1}{2}}$", 0), (r"$5^{0{,}1}$", 0)],
        "hint": r"При $a \gt 1$: $a^r \gt 1$ для $r \gt 0$ і $a^r \lt 1$ для $r \lt 0$.",
        "solution": r"$2^{\frac{1}{3}}$, $5^{0{,}1}$ — більші за $1$; $\left(\frac{1}{4}\right)^{-\frac{1}{2}} = 2$. $0{,}5^{\frac{1}{2}} \approx 0{,}71$, $3^{-\frac{1}{2}} = \frac{1}{\sqrt{3}}$ — менші.",
    },

    # ==========================================
    # СХОДИНКА 3 — СКЛАДНИЙ
    # ==========================================
    # --- Моделювання ---
    {
        "type": "FIELDS", "difficulty": 3, "skill": "MODEL",
        "text": r"Знайдіть значення виразів при $x = 10$.",
        "fields": [(r"$\left(x^{\frac{1}{2}} + 1\right)\left(x^{\frac{1}{2}} - 1\right) =$", "9"), (r"$\left(x^{\frac{1}{2}} + 1\right)^2 - 2x^{\frac{1}{2}} =$", "11")],
        "hint": r"Спершу спростіть: різниця квадратів і квадрат суми.",
        "solution": r"$x - 1 = 9$; $\;x + 2x^{\frac{1}{2}} + 1 - 2x^{\frac{1}{2}} = x + 1 = 11$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"Кількість бактерій через $t$ год — $N = 100 \cdot 4^{\frac{t}{2}}$. Скільки бактерій буде через $3$ год?",
        "answer": "800",
        "hint": r"$4^{1{,}5} = (2^2)^{\frac{3}{2}}$.",
        "solution": r"$N = 100 \cdot 4^{\frac{3}{2}} = 100 \cdot 8 = 800$.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "MODEL",
        "text": r"Скоротіть дріб $\frac{a - 4b}{a^{\frac{1}{2}} - 2b^{\frac{1}{2}}}$ ($a, b \gt 0$, $a \ne 4b$).",
        "options": [(r"$a^{\frac{1}{2}} + 2b^{\frac{1}{2}}$", True), (r"$a^{\frac{1}{2}} - 2b^{\frac{1}{2}}$", False), (r"$a^{\frac{1}{2}} + b^{\frac{1}{2}}$", False), (r"$a + 2b$", False), (r"$1$", False)],
        "hint": r"$a - 4b = \left(a^{\frac{1}{2}}\right)^2 - \left(2b^{\frac{1}{2}}\right)^2$.",
        "solution": r"$\frac{\left(a^{\frac{1}{2}} - 2b^{\frac{1}{2}}\right)\left(a^{\frac{1}{2}} + 2b^{\frac{1}{2}}\right)}{a^{\frac{1}{2}} - 2b^{\frac{1}{2}}} = a^{\frac{1}{2}} + 2b^{\frac{1}{2}}$.",
    },
    {
        "type": "MATCH", "difficulty": 3, "skill": "MODEL",
        "text": r"Установіть відповідність між виразом (1–3) та його значенням (А–Д).",
        "options": [r"А) $4$", r"Б) $\frac{1}{8}$", r"В) $32$", r"Г) $8$", r"Д) $-8$"],
        "matches": [(r"1. $64^{\frac{1}{3}}$", r"А) $4$"), (r"2. $64^{-\frac{1}{2}}$", r"Б) $\frac{1}{8}$"), (r"3. $64^{\frac{5}{6}}$", r"В) $32$")],
        "hint": r"$64 = 2^6$.",
        "solution": r"$2^{2} = 4$; $2^{-3} = \frac{1}{8}$; $2^{5} = 32$.",
    },
    {
        "type": "ORDER", "difficulty": 3, "skill": "MODEL",
        "text": r"Розташуйте кроки обчислення $16^{-0{,}75}$.",
        "items": [r"$-0{,}75 = -\frac{3}{4}$", r"$16 = 2^4$", r"$\left(2^4\right)^{-\frac{3}{4}} = 2^{-3}$", r"$= \frac{1}{8}$"],
        "hint": r"Десятковий показник → звичайний дріб → основа як степінь.",
        "solution": r"$16^{-0{,}75} = \frac{1}{8}$.",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Нехай $a \gt 0$, $\left(a^{\frac{1}{3}} \cdot a^{\frac{1}{4}}\right)^{12} : a^6 = a^r$. Знайдіть $r$.",
        "answer": "1",
        "hint": r"$\left(\frac{1}{3} + \frac{1}{4}\right) \cdot 12$.",
        "solution": r"$a^{\frac{7}{12} \cdot 12} : a^6 = a^{7 - 6} = a^1$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Обчисліть $\left(\sqrt[3]{2} \cdot \sqrt[6]{2}\right)^4$.",
        "answer": "4",
        "hint": r"Запишіть корені як степені.",
        "solution": r"$2^{\left(\frac{1}{3} + \frac{1}{6}\right) \cdot 4} = 2^{\frac{1}{2} \cdot 4} = 4$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Знайдіть значення виразу $\frac{x^{\frac{1}{2}} - y^{\frac{1}{2}}}{x - y} \cdot \left(x^{\frac{1}{2}} + y^{\frac{1}{2}}\right)$ при $x = 7$, $y = 3$.",
        "answer": "1",
        "hint": r"$x - y = \left(x^{\frac{1}{2}} - y^{\frac{1}{2}}\right)\left(x^{\frac{1}{2}} + y^{\frac{1}{2}}\right)$.",
        "solution": r"Після скорочення вираз дорівнює $1$ при будь-яких $x, y \gt 0$, $x \ne y$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Обчисліть $81^{0{,}25} \cdot 9^{-1{,}5} \cdot 27^{\frac{2}{3}}$.",
        "answer": "1",
        "hint": r"Запишіть усе як степені числа $3$.",
        "solution": r"$3^{1} \cdot 3^{-3} \cdot 3^{2} = 3^{0} = 1$.",
    },
    {
        "type": "FIELDS", "difficulty": 3, "skill": "SOLVE",
        "text": r"Відомо, що $a^{\frac{1}{2}} = 3$. Знайдіть:",
        "fields": [("$a =$", "9"), (r"$a^{-\frac{3}{2}} =$ (дробом)", "1/27")],
        "hint": r"$a^{\frac{3}{2}} = \left(a^{\frac{1}{2}}\right)^3$.",
        "solution": r"$a = 3^2 = 9$; $a^{-\frac{3}{2}} = \frac{1}{3^3} = \frac{1}{27}$.",
    },
    # --- Аналіз результатів ---
    {
        "type": "ERROR", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Ярина спрощувала $\left(a^{\frac{3}{2}}\right)^{\frac{2}{3}} \cdot a^{\frac{1}{2}}$. У якому кроці помилка?",
        "steps": [r"$\left(a^{\frac{3}{2}}\right)^{\frac{2}{3}} = a^{\frac{3}{2} + \frac{2}{3}} = a^{\frac{13}{6}}$", r"$a^{\frac{13}{6}} \cdot a^{\frac{1}{2}} = a^{\frac{16}{6}}$", r"$= a^{\frac{8}{3}}$"],
        "wrong": 0,
        "hint": r"Степінь степеня — показники множать.",
        "solution": r"$\left(a^{\frac{3}{2}}\right)^{\frac{2}{3}} = a^{1}$, тож вираз дорівнює $a^{\frac{3}{2}}$.",
    },
    {
        "type": "TF", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Нехай $a \gt 0$, $r$ і $s$ — раціональні. Правда чи ні?",
        "statements": [
            (r"$a^r + a^s = a^{r + s}$", False),
            (r"Якщо $a \gt 1$ і $r \gt s$, то $a^r \gt a^s$", True),
            (r"Якщо $0 \lt a \lt 1$ і $r \gt s$, то $a^r \gt a^s$", False),
        ],
        "hint": r"Перевірте на $a = 4$ та $a = \frac{1}{4}$ при $r = \frac{1}{2}$, $s = 0$.",
        "solution": r"$4^{\frac{1}{2}} + 4^{0} = 3 \ne 4^{\frac{1}{2}}$. $4^{\frac{1}{2}} = 2 \gt 4^0 = 1$, а $\left(\frac{1}{4}\right)^{\frac{1}{2}} = \frac{1}{2} \lt 1$: для основи між $0$ і $1$ — навпаки.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Знайдіть область визначення виразу $(x - 2)^{\frac{1}{3}}$.",
        "options": [(r"$[2;\,+\infty)$", True), (r"$(2;\,+\infty)$", False), (r"$\mathbb{R}$", False), (r"$(-\infty;\,2]$", False)],
        "hint": r"Основа — невід'ємна; $0^r$ має зміст при $r \gt 0$.",
        "solution": r"Потрібно $x - 2 \gt 0$ або $x - 2 = 0$ (бо $\frac{1}{3} \gt 0$): $x \ge 2$. $\mathbb{R}$ — це для $\sqrt[3]{x - 2}$, а не для степеня.",
    },
    {
        "type": "MULTI", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Які вирази мають зміст при $x = -1$?",
        "options": [(r"$(x + 2)^{\frac{1}{2}}$", True), (r"$(x + 1)^{\frac{1}{3}}$", True), (r"$(x + 1)^{-\frac{1}{2}}$", False), (r"$x^{\frac{2}{3}}$", False), (r"$\left(x^2\right)^{\frac{1}{3}}$", True)],
        "hint": r"Обчисліть основу кожного степеня.",
        "solution": r"Основи: $1$, $0$ (показник додатний), $0$ (показник від'ємний — ні), $-1$ (від'ємна — ні), $1$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Скільки цілих $x$ з проміжку $[-5;\,5]$, при яких вираз $(x + 3)^{\frac{1}{2}} + (2 - x)^{-\frac{1}{4}}$ має зміст?",
        "answer": "5",
        "hint": r"$x + 3 \ge 0$ і $2 - x \gt 0$.",
        "solution": r"$-3 \le x \lt 2$: $x = -3, -2, -1, 0, 1$.",
    },

    # ==========================================
    # БОСИ — після опанування теми
    # ==========================================
    {
        "type": "SHORT", "difficulty": 4, "skill": "MODEL",
        "text": r"Кількість бактерій через $t$ год — $N = 100 \cdot 2^{\frac{t}{3}}$. Через скільки годин їх стане $1600$?",
        "answer": "12",
        "solution": r"$2^{\frac{t}{3}} = 16 = 2^4 \Rightarrow \frac{t}{3} = 4$, $t = 12$ год.",
    },
    {
        "type": "FIELDS", "difficulty": 4, "skill": "MODEL",
        "text": r"Об'єм куба $4$ см³. Запишіть ребро і площу грані як степені числа $2$: впишіть показники (дробом).",
        "fields": [(r"Ребро $= 2^{r}$ см, $\;r =$", "2/3"), (r"Площа грані $= 2^{s}$ см², $\;s =$", "4/3")],
        "solution": r"Ребро $4^{\frac{1}{3}} = (2^2)^{\frac{1}{3}} = 2^{\frac{2}{3}}$; площа грані $\left(2^{\frac{2}{3}}\right)^2 = 2^{\frac{4}{3}}$.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "SOLVE",
        "text": r"Спростіть $\frac{\left(a^{\frac{1}{2}} + b^{\frac{1}{2}}\right)^2 - \left(a^{\frac{1}{2}} - b^{\frac{1}{2}}\right)^2}{(ab)^{\frac{1}{2}}}$ ($a, b \gt 0$).",
        "answer": "4",
        "solution": r"Чисельник: $\left(a + 2(ab)^{\frac{1}{2}} + b\right) - \left(a - 2(ab)^{\frac{1}{2}} + b\right) = 4(ab)^{\frac{1}{2}}$. Ділимо: $4$.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "SOLVE",
        "text": r"Знайдіть значення виразу $\frac{x - 1}{x^{\frac{2}{3}} + x^{\frac{1}{3}} + 1} + 1$ при $x = 27$.",
        "answer": "3",
        "solution": r"$x - 1 = \left(x^{\frac{1}{3}}\right)^3 - 1 = \left(x^{\frac{1}{3}} - 1\right)\left(x^{\frac{2}{3}} + x^{\frac{1}{3}} + 1\right)$. Вираз дорівнює $x^{\frac{1}{3}} - 1 + 1 = x^{\frac{1}{3}} = 3$.",
    },
    {
        "type": "TF", "difficulty": 4, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [
            (r"$\left(a^2\right)^{\frac{1}{2}} = a$ при $a \gt 0$", True),
            (r"$\left((-2)^2\right)^{\frac{1}{2}} = -2$", False),
            (r"$2^{\frac{1}{2}} \cdot 2^{\frac{1}{3}} = 2^{\frac{5}{6}}$", True),
            (r"$\left(\frac{1}{9}\right)^{-\frac{1}{2}} = 3$", True),
        ],
        "solution": r"Властивість $(a^r)^s = a^{rs}$ — лише для $a \gt 0$: $\left((-2)^2\right)^{\frac{1}{2}} = 4^{\frac{1}{2}} = 2$. $\frac{1}{2} + \frac{1}{3} = \frac{5}{6}$ ✓. $9^{\frac{1}{2}} = 3$ ✓.",
    },

    # ==========================================
    # УЛЬТРА-БОСИ
    # ==========================================
    {
        "type": "SHORT", "difficulty": 5, "skill": "SOLVE",
        "text": r"Знайдіть $x$, якщо $4^x = 8^{\frac{1}{3}} \cdot 2^{\frac{1}{2}}$.",
        "answer": "0.75",
        "solution": r"Праворуч $2^{1} \cdot 2^{\frac{1}{2}} = 2^{\frac{3}{2}}$, ліворуч $2^{2x}$. Отже, $2x = \frac{3}{2}$, $x = 0{,}75$.",
    },
    {
        "type": "SHORT", "difficulty": 5, "skill": "SOLVE",
        "text": r"Відомо, що $a \gt 0$ і $a + a^{-1} = 7$. Знайдіть $\left(a^{\frac{1}{2}} + a^{-\frac{1}{2}}\right)^2$.",
        "answer": "9",
        "solution": r"$\left(a^{\frac{1}{2}} + a^{-\frac{1}{2}}\right)^2 = a + 2a^{\frac{1}{2}}a^{-\frac{1}{2}} + a^{-1} = a + a^{-1} + 2 = 9$.",
    },
]
