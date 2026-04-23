# bratrax.com — static site

This branch holds the content for the apex `bratrax.com` domain. It's separate from the app repo (which currently serves the login at this domain) so content/legal pages can ship without coupling to app deploys.

## Context

- Bratrax Lite launches May 12. Until then, `lite.bratrax.com` serves a waitlist (hosted separately on Coolify from the `waitlist` branch of this repo).
- Historically `bratrax.com` has redirected to the app login. Going forward we need it to serve a few routes (see below) while keeping the login working.
- This branch exists to be deployed alongside the app on Hetzner.

## What bratrax.com needs to do

| URL | Behavior |
|---|---|
| `https://bratrax.com/` | 302 redirect → `https://lite.bratrax.com/` (temporary, until a real landing page replaces it) |
| `https://bratrax.com/privacy-policy` | Serve `privacy/index.html` |
| `https://bratrax.com/terms-of-service` | Serve `terms/index.html` |
| `https://bratrax.com/partials/footer.html` | Serve with `Access-Control-Allow-Origin: *` — fetched cross-origin by `lite.bratrax.com` and any future subdomains |
| `https://bratrax.com/login` | **Must keep working** — continues to serve the app login wherever it currently routes to |

## File structure in this branch

```
privacy/index.html     → https://bratrax.com/privacy-policy
terms/index.html       → https://bratrax.com/terms-of-service
partials/footer.html   → https://bratrax.com/partials/footer.html
```

No root `index.html` on purpose — root path is a redirect.

## Required Nginx config

```nginx
# Root path: temporary redirect to Lite waitlist until launch
location = / {
    return 302 https://lite.bratrax.com/;
}

# CORS for the shared footer partial (fetched by lite.bratrax.com)
location /partials/ {
    add_header Access-Control-Allow-Origin *;
    add_header Cache-Control "public, max-age=300";
}

# App login stays on its existing upstream — preserve however it's currently routed
# (likely a proxy_pass to the app container or a separate location /login block)

# Everything else serves statically from the file tree
```

## Deployment handoff

1. Clone this repo, checkout `bratrax-com-static` branch.
2. Serve the three directories (`privacy/`, `terms/`, `partials/`) from your Hetzner setup alongside the existing app.
3. Apply the Nginx config above, keeping whatever handles `/login` today intact.
4. Once deployed, tell Yuliya (`yuliya@inceptly.com`) the target IP or hostname for `bratrax.com`. She'll update the A record in Namecheap so DNS points at Hetzner.
5. Coordinate cutover — the old Namecheap-level redirect comes down the moment the new site is live.

## Verification after DNS switch

- [ ] `https://bratrax.com/` → 302 → `https://lite.bratrax.com/`
- [ ] `https://bratrax.com/privacy-policy` → HTML loads
- [ ] `https://bratrax.com/terms-of-service` → HTML loads
- [ ] `https://bratrax.com/partials/footer.html` → raw HTML, response header `Access-Control-Allow-Origin: *`
- [ ] `https://bratrax.com/login` → app login still works
- [ ] Cross-origin fetch from `https://lite.bratrax.com/a/` succeeds (DevTools → Network → the `footer.html` request should be 200 and the footer should render at the bottom of the page)

## Ongoing maintenance

- **Footer updates:** edit `partials/footer.html` on this branch, commit, push. Cached 5 minutes, so changes propagate within that window.
- **New legal pages:** drop an `index.html` into a new directory (e.g. `dpa/index.html` for a DPA page) and it's served at `/dpa` automatically.
- **When the real bratrax.com landing page is ready:** add an `index.html` at the repo root and remove the root-redirect Nginx block. `/privacy`, `/terms`, `/partials/` keep working unchanged.

## Who to ping

- **Yuliya** (`yuliya@inceptly.com`) — owns `lite.bratrax.com`, the footer content, the waitlist, and coordinates the DNS switch.
- **Brat** — anything about the app login routing, the domain overall, or strategic direction.

---

*Originally prepared for a Coolify deploy that got rolled back to consolidate infra with the app on Hetzner. The commit history on this branch starts clean — no prior Coolify artifacts.*
