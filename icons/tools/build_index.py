"""Build icons/ from pinned upstream sources. Rerun only to change versions.

  python icons/tools/build_index.py PHOSPHOR_PKG PHOSPHOR_META_JSON GAME_ICONS_REPO GAME_ICONS_COMMIT

PHOSPHOR_PKG is the unpacked `npm pack @phosphor-icons/core@2.1.1` (its `package/` dir).
PHOSPHOR_META_JSON is that package's `icons` export as JSON:
  node -e "import('./dist/index.mjs').then(m=>require('fs').writeFileSync('meta.json',JSON.stringify(m.icons)))"
GAME_ICONS_REPO is a clone of https://github.com/game-icons/icons at GAME_ICONS_COMMIT.
"""
import json, re, shutil, sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]           # icons/
ph_pkg, ph_meta, gi_repo, gi_commit = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4]
PH_VERSION = json.loads((ph_pkg / 'package.json').read_text())['version']
WEIGHTS = ['regular', 'thin', 'light', 'bold', 'fill', 'duotone']

# Hex and Hollow categories: keyword -> category, matched on whole words of the icon's name and tags.
HH = {
 'gothic': 'skull skeleton bone crossbones coffin grave gravestone tombstone tomb crypt ghost bat raven crow spider '
           'cobweb death dead reaper scythe vampire fang gargoyle haunted zombie demon devil dagger blood thorn '
           'moth candle candelabra castle graveyard mausoleum cemetery executioner guillotine noose',
 'witchy': 'witch potion cauldron crystal spell pentagram pentacle tarot broom rune magic wand herb incense sage '
           'spellbook grimoire occult ouija alchemy elixir familiar moon sparkle crescent evil seeing third',
 'animals': 'animal cat dog bat raven crow bird owl wolf fox frog toad snake spider moth butterfly opossum possum '
            'rat fish horse rabbit bunny deer bear paw insect bug cow pig squirrel beetle bee snail octopus lizard '
            'turtle raccoon goat sheep chicken duck crab whale shark dragonfly cockroach scorpion bird feather',
 'nature': 'tree leaf leaves flower plant mushroom forest mountain rose vine seed acorn pine cactus petal grass herb '
           'river rock stone feather nature tulip lotus sprout clover log wood bonsai cherry orchid daisy',
 'coffee': 'coffee mug cup tea teapot espresso kettle latte cafe',
 'music': 'music musical note guitar drum microphone mic headphones headphone speaker vinyl record cassette tape piano '
          'violin radio song playlist waveform equalizer amplifier concert sound volume lyre harp trumpet saxophone',
 'holiday': 'christmas xmas gift present snowflake snowman ornament santa halloween pumpkin valentine easter firework '
            'party cake birthday confetti holly mistletoe wreath sled candy cane jack lantern gingerbread',
 'food': 'food pizza burger hamburger cake cookie bread apple cheese fork spoon carrot pepper egg meat candy '
         'chocolate wine beer cocktail drink fruit cherry grape bowl soup pie donut doughnut croissant popcorn '
         'sandwich taco noodle sushi cooking lollipop icecream',
 'home': 'house home bed couch sofa chair armchair lamp door window key lock bathtub toilet kitchen oven fireplace '
         'bookshelf book cabinet shelf furniture rug curtain plant broom',
 'data-chart': 'chart graph histogram gauge percent ruler number calculator analytics trend presentation '
               'checklist list equal equals infinity sigma statistic funnel',
 'arrows': 'arrow arrows caret chevron',
 'weather': 'sun moon cloud cloudy rain snow snowflake storm lightning wind thermometer umbrella rainbow fog tornado '
            'sunrise sunset weather hurricane raindrop',
 'time': 'clock hourglass timer calendar alarm stopwatch watch sundial time',
 'emotion': 'heart heartbreak smiley smile sad angry cry tear laugh love drama emoji wink happy kiss grin frown',
}
KW = defaultdict(set)
for cat, words in HH.items():
    for w in words.split():
        KW[w].add(cat)
# Phosphor's own categories that map straight across.
PH_CAT = {'arrows': 'arrows', 'weather': 'weather'}
# Words that mean something else in a source (computer mouse, music "note" vs memo).
SKIP = {'phosphor': {'mouse'}}

def words(*parts):
    out = set()
    for p in parts:
        for w in re.split(r'[^a-z0-9]+', p.lower()):
            if w:
                out.add(w)
                if len(w) > 3 and w.endswith('s'):
                    out.add(w[:-1])
    return out

# A word in the name that rules a category out (baseball bat, trophy cup, crime scene tape, card suits).
VETO = {
 'gothic': 'baseball leth alien sand bot', 'animals': 'baseball blade leth', 'coffee': 'trophy dice shot rolling',
 'holiday': 'card plug union sugar', 'nature': 'axe bust', 'home': 'bus nuclear file folder app address return', 'music': 'crime scene button device', 'emotion': 'card', 'weather': 'download upload computing file check warning slash',
 'food': 'bone sword dagger chart git', 'time': 'article', 'witchy': 'angry',
}
VETO = {c: set(v.split()) for c, v in VETO.items()}
ARROW_OK = 'up down left right cursor return cycle branch back forward rotation clockwise anticlockwise direction 3d'.split()

def hh_cats(ws, source=None):
    cats = set()
    for w in ws:
        cats |= KW.get(w, set())
    cats = {c for c in cats if not (VETO.get(c, set()) & ws)}
    if 'logo' in ws:
        return set()  # brand logos are never motifs
    if source == 'game-icons' and 'arrows' in cats and not (set(ARROW_OK) & ws):
        cats.discard('arrows')  # game-icons arrows are mostly weapons; keep direction arrows only
    if 'witchy' in cats and ws & {'evil', 'seeing', 'third'} and 'eye' not in ws:
        cats.discard('witchy')
    return cats

# Fix category noise found by eye on the contact sheet.
def tidy(name, cats):
    if 'note' in name and 'music' not in name:
        cats.discard('music')
    return cats

index = []

# ---- Phosphor ----
dst = ROOT / 'phosphor'
if dst.exists(): shutil.rmtree(dst)
for w in WEIGHTS:
    (dst / w).mkdir(parents=True)
for m in json.loads(ph_meta.read_text()):
    n = m['name']
    paths = {}
    for w in WEIGHTS:
        fn = f'{n}.svg' if w == 'regular' else f'{n}-{w}.svg'
        src = ph_pkg / 'assets' / w / fn
        if src.exists():
            shutil.copyfile(src, dst / w / fn)
            paths[w] = f'icons/phosphor/{w}/{fn}'
    tags = [t for t in m.get('tags', []) if not t.startswith('*')]
    # Phosphor tags are broad ("dead" on a battery, "apple" on brand logos), so match on the name only and
    # take Phosphor's own arrows/weather/nature categories.
    ws = words(n) - SKIP['phosphor']
    cats = hh_cats(ws)
    cats |= {PH_CAT[c] for c in m.get('categories', []) if c in PH_CAT}
    if m.get('figma_category') == 'time': cats.add('time')
    if n.startswith('chart') or n.startswith('presentation-chart'): cats.add('data-chart')
    index.append({'id': f'ph:{n}', 'source': 'phosphor', 'name': n, 'path': paths['regular'], 'weights': paths,
                  'license': 'MIT', 'author': 'Phosphor Icons', 'tags': tags,
                  'categories': m.get('categories', []), 'hh': sorted(tidy(n, cats))})

# ---- game-icons ----
dst = ROOT / 'game-icons'
if dst.exists(): shutil.rmtree(dst)
lic = (gi_repo / 'license.txt').read_text()
authors = {}
for line in lic.splitlines():
    mm = re.match(r'- ([^,]+?)(?:, (\S+))?( - CC0)?$', line.strip())
    if mm:
        authors[mm.group(1).strip()] = {'url': mm.group(2), 'cc0': bool(mm.group(3))}
def author_for(folder):
    key = folder.replace('-', '')
    for name, info in authors.items():
        k = re.sub(r'[^a-z0-9]', '', name.lower())
        if k == key or key.startswith(k):
            return name, info
    return folder.replace('-', ' ').title(), {'url': None, 'cc0': False}
files = sorted(p for p in gi_repo.glob('*/*.svg') if p.parent.name != 'badges')
count = Counter(p.stem for p in files)
used_authors = {}
for p in files:
    folder, n = p.parent.name, p.stem
    name, info = author_for(folder)
    used_authors[name] = (folder, info)
    svg = p.read_text().replace('<path d="M0 0h512v512H0z"/>', '', 1).replace('fill="#fff"', 'fill="currentColor"')
    out = dst / folder / f'{n}.svg'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(svg)
    iid = f'gi:{n}' if count[n] == 1 else f'gi:{n}--{folder}'
    ws = words(n)
    index.append({'id': iid, 'source': 'game-icons', 'name': n, 'path': f'icons/game-icons/{folder}/{n}.svg',
                  'license': 'CC0-1.0' if info['cc0'] else 'CC-BY-3.0', 'author': name, 'tags': n.split('-'),
                  'categories': [], 'hh': sorted(tidy(n, hh_cats(ws, 'game-icons')))})

index.sort(key=lambda e: e['id'])
meta = {'sources': {
    'phosphor': {'package': '@phosphor-icons/core', 'version': PH_VERSION, 'license': 'MIT',
                 'repo': 'https://github.com/phosphor-icons/core', 'weights': WEIGHTS},
    'game-icons': {'repo': 'https://github.com/game-icons/icons', 'commit': gi_commit, 'license': 'CC-BY-3.0',
                   'changes': 'black 512x512 background square removed, white fill set to currentColor'}},
    'hh_categories': list(HH), 'count': len(index)}
(ROOT / 'index.json').write_text(json.dumps({'meta': meta, 'icons': index}, separators=(',', ':')))
by = defaultdict(list)
for e in index:
    for c in e['hh']:
        by[c].append(e['id'])
(ROOT / 'by-category.json').write_text(json.dumps({c: by[c] for c in HH}, indent=0))

# ---- LICENSES.md ----
mit = (ph_pkg / 'LICENSE').read_text().strip()
rows = '\n'.join(f'| {n} | `icons/game-icons/{f}/` | {"CC0 1.0" if i["cc0"] else "CC BY 3.0"} | {i["url"] or ""} |'
                 for n, (f, i) in sorted(used_authors.items(), key=lambda x: x[0].lower()))
(ROOT / 'LICENSES.md').write_text(f'''# Icon licenses

Two sources, both free for commercial use. Versions are pinned; `tools/build_index.py` rebuilds this folder.

## Phosphor Icons (MIT)

`icons/phosphor/<weight>/`, from `@phosphor-icons/core` {PH_VERSION} on npm
(https://github.com/phosphor-icons/core). Unmodified. No credit is needed on a pin. Text below and in
`LICENSE-phosphor-MIT.txt`.

```
{mit}
```

## game-icons.net (CC BY 3.0, a few CC0)

`icons/game-icons/<artist>/`, from https://github.com/game-icons/icons at commit `{gi_commit}`.
Changed for this repo: the black 512x512 background square was removed and the white fill set to `currentColor`
so the icon can be recolored. Each icon's artist is its folder name and the `author` field in `index.json`.

License: Creative Commons Attribution 3.0 Unported, full text in `LICENSE-CC-BY-3.0.txt`
(https://creativecommons.org/licenses/by/3.0/). The two CC0 artists: `LICENSE-CC0-1.0.txt`.
game-icons' own notice: "Icons provided under the Creative Commons 3.0 BY or CC0 if mentioned below ...
Please, include a mention "Icons made by {{author}}" in your derivative work."

**Credit on a pin:** any pin that uses a game-icons icon credits it in the Buffer description as
`Icons: <artist> / game-icons.net (CC BY 3.0)` (for example `Icons: Lorc / game-icons.net (CC BY 3.0)`; join several
artists with commas). `render/lib/icons.py` gives the exact line with `credit([...ids])`. CC0 artists need no credit,
but crediting them too does no harm.

| Artist | Folder | License | Link |
|---|---|---|---|
{rows}
''')
print(len(index), 'icons;', Counter(e['source'] for e in index))
