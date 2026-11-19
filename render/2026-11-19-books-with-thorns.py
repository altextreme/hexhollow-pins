# Hex & Hollow pin: Four books with thorns (barbed wire heart tote 4589401466)
# Skeleton d: photo as a full-width band at the top edge (hard bottom edge), huge headline,
# the reading list drawn as a stack of book spines in colors sampled from the photo, logo centered at the foot.
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, M = 1000, 1500, 64
F = 'assets/fonts/'
def ff(name, s): return ImageFont.truetype(F + name + '-normal.woff', s)

photo = Image.open('photos/4589401466-1.jpg').convert('RGB')
a = np.asarray(photo).astype(int)
def med(x0, y0, x1, y1): return np.median(a[y0:y1, x0:x1].reshape(-1, 3), axis=0)

# Palette, all sampled from the photo
canvas = med(380, 850, 500, 950)                                   # tote canvas
wall = med(420, 20, 560, 100)
field = tuple(int(c) for c in (canvas * 0.55 + wall * 0.45))       # unbleached canvas cream
r = a[600:720, 500:580].reshape(-1, 3)
rose = np.median(r[r[:, 0] > r[:, 1] + 50], axis=0)                 # the printed rose
head = tuple(int(c) for c in (rose * np.array([1.0, 0.62, 0.78])))  # same hue, deeper
crate = med(1120, 600, 1240, 900)                                   # weathered wood
walnut = tuple(int(c * 0.55) for c in crate)
wood = tuple(int(c * 0.95) for c in crate)
wire = tuple(int(c) for c in med(560, 470, 600, 500))               # the wire's ink
moss = tuple(int(c * 0.42) for c in canvas)                       # canvas in deep shadow (taupe)
cream = tuple(int(min(255, c * 1.08)) for c in canvas)

img = Image.new('RGB', (W, H), field)
d = ImageDraw.Draw(img)

# Photo band: full width from the top edge, hard bottom edge. Cropped into the bag body
# (no handles, no crate edge, no window), heart on the band's upper half.
BAND_H = 580
sx0, sx1 = 402, 1254
sh = int((sx1 - sx0) * BAND_H / W)
sy0 = 403
band = photo.crop((sx0, sy0, sx1, sy0 + sh)).resize((W, BAND_H), Image.LANCZOS)
img.paste(band, (0, 0))

# Headline
HS = 128
hname = 'fraunces-latin-900'
lines = ['Four books', 'with thorns']
while max(ImageFont.truetype(F + hname + '-normal.woff', HS).getbbox(l, anchor='ls')[2] for l in lines) > W - 2 * M:
    HS -= 1
hf = ff(hname, HS)
LEAD = int(HS * 1.0)
base = BAND_H + 64 - hf.getbbox('F', anchor='ls')[1]
for i, ln in enumerate(lines):
    d.text((M - hf.getbbox(ln[0], anchor='ls')[0], base + i * LEAD), ln, font=hf, fill=head, anchor='ls')
last_base = base + LEAD * (len(lines) - 1)
desc = hf.getbbox('g', anchor='ls')[3]

# The stack: one spine per book, widths varied on purpose, flush left
books = [
    (['Wuthering Heights'], 'Brontë, 1847', walnut, 872, 88),
    (['Frankenstein'], 'Shelley, 1818', moss, 760, 88),
    (['Rebecca'], 'du Maurier, 1938', wood, 816, 88),
    (['We Have Always Lived', 'in the Castle'], 'Jackson, 1962', wire, 872, 128),
]
tf = ff('inter-latin-600', 36)
af = ff('inter-latin-400', 30)
y = last_base + desc + 48
for tl, au, col, w, SP in books:
    d.rectangle([M, y, M + w - 1, y + SP - 1], fill=col)
    band_col = tuple(int(c * 0.82 + 255 * 0.18) for c in col)   # cloth bands near the spine ends
    for bx in (M + 22, M + w - 30):
        d.rectangle([bx, y + 14, bx + 7, y + SP - 15], fill=band_col)
    n = len(tl)
    for j, t in enumerate(tl):
        d.text((M + 54, y + SP / 2 + (j - (n - 1) / 2) * 42), t, font=tf, fill=cream, anchor='lm')
    d.text((M + w - 54, y + SP / 2), au, font=af, fill=cream, anchor='rm')
    y += SP
stack_end = y

# Logo centered at the foot
mono = Image.open('assets/hh-monogram-white-140.png').convert('RGBA')
mh = 34
mono = mono.resize((int(mono.width * mh / mono.height), mh), Image.LANCZOS)
tint = Image.new('RGBA', mono.size, walnut + (255,))
tint.putalpha(mono.split()[3])
wm = ff('inter-latin-600', 24)
wtxt = 'Hex & Hollow'
tw = mono.width + 12 + d.textlength(wtxt, font=wm)
lx = (W - tw) / 2
ly = H - M - mh
img.paste(tint, (int(lx), ly), tint)
d.text((lx + mono.width + 12, ly + mh / 2), wtxt, font=wm, fill=walnut, anchor='lm')

out = os.environ.get('PIN_OUT', 'pins/out.jpg')
os.makedirs(os.path.dirname(out), exist_ok=True)
img.save(out, 'JPEG', quality=80, optimize=True)
print(out, moss, HS, base, last_base, stack_end, ly)
