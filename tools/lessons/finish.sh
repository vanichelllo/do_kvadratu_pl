#!/usr/bin/env bash
# finish.sh <папка> <номер> <файл з повідомленням коміту> — перевірка, тест, коміт і пуш уроку
# (презентація обов'язкова, банк — якщо вже є). Посилання на сесію для коміту — у змінній CLAUDE_SESSION_URL. Тест імпорту проганяється в чистому worktree
# (закомічене + файли цього уроку), щоб недороблені файли паралельних агентів не впливали.
set -euo pipefail
REPO=/home/user/do_kvadratu_pl
SP=$(cd "$(dirname "$0")" && pwd)
WT=/tmp/lessons-wt
cd $REPO
D=content/school/$1; N=$2; MSG=$3
: "${CLAUDE_SESSION_URL:?задайте CLAUDE_SESSION_URL=https://claude.ai/code/session_…}"
BRANCH=$(git rev-parse --abbrev-ref HEAD)
FILES="$D/$N.html $D/meta.json"
[ -f $D/bank_$N.py ] && FILES="$FILES $D/bank_$N.py"
if [ -f $D/bank_$N.py ]; then python3 $SP/check_lesson.py $D/$N.html $D/bank_$N.py | grep -v "^  завдань\|^  типи"
else python3 $SP/check_lesson.py $D/$N.html; fi
[ -d $WT ] || git worktree add -q --detach $WT HEAD
git -C $WT checkout -q --detach "$(git rev-parse HEAD)"
git -C $WT reset -q --hard && git -C $WT clean -fdq
for f in $FILES; do mkdir -p "$WT/$(dirname $f)"; cp "$f" "$WT/$f"; done
(cd $WT && SECRET_KEY=x python3 manage.py test materials.tests.SchoolContentTests 2>&1 | tail -3 | grep -q "^OK") \
  || { echo "ТЕСТ НЕ ПРОЙШОВ"; (cd $WT && SECRET_KEY=x python3 manage.py test materials.tests.SchoolContentTests 2>&1 | tail -30); exit 1; }
git -C $WT reset -q --hard && git -C $WT clean -fdq
git add $FILES
printf '%s\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nClaude-Session: %s\n' "$(cat $MSG)" "$CLAUDE_SESSION_URL" | git commit -q -F -
for i in 1 2 3 4; do git push -q -u origin "$BRANCH" && break || sleep $((2**i)); done
git log --oneline -1
