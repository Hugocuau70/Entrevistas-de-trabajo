import sys, json
from PIL import Image, ImageDraw, ImageFont
S = sys.argv[1]; OUT = f'{S}/charts'
F = '/usr/share/fonts/opentype/inter/Inter-%s.otf'
BLACK, GREY, LIGHT, MINT, CARBON, LINE = (0,0,0), (117,117,117), (226,226,226), (164,217,195), (35,43,50), (226,226,226)
DPI = 220
def font(w, px): return ImageFont.truetype(F % w, int(px))
def chart(name, w_in, h_in, cats, vals, hl, fmt, base=0, top=None, pot=None, quota=None, legend=None):
    W, H = int(w_in * DPI), int(h_in * DPI); im = Image.new('RGB', (W, H), (255, 255, 255)); d = ImageDraw.Draw(im)
    fs = 0.034 * H + 9; fv = font('SemiBold', fs); fc = font('Regular', fs)
    pt, pb, pl, pr = (0.16 if legend else 0.11) * H, 0.12 * H, 0.01 * W, 0.01 * W
    allv = vals + (pot or []) + ([quota] if quota else [])
    hi = top or max(allv) * 1.06
    y = lambda v: pt + (H - pt - pb) * (1 - (v - base) / (hi - base))
    n = len(vals); bw = (W - pl - pr) / n
    if legend:
        x0 = pl; 
        for lab, col in legend:
            d.rectangle([x0, 0.03 * H, x0 + fs * .9, 0.03 * H + fs * .9], fill=col); d.text((x0 + fs * 1.3, 0.03 * H - fs * .1), lab, font=fc, fill=GREY); x0 += fs * 1.3 + d.textlength(lab, font=fc) + fs * 1.5
    for i, v in enumerate(vals):
        x = pl + i * bw; a, b = x + bw * .16, x + bw * .84
        if pot is not None:
            d.rounded_rectangle([a, y(pot[i]), b, H - pb], radius=4, fill=LIGHT)
            t = fmt(pot[i]); d.text(((a + b) / 2 - d.textlength(t, font=fc) / 2, y(pot[i]) - fs * 1.35), t, font=fc, fill=GREY)
        col = MINT if (i in hl or pot is not None) else LIGHT
        if v > base: d.rounded_rectangle([a, y(v), b, H - pb], radius=4, fill=col)
        t = fmt(v)
        if pot is not None:
            ty = y(v) + fs * .35 if (H - pb - y(v)) > fs * 1.8 else y(v) - fs * 1.35
            d.text(((a + b) / 2 - d.textlength(t, font=fv) / 2, ty), t, font=fv, fill=BLACK)
        else:
            d.text(((a + b) / 2 - d.textlength(t, font=fv if i in hl else fc) / 2, y(v) - fs * 1.35), t, font=fv if i in hl else fc, fill=BLACK if i in hl else GREY)
        c = cats[i]; d.text(((a + b) / 2 - d.textlength(c, font=fc) / 2, H - pb + fs * .45), c, font=fc, fill=GREY)
    d.line([pl, H - pb, W - pr, H - pb], fill=LINE, width=2)
    if quota:
        yq = y(quota); xx = pl
        while xx < W - pr: d.line([xx, yq, min(xx + 18, W - pr), yq], fill=BLACK, width=3); xx += 30
        d.text((pl + 6, yq - fs * 1.45), 'Quota USD 350K', font=fv, fill=BLACK)
    im.save(f'{OUT}/{name}.png'); print(name, im.size)
seas = {r['row_id']: r for r in json.load(open(f'{S}/dash_files/seasonality.json'))['rows']}
kw = json.load(open(f'{S}/html/keywords.json'))
M = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']; L = list('JFMAMJJASOND')
k = lambda v: f'USD {v:.1f}K'
chart('p4_gb', 8.0, 3.2, ['Jan','Feb','Mar','Apr','May','Jun'], [6.9,12.1,17.3,20.7,22.5,11.4], [], k, pot=[34.6]*5+[16.3], legend=[('Potential', LIGHT), ('Projected', MINT)])
a = seas['5412|people']; chart('p6_audit', 5.7, 2.7, L, [round(a[m], 1) for m in M], [0,1,2], lambda v: f'{v:.0f}', base=94, top=104.5)
tax = next(x for x in kw['series'] if x['keyword'] == 'declaracion anual personas morales'); i0 = kw['months'].index('2025-01')
chart('p6_tax', 5.7, 2.7, L, tax['values'][i0:i0+12], [1,2,3], lambda v: f'{v:,.0f}')
chart('p16_mult', 7.4, 3.9, ['Dec','Jan','Feb','Mar','Apr','May','Jun'], [3.0,2.3,1.65,1.05,0.55,0.2,0.0], [0,1,2], lambda v: (f'{v:.2f}'.rstrip('0').rstrip('.') if v else '0'), top=3.3)
chart('p18_cum', 8.2, 4.0, ['Jan','Feb','Mar','Apr','May','Jun'], [11,38,89,161,251,354], [5], lambda v: f'USD {v:.0f}K', quota=350, top=390)
