# Hex & Hollow pin: the luna moth mug, "Weeks of waiting, one week of wings"
# Type-led field with a product cutout: the mug is cut cleanly from its plain white mockup (geometric
# cylinder mask, nothing of the white background kept) and set on a deep field sampled from the print's
# dahlias. Below it, the headline and a drawn, to-scale bar of the luna moth's life cycle.
import os, colorsys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, M = 1000, 1500, 64
OUT = os.environ.get('PIN_OUT', 'pins/out.jpg')
F = 'assets/fonts/'
photo = Image.open('photos/4587785543-2.jpg').convert('RGB')   # 2048 x 2048, white background
src = np.asarray(photo).astype(float)

# Palette, sampled from the print
def hue_pick(y0, y1, x0, x1, test, pct):
    reg = src[y0:y1, x0:x1].reshape(-1, 3)[::5] / 255.0
    hsv = np.array([colorsys.rgb_to_hsv(*p) for p in reg])
    m = test(hsv)
    return tuple(int(v) for v in np.percentile(reg[m], pct, axis=0) * 255)
DAHLIA = hue_pick(600, 1100, 600, 1450, lambda h: ((h[:, 0] > 0.95) | (h[:, 0] < 0.02)) & (h[:, 1] > 0.5) & (h[:, 2] > 0.3), 50)
GOLD = hue_pick(1150, 1500, 700, 1350, lambda h: (h[:, 0] > 0.07) & (h[:, 0] < 0.16) & (h[:, 1] > 0.4) & (h[:, 2] > 0.55), 90)
FIELD = tuple(int(c * 0.84) for c in DAHLIA)                  # deep wine, about (76, 32, 37)
WHITE = tuple(int(v) for v in np.median(src[450:520, 560:640].reshape(-1, 3), axis=0))  # the mug's own white, about 240
BONE = tuple(int(w * 0.94 + g * 0.06) for w, g in zip(WHITE, GOLD))                    # warmed a touch toward the gold
DIM = tuple(int(f + (b - f) * 0.74) for f, b in zip(FIELD, BONE))
SEG = tuple(int(f + (b - f) * 0.22) for f, b in zip(FIELD, BONE))   # field lifted toward the mug white

# Cutout: the mug as a cylinder (rim ellipse + body + base ellipse), measured on the mockup
SS = 2
mask = Image.new('L', (2048 * SS, 2048 * SS), 0)
md = ImageDraw.Draw(mask)
cx, rx = 1022.5, 491
top_cy, top_ry = 441, 103
bot_cy, bot_ry = 1531, 216
k = SS
md.ellipse(((cx - rx) * k, (top_cy - top_ry) * k, (cx + rx) * k, (top_cy + top_ry) * k), fill=255)
md.rectangle(((cx - rx) * k, top_cy * k, (cx + rx) * k, bot_cy * k), fill=255)
md.ellipse(((cx - rx) * k, (bot_cy - bot_ry) * k, (cx + rx) * k, (bot_cy + bot_ry) * k), fill=255)
mask = mask.resize((2048, 2048), Image.LANCZOS)
box = (int(cx - rx) - 2, top_cy - top_ry - 2, int(cx + rx) + 3, bot_cy + bot_ry + 3)
mug = photo.crop(box); mmask = mask.crop(box)

canvas = Image.new('RGB', (W, H), FIELD)
mh = 770
sc = mh / mug.height
mw = round(mug.width * sc)
mug = mug.resize((mw, mh), Image.LANCZOS); mmask = mmask.resize((mw, mh), Image.LANCZOS)
my = 104
canvas.paste(mug, ((W - mw) // 2, my), mmask)
d = ImageDraw.Draw(canvas)

head = ImageFont.truetype(F + 'young-serif-latin-400-normal.woff', 78)
lab = ImageFont.truetype(F + 'dm-sans-latin-500-normal.woff', 36)
small = ImageFont.truetype(F + 'dm-sans-latin-400-normal.woff', 36)
foot = ImageFont.truetype(F + 'dm-sans-latin-400-normal.woff', 30)

# Headline, two phrases, no period
y = 944
for line in ['Weeks of waiting,', 'one week of wings']:
    d.text((M, y), line, font=head, fill=GOLD)
    y += 88

# Life-cycle bar, drawn to scale in days (a summer generation)
stages = [('Egg', 10, '10 days'), ('Caterpillar', 25, '3 to 4 wk'), ('Cocoon', 17, '2 to 3 wk'), ('Moth', 7, '1 wk')]
total = sum(st[1] for st in stages)
x0, x1 = M, W - M
gap = 8
bar_y, bar_h = 1232, 40
x = x0
avail = (x1 - x0) - gap * (len(stages) - 1)
for i, (name, days, dur) in enumerate(stages):
    w = round(avail * days / total) if i < len(stages) - 1 else x1 - x
    moth = name == 'Moth'
    d.rectangle((x, bar_y, x + w - 1, bar_y + bar_h - 1), fill=GOLD if moth else SEG)
    if moth:
        lw = d.textlength(name, font=lab); dw = d.textlength(dur, font=small)
        d.text((x1 - lw, bar_y - 54), name, font=lab, fill=GOLD)
        d.text((x1 - dw, bar_y + bar_h + 14), dur, font=small, fill=GOLD)
    else:
        d.text((x, bar_y - 54), name, font=lab, fill=BONE)
        d.text((x, bar_y + bar_h + 14), dur, font=small, fill=DIM)
    x += w + gap

# Foot: logo centred at the foot
mono = Image.open('assets/hh-monogram-white-140.png').convert('RGBA')
mono = mono.resize((40, round(40 * mono.height / mono.width)), Image.LANCZOS)
tint = Image.new('RGBA', mono.size, BONE + (255,)); tint.putalpha(mono.split()[3])
wmf = ImageFont.truetype(F + 'dm-sans-latin-500-normal.woff', 30)
text = 'Hex & Hollow'
tw = d.textlength(text, font=wmf)
total_w = mono.width + 12 + tw
lx = (W - total_w) / 2
fy = H - M - mono.height
canvas.paste(tint, (int(lx), fy), tint)
bb = d.textbbox((0, 0), text, font=wmf)
d.text((lx + mono.width + 12, fy + (mono.height - (bb[3] - bb[1])) / 2 - bb[1]), text, font=wmf, fill=BONE)

os.makedirs(os.path.dirname(OUT) or '.', exist_ok=True)
canvas.save(OUT, 'JPEG', quality=84, optimize=True)
