"""Icon bank helper for pin scripts. See icons/LICENSES.md and the Icons section of PIPELINE.md.

In a render/ script (run from the repo root as `python render/<name>.py`):

    from lib.icons import icon, find, credit
    im.alpha_composite(icon('gi:raven', 160, '#e8dcc8'), (64, 700))   # im must be RGBA; or im.paste(ic, xy, ic)
    find('moth')                      # ids whose name or tags contain "moth"
    find(hh='coffee', source='phosphor')
    credit(['gi:raven'])              # -> 'Icons: Lorc / game-icons.net (CC BY 3.0)', or None for Phosphor only

Needs `pip install resvg-py` (the Render pins action installs it).
"""
import io, json, re
from functools import lru_cache
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
WEIGHTS = ('regular', 'thin', 'light', 'bold', 'fill', 'duotone')


@lru_cache(maxsize=1)
def _index():
    data = json.loads((ROOT / 'icons' / 'index.json').read_text())
    return {e['id']: e for e in data['icons']}


def entry(icon_id):
    """The index.json entry for an id like 'ph:skull' or 'gi:raven'."""
    try:
        return _index()[icon_id]
    except KeyError:
        raise KeyError(f'unknown icon {icon_id!r}; try find({icon_id.split(":")[-1]!r})') from None


def _hex(c):
    if isinstance(c, str):
        c = c.strip()
        if not re.fullmatch(r'#?[0-9a-fA-F]{6}', c):
            raise ValueError(f'color must be #rrggbb or an (r, g, b) tuple, got {c!r}')
        return '#' + c.lstrip('#').lower()
    r, g, b = (int(v) for v in c[:3])
    return f'#{r:02x}{g:02x}{b:02x}'


def svg(icon_id, color, weight='regular', accent=None):
    """The icon's SVG text recolored. weight applies to Phosphor only (regular, thin, light, bold, fill,
    duotone). For duotone, accent colors the back layer solid; without it the back layer is color at 20%."""
    e = entry(icon_id)
    if e['source'] == 'phosphor':
        if weight not in e['weights']:
            raise ValueError(f'{icon_id} has no {weight!r} weight; it has {sorted(e["weights"])}')
        path = e['weights'][weight]
    else:
        path = e['path']
    s = (ROOT / path).read_text().replace('currentColor', _hex(color))
    if accent is not None and weight == 'duotone' and e['source'] == 'phosphor':
        s = s.replace(' opacity="0.2"', f' fill="{_hex(accent)}"')
    return s


def icon(icon_id, size, color, weight='regular', accent=None):
    """Recolor and rasterize an icon to a transparent RGBA PIL image, size x size px (or (w, h))."""
    import resvg_py
    w, h = (size, size) if isinstance(size, int) else size
    png = resvg_py.svg_to_bytes(svg_string=svg(icon_id, color, weight, accent), width=int(w), height=int(h))
    im = Image.open(io.BytesIO(bytes(png))).convert('RGBA')
    if im.size != (w, h):  # resvg keeps the aspect ratio; icons are square, so this only pads odd sizes
        canvas = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        canvas.alpha_composite(im, ((w - im.width) // 2, (h - im.height) // 2))
        im = canvas
    return im


def find(*words, hh=None, source=None, limit=None):
    """Ids whose name or tags contain every word (whole words; plurals match). hh filters by Hex and Hollow category
    (gothic, witchy, animals, nature, coffee, music, holiday, food, home, data-chart, arrows, weather, time,
    emotion); source is 'phosphor' or 'game-icons'."""
    words = [w.lower() for w in words]
    out = []
    for e in _index().values():
        if source and e['source'] != source:
            continue
        if hh and hh not in e['hh']:
            continue
        toks = set(re.split(r'[^a-z0-9]+', ' '.join([e['name'], *e['tags']]).lower()))
        toks |= {t[:-1] for t in toks if len(t) > 3 and t.endswith('s')}
        if all(w in toks for w in words):
            out.append(e['id'])
    out.sort(key=lambda i: (len(_index()[i]['name']), i))  # shortest names first: 'gi:raven' before 'gi:raven-claw'
    return out[:limit] if limit else out


def credit(icon_ids):
    """The Buffer description line a pin needs for the game-icons icons it uses, or None if none need one."""
    artists = sorted({entry(i)['author'] for i in icon_ids
                      if entry(i)['source'] == 'game-icons' and entry(i)['license'] == 'CC-BY-3.0'})
    if not artists:
        return None
    return f'Icons: {", ".join(artists)} / game-icons.net (CC BY 3.0)'
