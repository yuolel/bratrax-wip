#!/usr/bin/env python3
"""Render a Bratrax Bulletin header card to PNG.

    python3 bulletin/render-header.py 03 "Subtitle line" out.png

Reads header-template.html, substitutes the issue number and subtitle, and
screenshots it with the headless Chromium that ships in this environment.
Standard library only.

The template links its two typefaces from Google Fonts. Those are fetched and
inlined into a temporary copy before rendering, for one reason: if the fonts
fail to load, Chromium silently falls back to a system sans and produces a card
that is subtly, plausibly wrong. Inlining turns that into a hard failure. The
committed template keeps the plain <link> so it stays readable and editable.
"""

import base64
import os
import re
import subprocess
import sys
import tempfile
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "header-template.html")

# Chromium honours neither a <link> timeout nor a "fonts are ready" signal, so
# give the page a fixed virtual clock to settle in instead.
VIRTUAL_TIME_MS = 8000
WIDTH, HEIGHT, SCALE = 1200, 630, 2

# Google Fonts serves woff2 only to browsers that claim to support it.
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"

CHROME_CANDIDATES = [
    "/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
    "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell",
    "/usr/bin/chromium",
    "/usr/bin/google-chrome",
]


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def inline_fonts(html):
    """Replace the Google Fonts <link> with a <style> carrying the fonts inline."""
    link = re.search(r'<link href="(https://fonts\.googleapis\.com/[^"]+)"[^>]*>', html)
    if not link:
        return html  # no webfont dependency; nothing to do

    css = fetch(link.group(1)).decode("utf-8")
    for font_url in sorted(set(re.findall(r"url\((https://fonts\.gstatic\.com/[^)]+)\)", css))):
        blob = base64.b64encode(fetch(font_url)).decode("ascii")
        css = css.replace(font_url, "data:font/woff2;base64," + blob)

    if "data:font/woff2" not in css:
        raise SystemExit("Fetched the font CSS but found no font files to inline.")

    return html.replace(link.group(0), "<style>\n" + css + "\n</style>")


def find_chrome():
    for path in CHROME_CANDIDATES:
        if os.path.exists(path):
            return path
    raise SystemExit(
        "No Chromium found. Looked in:\n  " + "\n  ".join(CHROME_CANDIDATES)
    )


def main():
    if len(sys.argv) != 4:
        raise SystemExit(
            'usage: render-header.py <issue-number> "<subtitle>" <output.png>'
        )
    issue, subtitle, out = sys.argv[1], sys.argv[2], os.path.abspath(sys.argv[3])

    with open(TEMPLATE, encoding="utf-8") as f:
        html = f.read()

    # Escape before substituting: a subtitle is prose and may legitimately
    # contain & or a quote, which would otherwise break the markup.
    safe = subtitle.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    html = html.replace("{{ISSUE}}", issue.zfill(2)).replace("{{SUBTITLE}}", safe)

    try:
        html = inline_fonts(html)
    except Exception as e:
        raise SystemExit(
            "Could not inline the webfonts, so the card would render in the "
            "wrong typeface. Refusing to produce a misleading image.\n"
            "  %s: %s" % (type(e).__name__, e)
        )

    with tempfile.TemporaryDirectory() as tmp:
        page = os.path.join(tmp, "card.html")
        with open(page, "w", encoding="utf-8") as f:
            f.write(html)

        subprocess.run(
            [
                find_chrome(),
                "--headless",
                "--disable-gpu",
                "--no-sandbox",
                "--hide-scrollbars",
                "--force-device-scale-factor=%d" % SCALE,
                "--window-size=%d,%d" % (WIDTH, HEIGHT),
                "--virtual-time-budget=%d" % VIRTUAL_TIME_MS,
                "--screenshot=" + out,
                "--user-data-dir=" + os.path.join(tmp, "profile"),
                "file://" + page,
            ],
            check=True,
            capture_output=True,
        )

    if not os.path.exists(out) or os.path.getsize(out) < 10_000:
        raise SystemExit("Chromium produced no usable image at " + out)

    print("%s  (%d x %d, %.0f KB)" % (out, WIDTH * SCALE, HEIGHT * SCALE,
                                      os.path.getsize(out) / 1024))


if __name__ == "__main__":
    main()
