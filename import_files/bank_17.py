TOPIC_NAME = "17. Тригонометричні вирази"
TASKS = [
    # ==========================================
    # ТЕСТОВІ ЗАВДАННЯ (CHOICE) - 30 шт.
    # ==========================================
    {
        "type": "CHOICE",
        "difficulty": 1,
        "text": r"Обчисліть значення $\sin 30^\circ$.",
        "svg_code": "",
        "options": [
            (r"А) $1$", False),
            (r"Б) $\frac{\sqrt{2}}{2}$", False),
            (r"В) $\frac{1}{2}$", True),
            (r"Г) $\frac{\sqrt{3}}{2}$", False),
            (r"Д) $0$", False)
        ],
        "topic_tags": ["17. Тригонометричні вирази"]
    },
    {
        "type": "CHOICE",
        "difficulty": 1,
        "text": r"Обчисліть значення $\cos 60^\circ$.",
        "svg_code": "",
        "options": [
            (r"А) $\frac{\sqrt{3}}{2}$", False),
            (r"Б) $1$", False),
            (r"В) $\frac{\sqrt{2}}{2}$", False),
            (r"Г) $0$", False),
            (r"Д) $\frac{1}{2}$", True)
        ],
        "topic_tags": ["17. Тригонометричні вирази"]
    },
    {
        "type": "CHOICE",
        "difficulty": 1,
        "text": r"Чому дорівнює $\text{tg } 45^\circ$?",
        "svg_code": "",
        "options": [
            (r"А) $\frac{\sqrt{3}}{3}$", False),
            (r"Б) $1$", True),
            (r"В) $\sqrt{3}$", False),
            (r"Г) $0$", False),
            (r"Д) Не існує", False)
        ],
        "topic_tags": ["17. Тригонометричні вирази"]
    },
    {
        "type": "CHOICE",
        "difficulty": 1,
        "text": r"Який знак має $\sin 150^\circ$?",
        "svg_code": "",
        "options": [
            (r"А) Додатний", True),
            (r"Б) Від'ємний", False),
            (r"В) Дорівнює нулю", False),
            (r"Г) Не існує", False),
            (r"Д) Залежить від косинуса", False)
        ],
        "topic_tags": ["17. Тригонометричні вирази"]
    },
    {
        "type": "CHOICE",
        "difficulty": 1,
        "text": r"Який знак має $\cos 210^\circ$?",
        "svg_code": "",
        "options": [
            (r"А) Додатний", False),
            (r"Б) Від'ємний", True),
            (r"В) Дорівнює нулю", False),
            (r"Г) Не існує", False),
            (r"Д) Знак постійно змінюється", False)
        ],
        "topic_tags": ["17. Тригонометричні вирази"]
    },
    {
        "type": "CHOICE",
        "difficulty": 1,
        "text": r"Спростіть вираз: $\sin^2 \alpha + \cos^2 \alpha$.",
        "svg_code": "",
        "options": [
            (r"А) $0$", False),
            (r"Б) $-1$", False),
            (r"В) $\text{tg}^2 \alpha$", False),
            (r"Г) $1$", True),
            (r"Д) $\cos 2\alpha$", False)
        ],
        "topic_tags": ["17. Тригонометричні вирази"]
    },
    {
        "type": "CHOICE",
        "difficulty": 1,
        "text": r"Спростіть вираз: $1 - \sin^2 \alpha$.",
        "svg_code": "",
        "options": [
            (r"А) $\sin^2 \alpha$", False),
            (r"Б) $\cos^2 \alpha$", True),
            (r"В) $-\cos^2 \alpha$", False),
            (r"Г) $1$", False),
            (r"Д) $\text{tg}^2 \alpha$", False)
        ],
        "topic_tags": ["17. Тригонометричні вирази"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"Знайдіть $\cos \alpha$, якщо $\sin \alpha = 0{,}6$ і $\alpha \in \left(\frac{\pi}{2}; \pi\right)$.",
        "svg_code": "",
        "options": [
            (r"А) $0{,}8$", False),
            (r"Б) $-0{,}8$", True),
            (r"В) $0{,}4$", False),
            (r"Г) $-0{,}4$", False),
            (r"Д) $-0{,}64$", False)
        ],
        "topic_tags": ["17. Тригонометричні вирази"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"За формулами зведення, чому дорівнює $\sin(180^\circ - \alpha)$?",
        "svg_code": "",
        "options": [
            (r"А) $\cos \alpha$", False),
            (r"Б) $-\cos \alpha$", False),
            (r"В) $\sin \alpha$", True),
            (r"Г) $-\sin \alpha$", False),
            (r"Д) $\text{tg } \alpha$", False)
        ],
        "topic_tags": ["17. Тригонометричні вирази"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"За формулами зведення, чому дорівнює $\cos(90^\circ + \alpha)$?",
        "svg_code": "",
        "options": [
            (r"А) $\sin \alpha$", False),
            (r"Б) $-\sin \alpha$", True),
            (r"В) $\cos \alpha$", False),
            (r"Г) $-\cos \alpha$", False),
            (r"Д) $1$", False)
        ],
        "topic_tags": ["17. Тригонометричні вирази"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"Чому дорівнює $\text{tg}(180^\circ - \alpha)$?",
        "svg_code": "",
        "options": [
            (r"А) $\text{tg } \alpha$", False),
            (r"Б) $-\text{tg } \alpha$", True),
            (r"В) $\frac{1}{\text{tg } \alpha}$", False),
            (r"Г) $-\frac{1}{\text{tg } \alpha}$", False),
            (r"Д) $\sin \alpha$", False)
        ],
        "topic_tags": ["17. Тригонометричні вирази"]
    },
    {
        "type": "CHOICE",
        "difficulty": 1,
        "text": r"Спростіть вираз: $2\sin \alpha \cos \alpha$.",
        "svg_code": "",
        "options": [
            (r"А) $\sin 2\alpha$", True),
            (r"Б) $\cos 2\alpha$", False),
            (r"В) $1$", False),
            (r"Г) $\text{tg } 2\alpha$", False),
            (r"Д) $\sin^2 \alpha$", False)
        ],
        "topic_tags": ["17. Тригонометричні вирази"]
    },
    {
        "type": "CHOICE",
        "difficulty": 1,
        "text": r"Спростіть вираз: $\cos^2 \alpha - \sin^2 \alpha$.",
        "svg_code": "",
        "options": [
            (r"А) $1$", False),
            (r"Б) $\sin 2\alpha$", False),
            (r"В) $\cos 2\alpha$", True),
            (r"Г) $-1$", False),
            (r"Д) $0$", False)
        ],
        "topic_tags": ["17. Тригонометричні вирази"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"Обчисліть: $\sin\left(\frac{\pi}{6}\right) + \cos\left(\frac{\pi}{3}\right)$.",
        "svg_code": "",
        "options": [
            (r"А) $\sqrt{3}$", False),
            (r"Б) $1$", True),
            (r"В) $\frac{\sqrt{3}+1}{2}$", False),
            (r"Г) $0$", False),
            (r"Д) $2$", False)
        ],
        "topic_tags": ["17. Тригонометричні вирази", "1. Числові множини"]
    },
    {
        "type": "CHOICE",
        "difficulty": 1,
        "text": r"Яка тригонометрична функція є парною?",
        "svg_code": "",
        "options": [
            (r"А) $y = \sin x$", False),
            (r"Б) $y = \text{tg } x$", False),
            (r"В) $y = \cos x$", True),
            (r"Г) Всі базові функції парні", False),
            (r"Д) Жодна з перелічених", False)
        ],
        "topic_tags": ["17. Тригонометричні вирази", "11. Функції та їх властивості"]
    },
    {
        "type": "CHOICE",
        "difficulty": 1,
        "text": r"Спростіть вираз $\cos(-\alpha)$.",
        "svg_code": "",
        "options": [
            (r"А) $-\cos \alpha$", False),
            (r"Б) $\cos \alpha$", True),
            (r"В) $\sin \alpha$", False),
            (r"Г) $-\sin \alpha$", False),
            (r"Д) $1 - \cos \alpha$", False)
        ],
        "topic_tags": ["17. Тригонометричні вирази"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"Обчисліть $\arcsin\left(\frac{1}{2}\right)$.",
        "svg_code": "",
        "options": [
            (r"А) $\frac{\pi}{3}$", False),
            (r"Б) $\frac{\pi}{6}$", True),
            (r"В) $\frac{\pi}{4}$", False),
            (r"Г) $\frac{\pi}{2}$", False),
            (r"Д) $0$", False)
        ],
        "topic_tags": ["17. Тригонометричні вирази"]
    },
    {
        "type": "CHOICE",
        "difficulty": 3,
        "text": r"Обчисліть $\arccos\left(-\frac{1}{2}\right)$.",
        "svg_code": "",
        "options": [
            (r"А) $-\frac{\pi}{3}$", False),
            (r"Б) $\frac{2\pi}{3}$", True),
            (r"В) $\frac{5\pi}{6}$", False),
            (r"Г) $-\frac{\pi}{6}$", False),
            (r"Д) $\frac{\pi}{3}$", False)
        ],
        "topic_tags": ["17. Тригонометричні вирази"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"Обчисліть $\arcsin(-1)$.",
        "svg_code": "",
        "options": [
            (r"А) $\pi$", False),
            (r"Б) $\frac{3\pi}{2}$", False),
            (r"В) $-\frac{\pi}{2}$", True),
            (r"Г) $\frac{\pi}{2}$", False),
            (r"Д) $0$", False)
        ],
        "topic_tags": ["17. Тригонометричні вирази"]
    },
    {
        "type": "CHOICE",
        "difficulty": 1,
        "text": r"Який найменший додатний період функції $y = \sin x$?",
        "svg_code": "",
        "options": [
            (r"А) $\pi$", False),
            (r"Б) $\frac{\pi}{2}$", False),
            (r"В) $2\pi$", True),
            (r"Г) $4\pi$", False),
            (r"Д) Не має періоду", False)
        ],
        "topic_tags": ["17. Тригонометричні вирази", "11. Функції та їх властивості"]
    },
    {
        "type": "CHOICE",
        "difficulty": 1,
        "text": r"Який найменший додатний період функції $y = \text{tg } x$?",
        "svg_code": "",
        "options": [
            (r"А) $2\pi$", False),
            (r"Б) $\pi$", True),
            (r"В) $\frac{\pi}{2}$", False),
            (r"Г) $\frac{\pi}{4}$", False),
            (r"Д) $3\pi$", False)
        ],
        "topic_tags": ["17. Тригонометричні вирази", "11. Функції та їх властивості"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"Знайдіть множину значень функції $y = 4\cos x$.",
        "svg_code": "",
        "options": [
            (r"А) $[-1; 1]$", False),
            (r"Б) $[0; 4]$", False),
            (r"В) $[-4; 4]$", True),
            (r"Г) $(-\infty; +\infty)$", False),
            (r"Д) $[1; 4]$", False)
        ],
        "topic_tags": ["17. Тригонометричні вирази", "11. Функції та їх властивості"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"Спростіть вираз $(1 - \cos \alpha)(1 + \cos \alpha)$.",
        "svg_code": "",
        "options": [
            (r"А) $\cos^2 \alpha$", False),
            (r"Б) $1$", False),
            (r"В) $\sin^2 \alpha$", True),
            (r"Г) $-\sin^2 \alpha$", False),
            (r"Д) $1 + \cos^2 \alpha$", False)
        ],
        "topic_tags": ["17. Тригонометричні вирази", "4. Одночлени, многочлени та формули скороченого множення"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"Знайдіть найбільше значення функції $y = 2 - \sin x$.",
        "svg_code": "",
        "options": [
            (r"А) $1$", False),
            (r"Б) $2$", False),
            (r"В) $3$", True),
            (r"Г) $0$", False),
            (r"Д) $4$", False)
        ],
        "topic_tags": ["17. Тригонометричні вирази", "11. Функції та їх властивості"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"Обчисліть $\cos 120^\circ$.",
        "svg_code": "",
        "options": [
            (r"А) $\frac{1}{2}$", False),
            (r"Б) $-\frac{1}{2}$", True),
            (r"В) $\frac{\sqrt{3}}{2}$", False),
            (r"Г) $-\frac{\sqrt{3}}{2}$", False),
            (r"Д) $-\frac{\sqrt{2}}{2}$", False)
        ],
        "topic_tags": ["17. Тригонометричні вирази"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"Обчисліть $\sin 180^\circ + \cos 270^\circ$.",
        "svg_code": "",
        "options": [
            (r"А) $0$", True),
            (r"Б) $1$", False),
            (r"В) $-1$", False),
            (r"Г) $2$", False),
            (r"Д) $-2$", False)
        ],
        "topic_tags": ["17. Тригонометричні вирази"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"Обчисліть $\text{tg } \frac{\pi}{3}$.",
        "svg_code": "",
        "options": [
            (r"А) $\frac{\sqrt{3}}{3}$", False),
            (r"Б) $1$", False),
            (r"В) $\sqrt{3}$", True),
            (r"Г) $0$", False),
            (r"Д) Не існує", False)
        ],
        "topic_tags": ["17. Тригонометричні вирази"]
    },
    {
        "type": "CHOICE",
        "difficulty": 1,
        "text": r"Яка з наведених формул є хибною?",
        "svg_code": "",
        "options": [
            (r"А) $\cos(-\alpha) = \cos \alpha$", False),
            (r"Б) $\sin(-\alpha) = \sin \alpha$", True),
            (r"В) $\text{tg}(-\alpha) = -\text{tg } \alpha$", False),
            (r"Г) $\sin^2 \alpha + \cos^2 \alpha = 1$", False),
            (r"Д) $\sin 2\alpha = 2\sin\alpha\cos\alpha$", False)
        ],
        "topic_tags": ["17. Тригонометричні вирази"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"Яка область визначення функції $y = \text{tg } x$?",
        "svg_code": "",
        "options": [
            (r"А) Всі дійсні числа", False),
            (r"Б) $x \neq \pi k, \quad k \in Z$", False),
            (r"В) $x \neq \frac{\pi}{2} + \pi k, \quad k \in Z$", True),
            (r"Г) $x > 0$", False),
            (r"Д) $[-1; 1]$", False)
        ],
        "topic_tags": ["17. Тригонометричні вирази", "11. Функції та їх властивості"]
    },
    {
        "type": "CHOICE",
        "difficulty": 3,
        "text": r"Спростіть дріб $\frac{\sin 2\alpha}{2\cos \alpha}$.",
        "svg_code": "",
        "options": [
            (r"А) $\cos \alpha$", False),
            (r"Б) $\sin \alpha$", True),
            (r"В) $\text{tg } \alpha$", False),
            (r"Г) $1$", False),
            (r"Д) $2\sin \alpha$", False)
        ],
        "topic_tags": ["17. Тригонометричні вирази", "8. Дробово-раціональні рівняння"]
    },

    # ==========================================
    # ЗАВДАННЯ НА ВІДПОВІДНІСТЬ (MATCH) - 4 шт.
    # ==========================================
    {
        "type": "MATCH",
        "difficulty": 1,
        "text": r"Узгодьте радіанну міру кута (1–3) із його градусною мірою (А–Д).",
        "svg_code": "",
        "options": [
            r"А) $30^\circ$",
            r"Б) $45^\circ$",
            r"В) $60^\circ$",
            r"Г) $180^\circ$",
            r"Д) $270^\circ$"
        ],
        "matches": [
            (r"1. $\frac{\pi}{6}$", r"А) $30^\circ$"),
            (r"2. $\frac{\pi}{4}$", r"Б) $45^\circ$"),
            (r"3. $\frac{3\pi}{2}$", r"Д) $270^\circ$")
        ],
        "topic_tags": ["17. Тригонометричні вирази"]
    },
    {
        "type": "MATCH",
        "difficulty": 2,
        "text": r"Узгодьте вираз, отриманий за допомогою формул зведення (1–3), із тотожно рівним йому (А–Д).",
        "svg_code": "",
        "options": [
            r"А) $\cos \alpha$",
            r"Б) $-\cos \alpha$",
            r"В) $\sin \alpha$",
            r"Г) $-\sin \alpha$",
            r"Д) $\text{tg } \alpha$"
        ],
        "matches": [
            (r"1. $\sin(90^\circ + \alpha)$", r"А) $\cos \alpha$"),
            (r"2. $\cos(180^\circ - \alpha)$", r"Б) $-\cos \alpha$"),
            (r"3. $\sin(180^\circ - \alpha)$", r"В) $\sin \alpha$")
        ],
        "topic_tags": ["17. Тригонометричні вирази"]
    },
    {
        "type": "MATCH",
        "difficulty": 2,
        "text": r"Узгодьте тригонометричний вираз (1–3) із його спрощеним виглядом (А–Д).",
        "svg_code": "",
        "options": [
            r"А) $\sin^2 \alpha$",
            r"Б) $\text{tg } \alpha$",
            r"В) $\sin 2\alpha$",
            r"Г) $\cos 2\alpha$",
            r"Д) $1$"
        ],
        "matches": [
            (r"1. $1 - \cos^2 \alpha$", r"А) $\sin^2 \alpha$"),
            (r"2. $\frac{\sin \alpha}{\cos \alpha}$", r"Б) $\text{tg } \alpha$"),
            (r"3. $2\sin \alpha \cos \alpha$", r"В) $\sin 2\alpha$")
        ],
        "topic_tags": ["17. Тригонометричні вирази"]
    },
    {
        "type": "MATCH",
        "difficulty": 3,
        "text": r"Узгодьте вираз з оберненою тригонометричною функцією (1–3) з його числовим значенням (А–Д).",
        "svg_code": "",
        "options": [
            r"А) $0$",
            r"Б) $\frac{\pi}{6}$",
            r"В) $\frac{\pi}{2}$",
            r"Г) $\pi$",
            r"Д) $-\frac{\pi}{2}$"
        ],
        "matches": [
            (r"1. $\arcsin(1)$", r"В) $\frac{\pi}{2}$"),
            (r"2. $\arcsin(0)$", r"А) $0$"),
            (r"3. $\arccos(-1)$", r"Г) $\pi$")
        ],
        "topic_tags": ["17. Тригонометричні вирази"]
    },

    # ==========================================
    # КОРОТКА ВІДПОВІДЬ (SHORT) - 4 шт.
    # ==========================================
    {
        "type": "SHORT",
        "difficulty": 2,
        "text": r"Обчисліть значення виразу: $4\sin 30^\circ + 2\cos 60^\circ - \text{tg } 45^\circ$.",
        "svg_code": "",
        "answer": "2",
        "topic_tags": ["17. Тригонометричні вирази"]
    },
    {
        "type": "SHORT",
        "difficulty": 3,
        "text": r"Знайдіть значення виразу $25 \cos^2 \alpha$, якщо відомо, що $\sin \alpha = 0{,}8$.",
        "svg_code": "",
        "answer": "9",
        "topic_tags": ["17. Тригонометричні вирази"]
    },
    {
        "type": "SHORT",
        "difficulty": 3,
        "text": r"Обчисліть значення виразу $\frac{12}{\pi} \cdot \arccos\left(-\frac{1}{2}\right)$.",
        "svg_code": "",
        "answer": "8",
        "topic_tags": ["17. Тригонометричні вирази"]
    },
    {
        "type": "SHORT",
        "difficulty": 3,
        "text": r"Знайдіть найбільше значення функції $y = 9 - 3\sin x$.",
        "svg_code": "",
        "answer": "12",
        "topic_tags": ["17. Тригонометричні вирази", "11. Функції та їх властивості"]
    }
]