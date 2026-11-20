# Font library

27 families, all SIL Open Font License (licenses alongside), as `.woff` files PIL reads directly:
`ImageFont.truetype('assets/fonts/<family>-latin-<weight>-normal.woff', size)`.
`specimen.png` shows every file. Latin subset only: no emoji, no non-Latin scripts.

Pick the face from the concept and the photo, then pair it with one neutral sans for small text. Two families per pin,
three at most. Rotate: don't reuse the previous run's display face (check the run log).

## Display serifs (headline only)

| Family | Weights | Reach for it when |
|---|---|---|
| fraunces | 400 600 900 | Warm, cozy, bookish. Field guides, kitchens, autumn. |
| playfair-display | 400 700 900 | Romantic, vampire, Victorian. Old-style figures, so not for big stat numbers. |
| bodoni-moda | 400 700 | Luxury, moody editorial. Only at large sizes; thins vanish small. |
| dm-serif-display | 400 | Bold, punchy serif headline. Pairs with dm-sans. |
| gloock | 400 | Sharp, high-contrast, edgy display serif. Gothic poster headlines that must read at feed size. |
| instrument-serif | 400 | Condensed, quiet, literary. Long headlines that need to stay big. |
| young-serif | 400 | Friendly, round, a little retro. Mugs, gifts, soft humor. |
| cormorant-garamond | 500 700 | Delicate, witchy, botanical. Large sizes only. Old-style figures. |
| eb-garamond | 400 600 | Classic book, dark academia, quotes. Old-style figures. |
| zilla-slab | 400 700 | Sturdy slab. Zines, how-tos, field notes. |

## Display sans and condensed

| Family | Weights | Reach for it when |
|---|---|---|
| anton | 400 | Loud, poster, gig flyer. All caps. |
| bebas-neue | 400 | Tall caps only. Labels, setlists, big numbers. |
| oswald | 400 600 | Condensed workhorse, mixed case. |
| barlow-condensed | 500 700 800 | Sporty, industrial, ticket stubs. |
| archivo-black | 400 | Heavy, blunt, punk flyer. |
| archivo / archivo-narrow | 400 600 800 / 500 700 | Versatile grotesk; narrow for tight lists. |
| space-grotesk | 400 500 700 | Slightly odd, techy, zine. |
| libre-franklin | 400 700 900 | Newspaper, classic American. |

## Text sans (body, labels, lists)

| Family | Weights | Notes |
|---|---|---|
| inter | 400 500 600 | Default neutral. |
| dm-sans | 400 500 700 | Rounder, friendlier. |
| manrope | 400 600 800 | Clean, modern. |
| ibm-plex-sans | 400 600 | Technical, slightly mechanical. |

## Monospace and typewriter

| Family | Weights | Reach for it when |
|---|---|---|
| courier-prime | 400 700 | Letters, case files, pen-pal and diary concepts. |
| ibm-plex-mono / jetbrains-mono | 400 600 / 400 700 | Specimen labels, lab notes, data, receipts. |

## Use with care (concept must call for it)

| Family | Weights | Rule |
|---|---|---|
| unifrakturmaguntia | 400 | Blackletter. Goth or metal concepts only, headline only, short words, never body. |
| pirata-one | 400 | Condensed blackletter-ish. Same rule. |
| caveat | 500 700 | Handwriting. Only for a margin note or annotation, never a headline or body. |

## Checks

- Big numbers want lining figures: fraunces, dm-serif-display, bodoni-moda, zilla-slab and every sans have them;
  playfair, cormorant and eb-garamond don't.
- Never fake bold or italic, never stretch. If a weight isn't here, pick another weight or family.
- More families: `npm pack @fontsource/<family>` if the registry is reachable. Add any you use here, with its license.
