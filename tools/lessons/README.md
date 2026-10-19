# Інструменти для уроків (презентації й банки)

- `lessons/<папка>_<номер>.txt` — джерела презентацій (маркери `@@TITLE`, `@@BRAND`, `@@SUBJECT`, `@@PROFILE A|B`,
  `@@CSS`, `@@SLIDES`, `@@RENDER`, `@@JS`, `@@INCLUDE <файл з parts/>`); для 5 кл. — без префікса папки.
- `python3 tools/lessons/assemble.py <джерело.txt> content/school/<папка>/<номер>.html` — збирає з `lesson_template.html`.
- `python3 tools/lessons/check_lesson.py <html> [bank.py]` — перевірки сайту + 5 завдань у клітинці, 5+2 боси, назва з дерева.
- `node tools/lessons/shot_lesson.js <html> tools/lessons/shots/<назва>` і `python3 tools/lessons/sheet.py … sheet.png 0.5` —
  знімки 1280/360, світла/темна тема, контактний аркуш. Перед цим: `cd tools/lessons && npm pack mathjax@3.2.2 &&
  mkdir -p mj && tar -xzf mathjax-3.2.2.tgz -C mj` (MathJax підставляється замість закритого CDN).
- `node tools/lessons/interact.js <html> <префікс> "<js>" …` — знімок після кожного JS (інтерактив).
- `tools/lessons/finish.sh <папка> <номер> <файл повідомлення>` — перевірка, `SchoolContentTests` у чистому worktree,
  коміт і пуш поточної гілки.
- `AGENT_BRIEF.md`, `BANK_BRIEF.md` — брифи для агентів (презентація / банк).
- `tree_pdf.py` + `print_pdf.js` — PDF дерева тем зі статусами.
