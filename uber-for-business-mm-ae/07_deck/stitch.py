import sys, json, base64, re
S, R, variant = sys.argv[1], sys.argv[2], sys.argv[3]; D = f'{S}/html/deck'
t = open(f'{S}/html/template.html').read()
css = open(f'{D}/deck.css').read()
if variant == 'presenter':
    css += '''
.s-uber { position: absolute; top: var(--pad); right: calc(var(--pad) * 1.15); display: block; line-height: 0; }
.s-uber i { display: inline-block; height: 2.5cqw; aspect-ratio: 715 / 244; background: no-repeat center / contain; }
.s-uber .lb { background-image: var(--uber-b); } .s-uber .lw { background-image: var(--uber-w); aspect-ratio: 640 / 216; }
.s-uber .lw { display: none; }
.slide.inv .s-uber .lb { display: none; } .slide.inv .s-uber .lw { display: inline-block; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) .slide:not(.inv) .s-uber .lb { display: none; } :root:not([data-theme="light"]) .slide:not(.inv) .s-uber .lw { display: inline-block; }
  :root:not([data-theme="light"]) .slide.inv .s-uber .lw { display: none; } :root:not([data-theme="light"]) .slide.inv .s-uber .lb { display: inline-block; } }
:root[data-theme="dark"] .slide:not(.inv) .s-uber .lb { display: none; } :root[data-theme="dark"] .slide:not(.inv) .s-uber .lw { display: inline-block; }
:root[data-theme="dark"] .slide.inv .s-uber .lw { display: none; } :root[data-theme="dark"] .slide.inv .s-uber .lb { display: inline-block; }
.slide .s-client { right: calc(var(--pad) * 1.15 + 9.5cqw); }
@media (max-width: 760px) { .s-uber i { height: 18px; } .slide .s-client { right: calc(var(--pad) + 70px); } }
'''
t = t.replace('</style>', css + '\n</style>', 1)
t = t.replace('<div class="page">\n  <header id="intro">', '''<div class="page">
  <nav class="tabs" role="tablist" aria-label="Views">
    <button type="button" role="tab" data-go="radar" aria-selected="true">Industry radar</button>
    <button type="button" role="tab" data-go="final-deck" aria-selected="false">Final deck</button>
    <button type="button" role="tab" data-go="salles-review" aria-selected="false">Salles Sainz review</button>
    <button type="button" role="tab" data-go="internal-brief" aria-selected="false">Internal brief</button>
  </nav>
  <div class="tabpanel" id="radar" data-tab="radar">
  <header id="intro">''', 1)
i = t.index('</details>') + len('</details>')
decks = open(f'{D}/final.html').read() + open(f'{D}/review.html').read() + open(f'{D}/brief.html').read()
if variant == 'presenter':
    lb = 'data:image/png;base64,' + base64.b64encode(open(f'{S}/logos/logo_black.png', 'rb').read()).decode()
    lw = 'data:image/png;base64,' + base64.b64encode(open(f'{S}/logos/logo_white.png', 'rb').read()).decode()
    tag = '<span class="s-uber" aria-hidden="true"><i class="lb"></i><i class="lw"></i></span>'
    t = t.replace('</style>', f':root {{ --uber-b: url("{lb}"); --uber-w: url("{lw}"); }}\n</style>', 1)
    decks = re.sub(r'(<article class="slide[^"]*" data-title="[^"]+">)', r'\1\n      ' + tag.replace('\\', '\\\\'), decks)
    def b64(n, mime): return f'data:{mime};base64,' + base64.b64encode(open(f'{S}/av/{n}', 'rb').read()).decode()
    kit = '../04_success-plan/launch-kit/'
    def vid(n, poster, label, href):
        return (f'<div class="kit-shot"><video autoplay muted loop playsinline preload="auto" poster="{b64(poster, "image/jpeg")}" aria-label="{label}"><source src="{b64(n, "video/mp4")}" type="video/mp4"></video>'
                f'<a class="kit-open" href="{kit}{href}" target="_blank" rel="noopener">Open ↗</a></div>')
    reps = {
        '<div class="kit-shot" data-kit="webinar"><span>Admin onboarding<br>webinar · mock-up</span></div>': vid('webinar2.mp4', 'webinar2_poster.jpg', 'Admin onboarding webinar mock-up', 'webinar-onboarding.html'),
        '<div class="kit-shot" data-kit="video"><span>Lever videos<br>mock-up · 5 × 15 s</span></div>': vid('levers_all.mp4', 'levers_poster.jpg', 'Lever videos mock-up', 'lever-videos.html'),
        '<div class="kit-shot" data-kit="email"><span>Launch email<br>mock-up</span></div>': vid('email_video.mp4', 'email_poster.jpg', 'Launch email mock-up', 'launch-email-video.html'),
        '<!--bye-logo-->': '<div class="bye-logo" aria-hidden="true"></div>',
        '<!--launchweek-img-->': f'<img class="full-slide" src="{b64("launch_week.jpg", "image/jpeg")}" alt="Launch week: busy season pit stop in the lobby">',
        '<!--intro-logo-->': '<div class="bye-logo intro-logo" aria-hidden="true"></div>',
        '<!--intro-u4b-->': ', Uber for Business',
        '<!--intro-photo--><span class="intro-init" aria-hidden="true">DC</span>': f'<img src="{b64("diego.jpg", "image/jpeg")}" alt="Diego Cuauhtémoc Guerrero">',
    }
    for k, v in reps.items():
        assert k in decks, k; decks = decks.replace(k, v)
m = re.search(r'\n  <section id="scorer">.*?</section>\n', t, re.S); assert m
t = t.replace(m.group(0), '\n', 1)
decks += ('<div class="tabpanel" id="scorer-tab" data-tab="scorer" hidden>\n  <p class="note">Hidden tab (open with #scorer). Prospecting tool kept out of the presentation: the role focuses on adoption.</p>'
          + m.group(0) + '</div>\n')
i = t.index('</details>') + len('</details>')
t = t[:i] + '\n  </div>\n' + decks + t[i:]
t = t.replace('drawRank(); drawHeat();\n</script>', 'drawRank(); drawHeat();\n' + open(f'{D}/deck.js').read() + '\n' + open(f'{D}/bob.js').read() + '\n</script>', 1)
for k, f in [('SEAS','seasonality'),('CEN','census'),('SCORES','scores')]:
    t = t.replace(f'/*{k}*/[]', json.dumps(json.load(open(f'{S}/dash_files/{f}.json'))['rows'], separators=(',',':')))
kw = json.load(open(f'{S}/html/keywords.json')); kw['series'] = [x for x in kw['series'] if x['keyword'] != 'data center queretaro']
t = t.replace('/*KW*/{}', json.dumps(kw, separators=(',',':')))
out = f'{R}/industry-radar.html' if variant == 'public' else f'{R}/industry-radar-presenter.html'
open(out, 'w').write(t); print(out, len(t))
