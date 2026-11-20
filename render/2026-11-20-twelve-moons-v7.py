# v7: tall review round 1 fixes. One sans family: Archivo (kicker, deck, footer) and Archivo Narrow (dates and
# names), so no two near-identical sans faces stack. Icons sit closer to their labels (12 px) than to their moons
# (28 px). Snow cloud scaled up to match the set. Credit adds the date source (USNO).
# v6 (Nov 19 2026, Anthony: "Redo the moon one taller"): 1000 x 2100, Pinterest's tallest ratio before feed cropping.
# Uses the room for the round 5 notes: spine centered on the page (x 500) with every gold moon on its entry's
# center line; icons sized by optical weight (ink area), not bounding box, so the fish and beaver come up toward
# the others (capped at 110 px on the long side); a plain mitten for the Cold Moon (no heart, no second snowflake);
# names in Archivo Narrow so the longest ("Strawberry Moon") fits a centered spine; headline larger and still in
# the top third.
# v5: creative director round 4 fixes. Each moon now carries its 2027 date (US time; Old Farmer's Almanac names,
# dates cross-checked on printdates.com, moonchildworld.com and pagangrimoire.com: Jan 22, Feb 20, Mar 22,
# Apr 20, May 20, Jun 18, Jul 18, Aug 17, Sep 15, Oct 15, Nov 13, Dec 13). September 2027's moon is the Harvest
# Moon (nearest the Sep 23 equinox), so it is named that, with wheat. Full names ("Hunter's Moon"). April's
# flower takes the headline rose, so the color says "pink".
# v4: one continuous year, a single spine with twelve gold full moons, entries alternating sides. Gloock headline.
# "Twelve moons, twelve excuses to stay up late" (Emotionally Nocturnal opossum mug, listing 4592258658), Nov 20 2026.
# Manual photo-free icon pin (Anthony asked for an infographic tied to a product with no product photography,
# built from the icon bank). One game-icons icon per moon's namesake.
# Names as listed by The Old Farmer's Almanac (almanac.com/full-moon-names); its September name is the Corn
# Moon, and the full moon nearest the autumn equinox is the Harvest Moon.
# Palette sampled from the mug's print in photos/4592258658-1.jpg: ground = the print's warm black, kept
# clearly wine-brown; headline = the opossum's dusty rose nose and ears; icons and names = the night-blooming
# flowers' ivory; labels = the mauve buds, dimmed; moon dots = the gold stars. No headline period.
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from lib.icons import icon

W, H, M = 1000, 2100, 72
FIELD = (52, 37, 41)     # the print's warm black ground, kept a wine-brown
ROSE = (205, 150, 157)   # opossum nose and ears (#B68D87), dusty, lifted for the ground
IVORY = (238, 228, 210)  # night-blooming flower petals
MAUVE = (178, 154, 160)  # mauve buds, dimmed toward the ground
GOLD = (222, 186, 118)   # print stars (#A1896A), lifted; moon dots only
SPINE = (104, 80, 88)    # ground lifted, for the year line

F = 'assets/fonts/'
def f(name, w, s): return ImageFont.truetype(f'{F}{name}-latin-{w}-normal.woff', s)
GL, AR, AN = 'gloock', 'archivo', 'archivo-narrow'

im = Image.new('RGBA', (W, H), FIELD + (255,))
d = ImageDraw.Draw(im)

def ink(s, font):
    b = d.textbbox((0, 0), s, font=font); return b

def text_top(xy, s, font, fill, tracking=0):
    """Draw s with its ink top at xy[1]."""
    x, y = xy
    top = ink(s, font)[1]
    if not tracking:
        d.text((x, y - top), s, font=font, fill=fill); return
    for ch in s:
        d.text((x, y - top), ch, font=font, fill=fill)
        x += d.textlength(ch, font=font) + tracking

def width(s, font, tracking=0):
    return d.textlength(s, font=font) + tracking * max(len(s) - 1, 0)

# Kicker: ties the pin to the mug at the label tier.
kf = f(AR, 600, 34)
text_top((M, 84), 'FOR THE EMOTIONALLY NOCTURNAL', kf, MAUVE, tracking=3)

# Headline: three phrase lines.
HS = 120
hf = f(GL, 400, HS)
capT = ink('T', hf); asc = capT[3] - capT[1]
y = 150
for ln in ['Twelve moons,', 'twelve excuses', 'to stay up late']:
    assert width(ln, hf) <= W - 2 * M
    text_top((M, y), ln, hf, ROSE)
    y += round(HS * 0.98)
base = y - round(HS * 0.98) + asc
print('headline last baseline', base)

# Deck: says what the timeline is.
df = f(AR, 400, 32)
dy = base + 30 + 30
text_top((M, dy), 'Each full moon’s traditional name, with its 2027 US date', df, MAUVE)
deck_bottom = dy + (ink('Eh', df)[3] - ink('Eh', df)[1])
print('deck bottom', deck_bottom)

TARGET = 74      # side of the square with the same ink area, in px: one optical weight for the set
MIN_SIDE, MAX_SIDE = 96, 110

def _finish(big, a, color):
    big = Image.merge('RGBA', (*[Image.new('L', big.size, c) for c in color], a)).crop(a.getbbox())
    a = big.split()[3]
    ink = (sum(i * v for i, v in enumerate(a.histogram())) / 255) ** 0.5   # equivalent square side at source size
    k = TARGET / ink
    k = max(k, MIN_SIDE / max(big.size))   # never under 96 px on the long side
    k = min(k, MAX_SIDE / max(big.size))   # never so big it crowds its neighbours
    return big.resize((round(big.width * k), round(big.height * k)), Image.LANCZOS)

def glyph(iid, color, dilate=0, boost=1.0):
    """Icon cropped to its ink and scaled to one optical weight; dilate fills out a line-drawn glyph."""
    big = icon(iid, 480, color)
    a = big.split()[3]
    if dilate:
        a = a.filter(ImageFilter.MaxFilter(dilate))
    g = _finish(big, a, color)
    if boost != 1.0:   # optical touch-up for a light glyph, still inside the long-side cap
        k = min(boost, MAX_SIDE / max(g.size))
        g = g.resize((round(g.width * k), round(g.height * k)), Image.LANCZOS)
    return g

def glyph_part(iid, color, keep):
    """Like glyph, but keeps only the ink inside the fraction box keep=(x0, y0, x1, y1) of the icon."""
    big = icon(iid, 480, color)
    a = big.split()[3]
    x0, y0, x1, y1 = [round(v * 480) for v in keep]
    mask = Image.new('L', a.size, 0); mask.paste(a.crop((x0, y0, x1, y1)), (x0, y0))
    return _finish(big, mask, color)

ICON = 106   # the slot each icon is centered in
MOONS = [
    ('JAN 22', 'Wolf', glyph('gi:wolf-head', IVORY)),
    ('FEB 20', 'Snow', glyph('gi:snowing', IVORY, boost=1.15)),
    ('MAR 22', 'Worm', glyph('gi:earth-worm', IVORY, 25)),
    ('APR 20', 'Pink', glyph('gi:flower-emblem', ROSE)),
    ('MAY 20', 'Flower', glyph('gi:shut-rose', IVORY)),
    ('JUN 18', 'Strawberry', glyph('gi:strawberry', IVORY)),
    ('JUL 18', 'Buck', glyph('gi:deer', IVORY)),
    ('AUG 17', 'Sturgeon', glyph_part('gi:double-fish', IVORY, (0, 0, 1, 0.5))),
    ('SEP 15', 'Harvest', glyph('gi:wheat', IVORY)),
    ('OCT 15', 'Hunter’s', glyph('gi:archer', IVORY)),
    ('NOV 13', 'Beaver', glyph('gi:beaver', IVORY)),
    ('DEC 13', 'Cold', glyph('gi:winter-gloves', IVORY)),
]

# The year: one spine, twelve moons, entries alternating left and right of it.
SX = W // 2                   # spine, centered on the page
R = 17                       # moon radius
FOOT = H - 64 - 60           # footer band top
CY0 = deck_bottom + 90 + 60
CY1 = FOOT - 70 - 60
STEP = (CY1 - CY0) / 11
d.line([SX, CY0, SX, CY1], fill=SPINE, width=3)
mf = f(AN, 500, 32)
nf = f(AN, 700, 39)
mcap = ink('JAN', mf); mcap = mcap[3] - mcap[1]
ncap = ink('Wolf', nf); ncap = ncap[3] - ncap[1]
GAP_MOON, GAP_TEXT = 28, 12
for i, (mon, name, g) in enumerate(MOONS):
    name = name + ' Moon'
    cy = CY0 + i * STEP
    d.ellipse([SX - R, cy - R, SX + R, cy + R], fill=GOLD)
    stack = mcap + 12 + ncap
    ty = round(cy - stack / 2)
    if i % 2 == 0:   # left of the spine, mirrored: icon beside the moon, text right-aligned to the icon
        ix = SX - R - GAP_MOON - ICON
        im.alpha_composite(g, (ix + (ICON - g.width) // 2, round(cy - g.height / 2)))
        tr = ix - GAP_TEXT
        text_top((tr - width(mon, mf, 3), ty), mon, mf, MAUVE, tracking=3)
        text_top((tr - width(name, nf), ty + mcap + 12), name, nf, IVORY)
        assert tr - width(name, nf) >= M, name
    else:            # right of the spine: icon beside the moon, text flush left after it
        ix = SX + R + GAP_MOON
        im.alpha_composite(g, (ix + (ICON - g.width) // 2, round(cy - g.height / 2)))
        tx = ix + ICON + GAP_TEXT
        text_top((tx, ty), mon, mf, MAUVE, tracking=3)
        text_top((tx, ty + mcap + 12), name, nf, IVORY)
        assert tx + width(name, nf) <= W - M, name
print('moon step', STEP, 'first', CY0, 'last', CY1, 'footer', FOOT)

# Footer: logo bottom left, source bottom right.
logo = Image.open('assets/hh-monogram-white-140.png').convert('RGBA')
lh = 60; lw = round(logo.width * lh / logo.height)
logo = logo.resize((lw, lh), Image.LANCZOS)
logo = Image.merge('RGBA', (*[Image.new('L', logo.size, v) for v in IVORY], logo.split()[3]))
im.alpha_composite(logo, (M, FOOT))
wf = f(AR, 600, 32)
bb = ink('Hex & Hollow', wf)
d.text((M + lw + 16, FOOT + (lh - (bb[3] - bb[1])) // 2 - bb[1]), 'Hex & Hollow', font=wf, fill=IVORY)
sf = f(AR, 400, 30)
src = ['Names: The Old Farmer’s Almanac', 'Dates: USNO, US time']
lcap = ink('N', sf); lcap = lcap[3] - lcap[1]
gap = lh - 2 * lcap                       # two lines spanning the logo's height
for j, line in enumerate(src):
    text_top((W - M - width(line, sf), FOOT + j * (lcap + gap)), line, sf, MAUVE)

im.convert('RGB').save(os.environ.get('PIN_OUT', '/tmp/pin.jpg'), quality=82, optimize=True, progressive=True)
