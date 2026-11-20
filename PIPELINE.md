# Hex & Hollow daily pin pipeline

One hand-designed Pinterest pin a day, built from a real Etsy listing photo, linking to that listing.
No fixed template. Everything a run needs is in this repo; nothing lives anywhere else.

## Standing rules (Anthony's words, Nov 19 2026)

- "I don't want the same layout every time." / "I need variety. Lists like tonite, infographics, illustrations, etc."
- "make sure that the color palette is always inspired by the image so it vibes well."
  Sample the field, headline and accent hues from the actual photo every time. Never a house palette.
- "Straight to queue": queue each pin in Buffer with `addToQueue`. No draft step.
- No em dashes anywhere (pin, title, description, alt text).

## Why it's shaped like this

Claude's sandbox can't reach i.etsystatic.com (Etsy photos). It can reach api.github.com and raw.githubusercontent.com.
So a GitHub Action downloads the listing photos into this repo, and raw.githubusercontent.com hosts the finished pin
for Buffer. No image bytes ever go through the GitHub connector (a pin as base64 is ~150K characters, too big for
one run). Instead each day's pin is a hand-written PIL script committed to `render/`, and the **Render pins** action
runs it on GitHub and commits the JPEG.

## Repo layout

| Path | What |
|---|---|
| `queue/photos.txt` | One `listing_id url` per line. Only `https://i.etsystatic.com/...` URLs are fetched. `#` lines are comments. |
| `photos/<listing_id>-<n>.jpg` | Written by the **Fetch listing photos** action. `n` counts that listing's lines in the file, top to bottom. |
| `render/<YYYY-MM-DD>-<slug>.py` | The day's pin as a PIL script. A push runs **Render pins**: Python 3.12 + Pillow + numpy, from the repo root, with env `PIN_OUT=pins/<same name>.jpg`. The script must save a 1000x1500 JPEG to `PIN_OUT`. Scripts whose pin already exists are skipped, so a pin is never overwritten. |
| `pins/<YYYY-MM-DD>-<slug>.jpg` | Finished pins, committed by Render pins. Served at `https://raw.githubusercontent.com/altextreme/hexhollow-pins/main/pins/<name>.jpg` |
| `assets/` | Logos: `hh-monogram-white-140.png` (monogram, tint it), `hh-logo-monogram-white.png`, `hh-logo-full-white.png`, `hh-logo-full-dark.png`. |
| `assets/fonts/` | 26 OFL families as `.woff` (PIL reads them): serifs, condensed, sans, mono, two blackletters, one handwriting. `FONTS.md` says when to use each; `specimen.png` shows them all. |
| `scripts/` | Reference pins as runnable PIL scripts (same `PIN_OUT` contract). Copy the approach, never the layout. |
| `icons/` | Icon bank: 1,512 Phosphor icons in 6 weights (MIT) and 4,180 game-icons.net icons (CC BY 3.0, a few CC0), as recolorable SVGs. `index.json` has one entry per icon (id, source, path, license, author, tags, `hh` categories); `by-category.json` lists ids per Hex and Hollow category; `LICENSES.md` has the licenses and artists; `contact-sheet.png` shows a sample. See **Icons** below. |
| `render/lib/icons.py` | Helper for pin scripts: `from lib.icons import icon, find, credit`. Not a pin; Render pins only runs `render/*.py`. |
| `TASTE_LOG.md` | What Anthony approved and rejected, in his words, with the pin files. Read it before designing and give it to the reviewer. |

Actions trigger on push to their paths and on workflow_dispatch, share one concurrency group, and their commits
don't retrigger workflows. **Fetch listing photos** logs a bad or non-Etsy URL as a warning and skips it rather than
failing. **Render pins** fails loudly if a script errors or doesn't produce a 1000x1500 JPEG; GitHub emails the
person who pushed (Anthony's account) when a run fails. (**Decode pins** for `pins/*.b64` still exists but isn't
used.)

## Daily steps

1. **Read the run log** at the bottom of this file. Don't repeat a listing pinned in the last 14 days, and don't
   repeat the previous run's format.
2. **Pick a listing.** Etsy connector `etsy_list_listings` (shop 66807773). Prefer listings with a lifestyle photo.
3. **Queue its photos.** `etsy_list_listing_images` → `url_fullxfull` for 2 to 4 lifestyle shots. Append
   `listing_id url` lines to `queue/photos.txt` and commit (GitHub connector `create_or_update_file`; it needs the
   file's current sha). Re-fetching old lines is harmless; trim the file now and then.
4. **Wait for the run.** Poll `GET https://api.github.com/repos/altextreme/hexhollow-pins/actions/runs?per_page=1`
   until `status: completed`, `conclusion: success` (about 15 s). Then download
   `https://raw.githubusercontent.com/altextreme/hexhollow-pins/main/photos/<id>-<n>.jpg` into the sandbox.
   Also download what you need from `assets/` and `assets/fonts/` the same way, to try the design locally first.
5. **Pick the format.** Rotate so consecutive days differ: list (setlist, playlist, checklist), big-number
   infographic, field guide or labelled diagram, how-to steps, illustration-led quote, comparison or "this or that".
   It must be adjacent value content people save even without buying, with the product as the photo.
   His best pins look like "5 Things to Put in a Pen-Pal Letter".
   Infographics, lists and diagrams can use the icon bank in `icons/` (see **Icons**). A photo-free icon
   infographic, palette still sampled from the product's photo, is also allowed (Anthony asked for one on Nov 19;
   see the twelve-moons row). Plan its drawn visual first: a grid or list of icons fails review.
6. **Write the script** to `render/<YYYY-MM-DD>-<slug>.py`: Python/PIL at 1000x1500 (follow the design-taste skill
   if available). It reads `photos/`, `assets/` and `assets/fonts/` by relative path and saves to
   `os.environ['PIN_OUT']`. Render it locally first if you can, then commit it with the GitHub connector.
   - Palette: take medians over small regions of the photo (see `scripts/`). Field = the photo's dominant deep hue,
     darkened but still clearly a color (not gray, not near-black). Headline = one saturated hue from the photo.
     One more accent at most. Everything else neutrals pulled from the photo's lights.
   - Image first, full bleed, under half the page height. Flush left, 64 px margins, strict grid.
   - Type: pick the face for the concept from `assets/fonts/FONTS.md`. Never reuse the previous run's display face
     (log it in the run log). For others, `npm pack @fontsource/<family>` if the registry is reachable.
   - Curly quotes and apostrophes. No widows, shadows, gradients, ornaments or em dashes.
   - Logo: `assets/hh-monogram-white-140.png` tinted to the light neutral, wordmark "Hex & Hollow" beside it.
   - Leave a clear pause above the footer; nothing near-touching anything.
   - Downscale to 180 px wide and check the headline and the main element still read.
   - Every fact must be true. Check anything you state. (The "opossums eat 5,000 ticks" claim was debunked; skip
     myths like it.)
   - Save JPEG quality ~80, aim 100 to 190 KB.
7. **Wait for Render pins and review the result.** Poll the Actions runs as in step 4. If it failed, read the run's
   log (`GET .../actions/runs/<id>/jobs`), fix the script and push it under a new slug. When it succeeds, download
   `https://raw.githubusercontent.com/altextreme/hexhollow-pins/main/pins/<name>.jpg` and look at it at full size
   and downscaled to 180 px wide. If anything is off (collision, near-tangent, unreadable at feed size, wrong
   crop), push a revised script under a new name (`-v2`, `-v3`) and review again. Never overwrite a file.
8. **Queue in Buffer.** Org `68ce2bdb4573424f589bb15a`, Pinterest channel `6a616171e2638b94d7b9e986`.
   `create_post` with `mode: addToQueue`, `schedulingType: automatic`, `assets[0].image.url` = the raw URL plus
   `altText`, `metadata.pinterest.boardServiceId`, `title`, `url` = `https://www.etsy.com/listing/<listing_id>`,
   and `text` = description. Voice: elder emo, goth, wry, "It was never a phase." End the description with 3 to 4
   plain search phrases.
   Boards: apparel `1111967032937184648` (Gothic Graphic Tees & Dark Aesthetic Clothing);
   mugs, tumblers, gifts `1111967032937184649` (Witchy & Gothic Mugs, Tumblers & Gifts);
   wall art `1111967032937184691` (Printable Wall Art); Witchy Vibes `1111967032937184729`.
9. **Append a run log row** below and commit.

## Layout skeletons (Anthony, Nov 19 2026: "Fix the layout rule")

Every pin picks a format, a headline face AND a layout skeleton, each different from the last 4 run log rows.
Look at the last 4 pins' JPEGs in `pins/`, not just the log. Rotate at minimum between:

- **a.** Photo full-bleed across the top (edge to edge, hard bottom edge), text block below.
- **b.** Full-bleed photo as the whole background, headline over a sampled-color scrim or panel, minimal text.
- **c.** Side-by-side split: the photo fills one whole side, top to bottom and out to the edge, hard edge on the
  inside; or a full-width photo band through the middle, edge to edge, with text above and below.
- **d.** Type-led: a huge headline fills most of the pin; the photo is a full-width band at the top or bottom edge.
- **e.** Photo full-bleed across the bottom, text top.
- **f.** Big-number or single-statement layout; the photo is a full-width strip at one edge.

## Photo rules (Anthony, Nov 18 2026, on the coffee v2 pin: "Having a faded out image like this in the corner is not in
the design taste skill. It's poorly executed. The graph is fine but it looks gross.")

The photo is always one of two things, nothing else:
1. **Full bleed**: it reaches the pin's edges on every side it touches, and meets the color field in one straight,
   hard, grid-aligned edge.
2. **Full-bleed background**: it covers the whole pin, and text sits on a scrim or panel sampled from it.

Never: a photo inset that floats inside the field, a crop parked in a corner, a feathered or vignetted edge on a cropped
photo, a fade on two or more sides of a crop, rounded or framed photos, or a bleed on only one side (bleed symmetrically
or not at all). A soft fade is allowed in exactly one case: a full-bleed photo whose own background (wall, sky, fog)
already matches the field, fading along ONE straight full-width edge into a field sampled from that same background,
so it reads as one continuous space (the ornament pin, goth-up-the-tree-v2, is the reference). If in doubt, hard edge.
The photo stays under about half the pin's height unless it is the full background.

Never use the "FIELD NOTES /" eyebrow again. Any eyebrow must differ every day, or leave it out. Move the logo
around the grid (any corner, or centered at the foot), never over photo features. Log the skeleton letter in Notes.
Before queuing, put the new pin beside the previous one: if a stranger would think they share a template, redo it.

## Creative director review (Anthony, Nov 18 2026: "You should have some sort of creative director agent give it a look
as part of the workflow." Tightened Nov 18 after it passed coffee v2, which Anthony rejected.)

After Render pins, start a fresh subagent as creative director. Give it: the new pin (full size and 180 px wide), the 3
most recent earlier pins, the listing title, TASTE_LOG.md, and every pin that file names as rejected or approved
(download them from pins/). Not your intent, and nothing defending your choices.

It loads the design-taste skill and works in this order:
1. **Hard fails first.** Answer each yes or no, with a reason. Any yes is an automatic FAIL, whatever the scores:
   - Does the photo float, sit in a corner, or have a feathered, faded or vignetted edge, outside the one allowed case
     in Photo rules?
   - Does the photo bleed on only one side, or fail to reach the edges it touches?
   - Does anything sit a few pixels from something else (a near-tangent), or collide?
   - Is any text under 22 px at 1000 px wide, or unreadable at 180 px wide?
   - Would a stranger think it shares a template with any of the last 3 pins?
   - Does it repeat anything TASTE_LOG.md lists as rejected?
   - Is any fact unchecked or wrong?
2. **Scores**, in the skill's scored critique format: hierarchy, palette fit with the photo, type, photo treatment,
   phone legibility, facts and tone. PASS needs every score at 8 of 10 or better.
3. **Return PASS, or numbered must-fixes.** Default to FAIL when unsure, and say plainly what Anthony would hate.

Fix every must-fix under a new file name, re-render, re-review. Stop after 3 rounds; if it still fails, don't queue it
and report what it kept rejecting. Log the round count and the hard-fail answers in Notes.

## Icons

`icons/` holds two open icon sets for infographics. Pull from it only when an icon carries information.

- **Use icons for:** drawn infographics (a marker per data point, a symbol per bar or zone), list items shown as
  icons instead of bullets or numerals, and labelled diagrams or how-to steps. The icon must say something the
  text would otherwise have to.
- **Never as decoration:** no clip-art sprinkled in corners, no icon next to a headline for vibes, no icon
  repeating the product photo. If removing it loses nothing, remove it. (Ornaments are already a hard fail.)
- **One family per pin:** all Phosphor in a single weight, or all game-icons. Never mix the two, and never mix
  Phosphor weights. Phosphor is the clean set for charts, arrows, time and data; game-icons is the gothic,
  witchy and animal motif set (raven, coffin, potion, moon, candle, skull, cat).
- **Color from the photo:** recolor every icon from the palette sampled for that pin (the light neutral, or the
  headline hue for the one icon that matters most). Phosphor `duotone` takes a second sampled hue as `accent`.
  No icon keeps a default color.
- **Size:** an icon that carries meaning is at least 96 px at full size so it reads at 180 px wide. `thin` and
  `light` Phosphor weights only above 200 px; below that use `regular`, `bold`, `fill` or `duotone`.
- **Find one:** `find('raven')`, `find('chart', source='phosphor')`, `find(hh='gothic')`, or read
  `icons/by-category.json` (categories: gothic, witchy, animals, nature, coffee, music, holiday, food, home,
  data-chart, arrows, weather, time, emotion). Categories come from name keywords, so look at the icon before
  using it. game-icons has no moth; `ph:butterfly` is the closest.
- **Draw it:** in a `render/` script,
  `from lib.icons import icon` then `ic = icon('gi:raven', 160, palette_light)` gives a transparent RGBA image
  (color as `#rrggbb` or an RGB tuple; `weight='bold'` and `accent=...` for Phosphor). Paste it with
  `im.paste(ic, (x, y), ic)`. To try it locally, `pip install resvg-py` and download `icons/index.json` plus the
  SVGs you need from raw.githubusercontent.com into the same paths.
- **Credit:** any pin that uses a game-icons icon credits it in the Buffer description, as the last line before
  the search phrases: `Icons: <artist> / game-icons.net (CC BY 3.0)`, for example
  `Icons: Lorc / game-icons.net (CC BY 3.0)`. `credit(['gi:raven', ...])` returns the exact line (artists
  joined with commas). game-icons asks for the artist's name, so don't drop it. Phosphor needs no credit. Log
  the icon ids in the run log Notes.

## Gotchas

- Buffer's plan caps the org at **10 scheduled posts**. Queue one a day; never batch.
- Buffer fetches the image when it publishes. Never delete or rename a queued pin's file here.
- raw.githubusercontent.com caches for about 5 minutes. Use a new filename for a changed pin; never overwrite.
- This repo is public: listing photos, pins, assets and scripts only. Nothing private, no tokens.
- If any step fails, stop, log it in the run log, and report what failed. Don't queue a half-finished pin.

## Run log

| Date | Listing | Format | Display face | Pin file | Board | Buffer post | Notes |
|---|---|---|---|---|---|---|---|
| 2026-11-19 | 4620217027 Carpool sweatshirt | List (setlist) | Anton | pins/2026-11-19-carpool-setlist.jpg | Gothic Graphic Tees | 6afe6c54b16549e9b81edc83 | Posts Nov 19 2:56 PM CT. Image re-hosted here after the old renderer was deleted. Anthony published it manually Nov 18 10:01 PM CT. |
| 2026-11-19 | 4604532797 Opossum mug | Big-number infographic | Fraunces | pins/2026-11-19-opossum-by-the-numbers.jpg | Witchy & Gothic Mugs | 6afe6e0259eff0b616d91629 | Posts Nov 19 4:28 PM CT. End-to-end test of this pipeline. |
| 2026-11-19 | 4588636322 Red moth sweatshirt | Comparison (moth or butterfly) | Fraunces | not pushed | Gothic Graphic Tees | none | FAILED at step 7: a ~110 KB pin is ~148K base64 chars, too big to pass through the text-only GitHub connector in one routine run, and this run has no git push access. Photos fetched (photos/4588636322-1..3.jpg). Nothing queued. Also redo the face: Fraunces repeats the previous run. |
| 2026-11-19 | 4588636322 Red moth sweatshirt | Labelled diagram (how to read a moth) | EB Garamond 600 | pins/2026-11-19-how-to-read-a-moth.jpg | Gothic Graphic Tees | 6afe72e1749099bdc70a5c43 | Posts Nov 19 6:59 PM CT. Used the photos fetched by the failed run; first pin through the render/ action. Note: this sandbox's proxy blocks api.github.com for this repo, so poll raw.githubusercontent.com for the pin (or use the connector's actions_list). |
| 2026-11-19 | 4588762149 Howling wolf moon tee | Comparison (myth vs truth) | Playfair Display 700 | pins/2026-11-19-what-the-howl-means.jpg | Gothic Graphic Tees | 6afe741259eff0b616dae864 | Test run Anthony asked for. Posts Nov 19 8:02 PM CT. Full path: photos queued, fetched, script rendered on GitHub, matched the local render. |
| 2026-11-19 | 4587520183 Skull and raven tee | Comparison (raven or crow) | Playfair Display 900 | pins/2026-11-19-raven-or-crow.jpg | Gothic Graphic Tees | 6afe748df6b6aa0cd49d38e8 | Test run Anthony asked for. Posts Nov 19 2:56 PM CT. Ran alongside the wolf run, so it repeats that pin's format and face family; next run, pick neither. The carpool post (6afe6c54...) no longer shows as scheduled in Buffer; this pin took its slot. |
| 2026-11-19 | 4587517884 Black cat tumbler | World-tour list (black cat luck, by place) | Bodoni Moda 700 | pins/2026-11-19-black-cat-luck.jpg | Witchy & Gothic Mugs | 6afe75ccb16549e9b82206e2 | Skeleton e (text top, photo bottom), logo top left, no eyebrow, forest green and print gold. Posts Nov 20 2:28 PM CT. Rendered on GitHub, matched the local render byte for byte. Earlier rows are all skeleton a. |
| 2026-11-19 | 4611527807 Toxic Energy frog mug | Single fact (toxic is learned) | Archivo Black | pins/2026-11-19-toxic-is-learned.jpg | Witchy & Gothic Mugs | 6afe7777b16549e9b8228f71 | Test run Anthony asked for. Skeleton b (full-bleed photo, headline over a walnut-shadow scrim), logo centered at the foot, no eyebrow, frog-lime headline. Posts Nov 20 3:12 PM CT. Matched the local render. Skipped 4588776000 (Team Edward tee: Twilight name and actor likenesses, a trademark and likeness risk to promote). A parallel run queued 4592243206 (ornament) photos at the same time, so this run avoided it. |
| 2026-11-19 | 4592243206 Midnight Mistletoe ornament | How-to steps (how to goth up a Christmas tree) | Instrument Serif 400 | pins/2026-11-19-goth-up-the-tree-v2.jpg | Witchy & Gothic Mugs | 6afe77f146636f319e87f7c6 | Skeleton b, light variant: full-bleed photo over the top two thirds, feathered (smoothstep, 300 px) into a pale fog field sampled from the room, berry-red headline low, 2x2 steps with string-gold numerals, logo bottom right, no eyebrow. First light-field pin. v1 (logo centered at the foot) was rendered but not queued because the parallel frog run, also skeleton b, uses that logo spot. Posts Nov 20 4:56 PM CT. Next run: use c, d or f; a, b and e are all in the last 4. |
| 2026-11-19 | 4588003563 Awake and Unafraid skeleton coffee tee | Infographic with a chart (caffeine decay curve: your 3 PM coffee is still up at midnight) | DM Serif Display 400 | pins/2026-11-19-coffee-still-up-v2.jpg | Gothic Graphic Tees | 6afe79b759eff0b616dd2567 | REJECTED by Anthony; replaced by v3 below. Run at 10:13 PM CT Nov 18. Skeleton d (type-led: huge bone headline over the top third, chart below in the left column, photo a tall crop bleeding off the right and bottom with a 30 px feathered left edge), logo bottom left, no eyebrow. Coffee-brown field from the wall shadow, bone from the print, curve in the print's exact red. Facts: 8 oz brewed about 95 mg; about 5 h average half-life, hedged on the pin. Creative director: 2 rounds (v1 cream field and near-duplicate red were rejected; v2 PASS). v1 rendered but not queued. Avoided 4592243206 and 4611527807, which parallel runs were working on. |
| 2026-11-19 | 4611527435 We Got Older cassette sweatshirt | Glossary (speak fluent tape deck: C90, leader, auto-reverse, the pencil fix) | Barlow Condensed 800 | pins/2026-11-19-speak-fluent-tape-deck.jpg | Gothic Graphic Tees | none (not queued) | Run at 10:17 PM CT Nov 18. Skeleton c (headline on top, photo as a hard-edged full-bleed band through the middle, 2x2 glossary below in IBM Plex Mono terms and Inter definitions), logo top right, no eyebrow. Latte headline on a deep coffee field, cream terms. Creative director: 1 round, PASS (quick wins: crop off the fingertip sliver at the band's bottom, tighten the bottom margin, darker field with the heart red as one accent). NOT QUEUED: Buffer showed 7 scheduled at the start, but parallel runs took it to 9 before create_post, so this run stopped at the 9-post rule. Pin is rendered and reviewed under the old review; re-review it under the hard-fail checks before any run queues it. |
| 2026-11-19 | 4592258658 Emotionally Nocturnal opossum mug | Infographic: timeline chart (when the night garden opens) | Cormorant Garamond 700 | pins/2026-11-19-night-bloom-clock.jpg | Witchy & Gothic Mugs | 6afe79ebb16549e9b82364d0 | REJECTED and deleted from Buffer by Anthony. Skeleton c: photo as a full-width band through the middle, both edges feathered into a rust-brown field (smoothstep), copper headline above, Gantt-style bloom chart below. Logo bottom left. Review after queuing did NOT pass: too close to the coffee pin, labels too small at 180 px, headline descenders touching the top fade. Skipped 4588773038 (Forks tee, same Twilight risk as 4588776000). |
| 2026-11-19 | 4588003563 Awake and Unafraid skeleton coffee tee | Infographic with a chart (caffeine decay curve) | DM Serif Display 400 | pins/2026-11-19-coffee-still-up-v3.jpg | Gothic Graphic Tees | 6afe79b759eff0b616dd2567 | REDO of the v2 row, made by the coordinator after Anthony rejected v2 ("faded out image like this in the corner... looks gross"). Skeleton a: photo full-bleed across the top 640 px with a hard edge, headline and full-width chart below, logo bottom right. Same Buffer post, image swapped to v3; posts Nov 20 5:40 PM CT. The creative director had passed v2, which led to the hard-fail checks and TASTE_LOG.md. |
| 2026-11-19 | 4611544912 Still Ready for the Pit mug (first tried 4618209079 In Bed by 9 sweatshirt) | Infographic: decibel level meter (2 minutes at 110 dB can damage your hearing, CDC Vital Signs 2017) | Zilla Slab 700 (round 1: Bebas Neue) | pins/2026-11-19-two-minutes-at-110-db-v2.jpg (also ears-at-a-rock-show, two-minutes-at-110-db) | none | none (not queued) | Anthony asked for one more infographic, unique and built for phones. Skeleton f. FAILED the creative director 3 rounds, so not queued per the rule. R1 (sweatshirt, semicircle gauge, Bebas red caps): template match with coffee-v4, same model crop as moth-v2, ear tips 8 px from the top edge, "how long your ears last" overstated CDC. R2 (pit mug, slate field, horizontal LED meter, photo bottom strip): template match with black-cat-luck-v2, meter too small at 180 px, slate not sampled from the photo, "hurt" vs "damage". R3 (wall-gray field, vertical meter): mug base 15 px from the photo edge, meter scale uneven at the 120 end and pale bars above 110 read as safe, three competing focal points, logo off the grid, "85 risk starts" drops "extended exposure". Next try: meter as the one hero at 45 to 50% width on an even scale, danger colors darkening upward, mug 60 px or more clear of the edge. Buffer stayed at 7 scheduled. |
| 2026-11-19 | 4611544912 Still Ready for the Pit mug | Infographic, pass 2 (CDC time limits by loudness: 2 minutes at 110 dB can cause damage) | Zilla Slab 700 (v3, v4), Oswald 600 (v5) | pins/2026-11-19-two-minutes-at-110-db-v5.jpg (also -v3, -v4) | none | none (not queued) | Anthony asked for one more pass. FAILED the creative director 3 more rounds, so not queued. R1 (v3, even 5 dB meter): bars 80/95/105/115 not in CDC data, time story not charted, looked like coffee-v4. R2 (v4, skeleton c band, horizontal time bars on a dark wood field): two bars were slivers, labels too small at 180 px, same band skeleton as tape-deck, same dark family as the queue. R3 (v5, light wall-gray field, huge red "2 minutes", log time scale, photo 2 as the bottom strip): read as skeleton e like black-cat-luck-v2, chart too thin to be the hero, gray field not a hue, 26 words, binder clips in the bottom 120 px, "Time until damage" firmer than CDC's "can cause damage". Reviewer's next ask: skeleton c split (photo fills the right half top to bottom), a deep hue from the vase, a thick vertical log timeline as the hero. Buffer untouched. |
| 2026-11-19 12:16 PM CT | 4589401466 Barbed wire heart tote | List: reading list (four gothic classics: Wuthering Heights, Frankenstein, Rebecca, We Have Always Lived in the Castle) | Libre Franklin 900 (R1), Fraunces 900 (R2, R3) | pins/2026-11-19-books-with-thorns-v2.jpg (also barbed-wire-reading-list, books-with-thorns) | none | none (not queued) | Scheduled run. Skeleton d all 3 rounds. FAILED the creative director 3 rounds, so not queued. Facts passed every round. R1 (cream field, red headline, ruled rows, photo band bottom): hard fails c (band edge chops the tote handles, crate edge ~12 px under it, white wall melts into the cream field), d (description lines blur at 180 px), e/f (reads as black-cat-luck-v2). R2 (photo band top, red Fraunces headline, book-spine stack, logo centered at foot): c (tote edge sliver at the left pin edge, near-alignments at x 823/834/879), d (author lines mush at 180 px), e/f (same build as coffee-v4 and moth/howl), spine tick bars called ornaments, gray spine not in photo. R3 (deep rose field, cream headline, zebra-striped spines, photo band bottom, logo top left): c (headline 6 px short of the list's right edge, cramped band padding, heart fills the band), d (sublines 3 px at 180), e/f (black-cat-luck-v2 again), cream/brown stripes muddy on maroon. What it kept rejecting: any "headline over rows plus a photo band" build reads as black-cat-luck-v2 or coffee-v4, and two-line rows never survive 180 px. Next try for this listing: skeleton c side split or a drawn timeline (1818 to 1962) with titles and quips only, logo off top left. Photos fetched: photos/4589401466-1.jpg, photos/4587785543-1.jpg (luna moth mug, unused). Buffer stayed at 6 scheduled. |
| 2026-11-19 1:52 PM CT | 4618215622 Running on Nostalgia skeleton Christmas sweatshirt | Infographic: drawn vertical timeline, stops to scale (nostalgia was a diagnosis: 1688 Hofer, 1860s Union army 5,000+ cases, 2012 Emotion study) | Archivo Narrow 700 | pins/2026-11-19-nostalgia-diagnosis-v2.jpg (also nostalgia-diagnosis) | none | none (not queued) | Scheduled run. Skeleton c, side split (photo 1 fills the left side top to bottom, hard vertical edge, text column right): new to the queue, and the reviewer said no template match both rounds. FAILED the creative director 2 rounds, then stopped: the crop can't be fixed with these photos. R1 (crimson field, years as big as headline): hard fails c (mug sliced to an 85 px sliver at the left edge, slogan 33 px from the split, hair cut along the split) and g ("1861: 5,000+ cases" put a war-long total on one year; "It makes a cold room feel warmer" overgeneralized the 2012 study). R2 (golden split at 618, black-cherry field, facts fixed and passed): c (half mug at the left edge, hair crown touching the top edge, plaid slivers at the bottom), black sweatshirt melts into the dark field along two thirds of the split, captions about 5 px at 180, unbalanced "was a" headline break. Why stopped: photo 1 is the only shot with the full slogan, and the mug ends 3 to 4 source px before the slogan starts, so no vertical crop can drop the mug or hold it whole and still clear the slogan; photos 2 and 3 hide "& Holiday Snacks" in the waistband. Next try for this listing: skeleton b or a horizontal build, and only with a new lifestyle photo. Also fetched photos/4587522510-1.jpg (sad teddy tee) and photos/4611527727-1.jpg (cracked heart tee): both square with wide subjects, so they don't suit a side split either. Buffer stayed at 6 scheduled. |
| 2026-11-19 5:20 PM CT | 4587785543 Luna moth mug (R1, R2); 4611545302 Still Growing skull hoodie (R3); 4619798702 Elder Emo Mom Still Loud sweatshirt (R4, R5) | R1-R2: infographic, to-scale luna moth life-cycle bar ("Weeks of waiting, one week of wings"). R3: single fact (skull sutures stay open past 100). R4-R5: single fact (Spotify/NYT 2018, hits from our early teens) | Young Serif (R1, R2), Anton (R3-R5) | pins/2026-11-19-still-loud-still-14-v2.jpg (also weeks-of-waiting, weeks-of-waiting-v2, skull-never-finishes, still-loud-still-14) | none | none (not queued) | Scheduled run. 5 creative director rounds, all FAIL; round 5 fallback NOT used because R5 failed hard-fail c (photo feature behind text), not only similarity or taste. Skeletons: R1 b (full-background lifestyle photo, bottom scrim); R2 product cutout on a wine field, headline and bar below; R3-R4 type-led, huge Anton headline top, garment cutout anchored at the foot on a light field; R5 b (2:3 lifestyle photo full background, bottom scrim). Hard fails: R1 a (scrim read as a photo faded into a field), c (logo on bokeh), e (tree-v3 order), f (same scene as rejected night-bloom-clock). R2 e (image top, headline, chart, logo foot = coffee-v4 order), g (no "luna" or "summer" qualifier; cocoon length shaky), moth hidden at the mug's edges. R3 h (the listing's only mockup cuts off the bottom of the "Still Growing" slogan, print soft and small). R4 h (print about 260 px wide, slogan unreadable at 180 px). R5 c (mug and hands ghost through the scrim behind the headline; headline and support line edges 2 to 3 px apart). Facts passed R3-R5. What it kept rejecting: product too small or hidden, and anything showing through behind text. Next try for 4619798702: same full-background photo with a solid sampled panel (no gradient) from y 1100 down, support line clearly shorter than the headline, logo on the text axis. Photos fetched: 4587785543-2, 4611545302-1, 4619798702-1 and -2. Buffer stayed at 5 scheduled. Note: 4611545302's listing photo itself clips the slogan; worth checking the mockup. |
| 2026-11-19 ~6 PM CT | 4619798702 Elder Emo Mom Still Loud sweatshirt | Single fact (Spotify/NYT 2018) | Barlow Condensed 800 | pins/2026-11-19-still-loud-still-14-v3.jpg | none | none (not queued) | Test run fired by trigger. Daily budget: 10 rounds already logged today, so this run had 2; used 1 and stopped, since the one left couldn't fix the template and photo problem the reviewer named. Skeleton b: 2:3 lifestyle photo as full background, scrim fully opaque from y 1100, headline and two short lines and logo flush left. R1 FAIL. Hard fails: a no, b no, c no (gaps fixed), d no (logo text at the 30 px floor), e YES (photo top two thirds over a dark band with a flush-left red condensed headline reads as coffee-v4 and carpool-setlist), f no, g YES ("our most-played hits" overstates a study of No. 1 hits from 1960 to 2000 about when tastes form), h no, i no. Also: "STILL LOUD" echoes the print directly under it. Next try for this listing: a headline that adds to the print, the fact phrased as "No. 1 hits we love most came out when we were about 11 to 16 (NYT/Spotify, 2018)", and a layout that isn't photo over dark band; a side split would crop the sweatshirt, so try a type-led or chart pin. Buffer stayed at 5 scheduled. |
| 2026-11-19 6:00 PM CT | 4618209015 Making Spirits Bright-ish cat Christmas sweatshirt | Infographic: drawn 4-step risk scale (holiday hazards, ranked for cats: poinsettia mild upset, holly vomiting, tinsel gut blockage, lilies kidney failure; ASPCA) | Space Grotesk 700 (labels Inter) | pins/2026-11-19-holiday-hazards-ranked-for-cats.jpg | Gothic Graphic Tees | 6aff8fd3d5f8acdd0d58ef59 | Scheduled run. Skeleton: type-led, red headline top, clean product cutout (photo 4, plain mockup) centered on a cream field sampled from the print, segmented scale below, logo bottom left, source bottom right. Palette: print red (176,25,41), print cream, oxblood, tree-light gold. Creative director: 1 round, PASS (scores 8/8/8/8/7/8). Round 5 fallback not used. Daily budget: 10 rounds logged when this run started, plus 1 by the parallel ~6 PM test run, so this run's 1 round makes 12 for Nov 19; the cap is now reached. Hard fails all no: text at or above 30 px, facts match ASPCA, cutout clean with no background, no spelling errors, em dashes or headline period, not a near copy of coffee-v4, tree-v3 or black-cat-luck-v2. Optional quick wins: notes at 32 to 34 px, "Least bad" instead of "Mild". Status updates: webhook URL blocked from this sandbox (proxy 403); sent through the n8n connector instead (executions started; delivery to Telegram not confirmed here). Posts Nov 20 3:12 PM CT. Buffer at 6 scheduled after this. Avoided 4619798702 because the parallel test run was working on it. |
| 2026-11-19 9:04 PM CT | 4592258658 Emotionally Nocturnal opossum mug | Infographic, MANUAL photo-free icon pin (Anthony asked for one with no product photography, built from the icon bank): one-spine timeline of the twelve full moon names with their 2027 dates (Jan 22 Wolf to Dec 13 Cold; Sep 15 is the Harvest Moon, nearest the equinox) | Gloock 400 (R4, R5); Young Serif (R2, R3); Cormorant Garamond 700 (R1) | pins/2026-11-20-twelve-moons-v5.jpg (also twelve-moons, -v2, -v3, -v4) | Witchy & Gothic Mugs | 6affb8a7ca85ebefb0ef498a | Manual run from the main chat, not the routine. No photo: type-led, mauve kicker ("For the emotionally nocturnal") and rose headline over a centered gold-moon spine, entries alternating sides, logo bottom left, Almanac credit bottom right. Palette sampled from the mug print (photos/4592258658-1.jpg): warm wine-brown ground, opossum-nose rose headline, flower ivory icons and names, mauve labels, star gold on the moon dots only; April's flower in the rose so the color says pink. Icons (game-icons, one family, ink-normalized to 96 px): wolf-head, snowing, earth-worm (alpha dilated to read solid), flower-emblem, shut-rose, strawberry, deer, double-fish (upper fish only), wheat, archer, beaver, cold-heart. Credit line in the Buffer description. Names checked on almanac.com/full-moon-names; dates cross-checked on several 2027 calendars and by the reviewer against USNO. Creative director: 5 rounds, all FAIL on taste, no hard fail from R2 on; round 5 fallback used (queued the best readable version). R1 mixed outline and solid icons, ragged icon alignment. R2 clip-art grid, no drawn visual, palette too purple. R3 two separate rails, dots meant nothing. R4 thermometer illegible, two flowers adjacent, "Hunter's" read cut off. R5 scores 8/9/7/6/7/8; what it still wanted: icons sized by optical weight (fish and beaver read light), no heart in the Cold icon, the spine centered on the content block (it sits at x 470 to fit "Strawberry Moon"), moons plotted by day of month. Lesson: a photo-free infographic needs its drawn visual planned first; a grid or list of icons fails review. Posts Sun Nov 22 9:30 AM CT (customScheduled). Buffer at 7 scheduled after this. |
