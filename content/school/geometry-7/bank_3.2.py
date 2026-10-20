TOPIC_NAME = "3.2. Перша і друга ознаки рівності трикутників"
COURSE = "Геометрія (7-9 класи)"
GRADE = "7 клас"

TASKS = [
    # ==========================================
    # СХОДИНКА 1 — БАЗОВИЙ
    # ==========================================
    # --- Моделювання ---
    {
        "type": "CHOICE", "difficulty": 1, "skill": "MODEL",
        "text": r"Про що йдеться в першій ознаці рівності трикутників?",
        "options": [(r"Про дві сторони і кут між ними", True), (r"Про три кути", False), (r"Про дві сторони і будь-який кут", False), (r"Про сторону і протилежний кут", False)],
        "hint": r"Кут має лежати між рівними сторонами.",
        "solution": r"Перша ознака: дві сторони і кут між ними.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "MODEL",
        "text": r"Про що йдеться в другій ознаці рівності трикутників?",
        "options": [(r"Про сторону і два прилеглі до неї кути", True), (r"Про два будь-які кути", False), (r"Про сторону і протилежний їй кут", False), (r"Про дві сторони", False)],
        "hint": r"Обидва кути прилягають до однієї сторони.",
        "solution": r"Друга ознака: сторона і два прилеглі до неї кути.",
    },
    {
        "type": "GROUP", "difficulty": 1, "skill": "MODEL",
        "text": r"Для $\triangle ABC$ і $\triangle A_1B_1C_1$ відомі рівності. Яка ознака підходить?",
        "groups": [r"Перша ознака", r"Друга ознака"],
        "items": [(r"$AB = A_1B_1$, $AC = A_1C_1$, $\angle A = \angle A_1$", 0), (r"$AB = A_1B_1$, $\angle A = \angle A_1$, $\angle B = \angle B_1$", 1),
                  (r"$BC = B_1C_1$, $\angle B = \angle B_1$, $\angle C = \angle C_1$", 1), (r"$BA = B_1A_1$, $BC = B_1C_1$, $\angle B = \angle B_1$", 0),
                  (r"$AC = A_1C_1$, $\angle A = \angle A_1$, $\angle C = \angle C_1$", 1)],
        "hint": r"Дві сторони + кут — перша; одна сторона + два кути при її кінцях — друга.",
        "solution": r"Кут $A$ між $AB$ і $AC$, кут $B$ між $BA$ і $BC$ — перша ознака. В інших — сторона й кути при її кінцях — друга.",
    },
    {
        "type": "MATCH", "difficulty": 1, "skill": "MODEL",
        "text": r"Установіть відповідність між рівністю (1–3) та її обґрунтуванням (А–Д).",
        "options": [r"А) вертикальні кути", r"Б) спільна сторона", r"В) означення бісектриси", r"Г) суміжні кути", r"Д) рівнобедрений трикутник"],
        "matches": [(r"1. $\angle AOC = \angle BOD$ (відрізки $AB$ і $CD$ перетинаються в $O$)", r"А) вертикальні кути"),
                    (r"2. $AC = AC$ у $\triangle ABC$ і $\triangle ADC$", r"Б) спільна сторона"),
                    (r"3. $\angle ABD = \angle CBD$, бо $BD$ ділить кут $B$ навпіл", r"В) означення бісектриси")],
        "hint": r"Кожна пара рівних елементів має причину.",
        "solution": r"Вертикальні кути рівні; спільна сторона рівна сама собі; бісектриса ділить кут на два рівні.",
    },
    {
        "type": "TF", "difficulty": 1, "skill": "MODEL",
        "text": r"Чи досить цих даних для рівності $\triangle ABC$ і $\triangle KLM$?",
        "statements": [
            (r"$AB = KL$, $BC = LM$, $\angle B = \angle L$", True),
            (r"$AB = KL$, $BC = LM$, $\angle A = \angle K$", False),
            (r"$AB = KL$, $\angle A = \angle K$, $\angle B = \angle L$", True),
        ],
        "hint": r"Чи лежить кут між рівними сторонами? Чи прилягають кути до рівної сторони?",
        "solution": r"Кут $B$ — між $AB$ і $BC$ (перша ознака). Кут $A$ не лежить між $AB$ і $BC$ — ознаки немає. Кути $A$, $B$ прилягають до $AB$ — друга ознака.",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"$\triangle ABC = \triangle KLM$, $AC = 7$ см. Знайдіть $KM$ (у см).",
        "answer": "7",
        "hint": r"$A \leftrightarrow K$, $C \leftrightarrow M$.",
        "solution": r"$KM$ відповідає $AC$: $7$ см.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"$\triangle AOC = \triangle BOD$, $\angle C = 40^\circ$. Знайдіть $\angle D$ (у градусах).",
        "answer": "40",
        "hint": r"Третя буква відповідає третій.",
        "solution": r"$\angle D$ відповідає $\angle C$: $40^\circ$.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"Відрізки $AB$ і $CD$ перетинаються в точці $O$, яка є серединою кожного з них. $AC = 6$ см. Знайдіть $BD$ (у см).",
        "answer": "6",
        "hint": r"$\triangle AOC = \triangle BOD$ за першою ознакою.",
        "solution": r"$AO = OB$, $CO = OD$, $\angle AOC = \angle BOD$ (вертикальні) — трикутники рівні, $BD = AC = 6$ см.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "SOLVE",
        "text": r"$AB = AD$, $\angle BAC = \angle DAC$, $BC = 5$ см. Знайдіть $DC$.",
        "options": [(r"$5$ см", True), (r"$10$ см", False), (r"$2{,}5$ см", False), (r"визначити не можна", False)],
        "hint": r"Порівняйте $\triangle ABC$ і $\triangle ADC$; $AC$ — спільна.",
        "solution": r"Перша ознака: $\triangle ABC = \triangle ADC$, тож $DC = BC = 5$ см.",
    },
    {
        "type": "SHORT", "difficulty": 1, "skill": "SOLVE",
        "text": r"$BD$ — бісектриса кута $ABC$ ($D$ на $AC$), $\angle ADB = \angle CDB$, $AB = 9$ см. Знайдіть $CB$ (у см).",
        "answer": "9",
        "hint": r"$\triangle ABD$ і $\triangle CBD$ — сторона $BD$ і два прилеглі кути.",
        "solution": r"За другою ознакою $\triangle ABD = \triangle CBD$, $CB = AB = 9$ см.",
    },
    # --- Аналіз ---
    {
        "type": "ERROR", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Петро доводить, що $\triangle ABC = \triangle ADC$. У якому кроці помилка?",
        "steps": [r"$AB = AD$ (за умовою)", r"$AC$ — спільна сторона", r"$\angle B = \angle D$ (за умовою)", r"Отже, $\triangle ABC = \triangle ADC$ за першою ознакою"],
        "wrong": 3,
        "hint": r"Між сторонами $AB$ і $AC$ лежить кут $A$, а не $B$.",
        "solution": r"Кути $B$ і $D$ не лежать між рівними сторонами — перша ознака не застосовна.",
    },
    {
        "type": "MULTI", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Яких даних досить, щоб $\triangle ABC = \triangle DEF$?",
        "options": [(r"$AB = DE$, $BC = EF$, $\angle B = \angle E$", True), (r"$AC = DF$, $\angle A = \angle D$, $\angle C = \angle F$", True),
                    (r"$\angle A = \angle D$, $\angle B = \angle E$, $\angle C = \angle F$", False), (r"$AB = DE$, $AC = DF$, $\angle B = \angle E$", False),
                    (r"$BC = EF$, $\angle B = \angle E$, $\angle C = \angle F$", True)],
        "hint": r"Шукайте «кут між сторонами» або «сторона і кути при її кінцях».",
        "solution": r"Перший — перша ознака, другий і п'ятий — друга. Рівні кути не гарантують рівних сторін; у четвертому кут $B$ не між $AB$ і $AC$.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Оля каже: «Якщо в трикутниках відповідні кути рівні, то трикутники рівні». Чи права вона?",
        "options": [(r"Ні: трикутники можуть мати однакові кути, але різні розміри", True), (r"Так, це ознака рівності", False),
                    (r"Так, якщо кути гострі", False), (r"Так, це друга ознака", False)],
        "hint": r"Уявіть трикутник і його збільшену копію.",
        "solution": r"Збільшена копія має ті самі кути, але довші сторони — трикутники не рівні.",
    },
    {
        "type": "TF", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Правда чи ні?",
        "statements": [
            (r"У рівних трикутників периметри рівні", True),
            (r"Трикутники з рівними периметрами рівні", False),
            (r"Рівні трикутники можна сумістити накладанням", True),
        ],
        "hint": r"Трикутники $3, 4, 5$ і $4, 4, 4$ мають однаковий периметр.",
        "solution": r"Відповідні сторони рівних трикутників рівні, тож і периметри. Обернене хибне: $3 + 4 + 5 = 4 + 4 + 4$.",
    },
    {
        "type": "CHOICE", "difficulty": 1, "skill": "ANALYZE",
        "text": r"Які кути трикутника $ABC$ прилеглі до сторони $AB$?",
        "options": [(r"$\angle A$ і $\angle B$", True), (r"$\angle A$ і $\angle C$", False), (r"$\angle B$ і $\angle C$", False), (r"лише $\angle C$", False)],
        "hint": r"Прилеглі кути — при кінцях сторони.",
        "solution": r"Кінці сторони $AB$ — вершини $A$ і $B$. Кут $C$ — протилежний до $AB$.",
    },
    # ==========================================
    # СХОДИНКА 2 — СЕРЕДНІЙ
    # ==========================================
    # --- Моделювання ---
    {
        "type": "ORDER", "difficulty": 2, "skill": "MODEL",
        "text": r"$AB = AD$, $\angle BAC = \angle DAC$. Розташуйте кроки доведення, що $BC = DC$.",
        "items": [
            r"Розглянемо $\triangle ABC$ і $\triangle ADC$",
            r"$AB = AD$ і $\angle BAC = \angle DAC$ — за умовою",
            r"$AC$ — спільна сторона",
            r"$\triangle ABC = \triangle ADC$ за першою ознакою",
            r"Отже, $BC = DC$",
        ],
        "hint": r"Трикутники → рівні елементи → ознака → висновок.",
        "solution": r"Це алгоритм доведення з уроку.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "MODEL",
        "text": r"Щоб виміряти відстань $AB$ через ставок, обрали точку $O$, продовжили $AO$ на $OC = AO$ і $BO$ на $OD = BO$. Виміряли $CD = 40$ м. Яка відстань $AB$?",
        "options": [(r"$40$ м", True), (r"$80$ м", False), (r"$20$ м", False), (r"визначити не можна", False)],
        "hint": r"$\triangle AOB$ і $\triangle COD$: дві сторони і вертикальні кути між ними.",
        "solution": r"За першою ознакою $\triangle AOB = \triangle COD$, тож $AB = CD = 40$ м.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "MODEL",
        "text": r"$\triangle ABC = \triangle DEF$, периметр $\triangle ABC$ — $24$ см, $DE = 7$ см, $EF = 8$ см. Знайдіть $DF$ (у см).",
        "answer": "9",
        "hint": r"Периметри рівних трикутників рівні.",
        "solution": r"$DF = 24 - 7 - 8 = 9$ см.",
    },
    {
        "type": "TF", "difficulty": 2, "skill": "MODEL",
        "text": r"Відрізки $AB$ і $CD$ перетинаються в точці $O$ — середині кожного з них. Правда чи ні?",
        "statements": [
            (r"$\triangle AOC = \triangle BOD$", True),
            (r"$AC = BD$", True),
            (r"$\angle CAO = \angle DBO$", True),
            (r"$AC = AD$", False),
        ],
        "hint": r"Рівні трикутники дають рівні відповідні елементи. А $AD$ — сторона іншого трикутника.",
        "solution": r"Перша ознака (вертикальні кути). $AC$ і $AD$ можуть бути різними.",
    },
    {
        "type": "FIELDS", "difficulty": 2, "skill": "MODEL",
        "text": r"Відрізки $AB$ і $CD$ перетинаються в точці $O$, $AO = OB$, $\angle CAO = \angle DBO$. $AC = 6$ см, $OC = 4$ см. Знайдіть $BD$ і $OD$ (у см).",
        "fields": [(r"$BD =$", "6"), (r"$OD =$", "4")],
        "hint": r"$\triangle AOC$ і $\triangle BOD$: сторона $AO = OB$ і прилеглі кути (один — вертикальний).",
        "solution": r"За другою ознакою $\triangle AOC = \triangle BOD$: $BD = AC = 6$, $OD = OC = 4$.",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Відрізки $AB$ і $CD$ перетинаються в точці $O$, $AO = OB$, $CO = OD$, $\angle OAC = 35^\circ$. Знайдіть $\angle OBD$ (у градусах).",
        "answer": "35",
        "hint": r"$\triangle AOC = \triangle BOD$; кут $A$ відповідає куту $B$.",
        "solution": r"$\angle OBD = \angle OAC = 35^\circ$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"$AB = AD$, $\angle BAC = \angle DAC$, $\angle ABC = 70^\circ$. Знайдіть $\angle ADC$ (у градусах).",
        "answer": "70",
        "hint": r"$\triangle ABC = \triangle ADC$; $B \leftrightarrow D$.",
        "solution": r"$\angle ADC = \angle ABC = 70^\circ$.",
    },
    {
        "type": "FIELDS", "difficulty": 2, "skill": "SOLVE",
        "text": r"$BD$ — бісектриса кута $ABC$ ($D$ на $AC$), $\angle ADB = \angle CDB$, $AB = 8$ см, $AD = 5$ см. Знайдіть $CB$ і $CD$ (у см).",
        "fields": [(r"$CB =$", "8"), (r"$CD =$", "5")],
        "hint": r"$\triangle ABD = \triangle CBD$ за другою ознакою.",
        "solution": r"$CB = AB = 8$, $CD = AD = 5$.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"$\triangle ABC = \triangle A_1B_1C_1$, $AB = 5$ см, $BC = 7$ см, $AC = 6$ см. Знайдіть периметр $\triangle A_1B_1C_1$ (у см).",
        "answer": "18",
        "hint": r"Відповідні сторони рівні.",
        "solution": r"$5 + 7 + 6 = 18$ см.",
    },
    {
        "type": "SHORT", "difficulty": 2, "skill": "SOLVE",
        "text": r"Відрізки $AB$ і $CD$ перетинаються в точці $O$, $AO = OB$, $\angle CAO = \angle DBO$, $AC = 11$ см. Знайдіть $BD$ (у см).",
        "answer": "11",
        "hint": r"Друга ознака: сторона $AO$ і кути при ній.",
        "solution": r"$\angle AOC = \angle BOD$ (вертикальні); $\triangle AOC = \triangle BOD$, $BD = AC = 11$ см.",
    },
    # --- Аналіз ---
    {
        "type": "ERROR", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Іра доводить рівність $\triangle ABC$ і $\triangle A_1B_1C_1$. У якому кроці помилка?",
        "steps": [r"$AB = A_1B_1$", r"$\angle A = \angle A_1$", r"$\angle C = \angle C_1$", r"Трикутники рівні за другою ознакою"],
        "wrong": 3,
        "hint": r"Чи прилягає кут $C$ до сторони $AB$?",
        "solution": r"У другій ознаці обидва кути прилеглі до рівної сторони: потрібні $\angle A$ і $\angle B$.",
    },
    {
        "type": "MULTI", "difficulty": 2, "skill": "ANALYZE",
        "text": r"$\triangle ABC = \triangle MNK$. Які рівності випливають?",
        "options": [(r"$AB = MN$", True), (r"$\angle C = \angle K$", True), (r"$BC = NK$", True), (r"$AC = MN$", False), (r"$\angle A = \angle N$", False)],
        "hint": r"$A \leftrightarrow M$, $B \leftrightarrow N$, $C \leftrightarrow K$.",
        "solution": r"Правильні: $AB = MN$, $BC = NK$, $AC = MK$, $\angle A = \angle M$, $\angle C = \angle K$.",
    },
    {
        "type": "CHOICE", "difficulty": 2, "skill": "ANALYZE",
        "text": r"$AB \parallel CD$, $AB = CD$, відрізки $AD$ і $BC$ перетинаються в точці $O$. За якою ознакою $\triangle AOB = \triangle DOC$?",
        "options": [(r"За другою", True), (r"За першою", False), (r"Вони не обов'язково рівні", False), (r"За третьою", False)],
        "hint": r"$\angle BAO = \angle CDO$ і $\angle ABO = \angle DCO$ — внутрішні різносторонні при паралельних.",
        "solution": r"Сторона $AB = DC$ і два прилеглі кути — друга ознака.",
    },
    {
        "type": "GROUP", "difficulty": 2, "skill": "ANALYZE",
        "text": r"Розподіліть: рівність обґрунтовано чи ні?",
        "groups": [r"Обґрунтовано", r"Не обґрунтовано"],
        "items": [(r"$\angle AOC = \angle BOD$, бо вони вертикальні", 0), (r"$AC = AC$ — спільна сторона", 0), (r"$\angle A = \angle C$, бо так видно на рисунку", 1),
                  (r"$AB = CD$, бо ці відрізки схожі", 1), (r"$\angle ABD = \angle CBD$, бо $BD$ — бісектриса", 0)],
        "hint": r"«Видно на рисунку» — не доведення.",
        "solution": r"Вертикальні кути, спільна сторона й означення бісектриси — обґрунтування. «Видно» і «схожі» — ні.",
    },
    {
        "type": "TF", "difficulty": 2, "skill": "ANALYZE",
        "text": r"У чотирикутнику $ABCD$: $AB = CD$, $BC = DA$, $\angle B = \angle D$. Правда чи ні?",
        "statements": [
            (r"$\triangle ABC = \triangle CDA$ за першою ознакою", True),
            (r"$\angle BAC = \angle DCA$", True),
            (r"$AB \parallel CD$", True),
            (r"$AC = BD$", False),
        ],
        "hint": r"Кут $B$ — між $AB$ і $BC$, кут $D$ — між $CD$ і $DA$.",
        "solution": r"$A \leftrightarrow C$, $B \leftrightarrow D$, $C \leftrightarrow A$: $\angle BAC = \angle DCA$ — внутрішні різносторонні при січній $AC$, тож $AB \parallel CD$. Про $BD$ нічого не відомо.",
    },
    # ==========================================
    # СХОДИНКА 3 — ПІДВИЩЕНИЙ
    # ==========================================
    # --- Моделювання ---
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"Точка $A$ — на іншому березі річки. На своєму березі відміряли $BC = 50$ м і по інший бік від $BC$ побудували кути $\angle CBD = \angle CBA$ і $\angle BCD = \angle BCA$. Виміряли $BD = 80$ м. Знайдіть $AB$ (у м).",
        "answer": "80",
        "hint": r"$\triangle ABC$ і $\triangle DBC$: спільна сторона $BC$ і прилеглі кути.",
        "solution": r"За другою ознакою $\triangle ABC = \triangle DBC$, тож $AB = DB = 80$ м.",
    },
    {
        "type": "FIELDS", "difficulty": 3, "skill": "MODEL",
        "text": r"$\triangle ABC = \triangle DEF$, $AB = 2x + 1$, $DE = 9$, $BC = y - 3$, $EF = 4$. Знайдіть $x$ і $y$.",
        "fields": [(r"$x =$", "4"), (r"$y =$", "7")],
        "hint": r"$AB = DE$, $BC = EF$.",
        "solution": r"$2x + 1 = 9$, $x = 4$; $y - 3 = 4$, $y = 7$.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "MODEL",
        "text": r"На одній стороні кута $A$ відклали $AB$ і $AD$, на другій — $AC = AB$ і $AE = AD$. Чому $BE = CD$?",
        "options": [(r"$\triangle ABE = \triangle ACD$ за першою ознакою", True), (r"$\triangle ABE = \triangle ACD$ за другою ознакою", False),
                    (r"$BE$ і $CD$ — вертикальні", False), (r"Бо $BD = CE$", False)],
        "hint": r"$AB = AC$, $AE = AD$, кут $A$ — спільний.",
        "solution": r"Дві сторони й спільний кут між ними — перша ознака; $BE$ і $CD$ — відповідні сторони.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "MODEL",
        "text": r"На одній стороні кута $A$ відклали $AB$ і $AD$, на другій — $AC = AB$ і $AE = AD$. $\angle ABE = 30^\circ$. Знайдіть $\angle ACD$ (у градусах).",
        "answer": "30",
        "hint": r"$\triangle ABE = \triangle ACD$; $B \leftrightarrow C$.",
        "solution": r"$\angle ACD = \angle ABE = 30^\circ$.",
    },
    {
        "type": "TF", "difficulty": 3, "skill": "MODEL",
        "text": r"Правда чи ні?",
        "statements": [
            (r"Дві сторони й кут між ними визначають трикутник однозначно", True),
            (r"Сторона і два кути, один з яких до неї не прилеглий, — це друга ознака", False),
            (r"Двох рівних сторін недостатньо для рівності трикутників", True),
        ],
        "hint": r"Друга ознака — саме прилеглі кути.",
        "solution": r"Перша ознака гарантує єдиність. Для двох сторін без кута можна побудувати різні трикутники.",
    },
    # --- Розв'язування ---
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Відрізки $AB$ і $CD$ перетинаються в точці $O$ — середині кожного; $AB = 10$ см, $CD = 12$ см, периметр $\triangle AOC$ — $20$ см. Знайдіть $BD$ (у см).",
        "answer": "9",
        "hint": r"$AO = 5$, $OC = 6$; знайдіть $AC$.",
        "solution": r"$AC = 20 - 5 - 6 = 9$; $\triangle AOC = \triangle BOD$, $BD = 9$ см.",
    },
    {
        "type": "FIELDS", "difficulty": 3, "skill": "SOLVE",
        "text": r"$AB = AD$, $\angle BAC = \angle DAC$; $\angle B = 80^\circ$, $\angle BCA = 35^\circ$. Знайдіть $\angle D$ і $\angle DCA$ (у градусах).",
        "fields": [(r"$\angle D =$", "80"), (r"$\angle DCA =$", "35")],
        "hint": r"$\triangle ABC = \triangle ADC$: $B \leftrightarrow D$, $C \leftrightarrow C$.",
        "solution": r"$\angle D = \angle B = 80^\circ$, $\angle DCA = \angle BCA = 35^\circ$.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"$AB \parallel CD$, $AB = CD$, відрізки $AD$ і $BC$ перетинаються в точці $O$, $AO = 4$ см. Знайдіть $OD$ (у см).",
        "answer": "4",
        "hint": r"$\triangle AOB = \triangle DOC$ за другою ознакою.",
        "solution": r"$OD$ відповідає $OA$: $4$ см.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "SOLVE",
        "text": r"Відрізки $AB$ і $CD$ перетинаються в точці $O$, $AO = OB$, $CO = OD$, $\angle CAO = 60^\circ$. Знайдіть $\angle DBO$ (у градусах).",
        "answer": "60",
        "hint": r"$\triangle AOC = \triangle BOD$; $A \leftrightarrow B$.",
        "solution": r"$\angle DBO = \angle CAO = 60^\circ$.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "SOLVE",
        "text": r"$BD$ — бісектриса кута $B$ трикутника $ABC$, $BA = BC$, $D$ на $AC$. Що можна стверджувати?",
        "options": [(r"$AD = CD$", True), (r"$AB = AC$", False), (r"$BD = AC$", False), (r"$\angle A = \angle ABC$", False)],
        "hint": r"$\triangle ABD$ і $\triangle CBD$: $BA = BC$, $BD$ спільна, кути між ними рівні.",
        "solution": r"За першою ознакою $\triangle ABD = \triangle CBD$, тож $AD = CD$.",
    },
    # --- Аналіз ---
    {
        "type": "ERROR", "difficulty": 3, "skill": "ANALYZE",
        "text": r"$AB \parallel CD$, $AB = CD$, $AD$ і $BC$ перетинаються в $O$. Максим доводить $\triangle AOB = \triangle DOC$. У якому кроці помилка?",
        "steps": [r"$AB = DC$ (за умовою)", r"$\angle BAO = \angle CDO$ — відповідні кути", r"$\angle ABO = \angle DCO$ — внутрішні різносторонні", r"$\triangle AOB = \triangle DOC$ за другою ознакою"],
        "wrong": 1,
        "hint": r"Як розташовані кути $BAO$ і $CDO$ відносно паралельних і січної $AD$?",
        "solution": r"$\angle BAO$ і $\angle CDO$ — внутрішні різносторонні (по різні боки від $AD$), а не відповідні. Висновок правильний, обґрунтування — ні.",
    },
    {
        "type": "MULTI", "difficulty": 3, "skill": "ANALYZE",
        "text": r"На одній стороні кута $A$ — точки $B$ і $D$ ($AB \lt AD$), на другій — $C$ і $E$, причому $AC = AB$, $AE = AD$. Що правильно?",
        "options": [(r"$BE = CD$", True), (r"$\angle ABE = \angle ACD$", True), (r"$\angle AEB = \angle ADC$", True), (r"$BD = CE$", True), (r"$BE = BC$", False)],
        "hint": r"$\triangle ABE = \triangle ACD$; $BD = AD - AB$, $CE = AE - AC$.",
        "solution": r"З рівності трикутників — рівність відповідних сторін і кутів. $BD = CE$ як різниці рівних відрізків. Про $BC$ нічого сказати не можна.",
    },
    {
        "type": "CHOICE", "difficulty": 3, "skill": "ANALYZE",
        "text": r"У $\triangle ABC$ і $\triangle KLM$: $AB = KL$, $\angle A = \angle K$, $AC = KM$. Якому куту дорівнює $\angle C$?",
        "options": [(r"$\angle M$", True), (r"$\angle L$", False), (r"$\angle K$", False), (r"визначити не можна", False)],
        "hint": r"Перша ознака; $C \leftrightarrow M$.",
        "solution": r"$\triangle ABC = \triangle KLM$, відповідні кути: $\angle C = \angle M$.",
    },
    {
        "type": "TF", "difficulty": 3, "skill": "ANALYZE",
        "text": r"У $\triangle ABC$: $AB = 5$, $AC = 7$, $\angle A = 40^\circ$. У $\triangle DEF$: $DE = 5$, $DF = 7$, $\angle E = 40^\circ$. Правда чи ні?",
        "statements": [
            (r"Трикутники обов'язково рівні", False),
            (r"Перша ознака тут не застосовна", True),
            (r"Якби $\angle D = 40^\circ$, трикутники були б рівні", True),
        ],
        "hint": r"Між сторонами $DE$ і $DF$ лежить кут $D$.",
        "solution": r"Кут $E$ не лежить між $DE$ і $DF$ — ознаки немає. З $\angle D = 40^\circ$ — перша ознака.",
    },
    {
        "type": "SHORT", "difficulty": 3, "skill": "ANALYZE",
        "text": r"Елементи $\triangle ABC$: $AB$, $BC$, $AC$, $\angle A$, $\angle B$, $\angle C$. Скільки існує трійок з них, рівність яких відповідним елементам іншого трикутника гарантує рівність трикутників за першою або другою ознакою?",
        "answer": "6",
        "hint": r"Перша: кожен кут зі сторонами, що його утворюють. Друга: кожна сторона з кутами при її кінцях.",
        "solution": r"Перша ознака: $3$ трійки (по одній на кожен кут). Друга: $3$ трійки (по одній на кожну сторону). Разом $6$.",
    },
    # ==========================================
    # БОСИ
    # ==========================================
    {
        "type": "SHORT", "difficulty": 4, "skill": "MODEL",
        "text": r"Щоб виміряти $AB$ через ставок, на продовженні $AC$ за точку $C$ відклали $CD = CA$, а на продовженні $BC$ — $CE = CB$. Виміряли $DE = 37$ м. Знайдіть $AB$ (у м).",
        "answer": "37",
        "solution": r"$\triangle ACB$ і $\triangle DCE$: $CA = CD$, $CB = CE$, $\angle ACB = \angle DCE$ (вертикальні). Перша ознака: $AB = DE = 37$ м.",
    },
    {
        "type": "FIELDS", "difficulty": 4, "skill": "MODEL",
        "text": r"$\triangle ABC = \triangle A_1B_1C_1$, $AB = 6$ см, $B_1C_1 = 7$ см, периметр $\triangle ABC$ — $21$ см. Знайдіть $BC$ і $A_1C_1$ (у см).",
        "fields": [(r"$BC =$", "7"), (r"$A_1C_1 =$", "8")],
        "solution": r"$BC = B_1C_1 = 7$; $AC = 21 - 6 - 7 = 8$, тож $A_1C_1 = 8$.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "SOLVE",
        "text": r"$AB \parallel CD$, $AB = CD$, відрізки $AD$ і $BC$ перетинаються в точці $O$; $AD = 14$ см, $BC = 10$ см. Знайдіть $BO$ (у см).",
        "answer": "5",
        "solution": r"$\triangle AOB = \triangle DOC$ (друга ознака), тож $BO = CO$ і $AO = DO$: $O$ — середина обох відрізків. $BO = 10 : 2 = 5$ см.",
    },
    {
        "type": "SHORT", "difficulty": 4, "skill": "SOLVE",
        "text": r"На одній стороні кута $A$ відклали $AB = 4$ см і $AD = 9$ см, на другій — $AC = AB$ і $AE = AD$; $BE = 11$ см. Знайдіть периметр $\triangle ACD$ (у см).",
        "answer": "24",
        "solution": r"$\triangle ABE = \triangle ACD$ (перша ознака): $CD = BE = 11$. $P = AC + AD + CD = 4 + 9 + 11 = 24$ см.",
    },
    {
        "type": "TF", "difficulty": 4, "skill": "ANALYZE",
        "text": r"$BD$ — бісектриса кута $B$ трикутника $ABC$, $BA = BC$, $D$ на $AC$. Правда чи ні?",
        "statements": [
            (r"$AD = DC$", True),
            (r"$\angle BDA = \angle BDC$", True),
            (r"$\angle A = \angle C$", True),
            (r"$BD = AD$", False),
        ],
        "solution": r"$\triangle ABD = \triangle CBD$ (перша ознака) — рівні всі відповідні елементи: $AD = DC$, $\angle BDA = \angle BDC$, $\angle A = \angle C$. $BD$ і $AD$ — сторони одного трикутника, рівність не випливає.",
    },
    # ==========================================
    # УЛЬТРА
    # ==========================================
    {
        "type": "SHORT", "difficulty": 5, "skill": "SOLVE",
        "text": r"Відрізки $AB$ і $CD$ перетинаються в точці $O$ — середині кожного. Периметр $\triangle AOC$ — $18$ см, периметр $\triangle AOD$ — $22$ см, $AC = 6$ см. Знайдіть $BC$ (у см).",
        "answer": "10",
        "solution": r"$OC = OD$, тож $AD - AC = 22 - 18 = 4$, $AD = 10$. $\triangle AOD = \triangle BOC$ (перша ознака, вертикальні кути), отже, $BC = AD = 10$ см.",
    },
    {
        "type": "SHORT", "difficulty": 5, "skill": "MODEL",
        "text": r"На одній стороні кута $A$ — точки $B$ і $D$ ($AB \lt AD$), на другій — $C$ і $E$, $AC = AB$, $AE = AD$; $BE$ і $CD$ перетинаються в точці $O$. Скільки пар рівних трикутників серед $\triangle ABE$, $\triangle ACD$, $\triangle BOD$, $\triangle COE$, $\triangle ABO$?",
        "answer": "2",
        "solution": r"$\triangle ABE = \triangle ACD$ (перша ознака). Звідси $\angle ABE = \angle ACD$, тож суміжні з ними $\angle DBO = \angle ECO$; $\angle ADC = \angle AEB$; $BD = CE$. За другою ознакою $\triangle BOD = \triangle COE$. $\triangle ABO$ пари серед названих не має.",
    },
]
