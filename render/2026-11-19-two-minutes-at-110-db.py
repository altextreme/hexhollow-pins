# "2 minutes at 110 dB can start to hurt your ears" (Elder Emo: Still Ready for the Pit mug, 4611544912)
# Skeleton f: a single statement led by a giant "2 minutes", a drawn LED level meter (80 to 120 dB) as the one visual,
# and the photo as a full-width strip on the bottom edge (the desk fills the bottom 120 px Pinterest covers).
# Facts: CDC Vital Signs, Feb 2017, "Too Loud! For Too Long!": 85 dB is about where extended exposure can cause
# hearing damage; rock concert 110 dB, 2 minutes can cause damage.
# Palette sampled from photos/4611544912-3.jpg: slate field from the blue-gray wall, headline in the desk's tan,
# the print's red for the loud end of the meter, neutrals from the window light.
import os
from PIL import Image, ImageDraw, ImageFont

W, H, M = 1000, 1500, 64
FIELD = (29, 42, 49)       # the blue-gray wall (#C8D5DB) taken deep
TAN   = (193, 167, 142)    # the wooden desk, #C1A78E
RED   = (169, 79, 80)      # the print's red at its brightest, #A94F50
LIGHT = (232, 236, 237)    # window light, off white
MUTED = (164, 178, 186)    # the wall, a step down
OFF   = (52, 68, 77)       # unlit meter segments, field lifted

F = 'assets/fonts/'
zilla = lambda s: ImageFont.truetype(F + 'zilla-slab-latin-700-normal.woff', s)
plex  = lambda w, s: ImageFont.truetype(F + f'ibm-plex-sans-latin-{w}-normal.woff', s)

S = 2
im = Image.new('RGB', (W * S, H * S), FIELD)
d = ImageDraw.Draw(im)
def T(x, y, s, font, fill, anchor='ls'):
    d.text((x * S, y * S), s, font=font, fill=fill, anchor=anchor)
def R(x0, y0, x1, y1, fill):
    d.rectangle([round(x0 * S), round(y0 * S), round(x1 * S) - 1, round(y1 * S) - 1], fill=fill)

# Logo, top left
logo = Image.open('assets/hh-monogram-white-140.png').convert('RGBA')
lh = 52 * S; lw = round(logo.width * lh / logo.height)
logo = logo.resize((lw, lh), Image.LANCZOS)
logo = Image.merge('RGBA', (*[Image.new('L', logo.size, c) for c in LIGHT], logo.split()[3]))
im.paste(logo, (M * S, M * S), logo)
T(M + lw // S + 16, M + 26, 'Hex & Hollow', plex(600, 30 * S), LIGHT, 'lm')

# Single statement: giant figure, then the rest of the sentence. One color, flush left, no period.
T(M, 330, '2 minutes', zilla(196 * S), TAN)
small = zilla(60 * S)
T(M, 428, 'at 110 dB can start', small, TAN)
T(M, 496, 'to hurt your ears', small, TAN)

# LED level meter, 80 to 120 dB in 2 dB steps, full width between the margins
n, gap = 20, 6
seg = (W - 2 * M - gap * (n - 1)) / n
my0, my1 = 592, 680
def xat(db):
    return M + (db - 80) / 2 * (seg + gap)
for i in range(n):
    db = 80 + 2 * i
    col = MUTED if db < 85 else LIGHT
    if db == 110: col = RED
    if db > 110: col = OFF
    R(xat(db), my0, xat(db) + seg, my1, col)
lab = plex(600, 30 * S)
T(xat(86), 568, 'risk starts', lab, LIGHT, 'ls')
T(xat(110) + seg, 568, 'loud rock show', lab, LIGHT, 'rs')
for db in (80, 90, 100, 110):
    T(xat(db), 724, str(db), lab, MUTED, 'ls')
T(W - M, 724, '120 dB', lab, MUTED, 'rs')

# The payoff line
T(M, 820, 'Earplugs are still punk', plex(400, 40 * S), LIGHT, 'ls')

# Photo: full-width strip on the bottom edge, hard top edge
PY = 900
ph = Image.open('photos/4611544912-3.jpg').convert('RGB')
ph = ph.resize((W * S, round(ph.height * W * S / ph.width)), Image.LANCZOS)
top = 330 * S
im.paste(ph.crop((0, top, W * S, top + (H - PY) * S)), (0, PY * S))

im = im.resize((W, H), Image.LANCZOS)
im.save(os.environ.get('PIN_OUT', '/tmp/pin.jpg'), quality=82, optimize=True, progressive=True)
