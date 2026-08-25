# Slack app — developer handover

**For:** whoever makes the Slack code changes
**Owner:** Yuliya
**Repo:** `VidTao/bratrax` (service lives in `slack/`, plus one file under `server/routes/`)
**Blocking:** the Slack Marketplace submission. Both tasks below must land before submitting.
**Written:** 2026-08-14, against `main` @ `0962068d2`

Two independent pieces of work:

1. **Migrate to the new Agent messaging experience** — Slack is deprecating the one we're on. Permanent, one-way, and it changes which events the bot receives.
2. **Remove two unused OAuth scopes** — small, but a guaranteed rejection if left.

Task 2 is safe and quick. Task 1 needs care. They can ship separately.

---

# Task 1 — Agent messaging experience migration

## Why

The Slack app config shows a banner: *"The agentic app experience is changing. You'll need to update your app to the new experience."* Clicking **Update Now** on **Features → Agents** shows this confirmation:

> Your app will have a Messages tab instead of Chat and History tabs. This update will also affect your app manifest, the events your app receives, and the types of messages in the DM channel. **This change is permanent.**

Slack's position: new apps can only use the Agent experience, `assistant_view` will eventually be deprecated, and existing apps are being asked to migrate. So this is happening regardless; the only choice is when.

**Do not click Update Now until the code is ready.** It is one-way, and the events it changes are the ones the bot runs on. Clicking it first means the assistant breaks in production for however long the fix takes.

## What changes

| Old (`assistant_view`) | New (`agent_view`) |
|---|---|
| Separate Chat and History tabs | One Messages tab; agents reply in-thread |
| `assistant_thread_started` event | Use `app_home_opened` to detect a user opening the DM |
| `assistant_thread_context_changed` event | `app_context_changed` |
| Suggested prompts live inside a thread | Suggested prompts sit at the top of the Messages tab |
| `thread_ts` required on assistant calls | `thread_ts` no longer required |

The regenerated Agent manifest subscribes to `message.im`, `app_home_opened` and `app_context_changed`.

⚠️ **The table above is assembled from Slack's changelog and public docs, not from a migration guide we were able to read directly** — Slack's docs block automated access. Treat it as a starting map, and confirm each row against **Learn more about these changes** in that modal before writing code.

## Every place our code touches this

All in `slack/listeners.py` unless noted.

| Location | What it does now | Migration impact |
|---|---|---|
| `manifest.yaml:17` `assistant_view:` block | Declares `assistant_description` + 3 `suggested_prompts` | Becomes the agent equivalent. Let Slack regenerate the manifest on update, then diff it against ours and reconcile — don't hand-write it |
| `listeners.py:463` `@app.event("assistant_thread_started")` | Calls `assistant_threads_setSuggestedPrompts` with the 3 prompts | **Highest risk.** This event goes away. Move the logic to `app_home_opened` |
| `listeners.py:480` `@app.event("assistant_thread_context_changed")` | `pass` — no-op | Rename to `app_context_changed`, or delete. It does nothing today |
| `listeners.py:216` and `:233` `assistant_threads_setStatus` | Sets and clears the "is thinking…" indicator | Verify it still works when `thread_ts` is optional. Note the fallback at `:223` — if this call fails the app adds an 👀 reaction instead, so a silent break here degrades rather than errors, which makes it easy to miss |
| `listeners.py:424` `@app.event("message")` | Handles `message.im` DMs | Should be unaffected — `message.im` survives. Confirm the payload shape hasn't changed |
| `listeners.py:389` `@app.event("app_mention")` | Channel mentions | Unaffected. Channels aren't part of this |

## Suggested approach

1. Read **Learn more about these changes** and correct the table above where it's wrong.
2. Create a **separate dev Slack app** from the current manifest and click Update Now on *that* one. There's a dev-app workflow already documented in `docs/SLACK_ASSISTANT.md` → Dev loop (cloudflared tunnel + separate app). This is what it's for — the change is permanent per app, so you get exactly one shot on production.
3. Diff Slack's regenerated manifest against `slack/manifest.yaml` and reconcile.
4. Port the event handlers.
5. Test against the dev app (checklist below).
6. Only then click Update Now on the production app and deploy in the same window.

## Test before and after

`docs/SLACK_ASSISTANT.md` has a 10-step E2E script. The steps that specifically exercise what's changing:

- Open a DM with the app → the three suggested prompts appear ("Today's spend", "Top campaigns", "Revenue chart")
- Ask a question in the DM → the "is thinking…" status appears, then clears when the answer posts
- Ask a follow-up in the same thread ("and just for Facebook?") → context carries
- Ask in a channel via `@bratrax` → 👀 reaction appears and is removed; the reaction path is the channel fallback and must still work
- Chart request over 20 data points → PNG uploads correctly
- Click a 7d/30d/90d re-run button → still acks within 3s

---

# Task 2 — Remove `links:read` and `links:write`

## Why

Neither is used. `@app.event("link_shared")` at `listeners.py:497` is a stub — `pass`, with a comment saying rich unfurls are future polish — and nothing calls `chat.unfurl`.

Slack's Marketplace guidelines are explicit:

> **DON'T** include scopes in your submitted app intended for future functionality. We will only approve scopes related to functionality we can test.

Leaving them in is a guaranteed review comment.

## Three files

**1. `slack/manifest.yaml`** — remove from `oauth_config.scopes.bot`:
```yaml
      - links:read
      - links:write
```
and from `settings.event_subscriptions.bot_events`:
```yaml
      - link_shared
```

**2. `server/routes/slack_settings.py`** — remove `"links:read"` and `"links:write"` from `SLACK_BOT_SCOPES`. That list carries a comment saying it must stay in sync with the manifest; this is why.

**3. `slack/listeners.py:497`** — delete the `link_shared` handler. Optional (it's a no-op), but leaving a handler for an unsubscribed event is confusing.

While you're in there: `assistant_thread_context_changed` at `:480` is the same shape — a `pass` handler. It doesn't cost a scope, so it isn't a review risk, but it can go in the same pass (see Task 1).

## Order matters

**Deploy the code first, then update the Slack app config.**

`SLACK_BOT_SCOPES` builds the `scope=` parameter on the install URL. If the scopes come out of the Slack config while the deployed code still requests them, Slack rejects the authorization as an invalid scope and **new installs break** until the deploy lands.

Existing installs are unaffected either way — they keep the token they were already granted. Nobody needs to reconnect.

---

# Task 3 (small) — respond to `help`

Slack's guidelines for agent/assistant apps:

> **DO** respond with usage instructions when someone sends `help` in the "Chat" tab or in the AI agent container view.

The app currently has no `help` branch; "help" would go to the LLM like any other question. Low effort, and reviewers do test it. A short static reply listing what it can answer, how to mention it in a channel, and a link to `https://bratrax.com/faq#slack` is enough.

---

# What NOT to do

- **Don't click Update Now on the production app before the code is ready.** One-way.
- **Don't hand-write the new manifest.** Let Slack regenerate it and reconcile.
- **Don't remove scopes from the Slack config before deploying the code.** Breaks new installs.
- **Don't turn on Socket Mode.** It's correctly off and Marketplace apps need Request URLs.
- **Don't enable the Slack MCP Server toggle** on the Agents page. Unrelated to us — our MCP endpoint is our own, not Slack's.

---

# Reference

- `docs/SLACK_ASSISTANT.md` — architecture, dev loop, E2E script, known limitations
- `slack/manifest.yaml` — source of truth for app config
- `assets/slack-submission-status.md` (in `yuolel/bratrax-wip`) — the full outstanding-items list for the submission
- Slack Marketplace guidelines: <https://docs.slack.dev/slack-marketplace/slack-marketplace-app-guidelines-and-requirements>

## Verified against the code on 2026-08-14

Re-checked after the repo moved 74 commits, so the handover reflects current `main`:

- 18 bot scopes in the manifest, matching `SLACK_BOT_SCOPES`
- 7-tool read-only MCP allowlist; `query_sql` and `workshop_write_knowledge` excluded
- Four Slack tables, none with a message-content column; the only writes are installations and channel links
- No scheduler — the assistant is strictly reactive

Worth re-running these if the repo moves again: the privacy policy and the published FAQ both depend on them.
