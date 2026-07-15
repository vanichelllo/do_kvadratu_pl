from django.core.management.base import BaseCommand
from materials.models import DiagnosticTopic, Question, AnswerOption, MatchItem


class Command(BaseCommand):
    help = 'Автоматичне наповнення бази даних діагностичним тестом НМТ (22 питання)'

    def handle(self, *args, **kwargs):
        self.stdout.write("Починаємо генерацію тесту (монолітна структура)...")

        # Очищаємо базу від старих питань
        Question.objects.all().delete()

        # 1. Створюємо теми
        topics_data = [
            "Числа, вирази та рівняння",
            "Функції та похідна",
            "Числові послідовності",
            "Планіметрія",
            "Стереометрія та вектори",
            "Елементи стохастики",
        ]

        topics = {}
        for topic_name in topics_data:
            topic, created = DiagnosticTopic.objects.get_or_create(name=topic_name)
            topics[topic_name] = topic

        # 2. Масив даних.
        # Формат: (Текст, Тема, Тип, Відповідь_для_відкритого, [ (Варіант, Чи_правильний), ... ], [ (Умова_зліва, Індекс_правильного_варіанту), ... ])
        questions_data = [
            # --- ЧАСТИНА 1: ОДИН З П'ЯТИ (1-15) ---
            (r"Розв’яжіть рівняння $\frac{3x}{4} = 6$.", topics["Числа, вирази та рівняння"], 'CHOICE', None,
             [("2", False), ("4.5", False), ("8", True), ("18", False), ("24", False)], None),

            (
            r"У коробці лежать 48 маркерів: сині та червоні. Синіх маркерів у 3 рази більше, ніж червоних. Скільки всього червоних маркерів у цій коробці?",
            topics["Числа, вирази та рівняння"], 'CHOICE', None,
            [("12", True), ("16", False), ("24", False), ("32", False), ("36", False)], None),

            (
            r"У трикутнику $ABC$ відомо, що $\angle A = 40^\circ$, $\angle C = 80^\circ$. Знайдіть градусну міру кута між висотою $BH$ та бісектрисою $BL$, проведеними з вершини $B$.",
            topics["Планіметрія"], 'CHOICE', None,
            [(r"$10^\circ$", False), (r"$20^\circ$", True), (r"$30^\circ$", False), (r"$40^\circ$", False),
             (r"$50^\circ$", False)], None),

            (r"Обчисліть значення виразу $\log_2 24 - \log_2 3$.", topics["Числа, вирази та рівняння"], 'CHOICE', None,
             [("3", True), ("4", False), ("8", False), (r"$\log_2 21$", False), ("21", False)], None),

            (r"Спростіть вираз $\frac{x^2 - 16}{x^2 - 4x}$.", topics["Числа, вирази та рівняння"], 'CHOICE', None,
             [(r"$\frac{x-4}{x}$", False), (r"$\frac{x+4}{x}$", True), (r"$\frac{4}{x}$", False), ("x+4", False),
              ("x-4", False)], None),

            (r"Знайдіть область визначення функції $y = \sqrt{6 - 2x}$.", topics["Функції та похідна"], 'CHOICE', None,
             [(r"$[3; +\infty)$", False), (r"$(-\infty; 3]$", True), (r"$[-3; +\infty)$", False),
              (r"$(-\infty; -3]$", False), (r"$(-\infty; +\infty)$", False)], None),

            (
            r"Графік функції $y = f(x)$ проходить через точку $M(2; -4)$. Через яку точку обов'язково проходить графік функції $y = f(x - 1) + 3$?",
            topics["Функції та похідна"], 'CHOICE', None,
            [("(1; -1)", False), ("(3; -1)", True), ("(1; -7)", False), ("(3; -7)", False), ("(2; -1)", False)], None),

            (
            r"Знайдіть найбільший цілий розв'язок системи нерівностей $\begin{cases} 3x - 5 \le 4 \\ -2x < 6 \end{cases}$.",
            topics["Числа, вирази та рівняння"], 'CHOICE', None,
            [("-3", False), ("-2", False), ("2", False), ("3", True), ("4", False)], None),

            (
            r"Які з наведених тверджень є правильними? I. Діагоналі будь-якого ромба рівні. II. Діагоналі будь-якого прямокутника перпендикулярні. III. Діагоналі будь-якого квадрата є бісектрисами його кутів.",
            topics["Планіметрія"], 'CHOICE', None,
            [("лише I", False), ("лише II", False), ("лише III", True), ("лише I та III", False),
             ("I, II та III", False)], None),

            (
            r"У геометричній прогресії $(b_n)$ задано $b_1 = 3$ і знаменник $q = -2$. Знайдіть четвертий член $b_4$ цієї прогресії.",
            topics["Числові послідовності"], 'CHOICE', None,
            [("-24", True), ("24", False), ("-48", False), ("-12", False), ("16", False)], None),

            (r"На тарілці лежать 5 яблук і 7 груш. Яка ймовірність того, що навмання взятий фрукт виявиться яблуком?",
             topics["Елементи стохастики"], 'CHOICE', None,
             [(r"$\frac{5}{7}$", False), (r"$\frac{7}{12}$", True), (r"$\frac{5}{12}$", False),
              (r"$\frac{1}{5}$", False), (r"$\frac{1}{12}$", False)], None),

            (
            r"Задано вектори $\vec{a}(2; -1; 3)$ та $\vec{b}(m; 2; -2)$. За якого значення $m$ ці вектори є перпендикулярними?",
            topics["Стереометрія та вектори"], 'CHOICE', None,
            [("-4", False), ("-2", False), ("0", False), ("2", False), ("4", True)], None),

            (
            r"Із точки $A$ до площини $\alpha$ проведено перпендикуляр $AO$ та похилу $AB$. Знайдіть довжину проекції похилої на площину $\alpha$, якщо $AB = 13$ см, $AO = 12$ см.",
            topics["Стереометрія та вектори"], 'CHOICE', None,
            [("1 см", False), ("5 см", True), (r"$\sqrt{313}$ см", False), ("25 см", False),
             (r"$\sqrt{119}$ см", False)], None),

            (r"Відомо, що $\begin{cases} x - y = 4 \\ x^2 - y^2 = 20 \end{cases}$. Знайдіть значення виразу $x + y$.",
             topics["Числа, вирази та рівняння"], 'CHOICE', None,
             [("5", True), ("16", False), ("24", False), ("80", False), ("Неможливо визначити", False)], None),

            (r"Обчисліть значення похідної функції $f(x) = x^3 - 4x$ у точці $x_0 = 2$.", topics["Функції та похідна"],
             'CHOICE', None,
             [("0", False), ("4", False), ("8", True), ("12", False), ("24", False)], None),

            # --- ЧАСТИНА 2: ВІДПОВІДНОСТІ (16-18) монолітні ---
            (r"Установіть відповідність між функцією (1–3) та її властивістю (А–Д).", topics["Функції та похідна"],
             'MATCH', None,
             # Варіанти праворуч (А, Б, В, Г, Д)
             [("А. Графік не перетинає вісь x.", False),
              ("Б. Функція є непарною.", False),
              ("В. Областю значень функції є проміжок [-1; 1].", False),
              ("Г. Графік функції проходить через початок координат.", False),
              ("Д. Функція спадає на всій області визначення.", False)],
             # Умови ліворуч (1, 2, 3) та індекс правильної відповіді з масиву вище
             [(r"1. $y = \frac{2}{x}$", 1),  # Б
              (r"2. $y = 3^x$", 0),  # А
              (r"3. $y = \cos x$", 2)]  # В
             ),

            (r"Установіть відповідність між виразом (1–3) та його значенням (А–Д), якщо $a = 0.5$.",
             topics["Числа, вирази та рівняння"], 'MATCH', None,
             [("А. 1", False), ("Б. 2", False), ("В. 3", False), ("Г. 4", False), ("Д. 0.5", False)],
             [(r"1. $4a + 1$", 2),  # В (3)
              (r"2. $a^{-2}$", 3),  # Г (4)
              (r"3. $|a - 1.5|$", 0)]  # А (1)
             ),

            (
            r"У прямокутному $\triangle ABC$ ($\angle C=90^\circ$) катет $AC = 6$ см, а $\angle B = 30^\circ$. Установіть відповідність між геометричною величиною (1–3) та її значенням (А–Д).",
            topics["Планіметрія"], 'MATCH', None,
            [(r"А. $6\sqrt{3}$ см", False), ("Б. 12 см", False), (r"В. $3\sqrt{3}$ см", False), ("Г. 6 см", False),
             ("Д. 18 см", False)],
            [(r"1. Гіпотенуза $AB$", 1),  # Б (12)
             (r"2. Катет $BC$", 0),  # А (6\sqrt{3})
             (r"3. Радіус описаного кола", 3)]  # Г (6)
            ),

            # --- ЧАСТИНА 3: ВІДКРИТА ФОРМА (19-22) ---
            (
            r"Ціна смартфона становила 10 000 грн. Спочатку ціну підвищили на 20%, а під час розпродажу нову ціну знизили на 15%. Якою стала остаточна ціна смартфона (у грн)?",
            topics["Числа, вирази та рівняння"], 'SHORT', "10200", [], None),

            (r"Обчисліть інтеграл $\int_1^2 (6x^2) dx$.", topics["Функції та похідна"], 'SHORT', "14", [], None),

            (
            r"Основою прямої призми є прямокутний трикутник із катетами 6 см і 8 см. Висота призми дорівнює 10 см. Знайдіть об'єм цієї призми (у см³).",
            topics["Стереометрія та вектори"], 'SHORT', "240", [], None),

            (r"Визначте найбільший корінь рівняння $(x^2 - 4x - 5)\sqrt{x - 2} = 0$.",
             topics["Числа, вирази та рівняння"], 'SHORT', "5", [], None),
        ]

        # 3. Запис у базу даних
        for text, topic, q_type, correct_short, options, match_items in questions_data:
            question = Question.objects.create(
                text=text,
                topic=topic,
                question_type=q_type,
                correct_short_answer=correct_short
            )

            created_options = []
            if options:
                for opt_text, is_correct in options:
                    opt = AnswerOption.objects.create(
                        question=question,
                        text=opt_text,
                        is_correct=is_correct
                    )
                    created_options.append(opt)

            # Якщо це завдання на відповідність, створюємо ліву колонку
            if q_type == 'MATCH' and match_items:
                for match_text, correct_opt_idx in match_items:
                    MatchItem.objects.create(
                        question=question,
                        text=match_text,
                        correct_option=created_options[correct_opt_idx]
                    )

        self.stdout.write(self.style.SUCCESS("✅ Успіх! 22 завдання (з монолітними відповідностями) завантажено."))