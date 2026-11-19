# "Rock concert, 110 dB: 2 minutes can cause damage" (Elder Emo Mug: Still Ready for the Pit, listing 4611544912;
# the photo is that listing's own image, photos/4611544912-3.jpg). Pass 2, v3.
# Skeleton f: photo as a full-width strip on the top edge; a single statement; the hero is a rising bar meter,
# one bar per 5 dB from 80 to 120, evenly spaced, color ramping from neutral to the print's crimson at 110 and up.
# Copy follows CDC Vital Signs, Feb 2017, "Too Loud! For Too Long!" word for word: "110dB Rock concert 2 minutes can
# cause damage"; "85dB is the approximate point at which extended exposure can cause hearing damage."
# Palette from the photo: field = the desk's tan, lifted (#C3AA91 -> #E4D6C8); crimson = the mug print (#932B2F);
# ink = the mug's near-black (#242222); the ramp starts at the desk's shadow tan.
import os
from PIL import Image, ImageDraw, ImageFont

W, H, M = 1000, 1500, 64
FIELD = (228, 214, 200)
RED   = (147, 43, 47)
INK   = (36, 34, 34)
LOW   = (176, 160, 146)    # desk grain in shadow, the quiet end of the ramp

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
def L(x0, y0, x1, y1, fill, w=3):
    d.line([x0 * S, y0 * S, x1 * S, y1 * S], fill=fill, width=w * S)

# Photo strip, top edge: mug clear of both strip edges
PH = 500
ph = Image.open('photos/4611544912-3.jpg').convert('RGB')
ph = ph.resize((W * S, round(ph.height * W * S / ph.width)), Image.LANCZOS)
top = 345 * S
im.paste(ph.crop((0, top, W * S, top + PH * S)), (0, 0))

# Headline: one sentence, CDC's words, broken by phrase, no period
hf = zilla(139)          # sized so line 2 ends on the right margin, x = 936
T(M, 600, 'Rock concert, 110 dB:', hf, RED)
T(M, 684, '2 minutes can cause damage', hf, RED)

# Rising bar meter: 9 bars, 80 to 120 dB, even 5 dB steps across the full measure
dbs = list(range(80, 125, 5))
gap = 16
bw = (W - 2 * M - gap * (len(dbs) - 1)) / len(dbs)
base = 1190
def bh(db): return 70 + (db - 80) / 40 * 330
def bx(i): return M + i * (bw + gap)
def ramp(db):
    t = min(1, max(0, (db - 80) / 30))
    return tuple(round(LOW[k] + (RED[k] - LOW[k]) * t) for k in range(3))
for i, db in enumerate(dbs):
    R(bx(i), base - bh(db), bx(i) + bw, base, ramp(db))

lab = plex(600, 32 * S)
# numbers under the bars that carry meaning, each centered on its bar
for i, db in enumerate(dbs):
    if db in (80, 85, 100, 110, 120):
        T(bx(i) + bw / 2, base + 40, str(db), lab, RED if db == 110 else INK, 'ms')
T(bx(6) + bw / 2, base + 80, 'rock concert', plex(600, 30 * S), RED, 'ms')

# 85 dB note, set above the quiet bars with a leader down to the 85 bar
note = plex(400, 30 * S)
nx, ny = M, 852
for j, line in enumerate(['85 dB: extended exposure', 'can cause hearing damage']):
    T(nx, ny + j * 40, line, note, INK)
cx = bx(1) + bw / 2
L(cx, ny + 58, cx, base - bh(85) - 14, INK, 2)

# Footer: logo left, source right, one baseline, clear of the bottom 120 px
logo = Image.open('assets/hh-monogram-white-140.png').convert('RGBA')
lh = 44 * S; lw = round(logo.width * lh / logo.height)
logo = logo.resize((lw, lh), Image.LANCZOS)
logo = Image.merge('RGBA', (*[Image.new('L', logo.size, c) for c in INK], logo.split()[3]))
fy = 1352                                   # shared baseline
im.paste(logo, (M * S, (fy - 40) * S), logo)
T(M + lw / S + 14, fy, 'Hex & Hollow', plex(600, 30 * S), INK)
T(W - M, fy, 'Source: CDC', plex(400, 30 * S), INK, 'rs')

im = im.resize((W, H), Image.LANCZOS)
im.save(os.environ.get('PIN_OUT', '/tmp/pin.jpg'), quality=82, optimize=True, progressive=True)
