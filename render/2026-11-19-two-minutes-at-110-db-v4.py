# "Rock concert, 110 dB: 2 minutes can cause damage" (Elder Emo Mug: Still Ready for the Pit, listing 4611544912;
# photo = that listing's own third image, photos/4611544912-3.jpg). Pass 2, v4, after creative director round 1.
# Skeleton c (band variant): headline on top, the photo as a full-width band through the middle with hard edges,
# the chart below. Chart = CDC's own time data on one linear time axis (0 to 2 hours), one bar per CDC entry:
# 90 dB 2 hours, 100 dB 14 minutes, 110 dB 2 minutes, 120 dB 1 minute. Only the 110 bar is red.
# Source: CDC Vital Signs, Feb 2017, "Too Loud! For Too Long!" ("110dB Rock concert 2 minutes can cause damage").
# Palette from the photo: field = the shelf's dark wood (#47321F) taken deep; headline = the desk's tan (#C3AA91);
# the one accent = the print's red, light side (#D66E68), used only on the 110 dB row; neutrals = the print's white and the desk grain.
import os
from PIL import Image, ImageDraw, ImageFont

W, H, M = 1000, 1500, 64
FIELD = (42, 29, 20)       # shelf wood, deep
TAN   = (195, 170, 145)    # desk, #C3AA91
RED   = (214, 110, 104)    # print red, light side of its range (between the 75th and 90th percentile reds), 4.9:1 on the field
WHITE = (238, 232, 226)    # print white, warmed
GRAIN = (138, 116, 96)     # desk grain: the neutral bars

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

# Headline: CDC's words, broken by phrase, ends on the right margin, no period
hf = zilla(139)
T(M, 150, 'Rock concert, 110 dB:', hf, TAN)
T(M, 234, '2 minutes can cause damage', hf, TAN)

# Photo band through the middle, full width, hard top and bottom edges, mug clear of both
BY0, BY1 = 300, 820
ph = Image.open('photos/4611544912-3.jpg').convert('RGB')
ph = ph.resize((W * S, round(ph.height * W * S / ph.width)), Image.LANCZOS)
top = 330 * S
im.paste(ph.crop((0, top, W * S, top + (BY1 - BY0) * S)), (0, BY0 * S))

# Time chart: how long until damage can start, linear axis, 0 to 2 hours = 0 to 600 px
lab = plex(600, 32 * S)
val = plex(600, 32 * S)
x0 = 216; full = 600
rows = [('90 dB', 120, '2 hr', GRAIN, WHITE),
        ('100 dB', 14, '14 min', GRAIN, WHITE),
        ('110 dB', 2, '2 min', RED, RED),
        ('120 dB', 1, '1 min', GRAIN, WHITE)]
y = 880; bh = 56; pitch = 100
for name, mins, txt, col, tcol in rows:
    T(M, y + bh / 2, name, lab, RED if mins == 2 else WHITE, 'lm')
    w = max(8, full * mins / 120)
    R(x0, y, x0 + w, y + bh, col)
    T(x0 + w + 18, y + bh / 2, txt, val, tcol, 'lm')
    if mins == 2:
        T(x0 + w + 18 + d.textlength(txt, font=val) / S + 18, y + bh / 2, 'rock concert', plex(400, 32 * S), TAN, 'lm')
    y += pitch

# Footer: logo left, source right, one baseline, clear of the bottom 120 px
logo = Image.open('assets/hh-monogram-white-140.png').convert('RGBA')
lh = 44 * S; lw = round(logo.width * lh / logo.height)
logo = logo.resize((lw, lh), Image.LANCZOS)
logo = Image.merge('RGBA', (*[Image.new('L', logo.size, c) for c in WHITE], logo.split()[3]))
fy = 1356
im.paste(logo, (M * S, (fy - 40) * S), logo)
T(M + lw / S + 14, fy, 'Hex & Hollow', plex(600, 32 * S), WHITE)
T(W - M, fy, 'Source: CDC, Feb 2017', plex(400, 32 * S), WHITE, 'rs')

im = im.resize((W, H), Image.LANCZOS)
im.save(os.environ.get('PIN_OUT', '/tmp/pin.jpg'), quality=82, optimize=True, progressive=True)
