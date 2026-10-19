"""Збирає презентацію з шаблону: python3 assemble.py <джерело.txt> <вихід.html>
Джерело: рядки-маркери @@TITLE <назва>, @@BRAND <курс>, @@SUBJECT <предмет>, @@PROFILE A|B,
@@CSS, @@SLIDES, @@RENDER, @@JS — вміст іде після маркера."""
import os, re, sys
SP = os.path.dirname(os.path.abspath(__file__))
src, out = sys.argv[1], sys.argv[2]
text = open(src, encoding='utf-8').read()
# @@INCLUDE <файл> — вставляє спільний фрагмент (CSS чи JS) з папки parts
text = re.sub(r'^@@INCLUDE\s+(\S+)\s*$', lambda m: open(f'{SP}/parts/{m.group(1)}', encoding='utf-8').read().rstrip('\n'), text, flags=re.M)
parts, meta, cur = {'CSS': [], 'SLIDES': [], 'RENDER': [], 'JS': []}, {'BRAND': 'Математика (5-6 класи)', 'SUBJECT': 'Математика', 'PROFILE': 'A'}, None
for line in text.split('\n'):
    m = re.match(r'^@@(TITLE|BRAND|SUBJECT|PROFILE|CSS|SLIDES|RENDER|JS)\s*(.*)$', line)
    if m:
        if m.group(1) in parts: cur = m.group(1)
        else: meta[m.group(1)] = m.group(2).strip()
        continue
    if cur: parts[cur].append(line)
tpl = open(SP + '/lesson_template.html', encoding='utf-8').read()
check = open(SP + f"/check_{meta['PROFILE']}.txt", encoding='utf-8').read()
slides = '\n'.join(parts['SLIDES']).strip('\n')
total = len(re.findall(r'class="slide-card[ "]', slides))
html = (tpl.replace('{{TITLE}}', meta['TITLE']).replace('{{BRAND}}', meta['BRAND']).replace('{{SUBJECT}}', meta['SUBJECT'])
        .replace('{{CSS}}', '\n'.join(parts['CSS']).strip('\n'))
        .replace('{{SLIDES}}', slides).replace('{{RENDER}}', '\n'.join(parts['RENDER']).strip('\n'))
        .replace('{{JS}}', '\n'.join(parts['JS']).strip('\n')).replace('{{CHECK}}', check).replace('{{TOTAL}}', str(total)))
assert '{{' not in html.replace('${{', ''), 'залишився маркер'
open(out, 'w', encoding='utf-8').write(html)
print(f'{out}: {total} слайдів, {len(html.encode())} байт')
