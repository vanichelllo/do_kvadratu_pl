TOPIC_NAME = "3.4. Третя ознака рівності трикутників"
COURSE = "Геометрія (7-9 класи)"
GRADE = "7 клас"

TASKS = [
    # ==========================================
    # СХОДИНКА 1 — БАЗОВИЙ
    # ==========================================
    # --- Моделювання ---
    {
        "type": "CHOICE", "difficulty": 1, "skill": "MODEL",
        "text": r"У трикутниках $ABC$ і $MNK$: $AB = MN$, $BC = NK$, $AC = MK$. За якою ознакою вони рівні?",
        "options": [("за третьою (за трьома сторонами)", True), ("за першою (дві сторони й кут між ними)", False),
                    ("за другою (сторона й два прилеглі кути)", False), ("вони не обов'язково рівні", False)],
        "hint": r"Що відомо: сторони чи кути?",
        "solution": r"Відомо три пари відповідно рівних сторін — це третя ознака.",
    },
    {
        "type": "MATCH", "difficulty": 1, "skill": "MODEL",
        "text": r"Установіть відповідність між даними (1–3) та ознакою, за якою трикутники $ABC$ і $A_1B_1C_1$ рівні (А–Г).",
        "options": ["А) перша ознака", "Б) друга ознака", "В) третя ознака", "Г) даних недостатньо"],
        "matches": [(r"1. $AB = A_1B_1$, $BC = B_1C_1$, $AC = A_1C_1$", "В) третя ознака"),
                    (r"2. $AB = A_1B_1$, $AC = A_1C_1$, $\angle A = \angle A_1$", "А) перша ознака"),
                    (r"3. $\angle A = \angle A_1$, $\angle B = \angle B_1$, $\angle C = \angle C_1$", "Г) даних недостатньо")],
        "hint": r"Перша ознака — СКС, друга — КСК, третя — ССС.",
        "solution": r"1) Три сторони — третя ознака. 2) Дві сторони й кут між ними — перша. 3) Рівність трьох кутів не є ознакою рівності трикутників.",
    },
    {
        "type": "TF", "difficulty": 1, "skill": "MODEL",
        "text": r"Правда чи ні?",
        "statements": [(r"Якщо три сторони одного трикутника відповідно дорівнюють трьом сторонам іншого, то трикутники рівні", True),
                       ("Якщо три кути одного трикутника відповідно дорівнюють трьом кутам іншого, то трикутники рівні", False),
                       ("У рівних трикутниках проти рівних сторін лежать рівні кути", True)],
        "hint": "Згадайте приклад з рівносторонніми трикутниками різного розміру.",
        "solution": r"Перше — третя ознака. Рівносторонні трикутники зі сторонами $1$ і $10$ мають рівні кути, але не рівні. У рівних трикутниках відповідні елементи рівні.",
    },
    {
        "type": "GROUP", "difficulty": 1, "skill": "MODEL",
        "text": r"Розподіліть дані: чи досить їх, щоб стверджувати $\triangle ABC = \triangle DEF$?",
        "groups": ["досить", "не досить"],
        "items": [(r"$AB = DE$, $BC = EF$, $AC = DF$", 0), (r"$AB = DE$, $BC = EF$, $\angle B = \angle E$", 0),
                  (r"$AB = DE$, $\angle A = \angle D$, $\angle B = \angle E$", 0), (r"$AB = DE$, $BC = EF$", 1),
                  (r"$\angle A = \angle D$, $\angle B = \angle E$, $\angle C = \angle F$", 1), (r"$AB = DE$, $BC = EF$, $\angle A = \angle D$", 1)],
        "hint": "Перевірте кожен набір на відповідність одній з трьох ознак.",
        "solution": r"Досить: ССС, СКС ($\angle B$ між $AB$ і $BC$), КСК (кути прилеглі до $AB$). Не досить: дві сторони без третього елемента; три кути; дві сторони й кут не між ними.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "MODEL",
        "text": r"$\triangle ABC = \triangle KLM$ за трьома сторонами, $AB = KL$, $BC = LM$, $AC = KM$. Який кут дорівнює $\angle A$?",
        "options": [(r"$\angle K$", True), (r"$\angle L$", False), (r"$\angle M$", False)],
        "hint": r"Кут $A$ лежить проти сторони $BC$. Проти якої сторони лежить шуканий кут?",
        "solution": r"$\angle A$ лежить проти $BC$, а $BC = LM$, проти якої лежить $\angle K$. Отже, $\angle A = \angle K$.",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"$\triangle ABC = \triangle DEF$ за трьома сторонами, $AB = DE$, $BC = EF$, $AC = DF$, $\angle E = 72^\circ$. Знайдіть $\angle B$ (у градусах).",
        "answer": "72",
        "hint": r"Відповідні вершини: $B \leftrightarrow E$.",
        "solution": r"Трикутники рівні, $B$ відповідає $E$: $\angle B = \angle E = 72^\circ$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"У трикутниках $ABC$ і $A_1B_1C_1$: $AB = A_1B_1 = 5$ см, $BC = B_1C_1 = 6$ см, $AC = A_1C_1$. Периметр $\triangle ABC$ дорівнює $18$ см. Знайдіть $A_1C_1$ (у см).",
        "answer": "7",
        "hint": "Знайдіть третю сторону трикутника $ABC$ з периметра.",
        "solution": r"$AC = 18 - 5 - 6 = 7$ см, і $A_1C_1 = AC = 7$ см.",
    },
    {
        "type": "FIELDS", "difficulty": 1, "skill": "SOLVE",
        "text": r"$\triangle MNP = \triangle RST$ за трьома сторонами ($M \leftrightarrow R$, $N \leftrightarrow S$, $P \leftrightarrow T$), $\angle M = 40^\circ$, $\angle N = 65^\circ$. Знайдіть:",
        "fields": [(r"$\angle R =$", "40"), (r"$\angle S =$", "65")],
        "hint": "Рівні кути — у відповідних вершинах.",
        "solution": r"$\angle R = \angle M = 40^\circ$, $\angle S = \angle N = 65^\circ$.",
    },
    {
        "type": "MULTI", "difficulty": 1, "skill": "SOLVE",
        "text": r"$AB = AD$, $CB = CD$ (чотирикутник $ABCD$). Які рівності правильні?",
        "options": [(r"$\triangle ABC = \triangle ADC$", True), (r"$\angle B = \angle D$", True), (r"$\angle BAC = \angle DAC$", True),
                    (r"$AB = BC$", False), (r"$\angle BAC = \angle BCA$", False)],
        "hint": r"Розгляньте трикутники $ABC$ і $ADC$ зі спільною стороною $AC$.",
        "solution": r"$\triangle ABC = \triangle ADC$ за трьома сторонами ($AC$ — спільна). Звідси $\angle B = \angle D$, $\angle BAC = \angle DAC$. Рівність $AB = BC$ і рівність кутів $BAC$ і $BCA$ з умови не випливають.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"Сторони трикутника $ABC$: $AB = 4$ см, $BC = 9$ см, $AC = 7$ см. Трикутник $KLM$ рівний йому, причому $KL = 9$ см, $LM = 7$ см. Знайдіть $KM$ (у см).",
        "answer": "4",
        "hint": "Рівні трикутники мають однакові набори сторін.",
        "solution": r"Сторони $KLM$ — це ті самі $4$, $9$ і $7$ см. Дві вже названі, тож $KM = 4$ см.",
    },
    # --- Аналіз результатів ---
    {
        "type": "ERROR", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Оля доводить, що $\triangle ABC = \triangle ADC$, якщо $AB = AD$, $BC = DC$. У якому кроці помилка?",
        "steps": [r"$AB = AD$ (за умовою)", r"$BC = DC$ (за умовою)", r"$\angle B = \angle D$ (за умовою)", r"$\triangle ABC = \triangle ADC$ за першою ознакою"],
        "wrong": 2,
        "hint": "Перечитайте, що дано в умові.",
        "solution": r"Рівності кутів $B$ і $D$ в умові немає. Правильно: третьою парою є спільна сторона $AC$, і трикутники рівні за третьою ознакою.",
    },
    {
        "type": "TF", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Учень довів: $\triangle ABC = \triangle MNK$ за трьома сторонами, $AB = MN$, $BC = NK$, $AC = MK$. Правда чи ні?",
        "statements": [(r"$\angle C = \angle K$", True), (r"$\angle A = \angle N$", False), (r"$\angle B = \angle N$", True)],
        "hint": "Порядок літер у записі рівності задає відповідність вершин.",
        "solution": r"Відповідність $A \leftrightarrow M$, $B \leftrightarrow N$, $C \leftrightarrow K$. Тому $\angle C = \angle K$, $\angle B = \angle N$, а $\angle A = \angle M$.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Учень: «Усі кути двох трикутників відповідно рівні, тому трикутники рівні». Чи правий він?",
        "options": [("Ні: трикутники можуть мати однакові кути й різні розміри", True), ("Так, це третя ознака", False), ("Так, це друга ознака", False)],
        "hint": "Порівняйте маленький і великий рівносторонні трикутники.",
        "solution": r"Третя ознака — про три сторони, а не про три кути. Рівносторонні трикутники зі сторонами $2$ і $5$ мають рівні кути, але не рівні.",
    },
    {
        "type": "MULTI", "difficulty": 1, "skill": "ANALYZE",
        "text": r"$\triangle ABC = \triangle ABD$ за трьома сторонами ($C \leftrightarrow D$). Що з цього випливає?",
        "options": [(r"$AC = AD$", True), (r"$BC = BD$", True), (r"$\angle ACB = \angle ADB$", True), (r"$AC = BC$", False)],
        "hint": "У рівних трикутниках відповідні сторони й кути рівні.",
        "solution": r"Відповідні сторони: $AC = AD$, $BC = BD$; відповідні кути: $\angle C = \angle D$. Рівність $AC = BC$ не випливає.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Скільки пар рівних сторін потрібно знайти, щоб застосувати третю ознаку рівності трикутників?",
        "answer": "3",
        "hint": "Назва ознаки — «за трьома сторонами».",
        "solution": r"Три пари відповідно рівних сторін.",
    },

    # ==========================================
    # СХОДИНКА 2 — СЕРЕДНІЙ
    # ==========================================
    # --- Моделювання ---
    {
        "type": "ORDER", "difficulty": 2, "skill": "MODEL",
        "text": r"$AB = CD$, $BC = AD$ (точки $B$ і $D$ — по різні боки від $AC$). Упорядкуйте кроки доведення, що $\angle B = \angle D$.",
        "items": [r"Розглянемо $\triangle ABC$ і $\triangle CDA$", r"$AB = CD$ і $BC = DA$ за умовою", r"$AC$ — спільна сторона",
                  r"$\triangle ABC = \triangle CDA$ за трьома сторонами", r"Отже, $\angle B = \angle D$ як відповідні кути"],
        "hint": "Назвати трикутники → три пари сторін → ознака → висновок.",
        "solution": r"Стандартна схема доведення: трикутники, три пари рівних сторін (дві за умовою і спільна), ознака, висновок про відповідні кути.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "MODEL",
        "text": r"$AB = BC$, $AD = DC$, точки $B$ і $D$ по різні боки від $AC$. Яка пара трикутників рівна за третьою ознакою?",
        "options": [(r"$\triangle ABD$ і $\triangle CBD$", True), (r"$\triangle ABC$ і $\triangle ADC$", False), (r"$\triangle ABD$ і $\triangle ADC$", False), (r"$\triangle ABC$ і $\triangle ABD$", False)],
        "hint": r"Шукайте трикутники зі спільною стороною $BD$.",
        "solution": r"$AB = CB$, $AD = CD$, $BD$ — спільна: $\triangle ABD = \triangle CBD$. Трикутники $ABC$ і $ADC$ рівнобедрені, але, взагалі кажучи, різні.",
    },
    {
        "type": "TF", "difficulty": 2, "skill": "MODEL",
        "text": r"$ABCD$ — чотирикутник, у якого $AB = CD$ і $BC = AD$. Правда чи ні?",
        "statements": [(r"$\triangle ABC = \triangle CDA$", True), (r"$\angle BAC = \angle DCA$", True),
                       (r"$\angle BCA = \angle DAC$", True), (r"$\triangle ABC = \triangle ADC$ (саме з такою відповідністю вершин)", False)],
        "hint": r"Спільна сторона $AC$. Яка вершина відповідає $A$?",
        "solution": r"$\triangle ABC = \triangle CDA$: $A \leftrightarrow C$, $B \leftrightarrow D$, $C \leftrightarrow A$. Звідси $\angle BAC = \angle DCA$, $\angle BCA = \angle DAC$. Запис $\triangle ABC = \triangle ADC$ означав би $AB = AD$ — цього не дано.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "MODEL",
        "text": r"$AB = AD$, $CB = CD$, $\angle BAD = 80^\circ$. Знайдіть $\angle BAC$ (у градусах).",
        "answer": "40",
        "hint": r"Діагональ $AC$ ділить кут $BAD$ на рівні частини.",
        "solution": r"$\triangle ABC = \triangle ADC$ за трьома сторонами, тож $\angle BAC = \angle DAC = 80^\circ : 2 = 40^\circ$.",
    },
    {
        "type": "MATCH", "difficulty": 2, "skill": "MODEL",
        "text": r"$\triangle PQR = \triangle XYZ$ за трьома сторонами, $PQ = XY$, $QR = YZ$, $PR = XZ$. Установіть відповідність між кутами (1–3) та рівними їм кутами (А–Г).",
        "options": [r"А) $\angle X$", r"Б) $\angle Y$", r"В) $\angle Z$", "Г) жоден із кутів трикутника $XYZ$"],
        "matches": [(r"1. $\angle P$", r"А) $\angle X$"), (r"2. $\angle Q$", r"Б) $\angle Y$"), (r"3. $\angle R$", r"В) $\angle Z$")],
        "solution": r"Відповідність вершин: $P \leftrightarrow X$, $Q \leftrightarrow Y$, $R \leftrightarrow Z$.",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"$AB = BC$, $M$ — середина $AC$. Знайдіть кут $AMB$ (у градусах).",
        "answer": "90",
        "hint": r"Доведіть рівність трикутників $ABM$ і $CBM$; кути $AMB$ і $CMB$ — суміжні.",
        "solution": r"$\triangle ABM = \triangle CBM$ за трьома сторонами. $\angle AMB = \angle CMB$, а разом $180^\circ$. Отже, $\angle AMB = 90^\circ$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"$AB = AD$, $CB = CD$, $\angle ABC = 110^\circ$. Знайдіть $\angle ADC$ (у градусах).",
        "answer": "110",
        "hint": r"Трикутники $ABC$ і $ADC$ рівні.",
        "solution": r"$\triangle ABC = \triangle ADC$ за трьома сторонами ($AC$ — спільна), $\angle ADC = \angle ABC = 110^\circ$.",
    },
    {
        "type": "FIELDS", "difficulty": 2, "skill": "SOLVE",
        "text": r"Відрізки $AC$ і $BD$ перетинаються. $AB = CD$, $BC = DA$, $\angle ABC = 100^\circ$, $\angle BAC = 30^\circ$. Знайдіть (у градусах):",
        "fields": [(r"$\angle CDA =$", "100"), (r"$\angle DCA =$", "30")],
        "hint": r"$\triangle ABC = \triangle CDA$. Яка вершина відповідає $A$?",
        "solution": r"$\triangle ABC = \triangle CDA$ за трьома сторонами: $A \leftrightarrow C$, $B \leftrightarrow D$. $\angle CDA = \angle ABC = 100^\circ$, $\angle DCA = \angle BAC = 30^\circ$.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "SOLVE",
        "text": r"Точки $C$ і $D$ лежать по різні боки від прямої $AB$, $AC = AD$, $BC = BD$. Що можна стверджувати про пряму $AB$?",
        "options": [(r"$AB$ — бісектриса кутів $CAD$ і $CBD$", True), (r"$AB \parallel CD$", False), (r"$AB = CD$", False), ("нічого певного", False)],
        "hint": r"$\triangle ACB = \triangle ADB$ — що звідси випливає для кутів при $A$ і $B$?",
        "solution": r"$\triangle ACB = \triangle ADB$ за трьома сторонами ($AB$ — спільна). Тому $\angle CAB = \angle DAB$ і $\angle CBA = \angle DBA$: $AB$ ділить кути $CAD$ і $CBD$ навпіл.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Периметри рівних трикутників $ABC$ і $DEF$ дорівнюють $24$ см. $AB = DE = 8$ см, $BC = EF$, $AC = DF = 10$ см. Знайдіть $EF$ (у см).",
        "answer": "6",
        "hint": "Знайдіть $BC$ з периметра.",
        "solution": r"$BC = 24 - 8 - 10 = 6$ см, $EF = BC = 6$ см.",
    },
    # --- Аналіз результатів ---
    {
        "type": "ERROR", "difficulty": 2, "skill": "ANALYZE",
        "text": r"$AB = CD$, $BC = AD$. Денис доводить рівність кутів. У якому кроці помилка?",
        "steps": [r"$\triangle ABC$ і $\triangle CDA$: $AB = CD$, $BC = DA$", r"$AC$ — спільна", r"$\triangle ABC = \triangle CDA$ за третьою ознакою", r"Тому $\angle BAC = \angle DAC$"],
        "wrong": 3,
        "hint": r"Яка вершина $\triangle CDA$ відповідає вершині $A$?",
        "solution": r"$A \leftrightarrow C$, тому $\angle BAC = \angle DCA$, а не $\angle DAC$.",
    },
    {
        "type": "TF", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [(r"Два рівносторонні трикутники з однаковим периметром рівні", True),
                       (r"Два рівнобедрені трикутники з рівними бічними сторонами рівні", False),
                       (r"Два рівнобедрені трикутники з рівними основами й рівними бічними сторонами рівні", True)],
        "hint": "Скільки сторін відомо в кожному випадку?",
        "solution": r"Рівний периметр рівносторонніх — рівні всі сторони, третя ознака. Бічні сторони $5$ і $5$ при основах $2$ і $8$ дають різні трикутники. Основа й дві бічні — три сторони.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Відомо: $AB = A_1B_1$, $AC = A_1C_1$, а периметри трикутників $ABC$ і $A_1B_1C_1$ рівні. Чи рівні трикутники?",
        "options": [("Так, за третьою ознакою", True), ("Ні, бо не відомі кути", False), ("Так, за першою ознакою", False), ("Даних недостатньо", False)],
        "hint": r"Що можна сказати про $BC$ і $B_1C_1$?",
        "solution": r"$BC = P - AB - AC = P_1 - A_1B_1 - A_1C_1 = B_1C_1$. Три пари рівних сторін — третя ознака.",
    },
    {
        "type": "MULTI", "difficulty": 2, "skill": "ANALYZE",
        "text": r"У трикутнику $ABC$: $AB = BC$, $BM$ — медіана. Що з переліченого можна довести за допомогою третьої ознаки?",
        "options": [(r"$BM$ — бісектриса кута $B$", True), (r"$BM \perp AC$", True), (r"$\angle A = \angle C$", True), (r"$BM = AC$", False), (r"$AM = AB$", False)],
        "hint": r"$\triangle ABM = \triangle CBM$. Перелічіть рівні кути.",
        "solution": r"З $\triangle ABM = \triangle CBM$: $\angle ABM = \angle CBM$ (бісектриса), $\angle AMB = \angle CMB = 90^\circ$ (суміжні й рівні), $\angle A = \angle C$. Про довжини $BM$ і $AM$ висновків немає.",
    },
    {
        "type": "GROUP", "difficulty": 2, "skill": "ANALYZE",
        "text": r"$AB = AD$, $CB = CD$ (чотирикутник $ABCD$, діагоналі перетинаються в $O$). Розподіліть твердження.",
        "groups": ["випливає з умови", "не випливає"],
        "items": [(r"$\angle ABC = \angle ADC$", 0), (r"$\angle BCA = \angle DCA$", 0), (r"$\angle BAC = \angle DAC$", 0),
                  (r"$AB = BC$", 1), (r"$AC = BD$", 1), (r"$AO = OC$", 1)],
        "hint": r"$\triangle ABC = \triangle ADC$ — що звідси випливає?",
        "solution": r"З рівності $\triangle ABC = \triangle ADC$ отримуємо рівність відповідних кутів. Довжини $AB$ і $BC$, діагоналей, відрізків $AO$ і $OC$ можуть бути різними.",
    },

    # ==========================================
    # СХОДИНКА 3 — ПІДВИЩЕНИЙ
    # ==========================================
    # --- Моделювання ---
    {
        "type": "ORDER", "difficulty": 3, "skill": "MODEL",
        "text": r"$AB = DC$, $AC = DB$, відрізки $AC$ і $BD$ перетинаються в $O$. Упорядкуйте кроки доведення $\angle BAO = \angle CDO$.",
        "items": [r"Розглянемо $\triangle ABC$ і $\triangle DCB$", r"$AB = DC$, $AC = DB$ за умовою, $BC$ — спільна",
                  r"$\triangle ABC = \triangle DCB$ за третьою ознакою", r"Звідси $\angle BAC = \angle CDB$",
                  r"$\angle BAO = \angle BAC$ і $\angle CDO = \angle CDB$, отже $\angle BAO = \angle CDO$"],
        "solution": r"Трикутники зі спільною стороною $BC$ рівні за трьома сторонами ($A \leftrightarrow D$). Кут $BAO$ — це кут $BAC$, а $CDO$ — кут $CDB$.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "MODEL",
        "text": r"Як обґрунтувати, що побудований циркулем і лінійкою кут дорівнює даному (побудова «відкласти кут, рівний даному»)?",
        "options": [("Будуємо трикутники з рівними сторонами — вони рівні за третьою ознакою", True), ("За першою ознакою", False),
                    ("Кути рівні, бо однакові радіуси", False), ("Обґрунтування не потрібне", False)],
        "solution": r"При побудові відкладаємо дві рівні сторони (радіуси) і третю — відстань між засічками. Трикутники рівні за трьома сторонами, отже, рівні й кути.",
    },
    {
        "type": "TF", "difficulty": 3, "skill": "MODEL",
        "text": r"Відрізки $AB$ і $CD$ рівні й перетинаються в точці $O$; $AC = BD$, $AD = BC$. Правда чи ні?",
        "statements": [(r"$\triangle ACD = \triangle BDC$", True), (r"$\triangle ACB = \triangle BDA$", True),
                       (r"$\angle CAD = \angle DBC$", True), (r"$AC = AD$", False)],
        "solution": r"$\triangle ACD$ і $\triangle BDC$: $AC = BD$, $AD = BC$, $CD$ — спільна. $\triangle ACB$ і $\triangle BDA$: $AC = BD$, $CB = DA$, $AB$ — спільна. З першої рівності: $\angle CAD = \angle DBC$ ($A \leftrightarrow B$). $AC = AD$ не дано.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"Точки $C$ і $D$ лежать по різні боки від прямої $AB$, $AC = AD$, $BC = BD$, $\angle CAD = 70^\circ$, $\angle CBD = 50^\circ$. Знайдіть $\angle CAB + \angle CBA$ (у градусах).",
        "answer": "60",
        "solution": r"$\triangle ACB = \triangle ADB$ за трьома сторонами, тож $AB$ — бісектриса кутів $CAD$ і $CBD$: $\angle CAB = 35^\circ$, $\angle CBA = 25^\circ$, сума $60^\circ$.",
    },
    {
        "type": "MATCH", "difficulty": 3, "skill": "MODEL",
        "text": r"$ABCD$ — чотирикутник, $AB = BC = CD = DA$, діагоналі перетинаються в $O$. Установіть відповідність між трикутником (1–3) та рівним йому (А–Г).",
        "options": [r"А) $\triangle CDA$", r"Б) $\triangle ABO$", r"В) $\triangle CBD$", r"Г) $\triangle AOB$"],
        "matches": [(r"1. $\triangle ABC$", r"А) $\triangle CDA$"), (r"2. $\triangle ABD$", r"В) $\triangle CBD$"), (r"3. $\triangle COB$", r"Г) $\triangle AOB$")],
        "solution": r"$\triangle ABC = \triangle CDA$ і $\triangle ABD = \triangle CBD$ за трьома сторонами. З останньої рівності $BD$ — бісектриса кута $B$; тоді $\triangle COB = \triangle AOB$ за першою ознакою ($CB = AB$, $BO$ — спільна, кути при $B$ рівні). $\triangle ABO$ — лише частина $\triangle ABC$.",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"$AB = AD$, $CB = CD$, діагоналі $AC$ і $BD$ перетинаються в $O$, $BD = 12$ см. Знайдіть $BO$ (у см).",
        "answer": "6",
        "solution": r"$\triangle ABC = \triangle ADC$ (ССС), тому $\angle BAO = \angle DAO$. Тоді $\triangle ABO = \triangle ADO$ за першою ознакою ($AB = AD$, $AO$ — спільна, кути при $A$ рівні): $BO = DO = 6$ см.",
    },
    {
        "type": "FIELDS", "difficulty": 3, "skill": "SOLVE",
        "text": r"$AB = AD$, $CB = CD$, $\angle BAD = 60^\circ$, $\angle BCD = 100^\circ$, діагоналі перетинаються в $O$. Знайдіть (у градусах):",
        "fields": [(r"$\angle BCA =$", "50"), (r"$\angle AOB =$", "90")],
        "solution": r"$\triangle ABC = \triangle ADC$: $AC$ — бісектриса кутів $A$ і $C$, $\angle BCA = 50^\circ$. $\triangle ABO = \triangle ADO$ (СКС) $\Rightarrow$ $\angle AOB = \angle AOD$, суміжні — по $90^\circ$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Периметр чотирикутника $ABCD$ дорівнює $30$ см, $AB = AD$, $CB = CD$, $AB - BC = 3$ см. Знайдіть $AB$ (у см).",
        "answer": "9",
        "solution": r"$2AB + 2BC = 30$, $AB + BC = 15$, $AB - BC = 3$ $\Rightarrow$ $AB = 9$ см.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "SOLVE",
        "text": r"$AB = CD$, $BC = AD$, $\angle ABC = 120^\circ$, точки $B$ і $D$ по різні боки від $AC$. Знайдіть $\angle ADC$.",
        "options": [(r"$120^\circ$", True), (r"$60^\circ$", False), (r"$240^\circ$", False), ("не можна визначити", False)],
        "solution": r"$\triangle ABC = \triangle CDA$ за трьома сторонами ($B \leftrightarrow D$), тож $\angle ADC = \angle ABC = 120^\circ$.",
    },
    {
        "type": "MULTI", "difficulty": 3, "skill": "SOLVE",
        "text": r"Відрізки $AC$ і $BD$ перетинаються в точці $O$, $AB = CD$, $BC = DA$. Які твердження правильні?",
        "options": [(r"$\angle BAC = \angle DCA$", True), (r"$AB \parallel CD$", True), (r"$BC \parallel AD$", True), (r"$AC \perp BD$", False), (r"$AC = BD$", False)],
        "solution": r"$\triangle ABC = \triangle CDA$ (ССС): $\angle BAC = \angle DCA$ — внутрішні різносторонні при $AB$, $CD$ і січній $AC$, тому $AB \parallel CD$. Аналогічно $\angle BCA = \angle DAC$ дає $BC \parallel AD$. Перпендикулярність і рівність діагоналей не випливають.",
    },
    # --- Аналіз результатів ---
    {
        "type": "ERROR", "difficulty": 3, "skill": "ANALYZE",
        "text": r"$AB = AD$, $CB = CD$, $O$ — точка перетину $AC$ і $BD$. Марко доводить $BO = OD$. У якому кроці помилка?",
        "steps": [r"$\triangle ABC = \triangle ADC$ за третьою ознакою", r"Отже, $\angle BAO = \angle DAO$", r"$\triangle ABO = \triangle ADO$ за третьою ознакою", r"Тому $BO = DO$"],
        "wrong": 2,
        "solution": r"Для третьої ознаки треба знати $BO = DO$ — а це саме те, що доводимо. Правильно: $\triangle ABO = \triangle ADO$ за першою ознакою ($AB = AD$, $AO$ — спільна, $\angle BAO = \angle DAO$).",
    },
    {
        "type": "TF", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [(r"Якщо в трикутниках $ABC$ і $A_1B_1C_1$: $AB = A_1B_1$, $BC = B_1C_1$ і медіани $BM = B_1M_1$, то трикутники рівні", True),
                       (r"Два трикутники з рівними периметрами рівні", False),
                       (r"Якщо дві сторони й периметр одного трикутника дорівнюють двом сторонам і периметру іншого, то трикутники рівні", True)],
        "solution": r"Про медіани: продовжимо медіану на її довжину — отримаємо трикутники зі сторонами $AB$, $BC$, $2BM$; вони рівні за ССС, звідки рівні кути при $B$, і далі — перша ознака. Рівні периметри: $3, 4, 5$ і $4, 4, 4$. Дві сторони й периметр визначають третю сторону.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Учень стверджує: «Якщо $AB = A_1B_1$, $BC = B_1C_1$ і $\angle A = \angle A_1$, то трикутники рівні». Чи правий він?",
        "options": [("Ні: кут $A$ не лежить між сторонами $AB$ і $BC$", True), ("Так, за першою ознакою", False), ("Так, за третьою ознакою", False), ("Так, за другою ознакою", False)],
        "solution": r"Між $AB$ і $BC$ лежить кут $B$. Дві сторони й кут не між ними — не ознака: існують нерівні трикутники з такими даними.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Скільки різних (нерівних) трикутників можна скласти з паличок довжиною $2$, $3$, $4$ і $6$ см, використовуючи щоразу три палички?",
        "answer": "2",
        "solution": r"Трійки: $(2,3,4)$ — так; $(2,3,6)$ — ні ($2 + 3 \lt 6$); $(2,4,6)$ — ні ($2 + 4 = 6$); $(3,4,6)$ — так. За третьою ознакою трикутники з однаковими сторонами рівні, тож різних — $2$.",
    },

    {
        "type": "GROUP", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Розподіліть умови: за якою ознакою з них випливає $\triangle ABC = \triangle A_1B_1C_1$?",
        "groups": ["лише через третю ознаку", "одразу за першою або другою", "не випливає"],
        "items": [(r"$AB = A_1B_1$, $AC = A_1C_1$, $P_{ABC} = P_{A_1B_1C_1}$", 0), (r"Обидва рівносторонні, $AB = A_1B_1$", 0),
                  (r"$AB = A_1B_1$, $\angle A = \angle A_1$, $\angle B = \angle B_1$", 1), (r"$AC = A_1C_1$, $BC = B_1C_1$, $\angle C = \angle C_1$", 1),
                  (r"$AB = A_1B_1$, $BC = B_1C_1$, $\angle A = \angle A_1$", 2), (r"Обидва рівнобедрені з основами $AC = A_1C_1$", 2)],
        "solution": r"Рівні периметри дають рівні треті сторони — ССС; у рівносторонніх рівні всі сторони — ССС. КСК і СКС — друга й перша ознаки. Кут не між сторонами і лише основа рівнобедреного — даних недостатньо.",
    },

    # ==========================================
    # БОСИ
    # ==========================================
    {
        "type": "SHORT", "difficulty": 4, "skill": "SOLVE",
        "text": r"$AB = AD$, $CB = CD$, $\angle BAD = 50^\circ$, $\angle ABD = 65^\circ$. Знайдіть кут між діагоналями $AC$ і $BD$ (у градусах).",
        "answer": "90",
        "solution": r"$AC$ — бісектриса кута $A$ (з $\triangle ABC = \triangle ADC$), а в рівнобедреному $\triangle ABD$ бісектриса до основи — висота. Кут $90^\circ$; дані про $50^\circ$ і $65^\circ$ зайві.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "MODEL",
        "text": r"У чотирикутнику $ABCD$: $AB = CD$, $BC = AD$, $\angle BAD = 110^\circ$. Знайдіть $\angle BCD$ (у градусах).",
        "answer": "110",
        "solution": r"Проведемо діагональ $BD$. $\triangle ABD = \triangle CDB$ за трьома сторонами: $AB = CD$, $AD = CB$, $BD$ — спільна. Відповідність $A \leftrightarrow C$, тому $\angle BCD = \angle DAB = 110^\circ$.",
    },
    {
        "type": "CHOICE", "difficulty": 4, "skill": "ANALYZE",
        "text": r"У трикутниках $ABC$ і $A_1B_1C_1$: $AB = A_1B_1$, $AC = A_1C_1$, медіани $AM = A_1M_1$. Чи рівні трикутники?",
        "options": [("Так, завжди", True), ("Ні, не обов'язково", False), ("Лише якщо трикутники рівнобедрені", False)],
        "solution": r"Подвоїмо медіану: $AM = MD$. $\triangle ABM = \triangle DCM$ (СКС) дає $CD = AB$. $\triangle ACD$ визначено трьома сторонами $AC$, $CD = AB$, $AD = 2AM$ — так само для другого трикутника. Звідси $\angle CAM = \angle C_1A_1M_1$, і аналогічно $\angle BAM = \angle B_1A_1M_1$; тоді $\angle A = \angle A_1$ і трикутники рівні за першою ознакою.",
    },
    {
        "type": "TF", "difficulty": 4, "skill": "ANALYZE",
        "text": r"Точки $A$ і $B$ лежать по один бік від прямої $CD$, $AC = BD$, $AD = BC$, відрізки $AD$ і $BC$ перетинаються в $O$. Правда чи ні?",
        "statements": [(r"$\triangle ACD = \triangle BDC$", True), (r"$\angle ACD = \angle BDC$", True),
                       (r"$\angle CAD = \angle DBC$", True), (r"$OC = OD$", True)],
        "solution": r"$\triangle ACD = \triangle BDC$ (ССС, $CD$ — спільна): $\angle ACD = \angle BDC$, $\angle ADC = \angle BCD$, $\angle CAD = \angle DBC$. У $\triangle OCD$ кути при $C$ і $D$ рівні ($\angle OCD = \angle BCD = \angle ADC = \angle ODC$), тож він рівнобедрений: $OC = OD$.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "SOLVE",
        "text": r"$AB = AD = 13$ см, $CB = CD$, діагоналі $AC$ і $BD$ перетинаються в точці $O$, $BO = 5$ см. Знайдіть периметр трикутника $ABD$ (у см).",
        "answer": "36",
        "solution": r"$\triangle ABC = \triangle ADC$ (ССС), тож $\angle BAO = \angle DAO$. $\triangle ABO = \triangle ADO$ за першою ознакою: $DO = BO = 5$ см, $BD = 10$ см. $P = 13 + 13 + 10 = 36$ см.",
    },

    # ==========================================
    # УЛЬТРА-БОСИ
    # ==========================================
    {
        "type": "SHORT", "difficulty": 5, "skill": "ANALYZE",
        "text": r"Скільки існує попарно нерівних трикутників з цілими сторонами, периметр яких дорівнює $12$?",
        "answer": "3",
        "solution": r"Сторони $a \le b \le c$, $a + b \gt c$, $a + b + c = 12$, отже $c \lt 6$: $(2,5,5)$, $(3,4,5)$, $(4,4,4)$. За третьою ознакою трикутники з однаковими сторонами рівні — різних $3$.",
    },
    {
        "type": "SHORT", "difficulty": 5, "skill": "MODEL",
        "text": r"На площині дано відрізок $AB = 5$ см. Скільки існує точок $C$, для яких $AC = 4$ см і $BC = 3$ см?",
        "answer": "2",
        "solution": r"$C$ — точка перетину кола з центром $A$ радіуса $4$ і кола з центром $B$ радіуса $3$. $3 + 4 \gt 5$, кола перетинаються у двох точках, симетричних відносно $AB$. Обидва трикутники рівні за третьою ознакою.",
    },
]
