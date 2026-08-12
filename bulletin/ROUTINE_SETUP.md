# Bratrax Bulletin routine — setup

The **Bratrax Bulletin** is a marketing-forward email digest of what shipped,
drafted monthly into the beehiiv publication "The Dashboard" and sent to the
whole newsletter list — including prospects who have never used the product.

Claude's instructions live in [`PROMPT.md`](./PROMPT.md); coverage state lives in
[`LEDGER.md`](./LEDGER.md). This file covers the one-time routine setup.

> **It is never auto-sent.** Two independent reasons: `PROMPT.md` forbids it, and
> the beehiiv tool the routine uses (`save_post`) can only create a draft —
> publishing and scheduling are human actions in the beehiiv UI. There is no code
> path from this routine to a subscriber's inbox.

## How the two routines divide the work

| | Weekly release-comms | Monthly Bulletin |
|---|---|---|
| Prompt | `scripts/release_comms/PROMPT.md` in `vidtao/bratrax` | `bulletin/PROMPT.md` here |
| Cadence | Weekly, Monday | Monthly |
| Reads | Commits on `vidtao/bratrax` + `vidtao/rill` | `bulletin/LEDGER.md` |
| Writes | `changelog/index.html` **+ new ledger rows**, in one PR | beehiiv draft, then ledger statuses (direct push) |
| Audience | Internal Slack, then customers via the changelog | Whole newsletter list, incl. prospects |

The weekly routine owns "what shipped and is it live". Every changelog entry it
publishes also gets a `pending` ledger row in the same pull request. The Bulletin
consumes those rows a month later.

**Why they stay separate.** A and B were combined because they share one commit
scan and one live-vs-in-progress classification, so they can never disagree. The
Bulletin shares neither — it reads human-merged state. Folding it in would also
mean it read the changelog *before* that week's PR was merged, so it would never
see the entries the digest had just found. Keeping them apart also keeps the
digest the team relies on out of the blast radius of a longer, more failure-prone
job that writes to beehiiv.

**Net PR count: one per week.** The Bulletin opens none — it pushes the ledger
directly, scoped to that one file, because nothing fetches it. Everything the
site actually serves still goes through review.

## One-time setup

**This has to be done in the web UI, not from a session.** Creating the routine
with the `create_trigger` MCP tool was tried on 2026-08-11 and does not work
here: the `connectors` parameter is rejected for this organization, and a routine
created without it fires sessions carrying **no** connector (`mcp__*`) tools at
all. That routine would reach neither beehiiv nor Slack, and could not even
report the failure — a silent miss every month. The trigger created during that
attempt was deleted for exactly that reason.

Open <https://claude.ai/code/routines> and click **New routine**.

### Routine — Bratrax Bulletin

| Field | Value |
| --- | --- |
| Name | `Bratrax Bulletin` |
| Sources | **Two:** `yuolel/bratrax-wip` AND `vidtao/rill` |
| Branch | `bratrax-com-static` on `yuolel/bratrax-wip` (where `PROMPT.md` lives) |
| Schedule | Monthly. `0 9 1 * *` is the 1st at 09:00; pick a weekday-ish slot that is **not Monday**, so it never races the weekly changelog PR before anyone has merged it |
| Connectors | **Slack** and **beehiiv** — both required, and the reason this must be created in the UI |

Prompt body (paste exactly):

```
Read bulletin/PROMPT.md and execute it.

Never send, schedule, or publish the post — you create a draft only; a human
sends it in beehiiv. If the previous issue is still an unsent draft, or there
is not enough new material, skip cleanly and say so in #ext-bratrax. If you
cannot find bulletin/PROMPT.md, stop and report it there rather than
improvising an issue.
```

The extra paragraph is belt-and-braces: each firing starts a fresh session with
no memory, so the three constraints that must survive a confused run are stated
in the trigger itself rather than left solely to a file it might fail to read.

### Why each source is attached

- **`yuolel/bratrax-wip`** — the prompt, the ledger, and the changelog. The
  routine writes exactly one file here.
- **`vidtao/rill`** — the frontend fork. Needed to verify UI labels against the
  Svelte that renders them, to confirm a help article exists before linking it,
  and to check platform lists and counts against the code.

**`vidtao/bratrax` is not attached.** The Bulletin never reads or writes the app
repo. The weekly routine still needs it, since its own prompt lives there.

**There is no "GitHub connector"** — GitHub is not in the connector list (that
list is third-party integrations: Slack, beehiiv, Canva, Figma, …). Repository
access comes from the **Sources** field. **beehiiv *is* a connector** and must be
attached; without it the routine can read the ledger and then do nothing.

## Running it

Set the monthly schedule even if you plan to trigger it by hand — "manual"
reliably becomes "forgotten" a few months in, and a scheduled fire with nothing
new just posts *"nothing substantial enough to send this cycle"* and stops, which
costs nothing. Use **Run now** whenever you want an issue early.

**The routine has never run end to end.** Issue #1 was drafted collaboratively in
a session, not by it. Its first pass is the first real test — watch the session
log. Expect a **skip** on that first run for two reasons: issue #1 is still an
unsent draft (Step 1 stops there), and only one entry is currently `pending`.

## How coverage is tracked

[`LEDGER.md`](./LEDGER.md) is the record; read its header for the state model. In
short: `pending` rows are candidates, everything else is closed, and an entry cut
from an issue does not come back around.

Three things worth knowing:

- **The routine writes the ledger at draft time**, so `sent` means "went into
  issue #N", not "confirmed in an inbox". Step 1's beehiiv check is what stops
  that becoming a lie: if the previous issue never went out, nothing new is
  drafted and nothing new is marked.
- **Nobody is expected to review the ledger diff.** That is deliberate, and it is
  why the beehiiv check exists rather than relying on a human noticing.
- **To resurface an entry**, set its row back to `pending`. Hand-editing is the
  intended override.

## Known gaps, deliberately

- **No images.** The routine cannot screenshot the app and must never generate a
  product image, so drafts ship text-only. It says in Slack which entries would
  benefit; a human adds them in the beehiiv editor before sending.
- **The Bulletin cannot report anything the changelog missed.** By design. If it
  spots a gap it flags it in Slack, and the fix is to get the entry onto the
  changelog via the weekly routine, which also creates its ledger row.
- **`/help` is behind login**, so every help link bounces a prospect to sign-in.
  Putting `/help` on the frontend public-route allowlist would fix that and has
  marketing value well beyond this email, but it is an app change.
