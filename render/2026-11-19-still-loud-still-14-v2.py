# Hex & Hollow pin: the Elder Emo Mom "Still loud, just home by ten" sweatshirt, "Still loud, still 14"
# Skeleton b: the 2:3 lifestyle photo is the whole background, edge to edge on all four sides.
# A scrim sampled from the sweatshirt's own black rises from the bottom edge and carries the headline,
# one supporting line and the logo. The printed slogan stays well clear of it.
import os
import colorsys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, M = 1000, 1500, 64
OUT = os.environ.get('PIN_OUT', 'pins/out.jpg')
F = 'assets/fonts/'
photo = Image.open('photos/4619798702-1.jpg').convert('RGB')   # 1024 x 1536 lifestyle photo
src = np.asarray(photo).astype(float)

# Palette, sampled from the photo: the print's red and white, the sweatshirt's black
reg = src[880:1000, 300:760].reshape(-1, 3)[::2] / 255.0
hsv = np.array([colorsys.rgb_to_hsv(*p) for p in reg])
RED = tuple(int(v) for v in np.percentile(reg[((hsv[:, 0] > 0.95) | (hsv[:, 0] < 0.03)) & (hsv[:, 1] > 0.55) & (hsv[:, 2] > 0.45)], 92, axis=0) * 255)
reg2 = src[820:900, 300:760].reshape(-1, 3)[::2] / 255.0
hsv2 = np.array([colorsys.rgb_to_hsv(*p) for p in reg2])
PAPER = tuple(int(v) for v in np.median(reg2[(hsv2[:, 1] < 0.2) & (hsv2[:, 2] > 0.75)], axis=0) * 255)
BLACK = tuple(int(v) for v in np.median(src[1020:1100, 120:300].reshape(-1, 3), axis=0))

canvas = photo.resize((W, H), Image.LANCZOS)

# Bottom scrim: one straight full-width edge, eased ramp into the sweatshirt's black
top, solid = 960, 1110
arr = np.asarray(canvas).astype(float)
t = np.clip((np.arange(H) - top) / (solid - top), 0, 1)
alpha = (t * t * (3 - 2 * t)) * 0.93
arr = arr * (1 - alpha[:, None, None]) + np.array(BLACK)[None, None, :] * alpha[:, None, None]
canvas = Image.fromarray(arr.clip(0, 255).astype('uint8'))
d = ImageDraw.Draw(canvas)

# Logo, centred at the foot
mono = Image.open('assets/hh-monogram-white-140.png').convert('RGBA')
mono = mono.resize((38, round(38 * mono.height / mono.width)), Image.LANCZOS)
tint = Image.new('RGBA', mono.size, PAPER + (255,)); tint.putalpha(mono.split()[3])
wmf = ImageFont.truetype(F + 'dm-sans-latin-500-normal.woff', 30)
text = 'Hex & Hollow'
tw = d.textlength(text, font=wmf)
lx = (W - (mono.width + 12 + tw)) / 2
fy = H - M - mono.height
canvas.paste(tint, (int(lx), fy), tint)
bb = d.textbbox((0, 0), text, font=wmf)
d.text((lx + mono.width + 12, fy + (mono.height - (bb[3] - bb[1])) / 2 - bb[1]), text, font=wmf, fill=PAPER)

# Supporting line, one line, above the logo
body = ImageFont.truetype(F + 'dm-sans-latin-400-normal.woff', 31)
line = 'Spotify data: our most-played hits are from our early teens.'
sb = d.textbbox((0, 0), line, font=body)
sy = fy - 46 - (sb[3] - sb[1]) - sb[1]
d.text((M, sy), line, font=body, fill=PAPER)

# Headline, one line in Anton caps, the print's red, no period, fitted to the measure
size = 116
head = ImageFont.truetype(F + 'anton-latin-400-normal.woff', size)
hl = 'STILL LOUD, STILL 14'
while d.textlength(hl, font=head) > W - 2 * M:
    size -= 2
    head = ImageFont.truetype(F + 'anton-latin-400-normal.woff', size)
cap = d.textbbox((0, 0), 'S', font=head)
hy = sy + sb[1] - 46 - (cap[3] - cap[1]) - cap[1]
d.text((M, hy), hl, font=head, fill=RED)

os.makedirs(os.path.dirname(OUT) or '.', exist_ok=True)
canvas.save(OUT, 'JPEG', quality=84, optimize=True)
