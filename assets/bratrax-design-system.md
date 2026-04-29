# Bratrax Design System

**Version:** 1.2
**Last Updated:** 2026-04-29
**Brand:** Bratrax — Service-as-Software Analytics
**Aesthetic:** Contrarian, editorial, anti-BI-tool. Halftone print meets graph paper meets screen-print energy. Dark, technical, strategic color pops.

---

## Table of Contents

1. [Color System](#color-system)
2. [Typography](#typography)
3. [Spacing Scale](#spacing-scale)
4. [Visual Texture System](#visual-texture-system)
5. [Component Styles](#component-styles)
6. [Color Pairing Rules](#color-pairing-rules)
7. [The Logo](#the-logo)
8. [Brand Personality](#brand-personality)

---

## Color System

### Core Palette

| Token | Name | Hex | RGB | Usage |
|---|---|---|---|---|
| `color-bg` | Near Black | `#0A0A0A` | 10, 10, 10 | Primary background |
| `color-surface` | Off Black | `#141414` | 20, 20, 20 | Card surfaces, elevated backgrounds |
| `color-surface-hover` | Dark | `#1E1E1E` | 30, 30, 30 | Hover states on surfaces |
| `color-border` | Mid Gray | `#3A3A3A` | 58, 58, 58 | Borders, dividers, card edges |
| `color-text-muted` | Muted | `#858585` | 133, 133, 133 | Secondary text, labels, captions |
| `color-text-secondary` | Light Gray | `#B0B0B0` | 176, 176, 176 | Paragraph body text |
| `color-text` | Off White | `#E8E4DC` | 232, 228, 220 | Primary text color |
| `color-text-bright` | White | `#FAFAF5` | 250, 250, 245 | Headlines, maximum emphasis |

### Accent Colors

| Token | Name | Hex / Value | RGB | Usage |
|---|---|---|---|---|
| `color-acid` | Acid Green | `#D4FF00` | 212, 255, 0 | Primary accent — CTAs, highlights, the logo dot, positive emphasis |
| `color-acid-dim` | Acid Dim | `rgba(212,255,0,0.08)` | — | Subtle acid backgrounds, eyebrow badges |
| `color-acid-mid` | Acid Mid | `rgba(212,255,0,0.25)` | — | Borders with acid tint, graph paper lines |
| `color-red` | Tomato Red | `#FF3B30` | 255, 59, 48 | Strikethroughs, falsification motif, negative trends, "what's wrong" |
| `color-blue` | Cyan | `#00D4FF` | 0, 212, 255 | Tertiary accent — used very sparingly for data viz variety |
| `color-lavender` | Lavender | `#B4A0FF` | 180, 160, 255 | Quaternary — reserved, barely used, only if needed |

### CSS Custom Properties

```css
:root {
  /* Core */
  --color-bg: #0A0A0A;
  --color-surface: #141414;
  --color-surface-hover: #1E1E1E;
  --color-border: #3A3A3A;
  --color-text-muted: #858585;
  --color-text-secondary: #B0B0B0;
  --color-text: #E8E4DC;
  --color-text-bright: #FAFAF5;

  /* Accents */
  --color-acid: #D4FF00;
  --color-acid-dim: rgba(212, 255, 0, 0.08);
  --color-acid-mid: rgba(212, 255, 0, 0.25);
  --color-red: #FF3B30;
  --color-blue: #00D4FF;
  --color-lavender: #B4A0FF;
}
```

---

## Typography

### Font Stack

| Role | Font Family | Weights | Fallback | Usage |
|---|---|---|---|---|
| Display | Outfit | 300-900 | Helvetica Neue, sans-serif | Headlines, section titles (weight 900 for big headlines) |
| Serif Accent | DM Serif Display | 400 italic | Georgia, serif | Single-word emphasis within headlines — always italic, always one word per headline |
| Monospace | Space Mono | 400, 700 | JetBrains Mono, monospace | Logo, section labels, technical data, nav items, buttons, coordinates |
| Body | Outfit | 300, 400 | sans-serif | Paragraph text, descriptions |

### Google Fonts Import

```html
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@1&family=Outfit:wght@300;400;600;700;900&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
```

### Type Scale (Web)

| Token | Font | Size | Weight | Line Height | Letter Spacing | Usage |
|---|---|---|---|---|---|---|
| `type-hero` | Outfit | `clamp(44px, 5.5vw, 76px)` | 900 | 1.05 | -0.5px | Hero headline |
| `type-h2` | Outfit | `clamp(36px, 4.5vw, 60px)` | 900 | 1.15 | -0.1px | Section headlines |
| `type-h3` | Outfit | `clamp(24px, 2.6vw, 34px)` | 900 | 1.2 | 0 | Subsection headlines |
| `type-h4` | Outfit | 22px | 900 | 1.3 | +0.3px | Card titles, FAQ questions |
| `type-serif-accent` | DM Serif Display | inherits from parent | 400 italic | inherits | inherits | Single emphasized word in a headline |
| `type-body` | Outfit | 17px | 300 | 1.7-1.85 | 0 | Body paragraphs |
| `type-mono-label` | Space Mono | 11px | 700 | — | 2px | Section labels ("01 — THE PROBLEM"), nav links |
| `type-mono-small` | Space Mono | 12px | 400 | 1.7 | 0.5px | Footnotes, technical text |
| `type-button` | Space Mono | 12px | 700 | — | 1.5px | Button text (uppercase) |

### Typography Rules

1. **Headlines** use Outfit at weight 900 across all levels (H1–H4). Weight stays constant; size, line-height, and letter-spacing are what change as the hierarchy descends.
2. **Letter-spacing — per-token defaults with a global envelope.** Outfit 900 has dense glyph forms; tracking is the single most common readability failure. Each heading token carries a fixed default value (see Type Scale table) — that's the canonical setting for that level. Deviation from a token default requires explicit reason and must stay within the global envelope. Limits per surface:
   - **Headlines (Outfit 900):** envelope `-0.5px` to `+0.5px`. Token defaults: H1 `-0.5px` · H2 `-0.1px` · H3 `0` · H4 `+0.3px`. Going tighter than `-0.5px` causes adjacent letters to smush (common pairs like `Th`, `Wh`, `Sa`). Going looser than `+0.5px` makes headlines read as labels rather than headings. If a headline looks loose at these limits, **reduce font size before tightening spacing.**
   - **Body text (Outfit 300):** always `0`. Never negative-track body copy.
   - **Space Mono labels:** `0` to `+2px`. Positive spacing only.
   - **DM Serif Display italic accents:** `0` to `-0.5px` maximum. Italics need air, especially next to Outfit 900.
3. **One word per headline** may be wrapped in DM Serif Display italic for emphasis. It inherits the size of the parent headline but the font change creates the accent.
4. The **serif accent word** should carry the insight — "skips", "why", "deciding", "another one" — not filler words.
5. **Body text** is Outfit weight 300 at 17px. Color is `color-text-secondary` (#B0B0B0).
6. All **technical/UI text** (nav, buttons, labels, section numbers) is Space Mono.
7. The **serif accent word** in headlines always gets acid green color (`#D4FF00`).
8. **No orphan words.** Headlines, pull quotes, and short text blocks must not leave a single word alone on the last line. Use `text-wrap: balance` in CSS for headlines/pull quotes. For specific cases, use `&nbsp;` between the last two words to prevent the break. Check at both desktop and mobile widths.

### CSS Type Tokens

```css
/* Hero headline */
.type-hero {
  font-family: 'Outfit', 'Helvetica Neue', sans-serif;
  font-size: clamp(44px, 5.5vw, 76px);
  font-weight: 900;
  line-height: 1.05;
  letter-spacing: -0.5px;
  color: var(--color-text-bright);
}

/* Section headline */
.type-h2 {
  font-family: 'Outfit', 'Helvetica Neue', sans-serif;
  font-size: clamp(36px, 4.5vw, 60px);
  font-weight: 900;
  line-height: 1.15;
  letter-spacing: -0.1px;
  color: var(--color-text-bright);
}

/* Subsection headline */
.type-h3 {
  font-family: 'Outfit', 'Helvetica Neue', sans-serif;
  font-size: clamp(24px, 2.6vw, 34px);
  font-weight: 900;
  line-height: 1.2;
  letter-spacing: 0;
  color: var(--color-text-bright);
}

/* Card title / FAQ question */
.type-h4 {
  font-family: 'Outfit', 'Helvetica Neue', sans-serif;
  font-size: 22px;
  font-weight: 900;
  line-height: 1.3;
  letter-spacing: 0.3px;
  color: var(--color-text-bright);
}

/* Serif accent — single word within headline */
.type-serif-accent {
  font-family: 'DM Serif Display', Georgia, serif;
  font-style: italic;
  font-weight: 400;
  color: var(--color-acid);
}

/* Body text */
.type-body {
  font-family: 'Outfit', sans-serif;
  font-size: 17px;
  font-weight: 300;
  line-height: 1.7;
  color: var(--color-text-secondary);
}

/* Section label */
.type-mono-label {
  font-family: 'Space Mono', 'JetBrains Mono', monospace;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: rgba(212, 255, 0, 0.7);
}

/* Technical text / footnotes */
.type-mono-small {
  font-family: 'Space Mono', 'JetBrains Mono', monospace;
  font-size: 12px;
  font-weight: 400;
  line-height: 1.7;
  letter-spacing: 0.5px;
  color: var(--color-text-muted);
}

/* Button text */
.type-button {
  font-family: 'Space Mono', 'JetBrains Mono', monospace;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 1.5px;
  text-transform: uppercase;
}
```

---

## Spacing Scale

**Base unit:** 8px

| Token | Value | Usage |
|---|---|---|
| `space-xs` | 8px | Tight gaps |
| `space-sm` | 16px | Between related items |
| `space-md` | 24px | Between paragraphs, label to heading |
| `space-lg` | 32px | Card internal padding |
| `space-xl` | 48px | Between sections within a page section |
| `space-2xl` | 64px | Major section breaks |
| `space-3xl` | 140px | Page section padding (top/bottom) |

### CSS Spacing Tokens

```css
:root {
  --space-xs: 8px;
  --space-sm: 16px;
  --space-md: 24px;
  --space-lg: 32px;
  --space-xl: 48px;
  --space-2xl: 64px;
  --space-3xl: 140px;
}
```

---

## Visual Texture System

### 1. Graph Paper Grid

Fixed background overlay with acid green lines at 4% opacity, 40px grid spacing.

```css
.graph-paper-grid {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
  background-image:
    linear-gradient(rgba(212, 255, 0, 0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(212, 255, 0, 0.04) 1px, transparent 1px);
  background-size: 40px 40px;
}
```

### 2. Halftone Dither

Radial-gradient dot patterns using acid green dots (1.5-2.5px) at various opacities. Used for decorative backgrounds and hero elements.

```css
.halftone-dither {
  background-image: radial-gradient(
    rgba(212, 255, 0, 0.15) 1.5px,
    transparent 1.5px
  );
  background-size: 8px 8px;
}
```

### 3. Dithered Red Square

Rotated square with red halftone dots. Used very sparingly as a decorative tension element.

```css
.dithered-red-square {
  width: 120px;
  height: 120px;
  transform: rotate(12deg);
  background-image: radial-gradient(
    rgba(255, 59, 48, 0.25) 2px,
    transparent 2px
  );
  background-size: 6px 6px;
}
```

### 4. No noise/grain overlay

Noise/grain overlays were tested and rejected due to rendering issues.

---

## Component Styles

### Buttons

**Primary Button:**
```css
.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 14px 32px;
  background: var(--color-acid);
  color: #000;
  font-family: 'Space Mono', monospace;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  border: none;
  cursor: pointer;
  text-decoration: none;
  transition: opacity 0.2s, transform 0.2s;
}

.btn-primary:hover {
  opacity: 0.88;
  transform: translateY(-1px);
}
```

**Outline Button:**
```css
.btn-outline {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 14px 32px;
  background: transparent;
  border: 1px solid var(--color-border);
  color: var(--color-text);
  font-family: 'Space Mono', monospace;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  cursor: pointer;
  text-decoration: none;
  transition: border-color 0.2s;
}

.btn-outline:hover {
  border-color: var(--color-acid);
}
```

### Cards

**Definition / Method Card:**
```css
.card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  padding: var(--space-lg);
  position: relative;
  transition: background 0.2s;
  /* No border-radius — sharp edges for editorial feel */
}

.card:hover {
  background: var(--color-surface-hover);
}

/* Top accent bar — 4px, color varies per card */
.card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: var(--card-accent-color, var(--color-acid));
}

/* Variants */
.card--acid { --card-accent-color: var(--color-acid); }
.card--red { --card-accent-color: var(--color-red); }
.card--blue { --card-accent-color: var(--color-blue); }
```

### Section Labels

Format: `"01 — THE PROBLEM"`

```css
.section-label {
  font-family: 'Space Mono', monospace;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: rgba(212, 255, 0, 0.7);
}
```

### Flip Cards (Contrast Section)

```css
.flip-card {
  perspective: 1000px;
  cursor: pointer;
}

.flip-card-inner {
  border: 1px dashed var(--color-border);
  transition: transform 0.6s;
  transform-style: preserve-3d;
}

.flip-card:hover .flip-card-inner {
  transform: rotateY(180deg);
}

/* Front side */
.flip-card-front {
  /* "WHAT THEY TOLD YOU" label in red */
  /* Quote in Outfit 22px weight 700 */
  /* "Hover for the truth →" in muted with acid arrow, right-aligned */
}

/* Back side */
.flip-card-back {
  /* "THE TRUTH" label in acid */
  /* Response in Outfit 20px weight 600 */
  transform: rotateY(180deg);
}
```

### Pull Quote

```css
.pull-quote {
  font-family: 'DM Serif Display', Georgia, serif;
  font-size: clamp(28px, 3.5vw, 44px);
  font-style: italic;
  text-align: center;
  color: var(--color-text);
  line-height: 1.3;
}

.pull-quote .highlight {
  color: var(--color-acid);
}

.pull-quote-attribution {
  font-family: 'Space Mono', monospace;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--color-text-muted);
  margin-top: var(--space-md);
  text-align: center;
}
```

### Newsletter Signup

```css
.newsletter-input {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  padding: 14px 16px;
  font-family: 'Outfit', sans-serif;
  font-size: 14px;
  color: var(--color-text);
}

.newsletter-input:focus {
  border-color: var(--color-acid);
  outline: none;
}

.newsletter-button {
  /* Same as .btn-primary */
  background: var(--color-acid);
  color: #000;
  font-family: 'Space Mono', monospace;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  padding: 14px 32px;
  border: none;
  cursor: pointer;
}
```

---

## Color Pairing Rules

### On Near Black / Off Black Backgrounds (Default)

| Element | Color | Token |
|---|---|---|
| Headlines | White (#FAFAF5) | `color-text-bright` |
| Body text | Light Gray (#B0B0B0) | `color-text-secondary` |
| Labels/captions | Muted (#858585) | `color-text-muted` |
| Primary accent | Acid Green (#D4FF00) | `color-acid` |
| Negative/warning | Tomato Red (#FF3B30) | `color-red` |
| Borders | Mid Gray (#3A3A3A) | `color-border` |

### Special Rules

- The **serif accent word** in headlines always gets acid green color.
- **Strikethrough/falsification text** gets red or muted color.
- Section labels use acid green at **70% opacity** — not full brightness.

---

## The Logo

### Inline Wordmark (Primary Mark)

The Bratrax logo is a single-line inline wordmark: **"BRATRAX."** in Space Mono Bold, uppercase, with modified letterforms.

- **The T** is italicized (Space Mono Bold Italic) with its vertical stem extended diagonally, creating the defining brand element
- **The R** (second occurrence, in "RAX") is also italic (Bold Italic), echoing the T's slant angle
- **B, R, A** and **A, X** remain upright
- **The period "."** is a circle in acid green (#D4FF00)

> **Note:** An earlier stacked version (BRAT / RAX.) existed but has been retired in favor of the inline mark for simplicity and versatility.

### Logo Files

> **Naming convention:** "Light" and "Dark" refer to the **logo color**, not the background. Light logo = light-colored text = use on dark backgrounds. Dark logo = dark-colored text = use on light backgrounds.

| File | Logo color | Use on |
|---|---|---|
| `Bratrax Logo Light Inline.png` | Light text (#E8E4DC) | Dark backgrounds |
| `Bratrax Logo Light Inline.svg` | Light text (#E8E4DC) | Dark backgrounds (vector) |
| `Bratrax Logo Dark Inline.svg` | Dark text (#0A0A0A) | Light/white backgrounds |
| `Bratrax Logo Dark Inline.png` | Dark text (#0A0A0A) | Light/white backgrounds |

All files located at: `C:\Users\Yuliya\Jeeves\brands\bratrax\`

### Usage Rules

- **Minimum size:** 14px cap height.
- **Clear space:** At least 1× the cap height on all sides.
- **Never** set the logo in a different typeface.
- **Never** remove or recolor the acid green dot — it's always `#D4FF00`.
- **Never** straighten the T or R italic — the diagonal is the brand mark.
- The dot stays `#D4FF00` on both light and dark versions.

### Figma Source

Logo vectors and exploration file: [Bratrax — Logo Exploration](https://www.figma.com/design/DcDsW3u51vHZFQ4C7AM7lM)

---

## Brand Personality

- Honest. Experienced. Unimpressed (by the industry).
- The brand voice is Brat Vukovich's — blunt, story-driven, unafraid to name what others won't.
- Anti-dashboard-porn. Anti-attribution-theater. Pro-shared-meaning.
- Visual identity draws from halftone print, graph paper, and screen-print energy.
- Dark and technical with strategic pops of acid green for emphasis and red for falsification/tension.

---

## Changelog

### v1.2 — 2026-04-29 — Letter-spacing rule formalized; H4 tracking opened

Built directly on top of the v1.1 typography refinement (same day) after testing the new tokens against real comparison-page content.

**Approach: per-token defaults with a global envelope.** Each heading level now has a single fixed letter-spacing value baked into its token — that's the canonical setting. The system also defines a global envelope (`-0.5px` to `+0.5px`) for headlines, but deviation from token defaults requires explicit reason. This gives both predictability (every H4 across the system tracks the same) and flexibility (the envelope handles edge cases) without leaving the call to designer judgment.

**Changes:**

- `type-h4` letter-spacing updated: `0` → `+0.3px`. At 22px, weight-900 Outfit reads slightly compressed even at neutral tracking; positive territory opens the FAQ-question / card-title surface so it breathes properly without feeling like a label.
- Letter-spacing rule reformulated as **per-token defaults + global envelope** rather than per-surface ranges. Token defaults: H1 `-0.5px` · H2 `-0.1px` · H3 `0` · H4 `+0.3px`. Envelope: `-0.5px` to `+0.5px`.
- Rule explicitly allows positive letter-spacing on headlines (previously v1.1's wording defaulted to negative-only, which was a holdover assumption).

**No breaking changes** from v1.1 → v1.2. H1, H2, H3 token values are unchanged. Only H4 gained `+0.3px`.

### v1.1 — 2026-04-29 — Typography refinement

Triggered by readability issues at H2–H3 sizes on the comparison pages (Outfit 900 + tight tracking causing visible smush at non-hero sizes).

**Approach: looser spacing, keep weight 900.** Headline weight stays at Outfit 900 across all levels — that's the brand's signature. Solve the smoosh by relaxing letter-spacing toward 0 and giving headlines more line-height breathing room as size descends.

**Changes:**

- `type-h2` updated: line-height `1.1 → 1.15`, letter-spacing `-0.3px → -0.1px`. Weight stays 900.
- `type-h3` added (NEW token): `clamp(24px, 2.6vw, 34px)` · weight 900 · line-height 1.2 · letter-spacing 0. The system previously had no explicit H3 token; pages were extending the H2 spec down by default.
- `type-h4` added (NEW token): 22px · weight 900 · line-height 1.3 · letter-spacing 0.
- Letter-spacing rule expanded into per-surface limits: headlines `0` to `-0.5px` max, body always `0`, Space Mono labels positive-only (`0` to `+2px`), DM Serif italics `0` to `-0.5px` max.
- New design principle codified: *"If a headline looks loose at these limits, reduce font size before tightening spacing."*

**Surface principle deferred.** A formal "no graph paper texture on elevated elements" rule was considered but deferred to keep card and surface specs flexible. Existing cards default to solid `#141414` fills; that pattern stays as-is.

**No breaking changes.** Existing pages on v1.0 typography still render correctly; the new tokens only refine what was already implicit.

### v1.0 — 2026-03-24 — Initial system

Color, typography, spacing, texture, components, logo, and brand personality.
