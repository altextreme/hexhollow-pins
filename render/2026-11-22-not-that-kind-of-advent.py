# Hex & Hollow topical pin (no product, no link): December's darker folk dates.
# Dec 5 Krampusnacht (Alpine eve of St. Nicholas Day; Krampus carries birch switches),
# Dec 13 St. Lucia Day (Sweden, a crown of candles), Dec 21 2026 winter solstice
# (longest night in the northern hemisphere), Dec 24 the Yule Cat (Iceland: those
# without new clothes for Christmas get eaten). December 2026 starts on a Tuesday.
# Skeleton: drawn month calendar as the hero at the top, blackletter headline below
# it flush left, a 2x2 key under that, logo bottom left. Icons: game-icons, one family.
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from PIL import Image, ImageDraw, ImageFont
from lib.icons import icon

W, H, M = 1000, 1500, 64
FIELD = (21, 41, 34)      # deep spruce
TILE = (34, 60, 50)       # field lifted, for the plain day grid
BONE = (234, 226, 209)
GOLD = (214, 170, 84)     # candle gold, the one accent
DIM = (163, 178, 166)     # spruce-gray for small text

F = 'assets/fonts/'
black = lambda s: ImageFont.truetype(F + 'pirata-one-latin-400-normal.woff', s)
sans = lambda s, w=400: ImageFont.truetype(F + f'inter-latin-{w}-normal.woff', s)

im = Image.new('RGBA', (W, H), FIELD + (255,))
d = ImageDraw.Draw(im)

def text_top(x, y, s, font, fill, anchor_w=None):
    bb = d.textbbox((0, 0), s, font=font)
    if anchor_w is not None:
        x = x + (anchor_w - (bb[2] - bb[0])) / 2
    d.text((x - bb[0], y - bb[1]), s, font=font, fill=fill)
    return y + bb[3] - bb[1]

# --- Calendar ---------------------------------------------------------------
GAP = 8
CW = (W - 2 * M - 6 * GAP) / 7
CH = 116
top = 64
hf = sans(30, 500)
for i, ch in enumerate('SMTWTFS'):
    text_top(M + i * (CW + GAP), top, ch, hf, DIM, anchor_w=CW)
gy = top + 22 + 30
marks = {5: 'gi:devil-mask', 13: 'gi:candles', 21: 'gi:moon', 24: 'gi:cat'}
nf = sans(32, 500)
start = 2  # Tuesday
for day in range(1, 32):
    k = start + day - 1
    r, c = divmod(k, 7)
    x = round(M + c * (CW + GAP)); y = round(gy + r * (CH + GAP))
    x2 = round(M + c * (CW + GAP) + CW)
    if day in marks:
        d.rectangle([x, y, x2, y + CH], fill=GOLD)
        ic = icon(marks[day], 96, FIELD)
        im.alpha_composite(ic, (x + (x2 - x - 96) // 2, y + (CH - 96) // 2))
    else:
        d.rectangle([x, y, x2, y + CH], fill=TILE)
        text_top(x + 14, y + 14, str(day), nf, DIM)
cal_bottom = gy + 5 * CH + 4 * GAP

# --- Headline ---------------------------------------------------------------
bf = black(132)
y = text_top(M, cal_bottom + 58, 'Not that kind', bf, BONE)
y = text_top(M, y + 22, 'of advent', bf, BONE)

# --- Key --------------------------------------------------------------------
keys = [('Dec 5', 'Krampusnacht', 'Krampus brings the birch'),
        ('Dec 13', 'St. Lucia', 'A crown of candles'),
        ('Dec 21', 'Solstice', 'The longest night'),
        ('Dec 24', 'The Yule Cat', 'No new clothes? Dinner')]
kd, kn, kl = sans(30, 600), sans(36, 500), sans(30)
ky0 = y + 46
colw = (W - 2 * M) / 2
rows_y = []
for i, (dt, name, line) in enumerate(keys):
    r, c = divmod(i, 2)
    x = M + c * colw
    base = ky0 + r * 150
    d.text((x, base + 22), dt.upper(), font=kd, fill=GOLD, anchor='ls')
    d.text((x, base + 70), name, font=kn, fill=BONE, anchor='ls')
    d.text((x, base + 112), line, font=kl, fill=DIM, anchor='ls')
    rows_y.append(base + 112 + 8)
key_bottom = max(rows_y)

# --- Footer -----------------------------------------------------------------
logo = Image.open('assets/hh-monogram-white-140.png').convert('RGBA')
LH = 44
logo = logo.resize((round(logo.width * LH / logo.height), LH), Image.LANCZOS)
tint = Image.new('RGBA', logo.size, DIM + (255,)); tint.putalpha(logo.getchannel('A'))
fy = H - 64 - LH
im.alpha_composite(tint, (M, fy))
ff = sans(30, 500)
bb = d.textbbox((0, 0), 'Hex & Hollow', font=ff)
d.text((M + logo.width + 14, fy + (LH - (bb[3] - bb[1])) / 2 - bb[1]), 'Hex & Hollow', font=ff, fill=DIM)
mt = 'December 2026'
bb2 = d.textbbox((0, 0), mt, font=ff)
d.text((W - M - (bb2[2] - bb2[0]) - bb2[0], fy + (LH - (bb[3] - bb[1])) / 2 - bb[1]), mt, font=ff, fill=DIM)
print('cal_bottom', cal_bottom, 'headline_bottom', y, 'key_bottom', key_bottom, 'footer_top', fy)
im.convert('RGB').save(os.environ.get('PIN_OUT', 'out.jpg'), 'JPEG', quality=84, optimize=True)
