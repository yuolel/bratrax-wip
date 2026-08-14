# Slack Marketplace submission — outstanding items

**Status:** Not submitted. Listing filled in; six items open.
**Last checked:** 2026-08-11 against `VidTao/bratrax` `main` @ `0962068d2`.

Working reference for the fields themselves: [`slack-submission-form.md`](slack-submission-form.md).

---

## Done

- **The app works and is live to customers.** Settings → Slack connects a workspace; no Marketplace dependency.
- **Listing form filled and verified** field-by-field against the sheet — name, both descriptions, icon, background colour (`#0a0a0a`), categories, all three URLs, language, pricing, and *Install from your landing page* with Direct install correctly empty.
- **All three URLs live** (PR #63, merged): `/slack` exists, the privacy policy discloses Slack and Anthropic and no longer claims data never reaches an LLM, and the FAQ has a Slack section with its AI section corrected.

---

## Open — six items

### 1. Agents migration ⚠️ do first
Slack shows a banner: *"The agentic app experience is changing. You'll need to update your app to the new experience."* Bratrax uses `assistant:write` and the assistant-thread events, so this is aimed at us. **First because a required migration would change the app config and manifest, and the other five are downstream.** Status: unread — click through to Agents and see what it asks.

### 2. Scope reasons — 18 required, 0 written
Submission step 2 shows *"Please add reasons for your app to request this scope"* against every scope. All 18 need a written justification via **Manage Reasons**. Not optional; Slack reviews the reasons as well as the scopes.

Can be drafted from the code — the three that usually draw questions are already answered in `slack-submission-form.md`:

| Scope | Reason |
|---|---|
| `channels:history`, `groups:history` | Thread context is rebuilt from Slack history per question; the service is stateless and stores no conversation |
| `groups:write` | Creates the private `#ext-<slug>` channel in the shared Bratrax community workspace |
| `users:read.email` | Matches a Slack user to their Bratrax account so a DM resolves to the right store |

### 3. Security and compliance questionnaire
Submission step 3. Expect encryption in transit and at rest, retention and deletion, internal access controls, incident response, subprocessors, GDPR posture, and possibly SOC 2. The updated privacy policy already answers several. Likely the largest single item.

### 4. App images
Three, 1600×1000, PNG or JPG. The only empty field on the listing form. Shot 1 should be a **real screenshot** of the bot answering in a channel — it's the image reviewers study hardest and it doubles as evidence the app works. Icon is done.

### 5. Reviewer test credentials
Submission step 4 (locked until 2 and 3 are done). Needs an **admin**-role account on the demo client — `/try-demo` issues `viewer`, and every Slack settings route is gated by `_require_admin_or_super`, so a viewer cannot connect a workspace. Paste-ready instructions in `slack-submission-form.md` §3. Yuliya can obtain.

### 6. Install count
Slack's guidance mentions roughly 10 installations on workspaces other than our own. Now that customers can self-connect this should climb on its own. **Unverified** — the exact threshold and any exceptions could not be confirmed; Slack's docs block automated access. Check the real number before submitting.

---

## Verified against current code (2026-08-11)

Re-checked after the product repo moved 74 commits. Nothing changed that affects any published claim:

- **18 bot scopes** — same set as the manifest.
- **7-tool read-only MCP allowlist** — `query_sql` and `workshop_write_knowledge` still excluded.
- **Four Slack tables** — `slack_installations`, `slack_oauth_states`, `slack_channel_links`, `slack_link_codes`. No message-content column; the only writes are installations and channel links.
- **No scheduler** — the assistant is still strictly reactive. No alerts, no digests.

Re-run these checks before submitting if the repo moves again; the privacy policy and FAQ both depend on them.
