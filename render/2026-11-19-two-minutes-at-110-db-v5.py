# "2 minutes at a 110 dB rock concert can cause damage" (Elder Emo Mug: Still Ready for the Pit, listing 4611544912;
# photo = that listing's own second image, photos/4611544912-2.jpg, front and back of the mug on a desk).
# Pass 2, v5, after creative director round 2. Skeleton f: big statement on a light field, the photo as a full-width
# strip at the bottom edge with a hard top edge. The visual: CDC's four time limits on one log time scale.
# Source: CDC Vital Signs, Feb 2017, "Too Loud! For Too Long!": "90dB Leaf blower 2 hours can cause damage",
# "100dB Sporting Event 14 minutes", "110dB Rock concert 2 minutes", "120dB Siren 1 minute".
# Palette from the photo: field = the wall's light gray (213,216,217) lifted a touch; ink = the mug black;
# the one accent = the heart print's crimson (median of its red pixels, #B52527); neutrals from the desk and laptop.
import os, math
from PIL import Image, ImageDraw, ImageFont

W, H, M = 1000, 1500, 64
FIELD = (224, 226, 226)    # wall, lifted
INK   = (28, 28, 30)       # mug black
RED   = (181, 37, 39)      # heart crimson
MUTED = (88, 88, 92)       # laptop gray
AXIS  = (160, 158, 154)    # desk shadow

F = 'assets/fonts/'
osw = lambda w, s: ImageFont.truetype(F + f'oswald-latin-{w}-normal.woff', s)
arc = lambda w, s: ImageFont.truetype(F + f'archivo-latin-{w}-normal.woff', s)

S = 2
im = Image.new('RGB', (W * S, H * S), FIELD)
d = ImageDraw.Draw(im)
def T(x, y, s, font, fill, anchor='ls'):
    d.text((x * S, y * S), s, font=font, fill=fill, anchor=anchor)
def DOT(x, y, r, fill):
    d.ellipse([(x - r) * S, (y - r) * S, (x + r) * S, (y + r) * S], fill=fill)

# Headline: the number is the hero, the CDC sentence finishes it. No period.
T(M, 236, '2 minutes', osw(600, 200 * S), RED)
T(M, 340, 'at a 110 dB rock concert', osw(400, 88 * S), INK)
T(M, 440, 'can cause damage', osw(400, 88 * S), INK)

# Logo, top right, ink
logo = Image.open('assets/hh-monogram-white-140.png').convert('RGBA')
lh = 52 * S; lw = round(logo.width * lh / logo.height)
logo = logo.resize((lw, lh), Image.LANCZOS)
logo = Image.merge('RGBA', (*[Image.new('L', logo.size, c) for c in INK], logo.split()[3]))
im.paste(logo, ((W - M) * S - lw, 64 * S), logo)

# Log time scale, 1 minute to 2 hours
cap = arc(600, 36 * S); nm = arc(600, 50 * S); vl = arc(400, 50 * S)
T(M, 520, 'Time until damage, log scale', cap, MUTED)
x0, x1, ay = 84, 916, 712
X = lambda mins: x0 + (x1 - x0) * math.log(mins) / math.log(120)
d.rectangle([x0 * S, (ay - 5) * S, x1 * S, (ay + 5) * S], fill=AXIS)
for mins in (1, 14, 120):
    DOT(X(mins), ay, 20, INK)
DOT(X(2), ay, 26, RED)
T(M, 600, 'Siren, 120 dB', nm, INK)
T(M, 656, '1 minute', vl, MUTED)
T(W - M, 600, 'Leaf blower, 90 dB', nm, INK, 'rs')
T(W - M, 656, '2 hours', vl, MUTED, 'rs')
T(X(14), 800, 'Sporting event, 100 dB', nm, INK, 'ms')
T(X(14), 856, '14 minutes', vl, MUTED, 'ms')

# Photo strip, full width, hard top edge, bleeds left, right and bottom; mugs and clips 60+ px clear
PY = 900
ph = Image.open('photos/4611544912-2.jpg').convert('RGB').resize((W * S, W * S), Image.LANCZOS)
im.paste(ph.crop((0, 360 * S, W * S, (360 + H - PY) * S)), (0, PY * S))

# Source shares the caption line, right aligned
T(W - M, 520, 'Source: CDC, Feb 2017', arc(400, 32 * S), MUTED, 'rs')

im = im.resize((W, H), Image.LANCZOS)
im.save(os.environ.get('PIN_OUT', '/tmp/pin.jpg'), quality=82, optimize=True, progressive=True)
