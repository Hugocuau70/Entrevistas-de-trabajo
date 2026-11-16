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
LOGO_W, LOGO_B = '/tmp/claude-0/-home-user-Entrevistas-de-trabajo/88e3197a-7a0a-53b4-a474-d84a37e1b8be/scratchpad/logos/logo_white.png', '/tmp/claude-0/-home-user-Entrevistas-de-trabajo/88e3197a-7a0a-53b4-a474-d84a37e1b8be/scratchpad/logos/logo_black.png'
BLACK, WHITE = RGBColor(0,0,0), RGBColor(255,255,255)
G2, G3, SURF, LINE, ACC = RGBColor(0x54,0x54,0x54), RGBColor(0x75,0x75,0x75), RGBColor(0xF6,0xF6,0xF6), RGBColor(0xE2,0xE2,0xE2), RGBColor(0x27,0x6E,0xF1)
MID, LOWC = RGBColor(0xEE,0xEE,0xEE), RGBColor(0xFF,0xD9,0xB0)
FONT = 'Inter'
prs = Presentation(); prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BL = prs.slide_layouts[6]
W, H = 13.333, 7.5; ML = 0.7; CW = W - 2 * ML
state = {'n': 0}
TOTAL = 15

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


GREY = RGBColor(0xB0,0xB0,0xB0)
# 1 Cover
s = new(inv=True, foot='Diego Cuauhtémoc · Mid-Market Account Executive', logo=False, notes='Apertura (30 s): "Soy Diego Cuauhtémoc, Account Executive de Uber for Business para Mid-Market. Después de la sesión de discovery de mi BDR con Salles Sainz Grant Thornton, hoy les traigo el plan para ganar su temporada alta 2027." Agenda: perfil y estrategia, role play, mutual success plan.')
s.shapes.add_picture(LOGO_W, Inches(ML), Inches(0.6), height=Inches(0.85))
tb(s, ML, 2.05, 8, 0.3, 'Mid-Market Mexico · H1 2027', 11, True, GREY, caps=True)
tb(s, ML, 2.45, 10.5, 1.8, 'Salles Sainz Grant Thornton: winning busy season 2027', 44, True, WHITE)
tb(s, ML, 4.45, 10, 0.8, 'Section 1 · Company profile, strategy and role play   ·   Section 2 · Mutual success plan', 16, False, GREY)

# 2 About me
s = new('A consultative seller who grows accounts with data', 'About me', foot='Diego Cuauhtémoc · Mid-Market Account Executive', notes='Máximo 40 segundos. Mensaje: vendo de forma consultiva y crezco cuentas con datos.')
grid(s, 2.0, 2.7, [dict(k='Más Gallo Media · Head of Industry', big='USD 1M', body='monthly pipeline across GBM, Bitso and Televisa; closed a MXN 450K data project from discovery to signature.'),
  dict(k='Pinterest · Sr. Performance Solutions Partner', big='2x', body="Marriott's monthly investment, from USD 50K to 100K, with a country proposal for Mexico and Brazil; Coppel's budget 4.4x."),
  dict(k='Lapzo · Head of Growth', big='MXN 1.4M', body='in new monthly recurring revenue from the 118 SQLs my campaigns generated (May–Jul 2026).')], 3, bigsize=32)
card(s, ML, 4.95, CW, 1.15, 'What I bring to Uber for Business', None, "Discovery that finds the real budget, proposals built on the client's own numbers, and accounts that keep growing after signature.", accent=True, bodysize=15)

# 3 Company profile
s = new('Salles Sainz Grant Thornton: an ideal mid-market account', 'Section 1 · Company profile', foot='Sources: grantthornton.mx; Revelio Labs (Mar 2026); selected from 19 industries with INEGI and Google search data (appendix)',
        notes='Los 4 datos del caso: empleados, casos de uso, gasto potencial, urgencia. Gasto: USD 287K/año a adopción plena, USD 91K en H1 (caso base).')
grid(s, 2.0, 2.55, [dict(k='Employees', big='950–1,000', body="Nine offices; Grant Thornton's largest member firm in Latin America.", bigsize=28),
  dict(k='Main use cases', body='Client-site travel, late returns after closings, intercity days, closing-night meals', bodysize=15),
  dict(k='Potential spend', big='USD 287K', body='a year at full adoption; USD 91K inside H1 2027 (base case).', accent=True, bigsize=28),
  dict(k='Urgency', big='High', body='Busy season starts in January: signature needed by Dec 11.', bigsize=28)], 4)
grid(s, 4.8, 1.3, [dict(k='Why ideal', body='The work happens at the client: audit and tax teams travel daily in busy season'),
  dict(k='Why ideal', body="Nine offices along Mexico's business corridors, close to nearshoring plants"),
  dict(k='Why ideal', body='Staff pay and claim today; none of that travel is recovered from clients')], 3, bodysize=14)

# 4 GB forecast
s = new('Base case: USD 287K a year, USD 91K inside H1 because usage ramps', 'Section 1 · Revenue analysis · internal view', foot=F1,
        notes='Temporada alta: 650×4 + 350×0.5 = 2,775 viajes × USD 10 + 455 pedidos Eats × USD 15 = USD 34.6K/mes. Baja: USD 16.3K/mes. Adopción 20%→70%: arranca bajo por el piloto en 2 oficinas; nunca 100% porque hay quien maneja, clientes que mandan transporte y quien prefiere otra app. Si preguntan por concentración: el plan de H1 cierra sin esta cuenta (Sección 3); conservador = USD 40K (12%).')
kp = [('USD 287K', 'Annual GB potential at full adoption'), ('USD 189K', 'H1 2027 potential'), ('USD 91K', 'H1 2027 projected · 26% of the USD 350K quota')]
for i, (v, l) in enumerate(kp):
    x = ML + i * 2.75; rect(s, x, 2.0, 0.06, 1.0, ACC if i == 2 else LINE)
    tb(s, x + 0.2, 1.95, 2.5, 0.6, v, 26, True, BLACK); tb(s, x + 0.2, 2.6, 2.5, 0.5, l, 10, False, G3)
bar_chart(s, ML, 3.45, 8.0, 3.2, ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'], [6.9, 12.1, 17.3, 20.7, 22.5, 11.4], [], '"USD "0.0"K"', 'Monthly GB, H1 2027 (USD thousands)', series2=[34.6, 34.6, 34.6, 34.6, 34.6, 16.3])
tb(s, 9.2, 1.95, 3.45, 0.3, 'Scenarios', 10, True, G3, caps=True)
table(s, 2.3, ['', 'Base', 'Conservative'], [['Rides Jan–May', '4', '2'], ['Rides Jun–Dec', '2', '1'], ['Adoption month 6', '70%', '50%'], ['Annual potential', 'USD 287K', 'USD 176K'], ['H1 projected', 'USD 91K', 'USD 40K'], ['Share of quota', '26%', '12%']], [1.3, 0.8, 1.35], 10.5, x=9.2, w=3.45)
tb(s, 9.2, 5.35, 3.45, 1.4, 'GB = gross value of rides and Eats orders billed through Uber = rides × USD 10 + Eats orders × USD 15 (case inputs). 1,000 employees, 65% client-facing; other staff 0.5 rides a month; Eats 2 vouchers a month at 35% participation in busy season.', 9, False, G3)

# 5 Strategy
s = new('Land before busy season, expand after it, replicate across the vertical', 'Section 1 · Acquisition strategy', foot=F1)
sw = (CW - 0.6) / 4
steps = [('Today', 'Stakeholder meeting', 'BDR discovery done. Confirm pains, map the committee and the paper process.'),
         ('Land · Dec', 'Travel for client-site work', 'Ride Policies and engagement codes; pilot in Mexico City and Monterrey on Jan 4.'),
         ('Expand · Q1–Q2', 'All nine offices', 'Uber Eats vouchers for closing nights; Central for guests and candidates.'),
         ('Replicate · H2', 'Reference in audit and tax', 'Use the case with BDO, Crowe, RSM, Forvis Mazars and Baker Tilly.')]
for i, (n, t, b) in enumerate(steps):
    x = ML + i * (sw + 0.2); rect(s, x, 2.0, sw, 0.05, BLACK)
    tb(s, x, 2.15, sw, 0.35, n, 15, True, ACC); tb(s, x, 2.55, sw, 0.35, t, 14, True); tb(s, x, 2.95, sw, 1.2, b, 12)
grid(s, 4.55, 1.9, [dict(k='Why they buy', body='Margin (rebillable trips), control (one invoice), duty of care'),
  dict(k='Why now', body='Busy season starts in January; a December signature is the only way to capture it'),
  dict(k='Concentration check', body='The H1 plan closes without this account; it is upside and a vertical reference')], 3, bodysize=14)

# 6 Busy season
s = new('Your busy season lands in the first half of 2027', 'Section 1 · Role play · What we see in your market', foot='Sources: INEGI EMS 2022–2025 (detrended); Google Keyword Planner MX; LGSM art. 181',
        notes='Inicio del role play: el panel es el comité de SSGT. Abrir con lo que vemos de su mercado y validar.')
a = seas['5412|people']; ms = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']; L = list('JFMAMJJASOND')
ch = bar_chart(s, ML, 2.2, 5.7, 2.7, L, [round(a[m], 1) for m in ms], [0, 1, 2], '0', 'Audit, accounting and tax firms · headcount index (100 = average month)')
ch.value_axis.minimum_scale = 94; ch.value_axis.maximum_scale = 104
tax = next(x for x in kw['series'] if x['keyword'] == 'declaracion anual personas morales'); i0 = kw['months'].index('2025-01')
bar_chart(s, 6.95, 2.2, 5.7, 2.7, L, tax['values'][i0:i0 + 12], [1, 2, 3], '#,##0', 'Monthly Google searches in Mexico, 2025 · "declaración anual personas morales"')
grid(s, 5.15, 1.4, [dict(k='Mar 31', body='Annual corporate tax returns'), dict(k='Apr 30', body='Shareholder meetings approve financial statements'),
  dict(k='Implication', body='Mobility must be live by mid-January', accent=True)], 3, bodysize=15)

# 7 Five moments
s = new('Five moments, one platform configured to your policies', 'Section 1 · Role play · Solution', foot=FB)
grid(s, 2.0, 3.0, [dict(k='01 · Daily', body='Office or home to client site\n\nEach trip tagged to its engagement.', prod='Uber Travel + expense codes'),
  dict(k='02 · Closing weeks', body='Late ride home\n\nCovered after 9 p.m.; trip tracking and safety support.', prod='Ride Policies'),
  dict(k='03 · Multi-city', body='Airport and intercity days\n\nMonterrey, Guadalajara, Querétaro and border plants.', prod='Uber Travel'),
  dict(k='04 · Guests', body='Clients and candidates\n\nBooked by assistants or HR on their behalf.', prod='Uber Central'),
  dict(k='05 · Overtime', body='Closing-night meals\n\nWithin set hours and caps.', prod='Vouchers · Uber Eats')], 5, bodysize=13)
card(s, ML, 5.25, CW, 1.0, 'Built in', None, 'Roster and engagement codes synced by SFTP or Concur · trip flagging and approvals · one monthly invoice instead of hundreds of claims', bodysize=14)

# 8 Rebillable
s = new('Turn travel cost into recoverable cost', 'Section 1 · Role play · Margin', foot=FB, notes='La pregunta clave: ¿quién termina pagando esos viajes? Con códigos por encargo, el cliente, si la carta de encargo lo permite.')
steps = [('1', 'Select the engagement', 'The auditor picks the engagement code in the app before riding.'), ('2', 'Bill centrally', "The trip is charged to the firm's account. Nobody pays out of pocket."),
         ('3', 'Report by engagement', 'A monthly file through SFTP lists every trip by engagement code.'), ('4', 'Rebill the client', 'Billing adds rebillable trips to the client invoice, as the engagement letter allows.')]
for i, (n, t, b) in enumerate(steps):
    x = ML + i * (sw + 0.2); rect(s, x, 2.0, sw, 0.05, BLACK)
    tb(s, x, 2.15, sw, 0.4, n, 18, True, ACC); tb(s, x, 2.6, sw, 0.35, t, 14, True); tb(s, x, 3.0, sw, 1.2, b, 12)
card(s, ML, 4.9, CW, 0.9, None, None, 'Every trip carries the engagement code, date, route, time and fare: support your own audit teams would accept.', bodysize=15)

# 9 Numbers
s = new('Your mobility in numbers', 'Section 1 · Role play · Your numbers', foot=FB, notes='Construir en vivo: pedir al panel sus números (personas en campo, viajes al mes, % aceptado por clientes). Versión interactiva en el Radar.')
table(s, 2.0, ['', 'Busy-season month', 'Rest of the year'], [['Trips your people pay out of pocket and claim back today', '2,775', '1,475'],
  ['Trips you could charge to clients', '1,560', '780'], ['Estimated monthly budget, on one invoice', 'USD 38K', 'USD 16K'], ['Of which could be recovered from clients', 'USD 16K', 'USD 8K']], [2.6, 1, 1], 15)
tb(s, ML, 4.6, CW, 0.9, 'Starting point to adjust with your team: 1,000 professionals, 65% at client sites, 4 trips per person a month in busy season and 2 the rest of the year, 60% of trips accepted on client invoices, 1 closing-night meal per person a month in busy season. Average trip USD 10; average meal USD 15.', 11, False, G3)

# 10 Rollout + next step
s = new('Live before busy season, with a decision in early December', 'Section 1 · Role play · Next steps', foot=FB, notes='Cerrar el role play con un siguiente paso concreto y fechado.')
tl = [('By Dec 4', 'Align', 'Scope, policies, vendor and independence checks.'), ('By Dec 11', 'Sign', 'Agreement, billing and invoicing setup.'), ('Dec 14–18', 'Configure', 'Roster and engagement codes by SFTP; policies.'),
      ('Jan 4', 'Pilot', 'Mexico City and Monterrey teams.'), ('Jan 18', 'Scale', 'All nine offices; Eats on closing nights.'), ('Mar 2027', 'Review', 'Usage, rebilled trips, exceptions.')]
grid(s, 2.0, 2.2, [dict(k=a, body=b + '\n\n' + c, accent=(i == 3)) for i, (a, b, c) in enumerate(tl)], 6, bodysize=13)
grid(s, 4.5, 1.4, [dict(k='To confirm with you today', body='Who signs and up to what amount · independence and vendor checks · legal and data-privacy terms · decision date'),
  dict(k='Proposed next step', body='A 30-minute working session this week with Finance, HR and IT', accent=True)], 2, bodysize=14)

# 11 MSP
s = new('From signature to habit in eight weeks, with owners on both sides', 'Section 2 · Mutual success plan', foot='Proposed targets, to agree at signature · ' + F2)
ph = [('By Dec 11', 'Sign', 'SSGT: CFO\nUber: Account Executive', 'Invoicing agreed with Tax'), ('Dec 14–18', 'Configure', 'SSGT: IT Manager\nUber: Implementation lead', 'Roster and codes live'),
      ('Jan 4–15', 'Pilot', 'SSGT: Admin Director\nUber: Account Manager', '60% of pilot staff active'), ('Jan 18 – Feb 28', 'Scale', 'SSGT: office champions\nUber: Account Manager', '85% activation, 9 offices'),
      ('Mar and May', 'Review', 'SSGT: CFO + HR\nUber: Account Executive', 'H2 expansion agreed')]
grid(s, 2.0, 2.2, [dict(k=a, body=b + '\n\n' + c, prod=d, accent=(i == 2)) for i, (a, b, c, d) in enumerate(ph)], 5, bodysize=12)
grid(s, 4.45, 1.75, [dict(k='First value', big='Week 1', body='trip report by engagement'), dict(k='Coded trips', big='90%+', body='ready to rebill'),
  dict(k='Claims replaced', big='−70%', body='vs. busy season 2026'), dict(k='Policy exceptions', big='<5%', body='after week 4')], 4, bigsize=26)

# 12 Adoption
s = new('How we turn a contract into a habit, and what we watch', 'Section 2 · Mutual success plan', foot=F2)
tb(s, ML, 2.0, 5.6, 0.35, 'Launch playbook', 14, True)
bullets(s, ML, 2.45, 5.6, 4, [('Partner kickoff:', ' a two-minute message from the Managing Partner at the busy-season kickoff.'), ('Join in one scan:', ' QR invite at office meetings.'),
  ('One champion per office', ' who answers questions and spots friction.'), ('Visible moment:', ' the first closing night with Uber Eats vouchers.'), ('Weekly usage report', ' by office during January and February.')], 14)
table(s, 2.0, ['If we see', 'We do'], [['Activation below 40% in week 1', 'Champion and manager follow-up by office'], ['Many flagged or declined trips', 'Policy review in week 2 with HR and Finance'],
  ['Fewer than 90% of trips coded', 'Make the code mandatory; report to engagement managers'], ['Long waits near plants', 'Scheduled trips through Uber Central']], [1.2, 1.5], 12.5, x=6.8, w=W - ML - 6.8)

# 13 FAQ
s = new('Questions we often hear', 'Appendix · Q&A', foot='Answers to confirm with Uber Legal and Tax before the meeting')
table(s, 2.0, ['Question', 'Short answer'], [['Is it deductible?', 'We will set up company invoicing (CFDI) with your tax team before go-live and confirm the format in writing.'],
  ['Does the platform-worker reform affect the service?', 'Drivers are now registered with IMSS under the 2025 reform. The service continues normally; fares adjusted in mid-2026 are reflected in the forecast.'],
  ["What happens to our employees' data?", "We sync only what the account needs (name, email, group). A data-processing addendum covers Mexico's privacy law."],
  ['What about personal trips?', 'Business and personal profiles stay separate; policies, flags and approvals stop misuse.'],
  ['Are there drivers near industrial parks?', 'Coverage varies by area; Uber Central lets assistants schedule trips in advance where needed.']], [1.4, 3.6], 13)

# 14 Committee
s = new('Who we expect in the room', 'Appendix · Role-play preparation', foot='Appendix')
table(s, 2.0, ['Role', 'Likely title', 'Cares about', 'What we need from them'], [
  ['Economic buyer', 'Managing Partner / CFO', 'Margin, recovery, control', 'Budget owner and signature'],
  ['Champion', 'Administration or HR Director', 'Fewer claims, staff safety', 'Sponsor the policy internally'],
  ['Technical evaluator', 'IT Manager', 'SFTP, SSO, Concur, data', 'Roster and engagement-code files'],
  ['Risk / Legal', 'Quality & Risk Partner', 'Independence, privacy, terms', 'Vendor and independence clearance'],
  ['User / possible blocker', 'Audit Partner', 'Client acceptance, no extra admin', 'Agree on rebilling rules']], [1.3, 1.5, 1.5, 1.6], 13)

# 15 Why audit
s = new('The data points to audit, and audit points to H1', 'Appendix · Account selection', foot='Sources: INEGI EMS, EMIM, ENEC and Economic Census 2024; Google Keyword Planner MX · Appendix')
grid(s, 2.1, 2.6, [dict(k='Industry rank', big='#1', body='Audit, accounting and tax leads our opportunity scorer across 19 industries (87.8 of 100).'),
  dict(k='People peak', big='Jan–Feb', body='Audit-firm headcount peaks in Q1 (INEGI), while revenue peaks in December.'),
  dict(k='Deadline spike', big='~10x', body='Searches for annual corporate tax returns in March vs. the rest of the year.'),
  dict(k='Category momentum', big='+32%', body='"uber empresas" searches, Jan–Aug 2026 vs. 2025; "didi empresas" −21%.')], 4)

assert state['n'] == TOTAL, state['n']
prs.save(OUT); print('saved', OUT)
