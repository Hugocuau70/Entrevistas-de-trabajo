"""Rellena la plantilla oficial de Hootsuite ("Hootsuite Interview Assignment - Slide Deck Template")
con el caso Binance LATAM (post-hackeo del 29 oct 2026).

Uso:
  python3 fill_template.py base.pptx salida.pptx

`base.pptx` = la plantilla exportada de Google Slides, ya reordenada a 10 slides
(1 portada, 2 Who Am I, 3 agenda con tiempos, 12 stats, 15 tres columnas, 12 duplicada,
14 dos columnas, 8 "Listen", 5 divisor, 12 duplicada (mapa de contenidos), 13 bullets). Todo el formato (fuentes Montserrat,
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
        [("Rebuilding trust at the speed of social", {"sz": 30})],
        [("A value proposal for Binance LATAM", {"sz": 20})],
        [("Diego Cuauhtémoc Guerrero  ·  November 2026", {"sz": 14})],
    ])
    notes(s,
          "[0:00–0:30] Thank you all for the time today. For this role play I chose Binance — specifically Binance LATAM: Brazil, Mexico and Argentina. "
          "On October 29 Binance suffered the largest crypto theft on record, about 6.3 billion dollars — and it started with a fake job interview. "
          "So today I'm the one in a job interview, and I promise there's no malware in this deck. "
          "Context: last week I ran discovery with the Director of Social Media for Binance LATAM. Today I'm coming back to show how Hootsuite "
          "helps them protect users and rebuild trust — this is not a feature tour, and Hootsuite is not a cybersecurity product. "
          "It's about the part of the crisis that happens in public, on social.")

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
        [("Why Hootsuite: ", {"b": True}), ("I started my career as a community manager using Hootsuite every day. "
                                            "Today I can pitch it as the tool that turns social listening into business impact.", {})],
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
        ("LAPZO", "Head of Growth · 2026", "118 SQLs and MXN 1.4M in new MRR in one quarter"),
        ("Pinterest", "Sr. Performance Solutions Partner · 2024–26", "Marriott USD 50K → 100K/month with a Brazil + Mexico proposal; Coppel 4.4×"),
        ("Más Gallo Media", "Head of Sales · 2022–24", "USD 1M/month pipeline with Bitso, GBM and Televisa — crypto and fintech from the inside"),
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
          "[0:45–3:00] Quick intro. I'm Diego, based in Mexico City. I'll go from most recent. "
          "Today I lead growth at LAPZO, a B2B SaaS, where my campaigns fed 118 SQLs and 1.4 million pesos in new MRR in a quarter. "
          "Before that, at Pinterest, I doubled Marriott's monthly investment from 50 to 100 thousand dollars with a country-specific proposal "
          "for Brazil and Mexico — the markets that matter most for Binance LATAM. "
          "And before that I was Head of Sales at Más Gallo Media, running full sales cycles with enterprise accounts — including Bitso, "
          "the Mexican crypto exchange, plus GBM and Televisa — about a million dollars a month in pipeline. So I know how crypto and fintech "
          "brands buy, and who sits at the table: marketing, security, legal, procurement. "
          "Why Hootsuite: I actually started my career as a community manager using Hootsuite every day. Today I can pitch it as the tool "
          "that turns social listening into business impact — that's a full circle for me.")

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
        big=["$6.3", "$5.3", "98", "323", "30"],
        small=["B", "B", "%", "M", " min"],
        desc=[
            "stolen on Oct 29 — the largest crypto theft on record, started by a fake job interview",
            "net outflows in the first 3 days after withdrawals reopened (Nov 1–3)",
            "of stolen assets already replenished by Nov 3 — a story competing with fear and rumors",
            "registered users — every one a target for fake ‘compensation’ and ‘priority withdrawal’ scams",
            "Bybit, another exchange hacked for $1.5B in 2025: its CEO posted in ~30 min — today’s bar for crisis response",
        ],
    )
    notes(s,
          "[3:00–7:00] Let me play back what I heard in discovery — tell me if I got anything wrong. "
          "On October 29, hackers took about 6.3 billion dollars from Binance hot wallets — the largest crypto theft on record. "
          "Binance says it began months earlier with a fake job interview and a tampered AI tool; TRM Labs and the FBI point to North Korea's TraderTraitor group. "
          "Binance moved fast on the money: it paused withdrawals, reopened them on November 1, and by November 3 said 98% of stolen assets had been replenished "
          "with its own funds. But trust moves on social, not on-chain: net outflows reached about 5.3 billion dollars in the first three days. "
          "You shared three problems with me. "
          "First, the scam wave. With 323 million registered users, every user is a target: fake support accounts, fake 'compensation' forms, "
          "fake 'withdrawals reopened' posts, 'priority processing' fees. Binance's own co-CEO had to warn users publicly. In LATAM, a lot of it happens "
          "in Spanish and Portuguese, in WhatsApp, Telegram, X and Instagram — and your team finds it manually. "
          "Second, the recovery story isn't landing. 98% replenished is good news, but in the feeds of Brazilian and Mexican users it competes with fear, "
          "rumors and competitors' marketing. You don't have an hourly view of sentiment by country. "
          "Third, speed and control. The benchmark is Bybit's CEO, who posted within about 30 minutes of its 2025 hack and livestreamed soon after. "
          "And in Brazil, Binance just applied for its crypto license — so every public message is now under regulator scrutiny, which means approvals "
          "with Legal can't take days. "
          "I also looked at what you've published since the 29th: the 'Initial Findings' post got two to five times the engagement of the "
          "routine recovery updates — people want the explanation, ideally in their own language (see appendix). "
          "Did I capture that right? Anything you'd add or re-prioritize? [pause]")

    # ---------------- 5 · How Hootsuite helps (three columns) ----------------
    s = S[4]
    fill(tb(s, 191), ["Three outcomes, one Social OS"])
    cols = [
        (184, "Protect users", "Lumen by Talkwalker + Nest",
         "Catch fake support accounts and ‘compensation’ scams in Spanish and Portuguese across 150M+ sources. Alert, warn, request takedowns."),
        (187, "Rebuild trust", "Lumen + Wisdom + Perch",
         "Hourly sentiment by country. Know which rumor is spreading — and publish verified, Legal-approved updates in minutes."),
        (190, "Amplify the truth", "Parliament + Nest",
         "Employees and ambassadors share official updates in one click. One inbox answers users with verified information."),
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
          "[7:00–13:00] Here's how Hootsuite maps to those three outcomes — and to be clear, this doesn't replace your security team; it's the social layer of the crisis. "
          "1 · Protect users. Lumen by Talkwalker monitors over 150 million sources in 187 languages — so we can watch for 'Binance' next to 'compensação', "
          "'reembolso', 'frase semilla', 'retiro prioritario', and for your logo inside scam images. When a fake support account appears, Security and Comms "
          "get an alert in minutes, you warn users from official channels, and you request the takedown. Nest gives Care the verified answer to send. "
          "2 · Rebuild trust. Lumen shows sentiment by country, hour by hour — Brazil is not Mexico. Wisdom, our AI agent, tells you which rumor is "
          "driving the negative spike and what to say. Perch gets that message approved by Legal and Compliance in minutes, not days — "
          "critical while Brazil's central bank reviews your license — and published everywhere at once. "
          "3 · Amplify the truth. Parliament lets employees and community ambassadors share the official update in one click, so the verified "
          "message outnumbers the rumors. And Nest puts every DM and comment in Spanish and Portuguese into one inbox with SLAs. "
          "Which of these three would make the biggest difference for your team in the next 30 days?")

    # ---------------- 6 · Business impact (stats) ----------------
    s = S[5]
    stats_table(
        s, "What success could look like in 90 days",
        big=["<1", "<24", "24", "1", "90"],
        small=["h", "h", "/7", " view", " days"],
        desc=[
            "from the first scam post to an alert and an official warning in Spanish and Portuguese",
            "from fake account detection to takedown request — SIX Group closed 80 unofficial accounts this way",
            "one inbox for BR, MX and AR with SLAs and verified answers drafted by Wisdom",
            "hourly sentiment by country and share of voice vs. Coinbase, OKX, Bybit, Bitso, Mercado Bitcoin",
            "to prove it in a pilot. Targets are illustrative — we set the baselines with your data in week 2",
        ],
    )
    notes(s,
          "[13:00–16:30] What does success look like? These are illustrative targets — we'd set the real baselines with your data. "
          "Under one hour from the first scam post to an alert and an official warning, in Spanish and Portuguese. "
          "Under 24 hours from detecting a fake account to the takedown request — that's the standard SIX Group, the Swiss exchange operator, "
          "reached using Hootsuite as its social compliance hub: 80 unofficial accounts closed. "
          "24/7 coverage for Brazil, Mexico and Argentina in one inbox, with SLAs. "
          "And one view your leadership can trust: sentiment by country, hour by hour, and share of voice versus Coinbase, OKX, Bybit, Bitso and Mercado Bitcoin. "
          "Why it matters in money: outflows were about 5.3 billion dollars in three days. If faster, clearer communication keeps even a fraction "
          "of a percent of that on the platform, the investment pays for itself many times over. "
          "How is your leadership measuring the recovery today?")

    # ---------------- 7 · Path forward (two columns) ----------------
    s = S[6]
    fill(tb(s, 176), ["A 90-day pilot to prove value — then scale"])
    fill(tb(s, 173), ["Live in days, not months — protection first, while the crisis is still unfolding."])
    fill(tb(s, 175), [
        [("Days 1–30 · Protect: ", {"b": True}), ("scam & impersonation radar in ES/PT, alerts to Security and Comms, approvals in Perch", {})],
        [("Days 31–60 · Respond: ", {"b": True}), ("Nest for BR, MX and AR, verified answer library, Wisdom-drafted replies", {})],
        [("Days 61–90 · Rebuild: ", {"b": True}), ("sentiment dashboard by country, Parliament with employees, executive review", {})],
    ], ppr_from=1)
    fill(tb(s, 174), [
        [("This week: ", {"b": True}), ("security & legal review with your InfoSec and Legal teams (Brazil license in mind)", {})],
        [("Week 2: ", {"b": True}), ("set up the scam radar and baselines with Care, Security and Comms", {})],
        [("Week 3: ", {"b": True}), ("pilot proposal and mutual success plan for LATAM leadership", {})],
        [("Does this reflect your priorities? What would make this a “yes” for your leadership?", {"b": True, "i": True})],
    ], ppr_from=1)
    for sid in (174, 175):
        for p in tb(s, sid).findall("a:p", NS):
            for r in p.findall("a:r/a:rPr", NS):
                r.set("sz", "1200")
    notes(s,
          "[16:30–19:30] Because you're still inside the crisis, the pilot is designed to go live in days and protect users first. "
          "Days 1–30, protect: a scam and impersonation radar in Spanish and Portuguese, alerts routed to Security and Comms, and approval workflows "
          "with Legal in Perch. Days 31–60, respond: Nest for Brazil, Mexico and Argentina with a verified answer library and Wisdom-drafted replies. "
          "Days 61–90, rebuild: a sentiment dashboard by country for leadership, Parliament with employees, and an executive review against the targets. "
          "Next steps: this week, a security and legal review with InfoSec and Legal — especially with the Brazilian license under review, let's start there. "
          "Week two, set up the scam radar and baselines with Care, Security and Comms. Week three, a pilot proposal and mutual success plan for LATAM leadership. "
          "So — does this reflect your priorities, and what would make this a 'yes' for your leadership? [stop and listen] "
          "Transition: let me show you what Binance's conversation looks like right now.")

    # ---------------- 8 · Listen (demo divider) ----------------
    s = S[7]
    fill(tb(s, 132), ["Let’s listen: live demo"])
    notes(s,
          "[10-minute demo] 1) Brand pulse: Binance in Spanish and Portuguese since Oct 29 — volume spike, sentiment, top themes. "
          "2) Scam radar: Binance + compensação / reembolso / soporte / frase semilla / retiro prioritario. 3) Sentiment by country: Brazil vs. Mexico vs. Argentina. "
          "4) Share of voice vs. Coinbase, OKX, Bybit, Bitso, Mercado Bitcoin. 5) Ask Wisdom: 'What are the top rumors about the Binance hack in Brazil this week, "
          "and what should we tell users?' Close: 'What would you want to monitor first?' Full script and boolean queries in 04_demo_social_listening.md.")

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

    # ---------------- 10 · Appendix: Binance content map ----------------
    s = S[9]
    stats_table(
        s, "Appendix: what Binance posted after Oct 29",
        big=["602", "300", "123", "117", "3"],
        small=["", "", "", "", " chats"],
        desc=[
            "reactions + 124 reposts — ‘Initial Findings and Response Update’: the post that explains what happened",
            "reactions — Recovery Update #7: 98% of stolen assets replenished + new Proof of Reserves snapshot",
            "reactions — Recovery Update #8: withdrawals reopen for more assets. Routine updates engage less",
            "reactions — ‘Withdrawal data update’: deposits vs. withdrawals chart",
            "official WhatsApp channels: Binance Argentina (ES), Brasil (PT), LATAM (ES), checked via Binance Verify",
        ],
    )
    notes(s,
          "Content map (Binance LinkedIn page as of Nov 6, plus regional channels). Use it in discovery and in the demo. "
          "What they did well: a numbered 'Security Incident | Recovery Update' series on X and LinkedIn (#4 Nov 1 phase-one withdrawals; "
          "#6 Nov 3; #7 Nov 4 98% replenished + Proof of Reserves; #8 Nov 5 more assets), a data post showing deposits vs. withdrawals, "
          "an apology, scam warnings, and regional WhatsApp channels in Spanish and Portuguese. "
          "What the data suggests: the explanatory 'Initial Findings' post got about 602 reactions and 124 reposts — two to five times the routine "
          "updates (300, 123, 117), and engagement on the numbered series is fading. Every post uses the same black 'ANNOUNCEMENT' image, "
          "and the global posts are in English only (LATAM users see 'Show translation'). "
          "Opportunity: localized Spanish/Portuguese versions, a human face or livestream (the Bybit benchmark), dedicated anti-scam creatives, "
          "and listening to learn which update actually reassures each country.")

    # ---------------- 11-15 · Appendix: Lumen screenshots (query "binance") ----------------
    LUMEN_SRC = "Source: Hootsuite Lumen · Quick Search “binance” · 30 Oct – 6 Nov 2026"
    lumen = [
        ("lumen_1_key_metrics.png", "Lumen: 1.3M Binance mentions in one week",
         [[("1.3M results ", {"b": True}), ("(+102%) and ", {}), ("8.1M interactions", {"b": True}), (" in the first week.", {})],
          [("Peak on Oct 30 ", {"b": True}), ("(~470K mentions in a day); Friday hit 32K mentions in a single hour.", {})],
          [("12.7% positive vs. 35.8% negative", {"b": True}), (" — 178.8B potential reach.", {})]],
         "Key Metrics view. Talk track: the crisis is a reach event of historic size — 1.3 million mentions and 8.1 million interactions in a week. "
         "Volume peaked on October 30 and decays every day; the question is what replaces it: fear or the recovery story."),
        ("lumen_2_sentiment.png", "Negative outweighs positive almost 3 to 1",
         [[("Share: ", {"b": True}), ("35.8% negative · 51.5% neutral · 12.7% positive.", {})],
          [("Negative drivers: ", {"b": True}), ("size of the heist, attribution to North Korea, fear for the whole system.", {})],
          [("No positive themes detected", {"b": True}), (" — the 98% recovery isn’t generating positive conversation yet.", {})]],
         "Sentiment view. The AI summary finds three negative drivers — the magnitude of the heist, North Korea attribution, systemic insecurity — "
         "and no documents expressing positive sentiment. That is the gap: Binance's good news (98% replenished) isn't showing up as positive conversation. "
         "Note the spikes around Nov 1 and Nov 2, when withdrawals reopened."),
        ("lumen_3_themes.png", "Themes: the hack drowns Binance’s voice",
         [[("Top themes: ", {"b": True}), ("hack, crypto, billion, North Korea, funds, security.", {})],
          [("binance.com: 2.4K shares", {"b": True}), (" vs. 91.2K links on X (t.co) and Reuters, AP, TradingView.", {})],
          [("#Binance 12.9K posts", {"b": True}), (" (+106%); FBI and Coinbase appear among smart themes.", {})]],
         "Themes view. The word cloud is the narrative: hack, billion, North Korea, funds. Binance's own site was shared 2.4 thousand times "
         "versus 91 thousand links on X and major media — the official source is a small voice in its own crisis."),
        ("lumen_4_results.png", "In LATAM, creators set the narrative",
         [[("Chumel Torres", {"b": True}), (" (MX): “el peor hackeo de la historia” — 48.5K engagement, negative.", {})],
          [("g1 Globo", {"b": True}), (" (BR) in Portuguese; Al Jazeera 73.4K; Watcher.Guru 48.1K on X.", {})],
          [("None of the top posts are Binance’s", {"b": True}), (" — the story is told by others, in ES and PT.", {})]],
         "Results sorted by engagement. The most engaged posts come from media and creators: Al Jazeera, Watcher.Guru — and for LATAM, "
         "Chumel Torres in Mexico and g1 Globo in Brazil. Binance isn't in the top results of its own crisis. This is why localized, "
         "human content and creator relationships matter."),
        ("lumen_5_influencers.png", "X is ~92% of volume, much of it automated",
         [[("137.3K authors", {"b": True}), (" (+112%) across 123.3K sites.", {})],
          [("X: 1.2M of 1.3M results", {"b": True}), ("; then online news 65K, Bluesky 26K, YouTube 9K.", {})],
          [("Top “authors” are automated aggregators", {"b": True}), (" (thebittimes.com) — filter noise to find real voices.", {})]],
         "Influencers view. 137 thousand authors, but the top ones by volume are automated news aggregators — noise. X carries about 92% of results. "
         "With Lumen you filter that out to find the real voices to engage, and the forums like bitcointalk where sentiment is most negative."),
    ]
    for k, (img, title, bullets, note) in enumerate(lumen):
        s = S[10 + k]
        fill(tb(s, 167), [title])
        body_sh = shape(s, 166)
        body_sh.left, body_sh.top = Emu(int(6.05 * 914400)), Emu(int(1.25 * 914400))
        body_sh.width, body_sh.height = Emu(int(3.6 * 914400)), Emu(int(3.7 * 914400))
        fill(body_sh._element.txBody, bullets, ppr_from=1, first_ppr_from=1)
        for p in body_sh._element.txBody.findall("a:p", NS):
            sb = p.find("a:pPr/a:spcBef/a:spcPts", NS)
            if sb is not None:
                sb.set("val", "1200")
            for r in p.findall("a:r/a:rPr", NS):
                r.set("sz", "1200")
        fill(tb(s, 168), [LUMEN_SRC])
        im_path = os.path.join(HERE, "assets", img)
        with Image.open(im_path) as im:
            iw, ih = im.size
        max_w, max_h = 5.6, 3.85
        w_in = min(max_w, max_h * iw / ih)
        h_in = w_in * ih / iw
        pic = s.shapes.add_picture(im_path, Inches(0.25), Inches(1.2), Inches(w_in), Inches(h_in))
        pic.name = "Lumen screenshot"
        pic.line.color.rgb = __import__("pptx").dml.color.RGBColor(0xC9, 0xD3, 0xD0)
        pic.line.width = Pt(0.75)
        notes(s, note + " (Screenshot from my Hootsuite trial — also my backup if the live demo fails.)")

    # ---------------- 10 · Appendix: sources ----------------
    s = S[15]
    fill(tb(s, 167), ["Appendix: where the numbers come from"])
    fill(tb(s, 166), [
        "All Binance and market figures are public; the discovery call is a role-play assumption.",
        "$6.3B stolen on Oct 29, 2026; fake job interview + tampered AI tool — CNBC, NBC News, Washington Post",
        "Withdrawals reopened Nov 1; ~$5.3B net outflows Nov 1–3; 98% replenished — CNBC, FinanceFeeds, CNN",
        "Scam warnings (fake compensation, priority processing) — Binance statements via Bitcoin.com, Crypto Times",
        "323M registered users (Jul 2026) — Binance 9th anniversary release",
        "Benchmark: after its US$1.5B hack (Feb 2025), Bybit’s CEO posted on X within ~30 min, then livestreamed — Cointelegraph, CryptoSlate",
        "Social OS, Wisdom, 150M+ sources, 187 languages — Hootsuite press release, 24 Jun 2026; SIX Group — Hootsuite story",
    ], ppr_from=1, first_ppr_from=0)
    fill(tb(s, 168), ["Impact targets are illustrative and would be baselined with Binance data during the pilot."])
    notes(s, "Backup slide — use only if asked where a number comes from.")

    prs.save(out)
    print("saved", out)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
