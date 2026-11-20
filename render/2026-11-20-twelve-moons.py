# "Twelve moons, twelve excuses to stay up late" (Emotionally Nocturnal opossum mug, listing 4592258658), Nov 20 2026.
# Manual photo-free icon pin (Anthony asked for an infographic tied to a product with no product photography,
# built from the icon bank). Infographic: the traditional full moon names, one game-icons icon per namesake.
# Names as listed by The Old Farmer's Almanac (almanac.com/full-moon-names); September is its Corn Moon.
# Palette sampled from the mug's print in photos/4592258658-1.jpg: field = the plum-black ground behind the
# opossum, deepened toward aubergine; headline = the opossum's pink nose and ears, lifted; icons = the gold
# stars, lifted; names = the night-blooming flowers' cream; labels = the mauve buds, dimmed.
# One icon family (game-icons, all one color). No headline period: one sentence.
import os
from PIL import Image, ImageDraw, ImageFont
from lib.icons import icon

W, H, M = 1000, 1500, 72
FIELD = (44, 29, 39)     # plum-black ground of the print, kept clearly aubergine
ROSE = (226, 152, 158)   # opossum nose and ears (#B68D87), lifted for the dark field
GOLD = (222, 186, 118)   # print stars (#A1896A), lifted
CREAM = (238, 228, 210)  # night-blooming flower petals
MAUVE = (176, 150, 158)  # mauve buds, dimmed toward the field
RULE = (82, 60, 74)      # field lifted, for one hairline

F = 'assets/fonts/'
def f(name, w, s): return ImageFont.truetype(f'{F}{name}-latin-{w}-normal.woff', s)
CG, IN = 'cormorant-garamond', 'inter'

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

# Headline: display serif, two balanced phrase lines, close leading.
hf = f(CG, 700, 96)
lines = ['Twelve moons, twelve', 'excuses to stay up late']
cap = d.textbbox((0, 0), 'T', font=hf)
asc = cap[3] - cap[1]
y = 92
for ln in lines:
    assert width(ln, hf) <= W - 2 * M, (ln, width(ln, hf))
    text_top((M, y), ln, hf, ROSE)
    y += round(96 * 0.94)
head_bottom = y - round(96 * 0.94) + asc + 30  # descender room
print('headline bottom ~', head_bottom)

# Grid: 3 columns x 4 rows, read left to right like a calendar.
MOONS = [
    ('JAN', 'Wolf', 'gi:wolf-howl'), ('FEB', 'Snow', 'gi:snowing'), ('MAR', 'Worm', 'gi:earth-worm'),
    ('APR', 'Pink', 'gi:daisy'), ('MAY', 'Flower', 'gi:flowers'), ('JUN', 'Strawberry', 'gi:strawberry'),
    ('JUL', 'Buck', 'gi:deer'), ('AUG', 'Sturgeon', 'gi:double-fish'), ('SEP', 'Corn', 'gi:corn'),
    ('OCT', 'Hunter’s', 'gi:bow-arrow'), ('NOV', 'Beaver', 'gi:beaver'), ('DEC', 'Cold', 'gi:thermometer-cold'),
]
GT = head_bottom + 84
d.line([M, GT - 42, W - M, GT - 42], fill=RULE, width=2)
COLW = (W - 2 * M) // 3
ROWH = 250
ICON = 104
mf = f(IN, 500, 30)
nf = f(CG, 700, 50)
for i, (mon, name, iid) in enumerate(MOONS):
    cx = M + (i % 3) * COLW
    ry = GT + (i // 3) * ROWH
    ic = icon(iid, ICON, GOLD)
    im.alpha_composite(ic, (cx, ry))
    my = ry + ICON + 20
    text_top((cx, my), mon, mf, MAUVE, tracking=3)
    ny = my + 30 + 10
    assert width(name, nf) <= COLW - 24, (name, width(name, nf))
    text_top((cx, ny), name, nf, CREAM)
grid_end = GT + 3 * ROWH + ICON + 20 + 30 + 10 + 40
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
sf = f(IN, 400, 30)
src = 'Names: The Old Farmer’s Almanac'
sb = d.textbbox((0, 0), src, font=sf)
d.text((W - M - (sb[2] - sb[0]) - sb[0], ly + (lh - (sb[3] - sb[1])) // 2 - sb[1]), src, font=sf, fill=MAUVE)
print('footer top', ly, 'gap to grid', ly - grid_end)

im.convert('RGB').save(os.environ.get('PIN_OUT', '/tmp/pin.jpg'), quality=82, optimize=True, progressive=True)
