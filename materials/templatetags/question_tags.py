import random

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
