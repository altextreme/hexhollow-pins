# Test of the Render pins action, not a real pin. Exercises photos/, assets/ and assets/fonts/ by relative path
# and the PIN_OUT contract. Run from the repo root.
import os
from PIL import Image, ImageDraw, ImageFont
import numpy as np
W, H, M = 1000, 1500, 64
ph = Image.open('photos/4588636322-1.jpg').convert('RGB')
a = np.asarray(ph.resize((64, 64))).reshape(-1, 3)
dark = tuple(int(v) for v in np.median(a[a.sum(1) < np.percentile(a.sum(1), 25)], 0))
field = tuple(max(0, int(v * 0.55)) for v in dark)
light = tuple(int(v) for v in np.median(a[a.sum(1) > np.percentile(a.sum(1), 75)], 0))
im = Image.new('RGB', (W, H), field)
s = W / ph.width
ph = ph.resize((W, round(ph.height * s)), Image.LANCZOS)
im.paste(ph.crop((0, 0, W, 660)), (0, 0))
d = ImageDraw.Draw(im)
f = ImageFont.truetype('assets/fonts/bebas-neue-latin-400-normal.woff', 120)
g = ImageFont.truetype('assets/fonts/inter-latin-400-normal.woff', 30)
d.text((M, 720), 'RENDER TEST', font=f, fill=light)
d.text((M, 870), 'Photo, fonts and logo all loaded from the repo.', font=g, fill=light)
logo = Image.open('assets/hh-monogram-white-140.png').convert('RGBA').resize((70, 70))
im.paste(logo, (M, H - 56 - 70), logo)
im.save(os.environ.get('PIN_OUT', '/tmp/pin.jpg'), quality=80, optimize=True)
print('field', field, 'light', light)
