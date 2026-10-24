TOPIC_NAME = "4.2. Довжина кола. Довжина дуги кола"
COURSE = "Геометрія (7-9 класи)"
GRADE = "9 клас"

TASKS = [
    # ===== СХОДИНКА 1 =====
    # --- Моделювання ---
    {
        "type": "CHOICE", "difficulty": 1, "skill": "MODEL",
        "text": r"Яка формула довжини кола радіуса $R$?",
        "options": [(r"$C = 2\pi R$", True), (r"$C = \pi R^2$", False), (r"$C = \pi R$", False), (r"$C = 2R$", False)],
        "hint": "$C = \\pi d$, а $d = 2R$.",
        "solution": r"$C = \pi d = 2\pi R$. $\pi R^2$ — площа круга.",
    },
    {
        "type": "MATCH", "difficulty": 1, "skill": "MODEL",
        "text": r"Установіть відповідність між радіусом (1–3) та довжиною кола (А–Д).",
        "options": [r"А) $6\pi$", r"Б) $10\pi$", r"В) $3\pi$", r"Г) $25\pi$", r"Д) $\pi$"],
        "matches": [(r"1. $R = 3$", r"А) $6\pi$"), (r"2. $R = 5$", r"Б) $10\pi$"), (r"3. $R = 0{,}5$", r"Д) $\pi$")],
        "hint": "$C = 2\\pi R$.",
        "solution": r"$6\pi$, $10\pi$, $\pi$.",
    },
    {
        "type": "TF", "difficulty": 1, "skill": "MODEL",
        "text": r"Правда чи ні?",
        "statements": [(r"Відношення довжини кола до діаметра однакове для всіх кіл", True), (r"$\pi = 3{,}14$ точно", False), (r"Дуга $180^\circ$ — половина кола", True)],
        "hint": "$\\pi$ — ірраціональне.",
        "solution": r"$\pi = 3{,}14159\ldots$ — $3{,}14$ лише наближення.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "MODEL",
        "text": r"Яка формула довжини дуги в $\alpha^\circ$?",
        "options": [(r"$\dfrac{\pi R \alpha}{180}$", True), (r"$\dfrac{\pi R \alpha}{360}$", False), (r"$\dfrac{\pi R^2 \alpha}{360}$", False), (r"$\pi R \alpha$", False)],
        "hint": "Дуга $1^\\circ$ — $\\dfrac{2\\pi R}{360}$.",
        "solution": r"$\dfrac{2\pi R}{360} \cdot \alpha = \dfrac{\pi R\alpha}{180}$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "MODEL",
        "text": r"Діаметр круглої клумби $4$ м. Скільки метрів бордюру потрібно навколо неї? ($\pi \approx 3{,}14$)",
        "answer": "12,56",
        "hint": "$C = \\pi d$.",
        "solution": r"$3{,}14 \cdot 4 = 12{,}56$ м.",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"Довжина кола $C = 16\pi$. Знайдіть радіус.",
        "answer": "8",
        "hint": "$2\\pi R = 16\\pi$.",
        "solution": r"$R = 8$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"Знайдіть довжину кола з діаметром $9$. Відповідь — число, на яке множиться $\pi$.",
        "answer": "9",
        "hint": "$C = \\pi d$.",
        "solution": r"$C = 9\pi$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"Знайдіть довжину дуги $90^\circ$ кола радіуса $4$. Відповідь — число, на яке множиться $\pi$.",
        "answer": "2",
        "hint": "Чверть кола $8\\pi$.",
        "solution": r"$\dfrac{\pi \cdot 4 \cdot 90}{180} = 2\pi$.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "SOLVE",
        "text": r"Знайдіть довжину півкола радіуса $5$.",
        "options": [(r"$5\pi$", True), (r"$10\pi$", False), (r"$2{,}5\pi$", False), (r"$25\pi$", False)],
        "hint": "Половина від $2\\pi R$.",
        "solution": r"$\pi R = 5\pi$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"Довжина дуги $60^\circ$ дорівнює $2\pi$. Знайдіть радіус.",
        "answer": "6",
        "hint": "$\\dfrac{\\pi R \\cdot 60}{180} = \\dfrac{\\pi R}{3}$.",
        "solution": r"$\dfrac{\pi R}{3} = 2\pi$, $R = 6$.",
    },
    # --- Аналіз ---
    {
        "type": "ERROR", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Оля шукала довжину кола з діаметром $12$. У якому кроці помилка?",
        "steps": [r"$C = 2\pi R$", r"$C = 2\pi \cdot 12 = 24\pi$"],
        "wrong": 1,
        "hint": "Чому дорівнює радіус?",
        "solution": r"$R = 6$, $C = 12\pi$.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Радіус кола збільшили втричі. Як змінилася довжина кола?",
        "options": [(r"збільшилася втричі", True), (r"збільшилася в $9$ разів", False), (r"не змінилася", False), (r"збільшилася на $3$", False)],
        "hint": "$C = 2\\pi R$ — пропорційна $R$.",
        "solution": r"$2\pi \cdot 3R = 3 \cdot 2\pi R$.",
    },
    {
        "type": "TF", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Коло радіуса $6$. Правда чи ні?",
        "statements": [(r"Довжина кола $12\pi$", True), (r"Довжина дуги $60^\circ$ дорівнює $60$", False), (r"Дуга $120^\circ$ — третина кола", True)],
        "hint": "Довжина дуги — не те саме, що градусна міра.",
        "solution": r"Дуга $60^\circ$: $\dfrac{6\pi}{3} = 2\pi$.",
    },
    {
        "type": "GROUP", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Довжина кола яка?",
        "groups": [r"$10\pi$", r"$20\pi$"],
        "items": [(r"$R = 5$", 0), (r"$d = 10$", 0), (r"$R = 10$", 1), (r"$d = 20$", 1), (r"$R = 2{,}5 \cdot 2$", 0), (r"$d = 2 \cdot 10$", 1)],
        "hint": "$C = 2\\pi R = \\pi d$.",
        "solution": r"$R = 5$ або $d = 10$ — $10\pi$; $R = 10$ або $d = 20$ — $20\pi$.",
    },
    {
        "type": "MULTI", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Які дуги кола радіуса $9$ мають довжину $3\pi$?",
        "options": [(r"дуга $60^\circ$", True), (r"шоста частина кола", True), (r"дуга $30^\circ$", False), (r"дуга $90^\circ$", False)],
        "hint": "$\\dfrac{\\pi \\cdot 9 \\cdot \\alpha}{180} = 3\\pi$.",
        "solution": r"$\alpha = 60^\circ$ — шоста частина $360^\circ$.",
    },

    # ===== СХОДИНКА 2 =====
    # --- Моделювання ---
    {
        "type": "SHORT", "difficulty": 2, "skill": "MODEL",
        "text": r"Колесо радіусом $0{,}4$ м проїхало $50{,}24$ м. Скільки обертів воно зробило? ($\pi \approx 3{,}14$)",
        "answer": "20",
        "solution": r"$C = 2 \cdot 3{,}14 \cdot 0{,}4 = 2{,}512$ м; $50{,}24 : 2{,}512 = 20$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "MODEL",
        "text": r"Хвилинна стрілка завдовжки $12$ см. Який шлях проходить її кінець за $20$ хвилин? Відповідь — число, на яке множиться $\pi$.",
        "answer": "8",
        "solution": r"$20$ хв — третина оберту ($120^\circ$): $\dfrac{\pi \cdot 12 \cdot 120}{180} = 8\pi$.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "MODEL",
        "text": r"Коло описане навколо квадрата зі стороною $4$. Знайдіть довжину кола.",
        "options": [(r"$4\sqrt2\,\pi$", True), (r"$8\pi$", False), (r"$4\pi$", False), (r"$2\sqrt2\,\pi$", False), (r"$16\pi$", False)],
        "solution": r"$d = 4\sqrt2$ (діагональ), $C = 4\sqrt2\,\pi$. В — вписане коло.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "MODEL",
        "text": r"Коло вписане в квадрат зі стороною $10$. Знайдіть довжину кола — число, на яке множиться $\pi$.",
        "answer": "10",
        "solution": r"$d = 10$, $C = 10\pi$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "MODEL",
        "text": r"Коло описане навколо правильного шестикутника зі стороною $5$. Знайдіть довжину кола — число, на яке множиться $\pi$.",
        "answer": "10",
        "solution": r"$R = a = 5$, $C = 10\pi$.",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Довжина дуги $4\pi$, радіус $12$. Знайдіть градусну міру дуги.",
        "answer": "60",
        "solution": r"$\dfrac{\pi \cdot 12\alpha}{180} = 4\pi$ ⟹ $\alpha = 60^\circ$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Довжина кола $24\pi$. Знайдіть довжину дуги $45^\circ$ — число, на яке множиться $\pi$.",
        "answer": "3",
        "solution": r"$45^\circ$ — восьма частина: $24\pi : 8 = 3\pi$.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "SOLVE",
        "text": r"Вписаний кут $30^\circ$ спирається на дугу кола радіуса $9$. Знайдіть довжину цієї дуги.",
        "options": [(r"$3\pi$", True), (r"$1{,}5\pi$", False), (r"$6\pi$", False), (r"$30$", False), (r"$9\pi$", False)],
        "solution": r"Дуга $60^\circ$: $\dfrac{9\pi \cdot 60}{180} = 3\pi$. Б — узяли дугу $30^\circ$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Коло вписане в правильний трикутник зі стороною $6\sqrt3$. Знайдіть довжину кола — число, на яке множиться $\pi$.",
        "answer": "6",
        "solution": r"$r = \dfrac{a}{2\sqrt3} = 3$, $C = 6\pi$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Знайдіть радіус кола, якщо дуга $150^\circ$ має довжину $5\pi$.",
        "answer": "6",
        "solution": r"$\dfrac{150\pi R}{180} = 5\pi$, $R = 6$.",
    },
    # --- Аналіз ---
    {
        "type": "ERROR", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Тарас шукав довжину дуги $40^\circ$ при $R = 9$. У якому кроці помилка?",
        "steps": [r"$l = \dfrac{\pi R \alpha}{360}$", r"$= \dfrac{\pi \cdot 9 \cdot 40}{360} = \pi$"],
        "wrong": 0,
        "solution": r"У знаменнику $180$: $l = 2\pi$.",
    },
    {
        "type": "TF", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [(r"Дуги з однаковою градусною мірою в різних колах мають різні довжини", True), (r"Довжина дуги пропорційна і радіусу, і градусній мірі", True), (r"Довжина дуги $360^\circ$ дорівнює $\pi R$", False)],
        "solution": r"$l = \dfrac{\pi R\alpha}{180}$; при $\alpha = 360^\circ$: $2\pi R$.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Довжину кола збільшили на $2\pi$. На скільки збільшився радіус?",
        "options": [(r"на $1$", True), (r"на $2$", False), (r"на $\pi$", False), (r"на $2\pi$", False), (r"залежить від радіуса", False)],
        "solution": r"$2\pi(R + x) = 2\pi R + 2\pi$ ⟹ $x = 1$ — незалежно від $R$!",
    },
    {
        "type": "MULTI", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Колесо зробило $5$ обертів і проїхало $10\pi$ м. Що правильно?",
        "options": [(r"довжина кола колеса $2\pi$ м", True), (r"радіус $1$ м", True), (r"діаметр $2$ м", True), (r"радіус $2$ м", False)],
        "solution": r"$C = 2\pi$, $R = 1$ м.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "ANALYZE",
        "text": r"У скільки разів довжина кола, описаного навколо квадрата, більша за довжину вписаного кола? Відповідь округліть до сотих.",
        "answer": "1,41",
        "solution": r"$R = \dfrac{a\sqrt2}{2}$, $r = \dfrac{a}{2}$: $\sqrt2 \approx 1{,}41$.",
    },

    # ===== СХОДИНКА 3 =====
    # --- Моделювання ---
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"Земля обертається навколо Сонця по орбіті радіусом близько $150$ млн км. Скільки мільйонів кілометрів вона проходить за рік? ($\pi \approx 3{,}14$)",
        "answer": "942",
        "solution": r"$2 \cdot 3{,}14 \cdot 150 = 942$ млн км.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"Шкив радіуса $10$ см обертається з частотою $3$ оберти за секунду. Яку відстань проходить точка обода за хвилину (у метрах, $\pi \approx 3{,}14$)?",
        "answer": "113,04",
        "solution": r"$C = 0{,}628$ м; $180$ обертів: $113{,}04$ м.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "MODEL",
        "text": r"Знайдіть периметр фігури, обмеженої півколом діаметра $AB = 8$ і самим діаметром.",
        "options": [(r"$4\pi + 8$", True), (r"$8\pi + 8$", False), (r"$4\pi$", False), (r"$8\pi$", False), (r"$16\pi + 8$", False)],
        "solution": r"Півколо $\pi \cdot 4 = 4\pi$, плюс $AB = 8$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"Мотузку обмотали навколо екватора м'яча довжиною $C$. Її подовжили на $6{,}28$ м і рівномірно підняли над поверхнею. На яку висоту (у м, $\pi \approx 3{,}14$)?",
        "answer": "1",
        "solution": r"$2\pi(R + h) - 2\pi R = 6{,}28$ ⟹ $h = 1$ м — незалежно від розміру!",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"Сектор кола радіуса $6$ з центральним кутом $120^\circ$. Знайдіть периметр сектора, якщо $\pi \approx 3$.",
        "answer": "24",
        "solution": r"Дуга $\dfrac{6\pi \cdot 120}{180} = 4\pi \approx 12$; периметр $12 + 6 + 6 = 24$.",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Хорда $AB$ кола радіуса $6$ дорівнює $6$. Знайдіть довжину меншої дуги $AB$ — число, на яке множиться $\pi$.",
        "answer": "2",
        "solution": r"$\triangle AOB$ рівносторонній, дуга $60^\circ$: $\dfrac{6\pi}{3} = 2\pi$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Хорда $AB = 6\sqrt3$ кола радіуса $6$. Знайдіть довжину меншої дуги $AB$ — число, на яке множиться $\pi$.",
        "answer": "4",
        "solution": r"За теоремою косинусів $\cos\angle AOB = \dfrac{36 + 36 - 108}{72} = -\dfrac12$, кут $120^\circ$: $\dfrac{6\pi \cdot 120}{180} = 4\pi$.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "SOLVE",
        "text": r"Довжини двох дуг, на які точки $A$ і $B$ ділять коло, відносяться як $2 : 7$, радіус $9$. Знайдіть довжину меншої дуги.",
        "options": [(r"$4\pi$", True), (r"$14\pi$", False), (r"$2\pi$", False), (r"$8\pi$", False), (r"$40$", False)],
        "solution": r"$C = 18\pi$; менша — $\dfrac29$: $4\pi$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Колесо зробило $25$ обертів на відстані $94{,}2$ м. Знайдіть діаметр колеса (у м, $\pi \approx 3{,}14$).",
        "answer": "1,2",
        "solution": r"$C = 94{,}2 : 25 = 3{,}768$; $d = 3{,}768 : 3{,}14 = 1{,}2$ м.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Сторона правильного трикутника, вписаного в коло, дорівнює $9$. Знайдіть довжину кола — число, на яке множиться $\pi$, піднесене до квадрата.",
        "answer": "108",
        "solution": r"$R = \dfrac{9}{\sqrt3} = 3\sqrt3$, $C = 6\sqrt3\,\pi$; $(6\sqrt3)^2 = 108$.",
    },
    # --- Аналіз ---
    {
        "type": "TF", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [(r"Периметр вписаного правильного многокутника менший за довжину кола", True), (r"Периметр описаного правильного многокутника більший за довжину кола", True), (r"Периметр вписаного шестикутника дорівнює $3d$", True), (r"$\pi \gt 3{,}2$", False)],
        "solution": r"Вписаний — усередині, описаний — ззовні. $6R = 3d$. $\pi \approx 3{,}14$.",
    },
    {
        "type": "ERROR", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Оля: «Кут між хордою і радіусом $30^\circ$, $R = 9$. Знайти меншу дугу». У якому кроці помилка?",
        "steps": [r"$\triangle AOB$ рівнобедрений, кути при основі по $30^\circ$", r"$\angle AOB = 120^\circ$", r"$l = \dfrac{\pi \cdot 9 \cdot 120}{360} = 3\pi$"],
        "wrong": 2,
        "solution": r"У знаменнику $180$: $l = 6\pi$.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Що довше: півколо радіуса $1$ чи діаметр кола радіуса $1{,}5$?",
        "options": [(r"півколо", True), (r"діаметр", False), (r"однакові", False), (r"не можна порівняти", False)],
        "solution": r"$\pi \approx 3{,}14 \gt 3$.",
    },
    {
        "type": "MULTI", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Два кола радіусів $2$ і $6$. Що правильно?",
        "options": [(r"довжини відносяться як $1 : 3$", True), (r"дуга $90^\circ$ меншого = дуга $30^\circ$ більшого", True), (r"довжини відносяться як $1 : 9$", False), (r"дуга $60^\circ$ більшого $= 2\pi$", True)],
        "solution": r"$4\pi : 12\pi$. $\pi = \pi$. $\dfrac{6\pi \cdot 60}{180} = 2\pi$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Довжина кола дорівнює периметру квадрата зі стороною $\pi$. Знайдіть радіус кола.",
        "answer": "2",
        "solution": r"$2\pi R = 4\pi$, $R = 2$.",
    },

    # ===== БОСИ =====
    {
        "type": "SHORT", "difficulty": 4, "skill": "MODEL",
        "text": r"Дві шестерні зчеплені: радіуси $3$ см і $5$ см. Більша зробила $12$ обертів. Скільки обертів зробила менша?",
        "answer": "20",
        "solution": r"Шлях точок обода однаковий: $12 \cdot 10\pi = n \cdot 6\pi$, $n = 20$.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "MODEL",
        "text": r"Фігура: квадрат зі стороною $4$, на кожній стороні назовні побудовано півколо. Знайдіть периметр фігури — число, на яке множиться $\pi$.",
        "answer": "8",
        "solution": r"Чотири півкола радіуса $2$: $4 \cdot 2\pi = 8\pi$.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "SOLVE",
        "text": r"Хорда кола віддалена від центру на $4$ і має довжину $8$. Знайдіть градусну міру меншої дуги.",
        "answer": "90",
        "solution": r"Половина хорди $4$ = відстань $4$ ⟹ рівнобедрений прямокутний трикутник, півкут $45^\circ$, центральний кут $90^\circ$.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "SOLVE",
        "text": r"Периметр сектора дорівнює $4R$ (де $R$ — радіус). Знайдіть градусну міру дуги сектора, якщо $\pi \approx 3$.",
        "answer": "120",
        "solution": r"$2R + l = 4R$ ⟹ $l = 2R = \dfrac{\pi R\alpha}{180}$ ⟹ $\alpha = \dfrac{360}{\pi} \approx 120^\circ$.",
    },
    {
        "type": "TF", "difficulty": 4, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [(r"Півколо діаметра $d$ дорівнює сумі двох півкіл діаметрів $\dfrac{d}{2}$", True), (r"Чим більше маленьких півкіл на діаметрі, тим довша ламана з них", False), (r"Довжина кола радіуса $R$ більша за $6R$", True)],
        "solution": r"$\dfrac{\pi d}{2} = 2 \cdot \dfrac{\pi d}{4}$ — сума завжди $\dfrac{\pi d}{2}$ при будь-якій кількості півкіл. $2\pi R \gt 6R$.",
    },
    {
        "type": "SHORT", "difficulty": 5, "skill": "SOLVE",
        "text": r"Три кола радіуса $1$ попарно дотикаються зовні. Знайдіть довжину межі «трикутника» між ними (утвореного трьома дугами) — число, на яке множиться $\pi$.",
        "answer": "1",
        "solution": r"Центри — рівносторонній трикутник зі стороною $2$; кожна дуга — $60^\circ$ кола радіуса $1$: $\dfrac{\pi}{3}$. Три дуги: $\pi$.",
    },
    {
        "type": "SHORT", "difficulty": 5, "skill": "MODEL",
        "text": r"Монету радіуса $1$ котять без проковзування навколо такої самої нерухомої монети. Скільки обертів навколо свого центру вона зробить за одне коло?",
        "answer": "2",
        "solution": r"Центр рухомої монети описує коло радіуса $2$: шлях $4\pi$; $4\pi : 2\pi = 2$ оберти.",
    },
]
