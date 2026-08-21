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


# Hints were read off 3x zooms of each header strip. The three captures were
# taken at different UI scales, which is why none of these numbers repeat.
JOBS = [
    (
        "raw-chart.png", "shot-chart.png",
        [Occurrence(avatar=(12, 14, 62, 64), name_row=(64, 16, 430, 40),
                    timestamp="19 minutes ago")],
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
]

if __name__ == "__main__":
    originals = HERE / "originals"
    shots = HERE / "shots"
    shots.mkdir(exist_ok=True)

    for src_name, dst_name, occs in JOBS:
        patch(originals / src_name, shots / dst_name, occs)

    # The follow-up capture caught the top hairline of the next message.
    # Left in, it reads as a crop artefact rather than as part of the thread.
    fu = shots / 'shot-follow-up.png'
    with Image.open(fu) as im:
        im.crop((0, 0, im.width, 590)).save(fu, 'PNG')
    print('  shot-follow-up.png: trimmed to 1200x590 (stray divider)')

    # No name or photo in the Messages-tab capture; it only needs the stray
    # half-rendered element at the bottom edge trimmed off.
    prompts = Image.open(originals / "raw-prompts.png").convert("RGB")
    prompts.crop((0, 0, 1400, 668)).save(shots / "shot-prompts.png", "PNG")
    print("  shot-prompts.png: cropped to 1400x668 (trimmed clipped element)")
