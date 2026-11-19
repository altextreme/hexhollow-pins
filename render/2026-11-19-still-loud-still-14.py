# Hex & Hollow pin: the Elder Emo Mom "Still loud, just home by ten" sweatshirt, "Still loud, still 14"
# Type-led field with a product cutout: a huge headline in the print's red holds the top of a pale field
# mixed from the print's white and red; the sweatshirt, cut cleanly from its plain white mockup
# (flood-filled background removed, nothing of it kept), anchors the foot.
import os
import colorsys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, M = 1000, 1500, 64
OUT = os.environ.get('PIN_OUT', 'pins/out.jpg')
F = 'assets/fonts/'
photo = Image.open('photos/4619798702-2.jpg').convert('RGB')   # 2048 x 2048, white background
src = np.asarray(photo).astype(float)

# Palette, sampled from the print
reg = src[700:1150, 700:1350].reshape(-1, 3)[::2] / 255.0
hsv = np.array([colorsys.rgb_to_hsv(*p) for p in reg])
RED = tuple(int(v) for v in np.median(reg[((hsv[:, 0] > 0.95) | (hsv[:, 0] < 0.03)) & (hsv[:, 1] > 0.5) & (hsv[:, 2] > 0.4)], axis=0) * 255)
PAPER = tuple(int(v) for v in np.median(reg[(hsv[:, 1] < 0.15) & (hsv[:, 2] > 0.75)], axis=0) * 255)   # the print's white
CHAR = tuple(int(v) for v in np.median(src[1300:1500, 500:700].reshape(-1, 3), axis=0))              # the sweatshirt's black
FIELD = tuple(int(p * 0.94 + r * 0.06) for p, r in zip(PAPER, RED))   # print white with a breath of its red
INK = tuple(int(c + (f - c) * 0.12) for c, f in zip(CHAR, FIELD))

# Cutout: flood-fill the white background (and its light outline) from the corners, keep the rest
g = src.mean(axis=2)
bg_like = (g > 200).astype('uint8') * 255
seed = Image.fromarray(bg_like).copy()
for c in [(0, 0), (2047, 0), (0, 2047), (2047, 2047)]:
    ImageDraw.floodfill(seed, c, 128)
bgmask = (np.array(seed) == 128)
# Soft edge: near the outline, alpha comes from how far a pixel has moved from the light ground
# toward the garment's black, and the colour is un-mixed from that ground, so no halo is left
hard = Image.fromarray(np.where(bgmask, 0, 255).astype('uint8'))
inner = np.array(hard.filter(ImageFilter.MinFilter(9))) > 0
edge = (~bgmask) & (~inner)
lum_c = float(np.mean(CHAR))
soft = np.clip((200.0 - g) / (200.0 - lum_c), 0, 1)
a = np.where(inner, 1.0, np.where(edge, soft, 0.0))
am = np.clip(a, 0.05, 1)[..., None]
fg = np.where(edge[..., None], np.clip((src - (1 - am) * 225.0) / am, 0, 255), src)
photo = Image.fromarray(fg.astype('uint8'))
alpha = Image.fromarray((a * 255).astype('uint8'))
ys, xs = np.where(~bgmask)
box = (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)
shirt = photo.crop(box); ha = alpha.crop(box)

canvas = Image.new('RGB', (W, H), FIELD)
d = ImageDraw.Draw(canvas)

# Headline: two phrase lines, Anton caps, no period
head = ImageFont.truetype(F + 'anton-latin-400-normal.woff', 176)
lines = ['STILL LOUD,', 'STILL 14']
asc_top = d.textbbox((0, 0), 'Y', font=head)[1]
y = M - 4 - asc_top
lh = 188
for ln in lines:
    d.text((M, y), ln, font=head, fill=RED)
    y += lh
head_bottom = M - 4 + d.textbbox((0, 0), 'S', font=head)[3] - asc_top + lh * 1

# Supporting line
body = ImageFont.truetype(F + 'dm-sans-latin-400-normal.woff', 34)
blines = ['Spotify data on hit songs: men still play the', 'ones released when they were 13 to 16 most.', 'Women, 11 to 14. (New York Times, 2018)']
by = head_bottom + 40
for bl in blines:
    d.text((M, by), bl, font=body, fill=INK)
    by += 48

# Sweatshirt, anchored at the foot, centred
hw = 840
sc = hw / shirt.width
hh = round(shirt.height * sc)
shirt = shirt.resize((hw, hh), Image.LANCZOS); ha = ha.resize((hw, hh), Image.LANCZOS)
hy = H - M - hh
canvas.paste(shirt, ((W - hw) // 2, hy), ha)

# Logo, right of the second headline line, centred on its cap height
mono = Image.open('assets/hh-monogram-white-140.png').convert('RGBA')
mono = mono.resize((40, round(40 * mono.height / mono.width)), Image.LANCZOS)
tint = Image.new('RGBA', mono.size, INK + (255,)); tint.putalpha(mono.split()[3])
wmf = ImageFont.truetype(F + 'dm-sans-latin-500-normal.woff', 30)
text = 'Hex & Hollow'
tw = d.textlength(text, font=wmf)
lx = W - M - tw - 12 - mono.width
cap = d.textbbox((0, 0), 'S', font=head)
line2_mid = M - 4 + lh + (cap[3] - cap[1]) / 2
ly = int(line2_mid - mono.height / 2)
canvas.paste(tint, (int(lx), ly), tint)
bb = d.textbbox((0, 0), text, font=wmf)
d.text((W - M - tw, ly + (mono.height - (bb[3] - bb[1])) / 2 - bb[1]), text, font=wmf, fill=INK)

os.makedirs(os.path.dirname(OUT) or '.', exist_ok=True)
canvas.save(OUT, 'JPEG', quality=84, optimize=True)
