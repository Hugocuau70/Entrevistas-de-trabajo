import sys, json
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION
from pptx.enum.dml import MSO_LINE_DASH_STYLE

OUT, SEAS_PATH, KW_PATH = sys.argv[1], sys.argv[2], sys.argv[3]
SSGT_LOGO, MAP_PNG = '/tmp/claude-0/-home-user-Entrevistas-de-trabajo/88e3197a-7a0a-53b4-a474-d84a37e1b8be/scratchpad/logos/ssgt.png', '/tmp/claude-0/-home-user-Entrevistas-de-trabajo/88e3197a-7a0a-53b4-a474-d84a37e1b8be/scratchpad/logos/mexico_offices.png'
LOGO_W, LOGO_B = '/tmp/claude-0/-home-user-Entrevistas-de-trabajo/88e3197a-7a0a-53b4-a474-d84a37e1b8be/scratchpad/logos/logo_white.png', '/tmp/claude-0/-home-user-Entrevistas-de-trabajo/88e3197a-7a0a-53b4-a474-d84a37e1b8be/scratchpad/logos/logo_black.png'
BLACK, WHITE = RGBColor(0,0,0), RGBColor(255,255,255)
G2, G3, SURF, LINE, ACC = RGBColor(0x54,0x54,0x54), RGBColor(0x75,0x75,0x75), RGBColor(0xF6,0xF6,0xF6), RGBColor(0xE2,0xE2,0xE2), RGBColor(0x27,0x6E,0xF1)
MID, LOWC = RGBColor(0xEE,0xEE,0xEE), RGBColor(0xFF,0xD9,0xB0)
FONT = 'Inter'
prs = Presentation(); prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BL = prs.slide_layouts[6]
W, H = 13.333, 7.5; ML = 0.7; CW = W - 2 * ML
state = {'n': 0}
TOTAL = 7

def tb(s, x, y, w, h, text='', size=14, bold=False, color=BLACK, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, caps=False, spacing=None):
    box = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)); tf = box.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0; tf.vertical_anchor = anchor
    lines = text if isinstance(text, list) else [text]
    for i, ln in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph(); p.alignment = align
        if spacing: p.space_after = Pt(spacing)
        runs = ln if isinstance(ln, list) else [(ln, bold)]
        for t, b in runs:
            r = p.add_run(); r.text = t.upper() if caps else t; f = r.font; f.name = FONT; f.size = Pt(size); f.bold = b; f.color.rgb = color
    return box

def rect(s, x, y, w, h, fill=SURF, line=None, shape=MSO_SHAPE.RECTANGLE):
    r = s.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h)); r.fill.solid(); r.fill.fore_color.rgb = fill
    if line is None: r.line.fill.background()
    else: r.line.color.rgb = line; r.line.width = Pt(1)
    r.shadow.inherit = False
    if shape == MSO_SHAPE.ROUNDED_RECTANGLE: r.adjustments[0] = 0.06
    return r

def new(title=None, eyebrow=None, inv=False, foot=None, notes=None, logo=True):
    state['n'] += 1; s = prs.slides.add_slide(BL)
    bg = s.background.fill; bg.solid(); bg.fore_color.rgb = BLACK if inv else WHITE
    if logo:
        pic = s.shapes.add_picture(LOGO_W if inv else LOGO_B, 0, 0, height=Inches(0.42))
        pic.left = Inches(W - ML) - pic.width; pic.top = Inches(0.42)
    fg = WHITE if inv else BLACK; sub = RGBColor(0xB0,0xB0,0xB0) if inv else G3
    if eyebrow: tb(s, ML, 0.55, CW, 0.3, eyebrow, 11, True, sub, caps=True)
    if title: tb(s, ML, 0.85, CW, 1.0, title, 30, True, fg)
    ln = s.shapes.add_connector(1, Inches(ML), Inches(6.85), Inches(W - ML), Inches(6.85)); ln.line.color.rgb = RGBColor(0x33,0x33,0x33) if inv else LINE; ln.line.width = Pt(0.75)
    tb(s, ML, 6.95, CW - 1.2, 0.3, foot or 'Uber for Business · Salles Sainz Grant Thornton', 10, False, sub)
    tb(s, W - ML - 1.2, 6.95, 1.2, 0.3, f'{state["n"]} / {TOTAL}', 10, False, sub, PP_ALIGN.RIGHT)
    if notes: s.notes_slide.notes_text_frame.text = notes
    return s

def bullets(s, x, y, w, h, items, size=15):
    lines = [[('•  ', False), (b, True), (rest, False)] for b, rest in items]
    return tb(s, x, y, w, h, lines, size, spacing=9)

def card(s, x, y, w, h, k=None, big=None, body=None, prod=None, accent=False, bigsize=34, bodysize=13):
    rect(s, x, y, w, h, ACC if accent else SURF, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    fg = WHITE if accent else BLACK; kc = RGBColor(0xDD,0xE7,0xFD) if accent else G3; cy = y + 0.18
    if k: tb(s, x + 0.2, cy, w - 0.4, 0.3, k, 10, True, kc, caps=True); cy += 0.32
    if big: tb(s, x + 0.2, cy, w - 0.4, 0.7, big, bigsize, True, fg); cy += bigsize / 72 * 1.25 + 0.05
    if body: tb(s, x + 0.2, cy, w - 0.4, h - (cy - y) - 0.15, body, bodysize, False, fg)
    if prod: tb(s, x + 0.2, y + h - 0.45, w - 0.4, 0.35, prod, 11, True, WHITE if accent else ACC)

def grid(s, y, h, cards, cols, gap=0.22, **kw):
    w = (CW - gap * (cols - 1)) / cols
    for i, c in enumerate(cards):
        r, ci = divmod(i, cols); card(s, ML + ci * (w + gap), y + r * (h + gap), w, h, **{**kw, **c})

from pptx.oxml.ns import qn
from lxml import etree
def borders(cell, header):
    tcPr = cell._tc.get_or_add_tcPr()
    for tag in ('a:lnL', 'a:lnR', 'a:lnT', 'a:lnB'):
        for old in tcPr.findall(qn(tag)): tcPr.remove(old)
    for tag in ('a:lnL', 'a:lnR', 'a:lnT', 'a:lnB'):
        visible = tag == 'a:lnB'
        ln = etree.SubElement(tcPr, qn(tag), w=str(19050 if (visible and header) else 9525 if visible else 0))
        if visible:
            sf = etree.SubElement(ln, qn('a:solidFill')); etree.SubElement(sf, qn('a:srgbClr'), val='000000' if header else 'E2E2E2')
        else:
            etree.SubElement(ln, qn('a:noFill'))
def table(s, y, header, rows, widths, size=12, h=None, x=None, w=None):
    x = ML if x is None else x; tw = CW if w is None else w
    nr = len(rows) + 1; th = h or 0.42 * nr
    gt = s.shapes.add_table(nr, len(header), Inches(x), Inches(y), Inches(tw), Inches(th)).table
    tot = sum(widths)
    for i, wv in enumerate(widths): gt.columns[i].width = Emu(int(Inches(tw) * wv / tot))
    for r in range(nr):
        for c in range(len(header)):
            cell = gt.cell(r, c); cell.fill.solid(); cell.fill.fore_color.rgb = WHITE
            cell.margin_left = cell.margin_right = Inches(0.08); cell.margin_top = cell.margin_bottom = Inches(0.05)
            txt = header[c] if r == 0 else rows[r - 1][c]
            tf = cell.text_frame; tf.word_wrap = True; p = tf.paragraphs[0]; p.text = ''
            run = p.add_run(); run.text = txt.upper() if r == 0 else txt; f = run.font; f.name = FONT
            f.size = Pt(9.5 if r == 0 else size); f.bold = (r == 0) or (c == 0); f.color.rgb = G3 if r == 0 else BLACK
            borders(cell, r == 0)
    tbl = gt._tbl; tblPr = tbl.tblPr; tblPr.set('firstRow', '0'); tblPr.set('bandRow', '0')
    # remove style id so plain table
    for el in tblPr.findall('{http://schemas.openxmlformats.org/drawingml/2006/main}tableStyleId'): tblPr.remove(el)
    return gt

def bar_chart(s, x, y, w, h, cats, vals, hl, fmt='0', title=None, series2=None):
    cd = CategoryChartData(); cd.categories = cats
    if series2: cd.add_series('Potential', series2); cd.add_series('Projected', vals)
    else: cd.add_series('Value', vals)
    gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(x), Inches(y), Inches(w), Inches(h), cd); ch = gf.chart
    ch.has_title = False; ch.has_legend = bool(series2); ch.font.name = FONT; ch.font.size = Pt(10); ch.font.color.rgb = G3
    if series2:
        from pptx.enum.chart import XL_LEGEND_POSITION
        ch.legend.position = XL_LEGEND_POSITION.TOP; ch.legend.include_in_layout = False
    va = ch.value_axis; va.visible = False; va.has_major_gridlines = False
    ca = ch.category_axis; ca.format.line.color.rgb = LINE; ca.tick_labels.font.size = Pt(10)
    plot = ch.plots[0]; plot.gap_width = 40; plot.overlap = 100 if series2 else 0
    plot.has_data_labels = True; dl = plot.data_labels; dl.number_format = fmt; dl.number_format_is_linked = False; dl.font.size = Pt(9); dl.position = XL_LABEL_POSITION.OUTSIDE_END
    for si, ser in enumerate(plot.series):
        ser.format.fill.solid(); ser.format.fill.fore_color.rgb = MID if (series2 and si == 0) else (ACC if series2 else MID)
        if not series2:
            for i in range(len(vals)):
                pt = ser.points[i]; pt.format.fill.solid(); pt.format.fill.fore_color.rgb = ACC if i in hl else MID
    if title: tb(s, x, y - 0.3, w, 0.3, title, 10, False, G3)
    return ch

seas = {r['row_id']: r for r in json.load(open(SEAS_PATH))['rows']}
kw = json.load(open(KW_PATH))
F1, FB, F2 = 'Section 1 · Company profile and strategy', 'Section 1 · Role play · Salles Sainz Grant Thornton', 'Section 2 · Mutual success plan'



GREY = RGBColor(0xB0,0xB0,0xB0); F3 = 'Section 3 · Book of Business'
# 1 Cover
s = new(inv=True, foot='Diego Cuauhtémoc · Mid-Market Account Executive', logo=False, notes='Sección 3 (15 min). Mensaje: priorizo por detonador, no por tamaño; el timing de cierre define el H1.')
s.shapes.add_picture(LOGO_W, Inches(ML), Inches(0.6), height=Inches(0.85))
tb(s, ML, 2.05, 8, 0.3, 'Section 3', 11, True, GREY, caps=True)
tb(s, ML, 2.45, 11, 1.8, 'Book of Business: 150 accounts to USD 350K in H1 2027', 42, True, WHITE)
tb(s, ML, 4.45, 10, 0.6, 'Prioritization, products, forecast and what can move the number.', 16, False, GREY)
# 2 Prioritization
s = new('Prioritize by trigger, not by size: three tiers from the Industry radar', 'Section 3 · Prioritization', foot='Sources: Industry radar (INEGI, Economic Census 2024, Google Keyword Planner) · ' + F3,
        notes='Tiers del opportunity scorer. La distribución de las 150 cuentas por industria es un supuesto; se reemplaza con el book real en Salesforce.')
table(s, 2.0, ['Tier', 'Industries', 'Accounts', 'Why now', 'Motion'], [
  ['Tier 1', 'Audit and tax, engineering, pharma, consulting, data centers, construction', '40', 'Busy seasons and projects that start in Q1', 'AE-led with BDR support; work all 40 by January'],
  ['Tier 2', 'Food, electronics, advertising, auto parts, warehousing, IT, legal', '60', 'Steady travel; auto parts and warehousing slowed by the T-MEC review', 'BDR sequences; AE joins from the first meeting'],
  ['Tier 3', 'Telecom, hospitals, labs, staffing, security, trucking', '50', 'Low ride intensity or enterprise-size players', 'Automated nurture with intent signals; builds H2 pipeline']], [0.7, 2.2, 0.8, 1.9, 1.9], 13)
tb(s, ML, 4.9, CW, 0.5, 'Tiers come from the opportunity scorer (Tier 1 ≥ 55, Tier 2 40–55, Tier 3 < 40). The split of the 150 accounts by industry is an assumption to replace with the real book in Salesforce.', 11, False, G3)
# 3 Timing
s = new('In H1, when a deal closes matters more than how big it is', 'Section 3 · Business model', foot='Go-live the month after close; adoption curve from the account model · ' + F3,
        notes='GB se reconoce cuando la gente viaja. Un cierre en diciembre captura 3.0 meses de potencial en H1; uno en mayo, 0.2: 15 veces menos.')
bar_chart(s, ML, 2.3, 7.4, 3.9, ['Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'], [3.0, 2.3, 1.65, 1.05, 0.55, 0.2, 0.0], [0, 1, 2], '0.0#', 'Months of GB captured in H1 per USD 1 of monthly potential, by close month')
card(s, 8.5, 2.0, W - ML - 8.5, 1.3, 'Why', None, 'GB is recognized when people ride, not at signature. Adoption ramps from 20% to 70% by month 6.', bodysize=13)
card(s, 8.5, 3.45, W - ML - 8.5, 1.55, 'So', '15x', 'A December close is worth 15 times a May close inside H1.', accent=True, bigsize=30, bodysize=13)
card(s, 8.5, 5.15, W - ML - 8.5, 1.1, 'Rule', None, 'More than 90% of H1 GB has to come from deals closed by February.', bodysize=13)
# 4 Pipeline
s = new('A USD 16M portfolio; 51 opportunities and 12 wins reach the quota', 'Section 3 · Portfolio and pipeline', foot=F3,
        notes='Potencial del portafolio USD 16.3M/año. Crear 51 oportunidades (USD 7.7M de potencial anual); cerrar 12 (USD 2.0M) a 23%, en línea con la mediana de mercado (24%); en H1 se reconocen USD 354K por la rampa. La palanca es generar pipeline: reunirse con 85% de Tier 1. SSGT es uno de los cierres de diciembre, contado al promedio de Tier 1; su valor extra es upside.')
kp = [('USD 16.3M', 'Portfolio potential a year (all 150 at full adoption)'), ('USD 7.7M', 'Pipeline to create: 51 opportunities'), ('USD 2.0M', 'Pipeline to close: 12 deals at 23%'), ('USD 354K', 'GB recognized in H1 · 101% of quota')]
for i, (v, l) in enumerate(kp):
    x = ML + i * 3.0; rect(s, x, 2.0, 0.06, 0.95, ACC if i == 3 else LINE)
    tb(s, x + 0.2, 1.95, 2.8, 0.55, v, 24, True, BLACK); tb(s, x + 0.2, 2.5, 2.7, 0.5, l, 10, False, G3)
table(s, 3.25, ['Tier', 'Accounts', 'Meetings', 'Opportunities', 'Win rate', 'Wins', 'Closes', 'H1 GB'], [
  ['Tier 1', '40', '34', '25.5', '28%', '7.1', 'Dec–Feb', 'USD 324K'], ['Tier 2', '60', '30', '18.0', '20%', '3.6', 'Feb–Apr', 'USD 29K'],
  ['Tier 3', '50', '15', '7.5', '12%', '0.9', 'Apr–May', 'USD 1K'], ['Total', '150', '79', '51.0', '23%', '11.6', '', 'USD 354K']], [1, 1, 1, 1.2, 1, 0.8, 1.1, 1.1], 13)
tb(s, ML, 5.6, CW, 0.9, 'Annual potential per account = employees × GB per employee a year at full adoption (Tier 1: 950 × USD 240, calibrated on Salles Sainz Grant Thornton; Tier 2: 700 × USD 130; Tier 3: 500 × USD 70). Salles Sainz is one of the Tier 1 December wins, counted at the Tier 1 average; its extra value is upside. Win rates set against B2B benchmarks: mid-market median 24% (interquartile 20–28%); Tier 1 at 28% for warm, trigger-based deals. Adoption of 70% by month 6 matches the ground-transport policy-compliance average (67%); top performers reach 85%.', 9.5, False, G3)
# 5 Forecast
s = new('The forecast: front-load Tier 1, exit June with a strong run-rate', 'Section 3 · Forecast', foot='Cumulative GB recognized vs. quota, Jan–Jun 2027 · ' + F3,
        notes='Acumulado: ene 11K, feb 38K, mar 89K, abr 161K, may 251K, jun 354K. Run-rate de junio USD 103K/mes: base para H2. Si los cierres se retrasan un mes, H1 cae a ~USD 251K. Versión interactiva en el Radar.')
ch = bar_chart(s, ML, 2.35, 8.2, 4.0, ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'], [11, 38, 89, 161, 251, 354], [5], '"USD "0"K"', 'Cumulative GB recognized in H1 2027 (USD thousands) · quota USD 350K')
ln = s.shapes.add_connector(1, Inches(ML), Inches(2.6), Inches(ML + 8.2), Inches(2.6)); ln.line.color.rgb = BLACK; ln.line.dash_style = MSO_LINE_DASH_STYLE.DASH; ln.line.width = Pt(1.25)
tb(s, ML + 0.1, 2.32, 3, 0.25, 'Quota USD 350K', 10, True)
for i, (v, l) in enumerate([('USD 354K', 'H1 GB · 101% of quota'), ('12 wins', 'from 51 opportunities'), ('USD 103K', 'June monthly run-rate, the base for H2')]):
    y = 2.0 + i * 1.45; rect(s, 9.3, y, 0.06, 1.1, ACC if i == 0 else LINE)
    tb(s, 9.5, y, 3.2, 0.6, v, 26, True); tb(s, 9.5, y + 0.6, 3.2, 0.5, l, 11, False, G3)
# 6 Products
s = new('Lead with Uber Travel, open doors with Vouchers, scale with Central', 'Section 3 · Products', foot=F3)
grid(s, 2.0, 2.7, [dict(k='Core · all tiers', body='Uber Travel\n\nRecurring rides are where GB compounds month after month. Expense codes and Ride Policies make it a CFO decision.', prod='Most of the GB', accent=True),
  dict(k='Door opener · Tier 3 and adoption', body='Vouchers (Eats and rides)\n\nLow-friction first deal for events, overtime and closing nights; the fastest way to get profiles linked.', prod='Fast to sign, fast to use'),
  dict(k='Scale · Tier 1 and 2', body='Uber Central\n\nAssistants and front desks book for guests, candidates and staff without the app.', prod='Expands use beyond app users')], 3, bodysize=13)
card(s, ML, 5.0, CW, 1.0, 'Land and expand', None, 'Land with Travel for the busiest team, expand with Vouchers and Central once the first invoice proves the control story.', bodysize=15)
# 7 Factors
s = new('What can move the number, and what I do about it', 'Section 3 · Risks and tailwinds', foot=F3)
table(s, 2.0, ['Factor', 'Type', 'Effect on H1', 'Response'], [
  ['Client ramp-up (6 months to 70%)', 'Internal', 'A one-month slip costs about USD 100K', 'Close Tier 1 by February; adoption plan from day one'],
  ['Busy seasons and Querétaro data centers', 'External +', 'Q1 triggers for Tier 1', 'Sprint audit and pharma from November'],
  ['T-MEC review', 'External −', 'Auto parts and warehousing delay spend', 'Kept in Tier 2; pitch cost control, not growth'],
  ['Calendar: slow January, Easter week Mar 21–28, elections Jun 6', 'External −', 'Fewer decision days', 'Signatures in December; go-lives before mid-March'],
  ['Fares up to 7% after the 2026 platform reform', 'External ±', 'More GB per trip; price objections', 'Lead with control and recovery, not price'],
  ['My ramp, BDR capacity, Legal and CFDI setup', 'Internal', 'About 80 meetings in H1, 3 a week', 'Automate Tier 3; standard invoicing playbook with Tax']], [2.0, 0.9, 1.6, 2.0], 12)
assert state['n'] == TOTAL, state['n']
prs.save(OUT); print('saved', OUT)
