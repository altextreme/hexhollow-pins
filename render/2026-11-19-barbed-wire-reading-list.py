# Hex & Hollow pin: Books for a barbed wire heart (tote 4589401466)
# Skeleton d: type-led, huge rose headline on a canvas-cream field, photo as a full-width band at the bottom edge.
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, M = 1000, 1500, 64
F = 'assets/fonts/'
def font(w, s): return ImageFont.truetype(F + f'libre-franklin-latin-{w}-normal.woff', s)

photo = Image.open('photos/4589401466-1.jpg').convert('RGB')
a = np.asarray(photo).astype(int)
def med(x0, y0, x1, y1): return np.median(a[y0:y1, x0:x1].reshape(-1, 3), axis=0)

# Palette from the photo
canvas = med(380, 850, 500, 950)                       # tote canvas
wall = med(420, 20, 560, 100)                          # sunlit wall
field = tuple(int(c) for c in (canvas * 0.55 + wall * 0.45))   # unbleached canvas cream
r = a[600:720, 500:580].reshape(-1, 3)
rose = np.median(r[r[:, 0] > r[:, 1] + 50], axis=0)     # the printed rose
head = tuple(int(c) for c in (rose * np.array([1.0, 0.62, 0.78])))   # same hue, deeper
crate = med(1120, 600, 1240, 900)                       # weathered wood
ink = tuple(int(c * 0.55) for c in crate)               # dark walnut text
mid = tuple(int(c * 0.95) for c in crate)               # wood brown for secondary

img = Image.new('RGB', (W, H), field)
d = ImageDraw.Draw(img)

# Photo band, full width, hard top edge, bleeds off the bottom and both sides
BAND_Y = 930
BAND_H = H - BAND_Y
src_h = int(1254 * BAND_H / W)
top = 196                                   # wall above the tote's hem, heart fully in
crop = photo.crop((0, top, 1254, top + src_h)).resize((W, BAND_H), Image.LANCZOS)
img.paste(crop, (0, BAND_Y))

# Logo top right: monogram tinted to walnut + wordmark
mono = Image.open('assets/hh-monogram-white-140.png').convert('RGBA')
mh = 34
mono = mono.resize((int(mono.width * mh / mono.height), mh), Image.LANCZOS)
tint = Image.new('RGBA', mono.size, ink + (255,))
tint.putalpha(mono.split()[3])
wm = font(700, 24)
wtxt = 'Hex & Hollow'
ww = d.textlength(wtxt, font=wm)
lx = W - M - ww - 12 - mono.width
img.paste(tint, (int(lx), M), tint)
d.text((lx + mono.width + 12, M + mh / 2), wtxt, font=wm, fill=ink, anchor='lm')

# Headline, broken by phrase, pushed toward full width
HS = 106
while ImageFont.truetype(F + 'libre-franklin-latin-900-normal.woff', HS).getbbox('barbed wire heart', anchor='ls')[2] > W - 2 * M:
    HS -= 1
hf = font(900, HS)
lines = ['Books for a', 'barbed wire heart']
LEAD = int(HS * 1.04)
base = 222                                   # first baseline
for i, ln in enumerate(lines):
    d.text((M - hf.getbbox('B', anchor='ls')[0], base + i * LEAD), ln, font=hf, fill=head, anchor='ls')
last_base = base + LEAD * (len(lines) - 1)

# Subhead
sf = font(400, 30)
sy = last_base + 62
d.text((M, sy), 'Four classics that love like it hurts', font=sf, fill=mid, anchor='ls')

# Reading list, one column
books = [
    ('Wuthering Heights', 'Emily Brontë, 1847', 'Love as a weather event.'),
    ('Frankenstein', 'Mary Shelley, 1818', 'Begun at 18, for a ghost-story challenge.'),
    ('Rebecca', 'Daphne du Maurier, 1938', 'The first wife never really leaves.'),
    ('We Have Always Lived in the Castle', 'Shirley Jackson, 1962', 'Two sisters, one sugar bowl.'),
]
tf = font(700, 32)
af = font(400, 25)
numf = font(900, 44)
TX = M + 104
y0 = sy + 52
ROW = 102
for i, (t, au, note) in enumerate(books):
    ry = y0 + i * ROW
    d.line([(M, ry), (W - M, ry)], fill=mid, width=2)
    d.text((M, ry + 24 + 32), f'0{i+1}', font=numf, fill=head, anchor='ls')
    d.text((TX, ry + 24 + 28), t, font=tf, fill=ink, anchor='ls')
    aw = d.textlength(au + '. ', font=af)
    d.text((TX, ry + 24 + 64), au + '.', font=af, fill=mid, anchor='ls')
    d.text((TX + aw, ry + 24 + 64), note, font=af, fill=ink, anchor='ls')
list_end = y0 + len(books) * ROW

out = os.environ.get('PIN_OUT', 'pins/out.jpg')
os.makedirs(os.path.dirname(out), exist_ok=True)
img.save(out, 'JPEG', quality=82, optimize=True)
print(out, HS, y0 + 3 * ROW + 88, field, head, ink, mid, sy, list_end, BAND_Y)
