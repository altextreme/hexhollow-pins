# Hex & Hollow pin: Holiday hazards, ranked for cats
# Listing 4618209015, Making Spirits Bright-ish cat Christmas sweatshirt.
# Product cutout from the plain-background mockup (photo 4) on a cream field sampled from the print.
# Facts (ASPCA Animal Poison Control): poinsettia is mildly irritating and over-rated in toxicity;
# holly can cause vomiting; swallowed tinsel can block or tangle the gut; lilies can cause kidney failure in cats.
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 1000, 1500
M = 64
F = 'assets/fonts/'


def font(name, size):
    return ImageFont.truetype(F + name, size)


# ---------- product cutout ----------
src = Image.open('photos/4618209015-4.jpg').convert('RGB')
a = np.asarray(src).astype(np.int16)
lum = a.mean(axis=2)
# background is near-white and the mockup shadow is light gray; anything darker than 150 is garment
# (the print sits inside the garment and is kept by the hole fill below)
fg = (lum < 150).astype(np.uint8) * 255
mask = Image.fromarray(fg.astype(np.uint8), 'L')
# fill holes: flood the background from the corners, everything not reached is garment
work = mask.copy()
ImageDraw.floodfill(work, (0, 0), 128)
ImageDraw.floodfill(work, (src.width - 1, 0), 128)
ImageDraw.floodfill(work, (0, src.height - 1), 128)
ImageDraw.floodfill(work, (src.width - 1, src.height - 1), 128)
wa = np.asarray(work)
solid = np.where(wa == 128, 0, 255).astype(np.uint8)
mask = Image.fromarray(solid, 'L')
bbox = mask.getbbox()
garment = src.crop(bbox)
gmask = mask.crop(bbox)

# ---------- palette sampled from the print ----------
pa = a[bbox[1]:bbox[3], bbox[0]:bbox[2]]
r, g, b = pa[..., 0], pa[..., 1], pa[..., 2]
red_px = pa[(r > 140) & (g < 70) & (b < 80)]
cream_px = pa[(r > 200) & (g > 185) & (b > 160) & (r - b > 20)]
RED = tuple(int(v) for v in np.median(red_px, axis=0))
CREAM = tuple(int(v) for v in np.median(cream_px, axis=0))
# field: the print's cream, a touch lighter so the black garment stands hard against it
FIELD = tuple(min(255, c + 6) for c in CREAM)
INK = (34, 26, 24)          # warm near-black from the garment
DEEP = tuple(int(c * 0.55) for c in RED)  # oxblood, the print red darkened
GOLD = (196, 150, 74)       # tree-light gold from the lifestyle photo
GOLD_PALE = (226, 196, 140)

img = Image.new('RGB', (W, H), FIELD)
d = ImageDraw.Draw(img)

# ---------- headline ----------
hf = font('space-grotesk-latin-700-normal.woff', 104)
lines = ['Holiday hazards,', 'ranked for cats']
y = 72
for ln in lines:
    d.text((M - 4, y), ln, font=hf, fill=RED)
    y += 110
head_bottom = y

# ---------- garment ----------
gw = 800
gh = round(garment.height * gw / garment.width)
gimg = garment.resize((gw, gh), Image.LANCZOS)
gm = gmask.resize((gw, gh), Image.LANCZOS)
gx = (W - gw) // 2
gy = head_bottom + 40
img.paste(gimg, (gx, gy), gm)
g_bottom = gy + gh

# ---------- drawn scale ----------
items = [
    ('Poinsettia', 'mild upset', GOLD_PALE),
    ('Holly', 'vomiting', GOLD),
    ('Tinsel', 'gut blockage', RED),
    ('Lilies', 'kidney failure', DEEP),
]
sy = g_bottom + 56
lab = font('inter-latin-600-normal.woff', 30)
d.text((M, sy), 'Mild', font=lab, fill=INK)
em = 'Call the vet'
d.text((W - M - d.textlength(em, font=lab), sy), em, font=lab, fill=DEEP)
by = sy + 48
bh = 36
seg = (W - 2 * M) / 4
gap = 6
for i, (_, _, col) in enumerate(items):
    x0 = M + i * seg + (gap / 2 if i else 0)
    x1 = M + (i + 1) * seg - (gap / 2 if i < 3 else 0)
    d.rectangle([x0, by, x1, by + bh], fill=col)
nf = font('space-grotesk-latin-700-normal.woff', 38)
tf = font('inter-latin-400-normal.woff', 30)
ty = by + bh + 22
for i, (name, note, _) in enumerate(items):
    x0 = M + i * seg + (gap / 2 if i else 0)
    d.text((x0, ty), name, font=nf, fill=INK)
    d.text((x0, ty + 50), note, font=tf, fill=INK)
    assert d.textlength(note, font=tf) < seg - 24 and d.textlength(name, font=nf) < seg - 24
scale_bottom = ty + 50 + 38

# ---------- footer ----------
logo = Image.open('assets/hh-monogram-white-140.png').convert('RGBA')
lh = 56
logo = logo.resize((round(logo.width * lh / logo.height), lh), Image.LANCZOS)
tint = Image.new('RGBA', logo.size, INK + (255,))
tint.putalpha(logo.getchannel('A'))
fy = H - M - lh
img.paste(tint, (M, fy), tint)
wf = font('space-grotesk-latin-500-normal.woff', 32)
d.text((M + logo.width + 16, fy + (lh - 32) // 2 - 4), 'Hex & Hollow', font=wf, fill=INK)
src_t = 'Source: ASPCA'
d.text((W - M - d.textlength(src_t, font=tf), fy + (lh - 30) // 2 - 4), src_t, font=tf, fill=INK)

print('palette', RED, CREAM, FIELD, 'garment', gx, gy, gw, gh, 'scale bottom', scale_bottom, 'footer', fy)
img.save(os.environ.get('PIN_OUT', 'out.jpg'), 'JPEG', quality=82, optimize=True)
