            // --- Дві прямі a, b і січна c. Кути при точках A (на a) і B (на b) ---
            // thetaC — напрям січної (°), delta — нахил прямої b (°). Кути: UR, UL, LL, LR при вершині A чи B.
            function transversalGeom(thetaC, delta) {
                const rad = (d) => d * Math.PI / 180, u = 55, cx = 210, cy = 150;
                const A = [1.3 * Math.cos(rad(thetaC)), 1.3 * Math.sin(rad(thetaC))], B = [-A[0], -A[1]];
                const S = ([x, y]) => [cx + u * x, cy - u * y];
                const along = (P, deg, t) => [P[0] + t * Math.cos(rad(deg)), P[1] + t * Math.sin(rad(deg))];
                // Межі кутів (проти годинникової стрілки) при кожній вершині
                const sectors = {
                    A: { UR: [0, thetaC], UL: [thetaC, 180], LL: [180, thetaC + 180], LR: [thetaC + 180, 360] },
                    B: { UR: [delta, thetaC], UL: [thetaC, 180 + delta], LL: [180 + delta, thetaC + 180], LR: [thetaC + 180, 360 + delta] },
                };
                return { A, B, S, along, sectors, rad };
            }
            function transversalSvg(thetaC, delta, angles = []) {
                const G = transversalGeom(thetaC, delta), { A, B, S, along } = G;
                const line = (P, Q, cls) => { const [x1, y1] = S(P), [x2, y2] = S(Q); return `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" class="${cls}"/>`; };
                const text = (P, s, cls) => { const [x, y] = S(P); return `<text x="${x}" y="${y + 6}" class="${cls}">${s}</text>`; };
                let svg = '';
                angles.forEach(({ at, which, label, cls }) => {
                    const [s0, s1] = G.sectors[at][which], V = at === 'A' ? A : B, r = 0.5;
                    const [vx, vy] = S(V), [x0, y0] = S(along(V, s0, r)), [x1, y1] = S(along(V, s1, r));
                    svg += `<path d="M${vx} ${vy} L${x0} ${y0} A${r * 55} ${r * 55} 0 ${s1 - s0 > 180 ? 1 : 0} 0 ${x1} ${y1} Z" class="angle-arc ${cls || ''}"/>`;
                    if (label) svg += text(along(V, (s0 + s1) / 2, 0.86), label, `angle-label ${cls || ''}`);
                });
                svg += line(along(A, 0, -4.2), along(A, 0, 4.2), 'geo-line')
                     + line(along(B, delta, -4.2), along(B, delta, 4.2), 'geo-line')
                     + line(along([0, 0], thetaC, -2.7), along([0, 0], thetaC, 2.7), 'geo-line sec')
                     + text(along(along(A, 0, 3.3 - A[0]), 90, 0.32), 'a', 'line-name') + text(along(along(B, delta, (3.3 - B[0]) / Math.cos(G.rad(delta))), delta + 90, 0.32), 'b', 'line-name')
                     + text(along(along([0, 0], thetaC, 2.55), thetaC + 90, 0.3), 'c', 'line-name');
                [A, B].forEach((P) => { const [x, y] = S(P); svg += `<circle cx="${x}" cy="${y}" r="4.5" class="geo-dot"/>`; });
                return svg;
            }
            function angleValue(thetaC, delta, at, which) {
                const [s0, s1] = transversalGeom(thetaC, delta).sectors[at][which];
                return Math.round(s1 - s0);
            }
