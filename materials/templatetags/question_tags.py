import random
import re

from django import template

register = template.Library()
LETTERS = 'АБВГДЕЖЗ'


@register.simple_tag
def shuffled_options(question):
    """Варіанти тесту у випадковому порядку з літерами А, Б, В… за новим порядком.

    У банку правильна відповідь частіше стоїть під «Б», ніж під «Д», — без перемішування це можна вгадати.
    Відповідь перевіряється за id варіанта, тож порядок на оцінку не впливає.
    """
    options = list(question.options.all())
    random.shuffle(options)
    for index, option in enumerate(options):
        letter = LETTERS[index] if index < len(LETTERS) else str(index + 1)
        option.display_text = f'{letter}) {option.body}'
    return options


@register.simple_tag
def practice_label(material):
    """Напис кнопки практики: «Практика НМТ» для курсу НМТ, «Тренажер» / «Практика» — для шкільних тем."""
    from materials.practice import practice_button_label
    return practice_button_label(material)


PLAIN_NUMBER = re.compile(r'^\s*[-−]?\d+([.,]\d+)?\s*$')


@register.filter
def short_keyboard(question):
    """Клавіатура для короткої відповіді на телефоні й планшеті: цифрова («decimal») — лише коли відповідь —
    звичайне число чи десятковий дріб; звичайний дріб («4/9») чи текст на цифровій клавіатурі не набрати."""
    return 'decimal' if PLAIN_NUMBER.match(question.correct_short_answer or '') else 'text'
