"""Будує красивий HTML дерева тем (для друку в PDF): python3 tree_pdf.py <вихід.html>"""
import re, subprocess, sys, html
REPO = '/home/user/do_kvadratu_pl'
doc = open(f'{REPO}/docs/html_prompt.md', encoding='utf-8').read().split('## 7. ДЕРЕВО', 1)[1].split('### Підготовка до НМТ')[0]
git = lambda *a: subprocess.run(['git', '-C', REPO, *a], capture_output=True, text=True).stdout
tracked = set(git('ls-files', 'content/school').split())
added = set(re.findall(r'^\+  - (.+)$', git('diff', 'e14578a~3', 'HEAD', '--', 'docs/html_prompt.md'), flags=re.M))
FOLD = {'Математика (5-6 класи)': 'math', 'Алгебра (7-9 класи)': 'algebra', 'Геометрія (7-9 класи)': 'geometry',
        'Алгебра і початки аналізу (10-11 класи)': 'algebra', 'Геометрія (10-11 класи)': 'geometry'}
COLORS = {'Математика (5-6 класи)': '#27ae60', 'Алгебра (7-9 класи)': '#344e86', 'Геометрія (7-9 класи)': '#8e44ad',
          'Алгебра і початки аналізу (10-11 класи)': '#c0392b', 'Геометрія (10-11 класи)': '#d35400'}

# Розбір дерева: курс → клас → розділ → теми
courses = []
for line in doc.split('\n'):
    if line.startswith('### '): courses.append({'name': line[4:].strip(), 'grades': []})
    elif line.startswith('#### '): courses[-1]['grades'].append({'name': line[5:].strip(), 'chapters': []})
    elif (m := re.match(r'^- \*\*(.+)\*\*$', line)): courses[-1]['grades'][-1]['chapters'].append({'name': m.group(1), 'topics': []})
    elif (m := re.match(r'^  - ((\d+\.\d+)\. (.+))$', line)):
        courses[-1]['grades'][-1]['chapters'][-1]['topics'].append((m.group(2), m.group(3), m.group(1)))

tot = {'t': 0, 'p': 0, 'b': 0, 'n': 0}
def badges(folder, stem, full=None):
    s, st = '', {}
    if f'content/school/{folder}/{stem}.html' in tracked: s += '<span class="bd p">презентація</span>'; st['p'] = 1
    if f'content/school/{folder}/bank_{stem}.py' in tracked: s += '<span class="bd b">банк</span>'; st['b'] = 1
    if full in added: s += '<span class="bd n">нова</span>'; st['n'] = 1
    return s, st

body = []
for c in courses:
    color = COLORS[c['name']]
    body.append(f'<section class="course" style="--c:{color}"><h1><span class="sq">²</span>{html.escape(c["name"])}</h1>')
    for g in c['grades']:
        num = g['name'].split()[0]; folder = f'{FOLD[c["name"]]}-{num}'
        topics = [t for ch in g['chapters'] for t in ch['topics']]
        done = sum(f'content/school/{folder}/{t[0]}.html' in tracked for t in topics)
        pct = round(100 * done / len(topics)) if topics else 0
        body.append(f'<div class="grade"><h2>{html.escape(g["name"])}<span class="gstat">{done} з {len(topics)} презентацій'
                    f'<span class="bar"><i style="width:{pct}%"></i></span></span></h2><div class="chapters">')
        for ch in g['chapters']:
            n = re.match(r'Розділ (\d+)', ch['name']).group(1)
            sb, _ = badges(folder, f'summary-{n}')
            rows = []
            for stem, name, full in ch['topics']:
                b, st = badges(folder, stem, full)
                tot['t'] += 1; tot['p'] += st.get('p', 0); tot['b'] += st.get('b', 0); tot['n'] += st.get('n', 0)
                rows.append(f'<li><span class="num">{stem}</span><span class="nm">{html.escape(name)}</span><span class="bds">{b}</span></li>')
            title = re.sub(r'^Розділ \d+\. ', '', ch['name'])
            body.append(f'<div class="chapter"><h3><span class="chn">Розділ {n}</span>{html.escape(title)}</h3><ul>{"".join(rows)}'
                        f'<li class="sum"><span class="num">∑</span><span class="nm">Узагальнення розділу</span><span class="bds">{sb}</span></li></ul></div>')
        body.append('</div></div>')
    body.append('</section>')

page = f'''<!DOCTYPE html><html lang="uk"><head><meta charset="utf-8"><title>Дерево тем — ДО КВАДРАТУ</title><style>
@page {{ size: A4; margin: 14mm 12mm 16mm; }}
* {{ box-sizing: border-box; }}
body {{ font-family: Inter, 'DejaVu Sans', sans-serif; color: #2c3e50; margin: 0; font-size: 9.6pt; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
.cover {{ border-radius: 14px; background: linear-gradient(135deg, #344e86, #27ae60); color: #fff; padding: 22px 26px; margin-bottom: 16px; }}
.logo {{ font-weight: 800; letter-spacing: .08em; font-size: 11pt; opacity: .9; }}
.logo b {{ display: inline-block; background: #fff; color: #344e86; border-radius: 6px; padding: 1px 7px; margin-right: 6px; }}
.cover h1 {{ font-size: 24pt; margin: 10px 0 4px; font-weight: 800; }}
.cover p {{ margin: 0; opacity: .9; }}
.tiles {{ display: flex; gap: 10px; margin-top: 16px; }}
.tile {{ flex: 1; background: rgba(255,255,255,.16); border-radius: 10px; padding: 9px 12px; }}
.tile b {{ display: block; font-size: 18pt; font-weight: 800; }}
.legend {{ display: flex; gap: 14px; align-items: center; margin: 0 2px 6px; color: #7f8c8d; font-size: 8.8pt; flex-wrap: wrap; }}
.course {{ break-before: page; }}
.course:first-of-type {{ break-before: auto; }}
.course h1 {{ font-size: 16pt; margin: 6px 0 10px; color: var(--c); display: flex; align-items: center; gap: 10px; border-bottom: 3px solid var(--c); padding-bottom: 6px; }}
.sq {{ display: inline-flex; width: 26px; height: 26px; border-radius: 7px; background: var(--c); color: #fff; align-items: center; justify-content: center; font-size: 13pt; }}
.grade h2 {{ font-size: 12.5pt; margin: 12px 0 8px; display: flex; justify-content: space-between; align-items: center; break-after: avoid; }}
.gstat {{ font-size: 8.5pt; font-weight: 600; color: #7f8c8d; display: flex; align-items: center; gap: 8px; }}
.bar {{ display: inline-block; width: 90px; height: 7px; border-radius: 4px; background: #e6eaf0; overflow: hidden; }}
.bar i {{ display: block; height: 100%; background: var(--c); }}
.chapters {{ columns: 2; column-gap: 12px; }}
.chapter {{ break-inside: avoid; border: 1px solid #dce3ec; border-top: 4px solid var(--c); border-radius: 9px; padding: 8px 10px 6px; margin-bottom: 12px; background: #fff; }}
.chapter h3 {{ margin: 0 0 6px; font-size: 10.2pt; line-height: 1.3; }}
.chn {{ display: block; font-size: 7.6pt; text-transform: uppercase; letter-spacing: .06em; color: var(--c); font-weight: 800; }}
ul {{ list-style: none; margin: 0; padding: 0; }}
li {{ display: flex; gap: 6px; align-items: baseline; padding: 3px 0; border-top: 1px dashed #edf0f4; line-height: 1.3; }}
li:first-child {{ border-top: none; }}
li.sum {{ color: #7f8c8d; font-style: italic; }}
.num {{ flex: 0 0 30px; font-weight: 800; color: var(--c); font-variant-numeric: tabular-nums; }}
.nm {{ flex: 1; }}
.bds {{ display: flex; gap: 3px; flex-wrap: wrap; justify-content: flex-end; }}
.bd {{ font-size: 6.6pt; font-weight: 700; border-radius: 9px; padding: 1px 6px; white-space: nowrap; font-style: normal; }}
.bd.p {{ background: #e3f6ea; color: #1e8449; }}
.bd.b {{ background: #e5ebf7; color: #344e86; }}
.bd.n {{ background: #fdf0d8; color: #b9770e; }}
.note {{ color: #7f8c8d; font-size: 8.4pt; margin: 4px 2px 12px; }}
</style></head><body>
<div class="cover"><div class="logo"><b>²</b>ДО КВАДРАТУ</div><h1>Дерево тем шкільних курсів</h1>
<p>Класифікатор уроків сайту dokvadratu.com.ua · 5–11 класи · станом на 19.10.2026</p>
<div class="tiles"><div class="tile"><b>{tot["t"]}</b>тем</div><div class="tile"><b>{tot["p"]}</b>презентацій</div>
<div class="tile"><b>{tot["b"]}</b>банків завдань</div><div class="tile"><b>{tot["n"]}</b>тем додано з планів</div></div></div>
<div class="legend"><span class="bd p">презентація</span> є презентація <span class="bd b">банк</span> є банк завдань
<span class="bd n">нова</span> тема додана з планів учнів</div>
<p class="note">Стан — за гілкою PR #39 (ще не злитою в main). У кожному розділі є також урок «Узагальнення», у кожному класі — «Діагностика».</p>
{"".join(body)}</body></html>'''
open(sys.argv[1], 'w', encoding='utf-8').write(page)
print(tot)
