"""Зручні адреси уроків: /material/123-1-2-tsyfry-desiatkovyi-zapys/. Назва — транслітом за офіційною
українською системою (постанова КМУ № 55 від 27.01.2010), номер на початку — щоб адреса не ламалась,
коли назву змінено (неточна назва в адресі перенаправляє на правильну)."""
import re

TRANSLIT = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'h', 'ґ': 'g', 'д': 'd', 'е': 'e', 'є': 'ie', 'ж': 'zh', 'з': 'z',
    'и': 'y', 'і': 'i', 'ї': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p',
    'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
    'ь': '', 'ю': 'iu', 'я': 'ia',
}
WORD_START = {'є': 'ye', 'ї': 'yi', 'й': 'y', 'ю': 'yu', 'я': 'ya'}   # на початку слова — інакше
APOSTROPHES = "'’ʼ"
MAX_LENGTH = 60


def transliterate(text):
    result, prev = [], ''
    for char in text.lower():
        if char in APOSTROPHES:
            continue                       # апостроф не пишемо, і слово після нього не починається заново
        if char in TRANSLIT:
            if char in WORD_START and not prev.isalpha():
                result.append(WORD_START[char])
            elif char == 'г' and prev == 'з':
                result.append('gh')        # «зг» → «zgh», щоб не сплутати з «ж» (zh)
            else:
                result.append(TRANSLIT[char])
        else:
            result.append(char)
        prev = char
    return ''.join(result)


def slugify_title(title):
    """«1.2. Цифри. Десятковий запис» → «1-2-tsyfry-desiatkovyi-zapys» (не довше MAX_LENGTH, по межі слова)."""
    slug = re.sub(r'[^a-z0-9]+', '-', transliterate(title or '')).strip('-')
    if len(slug) > MAX_LENGTH:
        slug = slug[:MAX_LENGTH].rsplit('-', 1)[0]
    return slug or 'material'
