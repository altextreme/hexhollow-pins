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
for Buffer. Writes through the GitHub connector are text only, so a finished pin is pushed as base64 and an Action
decodes it.

## Repo layout

| Path | What |
|---|---|
| `queue/photos.txt` | One `listing_id url` per line. Only `https://i.etsystatic.com/...` URLs are fetched. `#` lines are comments. |
| `photos/<listing_id>-<n>.jpg` | Written by the **Fetch listing photos** action. `n` counts that listing's lines in the file, top to bottom. |
| `pins/<YYYY-MM-DD>-<slug>.jpg.b64` | Base64 of a finished pin. A push runs **Decode pins**, which writes `pins/<same name>.jpg` and deletes the `.b64`. |
| `pins/<YYYY-MM-DD>-<slug>.jpg` | Finished pins. Served at `https://raw.githubusercontent.com/altextreme/hexhollow-pins/main/pins/<name>.jpg` |
| `assets/` | Logos: `hh-monogram-white-140.png` (monogram, tint it), `hh-logo-monogram-white.png`, `hh-logo-full-white.png`, `hh-logo-full-dark.png`. |
| `assets/fonts/` | Anton 400, Inter 400/500/600, Fraunces 400/600/900 as `.woff` (PIL reads them). SIL OFL licenses alongside. |
| `scripts/` | The two reference pins as runnable PIL scripts. Run from the repo root. Copy the approach, never the layout. |

Both Actions trigger on push to their paths and on workflow_dispatch, share one concurrency group, and their commits
don't retrigger workflows.

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
   Also download what you need from `assets/` and `assets/fonts/` the same way (or clone the repo).
5. **Pick the format.** Rotate so consecutive days differ: list (setlist, playlist, checklist), big-number
   infographic, field guide or labelled diagram, how-to steps, illustration-led quote, comparison or "this or that".
   It must be adjacent value content people save even without buying, with the product as the photo.
   His best pins look like "5 Things to Put in a Pen-Pal Letter".
6. **Design it** in Python/PIL at 1000x1500 (follow the design-taste skill if available).
   - Palette: take medians over small regions of the photo (see `scripts/`). Field = the photo's dominant deep hue,
     darkened but still clearly a color (not gray, not near-black). Headline = one saturated hue from the photo.
     One more accent at most. Everything else neutrals pulled from the photo's lights.
   - Image first, full bleed, under half the page height. Flush left, 64 px margins, strict grid.
   - Type: pick the face for the concept. Faces in `assets/fonts/`; for others, `npm pack @fontsource/<family>`
     if the registry is reachable.
   - Curly quotes and apostrophes. No widows, shadows, gradients, ornaments or em dashes.
   - Logo: `assets/hh-monogram-white-140.png` tinted to the light neutral, wordmark "Hex & Hollow" beside it.
   - Leave a clear pause above the footer; nothing near-touching anything.
   - Downscale to 180 px wide and check the headline and the main element still read.
   - Every fact must be true. Check anything you state. (The "opossums eat 5,000 ticks" claim was debunked; skip
     myths like it.)
   - Save JPEG quality ~80, aim 100 to 190 KB.
7. **Push the pin.** Base64 it (`base64 -w 76`) to `pins/<YYYY-MM-DD>-<slug>.jpg.b64` and commit. Also commit the
   script as `scripts/<YYYY-MM-DD>-<slug>.py`. When Decode pins succeeds, download the raw URL and compare its
   sha256 with the local file.
8. **Queue in Buffer.** Org `68ce2bdb4573424f589bb15a`, Pinterest channel `6a616171e2638b94d7b9e986`.
   `create_post` with `mode: addToQueue`, `schedulingType: automatic`, `assets[0].image.url` = the raw URL plus
   `altText`, `metadata.pinterest.boardServiceId`, `title`, `url` = `https://www.etsy.com/listing/<listing_id>`,
   and `text` = description. Voice: elder emo, goth, wry, "It was never a phase." End the description with 3 to 4
   plain search phrases.
   Boards: apparel `1111967032937184648` (Gothic Graphic Tees & Dark Aesthetic Clothing);
   mugs, tumblers, gifts `1111967032937184649` (Witchy & Gothic Mugs, Tumblers & Gifts);
   wall art `1111967032937184691` (Printable Wall Art); Witchy Vibes `1111967032937184729`.
9. **Append a run log row** below and commit.

## Gotchas

- Buffer's plan caps the org at **10 scheduled posts**. Queue one a day; never batch.
- Buffer fetches the image when it publishes. Never delete or rename a queued pin's file here.
- raw.githubusercontent.com caches for about 5 minutes. Use a new filename for a changed pin; never overwrite.
- This repo is public: listing photos, pins, assets and scripts only. Nothing private, no tokens.
- If any step fails, stop, log it in the run log, and report what failed. Don't queue a half-finished pin.

## Run log

| Date | Listing | Format | Pin file | Board | Buffer post | Notes |
|---|---|---|---|---|---|---|
| 2026-11-19 | 4620217027 Carpool sweatshirt | List (setlist) | pins/2026-11-19-carpool-setlist.jpg | Gothic Graphic Tees | 6afe6c54b16549e9b81edc83 | Posts Nov 19 2:56 PM CT. Image re-hosted here after the old renderer was deleted. |
| 2026-11-19 | 4604532797 Opossum mug | Big-number infographic | pins/2026-11-19-opossum-by-the-numbers.jpg | Witchy & Gothic Mugs | 6afe6e0259eff0b616d91629 | Posts Nov 19 4:28 PM CT. End-to-end test of this pipeline. |
