// Tabs with hash routing
(() => {
  const TABS = ['radar', 'panel-deck', 'salles-review', 'internal-brief'];
  const show = (id) => {
    if (id === 'client-deck') id = 'panel-deck';
    if (!TABS.includes(id)) id = 'radar';
    document.querySelectorAll('[data-tab]').forEach((p) => { p.hidden = p.dataset.tab !== id; });
    document.querySelectorAll('.tabs button').forEach((b) => b.setAttribute('aria-selected', String(b.dataset.go === id)));
    window.__activeTab = id;
  };
  document.querySelectorAll('.tabs button').forEach((b) => b.addEventListener('click', () => { history.replaceState(null, '', '#' + b.dataset.go); show(b.dataset.go); window.scrollTo(0, 0); }));
  window.addEventListener('hashchange', () => show(location.hash.slice(1)));
  show(location.hash.slice(1));
})();

// Deck navigation
document.querySelectorAll('.tabpanel .slides').forEach((deck) => {
  const panel = deck.closest('.tabpanel'); const slides = [...deck.querySelectorAll('.slide')];
  const count = panel.querySelector('.count'); const prev = panel.querySelector('[data-act=prev]'); const next = panel.querySelector('[data-act=next]'); const all = panel.querySelector('[data-act=all]');
  slides.forEach((s, i) => { s.querySelectorAll('.pg').forEach((p) => { p.textContent = `${i + 1} / ${slides.length}`; }); s.setAttribute('aria-label', `Slide ${i + 1}: ${s.dataset.title}`); });
  let cur = 0, showAll = false;
  const render = () => {
    slides.forEach((s, i) => { s.hidden = !showAll && i !== cur; });
    count.textContent = showAll ? `${slides.length} slides` : `${cur + 1} / ${slides.length}`;
    prev.disabled = showAll || cur === 0; next.disabled = showAll || cur === slides.length - 1;
    all.setAttribute('aria-pressed', String(showAll)); all.textContent = showAll ? 'One at a time' : 'Show all';
  };
  prev.addEventListener('click', () => { cur = Math.max(0, cur - 1); render(); });
  next.addEventListener('click', () => { cur = Math.min(slides.length - 1, cur + 1); render(); });
  all.addEventListener('click', () => { showAll = !showAll; render(); });
  document.addEventListener('keydown', (e) => {
    if (panel.hidden || showAll || /INPUT|SELECT|TEXTAREA/.test(document.activeElement.tagName)) return;
    if (e.key === 'ArrowRight' || e.key === 'PageDown') { cur = Math.min(slides.length - 1, cur + 1); render(); }
    if (e.key === 'ArrowLeft' || e.key === 'PageUp') { cur = Math.max(0, cur - 1); render(); }
  });
  render();
});

// Slide charts
(() => {
  const NS = 'http://www.w3.org/2000/svg';
  const mk = (tag, attrs, text) => { const e = document.createElementNS(NS, tag); Object.entries(attrs).forEach(([k, v]) => e.setAttribute(k, v)); if (text !== undefined) e.textContent = text; return e; };
  function bars(host, labels, values, opt) {
    const W = 520, H = 210, pl = 6, pr = 6, pt = 22, pb = 22; const n = values.length; const bw = (W - pl - pr) / n;
    const lo = opt.base ?? 0, hi = Math.max(...values) * (opt.headroom ?? 1.05);
    const y = (v) => pt + (H - pt - pb) * (1 - (v - lo) / (hi - lo));
    const svg = mk('svg', { viewBox: `0 0 ${W} ${H}`, role: 'img', 'aria-label': opt.label });
    values.forEach((v, i) => {
      const hl = opt.hl.includes(i);
      svg.appendChild(mk('rect', { x: pl + i * bw + bw * 0.14, y: y(v), width: bw * 0.72, height: Math.max(1, H - pb - y(v)), rx: 2, fill: hl ? 'var(--accent)' : 'var(--b-mid)' }));
      svg.appendChild(mk('text', { x: pl + i * bw + bw / 2, y: y(v) - 5, 'text-anchor': 'middle', 'font-size': 11, 'font-weight': hl ? 700 : 500, fill: 'var(--ink)' }, opt.fmt(v)));
      svg.appendChild(mk('text', { x: pl + i * bw + bw / 2, y: H - 6, 'text-anchor': 'middle', 'font-size': 11, fill: 'var(--tertiary)' }, labels[i]));
    });
    host.replaceChildren(svg);
  }
  const ML1 = ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'];
  const a = byKey['5412|people'];
  if (a) bars(document.getElementById('chartAudit'), ML1, M.map((m) => a[m]), { base: 94, fmt: (v) => Math.round(v), hl: [0, 1, 2], label: 'Audit firm headcount index by month, highest in January to March', headroom: 1.01 });
  const tax = KW.series.find((s) => s.keyword === 'declaracion anual personas morales');
  if (tax) { const i0 = KW.months.indexOf('2025-01'); const v = tax.values.slice(i0, i0 + 12);
    bars(document.getElementById('chartTax'), ML1, v, { base: 0, fmt: (x) => (x >= 1000 ? (x / 1000).toFixed(1) + 'K' : String(x)), hl: [1, 2, 3], label: 'Searches for annual corporate tax return peak in March 2025 at 9,900' }); }
})();

// Business-case engine
window.GB = (() => {
  const RIDE = 10, EATS = 15, CURVE = [0.20, 0.35, 0.50, 0.60, 0.65, 0.70], QUOTA = 350000;
  const calc = (p) => {
    const ceil = (p.ceil ?? 70) / 70;
    const field = p.emp * p.field / 100, other = p.emp - field;
    const busy = (field * p.busy + other * 0.5) * RIDE + field * p.eats * (p.part / 100) * EATS;
    const off = (field * p.off + other * 0.5) * RIDE + p.emp * 0.1 * EATS;
    const pot = Array.from({ length: 12 }, (_, m) => (m < 5 ? busy : off));
    const proj = pot.slice(0, 6).map((v, m) => (m >= p.go ? v * CURVE[m - p.go] * ceil : 0));
    const sum = (a) => a.reduce((s, x) => s + x, 0);
    return { pot, proj, annual: sum(pot), h1pot: sum(pot.slice(0, 6)), h1: sum(proj), quota: sum(proj) / QUOTA };
  };
  const DEF = { emp: 1000, field: 65, busy: 4, off: 2, eats: 2, part: 35, ceil: 70, go: 0 };
  const CONS = { ...DEF, busy: 2, off: 1, ceil: 50 };
  const usd = (v) => (v >= 1e6 ? `USD ${(v / 1e6).toFixed(2)}M` : v >= 1000 ? `USD ${Math.round(v / 1000)}K` : `USD ${Math.round(v)}`);
  const pct = (v) => `${Math.round(v * 100)}%`;
  return { calc, DEF, CONS, usd, pct };
})();
(() => {
  const NS = 'http://www.w3.org/2000/svg';
  const mk = (tag, attrs, text) => { const e = document.createElementNS(NS, tag); Object.entries(attrs).forEach(([k, v]) => e.setAttribute(k, v)); if (text !== undefined) e.textContent = text; return e; };
  // Internal GB calculator
  const A = { emp: 'a_emp', field: 'a_field', busy: 'a_busy', off: 'a_off', eats: 'a_eats', part: 'a_part', ceil: 'a_ceil', go: 'a_go' };
  const fmtA = { emp: (v) => num(v), field: (v) => v + '%', busy: (v) => v, off: (v) => v, eats: (v) => v, part: (v) => v + '%', ceil: (v) => v + '%' };
  const readA = () => { const p = {}; Object.entries(A).forEach(([k, id]) => { p[k] = Number(document.getElementById(id).value); }); return p; };
  const setA = (p) => { Object.entries(A).forEach(([k, id]) => { document.getElementById(id).value = p[k]; }); };
  function drawA() {
    const p = readA(); Object.entries(fmtA).forEach(([k, f]) => { document.querySelectorAll(`[data-o=${A[k]}]`).forEach((e) => { e.textContent = f(p[k]); }); });
    const r = GB.calc(p);
    document.querySelectorAll('[data-ka=annual]').forEach((e) => { e.textContent = GB.usd(r.annual); });
    document.querySelectorAll('[data-ka=h1pot]').forEach((e) => { e.textContent = GB.usd(r.h1pot); });
    document.querySelectorAll('[data-ka=h1]').forEach((e) => { e.textContent = GB.usd(r.h1); });
    document.querySelectorAll('[data-ka=quota]').forEach((e) => { e.textContent = GB.pct(r.quota); });
    const isCons = ['busy', 'off', 'ceil'].every((k) => p[k] === GB.CONS[k]); const isBase = ['busy', 'off', 'ceil'].every((k) => p[k] === GB.DEF[k]);
    document.querySelectorAll('#calcA [data-scen]').forEach((b) => b.setAttribute('aria-pressed', String((b.dataset.scen === 'cons' && isCons) || (b.dataset.scen === 'base' && isBase))));
    const host = document.getElementById('chartA'); const W = 560, H = 190, pl = 4, pt = 20, pb = 24; const ML6 = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'];
    const max = Math.max(...r.pot.slice(0, 6)) * 1.12; const bw = (W - pl * 2) / 6; const y = (v) => pt + (H - pt - pb) * (1 - v / max);
    const svg = mk('svg', { viewBox: `0 0 ${W} ${H}`, role: 'img', 'aria-label': `Projected GB by month, H1 2027 total ${GB.usd(r.h1)}` });
    for (let m = 0; m < 6; m++) {
      const x = pl + m * bw;
      svg.appendChild(mk('rect', { x: x + bw * 0.12, y: y(r.pot[m]), width: bw * 0.76, height: H - pb - y(r.pot[m]), rx: 2, fill: 'var(--b-mid)' }));
      if (r.proj[m] > 0) svg.appendChild(mk('rect', { x: x + bw * 0.12, y: y(r.proj[m]), width: bw * 0.76, height: H - pb - y(r.proj[m]), rx: 2, fill: 'var(--accent)' }));
      svg.appendChild(mk('text', { x: x + bw / 2, y: y(r.pot[m]) - 6, 'text-anchor': 'middle', 'font-size': 11, fill: 'var(--tertiary)' }, GB.usd(r.pot[m])));
      if (r.proj[m] > 0) { const ty = y(r.proj[m]) + 15; const inside = H - pb - y(r.proj[m]) > 20;
        svg.appendChild(mk('text', { x: x + bw / 2, y: inside ? ty : y(r.proj[m]) - 4, 'text-anchor': 'middle', 'font-size': 11, 'font-weight': 700, fill: inside ? '#FFFFFF' : 'var(--accent)' }, GB.usd(r.proj[m]))); }
      svg.appendChild(mk('text', { x: x + bw / 2, y: H - 7, 'text-anchor': 'middle', 'font-size': 11, fill: 'var(--tertiary)' }, ML6[m]));
    }
    host.replaceChildren(svg);
  }
  Object.values(A).forEach((id) => document.getElementById(id).addEventListener('input', drawA));
  document.querySelectorAll('#calcA [data-scen]').forEach((b) => b.addEventListener('click', () => { const keep = readA(); const s = b.dataset.scen === 'cons' ? GB.CONS : GB.DEF; setA({ ...keep, busy: s.busy, off: s.off, ceil: s.ceil }); drawA(); }));
  drawA();
  // Client numbers calculator
  const B = { emp: 'b_emp', field: 'b_field', busy: 'b_busy', off: 'b_off', reb: 'b_reb', eats: 'b_eats' };
  const fmtB = { emp: (v) => num(v), field: (v) => v + '%', busy: (v) => v, off: (v) => v, reb: (v) => v + '%', eats: (v) => v };
  function drawB() {
    const p = {}; Object.entries(B).forEach(([k, id]) => { p[k] = Number(document.getElementById(id).value); });
    Object.entries(fmtB).forEach(([k, f]) => { document.querySelectorAll(`[data-o=${B[k]}]`).forEach((e) => { e.textContent = f(p[k]); }); });
    const field = p.emp * p.field / 100, other = p.emp - field;
    [[p.busy, p.eats * field, 0], [p.off, p.emp * 0.1, 1]].forEach(([rides, meals, i]) => {
      const trips = field * rides + other * 0.5; const reb = field * rides * p.reb / 100; const bud = trips * 10 + meals * 15; const rec = reb * 10;
      document.querySelectorAll(`[data-kb=trips${i}]`).forEach((e) => { e.textContent = num(Math.round(trips)); });
      document.querySelectorAll(`[data-kb=reb${i}]`).forEach((e) => { e.textContent = num(Math.round(reb)); });
      document.querySelectorAll(`[data-kb=bud${i}]`).forEach((e) => { e.textContent = GB.usd(bud); });
      document.querySelectorAll(`[data-kb=rec${i}]`).forEach((e) => { e.textContent = GB.usd(rec); });
    });
  }
  Object.values(B).forEach((id) => document.getElementById(id).addEventListener('input', drawB));
  drawB();
  // Internal brief uses fixed defaults
  const d = GB.calc(GB.DEF); const brief = document.getElementById('internal-brief');
  brief.querySelectorAll('[data-k=annual]').forEach((e) => { e.textContent = GB.usd(d.annual); });
  brief.querySelectorAll('[data-k=h1pot]').forEach((e) => { e.textContent = GB.usd(d.h1pot); });
  brief.querySelectorAll('[data-k=h1]').forEach((e) => { e.textContent = GB.usd(d.h1); });
  brief.querySelectorAll('[data-k=quota]').forEach((e) => { e.textContent = GB.pct(d.quota); });
  const plus = GB.calc({ ...GB.DEF, busy: GB.DEF.busy + 1 }).h1 - d.h1; const slip = d.h1 - GB.calc({ ...GB.DEF, go: 1 }).h1;
  brief.querySelectorAll('[data-k=sens]').forEach((e) => { e.textContent = GB.usd(plus); });
  brief.querySelectorAll('[data-k=slip]').forEach((e) => { e.textContent = GB.usd(slip); });
})();

// Salles Sainz review calculator (earlier version)
(() => {
  const scope = document.getElementById('salles-review'); if (!scope) return;
  const NS = 'http://www.w3.org/2000/svg';
  const mk = (tag, attrs, text) => { const e = document.createElementNS(NS, tag); Object.entries(attrs).forEach(([k, v]) => e.setAttribute(k, v)); if (text !== undefined) e.textContent = text; return e; };
  const C = { emp: 'c_emp', field: 'c_field', busy: 'c_busy', off: 'c_off', eats: 'c_eats', part: 'c_part', go: 'c_go' };
  const fmt = { emp: (v) => num(v), field: (v) => v + '%', busy: (v) => v, off: (v) => v, eats: (v) => v, part: (v) => v + '%' };
  function draw() {
    const p = { ceil: 70 }; Object.entries(C).forEach(([k, id]) => { p[k] = Number(document.getElementById(id).value); });
    Object.entries(fmt).forEach(([k, f]) => { scope.querySelectorAll(`[data-o=${C[k]}]`).forEach((e) => { e.textContent = f(p[k]); }); });
    const r = GB.calc(p);
    scope.querySelectorAll('[data-k=annual]').forEach((e) => { e.textContent = GB.usd(r.annual); });
    scope.querySelectorAll('[data-k=h1pot]').forEach((e) => { e.textContent = GB.usd(r.h1pot); });
    scope.querySelectorAll('[data-k=h1]').forEach((e) => { e.textContent = GB.usd(r.h1); });
    scope.querySelectorAll('[data-k=quota]').forEach((e) => { e.textContent = GB.pct(r.quota); });
    const host = document.getElementById('chartC'); const W = 560, H = 190, pl = 4, pt = 20, pb = 24; const ML6 = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'];
    const max = Math.max(...r.pot.slice(0, 6)) * 1.12; const bw = (W - pl * 2) / 6; const y = (v) => pt + (H - pt - pb) * (1 - v / max);
    const svg = mk('svg', { viewBox: `0 0 ${W} ${H}`, role: 'img', 'aria-label': `Projected GB by month, H1 2027 total ${GB.usd(r.h1)}` });
    for (let m = 0; m < 6; m++) {
      const x = pl + m * bw;
      svg.appendChild(mk('rect', { x: x + bw * 0.12, y: y(r.pot[m]), width: bw * 0.76, height: H - pb - y(r.pot[m]), rx: 2, fill: 'var(--b-mid)' }));
      if (r.proj[m] > 0) svg.appendChild(mk('rect', { x: x + bw * 0.12, y: y(r.proj[m]), width: bw * 0.76, height: H - pb - y(r.proj[m]), rx: 2, fill: 'var(--accent)' }));
      svg.appendChild(mk('text', { x: x + bw / 2, y: y(r.pot[m]) - 6, 'text-anchor': 'middle', 'font-size': 11, fill: 'var(--tertiary)' }, GB.usd(r.pot[m])));
      if (r.proj[m] > 0) svg.appendChild(mk('text', { x: x + bw / 2, y: Math.min(y(r.proj[m]) + 15, H - pb - 4), 'text-anchor': 'middle', 'font-size': 11, 'font-weight': 700, fill: '#FFFFFF' }, GB.usd(r.proj[m])));
      svg.appendChild(mk('text', { x: x + bw / 2, y: H - 7, 'text-anchor': 'middle', 'font-size': 11, fill: 'var(--tertiary)' }, ML6[m]));
    }
    host.replaceChildren(svg);
  }
  Object.values(C).forEach((id) => document.getElementById(id).addEventListener('input', draw));
  draw();
})();
