TOPIC_NAME = "НМТ 2026 (Основна сесія)"
TASKS = [
    # ==========================================
    # ТЕСТОВІ ЗАВДАННЯ (CHOICE) - 15 шт.
    # ==========================================
    {
        "type": "CHOICE",
        "difficulty": 1,
        "text": r"Розв'яжіть рівняння $\frac{x}{7} = 9$. <strong>(НМТ 2026)</strong>",
        "svg_code": "",
        "options": [
            (r"А) $2$", False),
            (r"Б) $\frac{7}{9}$", False),
            (r"В) $63$", True),
            (r"Г) $\frac{9}{7}$", False),
            (r"Д) $16$", False)
        ],
        "topic_tags": ["6. Лінійні рівняння. Лінійні рівняння з модулем"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"На рисунку схематично зображено залежності рівня шуму (дБ) від частоти звуку (Гц) у навколишньому середовищі та в навушниках із шумопоглинанням. За якої частоти звуку різниця між рівнем шуму в навколишньому середовищі та в навушниках є найбільшою? <strong>(НМТ 2026)</strong>",
        "svg_code": r"""
<svg viewBox="0 0 500 250" width="100%" height="250px" xmlns="http://www.w3.org/2000/svg">
    <!-- Grid -->
    <path d="M 50 200 L 450 200 M 50 150 L 450 150 M 50 100 L 450 100 M 50 50 L 450 50" stroke="#e0e0e0" stroke-width="1" fill="none"/>
    <path d="M 50 200 L 50 50 M 100 200 L 100 50 M 150 200 L 150 50 M 200 200 L 200 50 M 250 200 L 250 50 M 300 200 L 300 50 M 350 200 L 350 50 M 400 200 L 400 50 M 450 200 L 450 50" stroke="#e0e0e0" stroke-width="1" fill="none"/>

    <!-- Y Axis Labels -->
    <text x="40" y="205" font-family="sans-serif" font-size="12" text-anchor="end">0</text>
    <text x="40" y="155" font-family="sans-serif" font-size="12" text-anchor="end">20</text>
    <text x="40" y="105" font-family="sans-serif" font-size="12" text-anchor="end">40</text>
    <text x="40" y="55" font-family="sans-serif" font-size="12" text-anchor="end">60</text>
    <text x="40" y="25" font-family="sans-serif" font-size="12" text-anchor="end">80</text>

    <!-- X Axis Labels -->
    <text x="50" y="220" font-family="sans-serif" font-size="12" text-anchor="middle">20</text>
    <text x="100" y="220" font-family="sans-serif" font-size="12" text-anchor="middle">100</text>
    <text x="150" y="220" font-family="sans-serif" font-size="12" text-anchor="middle">200</text>
    <text x="200" y="220" font-family="sans-serif" font-size="12" text-anchor="middle">300</text>
    <text x="250" y="220" font-family="sans-serif" font-size="12" text-anchor="middle">500</text>
    <text x="300" y="220" font-family="sans-serif" font-size="12" text-anchor="middle">1000</text>
    <text x="350" y="220" font-family="sans-serif" font-size="12" text-anchor="middle">2000</text>
    <text x="400" y="220" font-family="sans-serif" font-size="12" text-anchor="middle">3000</text>
    <text x="450" y="220" font-family="sans-serif" font-size="12" text-anchor="middle">5000</text>

    <!-- Orange Line (Environment) -->
    <path d="M 50 60 L 100 40 L 150 20 L 200 65 L 250 68 L 300 70 L 350 50 L 400 52 L 450 65" stroke="#f39c12" stroke-width="2" fill="none"/>
    <circle cx="350" cy="50" r="3" fill="#f39c12"/>

    <!-- Green Line (Headphones) -->
    <path d="M 50 65 L 100 115 L 150 75 L 200 125 L 250 120 L 300 145 L 350 165 L 400 125 L 450 120" stroke="#aada58" stroke-width="2" fill="none"/>
    <circle cx="350" cy="165" r="3" fill="#aada58"/>

    <!-- Marker for visual clarity -->
    <line x1="350" y1="50" x2="350" y2="165" stroke="#e74c3c" stroke-dasharray="4" stroke-width="1.5"/>
</svg>
        """,
        "options": [
            (r"А) $200$", False),
            (r"Б) $300$", False),
            (r"В) $1000$", False),
            (r"Г) $2000$", True),
            (r"Д) $5000$", False)
        ],
        "topic_tags": ["11. Функції та їх властивості"]
    },
    {
        "type": "CHOICE",
        "difficulty": 1,
        "text": r"У трикутнику $ABC$ $\angle A = 30^\circ$, $\angle B = 35^\circ$. Визначте градусну міру кута $C$. <strong>(НМТ 2026)</strong>",
        "svg_code": "",
        "options": [
            (r"А) $65^\circ$", False),
            (r"Б) $295^\circ$", False),
            (r"В) $115^\circ$", True),
            (r"Г) $125^\circ$", False),
            (r"Д) $130^\circ$", False)
        ],
        "topic_tags": ["31. Трикутники"]
    },
    {
        "type": "CHOICE",
        "difficulty": 1,
        "text": r"Обчисліть: $\log_{0{,}5} 8 =$ <strong>(НМТ 2026)</strong>",
        "svg_code": "",
        "options": [
            (r"А) $-3$", True),
            (r"Б) $4$", False),
            (r"В) $-2$", False),
            (r"Г) $7{,}5$", False),
            (r"Д) $8{,}5$", False)
        ],
        "topic_tags": ["20. Логарифмічні вирази"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"На рисунку зображено чотирикутну піраміду $SABCD$. Точка $M$ належить стороні $AB$. Площини $ABS$ і $MCS$ перетинаються по прямій: <strong>(НМТ 2026)</strong>",
        "svg_code": r"""
<svg viewBox="0 0 200 150" width="100%" height="200px" xmlns="http://www.w3.org/2000/svg">
    <path d="M 100 10 L 40 120 M 100 10 L 100 140 M 100 10 L 180 120 M 100 10 L 140 70" stroke="#2c3e50" stroke-width="1.5" fill="none"/>
    <path d="M 40 120 L 100 140 L 180 120" stroke="#2c3e50" stroke-width="1.5" fill="none"/>
    <path d="M 40 120 L 140 70 L 180 120" stroke="#2c3e50" stroke-width="1" stroke-dasharray="4" fill="none"/>
    <circle cx="70" cy="130" r="3" fill="#e74c3c"/>
    <text x="95" y="8" font-family="sans-serif" font-size="12">S</text>
    <text x="25" y="125" font-family="sans-serif" font-size="12">B</text>
    <text x="100" y="155" font-family="sans-serif" font-size="12">A</text>
    <text x="185" y="125" font-family="sans-serif" font-size="12">D</text>
    <text x="145" y="75" font-family="sans-serif" font-size="12">C</text>
    <text x="50" y="145" font-family="sans-serif" font-size="12" fill="#e74c3c">M</text>
    <path d="M 100 10 L 70 130" stroke="#e74c3c" stroke-width="2" fill="none"/>
</svg>
        """,
        "options": [
            (r"А) $MC$", False),
            (r"Б) $AB$", False),
            (r"В) $SB$", False),
            (r"Г) $BC$", False),
            (r"Д) $SM$", True)
        ],
        "topic_tags": ["39. Вступ до стереометрії"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"У коробці лежать 30 тістечок двох видів: бісквіти та безе. Скільки всього бісквітних тістечок у цій коробці, якщо їх у 5 разів більше, ніж безе? <strong>(НМТ 2026)</strong>",
        "svg_code": "",
        "options": [
            (r"А) $5$", False),
            (r"Б) $6$", False),
            (r"В) $15$", False),
            (r"Г) $24$", False),
            (r"Д) $25$", True)
        ],
        "topic_tags": ["6. Лінійні рівняння. Лінійні рівняння з модулем"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"Спростіть вираз $\frac{(2x - 3)^2 - 9}{x}$. <strong>(НМТ 2026)</strong>",
        "svg_code": "",
        "options": [
            (r"А) $4x - 12$", True),
            (r"Б) $4x - 6$", False),
            (r"В) $4x$", False),
            (r"Г) $2x - 6$", False),
            (r"Д) $2x - 12$", False)
        ],
        "topic_tags": ["5. Розкладання на множники. Дробово-раціональні вирази"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"На рисунку зображено графік функції $y = f(x)$, визначеної на проміжку $[-3; 3]$. У яких чвертях розташований графік функції $y = f(x) + 3$? <strong>(НМТ 2026)</strong>",
        "svg_code": r"""
<svg viewBox="-50 -50 100 100" width="100%" height="200px" xmlns="http://www.w3.org/2000/svg">
    <!-- Grid -->
    <g stroke="#e0e0e0" stroke-width="0.5">
        <line x1="-40" y1="-40" x2="40" y2="-40"/><line x1="-40" y1="-30" x2="40" y2="-30"/><line x1="-40" y1="-20" x2="40" y2="-20"/><line x1="-40" y1="-10" x2="40" y2="-10"/>
        <line x1="-40" y1="10" x2="40" y2="10"/><line x1="-40" y1="20" x2="40" y2="20"/><line x1="-40" y1="30" x2="40" y2="30"/><line x1="-40" y1="40" x2="40" y2="40"/>
        <line x1="-40" y1="-40" x2="-40" y2="40"/><line x1="-30" y1="-40" x2="-30" y2="40"/><line x1="-20" y1="-40" x2="-20" y2="40"/><line x1="-10" y1="-40" x2="-10" y2="40"/>
        <line x1="10" y1="-40" x2="10" y2="40"/><line x1="20" y1="-40" x2="20" y2="40"/><line x1="30" y1="-40" x2="30" y2="40"/><line x1="40" y1="-40" x2="40" y2="40"/>
    </g>
    <!-- Axes -->
    <path d="M -50 0 L 50 0 M 0 -50 L 0 50" stroke="#2c3e50" stroke-width="1.5" fill="none"/>
    <!-- Parabola f(x) -->
    <path d="M -30 20 Q -20 10 -10 -20 Q 10 -40 30 10" stroke="#27ae60" stroke-width="2" fill="none"/>
    <text x="-35" y="10" font-family="sans-serif" font-size="8">-3</text>
    <text x="32" y="10" font-family="sans-serif" font-size="8">3</text>
    <text x="4" y="-22" font-family="sans-serif" font-size="8">y=f(x)</text>
</svg>
        """,
        "options": [
            (r"А) лише в II та III", False),
            (r"Б) лише в I та II", True),
            (r"В) лише в I, II та III", False),
            (r"Г) лише в I та IV", False),
            (r"Д) у всіх", False)
        ],
        "topic_tags": ["24. Побудова графіків функцій шляхом геометричних перетворень"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"Які з наведених тверджень є правильними?<br>I. Пряма, що проходить через центр кола і лежить із цим колом в одній площині, має з ним дві спільні точки.<br>II. Діаметр кола, перпендикулярний до його хорди, проходить через середину цієї хорди.<br>III. Можна провести два діаметри кола, що не мають жодної спільної точки. <strong>(НМТ 2026)</strong>",
        "svg_code": "",
        "options": [
            (r"А) лише I", False),
            (r"Б) лише II", False),
            (r"В) лише I та II", True),
            (r"Г) лише II та III", False),
            (r"Д) I, II та III", False)
        ],
        "topic_tags": ["38. Коло та круг"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"Послідовність $(a_n)$ задано формулою $n$-го члена $a_n = (-2)^n - 7$. Визначте четвертий член цієї послідовності. <strong>(НМТ 2026)</strong>",
        "svg_code": "",
        "options": [
            (r"А) $-15$", False),
            (r"Б) $9$", True),
            (r"В) $1$", False),
            (r"Г) $-6$", False),
            (r"Д) $-23$", False)
        ],
        "topic_tags": ["25. Числові послідовності"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"На діаграмі відображено інформацію про кількість шкільних гуртків. Макар планує відвідувати два гуртки: один спортивного напряму (їх 4) та один гурток будь-якого іншого напряму (їх загалом 10). Скільки всього існує варіантів такого вибору гуртків у Макара? <strong>(НМТ 2026)</strong>",
        "svg_code": r"""
<svg viewBox="0 0 100 100" width="100%" height="200px" xmlns="http://www.w3.org/2000/svg">
    <circle cx="50" cy="50" r="40" fill="none" stroke="#2c3e50" stroke-width="2"/>
    <path d="M 50 50 L 50 10 A 40 40 0 0 1 85 30 Z" fill="#e74c3c"/>
    <path d="M 50 50 L 85 30 A 40 40 0 0 1 90 55 Z" fill="#2ecc71"/>
    <path d="M 50 50 L 90 55 A 40 40 0 0 1 70 85 Z" fill="#9b59b6"/>
    <path d="M 50 50 L 70 85 A 40 40 0 0 1 20 75 Z" fill="#3498db"/>
    <path d="M 50 50 L 20 75 A 40 40 0 0 1 50 10 Z" fill="#f1c40f"/>
    <text x="65" y="35" font-family="sans-serif" font-size="8" fill="#fff" font-weight="bold">4</text>
    <text x="75" y="50" font-family="sans-serif" font-size="8" fill="#fff" font-weight="bold">1</text>
    <text x="65" y="70" font-family="sans-serif" font-size="8" fill="#fff" font-weight="bold">2</text>
    <text x="35" y="65" font-family="sans-serif" font-size="8" fill="#fff" font-weight="bold">4</text>
    <text x="40" y="35" font-family="sans-serif" font-size="8" fill="#fff" font-weight="bold">3</text>
</svg>
        """,
        "options": [
            (r"А) $60$", False),
            (r"Б) $16$", False),
            (r"В) $24$", False),
            (r"Г) $96$", False),
            (r"Д) $40$", True)
        ],
        "topic_tags": ["28. Комбінаторика"]
    },
    {
        "type": "CHOICE",
        "difficulty": 2,
        "text": r"Визначте довжину (модуль) вектора $\vec{a}(5; 2; -1)$. <strong>(НМТ 2026)</strong>",
        "svg_code": "",
        "options": [
            (r"А) $\sqrt{28}$", False),
            (r"Б) $6$", False),
            (r"В) $\sqrt{30}$", True),
            (r"Г) $\sqrt{32}$", False),
            (r"Д) $2\sqrt{7}$", False)
        ],
        "topic_tags": ["46. Вектори на площині та у просторі"]
    },
    {
        "type": "CHOICE",
        "difficulty": 3,
        "text": r"Знайдіть найбільший цілий розв'язок нерівності $(x - 4)(4 + x) < 8x - 7$. <strong>(НМТ 2026)</strong>",
        "svg_code": "",
        "options": [
            (r"А) $0$", False),
            (r"Б) $9$", False),
            (r"В) $-1$", False),
            (r"Г) $8$", True),
            (r"Д) $10$", False)
        ],
        "topic_tags": ["14. Квадратичні нерівності. Дробово-раціональні нерівності"]
    },
    {
        "type": "CHOICE",
        "difficulty": 3,
        "text": r"Для виготовлення картонної моделі трафарету $ABCDEFG$ Андрійко наклеїв квадрат зі стороною 6 см на прямокутник зі сторонами 4 см і 9 см. Спільною частиною є рівнобедрений трикутник, дві вершини якого збігаються з вершинами прямокутника. Обчисліть площу зображеного трафарету. <strong>(НМТ 2026)</strong>",
        "svg_code": r"""
<svg viewBox="-50 -50 250 100" width="100%" height="200px" xmlns="http://www.w3.org/2000/svg">
    <!-- Square (Rotated) -->
    <polygon points="0,0 40,-40 80,0 40,40" fill="#3498db" stroke="#2980b9" stroke-width="2"/>
    <!-- Rectangle -->
    <rect x="60" y="-20" width="90" height="40" fill="#f1c40f" stroke="#f39c12" stroke-width="2"/>
    <!-- Intersection Triangle -->
    <polygon points="60,-20 80,0 60,20" fill="#2ecc71" stroke="#27ae60" stroke-width="2"/>
    <text x="-15" y="5" font-family="sans-serif" font-size="12">A</text>
    <text x="35" y="-45" font-family="sans-serif" font-size="12">B</text>
    <text x="50" y="-25" font-family="sans-serif" font-size="12">C</text>
    <text x="155" y="-25" font-family="sans-serif" font-size="12">D</text>
</svg>
        """,
        "options": [
            (r"А) $64 \text{ см}^2$", False),
            (r"Б) $68 \text{ см}^2$", True),
            (r"В) $72 \text{ см}^2$", False),
            (r"Г) $40 \text{ см}^2$", False),
            (r"Д) $76 \text{ см}^2$", False)
        ],
        "topic_tags": ["37. Многокутники"]
    },
    {
        "type": "CHOICE",
        "difficulty": 3,
        "text": r"Розв'яжіть систему рівнянь $\begin{cases} 5^x = \sqrt{5} \\ \frac{y+1}{2x+3} = \frac{1-4x}{2} \end{cases}$. Якщо $(x_0; y_0)$ - розв'язок системи, то $x_0 + y_0 =$ <strong>(НМТ 2026)</strong>",
        "svg_code": "",
        "options": [
            (r"А) $-2{,}5$", True),
            (r"Б) $-3{,}5$", False),
            (r"В) $-7{,}5$", False),
            (r"Г) $1{,}5$", False),
            (r"Д) $-0{,}5$", False)
        ],
        "topic_tags": ["15. Системи рівнянь"]
    },

    # ==========================================
    # ЗАВДАННЯ НА ВІДПОВІДНІСТЬ (MATCH) - 3 шт.
    # ==========================================
    {
        "type": "MATCH",
        "difficulty": 2,
        "text": r"Доберіть до числового виразу (1-3) його значення (А-Д). <strong>(НМТ 2026)</strong>",
        "svg_code": "",
        "options": [
            r"А) $\frac{3}{2}$",
            r"Б) $3$",
            r"В) $\frac{1}{3}$",
            r"Г) $-\frac{1}{3}$",
            r"Д) $\frac{1}{2}$"
        ],
        "matches": [
            (r"1. $|\frac{5}{3} - 2|$", r"В) $\frac{1}{3}$"),
            (r"2. $3^{-2} \cdot (\frac{1}{3})^{-3}$", r"Б) $3$"),
            (r"3. $\sqrt{3} \cdot \sin\frac{\pi}{3}$", r"А) $\frac{3}{2}$")
        ],
        "topic_tags": ["1. Числові множини", "17. Тригонометричні вирази"]
    },
    {
        "type": "MATCH",
        "difficulty": 2,
        "text": r"Увідповідніть початок речення (1-3) із його закінченням (А-Д) так, щоб утворилося правильне твердження. <strong>(НМТ 2026)</strong>",
        "svg_code": "",
        "options": [
            r"А) $(-\infty; -2)$",
            r"Б) $[-2; 0)$",
            r"В) $[0; 1)$",
            r"Г) $(1; 2)$",
            r"Д) $[2; +\infty)$"
        ],
        "matches": [
            (r"1. Область визначення функції $y = \sqrt{x - 2}$ дорівнює", r"Д) $[2; +\infty)$"),
            (r"2. Точка екстремуму функції $y = x^2 + 2x + 3$ належить проміжку", r"Б) $[-2; 0)$"),
            (r"3. Абсциса точки перетину прямої $y = 6$ з графіком $y = x^3$ належить", r"Г) $(1; 2)$")
        ],
        "topic_tags": ["11. Функції та їх властивості", "26. Похідна"]
    },
    {
        "type": "MATCH",
        "difficulty": 3,
        "text": r"На рисунку зображено прямокутну трапецію $ABCD$, у якій $\angle CDA = 30^\circ$. Висота трапеції $CK$, довжина якої дорівнює 2 см, є бісектрисою кута $ACD$. Установіть відповідність між відрізком (1-3) та його довжиною (А-Д). <strong>(НМТ 2026)</strong>",
        "svg_code": r"""
<svg viewBox="-10 -10 220 100" width="100%" height="200px" xmlns="http://www.w3.org/2000/svg">
    <polygon points="0,0 80,0 160,80 0,80" fill="none" stroke="#2c3e50" stroke-width="2"/>
    <path d="M 80 0 L 80 80 M 0 80 L 80 0" stroke="#344e86" stroke-width="1.5" stroke-dasharray="4"/>
    <text x="-5" y="95" font-family="sans-serif" font-size="12">A</text>
    <text x="-5" y="-5" font-family="sans-serif" font-size="12">B</text>
    <text x="80" y="-5" font-family="sans-serif" font-size="12">C</text>
    <text x="165" y="95" font-family="sans-serif" font-size="12">D</text>
    <text x="75" y="95" font-family="sans-serif" font-size="12">K</text>
    <text x="130" y="75" font-family="sans-serif" font-size="10">30°</text>
</svg>
        """,
        "options": [
            r"А) $1$ см",
            r"Б) $\sqrt{3}$ см",
            r"В) $4$ см",
            r"Г) $2\sqrt{3}$ см",
            r"Д) $6\sqrt{3}$ см"
        ],
        "matches": [
            (r"1. $CD$", r"В) $4$ см"),
            (r"2. $BC$", r"Г) $2\sqrt{3}$ см"),
            (r"3. відстань від точки $B$ до прямої $AC$", r"Б) $\sqrt{3}$ см")
        ],
        "topic_tags": ["36. Чотирикутники", "35. Площа трикутника"]
    },

    # ==========================================
    # КОРОТКА ВІДПОВІДЬ (SHORT) - 4 шт.
    # ==========================================
    {
        "type": "SHORT",
        "difficulty": 3,
        "text": r"Обчисліть $\int_0^3 4(f(x) + 2) dx$, якщо $\int_0^3 f(x) dx = 10$. <strong>(НМТ 2026)</strong>",
        "svg_code": "",
        "answer": "64",
        "topic_tags": ["27. Первісна та інтеграл"]
    },
    {
        "type": "SHORT",
        "difficulty": 3,
        "text": r"У магазині в продажу є лише музичні диски, диски з науково-популярними фільмами та художніми фільмами. Кількість музичних дисків у три рази більша за кількість дисків із науковими фільмами і становить 40% від кількості дисків із художніми фільмами. Загальна кількість дорівнює 345. Визначте кількість музичних дисків. <strong>(НМТ 2026)</strong>",
        "svg_code": "",
        "answer": "90",
        "topic_tags": ["6. Лінійні рівняння. Лінійні рівняння з модулем", "2. Відношення, пропорції та відсотки"]
    },
    {
        "type": "SHORT",
        "difficulty": 3,
        "text": r"Задано циліндр із площею бічної поверхні $640\pi \text{ см}^2$ та конус. Радіус основи конуса вдвічі менший за радіус основи циліндра. Висота конуса дорівнює $15$ см, його твірна — $17$ см. Знайдіть об'єм $V$ циліндра. У відповідь запишіть $V/\pi$. <strong>(НМТ 2026)</strong>",
        "svg_code": "",
        "answer": "5120",
        "topic_tags": ["42. Циліндр", "43. Конус"]
    },
    {
        "type": "SHORT",
        "difficulty": 3,
        "text": r"Знайдіть значення $a$, за якого рівняння $\frac{\sqrt{x^2 - 10x} - \sqrt{36 - 5x}}{x - 2\log_2 a} = 0$ не має коренів. <strong>(НМТ 2026)</strong>",
        "svg_code": "",
        "answer": "0,25",
        "topic_tags": ["10. Ірраціональні рівняння", "22. Логарифмічні рівняння"]
    }
]