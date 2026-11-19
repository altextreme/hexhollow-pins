# hexhollow-pins

Image relay for Hex & Hollow Pinterest pins.

- `queue/photos.txt`: one `listing_id url` per line (Etsy image URLs only). A push runs **Fetch listing photos**, which saves each to `photos/<listing_id>-<n>.jpg`.
- `pins/<name>.jpg.b64`: base64 of a finished pin. A push runs **Decode pins**, which writes `pins/<name>.jpg` and removes the `.b64`.
- Finished pins are served from `https://raw.githubusercontent.com/<owner>/hexhollow-pins/main/pins/<name>.jpg`.
