# Hex & Hollow pin: Deck the halls. Ditch the lilies. (redo of holiday-hazards-ranked-for-cats)
# Listing 4618209015, Making Spirits Bright-ish cat Christmas sweatshirt.
# Skeleton c: display headline on top, the sweatshirt photo as a hard-edged full-bleed band through the middle,
# ranked hazard scale below, logo bottom right.
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
OXBLOOD = tuple(int(c * 0.52) for c in RED)         # print red, darkened
BEIGE = tuple(int((0.86 * c + 0.14 * k) * 0.95) for c, k in zip(CREAM, RED))  # field one step down, warmed by the print red

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
BAND_H = 720
band_y = head_bottom + 56
ch = 720
cw = round(ch * W / BAND_H)
cx = 1026
cy0 = 652
box = (cx - cw // 2, cy0, cx - cw // 2 + cw, cy0 + ch)
# the crop must be all garment: nothing near the mockup's white background
lum = a[box[1]:box[3], box[0]:box[2]].mean(axis=2)
assert lum[:, :8].max() < 120 and lum[:, -8:].max() < 120 and lum[:8].max() < 120 and lum[-8:].max() < 120, 'crop hits background'
band = src.crop(box).resize((W, BAND_H), Image.LANCZOS)
img.paste(band, (0, band_y))
band_bottom = band_y + BAND_H

# ---------- ranked scale ----------
items = [
    ('Poinsettia', 'mild upset', BEIGE, INK),
    ('Holly', 'vomiting', RED, CREAM),
    ('Tinsel', 'gut blockage', OXBLOOD, CREAM),
    ('Lilies', 'kidney failure', INK, CREAM),
]
lab = font('inter-latin-500-normal.woff', 30)
ly = band_bottom + 52
d.text((M, ly), 'Mostly fine', font=lab, fill=INK)
em = 'Call the vet'
d.text((W - M - d.textlength(em, font=lab), ly), em, font=lab, fill=RED)
by = ly + 30 + 20
bh = 90
gap = 6
seg = (W - 2 * M - 3 * gap) / 4
nf = font('inter-latin-600-normal.woff', 34)
tf = font('inter-latin-400-normal.woff', 30)
pad = 18
ny = by + bh + 20
for i, (name, note, col, txt) in enumerate(items):
    x0 = M + i * (seg + gap)
    x1 = x0 + seg
    d.rectangle([round(x0), by, round(x1), by + bh], fill=col)
    nb = nf.getbbox('PTL')  # cap height, so every name sits on one baseline
    d.text((x0 + pad, by + (bh - (nb[3] - nb[1])) / 2 - nb[1]), name, font=nf, fill=txt)
    assert d.textlength(name, font=nf) < seg - 2 * pad, name
    d.text((x0, ny), note, font=tf, fill=INK)
    lim = (W - M - x0) if i == 3 else (seg + gap - 20)
    assert d.textlength(note, font=tf) < lim, (note, d.textlength(note, font=tf), lim)
scale_bottom = ny + tf.getbbox('kidney failure')[3]

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
sb = tf.getbbox(srct)
d.text((M, fy + (lh - (sb[3] - sb[1])) / 2 - sb[1]), srct, font=tf, fill=INK)

print('palette', RED, CREAM, FABRIC, OXBLOOD, 'head', head_bottom, 'band', band_y, band_bottom,
      'scale', ly, scale_bottom, 'footer', fy, 'pause', fy - scale_bottom)
img.save(os.environ.get('PIN_OUT', 'out.jpg'), 'JPEG', quality=82, optimize=True)
