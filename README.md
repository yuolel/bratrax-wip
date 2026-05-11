# bratrax-wip

Source for [bratrax.com](https://bratrax.com) and related Bratrax web properties. The production site is served from the `bratrax-com-static` branch.

## Heads-up: hosting only serves a subset of the repo

The hosting that serves bratrax.com **does not expose subdirectories** like `assets/`, `dashboards/`, or `partials/` from the deployed branch at the public URL.

Concretely, the following do **not** load from the public site even though the files exist on `bratrax-com-static`:

- `https://bratrax.com/assets/anything.png`
- `https://bratrax.com/dashboards/anything.png`
- `https://bratrax.com/partials/footer.html`

Only top-level files (e.g. `/favicon.svg`, `/favicon.png`) and HTML routes (`/`, `/faq`, `/privacy-policy`, `/terms-of-service`, `/vs/hyros`, `/vs/triple-whale`) are reliably served.

If you reference an image from `/assets/...` in a page, **the image will 404 on production** even though the file is committed and merged.

## What to do instead

The legal pages (`privacy/index.html`, `terms/index.html`) and the comparison pages (`vs/hyros/`, `vs/triple-whale/`) already work around this. Match what they do:

### 1. For the Bratrax logo and any other SVG: inline it

Do **not** do this:

```html
<img src="/assets/Bratrax%20Logo%20Light%20Inline.svg" alt="Bratrax">
```

Do this — paste the SVG markup directly into the HTML:

```html
<svg width="189" height="26" viewBox="0 0 189 26" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Bratrax">
  <path d="..." fill="#E8E4DC"/>
  …
</svg>
```

You can copy the full logo SVG from `privacy/index.html` on the `bratrax-com-static` branch.

CSS that targets `.brand-mark img` should also target `.brand-mark svg`:

```css
.brand-mark img,
.brand-mark svg { height: 22px; width: auto; display: block; }
```

### 2. For PNGs and other binary assets: load from GitHub Raw

Replace `/assets/foo.png` and `/dashboards/foo.png` references with the equivalent `raw.githubusercontent.com` URL pointing at the `bratrax-com-static` branch:

```html
<!-- ❌ Broken on production -->
<img src="/assets/brat-portrait-big.png" alt="Brat Vukovich">

<!-- ✅ Loads from GitHub Raw -->
<img src="https://raw.githubusercontent.com/yuolel/bratrax-wip/bratrax-com-static/assets/brat-portrait-big.png" alt="Brat Vukovich">
```

URL pattern:

```
https://raw.githubusercontent.com/yuolel/bratrax-wip/bratrax-com-static/<path/from/repo/root>
```

### 3. For the shared footer partial: fetch from GitHub Raw

The shared footer at `partials/footer.html` is loaded at runtime via `fetch()`. Do not fetch it from `bratrax.com/partials/...` — that 404s. Fetch from GitHub Raw instead:

```html
<div id="brx-footer">
  <!-- inline fallback footer here so the page still has a footer if the fetch fails -->
</div>
<script>
  fetch('https://raw.githubusercontent.com/yuolel/bratrax-wip/bratrax-com-static/partials/footer.html')
    .then(function(r){ if(!r.ok) throw new Error('bad status'); return r.text(); })
    .then(function(html){ document.getElementById('brx-footer').innerHTML = html; })
    .catch(function(){});
</script>
```

Updating `partials/footer.html` on the `bratrax-com-static` branch updates every page that fetches it (subject to GitHub Raw's CDN cache, typically a few minutes).

## Caveats with GitHub Raw

- GitHub Raw has rate limits and is not designed for production traffic. It works fine at current volume; if traffic grows significantly, move assets to proper hosting (CDN or hosting that serves the deployed branch's subdirectories).
- Always pin the URL to a specific branch (`bratrax-com-static`), not a commit SHA, so updates propagate automatically.

## Long-term fix

The proper fix is for the hosting provider to serve all directories from `bratrax-com-static`. Until that happens, follow the patterns above.

## Repo layout

- `bratrax-com-static` — production branch served at bratrax.com
- `main` — repo docs (this file)
- `claude/*` — short-lived working branches
- `partials/footer.html` — shared dynamic footer (lives on `bratrax-com-static`)
- `assets/` — images used by HTML pages
- `dashboards/` — dashboard screenshots
- `og/` — Open Graph / Twitter social cards
- `privacy/`, `terms/`, `vs/`, `faq/` — page directories, each with an `index.html`
- `index.html` — landing page (bratrax.com homepage)
