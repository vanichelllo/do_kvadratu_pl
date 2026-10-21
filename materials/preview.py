"""Безкоштовний перегляд початку уроку: перші слайди презентації до покупки.

Решту слайдів вирізаємо на сервері, тож повний урок у браузер не потрапляє.
"""
import re

PREVIEW_SLIDES = 3

_SLIDE_OPEN = re.compile(r'<section\b[^>]*\bclass\s*=\s*["\'][^"\']*\bslide-card\b[^>]*>', re.I)
_SECTION_TAG = re.compile(r'<(/?)section\b[^>]*>', re.I)

# Скрипт уроку може звертатися до віджетів вирізаних слайдів — замість null даємо порожній елемент,
# щоб помилка не зупинила гортання
_SAFE_LOOKUP = """<script>
(function () {
    function dummy() {
        var el = document.createElement('div');
        el.querySelector = dummy;
        return el;
    }
    var byId = document.getElementById.bind(document);
    document.getElementById = function (id) { return byId(id) || dummy(); };
})();
</script>
"""

_END_SLIDE = """<section class="slide-card" data-slide="{n}">
    <div class="slide-header"><span class="slide-tag">Безкоштовний перегляд</span>
        <h2 class="slide-title">Це був початок уроку 👀</h2></div>
    <div class="slide-body">
        <p>У повному уроці ще {rest} — пояснення, інтерактивні приклади й «перевір себе»,
        а після уроку — практика сходинками.</p>
        <p>Щоб відкрити весь урок, натисніть <b>«Придбати повний урок»</b> угорі сторінки.</p>
    </div>
</section>
"""


def _slide_word(n):
    if n % 10 == 1 and n % 100 != 11:
        return f'{n} слайд'
    if 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14:
        return f'{n} слайди'
    return f'{n} слайдів'


def _section_end(html, start):
    """Кінець секції, що відкривається в позиції start (з урахуванням вкладених <section>)"""
    depth = 0
    for tag in _SECTION_TAG.finditer(html, start):
        depth += -1 if tag.group(1) else 1
        if depth == 0:
            return tag.end()
    return -1


def slide_count(html):
    return len(_SLIDE_OPEN.findall(html or ''))


def preview_slides(html):
    """Скільки слайдів показати в перегляді; 0 — перегляду немає (замало слайдів або інша будова)"""
    total = slide_count(html)
    return min(PREVIEW_SLIDES, total - 1) if total >= 3 else 0


def build_preview(html):
    """HTML з першими слайдами й заключним слайдом-запрошенням; '' — якщо перегляд неможливий"""
    shown = preview_slides(html)
    if not shown:
        return ''
    starts = [m.start() for m in _SLIDE_OPEN.finditer(html)]
    cut_from = starts[shown]
    cut_to = _section_end(html, starts[-1])
    head_end = html.lower().find('</head>')
    if cut_to < 0 or head_end < 0 or head_end > starts[0]:
        return ''
    end_slide = _END_SLIDE.format(n=shown + 1, rest=_slide_word(len(starts) - shown))
    return html[:head_end] + _SAFE_LOOKUP + html[head_end:cut_from] + end_slide + html[cut_to:]
