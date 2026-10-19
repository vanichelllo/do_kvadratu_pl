            // --- Покрокове розв'язання (STEPS задає урок): кожен клік додає рядок ---
            let shown = 1;
            window.renderEval = function () {
                const box = document.getElementById('eval-lines');
                box.innerHTML = STEPS.slice(0, shown).map(([line], k) => {
                    const html = line.replace(/\[\[(.+?)\]\]/g, k === shown - 1 ? '<mark>$1</mark>' : '$1');
                    return `<div class="eval-line${k === STEPS.length - 1 ? ' done' : ''}">${html}</div>`;
                }).join('');
                document.getElementById('eval-note').innerHTML = STEPS[shown - 1][1];
                if (window.MathJax && MathJax.typesetPromise) MathJax.typesetPromise([box, document.getElementById('eval-note')]);
            };
            window.evalStep = function () { shown = Math.min(shown + 1, STEPS.length); renderEval(); };
            window.evalReset = function () { shown = 1; renderEval(); };

            // --- Кроки прикладів з'являються по кліку ---
            window.nextStep = function (id) {
                const next = document.querySelector(`#${id} .step:not(.shown)`);
                if (next) next.classList.add('shown');
            };

            // --- Практика: перемикач завдань ---
            window.showTask = function (n) {
                document.querySelectorAll('.practice-task').forEach((t, k) => {
                    t.classList.toggle('on', k + 1 === n);
                    document.getElementById(`tab-${k + 1}`).classList.toggle('on', k + 1 === n);
                });
                if (window.onTask) window.onTask(n);
            };
