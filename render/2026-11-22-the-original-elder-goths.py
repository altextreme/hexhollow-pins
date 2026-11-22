# Topical pin: the oldest known ages of long-lived animals, as columns sunk to scale below a surface line.
# Facts: Ming the ocean quahog, 507 years (Bangor University, Butler et al. 2013); Greenland shark, oldest
# estimated at about 392 years (Nielsen et al., Science 2016); bowhead whale, about 211 years (George et al.,
# Canadian Journal of Zoology 1999); oldest human on record, Jeanne Calment, 122 years (Guinness).
import os, sys
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from lib.icons import icon

W, H = 1000, 1500
M = 64
FIELD = (13, 31, 41)      # abyss blue
SEA = (104, 158, 158)     # sea glass
BONE = (230, 220, 200)
MUTED = (138, 163, 165)
F = 'assets/fonts/'
def font(name, size): return ImageFont.truetype(F + name, size)

im = Image.new('RGBA', (W, H), FIELD + (255,))
d = ImageDraw.Draw(im)

# headline
hf = font('gloock-latin-400-normal.woff', 122)
d.text((M - 4, 64), 'The original', font=hf, fill=BONE)
d.text((M - 4, 196), 'elder goths', font=hf, fill=BONE)
sf = font('inter-latin-400-normal.woff', 36)
d.text((M, 368), 'Oldest known ages, in years', font=sf, fill=MUTED)

# columns
data = [
    ('gi:mussel', 507, 'Ming', 'quahog clam', SEA),
    ('gi:shark-fin', 392, 'Greenland', 'shark, est.', SEA),
    ('gi:whale-tail', 211, 'Bowhead', 'whale, est.', SEA),
    ('gi:person', 122, 'Oldest', 'human', BONE),
]
cw, gap = 170, 64
surface = 640
scale = 470 / 507
nf = font('gloock-latin-400-normal.woff', 76)
lf = font('inter-latin-500-normal.woff', 32)
qf = font('inter-latin-400-normal.woff', 30)
for i, (ic_id, yrs, name, qual, col) in enumerate(data):
    x0 = M + i * (cw + gap)
    cx = x0 + cw // 2
    ic = icon(ic_id, 240, col)
    ic = ic.crop(ic.getbbox())
    k = min(112 / (ic.width * ic.height) ** 0.5, 118 / ic.height)   # even optical size, capped height
    ic = ic.resize((round(ic.width * k), round(ic.height * k)), Image.LANCZOS)
    im.alpha_composite(ic, (cx - ic.width // 2, surface - 28 - ic.height))
    tip = surface + 12 + round(yrs * scale)
    d.rectangle([x0, surface + 12, x0 + cw, tip], fill=col)
    num = str(yrs)
    d.text((cx, tip + 22), num, font=nf, fill=BONE, anchor='mt')
    d.text((cx, tip + 112), name, font=lf, fill=BONE, anchor='mt')
    d.text((cx, tip + 152), qual, font=qf, fill=MUTED, anchor='mt')

# surface line
d.rectangle([M, surface, W - M, surface + 3], fill=MUTED)

# footer
ff = font('inter-latin-400-normal.woff', 30)
d.text((M, H - 64), 'Sources: Bangor, Science, Guinness', font=ff, fill=MUTED, anchor='ls')
mono = Image.open('assets/hh-monogram-white-140.png').convert('RGBA')
mono = mono.resize((round(mono.width * 44 / mono.height), 44), Image.LANCZOS)
r, g, b, a = mono.split()
tint = Image.new('RGBA', mono.size, BONE + (255,)); tint.putalpha(a)
wf = font('inter-latin-500-normal.woff', 30)
wtxt = 'Hex & Hollow'
tw = d.textlength(wtxt, font=wf)
wx = W - M - tw
mx = int(wx - 14 - mono.width)
im.alpha_composite(tint, (mx, H - 64 - 40))
d.text((wx, H - 64), wtxt, font=wf, fill=BONE, anchor='ls')

im.convert('RGB').save(os.environ.get('PIN_OUT', 'pins/out.jpg'), 'JPEG', quality=82, optimize=True)
