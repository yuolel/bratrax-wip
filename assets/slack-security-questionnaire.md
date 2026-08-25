# Slack Marketplace — Security & Compliance questionnaire

Submission step 3. Draft answers, grounded in code and in the two pages that
already carry legal weight:

- [`/security`](https://bratrax.com/security) — Annex II of the DPA, published 19 Aug 2026
- [`/subprocessors`](https://bratrax.com/subprocessors) — Annex III, same date

Where those pages already answer a question, **quote them rather than writing
something new**. They are contractual; a questionnaire answer that says something
different is a discrepancy a reviewer can find in one click.

Five things need confirming before this goes in. They are collected at the end.

---

## The four AI disclosures

Requesting `*:history` and `files:read` triggers Slack's enhanced review, which
requires these four specifically.

### 1. Which model is used

> The assistant is powered by Anthropic's Claude, called through Anthropic's
> commercial API. Anthropic PBC is a named subprocessor. No other LLM provider is
> involved. Customers who connect their own AI provider through MCP do so under
> their own contract with that provider; that traffic does not pass through
> Anthropic or through Bratrax's AI features.

Model id lives in `BRATRAX_SLACK_MODEL` (`slack/config.py:41`).

### 2. Retention, and how the LLM uses the data

> Bratrax stores no Slack message content. The Slack integration writes to four
> tables — workspace installations, single-use OAuth states, channel-to-account
> links, and single-use link codes. None has a column for message content.
> Conversation context is rebuilt from Slack's own history API on each question
> and discarded once the answer is sent; the service is stateless between
> questions.
>
> Data sent to Anthropic is transmitted to generate a response only and is not
> used to train models.

The "not used to train" wording is Annex III's, verbatim. The four-table claim is
verifiable in `server/migrations.py` (`create_slack_installations`,
`create_slack_oauth_states`, `create_slack_channel_links`,
`create_slack_link_codes`).

⚠️ **Incomplete** — Anthropic's own API-side retention still needs stating. See
confirmation item 1.

### 3. LLM data tenancy

> Anthropic's multi-tenant commercial API. Bratrax does not operate a dedicated
> or self-hosted model instance, does not fine-tune a model on customer data, and
> does not write customer data into any shared model, index, or vector store.
> Each request is independent.

### 4. LLM data residency

> Customer Personal Data is hosted on servers in the European Union (Finland).
> Encrypted backups are held in cloud storage in the United States. Anthropic PBC
> processes in the United States, so a question and the data needed to answer it
> are transferred to the US at the point the answer is generated. That transfer
> is covered by the European Commission's Standard Contractual Clauses, as
> incorporated into the Bratrax Data Processing Agreement.

---

## The zero-copy question

Slack's enhanced review tests one rule above all others: *"DON'T store any Slack
data you obtain. Store metadata instead and pull in data in real time, i.e.
zero-copy."*

This is exactly the architecture, and it is the strongest answer in the whole
questionnaire — lead with it.

> Bratrax stores Slack metadata only: the workspace and channel identifiers
> needed to route an answer to the right account, and the bot token needed to
> reply. Message content, thread history, files, and user profiles are read from
> Slack's API at the moment a question is asked and are not persisted. There is
> no message store, no conversation log, and no scheduled job — the assistant
> speaks only when mentioned or messaged directly.

Supporting facts, all verifiable:

| Claim | Where |
|---|---|
| Four tables, none holding message content | `server/migrations.py` |
| 7-tool read-only MCP allowlist; `query_sql` excluded | `docs/SLACK_ASSISTANT.md` |
| No scheduler — strictly reactive | no cron/APScheduler in `slack/` |
| Uninstall soft-deletes via `revoked_at` | `slack_installations` |

---

## Standard sections — already answered publicly

Point Slack at `/security`. Every row below is already committed there.

| Their question | Annex II says |
|---|---|
| Encryption in transit | TLS to the Service; internal traffic over an encrypted private network; encrypted DB connections |
| Encryption of backups | All backup copies encrypted |
| Password handling | Salted, one-way hashed, never stored or transmitted in plaintext |
| OAuth / platform credentials | Used only to retrieve authorized data, access restricted to systems that need it, never written to application logs |
| Tenant isolation | Dedicated logical data store per customer; application-level access controls scope every query |
| Access control | Admin / read-only viewer roles; least-privilege for personnel; access revoked on departure |
| Privileged access logging | Internal support role logs person, account, and time |
| Incident response | Investigated, documented, remediated; customers notified per DPA §7 |
| Change management | Version-controlled code review, second engineer before merge |
| Subprocessors | Listed at `/subprocessors`, notified per DPA §5.3, objectable under §5.4 |
| GDPR transfers | SCCs incorporated into the DPA |
| Deletion on termination | 30-day export window, 150 days cold retention, permanent deletion at 180 days |

---

## Confirm before submitting

Five gaps. Three are quick answers; two may need a decision.

### 1. Anthropic's API-side retention — *needs an answer*

Anthropic's standard commercial terms retain API inputs and outputs for a period
for abuse monitoring unless a zero-retention arrangement is in place. Slack asks
this directly and "not used for training" does not answer it — training and
retention are different questions.

Check which applies to the Bratrax account, then state the actual number. If it
is the standard retention, say so plainly; it is a normal answer and reviewers
see it constantly. Guessing here is the single riskiest thing in this document.

### 2. Encryption at rest on the live database — *needs verifying*

Annex II commits to encrypted **backups** and encrypted **connections**. It does
not state that the primary database is encrypted at rest, and Slack's
questionnaire asks about at-rest encryption directly.

If the volumes are encrypted, the answer is easy and Annex II is worth updating
to say so. If they are not, answer honestly — it is not disqualifying on its own.

### 3. The Slack bot token is stored unencrypted at application level

`bot_token TEXT NOT NULL` in `slack_installations`, written as received
(`slack/stores.py:92`). No application-level encryption.

Annex II's existing claims still hold — access is restricted and the token is
never logged — and at-rest protection then depends entirely on item 2. Worth
knowing before answering a question about credential storage.

### 4. SOC 2 — *answer "no"*

Nothing on the site claims a SOC 2 report and there is no evidence of one. Slack
asks; answer no rather than leaving it blank. It is not required for approval,
and a blank field invites a follow-up where a "no" does not.

### 5. Ignore `CLAUDE.md` on hosting

It says PostgreSQL runs on Cloud SQL. Annex II, published four days ago, says
customer data is hosted in the EU (Finland) with encrypted backups in US cloud
storage — and Annex III lists Hetzner (Finland) as primary hosting with Google
Cloud for backups only.

**Annex II and III are the answer.** They are contractual and current;
`CLAUDE.md` is stale on this point and should be corrected separately.
