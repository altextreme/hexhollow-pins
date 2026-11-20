# v2: creative director round 1 fixes (one solid glyph family, ink-normalized icons aligned to the text edge,
# bigger labels, product kicker, heavier display face).
# "Twelve moons, twelve excuses to stay up late" (Emotionally Nocturnal opossum mug, listing 4592258658), Nov 20 2026.
# Manual photo-free icon pin (Anthony asked for an infographic tied to a product with no product photography,
# built from the icon bank). Infographic: the traditional full moon names, one game-icons icon per namesake.
# Names as listed by The Old Farmer's Almanac (almanac.com/full-moon-names); September is its Corn Moon.
# Palette sampled from the mug's print in photos/4592258658-1.jpg: field = the plum-black ground behind the
# opossum, deepened toward aubergine; headline = the opossum's pink nose and ears, lifted; icons = the gold
# stars, lifted; names = the night-blooming flowers' cream; labels = the mauve buds, dimmed.
# One icon family (game-icons, all solid, one color). No headline period: one sentence.
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from lib.icons import icon

W, H, M = 1000, 1500, 72
FIELD = (44, 29, 39)     # plum-black ground of the print, kept clearly aubergine
ROSE = (226, 152, 158)   # opossum nose and ears (#B68D87), lifted for the dark field
GOLD = (222, 186, 118)   # print stars (#A1896A), lifted
CREAM = (238, 228, 210)  # night-blooming flower petals
MAUVE = (176, 150, 158)  # mauve buds, dimmed toward the field

F = 'assets/fonts/'
def f(name, w, s): return ImageFont.truetype(f'{F}{name}-latin-{w}-normal.woff', s)
YS, IN = 'young-serif', 'inter'

im = Image.new('RGBA', (W, H), FIELD + (255,))
d = ImageDraw.Draw(im)

def text_top(xy, s, font, fill, tracking=0):
    """Draw s with its ink top at xy[1]."""
    x, y = xy
    top = d.textbbox((0, 0), s, font=font)[1]
    if not tracking:
        d.text((x, y - top), s, font=font, fill=fill); return
    for ch in s:
        d.text((x, y - top), ch, font=font, fill=fill)
        x += d.textlength(ch, font=font) + tracking

def width(s, font, tracking=0):
    return d.textlength(s, font=font) + tracking * max(len(s) - 1, 0)

# Kicker at the label tier ties the pin to the mug without turning it into an ad.
kf = f(IN, 500, 30)
text_top((M, 76), 'FOR THE EMOTIONALLY NOCTURNAL', kf, MAUVE, tracking=3)

# Headline: friendly display serif (soft humor, like the mug), two balanced phrase lines.
HS = 76
hf = f(YS, 400, HS)
lines = ['Twelve moons, twelve', 'excuses to stay up late']
cap = d.textbbox((0, 0), 'T', font=hf)
asc = cap[3] - cap[1]
y = 134
for ln in lines:
    assert width(ln, hf) <= W - 2 * M, (ln, width(ln, hf))
    text_top((M, y), ln, hf, ROSE)
    y += round(HS * 1.04)
head_bottom = y - round(HS * 1.04) + asc
print('headline baseline ~', head_bottom)

def glyph(iid, box, color, dilate=0):
    """Icon cropped to its ink and scaled so its larger side is box px; dilate thickens a line-drawn glyph."""
    big = icon(iid, 480, color)
    a = big.split()[3]
    if dilate:
        a = a.filter(ImageFilter.MaxFilter(dilate))
    big = Image.merge('RGBA', (*[Image.new('L', big.size, c) for c in color], a))
    big = big.crop(a.getbbox())
    k = box / max(big.size)
    return big.resize((round(big.width * k), round(big.height * k)), Image.LANCZOS)

# Grid: 3 columns x 4 rows, read left to right like a calendar.
MOONS = [
    ('JAN', 'Wolf', 'gi:wolf-head'), ('FEB', 'Snow', 'gi:snowing'), ('MAR', 'Worm', 'gi:earth-worm'),
    ('APR', 'Pink', 'gi:daisy'), ('MAY', 'Flower', 'gi:flowers'), ('JUN', 'Strawberry', 'gi:strawberry'),
    ('JUL', 'Buck', 'gi:deer'), ('AUG', 'Sturgeon', 'gi:double-fish'), ('SEP', 'Corn', 'gi:corn'),
    ('OCT', 'Hunter’s', 'gi:hunting-horn'), ('NOV', 'Beaver', 'gi:beaver'), ('DEC', 'Cold', 'gi:thermometer-cold'),
]
GT = head_bottom + 30 + 58   # descenders, then a clear pause
COLW = (W - 2 * M) // 3
ICON = 102
ROWH = 252
mf = f(IN, 500, 34)
nf = f(YS, 400, 42)
mcap = d.textbbox((0, 0), 'JAN', font=mf); mcap = mcap[3] - mcap[1]
for i, (mon, name, iid) in enumerate(MOONS):
    cx = M + (i % 3) * COLW
    ry = GT + (i // 3) * ROWH
    g = glyph(iid, ICON, GOLD, dilate=13 if iid == 'gi:earth-worm' else 0)
    im.alpha_composite(g, (cx, ry + ICON - g.height))   # ink flush left on the text edge, sitting on one line
    my = ry + ICON + 22
    text_top((cx, my), mon, mf, MAUVE, tracking=3)
    ny = my + mcap + 14
    assert width(name, nf) <= COLW - 24, (name, width(name, nf))
    text_top((cx, ny), name, nf, CREAM)
grid_end = GT + 3 * ROWH + ICON + 22 + mcap + 14 + 42
print('grid end ~', grid_end)

# Footer: logo bottom left, source bottom right, on one baseline band.
logo = Image.open('assets/hh-monogram-white-140.png').convert('RGBA')
lh = 60; lw = round(logo.width * lh / logo.height)
logo = logo.resize((lw, lh), Image.LANCZOS)
logo = Image.merge('RGBA', (*[Image.new('L', logo.size, c) for c in CREAM], logo.split()[3]))
ly = H - 64 - lh
im.alpha_composite(logo, (M, ly))
wf = f(IN, 600, 30)
bb = d.textbbox((0, 0), 'Hex & Hollow', font=wf)
d.text((M + lw + 16, ly + (lh - (bb[3] - bb[1])) // 2 - bb[1]), 'Hex & Hollow', font=wf, fill=CREAM)
sf = f(IN, 400, 32)
src = 'Names: The Old Farmer’s Almanac'
sb = d.textbbox((0, 0), src, font=sf)
d.text((W - M - (sb[2] - sb[0]) - sb[0], ly + (lh - (sb[3] - sb[1])) // 2 - sb[1]), src, font=sf, fill=MAUVE)
print('footer top', ly, 'gap to grid', ly - grid_end)

im.convert('RGB').save(os.environ.get('PIN_OUT', '/tmp/pin.jpg'), quality=82, optimize=True, progressive=True)
