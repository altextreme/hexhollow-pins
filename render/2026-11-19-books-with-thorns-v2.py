# Hex & Hollow pin: Four books with thorns, v2 (barbed wire heart tote 4589401466)
# Skeleton d: type-led on a deep rose field, huge cream headline, the list as a stack of book spines,
# photo as a full-width band on the bottom edge with a hard top edge, logo top left.
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, M = 1000, 1500, 64
F = 'assets/fonts/'
def ff(name, s): return ImageFont.truetype(F + name + '-normal.woff', s)

photo = Image.open('photos/4589401466-1.jpg').convert('RGB')
a = np.asarray(photo).astype(int)
def med(x0, y0, x1, y1): return np.median(a[y0:y1, x0:x1].reshape(-1, 3), axis=0)

# Palette, sampled from the photo
r = a[600:720, 500:580].reshape(-1, 3)
rose = np.median(r[r[:, 0] > r[:, 1] + 50], axis=0)                     # the printed rose
field = tuple(int(c) for c in rose * np.array([0.52, 0.40, 0.48]))       # deep rose field
canvas = med(380, 850, 500, 950)
cream = tuple(int(min(255, c * 1.08)) for c in canvas)                  # tote canvas, lifted
crate = med(1120, 600, 1240, 900)
wood = tuple(int(c * 1.0) for c in crate)                               # weathered wood
walnut = tuple(int(c * 0.5) for c in crate)

img = Image.new('RGB', (W, H), field)
d = ImageDraw.Draw(img)

# Photo band on the bottom edge: full width, hard top edge. Crop keeps the whole heart,
# with a deliberate strip of plant and wall on the left.
BAND_Y = 1000
BAND_H = H - BAND_Y
sx0, sx1 = 200, 1254
sh = int((sx1 - sx0) * BAND_H / W)
sy0 = 650 - sh // 2
band = photo.crop((sx0, sy0, sx1, sy0 + sh)).resize((W, BAND_H), Image.LANCZOS)
img.paste(band, (0, BAND_Y))

# Logo top left, cream
mono = Image.open('assets/hh-monogram-white-140.png').convert('RGBA')
mh = 40
mono = mono.resize((int(mono.width * mh / mono.height), mh), Image.LANCZOS)
tint = Image.new('RGBA', mono.size, cream + (255,))
tint.putalpha(mono.split()[3])
img.paste(tint, (M, M), tint)
wm = ff('inter-latin-600', 32)
d.text((M + mono.width + 14, M + mh / 2), 'Hex & Hollow', font=wm, fill=cream, anchor='lm')

# Headline, pushed to the full measure
hname = 'fraunces-latin-900'
lines = ['Four books', 'with thorns']
HS = 200
while max(ImageFont.truetype(F + hname + '-normal.woff', HS).getbbox(l, anchor='ls')[2] for l in lines) > W - 2 * M:
    HS -= 1
hf = ff(hname, HS)
LEAD = int(HS * 0.98)
cap = -hf.getbbox('F', anchor='ls')[1]
base = M + mh + 64 + cap
for i, ln in enumerate(lines):
    d.text((M - hf.getbbox(ln[0], anchor='ls')[0], base + i * LEAD), ln, font=hf, fill=cream, anchor='ls')
last_base = base + LEAD
desc = hf.getbbox('g', anchor='ls')[3]

# Spines: equal length, alternating wood and canvas, each with its year and its thorn
books = [
    ('Wuthering Heights', '1847', 'Emily Brontë. Love as a weather event.'),
    ('Frankenstein', '1818', 'Mary Shelley, begun at 18. The maker runs.'),
    ('Rebecca', '1938', 'Daphne du Maurier. The first wife stays.'),
    ('We Have Always Lived in the Castle', '1962', 'Shirley Jackson. Mind the sugar bowl.'),
]
tf = ff('inter-latin-600', 40)
nf = ff('inter-latin-400', 32)
SP = 112
y = last_base + desc + 44
for i, (t, yr, note) in enumerate(books):
    bg, fg = (wood, cream) if i % 2 == 0 else (cream, walnut)
    d.rectangle([M, y, W - M - 1, y + SP - 1], fill=bg)
    d.text((M + 36, y + 48), t, font=tf, fill=fg, anchor='ls')
    d.text((W - M - 36, y + 90), yr, font=nf, fill=fg, anchor='rs')
    d.text((M + 36, y + 90), note, font=nf, fill=fg, anchor='ls')
    y += SP
stack_end = y

out = os.environ.get('PIN_OUT', 'pins/out.jpg')
os.makedirs(os.path.dirname(out), exist_ok=True)
img.save(out, 'JPEG', quality=80, optimize=True)
print(out, HS, field, base, last_base, stack_end, BAND_Y, sy0, sh)
