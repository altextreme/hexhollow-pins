# Hex & Hollow pin: "Your night owl era peaked at 20"
# Product: 4618215666 Elder Emo: Now With Earlier Bedtime crewneck.
# Skeleton: clean cutout of the flat mockup as the hero at the top, headline and subline in the middle,
# a drawn sleep-timing-by-age curve across the bottom third, sources left and monogram right at the foot.
# Palette sampled from the print: heart red deepened for the field (print red 156,17,34),
# letter cream (230,219,209) lifted, garment black (31,31,33) for the peak marker.
# Fact: Roenneberg et al., Current Biology 2004 (25,000 people): sleep timing gets later through adolescence,
# latest at about 19.5 (women) and 20.9 (men), then earlier again. The curve is drawn as a shape, no clock values.
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1000, 1500
M = 64
S = 2  # supersample the line art

FIELD = (124, 16, 30)       # print heart red, deepened
CREAM = (241, 232, 221)     # print cream, lifted
DIM = (222, 178, 172)       # cream over red, for small text
RULE = (176, 92, 98)        # axis hairlines
INK = (31, 31, 33)          # garment black

def font(fam, w, s):
    return ImageFont.truetype(f'assets/fonts/{fam}-latin-{w}-normal.woff', s)

im = Image.new('RGB', (W, H), FIELD)
d = ImageDraw.Draw(im)

def text(s, x, y, f, fill, anchor='l', dr=None):
    dr = dr or d
    bb = dr.textbbox((0, 0), s, font=f)
    w = bb[2] - bb[0]
    if anchor == 'c':
        x = x - w / 2
    elif anchor == 'r':
        x = x - w
    dr.text((x - bb[0], y - bb[1]), s, font=f, fill=fill)
    return (x, y, x + w, y + (bb[3] - bb[1]))

# --- Garment cutout (hero, top) -------------------------------------------------
src = Image.open('photos/4618215666-3.jpg').convert('RGB')
arr = np.asarray(src).astype(int)
# The garment is black, so mark everything darker than the soft gray studio shadow, then fill from the corners:
# whatever the corners can't reach (garment plus its print) is kept.
dark = Image.fromarray(np.where(arr.max(axis=2) < 150, 255, 0).astype(np.uint8), 'L')
dark = dark.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.MinFilter(5))  # close seams and pinholes
cand = dark.copy()
for pt in ((0, 0), (src.width - 1, 0), (0, src.height - 1), (src.width - 1, src.height - 1)):
    ImageDraw.floodfill(cand, pt, 128)
bg = np.asarray(cand) == 128
hard = Image.fromarray(np.where(bg, 0, 255).astype(np.uint8), 'L').copy()
mask = hard.filter(ImageFilter.MinFilter(5)).filter(ImageFilter.GaussianBlur(1.0))
bbox = hard.getbbox()
garment = src.crop(bbox)
gmask = mask.crop(bbox)
GH = 430
GW = round(garment.width * GH / garment.height)
garment = garment.resize((GW, GH), Image.LANCZOS)
gmask = gmask.resize((GW, GH), Image.LANCZOS)
gx = (W - GW) // 2
gy = 64
im.paste(garment, (gx, gy), gmask)
g_bottom = gy + GH

# --- Headline ---------------------------------------------------------------------
HF = font('young-serif', 400, 86)
y = g_bottom + 50
for line in ('Your night owl era', 'peaked at 20'):
    box = text(line, M, y, HF, CREAM)
    y += 104
head_bottom = box[3]

SF = font('dm-sans', 400, 32)
y = head_bottom + 34
for line in ('In a 2004 survey of 25,000 people, sleep timing', 'was latest near 20, then kept getting earlier'):
    box = text(line, M, y, SF, DIM)
    y += 46
sub_bottom = box[3]

# --- Chart --------------------------------------------------------------------------
LF = font('dm-sans', 500, 30)
BF = font('dm-sans', 700, 34)
cx0, cx1 = M + 120, W - M          # plot x range
cy_top, cy_bot = sub_bottom + 150, H - 64 - 44 - 120   # plot y range (above the footer and age labels)

def ax(age):
    return cx0 + (age - 10) / 50 * (cx1 - cx0)

def ay(v):
    return cy_bot - v * (cy_bot - cy_top)

# y-axis labels with a direction arrow
text('Later', M, cy_top - 4, LF, DIM)
text('Earlier', M, cy_bot - 26, LF, DIM)
axx = M + 46
d.line((axx, cy_top + 46, axx, cy_bot - 46), fill=RULE, width=3)
d.polygon([(axx, cy_top + 38), (axx - 9, cy_top + 54), (axx + 9, cy_top + 54)], fill=RULE)
d.polygon([(axx, cy_bot - 38), (axx - 9, cy_bot - 54), (axx + 9, cy_bot - 54)], fill=RULE)

# baseline and age ticks
d.line((cx0, cy_bot + 30, cx1, cy_bot + 30), fill=RULE, width=3)
for age in (10, 20, 30, 40, 50, 60):
    x = ax(age)
    d.line((x, cy_bot + 30, x, cy_bot + 44), fill=RULE, width=3)
    anchor = 'c'
    if age == 60:
        anchor = 'r'
        x = cx1
    if age == 10:
        anchor = 'l'
        x = cx0 - 2
    text(str(age), x, cy_bot + 58, LF, DIM, anchor)
text('Age', M, cy_bot + 58, LF, DIM)

# the curve: a smooth shape through the trend (later to a peak near 20, then earlier)
pts = [(10, 0.34), (12, 0.45), (14, 0.60), (16, 0.76), (18, 0.93), (20, 1.0), (22, 0.985),
       (25, 0.92), (30, 0.79), (35, 0.67), (40, 0.56), (45, 0.46), (50, 0.37), (55, 0.30), (60, 0.24)]
xs = np.array([p[0] for p in pts], float)
vs = np.array([p[1] for p in pts], float)
fine = np.linspace(10, 60, 400)
# monotone-ish smoothing via cubic Catmull-Rom through the points
def catmull(t):
    i = np.searchsorted(xs, t) - 1
    i = int(np.clip(i, 0, len(xs) - 2))
    p0 = vs[max(i - 1, 0)]; p1 = vs[i]; p2 = vs[i + 1]; p3 = vs[min(i + 2, len(vs) - 1)]
    u = (t - xs[i]) / (xs[i + 1] - xs[i])
    return 0.5 * ((2 * p1) + (-p0 + p2) * u + (2 * p0 - 5 * p1 + 4 * p2 - p3) * u * u + (-p0 + 3 * p1 - 3 * p2 + p3) * u ** 3)
curve = [(ax(t), ay(catmull(t))) for t in fine]

big = Image.new('RGBA', (W * S, H * S), (0, 0, 0, 0))
bd = ImageDraw.Draw(big)
fine2 = np.linspace(10, 60, 2400)
rr = 5 * S
for t in fine2:
    x, y = ax(t) * S, ay(catmull(t)) * S
    bd.ellipse((x - rr, y - rr, x + rr, y + rr), fill=CREAM + (255,))
for x, y in (curve[0], curve[-1]):
    r = 5 * S
    bd.ellipse((x * S - r, y * S - r, x * S + r, y * S + r), fill=CREAM + (255,))
# peak marker: black dot ringed in cream
peak_t = fine[int(np.argmax([catmull(t) for t in fine]))]
px, py = ax(peak_t), ay(catmull(peak_t))
r1, r2 = 22 * S, 14 * S
bd.ellipse((px * S - r1, py * S - r1, px * S + r1, py * S + r1), fill=CREAM + (255,))
bd.ellipse((px * S - r2, py * S - r2, px * S + r2, py * S + r2), fill=INK + (255,))
big = big.resize((W, H), Image.LANCZOS)
im.paste(big, (0, 0), big)
d = ImageDraw.Draw(im)

# peak label to the right of the marker
lx = px + 46
b1 = text('Peak night owl', lx, py - 96, BF, CREAM)
b2 = text('Age 19.5 for women, 20.9 for men', lx, b1[3] + 14, LF, DIM)

# --- Footer -----------------------------------------------------------------------
logo = Image.open('assets/hh-monogram-white-140.png').convert('RGBA')
LH = 44
logo = logo.resize((round(logo.width * LH / logo.height), LH), Image.LANCZOS)
tint = Image.new('RGBA', logo.size, DIM + (255,))
tint.putalpha(logo.getchannel('A'))
fy = H - M - LH
im.paste(tint, (W - M - logo.width, fy), tint)
FF = font('dm-sans', 400, 30)
src_line = 'Source: Roenneberg et al., Current Biology, 2004'
sb = d.textbbox((0, 0), src_line, font=FF)
d.text((M - sb[0], fy + (LH - (sb[3] - sb[1])) / 2 - sb[1]), src_line, font=FF, fill=DIM)

print('garment', gx, gy, GW, GH, 'head_bottom', head_bottom, 'sub_bottom', sub_bottom, 'plot', cy_top, cy_bot,
      'peak', round(px), round(py), 'label', b1, b2, 'footer', fy)
out = os.environ.get('PIN_OUT', 'out.jpg')
im.save(out, 'JPEG', quality=82, optimize=True)
