# Hex & Hollow pin: the luna moth mug. "Weeks of waiting, one week of wings"
# Skeleton b: the lifestyle photo is the whole background; a scrim sampled from the photo's own dark
# shadows rises from the bottom edge and carries the headline and a drawn, to-scale life-cycle bar.
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, M = 1000, 1500, 64
OUT = os.environ.get('PIN_OUT', 'pins/out.jpg')
F = 'assets/fonts/'
photo = Image.open('photos/4587785543-1.jpg').convert('RGB')

# Palette, sampled from the photo
src = np.asarray(photo).astype(float)
def med(x0, y0, x1, y1):
    return tuple(int(v) for v in np.median(src[y0:y1, x0:x1].reshape(-1, 3), axis=0))
SHADOW = med(900, 0, 1150, 150)          # the dark room behind the mug, about (48, 23, 17)
FIELD = tuple(int(c * 0.82) for c in SHADOW)
LUNA = (186, 182, 128)                   # the luna moth's wing highlights on the print
LINEN = med(500, 950, 900, 1150)         # the linen cloth, about (196, 194, 192)
DIM = tuple(int(f + (l - f) * 0.62) for f, l in zip(FIELD, LINEN))
SEG = tuple(int(f + (l - f) * 0.30) for f, l in zip(FIELD, LINEN))

# Photo: scale 1.3, mug centred, crop the top 60 px of bokeh
s = 1.3
big = photo.resize((round(1200 * s), round(1200 * s)), Image.LANCZOS)
offx, offy = 480, 60
canvas = big.crop((offx, offy, offx + W, offy + H)).convert('RGB')

# Bottom scrim: straight full-width edge, eased ramp into the sampled shadow color
top, solid = 950, 1110
arr = np.asarray(canvas).astype(float)
ys = np.arange(H)
t = np.clip((ys - top) / (solid - top), 0, 1)
alpha = (t * t * (3 - 2 * t)) * 0.94
arr = arr * (1 - alpha[:, None, None]) + np.array(FIELD)[None, None, :] * alpha[:, None, None]
canvas = Image.fromarray(arr.clip(0, 255).astype('uint8'))
d = ImageDraw.Draw(canvas)

head = ImageFont.truetype(F + 'young-serif-latin-400-normal.woff', 60)
lab = ImageFont.truetype(F + 'dm-sans-latin-500-normal.woff', 30)
small = ImageFont.truetype(F + 'dm-sans-latin-400-normal.woff', 30)

# Headline, two phrases, no period
y = 1146
for line in ['Weeks of waiting,', 'one week of wings']:
    d.text((M, y), line, font=head, fill=LUNA)
    y += 70

# Life-cycle bar, drawn to scale in days (summer brood)
stages = [('Egg', 10, '10 days'), ('Caterpillar', 25, '3 to 4 wk'), ('Cocoon', 17, '2 to 3 wk'), ('Moth', 7, '1 wk')]
total = sum(st[1] for st in stages)
x0, x1 = M, W - M
gap = 6
bar_y, bar_h = 1358, 28
x = x0
avail = (x1 - x0) - gap * (len(stages) - 1)
for i, (name, days, dur) in enumerate(stages):
    w = round(avail * days / total) if i < len(stages) - 1 else x1 - x
    moth = name == 'Moth'
    d.rectangle((x, bar_y, x + w - 1, bar_y + bar_h - 1), fill=LUNA if moth else SEG)
    # label above, duration below, left-aligned to the segment (moth: right-aligned to the margin)
    if moth:
        lw = d.textlength(name, font=lab); dw = d.textlength(dur, font=small)
        d.text((x1 - lw, bar_y - 46), name, font=lab, fill=LUNA)
        d.text((x1 - dw, bar_y + bar_h + 12), dur, font=small, fill=LUNA)
    else:
        d.text((x, bar_y - 46), name, font=lab, fill=LINEN)
        d.text((x, bar_y + bar_h + 12), dur, font=small, fill=DIM)
    x += w + gap

# Logo, top right over the dark bokeh
mono = Image.open('assets/hh-monogram-white-140.png').convert('RGBA')
mono = mono.resize((44, round(44 * mono.height / mono.width)), Image.LANCZOS)
tint = Image.new('RGBA', mono.size, LINEN + (255,)); tint.putalpha(mono.split()[3])
wm = ImageFont.truetype(F + 'dm-sans-latin-500-normal.woff', 30)
text = 'Hex & Hollow'
tw = d.textlength(text, font=wm)
lx = W - M - tw - 14 - mono.width
canvas.paste(tint, (int(lx), M), tint)
bb = d.textbbox((0, 0), text, font=wm)
d.text((W - M - tw, M + (mono.height - (bb[3] - bb[1])) / 2 - bb[1]), text, font=wm, fill=LINEN)

os.makedirs(os.path.dirname(OUT) or '.', exist_ok=True)
canvas.save(OUT, 'JPEG', quality=82, optimize=True)
