// Section 3 · Book of Business model
(() => {
  const scope = document.getElementById('final-deck'); if (!scope) return;
  const NS = 'http://www.w3.org/2000/svg';
  const mk = (tag, attrs, text) => { const e = document.createElementNS(NS, tag); Object.entries(attrs).forEach(([k, v]) => e.setAttribute(k, v)); if (text !== undefined) e.textContent = text; return e; };
  const R = [0.20, 0.35, 0.50, 0.60, 0.65, 0.70]; const CM = ['Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'];
  const mult = (ci) => (ci < 6 ? R.slice(0, 6 - ci).reduce((s, x) => s + x, 0) : 0);
  const usd = (v) => (v >= 1e6 ? `USD ${(v / 1e6).toFixed(1)}M` : `USD ${Math.round(v / 1000)}K`);
  const BASE = [
    { t: 'Tier 1', acc: 40, emp: 950, pe: 240, meet: .85, qual: .75, win: .28, timing: { 0: .4, 1: .3, 2: .3 } },
    { t: 'Tier 2', acc: 60, emp: 700, pe: 130, meet: .50, qual: .60, win: .20, timing: { 2: .25, 3: .5, 4: .25 } },
    { t: 'Tier 3', acc: 50, emp: 500, pe: 70, meet: .30, qual: .50, win: .12, timing: { 4: .5, 5: .5 } },
  ];
  function model(p) {
    const tiers = BASE.map((T) => ({ ...T, timing: { ...T.timing } }));
    tiers[0].win = p.w1 / 100; tiers[1].win = p.w2 / 100; tiers[0].meet = p.m1 / 100; tiers[0].emp = p.e1;
    const monthly = [0, 0, 0, 0, 0, 0]; const tot = { acc: 0, meet: 0, opp: 0, win: 0, pot: 0, pipe: 0, won: 0, h1: 0, jun: 0 };
    const rows = tiers.map((T) => {
      const annual = T.emp * T.pe, mo = annual / 12, meet = T.acc * T.meet, opp = meet * T.qual, win = opp * T.win; let h1 = 0, jun = 0; const closes = [];
      Object.entries(T.timing).forEach(([c, share]) => {
        const ci = Number(c) + p.slip, w = win * share; closes.push(CM[Math.min(ci, 6)] || 'H2');
        h1 += w * mo * mult(ci); for (let k = ci; k < 6; k++) monthly[k] += w * mo * R[k - ci]; if (ci <= 5) jun += w * mo * R[5 - ci];
      });
      tot.acc += T.acc; tot.meet += meet; tot.opp += opp; tot.win += win; tot.pot += T.acc * annual; tot.pipe += opp * annual; tot.won += win * annual; tot.h1 += h1; tot.jun += jun;
      return { t: T.t, acc: T.acc, meet, opp, rate: T.win, win, closes: [...new Set(closes)].join('–'), h1 };
    });
    return { rows, tot, monthly, cum: monthly.map((_, i) => monthly.slice(0, i + 1).reduce((s, x) => s + x, 0)) };
  }
  const ids = { w1: 'q_w1', w2: 'q_w2', m1: 'q_m1', e1: 'q_e1', slip: 'q_slip' };
  const fmt = { w1: (v) => v + '%', w2: (v) => v + '%', m1: (v) => v + '%', e1: (v) => num(v) };
  function draw() {
    const p = {}; Object.entries(ids).forEach(([k, id]) => { p[k] = Number(document.getElementById(id).value); });
    Object.entries(fmt).forEach(([k, f]) => scope.querySelectorAll(`[data-o=${ids[k]}]`).forEach((e) => { e.textContent = f(p[k]); }));
    const r = model(p), t = r.tot;
    const vals = { portfolio: usd(t.pot), pipe: usd(t.pipe), opps: Math.round(t.opp), won: usd(t.won), wins: Math.round(t.win), rate: Math.round(t.win / t.opp * 100) + '%', h1: usd(t.h1), quota: Math.round(t.h1 / 350000 * 100) + '%', jun: usd(t.jun) };
    Object.entries(vals).forEach(([k, v]) => scope.querySelectorAll(`[data-kb3=${k}]`).forEach((e) => { e.textContent = v; }));
    const tb = document.getElementById('bobFunnel'); tb.replaceChildren();
    r.rows.forEach((x) => { const tr = tb.insertRow(); [x.t, x.acc, Math.round(x.meet), x.opp.toFixed(1), Math.round(x.rate * 100) + '%', x.win.toFixed(1), x.closes, usd(x.h1)].forEach((v) => { tr.insertCell().textContent = v; }); });
    const tr = tb.insertRow(); tr.className = 'tot'; ['Total', t.acc, Math.round(t.meet), t.opp.toFixed(1), Math.round(t.win / t.opp * 100) + '%', t.win.toFixed(1), '', usd(t.h1)].forEach((v) => { const c = tr.insertCell(); c.textContent = v; c.style.fontWeight = '700'; });
    // cumulative chart
    const host = document.getElementById('chartCum'); const W = 560, H = 200, pl = 6, pt = 18, pb = 24; const ML6 = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'];
    const max = Math.max(380000, ...r.cum) * 1.08; const bw = (W - pl * 2) / 6; const y = (v) => pt + (H - pt - pb) * (1 - v / max);
    const svg = mk('svg', { viewBox: `0 0 ${W} ${H}`, role: 'img', 'aria-label': `Cumulative H1 GB reaches ${usd(t.h1)} against a USD 350K quota` });
    for (let m = 0; m < 6; m++) { const x = pl + m * bw; svg.appendChild(mk('rect', { x: x + bw * .14, y: y(r.cum[m]), width: bw * .72, height: H - pb - y(r.cum[m]), rx: 2, fill: m === 5 ? 'var(--mint)' : 'var(--b-mid)' }));
      svg.appendChild(mk('text', { x: x + bw / 2, y: y(r.cum[m]) - 5, 'text-anchor': 'middle', 'font-size': 11, 'font-weight': m === 5 ? 700 : 500, fill: 'var(--ink)' }, usd(r.cum[m])));
      svg.appendChild(mk('text', { x: x + bw / 2, y: H - 7, 'text-anchor': 'middle', 'font-size': 11, fill: 'var(--tertiary)' }, ML6[m])); }
    svg.appendChild(mk('line', { x1: pl, x2: W - pl, y1: y(350000), y2: y(350000), stroke: 'var(--ink)', 'stroke-width': 1.5, 'stroke-dasharray': '5 4' }));
    svg.appendChild(mk('text', { x: pl + 4, y: y(350000) - 5, 'font-size': 11, 'font-weight': 700, fill: 'var(--ink)' }, 'Quota USD 350K'));
    host.replaceChildren(svg);
  }
  Object.values(ids).forEach((id) => document.getElementById(id).addEventListener('input', draw));
  draw();
  // multiplier chart
  const host = document.getElementById('chartMult'); const W = 560, H = 230, pl = 6, pt = 22, pb = 24; const bw = (W - pl * 2) / 7; const y = (v) => pt + (H - pt - pb) * (1 - v / 3.3);
  const svg = mk('svg', { viewBox: `0 0 ${W} ${H}`, role: 'img', 'aria-label': 'H1 value of a deal by close month: December 3.0 months, May 0.2 months' });
  CM.forEach((m, i) => { const v = mult(i), x = pl + i * bw; svg.appendChild(mk('rect', { x: x + bw * .14, y: y(v), width: bw * .72, height: Math.max(1, H - pb - y(v)), rx: 2, fill: i <= 2 ? 'var(--mint)' : 'var(--b-mid)' }));
    svg.appendChild(mk('text', { x: x + bw / 2, y: y(v) - 5, 'text-anchor': 'middle', 'font-size': 12, 'font-weight': 700, fill: 'var(--ink)' }, v.toFixed(2).replace(/0$/, '')));
    svg.appendChild(mk('text', { x: x + bw / 2, y: H - 7, 'text-anchor': 'middle', 'font-size': 11, fill: 'var(--tertiary)' }, m)); });
  host.replaceChildren(svg);
})();
