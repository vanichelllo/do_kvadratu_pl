TOPIC_NAME = "26. Похідна"
TASKS = [
    # ==========================================
    # ТЕСТОВІ ЗАВДАННЯ (CHOICE) - 30 шт.
    # ==========================================
    {
        "type": "CHOICE",
        "difficulty": 1,
        "text": r"Знайдіть похідну функції $f(x) = x^4$.",
        "svg_code": "",
        "options": [
            (r"А) $4x^3$", True),
            (r"Б) $4x^4$", False),
            (r"В) $x^3$", False),
            (r"Г) $3x^3$", False),
            (r"Д) $\frac{x^5}{5}$", False)
        ],
        "topic_tags": ["26. Похідна"]
    },
    {
        "type": "CHOICE",
        "difficulty": 1,
        "text": r"Знайдіть похідну функції $f(x) = 5x + 3$.",
        "svg_code": "",
        "options": [
            (r"А) $5x$", False),
            (r"Б) $3$", False),
            (r"В) $5$", True),
            (r"Г) $0$", False),
            (r"Д) $8$", False)
        ],
        "topic_tags": ["26. Похідна", "11. Функції та їх властивості"]
    },
    {
        "type": "CHOICE",
        "difficulty": 1,
        "text": r"Знайдіть похідну функції $f(x) = \sin x + \cos x$.",
        "svg_code": "",
        "options": [
            (r"А) $\cos x + \sin x$", False),
            (r"Б) $-\cos x - \sin x$", False),
            (r"В) $\cos x - \sin x$", True),
            (r"Г) $-\cos x + \sin x$", False),
            (r"Д) $1$", False)
        ],
        "topic_tags": ["26. Похідна", "17. Тригонометричні вирази"]
    },
    {
        "type": "CHOICE",
        "difficulty": 1,
        "text": r"Обчисліть $f'(1)$, якщо $f(x) = 3x^2 - 2x + 1$.",
        "svg_code": "",
        "options": [
            (r"А) $4$", True),
            (r"Б) $2$", False),
            (r"В) $6$", False),
            (r"Г) $1$", False),
            (r"Д) $3$", False)
        ],
        "topic_tags": ["26. Похідна"]
    },
    {
        "type": "CHOICE",
        "difficulty": 1,
        "text": r"Знайдіть похідну функції $f(x) = \frac{1}{x}$.",
        "svg_code": "",
        "options": [
            (r"А) $\ln x$", False),
            (r"Б) $-\frac{1}{x^2}$", True),
            (r"В) $\frac{1}{x^2}$", False),
            (r"Г) $-x^{-1}$", False),
            (r"Д) $1$", False)
        ],
        "topic_tags": ["26. Похідна"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"Знайдіть похідну функції $y = \sqrt{x} + 2x^3$.",
        "svg_code": "",
        "options": [
            (r"А) $\frac{1}{2\sqrt{x}} + 6x^2$", True),
            (r"Б) $\frac{1}{\sqrt{x}} + 5x^2$", False),
            (r"В) $\sqrt{x} + 6x^2$", False),
            (r"Г) $\frac{1}{2\sqrt{x}} + 2x^2$", False),
            (r"Д) $x^{-1/2} + 6x^3$", False)
        ],
        "topic_tags": ["26. Похідна"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"Знайдіть кутовий коефіцієнт дотичної до графіка функції $f(x) = x^2 - 4x + 3$ у точці з абсцисою $x_0 = 3$.",
        "svg_code": "",
        "options": [
            (r"А) $-1$", False),
            (r"Б) $0$", False),
            (r"В) $1$", False),
            (r"Г) $2$", True),
            (r"Д) $3$", False)
        ],
        "topic_tags": ["26. Похідна", "12. Квадратична функція"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"Тіло рухається прямолінійно за законом $s(t) = t^2 + 3t + 2$ ($s$ вимірюється в метрах, $t$ — у секундах). Знайдіть швидкість тіла в момент часу $t = 2$ с.",
        "svg_code": "",
        "options": [
            (r"А) $5$ м/с", False),
            (r"Б) $7$ м/с", True),
            (r"В) $12$ м/с", False),
            (r"Г) $4$ м/с", False),
            (r"Д) $9$ м/с", False)
        ],
        "topic_tags": ["26. Похідна"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"Знайдіть критичні точки функції $f(x) = x^3 - 3x^2$.",
        "svg_code": "",
        "options": [
            (r"А) $0; 2$", True),
            (r"Б) $0; 3$", False),
            (r"В) $-2; 2$", False),
            (r"Г) $2; 3$", False),
            (r"Д) Тільки $0$", False)
        ],
        "topic_tags": ["26. Похідна", "7. Квадратні рівняння"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"Знайдіть проміжки зростання функції $y = x^2 - 6x + 5$.",
        "svg_code": "",
        "options": [
            (r"А) $(-\infty; 3]$", False),
            (r"Б) $[3; +\infty)$", True),
            (r"В) $[5; +\infty)$", False),
            (r"Г) $(-\infty; 6]$", False),
            (r"Д) $(-\infty; +\infty)$", False)
        ],
        "topic_tags": ["26. Похідна", "12. Квадратична функція", "13. Лінійні нерівності"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"Знайдіть похідну функції $f(x) = e^x \cdot \sin x$.",
        "svg_code": "",
        "options": [
            (r"А) $e^x \cos x$", False),
            (r"Б) $e^x (\sin x - \cos x)$", False),
            (r"В) $e^x (\sin x + \cos x)$", True),
            (r"Г) $\cos x$", False),
            (r"Д) $x e^{x-1} \sin x + e^x \cos x$", False)
        ],
        "topic_tags": ["26. Похідна", "17. Тригонометричні вирази", "19. Показникові вирази"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"Обчисліть значення похідної функції $f(x) = \frac{x+1}{x-1}$ у точці $x_0 = 2$.",
        "svg_code": "",
        "options": [
            (r"А) $-2$", True),
            (r"Б) $2$", False),
            (r"В) $-1$", False),
            (r"Г) $0$", False),
            (r"Д) $1$", False)
        ],
        "topic_tags": ["26. Похідна", "8. Дробово-раціональні рівняння"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"Знайдіть похідну складеної функції $y = \cos(3x)$.",
        "svg_code": "",
        "options": [
            (r"А) $-\sin(3x)$", False),
            (r"Б) $\sin(3x)$", False),
            (r"В) $3\sin(3x)$", False),
            (r"Г) $-3\sin(3x)$", True),
            (r"Д) $-\frac{1}{3}\sin(3x)$", False)
        ],
        "topic_tags": ["26. Похідна", "17. Тригонометричні вирази"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"Знайдіть точку мінімуму функції $f(x) = x^2 - 4x + 3$.",
        "svg_code": "",
        "options": [
            (r"А) $x = 1$", False),
            (r"Б) $x = 3$", False),
            (r"В) $x = 2$", True),
            (r"Г) $x = -2$", False),
            (r"Д) $x = 4$", False)
        ],
        "topic_tags": ["26. Похідна", "12. Квадратична функція"]
    },
    {
        "type": "CHOICE",
        "difficulty": 3,
        "text": r"Напишіть рівняння дотичної до графіка функції $f(x) = x^2 - 2x$ у точці з абсцисою $x_0 = 2$.",
        "svg_code": "",
        "options": [
            (r"А) $y = 2x - 4$", True),
            (r"Б) $y = 2x$", False),
            (r"В) $y = 2x - 2$", False),
            (r"Г) $y = 4x - 4$", False),
            (r"Д) $y = -2x + 4$", False)
        ],
        "topic_tags": ["26. Похідна", "11. Функції та їх властивості"]
    },
    {
        "type": "CHOICE",
        "difficulty": 3,
        "text": r"Знайдіть найбільше значення функції $f(x) = -x^2 + 6x - 5$ на відрізку $[0; 4]$.",
        "svg_code": "",
        "options": [
            (r"А) $-5$", False),
            (r"Б) $3$", False),
            (r"В) $4$", True),
            (r"Г) $5$", False),
            (r"Д) $0$", False)
        ],
        "topic_tags": ["26. Похідна", "12. Квадратична функція"]
    },
    {
        "type": "CHOICE",
        "difficulty": 3,
        "text": r"Знайдіть похідну функції $y = \ln(x^2 + 1)$.",
        "svg_code": "",
        "options": [
            (r"А) $\frac{1}{x^2 + 1}$", False),
            (r"Б) $\frac{2x}{x^2 + 1}$", True),
            (r"В) $\frac{x}{x^2 + 1}$", False),
            (r"Г) $2x \ln(x^2 + 1)$", False),
            (r"Д) $\frac{1}{2x}$", False)
        ],
        "topic_tags": ["26. Похідна", "20. Логарифмічні вирази"]
    },
    {
        "type": "CHOICE",
        "difficulty": 3,
        "text": r"При яких значеннях $x$ похідна функції $f(x) = \frac{x^3}{3} - x$ дорівнює нулю?",
        "svg_code": "",
        "options": [
            (r"А) Тільки $0$", False),
            (r"Б) $1$ і $-1$", True),
            (r"В) Тільки $1$", False),
            (r"Г) Тільки $-1$", False),
            (r"Д) Рівняння не має розв'язків", False)
        ],
        "topic_tags": ["26. Похідна", "7. Квадратні рівняння"]
    },
    {
        "type": "CHOICE",
        "difficulty": 3,
        "text": r"Тіло рухається за законом $s(t) = 2t^3 - 3t^2 + 5$. Знайдіть прискорення тіла в момент часу $t = 2$ с.",
        "svg_code": "",
        "options": [
            (r"А) $12$ м/с$^2$", False),
            (r"Б) $24$ м/с$^2$", False),
            (r"В) $18$ м/с$^2$", True),
            (r"Г) $6$ м/с$^2$", False),
            (r"Д) $30$ м/с$^2$", False)
        ],
        "topic_tags": ["26. Похідна"]
    },
    {
        "type": "CHOICE",
        "difficulty": 3,
        "text": r"Скільки критичних точок має функція $y = x^4 - 2x^2 + 3$?",
        "svg_code": "",
        "options": [
            (r"А) Жодної", False),
            (r"Б) Одну", False),
            (r"В) Дві", False),
            (r"Г) Три", True),
            (r"Д) Чотири", False)
        ],
        "topic_tags": ["26. Похідна", "7. Квадратні рівняння"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"На рисунку зображено графік <strong>похідної</strong> $y=f'(x)$. У якій точці функція $f(x)$ набуває максимуму?",
        "svg_code": r"""
<svg viewBox="-4 -3 6 5" width="100%" height="200px" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <marker id="arrD" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4" markerHeight="4" orient="auto-start-reverse"><path d="M 0 1 L 10 5 L 0 9 z" fill="#7f8c8d" /></marker>
    </defs>
    <line x1="-4" y1="0" x2="2" y2="0" stroke="#7f8c8d" stroke-width="0.05" marker-end="url(#arrD)"/>
    <line x1="0" y1="2" x2="0" y2="-3" stroke="#7f8c8d" stroke-width="0.05" marker-end="url(#arrD)"/>

    <!-- Parabola opening upwards, roots at -3 and -1 -->
    <path d="M -3.5 -1.25 Q -2 2 -0.5 -1.25" fill="none" stroke="#e74c3c" stroke-width="0.08"/>

    <circle cx="-3" cy="0" r="0.08" fill="#333"/>
    <text x="-3" y="0.4" font-size="0.3" font-family="sans-serif" text-anchor="middle">-3</text>

    <circle cx="-1" cy="0" r="0.08" fill="#333"/>
    <text x="-1" y="0.4" font-size="0.3" font-family="sans-serif" text-anchor="middle">-1</text>

    <text x="-2" y="-1.5" font-size="0.3" font-family="sans-serif" fill="#e74c3c">y = f'(x)</text>
</svg>
        """,
        "options": [
            (r"А) $x = -1$", False),
            (r"Б) $x = -3$", True),
            (r"В) $x = -2$", False),
            (r"Г) $x = 0$", False),
            (r"Д) Неможливо визначити", False)
        ],
        "topic_tags": ["26. Похідна", "11. Функції та їх властивості"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"На рисунку зображено графік <strong>похідної</strong> $y=f'(x)$. На якому з проміжків функція $f(x)$ <strong>зростає</strong>?",
        "svg_code": r"""
<svg viewBox="-1 -3 6 5" width="100%" height="200px" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <marker id="arrD2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4" markerHeight="4" orient="auto-start-reverse"><path d="M 0 1 L 10 5 L 0 9 z" fill="#7f8c8d" /></marker>
    </defs>
    <line x1="-1" y1="0" x2="5" y2="0" stroke="#7f8c8d" stroke-width="0.05" marker-end="url(#arrD2)"/>
    <line x1="0" y1="2" x2="0" y2="-3" stroke="#7f8c8d" stroke-width="0.05" marker-end="url(#arrD2)"/>

    <!-- Parabola opening downwards, roots at 1 and 3 -->
    <path d="M 0.5 1.25 Q 2 -2 3.5 1.25" fill="none" stroke="#e74c3c" stroke-width="0.08"/>

    <circle cx="1" cy="0" r="0.08" fill="#333"/>
    <text x="1" y="0.4" font-size="0.3" font-family="sans-serif" text-anchor="middle">1</text>

    <circle cx="3" cy="0" r="0.08" fill="#333"/>
    <text x="3" y="0.4" font-size="0.3" font-family="sans-serif" text-anchor="middle">3</text>

    <text x="2" y="-1.5" font-size="0.3" font-family="sans-serif" fill="#e74c3c">y = f'(x)</text>
</svg>
        """,
        "options": [
            (r"А) $(-\infty; 1]$ та $[3; +\infty)$", False),
            (r"Б) $[1; 3]$", True),
            (r"В) $[2; +\infty)$", False),
            (r"Г) $(-\infty; 2]$", False),
            (r"Д) Тільки $[1; 2]$", False)
        ],
        "topic_tags": ["26. Похідна", "11. Функції та їх властивості"]
    },
    {
        "type": "CHOICE",
        "difficulty": 3,
        "text": r"Знайдіть проміжки спадання функції $y = \frac{x^2}{x-2}$.",
        "svg_code": "",
        "options": [
            (r"А) $[0; 2)$ та $(2; 4]$", True),
            (r"Б) $(-\infty; 0]$ та $[4; +\infty)$", False),
            (r"В) $(0; 4)$", False),
            (r"Г) $[2; 4]$", False),
            (r"Д) $(-\infty; 2)$", False)
        ],
        "topic_tags": ["26. Похідна", "8. Дробово-раціональні рівняння",
                       "14. Квадратичні нерівності. Дробово-раціональні нерівності"]
    },
    {
        "type": "CHOICE",
        "difficulty": 3,
        "text": r"Знайдіть найменше значення функції $f(x) = x^3 - 3x$ на відрізку $[0; 2]$.",
        "svg_code": "",
        "options": [
            (r"А) $0$", False),
            (r"Б) $-2$", True),
            (r"В) $2$", False),
            (r"Г) $-3$", False),
            (r"Д) $-4$", False)
        ],
        "topic_tags": ["26. Похідна"]
    },
    {
        "type": "CHOICE",
        "difficulty": 3,
        "text": r"Знайдіть абсцису точки на графіку функції $y = x^2 - 3x + 1$, у якій дотична паралельна прямій $y = x + 5$.",
        "svg_code": "",
        "options": [
            (r"А) $2$", True),
            (r"Б) $1$", False),
            (r"В) $-1$", False),
            (r"Г) $3$", False),
            (r"Д) $0$", False)
        ],
        "topic_tags": ["26. Похідна", "6. Лінійні рівняння. Лінійні рівняння з модулем",
                       "11. Функції та їх властивості"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"Обчисліть $f'(\frac{\pi}{4})$, якщо $f(x) = \operatorname{tg} x$.",
        "svg_code": "",
        "options": [
            (r"А) $1$", False),
            (r"Б) $2$", True),
            (r"В) $0{,}5$", False),
            (r"Г) $\sqrt{2}$", False),
            (r"Д) $0$", False)
        ],
        "topic_tags": ["26. Похідна", "17. Тригонометричні вирази"]
    },
    {
        "type": "CHOICE",
        "difficulty": 3,
        "text": r"Знайдіть точки екстремуму функції $y = e^x - x$.",
        "svg_code": "",
        "options": [
            (r"А) $x = 1$", False),
            (r"Б) $x = 0$", True),
            (r"В) $x = e$", False),
            (r"Г) $x = -1$", False),
            (r"Д) Екстремумів немає", False)
        ],
        "topic_tags": ["26. Похідна", "19. Показникові вирази"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"Знайдіть похідну функції $y = (2x - 1)^5$.",
        "svg_code": "",
        "options": [
            (r"А) $5(2x - 1)^4$", False),
            (r"Б) $10(2x - 1)^4$", True),
            (r"В) $(2x - 1)^4$", False),
            (r"Г) $10x(2x - 1)^4$", False),
            (r"Д) $5x(2x - 1)^4$", False)
        ],
        "topic_tags": ["26. Похідна"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"Знайдіть похідну функції $y = \frac{x^2}{2} - \ln x$.",
        "svg_code": "",
        "options": [
            (r"А) $x - \frac{1}{x}$", True),
            (r"Б) $2x - \frac{1}{x}$", False),
            (r"В) $x + \frac{1}{x}$", False),
            (r"Г) $\frac{x^3}{3} - \frac{1}{x}$", False),
            (r"Д) $x - \ln x$", False)
        ],
        "topic_tags": ["26. Похідна", "20. Логарифмічні вирази"]
    },
    {
        "type": "CHOICE",
        "difficulty": 3,
        "text": r"При яких значеннях $x$ дотична до графіка функції $y = x^3 - 3x^2$ паралельна осі абсцис?",
        "svg_code": "",
        "options": [
            (r"А) $0; 2$", True),
            (r"Б) $0; 3$", False),
            (r"В) $1; -1$", False),
            (r"Г) Тільки $0$", False),
            (r"Д) Тільки $2$", False)
        ],
        "topic_tags": ["26. Похідна", "7. Квадратні рівняння", "11. Функції та їх властивості"]
    },

    # ==========================================
    # ЗАВДАННЯ НА ВІДПОВІДНІСТЬ (MATCH) - 4 шт.
    # ==========================================
    {
        "type": "MATCH",
        "difficulty": 1,
        "text": r"Узгодьте функцію (1–3) із її похідною (А–Д).",
        "svg_code": "",
        "options": [
            r"А) $y' = 3x^2$",
            r"Б) $y' = \frac{1}{2\sqrt{x}}$",
            r"В) $y' = -\sin x$",
            r"Г) $y' = \cos x$",
            r"Д) $y' = -\frac{1}{x^2}$"
        ],
        "matches": [
            (r"1. $y = x^3$", r"А) $y' = 3x^2$"),
            (r"2. $y = \cos x$", r"В) $y' = -\sin x$"),
            (r"3. $y = \frac{1}{x}$", r"Д) $y' = -\frac{1}{x^2}$")
        ],
        "topic_tags": ["26. Похідна"]
    },
    {
        "type": "MATCH",
        "difficulty": 2,
        "text": r"Узгодьте фізичний зміст (1–3) із відповідним математичним поняттям (А–Д).",
        "svg_code": "",
        "options": [
            r"А) Функція $f(t)$",
            r"Б) Перша похідна $f'(t)$",
            r"В) Друга похідна $f''(t)$",
            r"Г) Інтеграл $\int f(t) dt$",
            r"Д) Значення функції в точці $t=0$"
        ],
        "matches": [
            (r"1. Закон руху (шлях від часу)", r"А) Функція $f(t)$"),
            (r"2. Миттєва швидкість", r"Б) Перша похідна $f'(t)$"),
            (r"3. Прискорення", r"В) Друга похідна $f''(t)$")
        ],
        "topic_tags": ["26. Похідна"]
    },
    {
        "type": "MATCH",
        "difficulty": 2,
        "text": r"На рисунку зображено графік функції $y = f(x)$. Узгодьте точку (1–3) із властивістю похідної в ній (А–Д).",
        "svg_code": r"""
<svg viewBox="-4 -3 8 6" width="100%" height="200px" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <marker id="arrDarkM3" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4" markerHeight="4" orient="auto-start-reverse"><path d="M 0 1 L 10 5 L 0 9 z" fill="#7f8c8d" /></marker>
    </defs>
    <line x1="-4" y1="0" x2="4" y2="0" stroke="#7f8c8d" stroke-width="0.05" marker-end="url(#arrDarkM3)"/>
    <line x1="0" y1="3" x2="0" y2="-3" stroke="#7f8c8d" stroke-width="0.05" marker-end="url(#arrDarkM3)"/>

    <path d="M -3 2 Q -2 -2 -1 -1 T 1 1 T 3 -2" fill="none" stroke="#3498db" stroke-width="0.08"/>

    <circle cx="-2.3" cy="0.1" r="0.1" fill="#e74c3c"/>
    <text x="-2.3" y="0.6" font-size="0.3" font-family="sans-serif" text-anchor="middle">A</text>

    <circle cx="-0.1" cy="-1.1" r="0.1" fill="#e74c3c"/>
    <text x="-0.1" y="-0.5" font-size="0.3" font-family="sans-serif" text-anchor="middle">B</text>

    <circle cx="1.6" cy="-0.2" r="0.1" fill="#e74c3c"/>
    <text x="1.6" y="0.4" font-size="0.3" font-family="sans-serif" text-anchor="middle">C</text>
</svg>
        """,
        "options": [
            r"А) $f'(x) > 0$",
            r"Б) $f'(x) < 0$",
            r"В) $f'(x) = 0$",
            r"Г) $f'(x)$ не існує",
            r"Д) Похідна дорівнює функції"
        ],
        "matches": [
            (r"1. Точка A (функція спадає)", r"Б) $f'(x) < 0$"),
            (r"2. Точка B (локальний мінімум)", r"В) $f'(x) = 0$"),
            (r"3. Точка C (функція зростає)", r"А) $f'(x) > 0$")
        ],
        "topic_tags": ["26. Похідна", "11. Функції та їх властивості"]
    },
    {
        "type": "MATCH",
        "difficulty": 3,
        "text": r"Узгодьте функцію (1–3) з кількістю її критичних точок (А–Д).",
        "svg_code": "",
        "options": [
            r"А) Жодної",
            r"Б) Одна",
            r"В) Дві",
            r"Г) Три",
            r"Д) Безліч"
        ],
        "matches": [
            (r"1. $f(x) = 2x + 5$", r"А) Жодної"),
            (r"2. $f(x) = x^2 - 4x$", r"Б) Одна"),
            (r"3. $f(x) = x^3 - 3x$", r"В) Дві")
        ],
        "topic_tags": ["26. Похідна", "7. Квадратні рівняння"]
    },

    # ==========================================
    # КОРОТКА ВІДПОВІДЬ (SHORT) - 4 шт.
    # ==========================================
    {
        "type": "SHORT",
        "difficulty": 2,
        "text": r"Обчисліть $f'(2)$, якщо $f(x) = x^3 - 4x^2 + 5x - 1$.",
        "svg_code": "",
        "answer": "1",  # 3x^2 - 8x + 5 => 3(4) - 8(2) + 5 = 12 - 16 + 5 = 1
        "topic_tags": ["26. Похідна"]
    },
    {
        "type": "SHORT",
        "difficulty": 3,
        "text": r"Тіло рухається прямолінійно за законом $s(t) = t^3 - 3t^2 + 4t$. У який момент часу $t$ (у секундах) його прискорення дорівнюватиме $0$ м/с$^2$?",
        "svg_code": "",
        "answer": "1",  # v(t) = 3t^2 - 6t + 4. a(t) = 6t - 6. 6t - 6 = 0 => t = 1.
        "topic_tags": ["26. Похідна", "6. Лінійні рівняння. Лінійні рівняння з модулем"]
    },
    {
        "type": "SHORT",
        "difficulty": 3,
        "text": r"Знайдіть найбільше значення функції $f(x) = 2x^3 - 3x^2 - 12x$ на відрізку $[-2; 1]$.",
        "svg_code": "",
        "answer": "7",
        # f'(x) = 6x^2 - 6x - 12 = 6(x^2 - x - 2) = 6(x-2)(x+1). Крит. точки: 2, -1. На відрізку [-2; 1] лежить тільки -1. f(-1) = -2 - 3 + 12 = 7. Перевіримо кінці: f(-2) = -16 - 12 + 24 = -4. f(1) = 2 - 3 - 12 = -13. Найбільше 7.
        "topic_tags": ["26. Похідна", "7. Квадратні рівняння"]
    },
    {
        "type": "SHORT",
        "difficulty": 3,
        "text": r"Знайдіть кутовий коефіцієнт дотичної до графіка функції $f(x) = \frac{x^2 - 1}{x + 2}$ у точці з абсцисою $x_0 = -1$.",
        "svg_code": "",
        "answer": "-2",
        # f'(x) = ((2x)(x+2) - (x^2-1)(1)) / (x+2)^2 = (2x^2 + 4x - x^2 + 1) / (x+2)^2 = (x^2 + 4x + 1) / (x+2)^2. Підставляємо -1: (1 - 4 + 1) / 1^2 = -2 / 1 = -2.
        "topic_tags": ["26. Похідна", "8. Дробово-раціональні рівняння"]
    }
]