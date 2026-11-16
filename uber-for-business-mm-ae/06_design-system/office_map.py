
import sys, json, math
from PIL import Image, ImageDraw, ImageFont
S = sys.argv[1]
ring = json.load(open(f'{S}/geo/mexico.json'))[0]
C = math.cos(math.radians(23)); K = 15.5; X0, Y0 = -117.6, 33.2
P = lambda lon, lat: ((lon - X0) * C * K, (Y0 - lat) * K)
W, H = round(31.3 * C * K), round(19.2 * K)
FS = 17
cities = [('Tijuana', -117.04, 32.51, 10, 6, 'start'), ('Cd. Juárez', -106.42, 31.69, 10, 6, 'start'), ('Monterrey', -100.31, 25.67, 10, 6, 'start'),
          ('Aguascalientes', -102.29, 21.88, -9, -6, 'end'), ('Guadalajara', -103.35, 20.67, -2, 24, 'end'), ('Puerto Vallarta', -105.23, 20.65, -10, 2, 'end'),
          ('Querétaro', -100.39, 20.59, 8, -9, 'start'), ('Mexico City', -99.13, 19.43, 0, 30, 'middle'), ('Puebla', -98.21, 19.04, 10, -1, 'start')]
d = 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in (P(*pt) for pt in ring)) + ' Z'
svg = [f'<svg class="mxmap" viewBox="-6 -10 {W + 40} {H + 16}" role="img" aria-label="Map of Mexico with Salles Sainz Grant Thornton offices in Tijuana, Ciudad Juárez, Monterrey, Aguascalientes, Guadalajara, Puerto Vallarta, Querétaro, Mexico City and Puebla">',
       f'<path d="{d}" fill="var(--line)" stroke="var(--tertiary)" stroke-width="0.8" stroke-linejoin="round"/>']
for n, lon, lat, dx, dy, anc in cities:
    x, y = P(lon, lat)
    svg.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5.5" fill="var(--accent)" stroke="var(--paper)" stroke-width="1.5"/>')
    svg.append(f'<text x="{x + dx:.1f}" y="{y + dy:.1f}" text-anchor="{anc}" font-size="{FS}" font-weight="600" fill="var(--ink)">{n}</text>')
svg.append('</svg>')
open(f'{S}/geo/map.svg', 'w').write('\n'.join(svg))
SC = 6; padL, padT = 6, 10; WW, HH = W + 46, H + 26
img = Image.new('RGBA', (WW * SC, HH * SC), (0, 0, 0, 0)); dr = ImageDraw.Draw(img)
poly = [((x + padL) * SC, (y + padT) * SC) for x, y in (P(*pt) for pt in ring)]
dr.polygon(poly, fill=(226, 226, 226, 255), outline=(150, 150, 150, 255), width=int(0.8 * SC))
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', int(FS * 0.9 * SC))
for n, lon, lat, dx, dy, anc in cities:
    x, y = P(lon, lat); cx, cy = (x + padL) * SC, (y + padT) * SC; r = 5.5 * SC
    dr.ellipse([cx - r - 1.5 * SC, cy - r - 1.5 * SC, cx + r + 1.5 * SC, cy + r + 1.5 * SC], fill=(255, 255, 255, 255))
    dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(39, 110, 241, 255))
    tw = dr.textlength(n, font=font); tx = (x + dx + padL) * SC - (tw if anc == 'end' else tw / 2 if anc == 'middle' else 0); ty = (y + dy + padT) * SC - FS * 0.9 * SC * 0.85
    dr.text((tx, ty), n, fill=(0, 0, 0, 255), font=font)
img = img.resize((img.width // 2, img.height // 2), Image.LANCZOS); img.save(f'{S}/logos/mexico_offices.png'); print(img.size)
