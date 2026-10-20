TOPIC_NAME = "2.6. Ділення дробів"
COURSE = "Математика (5-6 класи)"
GRADE = "6 клас"

TASKS = [
    # ==========================================
    # СХОДИНКА 1 — БАЗОВИЙ
    # ==========================================
    # --- Моделювання ---
    {
        "type": "CHOICE", "difficulty": 1, "skill": "MODEL",
        "text": r"Який дріб обернений до $\frac{3}{7}$?",
        "options": [(r"$\frac{7}{3}$", True), (r"$\frac{3}{7}$", False), (r"$-\frac{3}{7}$", False), (r"$\frac{4}{7}$", False)],
        "hint": r"Обернений дріб — чисельник і знаменник міняються місцями.",
        "solution": r"$\frac{3}{7} \cdot \frac{7}{3} = 1$, тож обернений — $\frac{7}{3}$.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "MODEL",
        "text": r"Як поділити $\frac{a}{b}$ на $\frac{c}{d}$?",
        "options": [(r"$\frac{a}{b} \cdot \frac{d}{c}$", True), (r"$\frac{b}{a} \cdot \frac{c}{d}$", False), (r"$\frac{a : c}{b + d}$", False), (r"$\frac{a}{b} \cdot \frac{c}{d}$", False)],
        "hint": r"Перевертаємо дільник — другий дріб.",
        "solution": r"Ділене множимо на дріб, обернений до дільника.",
    },
    {
        "type": "GROUP", "difficulty": 1, "skill": "MODEL",
        "text": r"Не обчислюючи, розподіли: частка більша чи менша за ділене?",
        "groups": [r"Більша за ділене", r"Менша за ділене"],
        "items": [(r"$6 : \frac{1}{2}$", 0), (r"$6 : 2$", 1), (r"$\frac{3}{4} : \frac{1}{4}$", 0), (r"$\frac{3}{4} : 3$", 1), (r"$5 : \frac{2}{3}$", 0)],
        "hint": r"Ділимо на число, менше за $1$, — частка більша за ділене.",
        "solution": r"Дільники $\frac{1}{2}$, $\frac{1}{4}$, $\frac{2}{3}$ менші за $1$ — частка більша. Ділення на $2$ і $3$ зменшує число.",
    },
    {
        "type": "TF", "difficulty": 1, "skill": "MODEL",
        "text": r"Правда чи ні?",
        "statements": [
            (r"$\frac{2}{5}$ і $\frac{5}{2}$ — обернені дроби", True),
            (r"Число, обернене до $4$, — це $\frac{1}{4}$", True),
            (r"$3 : \frac{1}{3} = 1$", False),
        ],
        "hint": r"Скільки третин у трьох цілих?",
        "solution": r"$\frac{2}{5} \cdot \frac{5}{2} = 1$; $4 \cdot \frac{1}{4} = 1$; $3 : \frac{1}{3} = 3 \cdot 3 = 9$.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "MODEL",
        "text": r"У пакеті $2$ кг борошна. Скільки пакетиків по $\frac{1}{5}$ кг можна з нього насипати?",
        "options": [(r"$10$", True), (r"$\frac{2}{5}$", False), (r"$7$", False), (r"$5$", False)],
        "hint": r"Скільки разів $\frac{1}{5}$ вміщується у $2$? Це $2 : \frac{1}{5}$.",
        "solution": r"$2 : \frac{1}{5} = 2 \cdot 5 = 10$ пакетиків.",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"Обчисли: $4 : \frac{1}{3}$.",
        "answer": "12",
        "hint": r"$4 \cdot 3$.",
        "solution": r"$4 : \frac{1}{3} = 4 \cdot 3 = 12$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"Обчисли: $\frac{3}{5} : \frac{3}{10}$.",
        "answer": "2",
        "hint": r"$\frac{3}{5} \cdot \frac{10}{3}$.",
        "solution": r"$\frac{3 \cdot 10}{5 \cdot 3} = 2$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"Обчисли: $\frac{4}{7} : 2$. Відповідь запиши нескоротним дробом.",
        "answer": "2/7",
        "hint": r"Поділити на $2$ — помножити на $\frac{1}{2}$.",
        "solution": r"$\frac{4}{7} \cdot \frac{1}{2} = \frac{4}{14} = \frac{2}{7}$.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "SOLVE",
        "text": r"Обчисли: $\frac{1}{2} : \frac{1}{4}$.",
        "options": [(r"$2$", True), (r"$\frac{1}{8}$", False), (r"$\frac{1}{2}$", False), (r"$4$", False)],
        "hint": r"Скільки чвертей у половині?",
        "solution": r"$\frac{1}{2} \cdot 4 = 2$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"Обчисли: $\frac{5}{6} : \frac{5}{6}$.",
        "answer": "1",
        "hint": r"Число, поділене саме на себе.",
        "solution": r"$\frac{5}{6} \cdot \frac{6}{5} = 1$.",
    },
    # --- Аналіз ---
    {
        "type": "ERROR", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Сашко ділить $\frac{2}{3} : \frac{4}{5}$. У якому кроці помилка?",
        "steps": [r"$\frac{2}{3} : \frac{4}{5} = \frac{3}{2} \cdot \frac{4}{5}$", r"$= \frac{12}{10}$", r"$= 1\frac{1}{5}$"],
        "wrong": 0,
        "hint": r"Який дріб треба перевертати?",
        "solution": r"Перевертаємо дільник: $\frac{2}{3} \cdot \frac{5}{4} = \frac{10}{12} = \frac{5}{6}$.",
    },
    {
        "type": "MULTI", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Які вирази дорівнюють $\frac{3}{4} : \frac{1}{2}$?",
        "options": [(r"$\frac{3}{4} \cdot 2$", True), (r"$1\frac{1}{2}$", True), (r"$\frac{3}{2}$", True), (r"$\frac{3}{8}$", False), (r"$\frac{4}{3} \cdot \frac{1}{2}$", False)],
        "hint": r"Обчисли частку: $\frac{3}{4} \cdot \frac{2}{1}$.",
        "solution": r"$\frac{3}{4} \cdot 2 = \frac{3}{2} = 1\frac{1}{2}$. $\frac{3}{8}$ — це добуток, а не частка.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Оля: «$\frac{3}{4} : 3 = \frac{9}{4}$». Що не так?",
        "options": [(r"Треба множити на $\frac{1}{3}$: $\frac{3}{4} : 3 = \frac{1}{4}$", True), (r"Оля права", False),
                    (r"Правильно $\frac{3}{12}$, і далі не скорочується", False), (r"Правильно $4$", False)],
        "hint": r"Ділення на $3$ має зменшити число.",
        "solution": r"Оля помножила замість ділення. $\frac{3}{4} \cdot \frac{1}{3} = \frac{1}{4}$.",
    },
    {
        "type": "TF", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [
            (r"Перевірка ділення: частка $\cdot$ дільник $=$ ділене", True),
            (r"$\frac{1}{3} : \frac{1}{6} = 2$", True),
            (r"Ділити дроби можна, лише звівши їх до спільного знаменника", False),
        ],
        "hint": r"Спільний знаменник для ділення не потрібен.",
        "solution": r"$2 \cdot \frac{1}{6} = \frac{1}{3}$ ✓. Ділимо множенням на обернений дріб, без спільного знаменника.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Яке число не має оберненого?",
        "options": [(r"$0$", True), (r"$1$", False), (r"$\frac{1}{2}$", False), (r"$10$", False)],
        "hint": r"На що треба помножити число, щоб отримати $1$?",
        "solution": r"$0 \cdot x = 0 \ne 1$ — оберненого до нуля немає (на нуль ділити не можна). Обернене до $1$ — саме $1$.",
    },
    # ==========================================
    # СХОДИНКА 2 — СЕРЕДНІЙ
    # ==========================================
    # --- Моделювання ---
    {
        "type": "SHORT", "difficulty": 2, "skill": "MODEL",
        "text": r"Стрічку завдовжки $\frac{9}{10}$ м розрізали на шматки по $\frac{3}{10}$ м. Скільки шматків вийшло?",
        "answer": "3",
        "hint": r"$\frac{9}{10} : \frac{3}{10}$.",
        "solution": r"$\frac{9}{10} \cdot \frac{10}{3} = 3$ шматки.",
    },
    {
        "type": "ORDER", "difficulty": 2, "skill": "MODEL",
        "text": r"Розташуй кроки обчислення $1\frac{1}{3} : \frac{8}{9}$.",
        "items": [
            r"Мішане число — у неправильний дріб: $\frac{4}{3}$",
            r"Ділення — множення на обернений дріб: $\frac{4}{3} \cdot \frac{9}{8}$",
            r"Скорочуємо навхрест: $\frac{1 \cdot 3}{1 \cdot 2}$",
            r"Відповідь: $\frac{3}{2} = 1\frac{1}{2}$",
        ],
        "hint": r"Спершу позбудься мішаного числа.",
        "solution": r"$\frac{4}{3} \cdot \frac{9}{8} = \frac{36}{24} = \frac{3}{2}$.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "MODEL",
        "text": r"За $\frac{3}{4}$ год пішохід пройшов $3$ км. Яка його швидкість (км/год)?",
        "options": [(r"$4$ км/год", True), (r"$2\frac{1}{4}$ км/год", False), (r"$\frac{1}{4}$ км/год", False), (r"$3\frac{3}{4}$ км/год", False)],
        "hint": r"Швидкість — шлях, поділений на час.",
        "solution": r"$3 : \frac{3}{4} = 3 \cdot \frac{4}{3} = 4$ км/год.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "MODEL",
        "text": r"Площа прямокутника — $\frac{5}{6}$ м², довжина — $\frac{5}{4}$ м. Знайди ширину. Відповідь запиши нескоротним дробом.",
        "answer": "2/3",
        "hint": r"Ширина — площа, поділена на довжину.",
        "solution": r"$\frac{5}{6} : \frac{5}{4} = \frac{5}{6} \cdot \frac{4}{5} = \frac{4}{6} = \frac{2}{3}$ м.",
    },
    {
        "type": "TF", "difficulty": 2, "skill": "MODEL",
        "text": r"$3$ кг цукерок розклали в коробки по $\frac{3}{8}$ кг. Правда чи ні?",
        "statements": [
            (r"Коробок — $8$", True),
            (r"Кількість коробок знаходимо дією $3 \cdot \frac{3}{8}$", False),
            (r"Якби в коробку клали по $\frac{3}{4}$ кг, коробок було б удвічі менше", True),
        ],
        "hint": r"Скільки разів $\frac{3}{8}$ вміщується в $3$?",
        "solution": r"$3 : \frac{3}{8} = 3 \cdot \frac{8}{3} = 8$. Удвічі більша коробка — удвічі менше коробок: $3 : \frac{3}{4} = 4$.",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Обчисли: $\frac{7}{12} : \frac{14}{15}$. Відповідь запиши нескоротним дробом.",
        "answer": "5/8",
        "hint": r"$\frac{7}{12} \cdot \frac{15}{14}$; скорочуй $7$ і $14$, $15$ і $12$.",
        "solution": r"$\frac{7 \cdot 15}{12 \cdot 14} = \frac{1 \cdot 5}{4 \cdot 2} = \frac{5}{8}$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Обчисли: $2\frac{1}{2} : \frac{5}{8}$.",
        "answer": "4",
        "hint": r"$2\frac{1}{2} = \frac{5}{2}$.",
        "solution": r"$\frac{5}{2} \cdot \frac{8}{5} = 4$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Обчисли: $3\frac{3}{4} : 5$. Відповідь запиши нескоротним дробом.",
        "answer": "3/4",
        "hint": r"$3\frac{3}{4} = \frac{15}{4}$; поділити на $5$ — помножити на $\frac{1}{5}$.",
        "solution": r"$\frac{15}{4} \cdot \frac{1}{5} = \frac{3}{4}$.",
    },
    {
        "type": "FIELDS", "difficulty": 2, "skill": "SOLVE",
        "text": r"Обчисли частки.",
        "fields": [(r"$\frac{8}{9} : \frac{2}{3} =$", "4/3"), (r"$1\frac{1}{5} : 1\frac{1}{2} =$", "4/5")],
        "hint": r"Мішані числа — у неправильні дроби: $\frac{6}{5}$ і $\frac{3}{2}$.",
        "solution": r"$\frac{8}{9} \cdot \frac{3}{2} = \frac{4}{3}$; $\frac{6}{5} \cdot \frac{2}{3} = \frac{4}{5}$.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "SOLVE",
        "text": r"Обчисли: $6 : 1\frac{1}{2}$.",
        "options": [(r"$4$", True), (r"$9$", False), (r"$6\frac{1}{2}$", False), (r"$3$", False)],
        "hint": r"$1\frac{1}{2} = \frac{3}{2}$.",
        "solution": r"$6 \cdot \frac{2}{3} = 4$. $9$ — це $6 \cdot 1\frac{1}{2}$.",
    },
    # --- Аналіз ---
    {
        "type": "ERROR", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Іра ділить $2\frac{1}{4} : \frac{3}{4}$. У якому кроці помилка?",
        "steps": [r"$2\frac{1}{4} : \frac{3}{4} = 2 + \frac{1}{4} : \frac{3}{4}$", r"$\frac{1}{4} : \frac{3}{4} = \frac{1}{3}$", r"Відповідь: $2\frac{1}{3}$"],
        "wrong": 0,
        "hint": r"Ділити треба все мішане число, а не лише дробову частину.",
        "solution": r"$\frac{9}{4} \cdot \frac{4}{3} = 3$.",
    },
    {
        "type": "MULTI", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Які частки дорівнюють $2$?",
        "options": [(r"$\frac{2}{3} : \frac{1}{3}$", True), (r"$\frac{4}{5} : \frac{2}{5}$", True), (r"$1 : \frac{1}{2}$", True), (r"$\frac{1}{2} : 1$", False), (r"$2 : \frac{1}{2}$", False)],
        "hint": r"Обчисли кожну частку.",
        "solution": r"$\frac{2}{3} \cdot 3 = 2$; $\frac{4}{5} \cdot \frac{5}{2} = 2$; $1 \cdot 2 = 2$. А $\frac{1}{2} : 1 = \frac{1}{2}$, $2 : \frac{1}{2} = 4$.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Що більше: $\frac{5}{6} : \frac{1}{3}$ чи $\frac{5}{6} \cdot 3$?",
        "options": [(r"Вони рівні", True), (r"Частка", False), (r"Добуток", False), (r"Порівняти не можна", False)],
        "hint": r"Поділити на $\frac{1}{3}$ — це помножити на $3$.",
        "solution": r"Обидва вирази дорівнюють $\frac{5}{2} = 2\frac{1}{2}$.",
    },
    {
        "type": "GROUP", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Розподіли вирази: значення менше за $1$ чи більше за $1$?",
        "groups": [r"Менше за $1$", r"Більше за $1$"],
        "items": [(r"$\frac{2}{3} : \frac{3}{4}$", 0), (r"$\frac{3}{4} : \frac{2}{3}$", 1), (r"$\frac{1}{2} : 3$", 0), (r"$5 : 4$", 1), (r"$\frac{4}{9} : \frac{2}{9}$", 1)],
        "hint": r"Ділене менше за дільник — частка менша за $1$.",
        "solution": r"$\frac{8}{9}$ і $\frac{1}{6}$ — менші за $1$; $\frac{9}{8}$, $\frac{5}{4}$, $2$ — більші.",
    },
    {
        "type": "TF", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [
            (r"$\frac{a}{b} : \frac{a}{b} = 1$ (при $a \ne 0$)", True),
            (r"$1 : \frac{2}{7} = \frac{7}{2}$", True),
            (r"$\frac{1}{2} : \frac{1}{3} = \frac{1}{6}$", False),
        ],
        "hint": r"$\frac{1}{2} \cdot 3 = ?$",
        "solution": r"Число на саме себе — $1$. $1 : \frac{2}{7}$ — обернений дріб. $\frac{1}{2} : \frac{1}{3} = \frac{3}{2}$, а $\frac{1}{6}$ — добуток.",
    },
    # ==========================================
    # СХОДИНКА 3 — ПІДВИЩЕНИЙ
    # ==========================================
    # --- Моделювання ---
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"Велосипедист проїхав $8\frac{1}{3}$ км за $\frac{5}{6}$ год. Яка його швидкість (км/год)?",
        "answer": "10",
        "hint": r"$8\frac{1}{3} = \frac{25}{3}$.",
        "solution": r"$\frac{25}{3} \cdot \frac{6}{5} = 10$ км/год.",
    },
    {
        "type": "FIELDS", "difficulty": 3, "skill": "MODEL",
        "text": r"У бочці $12$ л води. Скільки відер по $\frac{3}{4}$ л і скільки банок по $1\frac{1}{2}$ л можна наповнити (окремо) цією водою?",
        "fields": [(r"Відер по $\frac{3}{4}$ л:", "16"), (r"Банок по $1\frac{1}{2}$ л:", "8")],
        "hint": r"$12 : \frac{3}{4}$ і $12 : \frac{3}{2}$.",
        "solution": r"$12 \cdot \frac{4}{3} = 16$; $12 \cdot \frac{2}{3} = 8$.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "MODEL",
        "text": r"Моторний човен проходить $\frac{2}{3}$ км за $\frac{1}{30}$ год. Скільки кілометрів він пройде за $1$ год?",
        "options": [(r"$20$ км", True), (r"$\frac{1}{45}$ км", False), (r"$10$ км", False), (r"$30$ км", False)],
        "hint": r"Швидкість: $\frac{2}{3} : \frac{1}{30}$.",
        "solution": r"$\frac{2}{3} \cdot 30 = 20$ км/год, тож за годину — $20$ км.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"Мотузку завдовжки $7\frac{1}{2}$ м розрізали на шматки по $1\frac{1}{4}$ м. Скільки зробили розрізів?",
        "answer": "5",
        "hint": r"Спершу знайди кількість шматків. Розрізів на $1$ менше.",
        "solution": r"$\frac{15}{2} : \frac{5}{4} = \frac{15}{2} \cdot \frac{4}{5} = 6$ шматків — $5$ розрізів.",
    },
    {
        "type": "TF", "difficulty": 3, "skill": "MODEL",
        "text": r"Обидва дроби правильні: $\frac{a}{b} \lt 1$ і $\frac{c}{d} \lt 1$. Правда чи ні?",
        "statements": [
            (r"Частка $\frac{a}{b} : \frac{c}{d}$ може бути більшою за $1$", True),
            (r"Частка завжди більша за ділене $\frac{a}{b}$", True),
            (r"Частка завжди менша за $1$", False),
        ],
        "hint": r"Спробуй $\frac{1}{2} : \frac{1}{4}$ і $\frac{1}{4} : \frac{1}{2}$.",
        "solution": r"Ділення на число, менше за $1$, збільшує ділене. $\frac{1}{2} : \frac{1}{4} = 2 \gt 1$, а $\frac{1}{4} : \frac{1}{2} = \frac{1}{2} \lt 1$.",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Обчисли: $\left(\frac{3}{4} + \frac{1}{2}\right) : \frac{5}{8}$.",
        "answer": "2",
        "hint": r"Спершу дужки: $\frac{3}{4} + \frac{2}{4}$.",
        "solution": r"$\frac{5}{4} \cdot \frac{8}{5} = 2$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Знайди $x$: $x \cdot \frac{3}{5} = \frac{9}{10}$. Відповідь запиши нескоротним дробом.",
        "answer": "3/2",
        "hint": r"Невідомий множник — добуток, поділений на відомий множник.",
        "solution": r"$x = \frac{9}{10} : \frac{3}{5} = \frac{9}{10} \cdot \frac{5}{3} = \frac{3}{2}$.",
    },
    {
        "type": "FIELDS", "difficulty": 3, "skill": "SOLVE",
        "text": r"Обчисли.",
        "fields": [(r"$4\frac{1}{2} : 1\frac{4}{5} =$", "5/2"), (r"$\frac{5}{6} : 2\frac{1}{2} : \frac{1}{3} =$", "1")],
        "hint": r"Ділення виконуй зліва направо; мішані числа — у неправильні дроби.",
        "solution": r"$\frac{9}{2} \cdot \frac{5}{9} = \frac{5}{2}$. $\frac{5}{6} \cdot \frac{2}{5} = \frac{1}{3}$; $\frac{1}{3} : \frac{1}{3} = 1$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Знайди $x$: $\frac{2}{3} : x = \frac{4}{9}$. Відповідь запиши нескоротним дробом.",
        "answer": "3/2",
        "hint": r"Невідомий дільник — ділене, поділене на частку.",
        "solution": r"$x = \frac{2}{3} : \frac{4}{9} = \frac{2}{3} \cdot \frac{9}{4} = \frac{3}{2}$.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "SOLVE",
        "text": r"Обчисли: $2\frac{2}{3} : \frac{4}{9} - 1\frac{1}{2} : \frac{3}{4}$.",
        "options": [(r"$4$", True), (r"$6$", False), (r"$2$", False), (r"$\frac{2}{3}$", False)],
        "hint": r"Обчисли кожну частку, потім віднімай.",
        "solution": r"$\frac{8}{3} \cdot \frac{9}{4} = 6$; $\frac{3}{2} \cdot \frac{4}{3} = 2$; $6 - 2 = 4$.",
    },
    # --- Аналіз ---
    {
        "type": "ERROR", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Максим обчислює $\frac{3}{4} : \frac{1}{2} : \frac{1}{2}$. У якому кроці помилка?",
        "steps": [r"$\frac{1}{2} : \frac{1}{2} = 1$", r"$\frac{3}{4} : 1 = \frac{3}{4}$", r"Відповідь: $\frac{3}{4}$"],
        "wrong": 0,
        "hint": r"Ділення виконують зліва направо.",
        "solution": r"$\frac{3}{4} : \frac{1}{2} = \frac{3}{2}$; $\frac{3}{2} : \frac{1}{2} = 3$. Відповідь: $3$.",
    },
    {
        "type": "MULTI", "difficulty": 3, "skill": "ANALYZE",
        "text": r"При яких натуральних $n$ частка $\frac{6}{7} : \frac{n}{7}$ — натуральне число?",
        "options": [(r"$n = 1$", True), (r"$n = 2$", True), (r"$n = 3$", True), (r"$n = 6$", True), (r"$n = 4$", False)],
        "hint": r"$\frac{6}{7} \cdot \frac{7}{n} = \frac{6}{n}$.",
        "solution": r"$\frac{6}{n}$ — натуральне, коли $n$ — дільник $6$: $1, 2, 3, 6$. При $n = 4$ — $1\frac{1}{2}$.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Частку $\frac{a}{b} : \frac{c}{d}$ помножили на $\frac{c}{d}$. Що вийшло?",
        "options": [(r"$\frac{a}{b}$", True), (r"$\frac{c}{d}$", False), (r"$1$", False), (r"$\frac{ad}{bc}$", False)],
        "hint": r"Так перевіряють ділення.",
        "solution": r"$\frac{ad}{bc} \cdot \frac{c}{d} = \frac{a}{b}$ — повертаємося до діленого.",
    },
    {
        "type": "TF", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [
            (r"$\frac{1}{2} : \frac{1}{4} : \frac{1}{8} = 16$", True),
            (r"$\frac{1}{2} : \left(\frac{1}{4} : \frac{1}{8}\right) = \frac{1}{4}$", True),
            (r"Для ділення порядок дій неважливий", False),
        ],
        "hint": r"Порівняй два перші вирази.",
        "solution": r"$\frac{1}{2} \cdot 4 = 2$, $2 \cdot 8 = 16$. У другому: $\frac{1}{4} : \frac{1}{8} = 2$, $\frac{1}{2} : 2 = \frac{1}{4}$. Результати різні.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Учень мав поділити число на $\frac{2}{3}$, а помилково помножив на $\frac{2}{3}$ і отримав $8$. Яку відповідь він мав отримати?",
        "answer": "18",
        "hint": r"Спершу знайди число: $x \cdot \frac{2}{3} = 8$.",
        "solution": r"$x = 8 : \frac{2}{3} = 12$. Правильна відповідь: $12 : \frac{2}{3} = 18$.",
    },
    # ==========================================
    # БОСИ
    # ==========================================
    {
        "type": "SHORT", "difficulty": 4, "skill": "MODEL",
        "text": r"Кран наповнює бак за $\frac{3}{4}$ год. Яку частину бака він наповнить за $\frac{1}{3}$ год? Відповідь запиши нескоротним дробом.",
        "answer": "4/9",
        "solution": r"За годину кран наповнює $1 : \frac{3}{4} = \frac{4}{3}$ бака. За $\frac{1}{3}$ год: $\frac{4}{3} \cdot \frac{1}{3} = \frac{4}{9}$ бака.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "MODEL",
        "text": r"Зі $\frac{4}{5}$ кг борошна печуть $2$ пироги. Скільки пирогів можна спекти з $6$ кг борошна?",
        "answer": "15",
        "solution": r"На пиріг: $\frac{4}{5} : 2 = \frac{2}{5}$ кг. $6 : \frac{2}{5} = 6 \cdot \frac{5}{2} = 15$ пирогів.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "SOLVE",
        "text": r"Обчисли: $\left(2\frac{1}{3} - 1\frac{1}{2}\right) : \left(\frac{5}{6} \cdot \frac{2}{5}\right)$. Відповідь запиши нескоротним дробом.",
        "answer": "5/2",
        "solution": r"$2\frac{1}{3} - 1\frac{1}{2} = \frac{14}{6} - \frac{9}{6} = \frac{5}{6}$. $\frac{5}{6} \cdot \frac{2}{5} = \frac{1}{3}$. $\frac{5}{6} : \frac{1}{3} = \frac{5}{2}$.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "SOLVE",
        "text": r"Знайди $x$: $\left(x + \frac{1}{2}\right) : \frac{3}{4} = 2$. Відповідь запиши нескоротним дробом.",
        "answer": "1",
        "solution": r"$x + \frac{1}{2} = 2 \cdot \frac{3}{4} = \frac{3}{2}$, $x = 1$.",
    },
    {
        "type": "TF", "difficulty": 4, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [
            (r"Якщо дільник зменшити вдвічі, частка збільшиться вдвічі", True),
            (r"Якщо ділене і дільник помножити на те саме число ($\ne 0$), частка не зміниться", True),
            (r"Частка двох правильних дробів завжди правильний дріб", False),
            (r"$\frac{3}{8} : \frac{3}{4} = \frac{1}{2}$", True),
        ],
        "solution": r"$a : \frac{b}{2} = 2 \cdot (a : b)$. Множення обох компонентів не змінює частку. $\frac{3}{4} : \frac{3}{8} = 2$ — неправильний. $\frac{3}{8} \cdot \frac{4}{3} = \frac{1}{2}$.",
    },
    # ==========================================
    # УЛЬТРА
    # ==========================================
    {
        "type": "SHORT", "difficulty": 5, "skill": "SOLVE",
        "text": r"Обчисли: $\frac{1}{2} : \frac{2}{3} : \frac{3}{4} : \frac{4}{5} : \frac{5}{6}$. Відповідь запиши нескоротним дробом.",
        "answer": "3/2",
        "solution": r"$\frac{1}{2} \cdot \frac{3}{2} \cdot \frac{4}{3} \cdot \frac{5}{4} \cdot \frac{6}{5} = \frac{1 \cdot 3 \cdot 4 \cdot 5 \cdot 6}{2 \cdot 2 \cdot 3 \cdot 4 \cdot 5} = \frac{6}{4} = \frac{3}{2}$: множники $3$, $4$, $5$ скорочуються.",
    },
    {
        "type": "SHORT", "difficulty": 5, "skill": "MODEL",
        "text": r"Перший насос викачує воду з басейну за $\frac{3}{4}$ год, другий — за $1\frac{1}{2}$ год. За скільки хвилин викачають воду обидва насоси разом?",
        "answer": "30",
        "solution": r"За годину: перший — $\frac{4}{3}$ басейну, другий — $\frac{2}{3}$; разом $2$ басейни за годину. Один басейн — за $1 : 2 = \frac{1}{2}$ год $= 30$ хв.",
    },
]
