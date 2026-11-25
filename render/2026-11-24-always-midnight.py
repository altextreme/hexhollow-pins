# Hex & Hollow topical pin: below 1,000 m the ocean is always midnight.
# Topical, photo-free, no link. Tall 1000 x 2100 by design: a depth chart drawn to scale,
# surface to the Challenger Deep, as stepped full-width zone bands. Palette chosen for the topic:
# pale sea fog above the surface and on the seafloor, five deepening ocean blues, one
# bioluminescent green accent for the 1,000 m "last light" line only.
# Facts: NOAA JetStream, Layers of the Ocean (sunlight 0 to 200 m, twilight 200 to 1,000 m,
# midnight 1,000 to 4,000 m, abyss 4,000 to 6,000 m, trenches 6,000 m to the bottom).
# NOAA Ocean Service, How far does light travel in the ocean? (light may reach about 1,000 m;
# the aphotic zone is below 1,000 m). Titanic wreck about 3,800 m (12,500 ft).
# NPR, Apr 2023: a snailfish filmed at 8,336 m in the Izu-Ogasawara Trench, the deepest fish
# ever caught on camera. Challenger Deep about 10,935 m (NOAA 2021 measurement).
# Trieste (Jacques Piccard and Don Walsh) first reached the Challenger Deep floor on Jan 23, 1960.
# Icons: game-icons.net by Delapouite (CC BY 3.0): sinking-ship, double-fish (one fish cropped),
# mini-submarine.
import os
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from lib.icons import icon  # noqa: E402

W, H, M = 1000, 2100, 64

FOG = (203, 214, 209)       # pale sea fog: top field and seafloor
INK = (16, 42, 52)          # deep sea ink: headline
INK_DIM = (62, 86, 92)      # small text on fog
BANDS = [                   # (top m, bottom m, color, name, range)
    (0, 200, (72, 146, 148), 'Sunlight', '0 to 200 m'),
    (200, 1000, (37, 96, 108), 'Twilight zone', '200 to 1,000 m'),
    (1000, 4000, (21, 57, 68), 'Midnight zone', '1,000 to 4,000 m'),
    (4000, 6000, (14, 39, 49), 'Abyss', '4,000 to 6,000 m'),
    (6000, 10935, (8, 25, 33), 'Trenches', '6,000 m to the bottom'),
]
PALE = (214, 226, 221)      # labels on water
PALE_DIM = (170, 195, 196)  # ranges on water
GLOW = (126, 224, 191)      # bioluminescent accent: the last light line only

SURF, FLOOR = 760, 1950
PPM = (FLOOR - SURF) / 10935


def Y(m):
    return round(SURF + m * PPM)


def font(fam, wt, size):
    return ImageFont.truetype(f'assets/fonts/{fam}-latin-{wt}-normal.woff', size)


HEAD = font('instrument-serif', 400, 168)
NAME = font('ibm-plex-sans', 600, 32)
BODY = font('ibm-plex-sans', 400, 32)
SMALL = font('ibm-plex-sans', 400, 30)

im = Image.new('RGBA', (W, H), FOG + (255,))
d = ImageDraw.Draw(im)

# ------------------------------------------------------------------ headline on the fog
y = 72
for line in ['Below 1,000 m,', 'it’s always', 'midnight']:
    d.text((M - 6, y), line, font=HEAD, fill=INK)
    last = y
    y += 156
SUB_Y = last + 204 + 40  # the g of midnight reaches about 204 px below its line top (measured)
d.text((M, SUB_Y), 'The ocean drawn to scale, surface to seafloor', font=BODY, fill=INK_DIM)

# ------------------------------------------------------------------ the water
for top, bot, col, name, rng in BANDS:
    d.rectangle([0, Y(top), W, Y(bot) - 1], fill=col)

# sunlight: the band is a sliver, so its label sits on the fog right above it
d.text((M, SURF - 58), 'Sunlight reaches only the top 200 m', font=BODY, fill=INK)

for top, bot, col, name, rng in BANDS[1:]:
    ty = Y(top) + 26
    d.text((M, ty), name, font=NAME, fill=PALE)
    nw = d.textlength(name, font=NAME)
    d.text((M + nw + 16, ty + 1), rng, font=SMALL, fill=PALE_DIM)

# the last light line at 1,000 m
LY = Y(1000)
d.rectangle([0, LY - 2, W, LY + 1], fill=GLOW)
lab = 'Last light, 1,000 m'
d.text((W - M - d.textlength(lab, font=NAME), Y(200) + 26), lab, font=NAME, fill=GLOW)


CW = 164                 # icon column width
TX = W - M - CW - 28     # labels right-align here


def marker(depth, ic, title, sub):
    """A hairline at the exact depth across the right half, icon and label sitting on it."""
    yy = Y(depth)
    x0 = TX - max(d.textlength(title, font=NAME), d.textlength(sub, font=SMALL))
    d.rectangle([x0, yy - 1, W, yy], fill=PALE)  # hairline at the exact depth, label edge to the bleed
    isz = ic.height
    ix = W - M - CW + (CW - ic.width) // 2   # icons centered in one column
    im.alpha_composite(ic, (ix, yy - 14 - isz))
    tx = TX
    d.text((tx - d.textlength(title, font=NAME), yy - 14 - 30 - 46), title, font=NAME, fill=PALE)
    d.text((tx - d.textlength(sub, font=SMALL), yy - 14 - 36), sub, font=SMALL, fill=PALE_DIM)


ship = icon('gi:sinking-ship', 124, PALE)
marker(3800, ship, 'The Titanic', '3,800 m')

two = icon('gi:double-fish', 196, PALE)
bb = two.getbbox()
fish = two.crop((bb[0], two.height // 2 + 4, bb[2], bb[3]))
fish = fish.crop(fish.getbbox())
marker(8336, fish, 'Deepest fish ever filmed', '8,336 m')

# ------------------------------------------------------------------ the seafloor
sub = icon('gi:mini-submarine', 124, PALE)
sx = W - M - CW + (CW - sub.width) // 2
im.alpha_composite(sub, (sx, FLOOR - 14 - sub.height))
t1, t2 = 'Challenger Deep, about 10,935 m', 'First reached by two people in 1960'
d.text((TX - d.textlength(t1, font=NAME), FLOOR - 14 - 30 - 46), t1, font=NAME, fill=PALE)
d.text((TX - d.textlength(t2, font=SMALL), FLOOR - 14 - 36), t2, font=SMALL, fill=PALE_DIM)
d.rectangle([0, FLOOR, W, H], fill=FOG)
FY = FLOOR + (H - FLOOR) // 2
d.text((M, FY - 20), 'Sources: NOAA, NPR', font=SMALL, fill=INK_DIM)
logo = Image.open('assets/hh-monogram-white-140.png').convert('RGBA')
LH = 40
logo = logo.resize((round(logo.width * LH / logo.height), LH), Image.LANCZOS)
tint = Image.new('RGBA', logo.size, INK_DIM + (255,))
tint.putalpha(logo.getchannel('A'))
im.alpha_composite(tint, (W - M - logo.width, FY - 20))

im.convert('RGB').save(os.environ.get('PIN_OUT', 'out.jpg'), quality=82, optimize=True)
