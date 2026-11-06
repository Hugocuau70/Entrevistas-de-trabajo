"""Rellena la plantilla oficial de Hootsuite ("Hootsuite Interview Assignment - Slide Deck Template")
con el caso GBM.

Uso:
  python3 fill_template.py base.pptx salida.pptx

`base.pptx` = la plantilla exportada de Google Slides, ya reordenada a 10 slides
(1 portada, 2 Who Am I, 3 agenda con tiempos, 12 stats, 15 tres columnas, 12 duplicada,
14 dos columnas, 8 "Listen", 5 divisor, 13 bullets). Todo el formato (fuentes Montserrat,
colores del tema, layouts) viene de la plantilla; aquí solo se cambia texto, foto y notas.
"""
import copy
import io
import os
import sys

from lxml import etree
from PIL import Image
from pptx import Presentation
from pptx.util import Emu, Inches, Pt

A = "http://schemas.openxmlformats.org/drawingml/2006/main"
NS = {"a": A}
HERE = os.path.dirname(os.path.abspath(__file__))
PHOTO = os.path.join(HERE, "assets", "diego.jpg")


def q(tag):
    return "{%s}%s" % (A, tag.split(":")[1])


def _base_rpr(p_el):
    r = p_el.find("a:r", NS)
    rpr = r.find("a:rPr", NS) if r is not None else None
    return copy.deepcopy(rpr) if rpr is not None else etree.SubElement(etree.Element(q("a:r")), q("a:rPr"))


def _apply(rpr, o):
    if "sz" in o:
        rpr.set("sz", str(int(o["sz"] * 100)))
    if "b" in o:
        rpr.set("b", "1" if o["b"] else "0")
    if "i" in o:
        rpr.set("i", "1" if o["i"] else "0")
    if "color" in o:  # scheme color name, e.g. dk1, lt2, accent1
        for f in rpr.findall("a:solidFill", NS):
            rpr.remove(f)
        sf = etree.Element(q("a:solidFill"))
        etree.SubElement(sf, q("a:schemeClr")).set("val", o["color"])
        rpr.insert(0, sf)
    if "font" in o:
        for t in ("a:latin", "a:ea", "a:cs", "a:sym"):
            el = rpr.find(t, NS)
            if el is not None:
                el.set("typeface", o["font"])


def fill(txbody, paras, ppr_from=None, first_ppr_from=None):
    """Replace all paragraphs of a txBody.

    paras: list of paragraphs; each paragraph is a list of runs (text, overrides) or a plain string.
    The first existing paragraph supplies pPr and run formatting; `ppr_from` (index) supplies the pPr
    for paragraphs after the first (useful when the template uses spcBef on later items).
    """
    ps = txbody.findall("a:p", NS)
    tpl_first = ps[first_ppr_from or 0]
    tpl_rest = ps[ppr_from] if ppr_from is not None and ppr_from < len(ps) else tpl_first
    base_first, base_rest = _base_rpr(tpl_first), _base_rpr(tpl_rest)
    end_rpr = tpl_first.find("a:endParaRPr", NS)
    for p in ps:
        txbody.remove(p)
    for i, para in enumerate(paras):
        if isinstance(para, str):
            para = [(para, {})]
        src = tpl_first if i == 0 else tpl_rest
        base_rpr = base_first if i == 0 else base_rest
        p = etree.SubElement(txbody, q("a:p"))
        ppr = src.find("a:pPr", NS)
        if ppr is not None:
            p.append(copy.deepcopy(ppr))
        for text, o in para:
            if text == "\n":
                br = etree.SubElement(p, q("a:br"))
                br.append(copy.deepcopy(base_rpr))
                continue
            r = etree.SubElement(p, q("a:r"))
            rpr = copy.deepcopy(base_rpr)
            _apply(rpr, o)
            r.append(rpr)
            etree.SubElement(r, q("a:t")).text = text
        if end_rpr is not None:
            p.append(copy.deepcopy(end_rpr))


def shape(slide, sid):
    for s in slide.shapes:
        if s.shape_id == sid:
            return s
    raise KeyError(sid)


def tb(slide, sid):
    return shape(slide, sid)._element.txBody


def set_cell(cell, paras, ppr_from=None, first_ppr_from=None):
    fill(cell._tc.txBody, paras, ppr_from=ppr_from, first_ppr_from=first_ppr_from)


def notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text


def stats_table(slide, title, big, small, desc, source=None):
    fill(tb(slide, 161), [title])
    t = [s for s in slide.shapes if s.has_table][0].table
    for c in range(5):
        set_cell(t.cell(0, c), [[(big[c], {"sz": 40}), (small[c], {"sz": 18})]])
        set_cell(t.cell(1, c), [desc[c]], first_ppr_from=1)


def main(src, out):
    prs = Presentation(src)
    S = prs.slides

    # ---------------- 1 · Cover ----------------
    s = S[0]
    fill(tb(s, 77), [
        [("From 22M accounts to a country of active investors", {"sz": 30})],
        [("A value proposal for GBM", {"sz": 20})],
        [("Diego Cuauhtémoc Guerrero  ·  November 2026", {"sz": 14})],
    ])
    notes(s,
          "[0:00–0:30] Thank you all for the time today. For this role play I chose GBM, Grupo Bursátil Mexicano — "
          "Mexico's largest brokerage by number of accounts. I chose it for a reason I'll explain in a second. "
          "Context: last week I ran discovery with GBM's Director of Social Media. Today I'm coming back to show how "
          "Hootsuite connects to the business goals she shared — this is not a feature tour.")

    # ---------------- 2 · Who Am I ----------------
    s = S[1]
    # Photo: replace the template portrait, cropped to the frame's aspect ratio
    pic = shape(s, 88)
    ar = pic.width / pic.height
    im = Image.open(PHOTO).convert("RGB")
    w, h = im.size
    nh = int(w / ar)
    top = int(h * 0.04)
    im = im.crop((0, top, w, top + nh))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=92)
    buf.seek(0)
    _, rid = s.part.get_or_add_image_part(buf)
    blip = pic._element.find(".//a:blip", NS)
    blip.set("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed", rid)
    src_rect = pic._element.find(".//a:srcRect", NS)
    if src_rect is not None:
        for k in list(src_rect.attrib):
            del src_rect.attrib[k]

    fill(tb(s, 85), [
        [("Diego Cuauhtémoc Guerrero", {"sz": 16})],
        [("Consultative seller · growth & performance leader · Mexico City · Spanish / English", {})],
        [("Why Hootsuite: ", {"b": True}), ("I’ve sat on GBM’s side of the table, and I speak the language of the "
                                            "marketing leaders I’d sell to — because I’ve been one.", {})],
    ], ppr_from=1)

    # Career highlights in the empty dark column, styled like the template's light text
    box = s.shapes.add_textbox(Emu(182872), Emu(1250000), Emu(2900000), Emu(3700000))
    box.name = "Career highlights"
    body = box.text_frame._txBody
    bp = body.find("a:bodyPr", NS)
    bp.set("wrap", "square")
    title_tb = tb(s, 86)
    title_p = copy.deepcopy(title_tb.find("a:p", NS))
    for p in body.findall("a:p", NS):
        body.remove(p)
    body.append(title_p)
    hl = [
        ("Más Gallo Media", "Head of Industry · 2022–24", "USD 1M/month pipeline with GBM, Bitso and Televisa — full cycle, discovery to close"),
        ("Pinterest", "Sr. Performance Solutions Partner · 2024–26", "Marriott USD 50K → 100K/month; Coppel 4.4× daily budget"),
        ("LAPZO", "Head of Growth · 2026", "118 SQLs and MXN 1.4M in new MRR in one quarter"),
    ]
    paras = []
    for co, role, line in hl:
        paras.append([(co, {"sz": 13, "b": True, "color": "lt2"}), ("  " + role, {"sz": 9, "b": False, "color": "accent1", "font": "Montserrat"})])
        paras.append([(line, {"sz": 11, "b": False, "color": "lt2", "font": "Montserrat"})])
    fill(body, paras)
    for i, p in enumerate(body.findall("a:p", NS)):
        ppr = p.find("a:pPr", NS)
        lns = ppr.find("a:lnSpc", NS)
        if lns is not None:
            ppr.remove(lns)
        sb = ppr.find("a:spcBef/a:spcPts", NS)
        if sb is not None:
            sb.set("val", "1400" if (i % 2 == 0 and i > 0) else "200")
    notes(s,
          "[0:30–3:00] Quick intro. I'm Diego, based in Mexico City. Three things about my background that matter for this role. "
          "One: at Más Gallo Media I ran the full sales cycle with enterprise accounts — including GBM, Bitso and Televisa — "
          "managing about a million dollars a month in pipeline. So I know how GBM buys and how many people sit at that table: "
          "marketing, compliance, IT, procurement. "
          "Two: at Pinterest I grew enterprise investment by selling business outcomes, not ad products — for example doubling "
          "Marriott's monthly investment from 50 to 100 thousand dollars with a country-specific proposal. "
          "Three: today I lead growth at LAPZO, a B2B SaaS, where my campaigns fed 118 SQLs and 1.4 million pesos in new MRR "
          "in a quarter. "
          "Why Hootsuite: the people I'd sell to — heads of social, CMOs — are people I've worked alongside for years.")

    # ---------------- 3 · Agenda ----------------
    s = S[2]
    body = tb(s, 95)
    ps = body.findall("a:p", NS)
    rows = [("3 min", "Who I am"), ("4 min", "What we heard"), ("6 min", "How we help"),
            ("7 min", "Impact & plan"), ("10 min", "Live demo")]
    tpl = ps[1]
    for p in ps:
        body.remove(p)
    for i, (tm, topic) in enumerate(rows):
        p = copy.deepcopy(tpl)
        for br in p.findall("a:br", NS):
            p.remove(br)
        runs = p.findall("a:r", NS)
        runs[0].find("a:t", NS).text = tm
        runs[1].find("a:t", NS).text = "\t"
        runs[2].find("a:t", NS).text = topic
        for extra in runs[3:]:
            p.remove(extra)
        for r in runs[:3]:
            r.find("a:rPr", NS).set("sz", "2000")
        ppr = p.find("a:pPr", NS)
        tabs = etree.Element(q("a:tabLst"))
        etree.SubElement(tabs, q("a:tab")).attrib.update({"pos": "1463040", "algn": "l"})
        bu = ppr.find("a:buNone", NS)  # schema order: ... bullets, tabLst, defRPr
        bu.addnext(tabs) if bu is not None else ppr.append(tabs)
        if i == 0:
            p.find("a:pPr/a:spcBef/a:spcPts", NS).set("val", "0")
        body.append(p)
    notes(s, "Agenda: 20 minutes of value presentation, then a 10-minute live demo of social listening. Don't read this slide — 10 seconds max.")

    # ---------------- 4 · What we heard (stats) ----------------
    s = S[3]
    stats_table(
        s, "What we heard in discovery",
        big=["22", "≈3", "+19", "500", "5"],
        small=["M", "%", "%", "+", "+"],
        desc=[
            "accounts opened by Q3 2025 — most through the Mercado Pago alliance",
            "of accounts are active (~670K clients). Activation is the growth lever",
            "fraud claims at CONDUSEF, Jan–May 2026 — fake ‘verified’ profiles offer scam investments",
            "GBM Advisors today, ~1,000 next year — and every post needs Compliance",
            "networks where first-time investors ask questions — with no single view or SLA",
        ],
    )
    notes(s,
          "[3:00–7:00] Let me play back what I heard in discovery — tell me if I got anything wrong. "
          "GBM's north star is in their Co-CEO Pedro de Garay's own words: 'Queremos convertir a México en un país de inversionistas exitosos.' "
          "GBM has done the hard part of acquisition: around 22 million accounts at the end of Q3 2025, most through Mercado Pago. "
          "But Moody's estimated only about 670 thousand active clients — roughly 3%. The next chapter is turning sign-ups into confident, active investors. "
          "Three things stand in the way, and all of them live on social. "
          "First, trust: fake GBM-looking profiles and AI-generated scam ads. CONDUSEF fraud claims rose about 19% in the first five months of 2026, "
          "and CONDUSEF warned about fake 'verified' profiles on Facebook, Instagram and TikTok. Today your team finds these manually, often after a customer complains. "
          "Second, scale: every time the Mercado Pago yield changes, DMs explode with first-time-investor questions across five-plus networks, with no single view and no SLA. "
          "Third, advisors: GBM Advisors went from about 250 to over 500, heading to a thousand. They want content, but Compliance can't approve every post by hand. "
          "Did I capture that right? Anything you'd add or re-prioritize? [pause]")

    # ---------------- 5 · How Hootsuite helps (three columns) ----------------
    s = S[4]
    fill(tb(s, 191), ["Three outcomes, one Social OS"])
    cols = [
        (184, "Protect trust", "Lumen by Talkwalker + Perch",
         "Spot impersonators, scam ads and sentiment spikes across 150M+ sources. Every post approved and compliance-checked."),
        (187, "Activate investors", "Nest + Wisdom",
         "One inbox for every network, routed to Care with SLAs. Wisdom drafts answers; listening turns top questions into content."),
        (190, "Scale advisors", "Parliament",
         "Pre-approved posts advisors share in one click. Compliance approves once — it scales to 1,000 voices."),
    ]
    for sid, head, app, body_txt in cols:
        sh = shape(s, sid)
        sh.top = Emu(int(3.55 * 914400))
        sh.height = Emu(int(2.0 * 914400))
        sh.width = Emu(int(2.75 * 914400))
        fill(sh._element.txBody, [
            [(head, {"b": True, "sz": 16, "font": "Montserrat"})],
            [(app, {"b": True, "sz": 10, "font": "Montserrat"})],
            [(body_txt, {"b": False, "sz": 10, "font": "Montserrat Medium"})],
        ])
        for i, p in enumerate(sh._element.txBody.findall("a:p", NS)):
            sb = p.find("a:pPr/a:spcBef/a:spcPts", NS)
            if sb is not None and i > 0:
                sb.set("val", "400")
        bodypr = sh._element.txBody.find("a:bodyPr", NS)
        for c in list(bodypr):
            bodypr.remove(c)
        etree.SubElement(bodypr, q("a:noAutofit"))
    notes(s,
          "[7:00–13:00] Here's how Hootsuite maps to those three outcomes — organized by your business outcomes, not our product menu. "
          "1 · Protect trust. Lumen by Talkwalker monitors over 150 million sources in 187 languages — your name, your logo in images, your executives, "
          "and scam language like 'rendimiento garantizado'. When a fake profile or a sentiment spike appears, the right people get an alert in minutes, "
          "not after a CONDUSEF complaint. Perch adds approval workflows and automated compliance checks, so every post is reviewed and archived — "
          "Compliance gets control without being the bottleneck. "
          "2 · Activate investors. Nest puts every DM and comment into one inbox, routes account questions to Care with SLAs, and Wisdom drafts replies "
          "from GBM's approved answers. The bigger value is the loop: listening shows the top questions of first-time investors — like confusion when "
          "the Mercado Pago yield changes — and your content team turns that into education that drives a first investment. "
          "3 · Scale advisors. Parliament gives GBM Advisors a library of pre-approved content to share in one click. Compliance approves once; it scales "
          "to a thousand trusted voices, and you see the reach and leads each advisor drives. Your Co-CEO said AI won't replace the advisor — it will make "
          "them more productive. This is exactly that. "
          "Across all three sits Wisdom, the AI agent launched in June — I'll show it live in the demo. "
          "Which of these three would make the biggest difference for your team next quarter?")

    # ---------------- 6 · Business impact (stats) ----------------
    s = S[5]
    stats_table(
        s, "What success could look like in 12 months",
        big=["+21", "<24", "500", "1", "90"],
        small=["K", "h", "K+", " view", " days"],
        desc=[
            "newly active investors if social care and content re-activate just 0.1% of ~21M dormant accounts",
            "from fake profile to takedown request — SIX Group closed 80 unofficial accounts this way",
            "organic impressions per advisor content wave: 1,000 advisors × ~500 connections, zero media cost",
            "of every conversation, risk and KPI: share of voice vs. Nu, Bitso and Mercado Pago, sentiment, response time",
            "to prove ROI in a pilot before scaling. Illustrative figures, validated with GBM’s data",
        ],
    )
    notes(s,
          "[13:00–16:30] What does this mean in business terms? These are illustrative — I'd rather build the real numbers with your data. "
          "Activation: around 21 million dormant accounts. Re-activating just one tenth of one percent is about 21 thousand new active investors. "
          "Trust: SIX Group, the Swiss exchange operator, used Hootsuite as its social compliance hub, closed 80 unofficial accounts and typically gets "
          "takedowns within 24 hours. Every hour a fake profile stays live is a potential victim and a headline. "
          "Advisors: a thousand advisors with ~500 connections each is half a million organic impressions per content wave, zero media cost. "
          "One view: share of voice versus Nu, Bitso and Mercado Pago, sentiment on trust topics, response times, advisor leads — the dashboard for your CMO. "
          "And 90 days to prove it. How does your leadership measure success for social today?")

    # ---------------- 7 · Path forward (two columns) ----------------
    s = S[6]
    fill(tb(s, 176), ["A 90-day pilot to prove value — then scale"])
    fill(tb(s, 173), ["Low risk by design: we start with what matters most to Compliance."])
    fill(tb(s, 175), [
        [("Days 1–30 · Listen & protect: ", {"b": True}), ("Lumen queries for brand, fraud and competitors; alerts; approvals in Perch", {})],
        [("Days 31–60 · Engage: ", {"b": True}), ("every network in Nest, Care routing, SLAs, Wisdom-assisted replies", {})],
        [("Days 61–90 · Amplify: ", {"b": True}), ("Parliament with 50 GBM Advisors; executive business review with ROI", {})],
    ], ppr_from=1)
    fill(tb(s, 174), [
        [("Week 1: ", {"b": True}), ("security & compliance review with your Compliance and IT teams", {})],
        [("Week 2: ", {"b": True}), ("KPI workshop with Customer Care and the GBM Advisors lead", {})],
        [("Week 3: ", {"b": True}), ("pilot proposal and mutual success plan for leadership", {})],
        [("Does this reflect your priorities? What would make this a “yes” for your leadership?", {"b": True, "i": True})],
    ], ppr_from=1)
    for sid in (174, 175):
        for p in tb(s, sid).findall("a:p", NS):
            for r in p.findall("a:r/a:rPr", NS):
                r.set("sz", "1200")
    notes(s,
          "[16:30–19:30] To make this low-risk, I propose a 90-day pilot. Days 1–30, listen and protect: Lumen queries for brand, fraud and competitors, "
          "alerts to Security and Comms, approval workflows with Compliance — the biggest risk first. Days 31–60, engage: every GBM network in Nest with "
          "routing, SLAs and Wisdom-assisted replies. Days 61–90, amplify: a Parliament pilot with 50 GBM Advisors and an executive business review with ROI. "
          "Next steps: week one, a security and compliance review — that's where financial-services deals slow down, so let's start there. Week two, a KPI "
          "workshop with Care and the GBM Advisors lead. Week three, a proposal and mutual success plan for leadership. "
          "So — does this reflect your priorities, and what would make this a 'yes' for your leadership? [stop and listen] "
          "Transition: let me show you what this looks like live.")

    # ---------------- 8 · Listen (demo divider) ----------------
    s = S[7]
    fill(tb(s, 132), ["Let’s listen: live demo"])
    notes(s,
          "[10-minute demo] 1) Brand pulse for GBM with 'glioblastoma' excluded. 2) Risk radar: GBM + estafa / fraude / perfil falso / no puedo retirar. "
          "3) First-time investor questions about GBM + Mercado Pago. 4) Share of voice vs. Nu, Bitso, Mercado Pago. 5) Ask Wisdom: 'Why did negative "
          "sentiment about GBM change this week, and what should my team do?' Close: 'What would you want to monitor first?' "
          "Full script and boolean queries in 04_demo_social_listening.md.")

    # ---------------- 9 · Thank you ----------------
    s = S[8]
    body = tb(s, 109)
    p = body.find("a:p", NS)
    runs = p.findall("a:r", NS)
    runs[0].find("a:t", NS).text = "Thank you"
    runs[-1].find("a:t", NS).text = "Questions? · ¿Preguntas?"
    for r in runs[1:-1]:
        if r.find("a:t", NS) is not None:
            p.remove(r)
    notes(s, "Q&A. Have 2–3 questions ready for the panel (see 05_preguntas_y_objeciones.md).")

    # ---------------- 10 · Appendix: sources ----------------
    s = S[9]
    fill(tb(s, 167), ["Appendix: where the numbers come from"])
    fill(tb(s, 166), [
        "All GBM and market figures are public; the discovery call is a role-play assumption.",
        "22M accounts and MXN 1,176bn in custody — Corporativo GBM, 3T25 quarterly report",
        "~670K active clients (mid-2025) — Moody’s, Oct 2025, cited by El CEO",
        "500+ advisors in 25 states, ~1,000 next year — Pioneros 2026 coverage (DPL News)",
        "Fraud claims up ~19%, Jan–May 2026 — CONDUSEF figures cited by El Imparcial",
        "Social OS, Wisdom, 150M+ sources, 187 languages — Hootsuite press release, 24 Jun 2026",
        "SIX Group: 80 unofficial accounts closed, takedowns within 24h — Hootsuite customer story",
    ], ppr_from=1, first_ppr_from=0)
    fill(tb(s, 168), ["Illustrative: +21K = 0.1% of ~21M dormant accounts; 500K+ = 1,000 advisors × ~500 connections."])
    notes(s, "Backup slide — use only if asked where a number comes from.")

    prs.save(out)
    print("saved", out)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
