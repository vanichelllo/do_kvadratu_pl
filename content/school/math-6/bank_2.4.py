TOPIC_NAME = "2.4. Множення дробів"
COURSE = "Математика (5-6 класи)"
GRADE = "6 клас"

TASKS = [
    # ==========================================
    # СХОДИНКА 1 — БАЗОВИЙ
    # ==========================================
    # --- Моделювання ---
    {
        "type": "CHOICE", "difficulty": 1, "skill": "MODEL",
        "text": r"Як помножити дріб $\frac{a}{b}$ на дріб $\frac{c}{d}$?",
        "options": [(r"$\frac{a \cdot c}{b \cdot d}$", True), (r"$\frac{a + c}{b + d}$", False), (r"$\frac{a \cdot d}{b \cdot c}$", False), (r"Спершу звести до спільного знаменника", False)],
        "hint": r"Чисельник — на чисельник, знаменник — на знаменник.",
        "solution": r"$\frac{a}{b} \cdot \frac{c}{d} = \frac{ac}{bd}$. Спільний знаменник не потрібен.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "MODEL",
        "text": r"Оля дала Тарасу $\frac{3}{4}$ плитки шоколаду, і він з'їв $\frac{2}{3}$ від неї. Яку частину всієї плитки з'їв Тарас? Відповідь запиши нескоротним дробом.",
        "answer": "1/2",
        "hint": r"«$\frac{2}{3}$ від $\frac{3}{4}$» — це $\frac{2}{3} \cdot \frac{3}{4}$.",
        "solution": r"$\frac{2 \cdot 3}{3 \cdot 4} = \frac{6}{12} = \frac{1}{2}$.",
    },
    {
        "type": "TF", "difficulty": 1, "skill": "MODEL",
        "text": r"Правда чи ні?",
        "statements": [
            (r"$\frac{1}{2} \cdot \frac{1}{3} = \frac{1}{6}$", True),
            (r"$\frac{2}{5} \cdot \frac{1}{2} = \frac{3}{7}$", False),
            (r"$\frac{3}{4} \cdot 2 = \frac{3}{2}$", True),
        ],
        "hint": r"Множимо, а не додаємо.",
        "solution": r"$\frac{1}{6}$ ✓; $\frac{2}{10} = \frac{1}{5}$, а не $\frac{3}{7}$; $\frac{6}{4} = \frac{3}{2}$ ✓.",
    },
    {
        "type": "GROUP", "difficulty": 1, "skill": "MODEL",
        "text": r"Розподіли добутки за значенням.",
        "groups": [r"Дорівнює $\frac{1}{4}$", r"Дорівнює $\frac{1}{3}$"],
        "items": [(r"$\frac{1}{2} \cdot \frac{1}{2}$", 0), (r"$\frac{2}{3} \cdot \frac{1}{2}$", 1), (r"$\frac{3}{4} \cdot \frac{1}{3}$", 0), (r"$\frac{1}{6} \cdot 2$", 1), (r"$\frac{1}{8} \cdot 2$", 0)],
        "hint": r"Обчисли й скороти.",
        "solution": r"$\frac{1}{4}$, $\frac{3}{12}$, $\frac{2}{8}$ — це $\frac{1}{4}$; $\frac{2}{6}$, $\frac{2}{6}$ — це $\frac{1}{3}$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "MODEL",
        "text": r"Пляшка вміщує $\frac{3}{4}$ л. Скільки літрів у $4$ таких пляшках?",
        "answer": "3",
        "hint": r"$\frac{3}{4} \cdot 4$.",
        "solution": r"$\frac{3 \cdot 4}{4} = 3$ л.",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"Обчисли: $\frac{2}{5} \cdot \frac{3}{7}$. Відповідь запиши дробом.",
        "answer": "6/35",
        "hint": r"$2 \cdot 3$ і $5 \cdot 7$.",
        "solution": r"$\frac{6}{35}$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"Обчисли: $\frac{3}{8} \cdot 4$. Відповідь запиши нескоротним дробом.",
        "answer": "3/2",
        "hint": r"Помнож чисельник на $4$ і скороти.",
        "solution": r"$\frac{12}{8} = \frac{3}{2} = 1\frac{1}{2}$.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "SOLVE",
        "text": r"Обчисли: $\frac{5}{6} \cdot \frac{3}{5}$.",
        "options": [(r"$\frac{1}{2}$", True), (r"$\frac{8}{11}$", False), (r"$\frac{15}{11}$", False), (r"$\frac{3}{6}$ і далі не скорочується", False)],
        "hint": r"Скороти $5$ і $5$, $3$ і $6$.",
        "solution": r"$\frac{5 \cdot 3}{6 \cdot 5} = \frac{1}{2}$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"Обчисли: $\frac{2}{3} \cdot 9$.",
        "answer": "6",
        "hint": r"$\frac{2 \cdot 9}{3}$.",
        "solution": r"$\frac{18}{3} = 6$.",
    },
    {
        "type": "FIELDS", "difficulty": 1, "skill": "SOLVE",
        "text": r"Обчисли. Відповіді запиши нескоротними дробами.",
        "fields": [(r"$\frac{1}{4} \cdot \frac{2}{3} =$", "1/6"), (r"$\frac{4}{5} \cdot \frac{5}{8} =$", "1/2")],
        "hint": r"Скорочуй навхрест.",
        "solution": r"$\frac{2}{12} = \frac{1}{6}$; $\frac{20}{40} = \frac{1}{2}$.",
    },
    # --- Аналіз ---
    {
        "type": "ERROR", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Петро множив $\frac{1}{2} \cdot \frac{1}{3}$. У якому кроці помилка?",
        "steps": [r"Спільний знаменник $6$: $\frac{3}{6} \cdot \frac{2}{6}$", r"$= \frac{3 \cdot 2}{6}$", r"$= 1$"],
        "wrong": 1,
        "hint": r"Знаменники теж треба перемножити.",
        "solution": r"Спільний знаменник не потрібен: $\frac{1}{2} \cdot \frac{1}{3} = \frac{1}{6}$. У Петра загубилося множення знаменників.",
    },
    {
        "type": "MULTI", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Які добутки менші за $\frac{1}{2}$?",
        "options": [(r"$\frac{1}{2} \cdot \frac{3}{4}$", True), (r"$\frac{1}{2} \cdot \frac{1}{2}$", True), (r"$\frac{1}{2} \cdot 3$", False), (r"$\frac{2}{3} \cdot \frac{3}{4}$", False)],
        "hint": r"Множення на правильний дріб зменшує число.",
        "solution": r"$\frac{3}{8}$ і $\frac{1}{4}$ — менші. $\frac{3}{2}$ більший, $\frac{6}{12} = \frac{1}{2}$ — дорівнює.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Що станеться з числом $10$, якщо помножити його на $\frac{3}{5}$?",
        "options": [("Зменшиться", True), ("Збільшиться", False), ("Не зміниться", False), ("Стане дробом, більшим за 10", False)],
        "hint": r"$\frac{3}{5} \lt 1$.",
        "solution": r"$10 \cdot \frac{3}{5} = 6 \lt 10$. Множення на правильний дріб зменшує число.",
    },
    {
        "type": "TF", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [
            (r"$\frac{2}{3}$ від $15$ — це $\frac{2}{3} \cdot 15$", True),
            (r"$\frac{a}{b} \cdot \frac{b}{a} = 1$", True),
            (r"Добуток двох правильних дробів — неправильний дріб", False),
        ],
        "hint": r"Спробуй $\frac{1}{2} \cdot \frac{1}{2}$.",
        "solution": r"Дріб від числа — множення ✓. $\frac{ab}{ba} = 1$ ✓. $\frac{1}{2} \cdot \frac{1}{2} = \frac{1}{4}$ — правильний.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Що більше: $\frac{3}{4} \cdot \frac{4}{5}$ чи $\frac{3}{4}$?",
        "options": [(r"$\frac{3}{4}$", True), (r"$\frac{3}{4} \cdot \frac{4}{5}$", False), ("Порівну", False), ("Порівняти неможливо", False)],
        "hint": r"Множимо на дріб, менший за $1$.",
        "solution": r"$\frac{3}{4} \cdot \frac{4}{5} = \frac{3}{5} \lt \frac{3}{4}$.",
    },

    # ==========================================
    # СХОДИНКА 2 — СЕРЕДНІЙ
    # ==========================================
    # --- Моделювання ---
    {
        "type": "SHORT", "difficulty": 2, "skill": "MODEL",
        "text": r"Прямокутник має сторони $\frac{3}{5}$ м і $\frac{5}{6}$ м. Знайди його площу (у м²). Відповідь запиши нескоротним дробом.",
        "answer": "1/2",
        "hint": r"Площа — добуток сторін.",
        "solution": r"$\frac{3 \cdot 5}{5 \cdot 6} = \frac{1}{2}$ м².",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "MODEL",
        "text": r"Велосипедист їде зі швидкістю $12$ км/год. Скільки кілометрів він проїде за $\frac{3}{4}$ год?",
        "answer": "9",
        "hint": r"Шлях = швидкість · час.",
        "solution": r"$12 \cdot \frac{3}{4} = 9$ км.",
    },
    {
        "type": "FIELDS", "difficulty": 2, "skill": "MODEL",
        "text": r"Кілограм цукерок коштує $160$ грн. Скільки коштує:",
        "fields": [(r"$\frac{3}{8}$ кг, грн:", "60"), (r"$1\frac{1}{4}$ кг, грн:", "200")],
        "hint": r"Ціна · маса.",
        "solution": r"$160 \cdot \frac{3}{8} = 60$; $160 \cdot \frac{5}{4} = 200$ грн.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "MODEL",
        "text": r"У класі $\frac{4}{7}$ учнів — дівчата, і $\frac{3}{4}$ з них займаються танцями. Яка частина всього класу — дівчата-танцівниці?",
        "options": [(r"$\frac{3}{7}$", True), (r"$\frac{7}{11}$", False), (r"$\frac{12}{11}$", False), (r"$\frac{1}{7}$", False)],
        "hint": r"Знайди $\frac{3}{4}$ від $\frac{4}{7}$ — це добуток.",
        "solution": r"$\frac{3}{4} \cdot \frac{4}{7} = \frac{3}{7}$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "MODEL",
        "text": r"Сторона квадрата — $\frac{2}{3}$ дм. Знайди його площу (у дм²). Відповідь запиши дробом.",
        "answer": "4/9",
        "hint": r"Площа квадрата — сторона на сторону.",
        "solution": r"$\frac{2}{3} \cdot \frac{2}{3} = \frac{4}{9}$ дм².",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Обчисли: $\frac{4}{9} \cdot \frac{15}{16}$. Відповідь запиши нескоротним дробом.",
        "answer": "5/12",
        "hint": r"Скорочуй навхрест: $4$ і $16$, $15$ і $9$.",
        "solution": r"Скорочуємо $4$ і $16$, $15$ і $9$: $\frac{1 \cdot 5}{3 \cdot 4} = \frac{5}{12}$.",
    },
    {
        "type": "FIELDS", "difficulty": 2, "skill": "SOLVE",
        "text": r"Обчисли $2\frac{1}{3} \cdot 1\frac{1}{2}$ і запиши мішаним числом.",
        "fields": [("ціла частина:", "3"), ("чисельник дробової частини:", "1"), ("знаменник:", "2")],
        "hint": r"Спершу — неправильні дроби: $\frac{7}{3}$ і $\frac{3}{2}$.",
        "solution": r"$\frac{7}{3} \cdot \frac{3}{2} = \frac{7}{2} = 3\frac{1}{2}$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Обчисли: $1\frac{1}{2} \cdot 2\frac{2}{3}$.",
        "answer": "4",
        "hint": r"$1\frac{1}{2} = \frac{3}{2}$, $2\frac{2}{3} = \frac{8}{3}$.",
        "solution": r"$\frac{3}{2} \cdot \frac{8}{3} = \frac{8}{2} = 4$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Обчисли: $\frac{5}{6} \cdot \frac{9}{10}$. Відповідь запиши нескоротним дробом.",
        "answer": "3/4",
        "hint": r"Скороти $5$ і $10$, $9$ і $6$.",
        "solution": r"$\frac{5 \cdot 9}{6 \cdot 10} = \frac{1 \cdot 3}{2 \cdot 2} = \frac{3}{4}$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Обчисли: $\frac{7}{12} \cdot 18$. Відповідь запиши нескоротним дробом.",
        "answer": "21/2",
        "hint": r"$18$ і $12$ скорочуються на $6$.",
        "solution": r"$\frac{7 \cdot 18}{12} = \frac{7 \cdot 3}{2} = \frac{21}{2} = 10\frac{1}{2}$.",
    },
    # --- Аналіз ---
    {
        "type": "ERROR", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Оля множила $2\frac{1}{3} \cdot 3$. У якому кроці помилка?",
        "steps": [r"Ціла частина: $2 \cdot 3 = 6$", r"Дробова частина лишається $\frac{1}{3}$", r"Відповідь: $6\frac{1}{3}$"],
        "wrong": 1,
        "hint": r"Чи множать дробову частину?",
        "solution": r"Дробову частину теж множимо: $\frac{1}{3} \cdot 3 = 1$. Відповідь $7$.",
    },
    {
        "type": "TF", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [
            (r"$\frac{2}{3} \cdot \frac{3}{4} = \frac{3}{4} \cdot \frac{2}{3}$", True),
            (r"$1\frac{1}{2} \cdot 1\frac{1}{2} = 1\frac{1}{4}$", False),
            (r"$\left(\frac{1}{2}\right)^3 = \frac{1}{8}$", True),
            (r"$\frac{5}{8} \cdot 0 = 0$", True),
        ],
        "hint": r"Перевір кожну рівність обчисленням.",
        "solution": r"Переставна властивість ✓. $\frac{3}{2} \cdot \frac{3}{2} = \frac{9}{4} = 2\frac{1}{4}$. $\frac{1}{2} \cdot \frac{1}{2} \cdot \frac{1}{2} = \frac{1}{8}$ ✓. Будь-що на $0$ — $0$ ✓.",
    },
    {
        "type": "MULTI", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Які добутки дорівнюють $1$?",
        "options": [(r"$\frac{3}{4} \cdot \frac{4}{3}$", True), (r"$2\frac{1}{2} \cdot \frac{2}{5}$", True), (r"$\frac{5}{6} \cdot \frac{6}{7}$", False), (r"$1\frac{1}{3} \cdot \frac{3}{4}$", True), (r"$\frac{1}{2} \cdot 2\frac{1}{2}$", False)],
        "hint": r"Число, помножене на обернене, дає $1$.",
        "solution": r"$1$; $\frac{5}{2} \cdot \frac{2}{5} = 1$; $\frac{5}{7}$; $\frac{4}{3} \cdot \frac{3}{4} = 1$; $\frac{5}{4}$.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Яке число треба помножити на $\frac{3}{8}$, щоб отримати $1$?",
        "options": [(r"$\frac{8}{3}$", True), (r"$\frac{3}{8}$", False), (r"$\frac{5}{8}$", False), (r"$8$", False)],
        "hint": r"Переверни дріб.",
        "solution": r"$\frac{3}{8} \cdot \frac{8}{3} = 1$ — це обернене число.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "ANALYZE",
        "text": r"У скільки разів $\frac{3}{4}$ від числа $48$ більше за $\frac{1}{4}$ від того самого числа?",
        "answer": "3",
        "hint": r"Порівняй $\frac{3}{4}$ і $\frac{1}{4}$.",
        "solution": r"$36 : 12 = 3$ — бо $\frac{3}{4}$ утричі більше за $\frac{1}{4}$.",
    },

    # ==========================================
    # СХОДИНКА 3 — ВИСОКИЙ
    # ==========================================
    # --- Моделювання ---
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"Сад займає $\frac{5}{8}$ ділянки, а $\frac{2}{5}$ саду — яблуні. Яка частина ділянки під яблунями? Відповідь запиши нескоротним дробом.",
        "answer": "1/4",
        "hint": r"$\frac{2}{5}$ від $\frac{5}{8}$ — це добуток.",
        "solution": r"$\frac{2}{5} \cdot \frac{5}{8} = \frac{2}{8} = \frac{1}{4}$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"Прямокутний паралелепіпед має виміри $\frac{1}{2}$ м, $\frac{2}{3}$ м і $\frac{3}{4}$ м. Знайди його об'єм (у м³). Відповідь запиши нескоротним дробом.",
        "answer": "1/4",
        "hint": r"Об'єм — добуток трьох вимірів.",
        "solution": r"$\frac{1 \cdot 2 \cdot 3}{2 \cdot 3 \cdot 4} = \frac{6}{24} = \frac{1}{4}$ м³.",
    },
    {
        "type": "FIELDS", "difficulty": 3, "skill": "MODEL",
        "text": r"Пішохід ішов $1\frac{1}{2}$ год зі швидкістю $4\frac{2}{3}$ км/год, а потім $\frac{3}{4}$ год зі швидкістю $4$ км/год.",
        "fields": [("перша частина шляху, км:", "7"), ("весь шлях, км:", "10")],
        "hint": r"Шлях = швидкість · час для кожної частини.",
        "solution": r"$\frac{3}{2} \cdot \frac{14}{3} = 7$ км; $\frac{3}{4} \cdot 4 = 3$ км; разом $10$ км.",
    },
    {
        "type": "ORDER", "difficulty": 3, "skill": "MODEL",
        "text": r"Розташуй значення від найменшого до найбільшого.",
        "items": [r"$\frac{1}{3} \cdot \frac{3}{4}$", r"$\frac{2}{3} \cdot \frac{3}{4}$", r"$\frac{3}{4} \cdot 1$", r"$\frac{3}{4} \cdot \frac{4}{3}$"],
        "hint": r"Обчисли кожен добуток.",
        "solution": r"$\frac{1}{4} \lt \frac{1}{2} \lt \frac{3}{4} \lt 1$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"Ціна товару $240$ грн. Спочатку її знизили до $\frac{5}{6}$ ціни, потім нову ціну — до $\frac{9}{10}$. Яка остаточна ціна (у грн)?",
        "answer": "180",
        "hint": r"Зниження множаться одне за одним.",
        "solution": r"$240 \cdot \frac{5}{6} \cdot \frac{9}{10} = 240 \cdot \frac{3}{4} = 180$ грн.",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Обчисли: $\frac{14}{15} \cdot \frac{25}{28} \cdot \frac{9}{10}$. Відповідь запиши нескоротним дробом.",
        "answer": "3/4",
        "hint": r"Скорочуй навхрест кожну пару.",
        "solution": r"Скорочуємо: $14$ і $28$ — на $14$, $25$ і $10$ — на $5$, $9$ і $15$ — на $3$: $\frac{1 \cdot 5 \cdot 3}{5 \cdot 2 \cdot 2}$, ще раз на $5$: $\frac{3}{4}$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Обчисли: $3\frac{3}{4} \cdot 2\frac{2}{5}$.",
        "answer": "9",
        "hint": r"$3\frac{3}{4} = \frac{15}{4}$, $2\frac{2}{5} = \frac{12}{5}$.",
        "solution": r"$\frac{15}{4} \cdot \frac{12}{5} = \frac{3 \cdot 3}{1 \cdot 1} = 9$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Обчисли: $\left(\frac{2}{3}\right)^2 \cdot 2\frac{1}{4}$.",
        "answer": "1",
        "hint": r"$\left(\frac{2}{3}\right)^2 = \frac{4}{9}$, $2\frac{1}{4} = \frac{9}{4}$.",
        "solution": r"$\frac{4}{9} \cdot \frac{9}{4} = 1$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Обчисли зручним способом: $\frac{5}{7} \cdot 13 + \frac{5}{7} \cdot 8$.",
        "answer": "15",
        "hint": r"Винеси спільний множник $\frac{5}{7}$.",
        "solution": r"$\frac{5}{7} \cdot (13 + 8) = \frac{5}{7} \cdot 21 = 15$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Обчисли: $1\frac{1}{2} \cdot 1\frac{1}{3} \cdot 1\frac{1}{4} \cdot 1\frac{1}{5}$.",
        "answer": "3",
        "hint": r"Запиши мішані числа дробами — сусідні множники скоротяться.",
        "solution": r"$\frac{3}{2} \cdot \frac{4}{3} \cdot \frac{5}{4} \cdot \frac{6}{5} = \frac{6}{2} = 3$ — усе проміжне скорочується.",
    },
    # --- Аналіз ---
    {
        "type": "ERROR", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Сашко обчислював $1\frac{1}{2} \cdot 2\frac{2}{3}$. У якому кроці помилка?",
        "steps": [r"Цілі частини: $1 \cdot 2 = 2$", r"Дробові: $\frac{1}{2} \cdot \frac{2}{3} = \frac{1}{3}$", r"Відповідь: $2\frac{1}{3}$"],
        "wrong": 0,
        "hint": r"Чи можна множити окремо цілі й дробові частини?",
        "solution": r"Мішані числа не множать «частинами». $\frac{3}{2} \cdot \frac{8}{3} = 4$.",
    },
    {
        "type": "TF", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [
            (r"Якщо помножити число на дріб, більший за $1$, воно збільшиться (для додатних чисел)", True),
            (r"Добуток двох мішаних чисел завжди більший за $1$", True),
            (r"Добуток числа на обернене до нього дорівнює $0$", False),
            (r"$\frac{a}{b} \cdot \frac{c}{d} = \frac{a}{d} \cdot \frac{c}{b}$", True),
        ],
        "hint": r"Спробуй на прикладах.",
        "solution": r"Множник більший за $1$ — число збільшується ✓. Кожне мішане число більше за $1$ ✓. Добуток з оберненим — $1$. Обидва дорівнюють $\frac{ac}{bd}$ ✓.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Сторону квадрата зменшили до $\frac{2}{3}$ початкової. Яку частину від початкової становить нова площа?",
        "options": [(r"$\frac{4}{9}$", True), (r"$\frac{2}{3}$", False), (r"$\frac{4}{3}$", False), (r"$\frac{1}{3}$", False)],
        "hint": r"Площа — сторона на сторону.",
        "solution": r"$\frac{2}{3} \cdot \frac{2}{3} = \frac{4}{9}$.",
    },
    {
        "type": "MULTI", "difficulty": 3, "skill": "ANALYZE",
        "text": r"При яких натуральних $n$ добуток $\frac{n}{6} \cdot \frac{3}{4}$ є натуральним числом?",
        "options": [("$n = 8$", True), ("$n = 4$", False), ("$n = 16$", True), ("$n = 6$", False), ("$n = 24$", True)],
        "hint": r"Спрости добуток: $\frac{3n}{24}$.",
        "solution": r"$\frac{3n}{24} = \frac{n}{8}$ — натуральне, коли $n$ ділиться на $8$: $8$, $16$, $24$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Добуток двох дробів дорівнює $\frac{3}{10}$. Один із них — $\frac{3}{5}$. Знайди другий. Відповідь запиши дробом.",
        "answer": "1/2",
        "hint": r"Який дріб треба помножити на $\frac{3}{5}$, щоб вийшло $\frac{3}{10}$?",
        "solution": r"$\frac{3}{5} \cdot \frac{1}{2} = \frac{3}{10}$ ✓.",
    },

    # ==========================================
    # БОСИ
    # ==========================================
    {
        "type": "SHORT", "difficulty": 4, "skill": "MODEL",
        "text": r"Басейн наповнили на $\frac{3}{4}$, потім злили $\frac{1}{3}$ води, яка в ньому була. Яка частина басейну заповнена тепер? Відповідь запиши нескоротним дробом.",
        "answer": "1/2",
        "solution": r"Лишилося $\frac{2}{3}$ від $\frac{3}{4}$: $\frac{2}{3} \cdot \frac{3}{4} = \frac{1}{2}$.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "MODEL",
        "text": r"М'яч відскакує на висоту $\frac{3}{5}$ від тієї, з якої впав. З якої висоти (у м) він відскочить після третього удару, якщо впав з висоти $12\frac{1}{2}$ м?",
        "answer": "2,7",
        "solution": r"$\frac{25}{2} \cdot \frac{3}{5} \cdot \frac{3}{5} \cdot \frac{3}{5} = \frac{25 \cdot 27}{2 \cdot 125} = \frac{27}{10} = 2{,}7$ м.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "SOLVE",
        "text": r"Обчисли: $\left(1 - \frac{1}{2}\right)\left(1 - \frac{1}{3}\right)\left(1 - \frac{1}{4}\right) \cdots \left(1 - \frac{1}{10}\right)$. Відповідь запиши дробом.",
        "answer": "1/10",
        "solution": r"$\frac{1}{2} \cdot \frac{2}{3} \cdot \frac{3}{4} \cdots \frac{9}{10} = \frac{1}{10}$.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "SOLVE",
        "text": r"Обчисли: $2\frac{1}{4} \cdot 1\frac{7}{9} - 1\frac{1}{3} \cdot 1\frac{1}{2}$.",
        "answer": "2",
        "solution": r"$\frac{9}{4} \cdot \frac{16}{9} = 4$; $\frac{4}{3} \cdot \frac{3}{2} = 2$; $4 - 2 = 2$.",
    },
    {
        "type": "TF", "difficulty": 4, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [
            (r"Якщо $\frac{a}{b} \cdot \frac{c}{d} = 1$, то $\frac{c}{d}$ — число, обернене до $\frac{a}{b}$", True),
            (r"Добуток двох нескоротних дробів завжди нескоротний", False),
            (r"Якщо помножити дріб на його знаменник, отримаємо чисельник", True),
            (r"$\frac{1}{2} \cdot \frac{1}{2} \lt \frac{1}{2} + \frac{1}{2}$", True),
        ],
        "solution": r"Означення оберненого ✓. $\frac{2}{3} \cdot \frac{3}{4} = \frac{6}{12}$ — скоротний. $\frac{a}{b} \cdot b = a$ ✓. $\frac{1}{4} \lt 1$ ✓.",
    },

    # ==========================================
    # УЛЬТРА-БОСИ
    # ==========================================
    {
        "type": "SHORT", "difficulty": 5, "skill": "SOLVE",
        "text": r"Обчисли: $\frac{2 \cdot 2}{1 \cdot 3} \cdot \frac{3 \cdot 3}{2 \cdot 4} \cdot \frac{4 \cdot 4}{3 \cdot 5} \cdots \frac{9 \cdot 9}{8 \cdot 10}$. Відповідь запиши дробом.",
        "answer": "9/5",
        "solution": r"Розділимо на два добутки: $\frac{2 \cdot 3 \cdots 9}{1 \cdot 2 \cdots 8} = 9$ і $\frac{2 \cdot 3 \cdots 9}{3 \cdot 4 \cdots 10} = \frac{2}{10}$. Разом $9 \cdot \frac{1}{5} = \frac{9}{5}$.",
    },
    {
        "type": "SHORT", "difficulty": 5, "skill": "MODEL",
        "text": r"Тарас прочитав $\frac{1}{3}$ книжки, наступного дня — $\frac{1}{4}$ решти, а третього — $\frac{1}{2}$ нової решти. Яку частину книжки йому лишилося прочитати? Відповідь запиши нескоротним дробом.",
        "answer": "1/4",
        "solution": r"Після першого дня лишилося $\frac{2}{3}$; після другого — $\frac{3}{4} \cdot \frac{2}{3} = \frac{1}{2}$; після третього — $\frac{1}{2} \cdot \frac{1}{2} = \frac{1}{4}$.",
    },
]
