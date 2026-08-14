# Slack Marketplace submission — outstanding items

**Status:** Not submitted. Listing filled in; nine items open.
**Last checked:** 2026-08-14 against `VidTao/bratrax` `main` @ `0962068d2`, and against Slack's published Marketplace guidelines.

Working reference for the fields themselves: [`slack-submission-form.md`](slack-submission-form.md).

---

## Done

- **The app works and is live to customers.** Settings → Slack connects a workspace; no Marketplace dependency.
- **Listing form filled and verified** field-by-field against the sheet — name, both descriptions, icon, background colour (`#0a0a0a`), categories, all three URLs, language, pricing, and *Install from your landing page* with Direct install correctly empty.
- **All three URLs live** (PR #63, merged): `/slack` exists, the privacy policy discloses Slack and Anthropic and no longer claims data never reaches an LLM, and the FAQ has a Slack section with its AI section corrected.

---

## Open — nine items

### 1. Agents migration ⚠️ do first — dev handover written: [slack-dev-handover.md](slack-dev-handover.md)
Slack is deprecating the `assistant_view` experience Bratrax is built on. **Update Now is one-way and permanent per app**, and it changes the events the bot runs on — `assistant_thread_started`, which drives our suggested prompts, goes away. Needs a developer, not a click. Full brief with file-and-line touchpoints, ordering, and a test plan: **[slack-dev-handover.md](slack-dev-handover.md)**.

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

### 6. Install count — threshold now confirmed
The guidelines list as unsuitable any app *"installed on less than 5 active workspaces and have less than 10 weekly active users."* Active workspaces are ones used in the past 28 days, sandboxes excluded. So the bar is **5 active workspaces and 10 weekly active users** — not the "roughly 10 installs" recorded earlier. Now that customers can self-connect this should climb on its own; check the real number before submitting.

### 7. Two disclaimers required — not yet written
The AI guidelines require both on the **landing page and in the long description**: that the app uses an LLM and can generate inaccurate output, and that a **paid Slack plan** is needed for the AI agent container (with a note that other features still work on free plans). Neither exists today.

### 8. Enhanced review is guaranteed — prepare for it
Requesting `*:history` and `files:read` automatically triggers Slack's enhanced review. We already meet the standard it tests against — their rule is *"DON'T store any Slack data you obtain. Store metadata instead and pull in data in real time, i.e. zero-copy"* — which is exactly the architecture. Four AI disclosures are also required in Security & Compliance: model used, retention and how the LLM uses the data, LLM data tenancy, LLM data residency.

### 9. Smaller listing fixes
- **Short description** should be 10 words or fewer; the current one is about 14.
- **Long description** should use Slack message formatting — bold headings rather than the CAPS currently in place.
- **Add a collaborator** to the app; required before approval.
- **Respond to `help`** in the agent container — a guideline requirement and a code gap. Covered in the dev handover.

---

## Verified against current code (2026-08-11)

Re-checked after the product repo moved 74 commits. Nothing changed that affects any published claim:

- **18 bot scopes** — same set as the manifest.
- **7-tool read-only MCP allowlist** — `query_sql` and `workshop_write_knowledge` still excluded.
- **Four Slack tables** — `slack_installations`, `slack_oauth_states`, `slack_channel_links`, `slack_link_codes`. No message-content column; the only writes are installations and channel links.
- **No scheduler** — the assistant is still strictly reactive. No alerts, no digests.

Re-run these checks before submitting if the repo moves again; the privacy policy and FAQ both depend on them.
