# Hex & Hollow pin: Deck the halls. Ditch the lilies. (redo of holiday-hazards-ranked-for-cats; v3 after creative director round 1:
# the scale is now a ranked bar chart, black bars with red kept for the one emergency (lilies),
# band shortened to 620; v4 after round 2: chart title now outranks the row names, source dimmed)
# Listing 4618209015, Making Spirits Bright-ish cat Christmas sweatshirt.
# Skeleton c: display headline on top, the sweatshirt photo as a hard-edged full-bleed band through the middle,
# ranked bar chart below, logo bottom right.
# Same product photo as v1 (photo 4, plain mockup), cropped into the torso so the print is the hero.
# Facts (ASPCA Animal Poison Control): poinsettia is mildly irritating and over-rated in toxicity;
# holly can cause vomiting; swallowed tinsel can block or tangle the gut; lilies can cause kidney failure in cats,
# so the advice is to keep them out of the house, not just out of reach.
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 1000, 1500
M = 64
F = 'assets/fonts/'


def font(name, size):
    return ImageFont.truetype(F + name, size)


src = Image.open('photos/4618209015-4.jpg').convert('RGB')
a = np.asarray(src).astype(np.int16)

# ---------- palette sampled from the print and the garment ----------
pa = a[705:1310, 807:1253]
r, g, b = pa[..., 0], pa[..., 1], pa[..., 2]
RED = tuple(int(v) for v in np.median(pa[(r > 140) & (g < 70) & (b < 80)], axis=0))
CREAM = tuple(int(v) for v in np.median(pa[(r > 200) & (g > 185) & (b > 160) & (r - b > 20)], axis=0))
FABRIC = tuple(int(v) for v in np.median(a[460:640, 820:1240].reshape(-1, 3), axis=0))
FIELD = CREAM
INK = tuple(max(0, c - 4) for c in FABRIC)          # the garment black

GRAY = tuple(round(i + (c - i) * 0.4) for i, c in zip(INK, CREAM))  # metadata gray
img = Image.new('RGB', (W, H), FIELD)
d = ImageDraw.Draw(img)

# ---------- headline (Gloock, display) ----------
hf = font('gloock-latin-400-normal.woff', 124)
lines = ['Deck the halls.', 'Ditch the lilies.']
widest = max(d.textlength(t, font=hf) for t in lines)
assert widest <= W - 2 * M, widest
asc = hf.getbbox('Dh')[1]                           # top of the ascenders
lead = 118
y0 = M - asc
for i, t in enumerate(lines):
    d.text((M - 4, y0 + i * lead), t, font=hf, fill=RED)
head_bottom = y0 + lead + hf.getbbox('Ditch the lilies.')[3]

# ---------- photo band: torso crop, print centered ----------
BAND_H = 620
band_y = head_bottom + 56
ch = 686
cw = round(ch * W / BAND_H)
cx = 1026
cy0 = 663
box = (cx - cw // 2, cy0, cx - cw // 2 + cw, cy0 + ch)
# the crop must be all garment: nothing near the mockup's white background
lum = a[box[1]:box[3], box[0]:box[2]].mean(axis=2)
assert lum[:, :8].max() < 120 and lum[:, -8:].max() < 120 and lum[:8].max() < 120 and lum[-8:].max() < 120, 'crop hits background'
band = src.crop(box).resize((W, BAND_H), Image.LANCZOS)
img.paste(band, (0, band_y))
band_bottom = band_y + BAND_H

# ---------- ranked bar chart: black bars, red only for the emergency ----------
items = [
    ('Poinsettia', 'mild upset', INK),
    ('Holly', 'vomiting', INK),
    ('Tinsel', 'gut blockage', INK),
    ('Lilies', 'kidney failure', RED),
]
lab = font('inter-latin-600-normal.woff', 34)
ly = band_bottom + 52
title = 'If the cat eats it'
tb = lab.getbbox(title)
d.text((M, ly - tb[1]), title, font=lab, fill=INK)
nf = font('inter-latin-500-normal.woff', 34)
tf = font('inter-latin-400-normal.woff', 34)
ncap = nf.getbbox('PTL')
tcap = tf.getbbox('kfl')
bar_x = 280
bt = 40
pitch = 64
out_gap = 18
widest_out = max(d.textlength(o, font=tf) for _, o, _ in items)
unit = (W - M - bar_x - out_gap - widest_out) / 4
ry = ly + (tb[3] - tb[1]) + 36
for i, (name, out, col) in enumerate(items):
    y = ry + i * pitch
    assert M + d.textlength(name, font=nf) < bar_x - 28, name
    d.text((M, y + (bt - (ncap[3] - ncap[1])) / 2 - ncap[1]), name, font=nf, fill=INK)
    x1 = bar_x + unit * (i + 1)
    d.rectangle([bar_x, y, round(x1), y + bt], fill=col)
    d.text((x1 + out_gap, y + (bt - (tcap[3] - tcap[1])) / 2 - tcap[1]), out, font=tf, fill=col)
    assert x1 + out_gap + d.textlength(out, font=tf) <= W - M + 1, out
scale_bottom = ry + 3 * pitch + bt

# ---------- footer ----------
logo = Image.open('assets/hh-monogram-white-140.png').convert('RGBA')
lh = 54
logo = logo.resize((round(logo.width * lh / logo.height), lh), Image.LANCZOS)
tint = Image.new('RGBA', logo.size, INK + (255,))
tint.putalpha(logo.getchannel('A'))
fy = H - M - lh
wf = font('inter-latin-500-normal.woff', 30)
word = 'Hex & Hollow'
ww = d.textlength(word, font=wf)
wx = W - M - ww
lx = round(wx - 14 - logo.width)
img.paste(tint, (lx, fy), tint)
wb = wf.getbbox(word)
d.text((wx, fy + (lh - (wb[3] - wb[1])) / 2 - wb[1]), word, font=wf, fill=INK)
srct = 'Source: ASPCA'
sf = font('inter-latin-400-normal.woff', 30)
sb = sf.getbbox(srct)
d.text((M, fy + (lh - (sb[3] - sb[1])) / 2 - sb[1]), srct, font=sf, fill=GRAY)

print('palette', RED, CREAM, FABRIC, 'unit', round(unit), 'head', head_bottom, 'band', band_y, band_bottom,
      'scale', ly, scale_bottom, 'footer', fy, 'pause', fy - scale_bottom)
img.save(os.environ.get('PIN_OUT', 'out.jpg'), 'JPEG', quality=82, optimize=True)
