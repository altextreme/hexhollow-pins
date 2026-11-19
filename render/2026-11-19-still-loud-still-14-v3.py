# Hex & Hollow pin: the Elder Emo Mom "Still loud, just home by ten" sweatshirt, "Still loud, still 14"
# Skeleton b: the 2:3 lifestyle photo is the whole background, edge to edge on all four sides.
# A scrim sampled from the sweatshirt's own black rises from a straight full-width line under the print
# and is fully opaque from y 1100 down, so nothing in the photo shows behind the headline, the two short
# supporting lines or the logo. Everything sits flush left on the 64 px margin.
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

# Bottom scrim: one straight full-width edge, eased ramp, fully opaque from y 1100 down
top, solid = 985, 1100
arr = np.asarray(canvas).astype(float)
t = np.clip((np.arange(H) - top) / (solid - top), 0, 1)
alpha = t * t * (3 - 2 * t)
arr = arr * (1 - alpha[:, None, None]) + np.array(BLACK)[None, None, :] * alpha[:, None, None]
canvas = Image.fromarray(arr.clip(0, 255).astype('uint8'))
d = ImageDraw.Draw(canvas)

# Logo, flush left at the foot, on the text axis
mono = Image.open('assets/hh-monogram-white-140.png').convert('RGBA')
mono = mono.resize((38, round(38 * mono.height / mono.width)), Image.LANCZOS)
tint = Image.new('RGBA', mono.size, PAPER + (255,)); tint.putalpha(mono.split()[3])
wmf = ImageFont.truetype(F + 'dm-sans-latin-500-normal.woff', 30)
text = 'Hex & Hollow'
lx = M
fy = H - M - mono.height
canvas.paste(tint, (lx, fy), tint)
bb = d.textbbox((0, 0), text, font=wmf)
d.text((lx + mono.width + 12, fy + (mono.height - (bb[3] - bb[1])) / 2 - bb[1]), text, font=wmf, fill=PAPER)

# Supporting lines, two short lines, clearly narrower than the headline
body = ImageFont.truetype(F + 'dm-sans-latin-400-normal.woff', 34)
blines = ['Spotify data: our most-played hits', 'came out in our early teens.']
xb = d.textbbox((0, 0), 'Sx', font=body)
blh = 48
sy_last = fy - 44 - (xb[3] - xb[1]) - xb[1]
for i, bl in enumerate(reversed(blines)):
    d.text((M, sy_last - i * blh), bl, font=body, fill=PAPER)
sy = sy_last - (len(blines) - 1) * blh

# Headline, one line in Barlow Condensed 800 caps, the print's red, no period, fitted to the measure
size = 116
head = ImageFont.truetype(F + 'barlow-condensed-latin-800-normal.woff', size)
hl = 'STILL LOUD, STILL 14'
while d.textlength(hl, font=head) > W - 2 * M:
    size -= 2
    head = ImageFont.truetype(F + 'barlow-condensed-latin-800-normal.woff', size)
cap = d.textbbox((0, 0), 'S', font=head)
hy = sy + xb[1] - 46 - (cap[3] - cap[1]) - cap[1]
d.text((M, hy), hl, font=head, fill=RED)

os.makedirs(os.path.dirname(OUT) or '.', exist_ok=True)
canvas.save(OUT, 'JPEG', quality=84, optimize=True)
