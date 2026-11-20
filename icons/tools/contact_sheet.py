"""Test sheet for render/lib/icons.py: 24 icons across the Hex and Hollow categories, recolored and rasterized.
Run from the repo root: python icons/tools/contact_sheet.py [out.png]   (the Icon sheet action does this)."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'render'))
from lib.icons import icon, entry, credit  # noqa: E402

PICKS = [  # (id, weight, hh category shown)
    ('gi:raven', None, 'gothic'), ('gi:coffin', None, 'gothic'), ('gi:candle-skull', None, 'gothic'),
    ('ph:skull', 'duotone', 'gothic'), ('gi:magic-potion', None, 'witchy'), ('gi:evil-moon', None, 'witchy'),
    ('ph:magic-wand', 'fill', 'witchy'), ('gi:cat', None, 'animals'), ('ph:paw-print', 'bold', 'animals'),
    ('gi:spotted-mushroom', None, 'nature'), ('ph:leaf', 'duotone', 'nature'), ('gi:rose', None, 'nature'),
    ('gi:coffee-mug', None, 'coffee'), ('ph:coffee', 'duotone', 'coffee'), ('ph:cassette-tape', 'bold', 'music'),
    ('gi:guitar', None, 'music'), ('gi:pumpkin-lantern', None, 'holiday'), ('ph:snowflake', 'light', 'holiday'),
    ('gi:hourglass', None, 'time'), ('ph:chart-bar', 'fill', 'data-chart'),
    ('ph:chart-pie-slice', 'duotone', 'data-chart'), ('ph:arrow-bend-down-right', 'bold', 'arrows'),
    ('ph:cloud-lightning', 'regular', 'weather'), ('gi:broken-heart', None, 'emotion'),
]
FIELD, BONE, MUTED, OXBLOOD = (36, 24, 32), (232, 220, 200), (150, 132, 140), (142, 42, 52)
COLS, CW, CH, M, IS = 6, 216, 250, 48, 120
W, H = M * 2 + COLS * CW, 170 + (len(PICKS) // COLS) * CH + 90
im = Image.new('RGBA', (W, H), FIELD + (255,))
d = ImageDraw.Draw(im)
fonts = Path('assets/fonts')
head = ImageFont.truetype(str(fonts / 'fraunces-latin-600-normal.woff'), 44)
mono = ImageFont.truetype(str(fonts / 'ibm-plex-mono-latin-400-normal.woff'), 16)
small = ImageFont.truetype(str(fonts / 'ibm-plex-mono-latin-400-normal.woff'), 15)
d.text((M, 48), 'Icon bank test sheet', font=head, fill=BONE)
d.text((M, 112), 'render/lib/icons.py: recolored from hex, rasterized with resvg. Phosphor duotone with an accent.', font=mono, fill=MUTED)
for k, (iid, weight, cat) in enumerate(PICKS):
    x, y = M + (k % COLS) * CW, 170 + (k // COLS) * CH
    kw = {'weight': weight} if weight else {}
    if weight == 'duotone':
        kw['accent'] = OXBLOOD
    ic = icon(iid, IS, BONE, **kw)
    im.alpha_composite(ic, (x + (CW - IS) // 2, y + 10))
    d.text((x + CW // 2, y + 150), iid, font=mono, fill=BONE, anchor='mt')
    d.text((x + CW // 2, y + 176), f'{cat}, {weight}' if weight else cat, font=small, fill=MUTED, anchor='mt')
line = credit([i for i, _, _ in PICKS])
d.text((M, H - 70), line, font=small, fill=MUTED)
out = sys.argv[1] if len(sys.argv) > 1 else 'icons/contact-sheet.png'
im.convert('RGB').save(out, optimize=True)
print(out, im.size, line)
