#!/usr/bin/env python3
"""Anonymise the raw Slack captures: photo -> initial tile, name -> "Julia".

Everything else in the capture is left untouched. These are real screenshots
going to a Slack reviewer who will compare them against the working app, so the
edits are deliberately limited to identity.

Two things make the name swap invisible rather than obviously pasted:

  * Slack's UI face is Lato, so the replacement is drawn in real Lato rather
    than a lookalike.
  * The point size is not guessed. Each capture was taken at a different UI
    scale, so the size is solved for by re-rendering the ORIGINAL string and
    binary-searching until its width matches the pixels being replaced.

"Julia" is much shorter than "Yuliya from Bratrax", so the timestamp that sits
beside it is erased and redrawn too — leaving it in place would open a gap that
never occurs in Slack, which is exactly the kind of tell that reads as doctored.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).parent
FONTS = HERE / "fonts"
BOLD = str(FONTS / "Lato-bold.ttf")
REGULAR = str(FONTS / "Lato-regular.ttf")

OLD_NAME = "Yuliya from Bratrax"
NEW_NAME = "Julia"

SLACK_INK = (29, 28, 29)      # #1D1C1D — Slack's primary text
SLACK_GRAY = (97, 96, 97)     # #616061 — timestamps and metadata
TILE = (124, 111, 100)        # warm neutral, same family as the Bratrax cream
WHITE = (255, 255, 255)


@dataclass
class Occurrence:
    """One "<avatar> <name> <timestamp>" header inside a capture.

    The boxes are generous search hints, not measurements — the exact pixel
    bounds are found inside them. `name_row` must be tight enough vertically to
    exclude the message text on the line below.
    """

    avatar: tuple[int, int, int, int]
    name_row: tuple[int, int, int, int]
    timestamp: str


def tight_bbox(im: Image.Image, box, thresh: int = 170):
    """Bounds of everything darker than `thresh` inside `box`, in image coords."""
    region = im.crop(box).convert("L")
    mask = region.point(lambda p: 255 if p < thresh else 0)
    bb = mask.getbbox()
    if bb is None:
        raise ValueError(f"nothing darker than {thresh} inside {box}")
    return (box[0] + bb[0], box[1] + bb[1], box[0] + bb[2], box[1] + bb[3])


def split_at_widest_gap(im: Image.Image, box, thresh: int = 170) -> int:
    """x of the widest run of blank columns in `box` — the name/timestamp gap.

    Word spaces inside "Yuliya from Bratrax" are narrower than the gap before
    the timestamp, so the widest run is reliably the one we want.
    """
    region = im.crop(box).convert("L")
    w, h = region.size
    px = region.load()
    blank = [all(px[x, y] >= thresh for y in range(h)) for x in range(w)]

    best_len = best_start = 0
    run_start = None
    for x, is_blank in enumerate(blank + [False]):
        if is_blank and run_start is None:
            run_start = x
        elif not is_blank and run_start is not None:
            if x - run_start > best_len:
                best_len, best_start = x - run_start, run_start
            run_start = None
    if best_len == 0:
        raise ValueError(f"no gap found in {box}")
    return box[0] + best_start


def fit_size(text: str, target_w: int, font_path: str) -> ImageFont.FreeTypeFont:
    """Largest size whose rendered width does not exceed `target_w`."""
    lo, hi = 6, 80
    while lo < hi:
        mid = (lo + hi + 1) // 2
        f = ImageFont.truetype(font_path, mid)
        if f.getbbox(text)[2] - f.getbbox(text)[0] <= target_w:
            lo = mid
        else:
            hi = mid - 1
    return ImageFont.truetype(font_path, lo)


def patch(src: Path, dst: Path, occurrences: list[Occurrence]) -> None:
    im = Image.open(src).convert("RGB")
    draw = ImageDraw.Draw(im)

    for i, occ in enumerate(occurrences, 1):
        # --- header text: measure, erase, redraw ---
        row = tight_bbox(im, occ.name_row)
        gap_x = split_at_widest_gap(im, row)
        name_box = (row[0], row[1], gap_x, row[3])
        name_w = name_box[2] - name_box[0]

        name_font = fit_size(OLD_NAME, name_w, BOLD)
        # Slack's timestamp is a couple of points down from the name; derive it
        # from the same fit rather than hardcoding a ratio.
        stamp_font = ImageFont.truetype(REGULAR, max(8, round(name_font.size * 0.92)))

        # Erase the whole header line, with a margin for antialiasing.
        draw.rectangle((row[0] - 2, row[1] - 4, row[2] + 4, row[3] + 4), fill=WHITE)

        # Baseline-align both runs on the original name's top edge.
        n_off = name_font.getbbox(NEW_NAME)
        draw.text((row[0] - n_off[0], row[1] - n_off[1]), NEW_NAME,
                  font=name_font, fill=SLACK_INK)

        name_end = row[0] + (n_off[2] - n_off[0])
        space = round(name_font.size * 0.55)
        s_off = stamp_font.getbbox(occ.timestamp)
        # Sit the timestamp's cap height on the name's, not its box top —
        # the smaller face would otherwise ride high.
        stamp_y = row[1] + (name_font.size - stamp_font.size) - s_off[1] + 1
        draw.text((name_end + space - s_off[0], stamp_y), occ.timestamp,
                  font=stamp_font, fill=SLACK_GRAY)

        # --- avatar: photo out, initial tile in ---
        # 235 rather than something closer to white: the photo's rounded
        # corners are antialiased, and a looser threshold swallows that halo
        # into the bbox and oversizes the tile. Average the two sides for the
        # same reason — the avatar is square, so a stray edge pixel on one
        # axis should not stretch it.
        av = tight_bbox(im, occ.avatar, thresh=235)
        size = round(((av[2] - av[0]) + (av[3] - av[1])) / 2)
        draw.rectangle((av[0] - 3, av[1] - 3, av[0] + size + 3, av[1] + size + 3),
                       fill=WHITE)
        draw.rounded_rectangle((av[0], av[1], av[0] + size, av[1] + size),
                               radius=max(2, round(size * 0.18)), fill=TILE)
        initial_font = ImageFont.truetype(BOLD, max(8, round(size * 0.52)))
        draw.text((av[0] + size / 2, av[1] + size / 2), NEW_NAME[0],
                  font=initial_font, fill=WHITE, anchor="mm")

        print(f"  {src.name} #{i}: name {name_box} -> Lato Bold {name_font.size}px, "
              f"avatar {size}px")

    im.save(dst, "PNG")


def patch_account_chip(src: Path, dst: Path, search: tuple[int, int, int, int],
                       fill: tuple[int, int, int]) -> None:
    """Redraw the Bratrax header's account chip with the new initial.

    Not a Slack capture, so none of the header machinery above applies — the
    chip is a solid square of one known colour, so it is located by matching
    that colour rather than by luminance.
    """
    im = Image.open(src).convert("RGB")
    region = im.crop(search)
    px = region.load()
    hits = [
        (x, y)
        for x in range(region.width)
        for y in range(region.height)
        if all(abs(px[x, y][c] - fill[c]) < 24 for c in range(3))
    ]
    if not hits:
        raise ValueError(f"no chip matching {fill} inside {search}")

    x0 = search[0] + min(x for x, _ in hits)
    y0 = search[1] + min(y for _, y in hits)
    x1 = search[0] + max(x for x, _ in hits)
    y1 = search[1] + max(y for _, y in hits)

    draw = ImageDraw.Draw(im)
    draw.rectangle((x0, y0, x1, y1), fill=fill)
    font = ImageFont.truetype(str(FONTS / "Outfit-bold.ttf"),
                              max(8, round((y1 - y0) * 0.62)))
    draw.text(((x0 + x1) / 2, (y0 + y1) / 2 + 1), NEW_NAME[0],
              font=font, fill=WHITE, anchor="mm")
    im.save(dst, "PNG")
    print(f"  {dst.name}: account chip {x1 - x0 + 1}x{y1 - y0 + 1} -> '{NEW_NAME[0]}'")


# Hints were read off 3x zooms of each header strip. Every capture was taken at
# a different UI scale, which is why none of these numbers repeat.
JOBS = [
    (
        "raw-campaign-table.png", "shot-campaign-table.png",
        [Occurrence(avatar=(8, 18, 60, 70), name_row=(62, 20, 480, 43),
                    timestamp="1 minute ago")],
    ),
    (
        "raw-channel-trend.png", "shot-channel-trend.png",
        [Occurrence(avatar=(10, 12, 62, 64), name_row=(64, 14, 470, 39),
                    timestamp="Yesterday at 1:48 PM")],
    ),
    (
        "raw-follow-up.png", "shot-follow-up.png",
        [
            Occurrence(avatar=(22, 10, 84, 72), name_row=(86, 18, 560, 46),
                       timestamp="1 minute ago"),
            Occurrence(avatar=(22, 306, 84, 372), name_row=(86, 316, 560, 344),
                       timestamp="Just now"),
        ],
    ),
    (
        "raw-chart.png", "shot-chart.png",
        [Occurrence(avatar=(12, 14, 62, 64), name_row=(64, 16, 430, 40),
                    timestamp="19 minutes ago")],
    ),
]

if __name__ == "__main__":
    originals = HERE / "originals"
    shots = HERE / "shots"
    shots.mkdir(exist_ok=True)

    for src_name, dst_name, occs in JOBS:
        patch(originals / src_name, shots / dst_name, occs)

    # The follow-up capture caught the leading edge of the next message below
    # the thread. Left in, that reads as a crop artefact rather than as part of
    # the answer. (channel-trend was re-cropped at source, so it needs nothing.)
    p = shots / "shot-follow-up.png"
    with Image.open(p) as im:
        w = im.width
        im.crop((0, 0, w, 590)).save(p, "PNG")
    print(f"  shot-follow-up.png: trimmed to {w}x590 (next message peeking in)")

    # The Bratrax settings captures carry no Slack chrome — only the account
    # chip in the header needs the initial swapped. Both themes render that chip
    # in the same violet, so one colour serves both.
    for theme in ("light", "dark"):
        patch_account_chip(
            originals / f"raw-settings-{theme}.png",
            shots / f"shot-settings-{theme}.png",
            search=(1740, 0, 1832, 70), fill=(86, 85, 255),
        )

    # The dark capture ran on past the page and caught a half-drawn tooltip in
    # the bottom 14px. Cutting there would leave the acid "connect another
    # workspace" button — the actual call to action, and the reason this image
    # exists — flush against the crop, so the page background is extended back
    # underneath it instead. Only background is synthesised; no content moves.
    p = shots / "shot-settings-dark.png"
    with Image.open(p) as im:
        w = im.width
        body = im.crop((0, 0, w, 877))
        bg = im.getpixel((60, 700))          # left margin, clear of the card
        padded = Image.new("RGB", (w, 877 + 22), bg)
        padded.paste(body, (0, 0))
        padded.save(p, "PNG")
    print(f"  shot-settings-dark.png: tooltip cut, background extended -> {w}x899")

    # No name or photo in the Messages-tab capture; it only needs the stray
    # half-rendered element at the bottom edge trimmed off.
    prompts = Image.open(originals / "raw-prompts.png").convert("RGB")
    prompts.crop((0, 0, 1400, 668)).save(shots / "shot-prompts.png", "PNG")
    print("  shot-prompts.png: cropped to 1400x668 (trimmed clipped element)")
