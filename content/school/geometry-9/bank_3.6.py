TOPIC_NAME = "3.6. Синус, косинус і тангенс кутів від 0° до 180°"
COURSE = "Геометрія (7-9 класи)"
GRADE = "9 клас"

TASKS = [
    # ==========================================
    # СХОДИНКА 1 — БАЗОВИЙ
    # ==========================================
    # --- Моделювання ---
    {
        "type": "MATCH", "difficulty": 1, "skill": "MODEL",
        "text": r"Установіть відповідність між виразом (1–3) та його значенням (А–Д).",
        "options": [r"А) $\frac12$", r"Б) $-\frac12$", r"В) $0$", r"Г) $-1$", r"Д) $1$"],
        "matches": [(r"1. $\sin 150^\circ$", r"А) $\frac12$"), (r"2. $\cos 120^\circ$", r"Б) $-\frac12$"), (r"3. $\cos 180^\circ$", r"Г) $-1$")],
        "solution": r"$\sin 150^\circ = \sin 30^\circ = \frac12$; $\cos 120^\circ = -\cos 60^\circ = -\frac12$; $\cos 180^\circ = -1$ (точка $(-1;\,0)$).",
    },
    {
        "type": "COORD", "difficulty": 1, "skill": "MODEL",
        "text": r"Позначте точку одиничного півкола, що відповідає куту $90^\circ$.",
        "xmin": -2, "xmax": 2, "ymin": -2, "ymax": 2, "step": 1, "answer": [0, 1],
        "solution": r"$M(\cos 90^\circ;\,\sin 90^\circ) = (0;\,1)$.",
    },
    {
        "type": "TF", "difficulty": 1, "skill": "MODEL",
        "text": r"Правда чи ні?",
        "statements": [(r"Синус тупого кута додатний", True), (r"Косинус тупого кута додатний", False),
                       (r"Тангенс тупого кута від'ємний", True)],
        "solution": r"Для тупого кута точка $M$ лежить у II чверті: $y \gt 0$, $x \lt 0$. Тому $\sin\alpha \gt 0$, $\cos\alpha \lt 0$, $\operatorname{tg}\alpha = \frac yx \lt 0$.",
    },
    {
        "type": "GROUP", "difficulty": 1, "skill": "MODEL",
        "text": r"Розподіліть значення за знаком.",
        "groups": ["додатні", "від'ємні", "дорівнюють нулю"],
        "items": [(r"$\cos 40^\circ$", 0), (r"$\cos 140^\circ$", 1), (r"$\sin 140^\circ$", 0), (r"$\operatorname{tg} 100^\circ$", 1),
                  (r"$\cos 90^\circ$", 2), (r"$\sin 180^\circ$", 2)],
        "solution": r"Синус кута від $0^\circ$ до $180^\circ$ невід'ємний; косинус і тангенс тупого кута від'ємні. $\cos 90^\circ = 0$, $\sin 180^\circ = 0$.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "MODEL",
        "text": r"Точка $M$ одиничного півкола має координати $\left(-\frac{\sqrt3}{2};\,\frac12\right)$. Якому куту $\alpha$ вона відповідає?",
        "options": [(r"$150^\circ$", True), (r"$30^\circ$", False), (r"$120^\circ$", False), (r"$60^\circ$", False)],
        "solution": r"$\cos\alpha = -\frac{\sqrt3}{2}$, $\sin\alpha = \frac12$ — тупий кут $180^\circ - 30^\circ = 150^\circ$.",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"Обчисліть $\operatorname{tg} 135^\circ$.",
        "answer": "-1",
        "solution": r"$\operatorname{tg} 135^\circ = -\operatorname{tg} 45^\circ = -1$.",
    },
    {
        "type": "FIELDS", "difficulty": 1, "skill": "SOLVE",
        "text": r"Знайдіть координати точки одиничного півкола, що відповідає куту $180^\circ$.",
        "fields": [(r"$x =$", "-1"), (r"$y =$", "0")],
        "solution": r"$(\cos 180^\circ;\,\sin 180^\circ) = (-1;\,0)$.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "SOLVE",
        "text": r"Знайдіть $\cos 150^\circ$.",
        "options": [(r"$-\frac{\sqrt3}{2}$", True), (r"$\frac{\sqrt3}{2}$", False), (r"$-\frac12$", False), (r"$\frac12$", False)],
        "solution": r"$\cos 150^\circ = -\cos 30^\circ = -\frac{\sqrt3}{2}$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"Обчисліть $\sin 120^\circ \cdot \cos 150^\circ$.",
        "answer": "-0,75",
        "solution": r"$\frac{\sqrt3}{2} \cdot \left(-\frac{\sqrt3}{2}\right) = -\frac34 = -0{,}75$.",
    },
    {
        "type": "MULTI", "difficulty": 1, "skill": "SOLVE",
        "text": r"Які рівності правильні?",
        "options": [(r"$\sin 135^\circ = \frac{\sqrt2}{2}$", True), (r"$\cos 135^\circ = -\frac{\sqrt2}{2}$", True), (r"$\sin 90^\circ = 0$", False),
                    (r"$\operatorname{tg} 180^\circ = 0$", True), (r"$\cos 0^\circ = 0$", False)],
        "solution": r"$\sin 135^\circ = \sin 45^\circ$, $\cos 135^\circ = -\cos 45^\circ$. $\sin 90^\circ = 1$, $\cos 0^\circ = 1$, $\operatorname{tg} 180^\circ = \frac{0}{-1} = 0$.",
    },
    # --- Аналіз результатів ---
    {
        "type": "ERROR", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Учень обчислював $\cos 120^\circ$. У якому кроці помилка?",
        "steps": [r"$120^\circ = 180^\circ - 60^\circ$", r"$\cos(180^\circ - \alpha) = \cos\alpha$", r"$\cos 120^\circ = \cos 60^\circ = \frac12$"],
        "wrong": 1,
        "solution": r"$\cos(180^\circ - \alpha) = -\cos\alpha$. Отже, $\cos 120^\circ = -\frac12$.",
    },
    {
        "type": "TF", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [(r"$\sin 100^\circ = \sin 80^\circ$", True), (r"$\cos 100^\circ = \cos 80^\circ$", False), (r"$\operatorname{tg} 90^\circ$ не існує", True)],
        "solution": r"$100^\circ = 180^\circ - 80^\circ$: синуси рівні, косинуси протилежні. $\cos 90^\circ = 0$ — тангенс не означений.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Учень: «$\sin 150^\circ = -\frac12$, бо кут тупий». Чи правий він?",
        "options": [(r"Ні: $\sin 150^\circ = \frac12$", True), ("Так", False), (r"Ні: $\sin 150^\circ = \frac{\sqrt3}{2}$", False), (r"Ні: $\sin 150^\circ = -\frac{\sqrt3}{2}$", False)],
        "solution": r"Синус кута від $0^\circ$ до $180^\circ$ невід'ємний: $\sin 150^\circ = \sin 30^\circ = \frac12$.",
    },
    {
        "type": "MULTI", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Для яких кутів $\alpha$ з проміжку $[0^\circ;\,180^\circ]$ виконується $\cos\alpha \lt 0$?",
        "options": [(r"$100^\circ$", True), (r"$179^\circ$", True), (r"$91^\circ$", True), (r"$90^\circ$", False), (r"$45^\circ$", False)],
        "solution": r"$\cos\alpha \lt 0$ лише для тупих кутів ($90^\circ \lt \alpha \le 180^\circ$). $\cos 90^\circ = 0$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Знайдіть $\sin^2 125^\circ + \cos^2 125^\circ$.",
        "answer": "1",
        "solution": r"Основна тотожність виконується для будь-якого кута: $\sin^2\alpha + \cos^2\alpha = 1$.",
    },

    # ==========================================
    # СХОДИНКА 2 — СЕРЕДНІЙ
    # ==========================================
    # --- Моделювання ---
    {
        "type": "COORD", "difficulty": 2, "skill": "MODEL",
        "text": r"Точку $A(2\sqrt2;\,0)$ повернули навколо початку координат на $135^\circ$ проти годинникової стрілки. Позначте отриману точку.",
        "xmin": -4, "xmax": 4, "ymin": -4, "ymax": 4, "step": 1, "answer": [-2, 2],
        "solution": r"$(2\sqrt2\cos 135^\circ;\,2\sqrt2\sin 135^\circ) = \left(2\sqrt2 \cdot \left(-\frac{\sqrt2}{2}\right);\,2\sqrt2 \cdot \frac{\sqrt2}{2}\right) = (-2;\,2)$.",
    },
    {
        "type": "FIELDS", "difficulty": 2, "skill": "MODEL",
        "text": r"Точка $M$ лежить на колі з центром $O(0;\,0)$ радіуса $6$, промінь $OM$ утворює з додатною піввіссю $Ox$ кут $150^\circ$. Знайдіть координати $M$ (ординату — числом).",
        "fields": [(r"$x = -k\sqrt3$, де $k =$", "3"), (r"$y =$", "3")],
        "solution": r"$M(6\cos 150^\circ;\,6\sin 150^\circ) = \left(-3\sqrt3;\,3\right)$.",
    },
    {
        "type": "TF", "difficulty": 2, "skill": "MODEL",
        "text": r"$\alpha$ і $\beta$ — суміжні кути. Правда чи ні?",
        "statements": [(r"$\sin\alpha = \sin\beta$", True), (r"$\cos\alpha = -\cos\beta$", True), (r"$\operatorname{tg}\alpha = \operatorname{tg}\beta$", False),
                       (r"$\cos\alpha + \cos\beta = 0$", True)],
        "solution": r"$\beta = 180^\circ - \alpha$: синуси рівні, косинуси й тангенси протилежні (якщо $\alpha \ne 90^\circ$). Наприклад, $\operatorname{tg} 60^\circ = \sqrt3$, $\operatorname{tg} 120^\circ = -\sqrt3$.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "MODEL",
        "text": r"Кут $A$ трикутника $ABC$ тупий. Яке з тверджень правильне?",
        "options": [(r"$\cos A \lt 0$", True), (r"$\sin A \lt 0$", False), (r"$\cos A \gt 0$", False), (r"$\operatorname{tg} A \gt 0$", False)],
        "solution": r"Для тупого кута $\cos A \lt 0$ і $\operatorname{tg} A \lt 0$, а $\sin A \gt 0$.",
    },
    {
        "type": "MATCH", "difficulty": 2, "skill": "MODEL",
        "text": r"Установіть відповідність між умовою (1–3) та кутом $\alpha$ ($0^\circ \le \alpha \le 180^\circ$) (А–Д).",
        "options": [r"А) $135^\circ$", r"Б) $45^\circ$", r"В) $120^\circ$", r"Г) $150^\circ$", r"Д) $60^\circ$"],
        "matches": [(r"1. $\cos\alpha = -\frac{\sqrt2}{2}$", r"А) $135^\circ$"), (r"2. $\operatorname{tg}\alpha = -\sqrt3$", r"В) $120^\circ$"),
                    (r"3. $\cos\alpha = -\frac{\sqrt3}{2}$", r"Г) $150^\circ$")],
        "solution": r"За косинусом і тангенсом кут визначається однозначно. $\cos 135^\circ = -\frac{\sqrt2}{2}$, $\operatorname{tg} 120^\circ = -\sqrt3$, $\cos 150^\circ = -\frac{\sqrt3}{2}$.",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"$\sin\alpha = 0{,}6$, $\alpha$ — тупий кут. Знайдіть $\cos\alpha$.",
        "answer": "-0,8",
        "solution": r"$\cos^2\alpha = 1 - 0{,}36 = 0{,}64$, $\cos\alpha = \pm 0{,}8$. Кут тупий — $\cos\alpha = -0{,}8$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"$\cos\alpha = -\frac{8}{17}$. Знайдіть $\sin\alpha$ (звичайним дробом, наприклад 3/4).",
        "answer": "15/17",
        "solution": r"$\sin\alpha = \sqrt{1 - \frac{64}{289}} = \sqrt{\frac{225}{289}} = \frac{15}{17}$ (синус невід'ємний).",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "SOLVE",
        "text": r"$\sin\alpha = \frac{\sqrt2}{2}$, $0^\circ \le \alpha \le 180^\circ$. Знайдіть $\alpha$.",
        "options": [(r"$45^\circ$ або $135^\circ$", True), (r"лише $45^\circ$", False), (r"лише $135^\circ$", False), (r"$45^\circ$ або $-45^\circ$", False)],
        "solution": r"$\sin 45^\circ = \sin 135^\circ = \frac{\sqrt2}{2}$. Обидва кути з проміжку $[0^\circ;\,180^\circ]$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Обчисліть $2\sin 150^\circ - 4\cos 120^\circ + \operatorname{tg} 135^\circ$.",
        "answer": "2",
        "solution": r"$2 \cdot \frac12 - 4 \cdot \left(-\frac12\right) + (-1) = 1 + 2 - 1 = 2$.",
    },
    {
        "type": "ORDER", "difficulty": 2, "skill": "SOLVE",
        "text": r"Розташуйте числа в порядку зростання.",
        "items": [r"$\cos 180^\circ$", r"$\cos 135^\circ$", r"$\cos 90^\circ$", r"$\sin 30^\circ$", r"$\sin 90^\circ$"],
        "solution": r"$-1 \lt -\frac{\sqrt2}{2} \lt 0 \lt \frac12 \lt 1$.",
    },
    # --- Аналіз результатів ---
    {
        "type": "ERROR", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Учень знаходив $\cos\alpha$, якщо $\sin\alpha = \frac{5}{13}$ і $\alpha$ — тупий. У якому кроці помилка?",
        "steps": [r"$\cos^2\alpha = 1 - \frac{25}{169} = \frac{144}{169}$", r"$\cos\alpha = \pm\frac{12}{13}$", r"$\cos\alpha = \frac{12}{13}$, бо корінь додатний"],
        "wrong": 2,
        "solution": r"Для тупого кута косинус від'ємний: $\cos\alpha = -\frac{12}{13}$.",
    },
    {
        "type": "TF", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [(r"Кут $\alpha \in [0^\circ;\,180^\circ]$ однозначно визначається своїм косинусом", True),
                       (r"Кут $\alpha \in [0^\circ;\,180^\circ]$ однозначно визначається своїм синусом", False),
                       (r"Якщо $\operatorname{tg}\alpha \lt 0$, то кут $\alpha$ тупий", True)],
        "solution": r"Різним кутам відповідають різні абсциси точок півкола, а ординати повторюються: $\sin 30^\circ = \sin 150^\circ$. Від'ємний тангенс — від'ємний косинус — тупий кут.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Чи існує кут $\alpha$, для якого $\sin\alpha = \frac35$ і $\cos\alpha = -\frac35$?",
        "options": [(r"Ні: $\sin^2\alpha + \cos^2\alpha \ne 1$", True), (r"Так, тупий кут", False), (r"Так, $\alpha = 135^\circ$", False), (r"Так, гострий кут", False)],
        "solution": r"$\frac{9}{25} + \frac{9}{25} = \frac{18}{25} \ne 1$ — такого кута немає. (Для $135^\circ$ обидва модулі дорівнюють $\frac{\sqrt2}{2}$.)",
    },
    {
        "type": "MULTI", "difficulty": 2, "skill": "ANALYZE",
        "text": r"$\cos\alpha = -0{,}3$. Що можна стверджувати?",
        "options": [(r"$\alpha$ — тупий кут", True), (r"$\sin\alpha \gt 0$", True), (r"$\operatorname{tg}\alpha \lt 0$", True), (r"$\cos(180^\circ - \alpha) = -0{,}3$", False), (r"$\sin\alpha = 0{,}7$", False)],
        "solution": r"Від'ємний косинус — тупий кут, синус додатний, тангенс від'ємний. $\cos(180^\circ - \alpha) = 0{,}3$. $\sin\alpha = \sqrt{1 - 0{,}09} = \sqrt{0{,}91} \ne 0{,}7$.",
    },
    {
        "type": "GROUP", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Розподіліть рівності: правильні чи хибні?",
        "groups": ["правильна", "хибна"],
        "items": [(r"$\sin 160^\circ = \sin 20^\circ$", 0), (r"$\cos 160^\circ = -\cos 20^\circ$", 0), (r"$\operatorname{tg} 160^\circ = -\operatorname{tg} 20^\circ$", 0),
                  (r"$\sin 160^\circ = -\sin 20^\circ$", 1), (r"$\cos 160^\circ = \cos 20^\circ$", 1), (r"$\cos 160^\circ = \sin 20^\circ$", 1)],
        "solution": r"$160^\circ = 180^\circ - 20^\circ$: синус зберігається, косинус і тангенс змінюють знак.",
    },

    # ==========================================
    # СХОДИНКА 3 — ПІДВИЩЕНИЙ
    # ==========================================
    # --- Моделювання ---
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"Точка $M(-5;\,12)$. Знайдіть косинус кута між променем $OM$ і додатною піввіссю $Ox$ (звичайним дробом, наприклад 3/4).",
        "answer": "-5/13",
        "solution": r"$OM = \sqrt{25 + 144} = 13$. $\cos\alpha = \frac{x}{OM} = -\frac{5}{13}$.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "MODEL",
        "text": r"Пряма $y = -x$ утворює з додатною піввіссю $Ox$ (у верхній півплощині) кут …",
        "options": [(r"$135^\circ$", True), (r"$45^\circ$", False), (r"$-45^\circ$", False), (r"$120^\circ$", False)],
        "solution": r"Точка $(-1;\,1)$ лежить на прямій: $\operatorname{tg}\alpha = \frac{1}{-1} = -1$, $\alpha = 135^\circ$.",
    },
    {
        "type": "TF", "difficulty": 3, "skill": "MODEL",
        "text": r"У трикутнику $ABC$ кути $A$, $B$, $C$. Правда чи ні?",
        "statements": [(r"$\sin(A + B) = \sin C$", True), (r"$\cos(A + B) = \cos C$", False),
                       (r"Серед $\cos A$, $\cos B$, $\cos C$ від'ємним може бути щонайбільше один", True)],
        "solution": r"$A + B = 180^\circ - C$: $\sin(A + B) = \sin C$, $\cos(A + B) = -\cos C$. Тупих кутів у трикутнику щонайбільше один.",
    },
    {
        "type": "FIELDS", "difficulty": 3, "skill": "MODEL",
        "text": r"Точку $A(2;\,0)$ повернули навколо початку координат на $135^\circ$ проти годинникової стрілки. Отримали точку $B(-\sqrt{p};\,\sqrt{q})$. Знайдіть $p$ і $q$.",
        "fields": [(r"$p =$", "2"), (r"$q =$", "2")],
        "solution": r"$B(2\cos 135^\circ;\,2\sin 135^\circ) = (-\sqrt2;\,\sqrt2)$.",
    },
    {
        "type": "MATCH", "difficulty": 3, "skill": "MODEL",
        "text": r"Установіть відповідність між точкою $M$ (1–3) та кутом між променем $OM$ і додатною піввіссю $Ox$ (А–Д).",
        "options": [r"А) $120^\circ$", r"Б) $150^\circ$", r"В) $135^\circ$", r"Г) $60^\circ$", r"Д) $90^\circ$"],
        "matches": [(r"1. $M(-1;\,\sqrt3)$", r"А) $120^\circ$"), (r"2. $M(-3;\,\sqrt3)$", r"Б) $150^\circ$"), (r"3. $M(0;\,5)$", r"Д) $90^\circ$")],
        "solution": r"1) $OM = 2$, $\cos\alpha = -\frac12$ — $120^\circ$. 2) $OM = \sqrt{12} = 2\sqrt3$, $\cos\alpha = -\frac{3}{2\sqrt3} = -\frac{\sqrt3}{2}$ — $150^\circ$. 3) Точка на осі $Oy$ — $90^\circ$.",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"$\operatorname{tg}\alpha = -\frac34$, $0^\circ \lt \alpha \lt 180^\circ$. Знайдіть $\cos\alpha$.",
        "answer": "-0,8",
        "solution": r"Тангенс від'ємний — кут тупий. Візьмемо точку $(-4;\,3)$: $r = 5$, $\cos\alpha = -\frac45 = -0{,}8$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Обчисліть $\sin 20^\circ + \sin 160^\circ - 2\sin 20^\circ + \cos 70^\circ + \cos 110^\circ$.",
        "answer": "0",
        "solution": r"$\sin 160^\circ = \sin 20^\circ$, $\cos 110^\circ = -\cos 70^\circ$. Сума: $\sin 20^\circ + \sin 20^\circ - 2\sin 20^\circ + 0 = 0$.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "SOLVE",
        "text": r"$\sin\alpha = \frac{12}{13}$, $\alpha$ — тупий. Знайдіть $\operatorname{tg}\alpha$.",
        "options": [(r"$-\frac{12}{5}$", True), (r"$\frac{12}{5}$", False), (r"$-\frac{5}{12}$", False), (r"$-\frac{12}{13}$", False), (r"$\frac{5}{13}$", False)],
        "solution": r"$\cos\alpha = -\frac{5}{13}$ (тупий кут). $\operatorname{tg}\alpha = \frac{12}{13} : \left(-\frac{5}{13}\right) = -\frac{12}{5}$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Обчисліть $\cos^2 150^\circ - \sin^2 120^\circ + \operatorname{tg}^2 120^\circ$.",
        "answer": "3",
        "solution": r"$\cos^2 150^\circ = \frac34$, $\sin^2 120^\circ = \frac34$, $\operatorname{tg}^2 120^\circ = 3$. Разом $3$.",
    },
    {
        "type": "MULTI", "difficulty": 3, "skill": "SOLVE",
        "text": r"Які кути $\alpha \in [0^\circ;\,180^\circ]$ задовольняють рівняння $2\sin^2\alpha = 1$?",
        "options": [(r"$45^\circ$", True), (r"$135^\circ$", True), (r"$30^\circ$", False), (r"$90^\circ$", False), (r"$150^\circ$", False)],
        "solution": r"$\sin^2\alpha = \frac12$, $\sin\alpha = \frac{\sqrt2}{2}$ (синус невід'ємний): $\alpha = 45^\circ$ або $135^\circ$.",
    },
    # --- Аналіз результатів ---
    {
        "type": "ERROR", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Учень розв'язував: «У трикутнику $\sin A = \frac12$. Знайдіть $A$». У якому кроці помилка?",
        "steps": [r"$\sin 30^\circ = \frac12$", r"Кут $A$ — кут трикутника, тож $0^\circ \lt A \lt 180^\circ$", r"Отже, $A = 30^\circ$ — єдина відповідь"],
        "wrong": 2,
        "solution": r"$\sin 150^\circ = \frac12$ теж, і кут $150^\circ$ у трикутнику можливий. Відповідь: $30^\circ$ або $150^\circ$ (без додаткових даних).",
    },
    {
        "type": "TF", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [(r"$\sin\alpha + \cos\alpha$ може бути від'ємним для деякого $\alpha \in [0^\circ;\,180^\circ]$", True),
                       (r"$\sin\alpha \cdot \cos\alpha \le 0$ для будь-якого тупого кута", True),
                       (r"Для будь-якого $\alpha \in [0^\circ;\,180^\circ]$ виконується $\sin\alpha \ge \cos\alpha$", False)],
        "solution": r"$\alpha = 180^\circ$: $0 + (-1) = -1 \lt 0$. Для тупого кута синус додатний, косинус від'ємний. $\alpha = 0^\circ$: $0 \lt 1$.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "ANALYZE",
        "text": r"У трикутнику $ABC$: $\cos A = -0{,}2$. Яким може бути кут $B$?",
        "options": [("лише гострим", True), ("гострим або тупим", False), ("лише тупим", False), ("прямим", False)],
        "solution": r"$\cos A \lt 0$ — кут $A$ тупий. У трикутнику лише один тупий кут, а прямого разом із тупим бути не може: $B$ гострий.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Скільки кутів $\alpha \in [0^\circ;\,180^\circ]$ задовольняють рівність $\sin\alpha = \frac{1}{3}$?",
        "answer": "2",
        "solution": r"Пряма $y = \frac13$ перетинає одиничне півколо у двох точках: кути $\alpha$ і $180^\circ - \alpha$.",
    },
    {
        "type": "GROUP", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Кут $\alpha \in [0^\circ;\,180^\circ]$. Розподіліть умови за тим, скільки кутів $\alpha$ їм відповідає.",
        "groups": ["жодного", "один", "два"],
        "items": [(r"$\sin\alpha = -\frac12$", 0), (r"$\cos\alpha = 1{,}2$", 0), (r"$\cos\alpha = -0{,}4$", 1), (r"$\sin\alpha = 1$", 1),
                  (r"$\operatorname{tg}\alpha = 5$", 1), (r"$\sin\alpha = 0{,}9$", 2)],
        "solution": r"$\sin\alpha \ge 0$ і $|\cos\alpha| \le 1$ — перші дві умови неможливі. Косинус і тангенс визначають кут однозначно; $\sin\alpha = 1$ лише при $90^\circ$. $\sin\alpha = 0{,}9$ — гострий і тупий кути.",
    },

    # ==========================================
    # БОСИ
    # ==========================================
    {
        "type": "SHORT", "difficulty": 4, "skill": "SOLVE",
        "text": r"$\sin\alpha + \cos\alpha = \frac15$, $0^\circ \lt \alpha \lt 180^\circ$. Знайдіть $\operatorname{tg}\alpha$ (звичайним дробом, наприклад 3/4).",
        "answer": "-4/3",
        "solution": r"$(\sin\alpha + \cos\alpha)^2 = \frac1{25}$, $1 + 2\sin\alpha\cos\alpha = \frac1{25}$, $\sin\alpha\cos\alpha = -\frac{12}{25}$ — кут тупий. $\sin\alpha$, $\cos\alpha$ — корені $t^2 - \frac15 t - \frac{12}{25} = 0$: $t = \frac45$ або $t = -\frac35$. $\sin\alpha = \frac45$, $\cos\alpha = -\frac35$, $\operatorname{tg}\alpha = -\frac43$.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "MODEL",
        "text": r"Знайдіть площу трикутника з вершинами $O(0;\,0)$, $A(4;\,0)$ і точкою $B$, яку отримали поворотом точки $(6;\,0)$ на $150^\circ$ проти годинникової стрілки навколо $O$.",
        "answer": "6",
        "solution": r"$B(6\cos 150^\circ;\,6\sin 150^\circ) = (-3\sqrt3;\,3)$. Основа $OA = 4$ на осі $Ox$, висота — ордината $B$: $3$. $S = \frac12 \cdot 4 \cdot 3 = 6$.",
    },
    {
        "type": "CHOICE", "difficulty": 4, "skill": "ANALYZE",
        "text": r"Порівняйте $\sin 100^\circ$ і $\sin 70^\circ$.",
        "options": [(r"$\sin 100^\circ \gt \sin 70^\circ$", True), (r"$\sin 100^\circ \lt \sin 70^\circ$", False), (r"$\sin 100^\circ = \sin 70^\circ$", False), ("порівняти неможливо", False)],
        "solution": r"$\sin 100^\circ = \sin 80^\circ$. На $[0^\circ;\,90^\circ]$ синус зростає: $\sin 80^\circ \gt \sin 70^\circ$.",
    },
    {
        "type": "TF", "difficulty": 4, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [(r"$\cos 1^\circ + \cos 2^\circ + \ldots + \cos 179^\circ = 0$", True),
                       (r"$\sin 1^\circ + \sin 2^\circ + \ldots + \sin 179^\circ \gt 0$", True),
                       (r"$\operatorname{tg} 10^\circ \cdot \operatorname{tg} 170^\circ \gt 0$", False),
                       (r"$\cos 50^\circ + \cos 130^\circ = 0$", True)],
        "solution": r"$\cos(180^\circ - \alpha) = -\cos\alpha$: доданки скорочуються парами, $\cos 90^\circ = 0$. Усі синуси додатні. $\operatorname{tg} 170^\circ = -\operatorname{tg} 10^\circ$, добуток від'ємний. $\cos 130^\circ = -\cos 50^\circ$.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "SOLVE",
        "text": r"Обчисліть $\operatorname{tg} 10^\circ \cdot \operatorname{tg} 20^\circ \cdot \operatorname{tg} 70^\circ \cdot \operatorname{tg} 80^\circ \cdot \operatorname{tg} 135^\circ$.",
        "answer": "-1",
        "solution": r"$\operatorname{tg}(90^\circ - \alpha) = \frac{\cos\alpha}{\sin\alpha} = \frac{1}{\operatorname{tg}\alpha}$, тому $\operatorname{tg} 10^\circ \operatorname{tg} 80^\circ = 1$, $\operatorname{tg} 20^\circ \operatorname{tg} 70^\circ = 1$. $\operatorname{tg} 135^\circ = -1$. Добуток $-1$.",
    },

    # ==========================================
    # УЛЬТРА-БОСИ
    # ==========================================
    {
        "type": "SHORT", "difficulty": 5, "skill": "ANALYZE",
        "text": r"Знайдіть найбільше значення виразу $3\sin\alpha - \cos^2\alpha$ для $\alpha \in [0^\circ;\,180^\circ]$.",
        "answer": "3",
        "solution": r"$3\sin\alpha - (1 - \sin^2\alpha) = \sin^2\alpha + 3\sin\alpha - 1$. При $t = \sin\alpha \in [0;\,1]$ функція $t^2 + 3t - 1$ зростає, найбільше значення при $t = 1$ ($\alpha = 90^\circ$): $1 + 3 - 1 = 3$.",
    },
    {
        "type": "SHORT", "difficulty": 5, "skill": "SOLVE",
        "text": r"$\operatorname{tg}\alpha = -2$, $0^\circ \lt \alpha \lt 180^\circ$. Знайдіть $\dfrac{\sin\alpha + 3\cos\alpha}{2\sin\alpha - \cos\alpha}$.",
        "answer": "-0,2",
        "solution": r"Поділимо чисельник і знаменник на $\cos\alpha \ne 0$: $\dfrac{\operatorname{tg}\alpha + 3}{2\operatorname{tg}\alpha - 1} = \dfrac{-2 + 3}{-4 - 1} = -\frac15 = -0{,}2$.",
    },
]
