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
BLACK, WHITE = RGBColor(0,0,0), RGBColor(255,255,255)
G2, G3, SURF, LINE, ACC = RGBColor(0x54,0x54,0x54), RGBColor(0x75,0x75,0x75), RGBColor(0xF6,0xF6,0xF6), RGBColor(0xE2,0xE2,0xE2), RGBColor(0x27,0x6E,0xF1)
MID, LOWC = RGBColor(0xEE,0xEE,0xEE), RGBColor(0xFF,0xD9,0xB0)
FONT = 'Inter'
prs = Presentation(); prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BL = prs.slide_layouts[6]
W, H = 13.333, 7.5; ML = 0.7; CW = W - 2 * ML
state = {'n': 0}
TOTAL = 22

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

def new(title=None, eyebrow=None, inv=False, foot=None, notes=None):
    state['n'] += 1; s = prs.slides.add_slide(BL)
    bg = s.background.fill; bg.solid(); bg.fore_color.rgb = BLACK if inv else WHITE
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
F1, FB, F2 = '1 · Account plan · Internal view', '1 · Role play · Salles Sainz Grant Thornton', '2 · Mutual success plan'

# 1 Cover
s = new(inv=True, foot='Diego Cuauhtémoc · Mid-Market Account Executive', notes='Presentación: 1) por qué esta cuenta, 2) role play con el comité de SSGT, 3) mutual success plan.')
tb(s, ML, 0.55, 8, 0.3, 'Uber for Business · Mid-Market Mexico · H1 2027', 11, True, RGBColor(0xB0,0xB0,0xB0), caps=True)
tb(s, ML, 2.3, 10.5, 1.8, 'Salles Sainz Grant Thornton: winning busy season 2027', 44, True, WHITE)
tb(s, ML, 4.3, 10, 0.8, 'Section 1 · Company profile, acquisition strategy and role play   ·   Section 2 · Mutual success plan', 16, False, RGBColor(0xB0,0xB0,0xB0))
lg = rect(s, W - ML - 2.6, 0.45, 2.6, 0.8, BLACK, line=RGBColor(0x75,0x75,0x75)); lg.line.dash_style = MSO_LINE_DASH_STYLE.DASH
tb(s, W - ML - 2.6, 0.45, 2.6, 0.8, 'Insert Uber for Business logo', 10, False, RGBColor(0xB0,0xB0,0xB0), PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)

# 2 Why this account
s = new('The data points to audit, and audit points to H1', '1 · Account selection', foot='Sources: INEGI EMS, EMIM, ENEC and Economic Census 2024; Google Keyword Planner MX',
        notes='Elegí la industria con datos, no por intuición: scorer de 19 industrias, estacionalidad INEGI y Keyword Planner.')
grid(s, 2.1, 2.6, [
  dict(k='Industry rank', big='#1', body='Audit, accounting and tax leads our opportunity scorer across 19 industries (87.8 of 100).'),
  dict(k='People peak', big='Jan–Feb', body='Audit-firm headcount peaks in Q1 (INEGI), while revenue peaks in December.'),
  dict(k='Deadline spike', big='~10x', body='Searches for annual corporate tax returns in March vs. the rest of the year.'),
  dict(k='Category momentum', big='+32%', body='"uber empresas" searches, Jan–Aug 2026 vs. 2025; "didi empresas" −21%.')], 4)
tb(s, ML, 5.0, CW, 0.6, 'Considered and set aside: pharma (fleets in place; HCP compliance limits Eats), data-center engineering (remote sites, enterprise contractors), firms with 30+ small offices.', 11, False, G3)

# 3 Company profile
s = new('Salles Sainz Grant Thornton at a glance', '1 · Company profile', foot='Sources: grantthornton.mx; Revelio Labs (Mar 2026); Líder Empresarial · ' + F1,
        notes='Los 4 datos que pide el caso: empleados, casos de uso, gasto potencial y urgencia.')
bullets(s, ML, 2.0, 6.6, 4.5, [('Largest Grant Thornton member firm in Latin America;', ' audit, tax, advisory and outsourcing.'),
  ('Nine offices', ' along Mexico\'s business corridors: Mexico City, Monterrey, Guadalajara, Querétaro, Puebla, Aguascalientes, Ciudad Juárez, Tijuana and Puerto Vallarta.'),
  ('Growing in the north', ' from Monterrey, close to nearshoring clients.'), ('Work happens at the client:', ' audit and tax teams spend busy season on client premises and plants.')])
x0 = 7.6; cw2 = (W - ML - x0 - 0.2) / 2
card(s, x0, 2.0, cw2, 2.1, 'Employees', '950–1,000', bigsize=30)
card(s, x0 + cw2 + 0.2, 2.0, cw2, 2.1, 'Urgency', None, 'High: busy season starts in January', bodysize=15)
card(s, x0, 4.3, cw2, 2.2, 'Main use cases', None, 'Client sites, late returns, intercity days, guests, closing-night meals', bodysize=14)
card(s, x0 + cw2 + 0.2, 4.3, cw2, 2.2, 'Potential spend', 'USD 287K', 'a year at full adoption', accent=True, bigsize=28)

# 4 GB forecast
s = new('What the account is worth, and what we can capture in H1', '1 · Revenue analysis · Gross Bookings (GB)', foot=F1,
        notes='GB = valor bruto de viajes y Eats facturados por Uber. Temporada alta: 650×4 + 350×0.5 = 2,775 viajes × USD 10 + 455 pedidos Eats × USD 15 = USD 34.6K/mes. Baja: USD 16.3K/mes. Adopción 20%→70% (piloto en 2 oficinas al inicio; nunca 100% porque hay quien maneja, clientes que mandan transporte y quien prefiere otra app). Conservador: 2 y 1 viajes, techo 50% → USD 40K (12%).')
kp = [('USD 287K', 'Annual GB potential at full adoption'), ('USD 189K', 'H1 2027 potential'), ('USD 91K', 'H1 2027 projected · 26% of the USD 350K quota')]
for i, (v, l) in enumerate(kp):
    x = ML + i * 2.75; bar = rect(s, x, 2.0, 0.06, 1.0, ACC if i == 2 else LINE)
    tb(s, x + 0.2, 1.95, 2.5, 0.6, v, 26, True, BLACK); tb(s, x + 0.2, 2.6, 2.5, 0.5, l, 10, False, G3)
pot = [34.6, 34.6, 34.6, 34.6, 34.6, 16.3]; proj = [6.9, 12.1, 17.3, 20.7, 22.5, 11.4]
bar_chart(s, ML, 3.45, 8.0, 3.2, ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'], proj, [], '"USD "0.0"K"', 'Monthly GB, H1 2027 (USD thousands)', series2=pot)
tb(s, 9.2, 1.95, 3.45, 0.3, 'Scenarios', 10, True, G3, caps=True)
table(s, 2.3, ['', 'Base', 'Conservative'], [['Rides Jan–May', '4', '2'], ['Rides Jun–Dec', '2', '1'], ['Adoption month 6', '70%', '50%'], ['Annual potential', 'USD 287K', 'USD 176K'], ['H1 projected', 'USD 91K', 'USD 40K'], ['Share of quota', '26%', '12%']], [1.3, 0.8, 1.35], 10.5, x=9.2, w=3.45)
tb(s, 9.2, 5.35, 3.45, 1.4, 'GB = rides × USD 10 + Eats orders × USD 15 (case inputs). 1,000 employees, 65% client-facing; other staff 0.5 rides a month; Eats 2 vouchers a month at 35% participation in busy season. Adoption ramps 20%→70%.', 9, False, G3)

# 5 Strategy
s = new('Land before busy season, expand after it, replicate across the vertical', '1 · Acquisition strategy', foot=F1,
        notes='Concentración: el plan de H1 cierra sin esta cuenta; SSGT es upside y referencia para la vertical de auditoría.')
steps = [('Today', 'Stakeholder meeting', 'BDR discovery done. Confirm pains, map the committee and the paper process.'),
         ('Land · Dec', 'Travel for client-site work', 'Ride Policies and engagement codes; pilot in Mexico City and Monterrey on Jan 4.'),
         ('Expand · Q1–Q2', 'All nine offices', 'Uber Eats vouchers for closing nights; Central for guests and candidates.'),
         ('Replicate · H2', 'Reference in audit and tax', 'Use the case with BDO, Crowe, RSM, Forvis Mazars and Baker Tilly.')]
sw = (CW - 0.6) / 4
for i, (n, t, b) in enumerate(steps):
    x = ML + i * (sw + 0.2); rect(s, x, 2.0, sw, 0.05, BLACK)
    tb(s, x, 2.15, sw, 0.35, n, 15, True, ACC); tb(s, x, 2.55, sw, 0.35, t, 14, True); tb(s, x, 2.95, sw, 1.2, b, 12)
grid(s, 4.55, 1.9, [dict(k='Why they buy', body='Margin (rebillable trips), control (one invoice), duty of care'),
  dict(k='Why now', body='Busy season starts in January; a December signature is the only way to capture it'),
  dict(k='Concentration check', body='The H1 plan closes without this account; it is upside and a vertical reference')], 3, bodysize=14)

# 6 Buying committee
s = new('Who we expect in the room', '1 · Role-play preparation', foot=F1, notes='Durante el role play: identificar cada rol con una pregunta (ver Internal brief).')
table(s, 2.0, ['Role', 'Likely title', 'Cares about', 'What we need from them'], [
  ['Economic buyer', 'Managing Partner / CFO', 'Margin, recovery, control', 'Budget owner and signature'],
  ['Champion', 'Administration or HR Director', 'Fewer claims, staff safety', 'Sponsor the policy internally'],
  ['Technical evaluator', 'IT Manager', 'SFTP, SSO, Concur, data', 'Roster and engagement-code files'],
  ['Risk / Legal', 'Quality & Risk Partner', 'Independence, privacy, terms', 'Vendor and independence clearance'],
  ['User / possible blocker', 'Audit Partner', 'Client acceptance, no extra admin', 'Agree on rebilling rules']], [1.3, 1.5, 1.5, 1.6], 13)

# 7 Role play divider
s = new(inv=True, foot='Uber for Business · Proposal for Salles Sainz Grant Thornton', notes='Aquí cambia la voz: el panel es el comité de compra de SSGT.')
tb(s, ML, 0.55, 8, 0.3, 'Role play', 11, True, RGBColor(0xB0,0xB0,0xB0), caps=True)
tb(s, ML, 2.6, 11, 1.6, 'Meeting with Salles Sainz Grant Thornton leadership', 40, True, WHITE)
tb(s, ML, 4.3, 10, 0.5, 'From here on, the panel is the buying committee.', 16, False, RGBColor(0xB0,0xB0,0xB0))

# 8 What we heard
s = new('What we heard from your team', 'Discovery recap', foot='Source: BDR discovery call (to validate) · grantthornton.mx · Revelio Labs (Mar 2026)', notes='Abrir con validación: "¿qué entendimos mal?"')
bullets(s, ML, 2.0, 7.2, 4.5, [('About 950–1,000 professionals', ' in nine offices: Mexico City, Monterrey, Guadalajara, Querétaro, Puebla, Aguascalientes, Ciudad Juárez, Tijuana and Puerto Vallarta.'),
  ('Field work peaks from January to May:', ' year-end audits, annual corporate tax returns and tax opinions.'),
  ('Ground travel runs on personal payment:', ' taxis and ride apps paid by staff, then claimed as expenses.'), ('Late finishes at client sites', ' during closing weeks, often after 9 p.m.')])
card(s, 8.3, 2.0, W - ML - 8.3, 2.3, 'Your priorities', None, 'Protect engagement margins\nTighten expense control\nKeep your people safe and engaged', bodysize=14)
r = rect(s, 8.3, 4.5, W - ML - 8.3, 0.45, LOWC, shape=MSO_SHAPE.ROUNDED_RECTANGLE); tb(s, 8.45, 4.5, W - ML - 8.6, 0.45, 'To confirm today: anything we got wrong?', 12, True, BLACK, anchor=MSO_ANCHOR.MIDDLE)

# 9 Busy season
s = new('Your busy season lands in the first half of 2027', 'Why now', foot='Sources: INEGI EMS 2022–2025 (detrended); Google Keyword Planner MX; LGSM art. 181')
a = seas['5412|people']; ms = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']; L = list('JFMAMJJASOND')
ch = bar_chart(s, ML, 2.2, 5.7, 2.7, L, [round(a[m], 1) for m in ms], [0, 1, 2], '0', 'Audit, accounting and tax firms · headcount index (100 = average month)')
ch.value_axis.minimum_scale = 94; ch.value_axis.maximum_scale = 104
tax = next(x for x in kw['series'] if x['keyword'] == 'declaracion anual personas morales'); i0 = kw['months'].index('2025-01')
bar_chart(s, 6.95, 2.2, 5.7, 2.7, L, tax['values'][i0:i0 + 12], [1, 2, 3], '#,##0', 'Monthly Google searches in Mexico, 2025 · "declaración anual personas morales"')
grid(s, 5.15, 1.4, [dict(k='Mar 31', body='Annual corporate tax returns'), dict(k='Apr 30', body='Shareholder meetings approve financial statements'),
  dict(k='Implication', body='Mobility must be live by mid-January', accent=True)], 3, bodysize=15)

# 10 Use cases
s = new('Five moments when your teams are on the move', 'Use cases', foot=FB)
grid(s, 2.0, 3.8, [dict(k='01 · Daily', body='Office or home to client site\n\nAudit and tax teams working on client premises.', prod='Uber Travel + engagement codes'),
  dict(k='02 · Closing weeks', body='Late exit after closing\n\nRides home after 9 p.m., covered by policy.', prod='Ride Policies'),
  dict(k='03 · Multi-city', body='Airport and intercity days\n\nMonterrey, Guadalajara, Querétaro and border plants.', prod='Uber Travel'),
  dict(k='04 · Guests', body='Clients, candidates and visitors\n\nBooked by assistants or HR on their behalf.', prod='Uber Central'),
  dict(k='05 · Overtime', body='Closing nights and weekends\n\nMeals for teams working late, within set hours and caps.', prod='Vouchers · Uber Eats')], 5, bodysize=13)
tb(s, ML, 6.0, CW, 0.3, 'The numbering follows a typical engagement day, from first visit to closing night.', 11, False, G3)

# 11 Solution
s = new('One platform, configured to your policies', 'Solution', foot=FB)
table(s, 2.0, ['Your need', 'Uber for Business capability', 'Result'], [
  ['Charge each trip to the right engagement', 'Expense codes loaded through SFTP', 'Trips ready to rebill to clients'],
  ['Keep nine offices up to date', 'Roster sync through SFTP or Concur', 'New hires and leavers handled automatically'],
  ['Control when and where people ride', 'Ride Policies, trip flagging, manager approval', 'Policy compliance by design'],
  ['Fewer expense claims', 'Centralized monthly billing', 'One invoice instead of hundreds of claims'],
  ['Book rides for others', 'Uber Central', 'Guests and candidates covered'],
  ['Feed teams on closing nights', 'Uber Eats vouchers with hours and caps', 'Recognition with controlled spend']], [1.4, 1.5, 1.4], 13)

# 12 Rebillable
s = new('Turn travel cost into recoverable cost', 'Margin', foot=FB, notes='La pregunta clave: ¿quién termina pagando esos viajes? Con códigos por encargo, el cliente, si la carta de encargo lo permite.')
steps = [('1', 'Select the engagement', 'The auditor picks the engagement code in the app before riding.'), ('2', 'Bill centrally', "The trip is charged to the firm's account. Nobody pays out of pocket."),
         ('3', 'Report by engagement', 'A monthly file through SFTP lists every trip by engagement code.'), ('4', 'Rebill the client', 'Billing adds rebillable trips to the client invoice, as the engagement letter allows.')]
for i, (n, t, b) in enumerate(steps):
    x = ML + i * (sw + 0.2); rect(s, x, 2.0, sw, 0.05, BLACK)
    tb(s, x, 2.15, sw, 0.4, n, 18, True, ACC); tb(s, x, 2.6, sw, 0.35, t, 14, True); tb(s, x, 3.0, sw, 1.2, b, 12)
card(s, ML, 5.3, CW, 0.9, None, None, 'Every trip carries the engagement code, date, route, time and fare: support your own audit teams would accept.', bodysize=15)

# 13 Duty of care
s = new('Duty of care during the hardest weeks of the year', 'People', foot=FB)
bullets(s, ML, 2.0, 5.8, 4, [('Covered rides home after late closings,', ' set by time window and destination.'), ('Every trip is GPS-tracked;', ' staff can share their trip status and reach in-app safety support.'), ('No cash, no claims:', " staff stop financing the firm's travel from their own pocket.")])
bullets(s, 7.0, 2.0, 5.6, 4, [('Uber Eats vouchers on closing nights', ' turn overtime into recognition.'), ('A visible benefit', ' in a profession where retaining seniors and managers is a constant challenge.'), ('Clear rules', ' that people understand from day one.')])

# 14 Your mobility in numbers
s = new('Your mobility in numbers', 'Your numbers', foot=FB, notes='Construir en vivo con el panel: preguntar cuántos van a oficinas de clientes, cuántas veces al mes, y qué permiten sus cartas de encargo. Versión interactiva en el Radar.')
table(s, 2.0, ['', 'Busy-season month', 'Rest of the year'], [['Trips your people pay out of pocket and claim back today', '2,775', '1,475'],
  ['Trips you could charge to clients', '1,560', '780'], ['Estimated monthly budget, on one invoice', 'USD 38K', 'USD 16K'], ['Of which could be recovered from clients', 'USD 16K', 'USD 8K']], [2.6, 1, 1], 15)
tb(s, ML, 4.6, CW, 0.9, 'Starting point: 1,000 professionals, 65% at client sites, 4 trips per person a month in busy season and 2 the rest of the year, 60% of trips accepted on client invoices, 1 closing-night meal per person a month in busy season. We fill these in with your team. Average trip USD 10; average meal USD 15.', 11, False, G3)

# 15 Rollout
s = new('Live before busy season: a six-step rollout', 'Mutual plan', foot=FB)
tl = [('By Dec 4', 'Align', 'Scope, policies, vendor and independence checks.'), ('By Dec 11', 'Sign', 'Agreement and billing setup.'), ('Dec 14–18', 'Configure', 'Roster and engagement codes through SFTP, ride policies.'),
      ('Jan 4', 'Pilot', 'Mexico City and Monterrey teams.'), ('Jan 18', 'Scale', 'All nine offices; Eats vouchers for closing nights.'), ('Mar 2027', 'Review', 'Usage, rebilled trips and policy exceptions.')]
grid(s, 2.0, 2.4, [dict(k=a, body=b + '\n\n' + c, accent=(i == 3)) for i, (a, b, c) in enumerate(tl)], 6, bodysize=13)
tb(s, ML, 4.7, CW, 0.4, 'Dates assume a decision in the first week of December. Each step has an owner on both sides; the full success plan is in Section 2.', 11, False, G3)

# 16 Next steps
s = new('To move forward, help us understand your process', 'Next steps', foot=FB, notes='Paper process: quién firma, umbrales, revisión de independencia, legal y datos, herramienta de gastos, fecha de decisión.')
tb(s, ML, 2.0, 7.0, 4.5, [[('•  ', False), (q, False)] for q in ['Who approves a new vendor, and up to what amount can each person sign?', 'Does the independence check or vendor due diligence apply to us, and how long does it take?',
   'Will Legal review our standard terms and data-privacy addendum, or use your own template?', 'Which expense tool do you use today (Concur or another), and who owns the travel policy?', 'What decision date gets you live before January?']], 15, spacing=10)
card(s, 8.2, 2.0, W - ML - 8.2, 2.2, 'Proposed next step', None, 'A 30-minute working session this week with Finance, HR and IT to confirm policies and the engagement-code file.', accent=True, bodysize=15)

# 17 Section 2 divider
s = new(inv=True)
tb(s, ML, 0.55, 8, 0.3, 'Section 2', 11, True, RGBColor(0xB0,0xB0,0xB0), caps=True)
tb(s, ML, 2.8, 11, 1.2, 'Mutual success plan', 44, True, WHITE)
tb(s, ML, 4.1, 10, 0.5, 'From signature to habit in eight weeks, with owners on both sides.', 16, False, RGBColor(0xB0,0xB0,0xB0))

# 18 Plan and owners
s = new('Five phases, one owner on each side', '2 · The plan', foot=F2)
table(s, 2.0, ['Phase', 'When', 'SSGT owner', 'Uber owner', 'Done when'], [
  ['Sign', 'By Dec 11', 'CFO', 'Account Executive', 'Agreement signed; billing and invoicing (CFDI) agreed with Tax'],
  ['Configure', 'Dec 14–18', 'IT Manager', 'Implementation lead', 'Roster and engagement codes loaded via SFTP; ride and Eats policies live'],
  ['Pilot', 'Jan 4–15', 'Admin Director', 'Account Manager', '60% of Mexico City and Monterrey staff activated; first trips with codes'],
  ['Scale', 'Jan 18 – Feb 28', 'Office champions', 'Account Manager', 'All nine offices live; 85% activation; Eats vouchers on closing nights'],
  ['Review', 'Mar and May', 'CFO + HR', 'Account Executive', 'Busy-season results; H2 expansion plan agreed']], [0.9, 1.1, 1.1, 1.2, 3.0], 12.5)

# 19 KPIs
s = new('Success measured in your terms, reviewed every week of busy season', '2 · Time to value', foot=F2)
grid(s, 2.0, 1.95, [dict(k='Activation', big='85%', body='of client-facing staff with a linked business profile by Feb 28.'), dict(k='First trip', big='14 days', body='Half of invited staff take a business trip within two weeks.'),
  dict(k='Coded trips', big='90%+', body='of trips carry an engagement code, ready to rebill.'), dict(k='Claims replaced', big='−70%', body='ground-transport expense claims vs. busy season 2026.'),
  dict(k='Policy exceptions', big='<5%', body='of trips flagged outside policy after week 4.'), dict(k='First value', big='Week 1', body='Day-one trip report by engagement for the pilot offices.', accent=True)], 3, bigsize=28, bodysize=12)
tb(s, ML, 6.35, CW, 0.3, 'Proposed targets, to agree with SSGT at signature.', 10, False, G3)

# 20 Playbook
s = new('How we turn a contract into a habit', '2 · Driving adoption', foot=F2)
grid(s, 2.0, 2.1, [dict(k='Sponsor', body='Partner kickoff\n\nA two-minute message from the Managing Partner at the busy-season kickoff.'), dict(k='Access', body='Join in one scan\n\nQR invite at office meetings; profiles linked in under two minutes.'),
  dict(k='People', body='One champion per office\n\nNine go-to contacts who answer questions and spot friction.'), dict(k='Rules', body='One-page policy\n\nWhen rides and meals are covered, and how to pick the engagement code.')], 4, bodysize=13)
grid(s, 4.35, 1.3, [dict(k='Weekly in Jan–Feb', body='Usage report by office, shared with champions and the Admin Director'), dict(k='Visible moment', body='First closing night with Uber Eats vouchers: the benefit people talk about')], 2, bodysize=14)

# 21 Risks
s = new('What could slow adoption, and what we do about it', '2 · Risks to adoption', foot=F2)
table(s, 2.0, ['Risk', 'Early signal', 'Response'], [['Staff do not link profiles', 'Activation below 40% after week 1', 'Champion follow-up and manager reminders by office'],
  ['Policies too tight', 'Many declined or flagged trips', 'Policy review in week 2 with HR and Finance'], ['Invoicing doubts', 'Finance holds the first invoice', 'Tax sign-off on the invoicing setup before go-live'],
  ['Thin coverage near plants', 'Long waits in industrial parks', 'Scheduled trips through Uber Central'], ['Codes left blank', 'Fewer than 90% of trips coded', 'Make the code mandatory; weekly report to engagement managers']], [1.3, 1.4, 2.0], 13)

# 22 FAQ
s = new('Questions we often hear', 'Appendix', foot='Answers to confirm with Uber Legal and Tax before the meeting')
table(s, 2.0, ['Question', 'Short answer'], [['Is it deductible?', 'We will set up company invoicing (CFDI) with your tax team before go-live and confirm the format in writing.'],
  ['Does the platform-worker reform affect the service?', 'Drivers are now registered with IMSS under the 2025 reform. The service continues normally; fares adjusted in mid-2026 are reflected in the forecast.'],
  ["What happens to our employees' data?", "We sync only what the account needs (name, email, group). A data-processing addendum covers Mexico's privacy law."],
  ['What about personal trips?', 'Business and personal profiles stay separate; policies, flags and approvals stop misuse.'],
  ['Are there drivers near industrial parks?', 'Coverage varies by area; Uber Central lets assistants schedule trips in advance where needed.']], [1.4, 3.6], 13)

assert state['n'] == TOTAL, state['n']
prs.save(OUT); print('saved', OUT)
