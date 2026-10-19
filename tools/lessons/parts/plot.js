            // --- Координатна площина: спільні перетворення координат ---
            function plane(x0, x1, y0, y1, W = 420, H = 300, pad = 26) {
                const sx = (x) => pad + (x - x0) / (x1 - x0) * (W - 2 * pad);
                const sy = (y) => H - pad - (y - y0) / (y1 - y0) * (H - 2 * pad);
                return { sx, sy, x0, x1, y0, y1, W, H, pad };
            }
            function axesSvg(P, stepX = 1, stepY = 1, labelX = 'x', labelY = 'y') {
                let svg = '';
                for (let x = Math.ceil(P.x0 / stepX) * stepX; x <= P.x1; x += stepX) svg += `<line x1="${P.sx(x)}" y1="${P.sy(P.y0)}" x2="${P.sx(x)}" y2="${P.sy(P.y1)}" class="grid-line"/>`;
                for (let y = Math.ceil(P.y0 / stepY) * stepY; y <= P.y1; y += stepY) svg += `<line x1="${P.sx(P.x0)}" y1="${P.sy(y)}" x2="${P.sx(P.x1)}" y2="${P.sy(y)}" class="grid-line"/>`;
                svg += `<line x1="${P.sx(P.x0)}" y1="${P.sy(0)}" x2="${P.sx(P.x1) + 8}" y2="${P.sy(0)}" class="axis"/>`
                     + `<line x1="${P.sx(0)}" y1="${P.sy(P.y0)}" x2="${P.sx(0)}" y2="${P.sy(P.y1) - 8}" class="axis"/>`
                     + `<path d="M${P.sx(P.x1) + 8} ${P.sy(0)} l-9 -4 v8 z" fill="currentColor"/>`
                     + `<path d="M${P.sx(0)} ${P.sy(P.y1) - 8} l-4 9 h8 z" fill="currentColor"/>`
                     + `<text x="${P.sx(P.x1) + 4}" y="${P.sy(0) + 18}" class="axis-name">${labelX}</text>`
                     + `<text x="${P.sx(0) + 8}" y="${P.sy(P.y1) - 2}" class="axis-name">${labelY}</text>`;
                for (let x = Math.ceil(P.x0 / stepX) * stepX; x <= P.x1; x += stepX) if (x !== 0) svg += `<text x="${P.sx(x)}" y="${P.sy(0) + 15}" class="tick">${String(x).replace('-', '−').replace('.', ',')}</text>`;
                for (let y = Math.ceil(P.y0 / stepY) * stepY; y <= P.y1; y += stepY) if (y !== 0) svg += `<text x="${P.sx(0) - 10}" y="${P.sy(y) + 4}" class="tick">${String(y).replace('-', '−').replace('.', ',')}</text>`;
                return svg + `<text x="${P.sx(0) - 9}" y="${P.sy(0) + 15}" class="tick">0</text>`;
            }
            // Гладка крива через точки екстремумів: між сусідніми точками s(t) = 3t² − 2t³
            const smooth = (pts) => (x) => {
                for (let i = 0; i + 1 < pts.length; i++) {
                    const [ax, ay] = pts[i], [bx, by] = pts[i + 1];
                    if (x >= ax - 1e-9 && x <= bx + 1e-9) { const t = (x - ax) / (bx - ax); return ay + (by - ay) * (3 * t * t - 2 * t * t * t); }
                }
                return NaN;
            };
            // Ламана через точки
            const broken = (pts) => (x) => {
                for (let i = 0; i + 1 < pts.length; i++) {
                    const [ax, ay] = pts[i], [bx, by] = pts[i + 1];
                    if (x >= ax - 1e-9 && x <= bx + 1e-9) return ay + (by - ay) * (x - ax) / (bx - ax);
                }
                return NaN;
            };
            // Крива, розфарбована за класом кожної точки (cls(x, y) → 'pos' / 'neg' / 'up' / …)
            function curveSvg(P, f, a, b, cls = () => '') {
                let svg = '', d = '', cur = null;
                const N = 240;
                for (let i = 0; i <= N; i++) {
                    const x = a + (b - a) * i / N, y = f(x);
                    if (!isFinite(y) || y < P.y0 - 0.05 || y > P.y1 + 0.05) { if (d) svg += `<path d="${d}" class="curve ${cur}"/>`; d = ''; continue; }
                    const c = cls(x, y);
                    const pt = `${P.sx(x).toFixed(1)} ${P.sy(y).toFixed(1)}`;
                    if (d && c !== cur) { svg += `<path d="${d} L${pt}" class="curve ${cur}"/>`; d = ''; }
                    d = d ? `${d} L${pt}` : `M${pt}`;
                    cur = c;
                }
                if (d) svg += `<path d="${d}" class="curve ${cur}"/>`;
                return svg;
            }
            const num = (v) => (Math.round(v * 10) / 10).toString().replace('.', ',').replace('-', '−');
