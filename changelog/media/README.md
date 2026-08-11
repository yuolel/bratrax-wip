# Changelog entry images

Screenshots shown inside entries on <https://bratrax.com/changelog>.

Keep this in sync with the image standard in
`scripts/release_comms/PROMPT.md` in the `vidtao/bratrax` repo — the weekly
release-comms routine follows the same rules when it requests a screenshot.

## Naming

One file per entry, named for that entry's slug — the `id` on its `<h3>` in
`changelog/index.html`:

| Entry `<h3 id="...">` | File |
| --- | --- |
| `amazon-integration` | `amazon-integration.png` |
| `support-chat` | `support-chat.png` |

## How to reference one

**The image goes after the entry text, not before it** — the reader gets the
point in words first, then the illustration. It sits outside the `.a` body div,
as the last child of the `<article>`, and is width-capped:

```html
<article class="cl-entry" data-type="New">
  <h3 id="amazon-integration">Connect Amazon Ads and Amazon Seller Central to Bratrax<span class="cl-tag cl-tag-inline" style="color:var(--color-acid)">New</span></h3>
  <div class="a"><p>…</p></div>
  <img src="https://raw.githubusercontent.com/yuolel/bratrax-wip/bratrax-com-static/changelog/media/amazon-integration.png"
       alt="Settings → Connections listing Amazon Ads and Amazon Seller Central, each with a Connect button"
       style="max-width:600px;margin-top:16px">
</article>
```

Use the absolute `raw.githubusercontent.com` URL rather than a relative path —
that's the convention the homepage already uses for its `dashboards/*.png`
product shots, and it resolves regardless of how the page is served.

## Specs

- **Placement:** after the entry text, last child of the `<article>`.
- **Display width:** **`max-width:600px`** — roughly two-thirds of the ~916px
  content column. The page's CSS defaults entry images to full width, which is
  too dominant for a UI screenshot, so the inline cap is required. Use the same
  cap on every image so they form a consistent column.
- **Capture width:** **1000px or wider**, so the screenshot is *downscaled*
  into the cap. Anything narrower gets upscaled and looks visibly soft.
- **Shape:** landscape. A portrait capture becomes a tall block that swamps the
  entry — recapture wider rather than shipping one.
- **Format:** PNG. Use a GIF only when motion genuinely carries the meaning —
  a few seconds of UI is easily 2–5 MB versus ~200 KB for a PNG, and would
  dominate the weight of an otherwise very light page.
- **Weight:** roughly **100–250 KB**, the band the existing `dashboards/*.png`
  shots sit in. Crop to the relevant region instead of shipping a full 4K
  desktop capture.
- **Theme:** dark UI — it matches the changelog page's own palette.
- **Alt text:** always. The page carries JSON-LD and cares about SEO, and it's
  the accessible default. Describe what is shown, using the app's real labels
  (e.g. "Settings → Connections", not "the Integrations tab").
- **Check it loads:** open the `raw.githubusercontent.com` URL before merging.
  A broken image is worse than no image.

## Which entries get an image

Only ones with a distinct visual surface a customer would recognise: a new
dashboard or panel, a new UI control, a new connector card, a new settings
screen.

Skip entries where there is nothing meaningful to show — bug fixes,
performance improvements, backend attribution changes, or anything whose only
"visual" is a number that looks the same as before.

Images are always optional. Every entry is written to read completely on its
own, so a missing screenshot never blocks publishing.
