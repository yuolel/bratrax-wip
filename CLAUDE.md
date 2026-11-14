# bratrax.com marketing site

Static pages for bratrax.com (home, pricing, FAQ, comparisons, legal). The `/stores/` directory is served separately; its redesign spec lives in `VidTao/bratrax` under `docs/seo/stores-redesign/`.

## Line breaks and labels on web pages

Yuliya has had to correct these repeatedly. Treat them as hard rules for every page, mockup and email in this project.

**Line breaks**
1. Never cap a heading or a section intro narrower than its column. No `max-width` in `ch` or px on `h1`/`h2`/intro paragraphs inside a section header: let them run the full width so they stay on one line wherever they fit.
2. Write a section intro as one short sentence that fits on one line at desktop (about 100 characters at most). If it needs two lines, it is too long: cut words, don't narrow the box.
3. `text-wrap: balance` only on `h1` and `h2` (it only acts when a heading has to wrap). Use `text-wrap: pretty` on everything else: card titles, paragraphs, list items. `pretty` stops a single word sitting alone on the last line without splitting the text into two half-empty lines.
4. No manual `<br>`. A `&nbsp;` between the last two words of a headline is the only allowed fix, and only if `balance` still leaves one word alone.
5. Before showing any page, look at it at 1440px and 390px and check every heading and intro for: a single word alone on the last line; a second line much shorter than the first because the box was narrowed; a break that splits a phrase that belongs together. Fix by rewriting or widening, never by narrowing.

**Labels**
6. No small uppercase "eyebrow" label above a heading unless it tells the reader something the heading doesn't (a date, a price, who it's from). "Use cases" above "What people use it for" adds nothing; drop it.

**Copy**
7. Lead every section with the benefit to the visitor, in their words. Explain how the data is collected only where someone asks (an FAQ or the methodology page), not in section intros.
8. The serif accent word in a headline goes on a word that carries the point, never the first word.
