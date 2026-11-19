# Hex & Hollow pin: the Still Growing skull and roses hoodie, "Your skull never quite finishes"
# Type-led field with a product cutout: a huge headline in the print's rose red holds the top of a
# parchment field sampled from the skull art; the hoodie, cut cleanly from its plain white mockup
# (flood-filled background removed, nothing of it kept), anchors the foot.
import os
import colorsys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, M = 1000, 1500, 64
OUT = os.environ.get('PIN_OUT', 'pins/out.jpg')
F = 'assets/fonts/'
photo = Image.open('photos/4611545302-1.jpg').convert('RGB')   # 2048 x 2048, white background
src = np.asarray(photo).astype(float)

# Palette, sampled from the photo
reg = src[750:1200, 850:1250].reshape(-1, 3)[::3] / 255.0
hsv = np.array([colorsys.rgb_to_hsv(*p) for p in reg])
ROSE = tuple(int(v) for v in np.median(reg[((hsv[:, 0] > 0.95) | (hsv[:, 0] < 0.03)) & (hsv[:, 1] > 0.5) & (hsv[:, 2] > 0.35)], axis=0) * 255)
BONE = tuple(int(v) for v in np.median(reg[(hsv[:, 0] > 0.06) & (hsv[:, 0] < 0.17) & (hsv[:, 1] < 0.35) & (hsv[:, 2] > 0.7)], axis=0) * 255)
CHAR = tuple(int(v) for v in np.median(src[1300:1500, 300:500].reshape(-1, 3), axis=0))   # the hoodie's charcoal
FIELD = BONE                                                  # parchment, about (217, 199, 178)
INK = tuple(int(c * 0.80) for c in CHAR)

# Cutout: flood-fill the white background (and its light outline) from the corners, keep the rest
g = src.mean(axis=2)
bg_like = (g > 200).astype('uint8') * 255
seed = Image.fromarray(bg_like).copy()
for c in [(0, 0), (2047, 0), (0, 2047), (2047, 2047)]:
    ImageDraw.floodfill(seed, c, 128)
bgmask = (np.array(seed) == 128)
# Soft edge: near the outline, alpha comes from how far a pixel has moved from the light ground
# toward the hoodie's charcoal, and the colour is un-mixed from that ground, so no halo is left
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
hood = photo.crop(box); ha = alpha.crop(box)

canvas = Image.new('RGB', (W, H), FIELD)
d = ImageDraw.Draw(canvas)

# Headline: three phrase lines, Anton caps, no period
head = ImageFont.truetype(F + 'anton-latin-400-normal.woff', 132)
lines = ['YOUR SKULL', 'NEVER QUITE', 'FINISHES']
asc_top = d.textbbox((0, 0), 'Y', font=head)[1]
y = M - 4 - asc_top
lh = 140
for ln in lines:
    d.text((M, y), ln, font=head, fill=ROSE)
    y += lh
head_bottom = M - 4 + d.textbbox((0, 0), 'F', font=head)[3] - asc_top + lh * 2

# Supporting line
body = ImageFont.truetype(F + 'dm-sans-latin-400-normal.woff', 34)
blines = ['Most of its seams were still open past age 100,', 'a study of head CT scans found.']
by = head_bottom + 40
for bl in blines:
    d.text((M, by), bl, font=body, fill=INK)
    by += 48

# Hoodie, anchored at the foot, centred
hw = 860
sc = hw / hood.width
hh = round(hood.height * sc)
hood = hood.resize((hw, hh), Image.LANCZOS); ha = ha.resize((hw, hh), Image.LANCZOS)
hy = H - M - hh
canvas.paste(hood, ((W - hw) // 2, hy), ha)

# Logo, top right beside the first headline line
mono = Image.open('assets/hh-monogram-white-140.png').convert('RGBA')
mono = mono.resize((40, round(40 * mono.height / mono.width)), Image.LANCZOS)
tint = Image.new('RGBA', mono.size, INK + (255,)); tint.putalpha(mono.split()[3])
wmf = ImageFont.truetype(F + 'dm-sans-latin-500-normal.woff', 30)
text = 'Hex & Hollow'
tw = d.textlength(text, font=wmf)
lx = W - M - tw - 12 - mono.width
ly = M
canvas.paste(tint, (int(lx), ly), tint)
bb = d.textbbox((0, 0), text, font=wmf)
d.text((W - M - tw, ly + (mono.height - (bb[3] - bb[1])) / 2 - bb[1]), text, font=wmf, fill=INK)

os.makedirs(os.path.dirname(OUT) or '.', exist_ok=True)
canvas.save(OUT, 'JPEG', quality=84, optimize=True)
