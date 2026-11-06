// Generador del deck: Hootsuite x GBM — Value Presentation (Enterprise AE)
// Uso: NODE_PATH=<node_modules con pptxgenjs, react-icons, react, react-dom, sharp> node build_deck.js
// Opcional: APPLY_THEME=<ruta a apply_theme.js del skill pptx> para escribir la paleta en el tema.

const path = require("path");
const pptxgen = require("pptxgenjs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const fa = require("react-icons/fa");

const OUT = path.join(__dirname, "Hootsuite_x_GBM_Value_Presentation_Diego_Cuauhtemoc.pptx");
const PHOTO = path.join(__dirname, "assets", "diego.jpg");

// ---------- Theme ----------
const THEME = {
  name: "Hootsuite x GBM",
  headFontFace: "Arial",
  bodyFontFace: "Calibri",
  colors: {
    dk1: "1B2333", // body text
    lt1: "FFFFFF",
    dk2: "143059", // Hootsuite-style night navy (dominant)
    lt2: "F2F4F8", // light tint for cards
    accent1: "FFC72C", // saffron (accent, used sparingly)
    accent2: "2E6BE6", // signal blue
    accent3: "1FA67A", // positive green
    accent4: "E5484D", // alert red
    accent5: "5B6475", // muted text
    accent6: "DCE3EE", // hairlines
    hlink: "2E6BE6",
    folHlink: "5B6475",
  },
};
const HEX = THEME.colors;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.title = "Hootsuite x GBM — Value Presentation";
pres.author = "Diego Cuauhtémoc Guerrero";
pres.subject = "Enterprise Account Executive interview — role play";
const C = pres.SchemeColor;

const W = 13.333, H = 7.5, MX = 0.6;

// ---------- Icons ----------
async function icon(Comp, color = "#FFFFFF", size = 256) {
  const svg = ReactDOMServer.renderToStaticMarkup(React.createElement(Comp, { color, size: String(size) }));
  const buf = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

async function circularPhoto(file, px = 600) {
  const mask = Buffer.from(`<svg width="${px}" height="${px}"><circle cx="${px / 2}" cy="${px / 2}" r="${px / 2}" fill="#fff"/></svg>`);
  const buf = await sharp(file).resize(px, px).composite([{ input: mask, blend: "dest-in" }]).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

// ---------- Layouts ----------
const FOOTER = "Hootsuite × GBM  |  Diego Cuauhtémoc Guerrero";

pres.defineSlideMaster({
  title: "COVER_DARK",
  background: { color: C.text2 },
  objects: [
    { placeholder: { options: { name: "kicker", type: "body", x: MX, y: 1.25, w: 7.6, h: 0.4, fontFace: THEME.bodyFontFace, fontSize: 13, bold: true, color: C.accent1, charSpacing: 2, margin: 0 }, text: "" } },
    { placeholder: { options: { name: "title", type: "title", x: MX, y: 1.8, w: 7.8, h: 2.3, fontFace: THEME.headFontFace, fontSize: 40, bold: true, color: C.background1, valign: "top", align: "left", margin: 0 }, text: "" } },
    { placeholder: { options: { name: "body", type: "body", x: MX, y: 4.25, w: 7.4, h: 1.0, fontFace: THEME.bodyFontFace, fontSize: 18, color: C.accent6, valign: "top", margin: 0 }, text: "" } },
  ],
});

pres.defineSlideMaster({
  title: "CONTENT",
  background: { color: C.background1 },
  margin: [0.5, 0.6, 0.6, 0.6],
  slideNumber: { x: W - 0.9, y: H - 0.45, w: 0.4, h: 0.3, fontFace: THEME.bodyFontFace, fontSize: 10, color: C.accent5, align: "right" },
  objects: [
    { text: { text: FOOTER, options: { x: MX, y: H - 0.45, w: 6, h: 0.3, fontFace: THEME.bodyFontFace, fontSize: 10, color: C.accent5, margin: 0 } } },
    { placeholder: { options: { name: "kicker", type: "body", x: MX, y: 0.42, w: 9, h: 0.3, fontFace: THEME.bodyFontFace, fontSize: 12, bold: true, color: C.accent2, charSpacing: 2, margin: 0 }, text: "" } },
    { placeholder: { options: { name: "title", type: "title", x: MX, y: 0.72, w: W - 2 * MX, h: 0.9, fontFace: THEME.headFontFace, fontSize: 30, bold: true, color: C.text2, valign: "top", align: "left", margin: 0 }, text: "" } },
  ],
});

// ---------- Helpers ----------
function rings(slide, cx, cy, rMax, n, color, startTransp = 55) {
  // Concentric "listening" rings — the deck's visual motif
  for (let i = 0; i < n; i++) {
    const r = rMax * (1 - i / n);
    slide.addShape(pres.shapes.OVAL, {
      objectName: `ring_${i}`,
      x: cx - r, y: cy - r, w: 2 * r, h: 2 * r,
      fill: { type: "none" },
      line: { color, width: 1.5, transparency: Math.min(90, startTransp + (n - i) * 6) },
    });
  }
}

function iconCircle(slide, data, x, y, d, fillColor, name) {
  slide.addShape(pres.shapes.OVAL, { objectName: `${name}_circle`, x, y, w: d, h: d, fill: { color: fillColor }, line: { type: "none" } });
  const pad = d * 0.27;
  slide.addImage({ objectName: `${name}_icon`, data, x: x + pad, y: y + pad, w: d - 2 * pad, h: d - 2 * pad });
}

function card(slide, x, y, w, h, name, fill = C.background2) {
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    objectName: name, x, y, w, h, rectRadius: 0.12, fill: { color: fill }, line: { type: "none" },
  });
}

function txt(slide, text, opts) {
  slide.addText(text, { isTextBox: true, margin: 0, valign: "top", fontFace: THEME.bodyFontFace, color: C.text1, ...opts });
}

(async () => {
  const I = {
    shield: await icon(fa.FaShieldAlt),
    chat: await icon(fa.FaComments),
    users: await icon(fa.FaUsers),
    radar: await icon(fa.FaSatelliteDish),
    bolt: await icon(fa.FaBolt, "#143059"),
    chart: await icon(fa.FaChartLine),
    check: await icon(fa.FaCheck),
    search: await icon(fa.FaSearch),
    flag: await icon(fa.FaFlagCheckered, "#143059"),
    brief: await icon(fa.FaBriefcase),
    store: await icon(fa.FaStore),
    rocket: await icon(fa.FaRocket),
    checkGreen: await icon(fa.FaCheckCircle, "#1FA67A"),
  };
  const photo = await circularPhoto(PHOTO);

  // ====================== COVER ======================
  pres.addSection({ title: "Cover" });
  let s = pres.addSlide({ masterName: "COVER_DARK", sectionTitle: "Cover" });
  rings(s, 10.9, 3.75, 3.4, 6, HEX.accent1, 30);
  s.addShape(pres.shapes.OVAL, { objectName: "core", x: 10.9 - 0.75, y: 3.75 - 0.75, w: 1.5, h: 1.5, fill: { color: C.accent1 }, line: { type: "none" } });
  s.addImage({ objectName: "core_icon", data: await icon(fa.FaChartLine, "#143059"), x: 10.9 - 0.42, y: 3.75 - 0.42, w: 0.84, h: 0.84 });
  s.addText("ENTERPRISE AE  ·  VALUE PRESENTATION", { placeholder: "kicker" });
  s.addText("From 22 million accounts to a country of active investors", { placeholder: "title" });
  s.addText("How Hootsuite Social OS helps GBM protect trust, activate investors and scale its advisors", { placeholder: "body" });
  txt(s, [
    { text: "Prepared for GBM’s Director of Social Media", options: { bold: true, breakLine: true } },
    { text: "Presented by Diego Cuauhtémoc Guerrero  ·  November 2026" },
  ], { x: MX, y: 6.05, w: 7.5, h: 0.7, fontSize: 14, color: C.background1 });
  s.addNotes(
    "[0:00–0:30] Thank you all for the time today. For this role play I chose GBM, Grupo Bursátil Mexicano — Mexico's largest brokerage by number of accounts. " +
    "I chose it for a reason I'll explain in a second: I've actually worked with GBM from the agency side. " +
    "Context for the role play: last week I ran discovery with GBM's Director of Social Media. Today I'm coming back to show how Hootsuite connects to the business goals she shared — not a feature tour."
  );

  // ====================== 1. WHO I AM ======================
  pres.addSection({ title: "Who I am" });
  s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Who I am" });
  s.addText("WHO I AM", { placeholder: "kicker" });
  s.addText("Hi, I’m Diego — I’ve sat on GBM’s side of the table", { placeholder: "title" });

  // Left: photo + identity
  card(s, MX, 1.85, 3.55, 4.9, "id_card", C.text2);
  s.addImage({ objectName: "photo", data: photo, x: MX + 0.73, y: 2.15, w: 2.1, h: 2.1, altText: "Diego Cuauhtémoc Guerrero" });
  txt(s, "Diego Cuauhtémoc Guerrero", { x: MX + 0.25, y: 4.4, w: 3.05, h: 0.75, fontSize: 18, bold: true, color: C.background1, align: "center", fontFace: THEME.headFontFace });
  txt(s, "Consultative seller · Growth & performance leader", { x: MX + 0.25, y: 5.25, w: 3.05, h: 0.6, fontSize: 14, color: C.accent6, align: "center" });
  txt(s, "Mexico City  ·  Spanish / English", { x: MX + 0.25, y: 6.0, w: 3.05, h: 0.35, fontSize: 13, color: C.accent1, align: "center", bold: true });

  // Right: three roles
  const roles = [
    { ic: I.store, co: "Más Gallo Media  ·  Head of Industry (2022–24)", line: "Managed a USD 1M/month pipeline with enterprise accounts like GBM, Bitso and Televisa — full cycle from discovery to close" },
    { ic: I.brief, co: "Pinterest  ·  Sr. Performance Solutions Partner (2024–26)", line: "Grew investment with Liverpool, Marriott (USD 50K → 100K/month) and Coppel (4.4× daily budget) through business cases" },
    { ic: I.rocket, co: "LAPZO  ·  Head of Growth (2026)", line: "Campaigns behind 118 SQLs and MXN 1.4M in new MRR in three months — I know what pipeline pressure feels like" },
  ];
  const rx = MX + 3.95, rw = W - MX - rx;
  roles.forEach((r, i) => {
    const y = 1.85 + i * 1.32;
    card(s, rx, y, rw, 1.17, `role_${i}`);
    iconCircle(s, r.ic, rx + 0.22, y + 0.26, 0.65, C.text2, `role_${i}`);
    txt(s, r.co, { x: rx + 1.1, y: y + 0.16, w: rw - 1.3, h: 0.32, fontSize: 15, bold: true, color: C.text2 });
    txt(s, r.line, { x: rx + 1.1, y: y + 0.5, w: rw - 1.3, h: 0.6, fontSize: 13, color: C.text1 });
  });
  card(s, rx, 5.85, rw, 0.9, "why_card", "FFF4D1");
  iconCircle(s, I.bolt, rx + 0.22, 5.98, 0.64, C.accent1, "why");
  txt(s, [
    { text: "Why Hootsuite: ", options: { bold: true, color: C.text2 } },
    { text: "I sell like a consultant and speak the language of marketing leaders — because I’ve been one, and I’ve been their partner." },
  ], { x: rx + 1.1, y: 6.05, w: rw - 1.3, h: 0.6, fontSize: 14, valign: "middle" });
  s.addNotes(
    "[0:30–3:00] Quick intro. I'm Diego, based in Mexico City. Three things about my background that matter for this role. " +
    "One: at Más Gallo Media I ran the full sales cycle with enterprise accounts — including GBM, Bitso and Televisa — and managed about a million dollars a month in pipeline. So I know how GBM buys, and how many stakeholders sit around the table: marketing, compliance, IT, procurement. " +
    "Two: at Pinterest I grew enterprise investment by selling business outcomes, not ad products — for example doubling Marriott's monthly investment from 50 to 100 thousand dollars with a country-specific proposal. " +
    "Three: today I lead growth at LAPZO, a B2B SaaS, where my campaigns fed 118 SQLs and 1.4 million pesos in new MRR in a quarter — so I understand SaaS metrics and pipeline discipline. " +
    "Why Hootsuite: the people I'd sell to — heads of social, CMOs — are people I've worked alongside for years. I want to bring that empathy plus a consultative process to an enterprise territory in Spanish- and Portuguese-speaking markets."
  );

  // ====================== 2. WHAT WE HEARD ======================
  pres.addSection({ title: "Value presentation" });
  s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Value presentation" });
  s.addText("WHAT WE HEARD IN DISCOVERY", { placeholder: "kicker" });
  s.addText("GBM’s ambition is clear — social is where trust is won", { placeholder: "title" });

  card(s, MX, 1.8, 5.45, 1.05, "quote_card", C.text2);
  txt(s, [
    { text: "“Queremos convertir a México en un país de inversionistas exitosos.”", options: { italic: true, bold: true, color: C.background1, breakLine: true, fontSize: 15 } },
    { text: "Pedro de Garay, Co-CEO of GBM — Pioneros 2026", options: { color: C.accent1, fontSize: 12 } },
  ], { x: MX + 0.25, y: 1.92, w: 5.0, h: 0.85, valign: "middle" });

  s.addChart(pres.charts.BAR, [{ name: "GBM", labels: ["Accounts opened", "Active clients"], values: [22.0, 0.67] }], {
    objectName: "accounts_chart",
    x: MX, y: 3.0, w: 5.45, h: 3.15, barDir: "col",
    chartColors: [HEX.dk2, HEX.accent1], invertedColors: [HEX.dk2], varyColors: true,
    showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: '0.0#"M"', dataLabelFontSize: 14, dataLabelFontBold: true, dataLabelColor: HEX.dk1, dataLabelFontFace: "+mn-lt",
    showTitle: true, title: "Millions — 2025", titleFontSize: 12, titleColor: HEX.accent5, titleFontFace: "+mn-lt",
    catAxisLabelColor: HEX.dk1, catAxisLabelFontSize: 13, catAxisLabelFontFace: "+mn-lt", valAxisHidden: true,
    valGridLine: { style: "none" }, catGridLine: { style: "none" }, showLegend: false, barGapWidthPct: 70,
  });
  txt(s, [
    { text: "≈3% of accounts are active ", options: { bold: true, color: C.text2 } },
    { text: "— activation is the growth lever" },
  ], { x: MX, y: 6.15, w: 5.45, h: 0.3, fontSize: 13 });
  txt(s, "Sources: Corporativo GBM 3T25 report; Moody’s (Oct 2025) via El CEO", { x: MX, y: 6.55, w: 5.45, h: 0.25, fontSize: 10, color: C.accent5 });

  const ch = [
    { ic: I.shield, c: C.accent4, h: "Trust is under attack", b: "Fake profiles and AI-made scam ads use trusted financial brands. Fraud claims at CONDUSEF rose ~19% (Jan–May 2026)." },
    { ic: I.chat, c: C.accent2, h: "Millions of new investors, scattered questions", b: "The Mercado Pago alliance brought first-time investors. Their questions land in DMs and comments across 5+ networks — with no single view." },
    { ic: I.users, c: C.accent3, h: "Advisors without a safe voice", b: "500+ GBM Advisors (≈1,000 next year) want to share content, but Compliance can’t review every post by hand." },
  ];
  const cx0 = MX + 5.85, cw = W - MX - cx0;
  ch.forEach((c, i) => {
    const y = 1.8 + i * 1.62;
    card(s, cx0, y, cw, 1.47, `challenge_${i}`);
    iconCircle(s, c.ic, cx0 + 0.25, y + 0.4, 0.68, c.c, `challenge_${i}`);
    txt(s, c.h, { x: cx0 + 1.15, y: y + 0.17, w: cw - 1.35, h: 0.35, fontSize: 16, bold: true, color: C.text2 });
    txt(s, c.b, { x: cx0 + 1.15, y: y + 0.55, w: cw - 1.35, h: 0.85, fontSize: 13 });
  });
  s.addNotes(
    "[3:00–7:00] Let me play back what I heard from you in discovery — tell me if I got anything wrong. " +
    "GBM's north star is in Pedro de Garay's own words: make Mexico a country of successful investors. And GBM has done the hard part of acquisition: around 22 million accounts at the end of Q3 2025, most of them through the Mercado Pago alliance. " +
    "But Moody's estimated only around 670 thousand active clients in mid-2025. That's roughly 3%. So the next chapter isn't more sign-ups — it's turning sign-ups into confident, active investors. " +
    "You shared three things standing in the way, all of which live on social. " +
    "First, trust. Fake GBM-looking profiles and AI-generated scam ads hurt people and the brand. CONDUSEF fraud claims rose about 19% in the first five months of 2026, and CONDUSEF itself warned about fake 'verified' profiles on Facebook, Instagram and TikTok. Today your team finds these manually, often after a customer complains. " +
    "Second, scale of conversation. First-time investors ask very basic questions — 'is my money safe?', 'why did my yield change?' — in DMs and comments across five or more networks. Your team juggles native tools, with no single view and no SLA. " +
    "Third, the advisor network. GBM Advisors went from about 250 to over 500 advisors, and you expect close to a thousand next year. They want content to share, but Compliance can't approve every post by hand. " +
    "Did I capture that right? Is there anything you'd add or re-prioritize? [pause — invite the panel to react]"
  );

  // ====================== 3. HOW HOOTSUITE HELPS ======================
  s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Value presentation" });
  s.addText("HOW HOOTSUITE HELPS", { placeholder: "kicker" });
  s.addText("Three business outcomes, one Social OS", { placeholder: "title" });
  const cols = [
    { ic: I.shield, c: C.accent4, k: "PROTECT TRUST", app: "Lumen by Talkwalker  +  Perch",
      pts: ["Monitor 150M+ sources in 187 languages for GBM’s name, logo and executives", "Spot impersonators, scam ads and sentiment spikes early; alert Security & Comms", "Every post passes approval workflows and automated compliance checks"],
      out: "Fewer victims, faster takedowns, audit-ready publishing" },
    { ic: I.chat, c: C.accent2, k: "ACTIVATE INVESTORS", app: "Nest  +  Lumen",
      pts: ["One inbox for every network, with routing to Care and clear SLAs", "Wisdom drafts answers from GBM’s approved knowledge", "Listening reveals what confuses new investors — and feeds content that drives a first investment"],
      out: "From a passive account to a first investment" },
    { ic: I.users, c: C.accent3, k: "SCALE ADVISORS", app: "Parliament",
      pts: ["A library of pre-approved posts advisors share on their own networks in one click", "Compliance approves once, then the content scales to 1,000 voices", "Track the reach, clicks and leads each advisor generates"],
      out: "Organic reach and leads, with zero compliance risk" },
  ];
  const gw = (W - 2 * MX - 2 * 0.3) / 3;
  cols.forEach((c, i) => {
    const x = MX + i * (gw + 0.3), y = 1.8, h = 4.35;
    card(s, x, y, gw, h, `outcome_${i}`);
    iconCircle(s, c.ic, x + 0.3, y + 0.3, 0.7, c.c, `outcome_${i}`);
    txt(s, c.k, { x: x + 1.15, y: y + 0.32, w: gw - 1.3, h: 0.32, fontSize: 15, bold: true, color: C.text2, charSpacing: 1 });
    txt(s, c.app, { x: x + 1.15, y: y + 0.66, w: gw - 1.3, h: 0.3, fontSize: 13, color: C.accent5, bold: true });
    s.addText(c.pts.map((p, j) => ({ text: p, options: { bullet: { indent: 14 }, breakLine: j < c.pts.length - 1, paraSpaceAfter: 6 } })),
      { isTextBox: true, objectName: `outcome_${i}_pts`, x: x + 0.3, y: y + 1.25, w: gw - 0.55, h: 2.2, fontSize: 13, color: C.text1, valign: "top", margin: 0, fontFace: THEME.bodyFontFace });
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { objectName: `outcome_${i}_result`, x: x + 0.2, y: y + h - 0.85, w: gw - 0.4, h: 0.65, rectRadius: 0.08, fill: { color: C.background1 }, line: { type: "none" } });
    txt(s, c.out, { x: x + 0.35, y: y + h - 0.85, w: gw - 0.7, h: 0.65, fontSize: 13, bold: true, color: C.text2, valign: "middle" });
  });
  card(s, MX, 6.3, W - 2 * MX, 0.6, "wisdom_band", C.text2);
  txt(s, [
    { text: "Wisdom", options: { bold: true, color: C.accent1 } },
    { text: " — Hootsuite’s AI agent across every app — turns social signals into the next best action for your team", options: { color: C.background1 } },
  ], { x: MX + 0.3, y: 6.3, w: W - 2 * MX - 0.6, h: 0.6, fontSize: 14, valign: "middle" });
  s.addNotes(
    "[7:00–13:00] Here's how Hootsuite maps to those three outcomes. Notice I'm organizing this by your business outcomes, not by our product menu. " +
    "PROTECT TRUST. With Lumen by Talkwalker, GBM monitors over 150 million sources in 187 languages — not just mentions of 'GBM', but your logo in images, your executives' names, and scam language like 'rendimiento garantizado'. When a fake profile or a sentiment spike appears, the right people get an alert in minutes, not after a CONDUSEF complaint. On the publishing side, Perch gives you approval workflows and automated compliance checks, so every post is reviewed and archived — your Compliance team gets control without becoming a bottleneck. " +
    "ACTIVATE INVESTORS. Nest puts every DM and comment from every network into one inbox, routes account questions to Care with SLAs, and Wisdom drafts replies based on GBM's approved answers. The bigger value is the loop: Lumen shows the top questions and fears of first-time investors — for example confusion when the Mercado Pago fund yield changes — and your content team turns that into education that moves people from an empty account to a first investment. " +
    "SCALE ADVISORS. Parliament gives GBM Advisors a library of pre-approved content they share on their own LinkedIn and networks with one click. Compliance approves once; the content scales to a thousand trusted voices. And you can see the reach, clicks and leads each advisor drives. " +
    "Tying it together is Wisdom, our AI agent launched in June, which works across all of these apps — you can literally ask it 'why did negative sentiment spike this week and what should we do?' I'll show you that live in the demo. " +
    "[Check-in question] Which of these three would make the biggest difference for your team in the next quarter?"
  );

  // ====================== 4. BUSINESS IMPACT ======================
  s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Value presentation" });
  s.addText("BUSINESS IMPACT", { placeholder: "kicker" });
  s.addText("What success could look like in 12 months", { placeholder: "title" });
  const stats = [
    { n: "+21K", l: "newly active investors", d: "If social care and insight-led content re-activate just 0.1% of ~21M dormant accounts", c: C.accent2, ic: I.chart },
    { n: "<24h", l: "from fake profile to takedown request", d: "Benchmark: with Hootsuite as its compliance hub, SIX Group closed 80 unofficial accounts — takedowns typically within 24h", c: C.accent4, ic: I.shield },
    { n: "500K+", l: "organic impressions per advisor content wave", d: "1,000 advisors × ~500 connections each, at zero media cost — and every post pre-approved", c: C.accent3, ic: I.users },
  ];
  stats.forEach((st, i) => {
    const x = MX + i * (gw + 0.3), y = 1.8;
    card(s, x, y, gw, 3.3, `stat_${i}`);
    iconCircle(s, st.ic, x + 0.3, y + 0.3, 0.55, st.c, `stat_${i}`);
    txt(s, st.n, { x: x + 0.3, y: y + 0.95, w: gw - 0.6, h: 0.95, fontSize: 54, bold: true, color: C.text2, fontFace: THEME.headFontFace });
    txt(s, st.l, { x: x + 0.3, y: y + 1.9, w: gw - 0.6, h: 0.6, fontSize: 15, bold: true, color: C.text2 });
    txt(s, st.d, { x: x + 0.3, y: y + 2.5, w: gw - 0.6, h: 0.75, fontSize: 12, color: C.accent5 });
  });
  txt(s, "KPIs we would track together in Hootsuite Analytics", { x: MX, y: 5.27, w: 8, h: 0.3, fontSize: 15, bold: true, color: C.text2 });
  const kpis = ["Share of voice vs. Nu, Bitso & Mercado Pago", "Net sentiment & trust topics", "First response time & resolution rate", "Advisor-sourced reach & leads"];
  const kw = (W - 2 * MX - 3 * 0.2) / 4;
  kpis.forEach((k, i) => {
    const x = MX + i * (kw + 0.2);
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { objectName: `kpi_${i}`, x, y: 5.68, w: kw, h: 0.72, rectRadius: 0.08, fill: { color: C.background1 }, line: { color: HEX.accent6, width: 1 } });
    s.addImage({ objectName: `kpi_${i}_check`, data: I.checkGreen, x: x + 0.18, y: 5.88, w: 0.32, h: 0.32 });
    txt(s, k, { x: x + 0.6, y: 5.68, w: kw - 0.75, h: 0.72, fontSize: 13, color: C.text1, valign: "middle" });
  });
  txt(s, "Illustrative scenarios — we will validate baselines with GBM’s own data during the pilot.", { x: MX, y: 6.55, w: 10, h: 0.3, fontSize: 11, italic: true, color: C.accent5 });
  s.addNotes(
    "[13:00–16:30] What does this mean in business terms? These are illustrative — I'd rather build the real numbers with your data — but they show the order of magnitude. " +
    "Activation: GBM has around 21 million dormant accounts. If better social care and insight-led education re-activate just one tenth of one percent, that's about 21 thousand new active investors. Plug in GBM's revenue per active client and the platform pays for itself many times over. " +
    "Trust: SIX Group, the Swiss exchange operator, used Hootsuite as its social compliance hub, closed 80 unofficial accounts and typically gets takedowns done within 24 hours. That's the standard I'd want for GBM — every hour a fake profile stays live is a potential victim and a headline. " +
    "Advisors: a thousand advisors with around 500 connections each means half a million organic impressions every time you publish a content wave — with zero media cost and every post pre-approved. " +
    "We'd track it together: share of voice versus Nu, Bitso and Mercado Pago; sentiment on trust topics; response times; and advisor-driven leads. " +
    "[Question] How does your leadership measure success for social today — and which of these metrics would resonate most with your CMO?"
  );

  // ====================== 5. PATH FORWARD ======================
  s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Value presentation" });
  s.addText("PROPOSED PATH", { placeholder: "kicker" });
  s.addText("A 90-day pilot to prove value — then scale", { placeholder: "title" });
  const phases = [
    { d: "DAYS 1–30", t: "Listen & protect", b: ["Lumen queries for brand, fraud and competitors", "Alert routing to Security & Comms", "Approval workflows in Perch with Compliance"] },
    { d: "DAYS 31–60", t: "Engage", b: ["Nest across all GBM networks", "Care routing, tags and SLAs", "Wisdom-assisted replies from approved answers"] },
    { d: "DAYS 61–90", t: "Amplify", b: ["Parliament pilot with 50 GBM Advisors", "First insight-led education campaign", "Executive business review with ROI"] },
  ];
  const pw = 2.85, py = 1.95;
  s.addShape(pres.shapes.LINE, { objectName: "timeline", x: MX + 0.35, y: py + 0.35, w: 2 * (pw + 0.2), h: 0, line: { color: HEX.accent6, width: 2 } });
  phases.forEach((p, i) => {
    const x = MX + i * (pw + 0.2);
    s.addShape(pres.shapes.OVAL, { objectName: `phase_${i}_dot`, x: x + 0.05, y: py + 0.05, w: 0.6, h: 0.6, fill: { color: C.text2 }, line: { type: "none" } });
    txt(s, String(i + 1), { x: x + 0.05, y: py + 0.05, w: 0.6, h: 0.6, fontSize: 18, bold: true, color: C.accent1, align: "center", valign: "middle", fontFace: THEME.headFontFace });
    txt(s, p.d, { x, y: py + 0.85, w: pw, h: 0.3, fontSize: 12, bold: true, color: C.accent2, charSpacing: 1 });
    txt(s, p.t, { x, y: py + 1.15, w: pw, h: 0.4, fontSize: 19, bold: true, color: C.text2, fontFace: THEME.headFontFace });
    s.addText(p.b.map((b, j) => ({ text: b, options: { bullet: { indent: 14 }, breakLine: j < p.b.length - 1, paraSpaceAfter: 6 } })),
      { isTextBox: true, objectName: `phase_${i}_pts`, x, y: py + 1.65, w: pw, h: 2.0, fontSize: 13, color: C.text1, valign: "top", margin: 0, fontFace: THEME.bodyFontFace });
  });
  // Next steps panel
  const nx = MX + 3 * (pw + 0.2) + 0.15, nw = W - MX - nx;
  card(s, nx, 1.8, nw, 4.95, "next_card", C.text2);
  iconCircle(s, I.flag, nx + 0.3, 2.05, 0.6, C.accent1, "next");
  txt(s, "Next steps", { x: nx + 1.05, y: 2.1, w: nw - 1.2, h: 0.5, fontSize: 19, bold: true, color: C.background1, fontFace: THEME.headFontFace, valign: "middle" });
  const steps = [
    ["Week 1", "Security & compliance review with your Compliance and IT teams"],
    ["Week 2", "Workshop with Customer Care and the GBM Advisors lead to set pilot KPIs"],
    ["Week 3", "Pilot proposal and mutual success plan for leadership sign-off"],
  ];
  steps.forEach((st, i) => {
    const y = 2.95 + i * 1.05;
    txt(s, st[0], { x: nx + 0.3, y, w: nw - 0.6, h: 0.3, fontSize: 13, bold: true, color: C.accent1 });
    txt(s, st[1], { x: nx + 0.3, y: y + 0.3, w: nw - 0.6, h: 0.65, fontSize: 13, color: C.background1 });
  });
  txt(s, "Does this reflect your priorities? What would make this a “yes” for your leadership?", { x: MX, y: 5.95, w: 3 * pw + 0.4, h: 0.8, fontSize: 16, italic: true, bold: true, color: C.text2, valign: "middle" });
  s.addNotes(
    "[16:30–19:30] To make this low-risk, I propose a 90-day pilot. " +
    "Days 1 to 30, listen and protect: we build the Lumen queries for brand, fraud and competitors, route alerts to Security and Communications, and set up approval workflows with Compliance — so the biggest risk is covered first. " +
    "Days 31 to 60, engage: we bring every GBM network into Nest, with care routing, tags and SLAs, and Wisdom-assisted replies. " +
    "Days 61 to 90, amplify: a Parliament pilot with 50 GBM Advisors and the first insight-led education campaign, closing with an executive business review where we show ROI against the KPIs we agreed. " +
    "For next steps, I'd suggest: next week, a security and compliance review with your Compliance and IT teams — I know from experience that's where financial-services deals slow down, so let's start there. Then a workshop with Customer Care and the GBM Advisors lead to lock the pilot KPIs. And in week three, a proposal and mutual success plan you can take to leadership. " +
    "[Close] So — does this reflect your priorities? And what would it take for this to be a 'yes' for your leadership? [stop talking, listen] " +
    "[Transition to demo] If it's helpful, let me show you what this looks like live — I'll spend ten minutes in our listening tool with GBM's real conversation."
  );

  // ====================== APPENDIX ======================
  pres.addSection({ title: "Appendix" });
  s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Appendix" });
  s.addText("APPENDIX  ·  LIVE DEMO", { placeholder: "kicker" });
  s.addText("Demo roadmap: GBM’s conversation, live in Lumen", { placeholder: "title" });
  const demo = [
    { t: "1 · Brand pulse", b: "Volume, sentiment and top themes for GBM in the last 30 days — noise like “glioblastoma (GBM)” filtered out", ic: I.radar },
    { t: "2 · Risk radar", b: "“GBM” + estafa / fraude / perfil falso / no puedo retirar — what is spiking, where, and who is amplifying it", ic: I.shield },
    { t: "3 · Competitive lens", b: "Share of voice and sentiment vs. Nu, Bitso, Mercado Pago and Hey Banco", ic: I.chart },
    { t: "4 · Ask Wisdom", b: "“Why did negative sentiment about GBM change this week, and what should my team do?”", ic: I.search },
  ];
  demo.forEach((d, i) => {
    const col = i % 2, row = Math.floor(i / 2);
    const x = MX + col * ((W - 2 * MX) / 2 + 0.15), y = 1.85 + row * 2.2;
    const w = (W - 2 * MX) / 2 - 0.15;
    card(s, x, y, w, 1.95, `demo_${i}`);
    iconCircle(s, d.ic, x + 0.3, y + 0.35, 0.7, C.text2, `demo_${i}`);
    txt(s, d.t, { x: x + 1.25, y: y + 0.35, w: w - 1.5, h: 0.4, fontSize: 18, bold: true, color: C.text2, fontFace: THEME.headFontFace });
    txt(s, d.b, { x: x + 1.25, y: y + 0.85, w: w - 1.5, h: 0.95, fontSize: 14 });
  });
  s.addNotes("Backup slide for the 10-minute demo. If the live tool fails, walk through this slide plus screenshots. See 05_demo_social_listening.md for the full script and boolean queries.");

  s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Appendix" });
  s.addText("APPENDIX  ·  SOURCES & ASSUMPTIONS", { placeholder: "kicker" });
  s.addText("Where the numbers come from", { placeholder: "title" });
  const src = [
    ["22M accounts (3T25) · MXN 1,176bn in custody", "Corporativo GBM, quarterly report 3T25 (BMV)"],
    ["~670K active clients (mid-2025)", "Moody’s report, Oct 2025, cited by El CEO"],
    ["~26.8M accounts, growth driven by Mercado Pago", "AMIB data cited by El CEO (2026)"],
    ["500+ advisors in 25 states, ≈1,000 next year", "Pioneros 2026 coverage (DPL News)"],
    ["Fraud claims +~19%, Jan–May 2026", "CONDUSEF figures cited by El Imparcial (Jun 2026)"],
    ["Social OS, Wisdom, 150M+ sources, 187 languages", "Hootsuite press release, Jun 24 2026"],
    ["SIX Group: 80 accounts closed, <24h takedowns", "Hootsuite customer story (via casestudies.com)"],
    ["+21K investors · 500K+ impressions", "Illustrative: 0.1% of ~21M dormant accounts; 1,000 advisors × ~500 connections"],
  ];
  const rows = src.map((r, i) => [
    { text: r[0], options: { bold: true, color: HEX.dk2, fill: { color: i % 2 ? "FFFFFF" : HEX.lt2 } } },
    { text: r[1], options: { color: HEX.dk1, fill: { color: i % 2 ? "FFFFFF" : HEX.lt2 } } },
  ]);
  s.addTable(rows, { objectName: "sources_table", x: MX, y: 1.85, w: W - 2 * MX, colW: [5.6, W - 2 * MX - 5.6], fontSize: 13, fontFace: THEME.bodyFontFace, rowH: 0.5, valign: "middle", border: { type: "solid", color: HEX.accent6, pt: 0.5 }, margin: [0, 0.12, 0, 0.12] });
  s.addNotes("Use only if asked where a number comes from. The discovery call itself is a role-play assumption.");

  await pres.writeFile({ fileName: OUT });
  if (process.env.APPLY_THEME) {
    const { applyTheme } = require(process.env.APPLY_THEME);
    await applyTheme(OUT, THEME);
  }
  console.log("Wrote", OUT);
})();
