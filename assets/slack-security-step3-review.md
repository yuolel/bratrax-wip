# Slack submission step 3 — Privacy & data governance

Review of the section as filled in on 2026-08-25, with paste-ready replacements.

The form opens with *"By submitting this information, you confirm that it is
accurate and truthful."* One field currently is not.

---

## 1. The tenancy answer contains a claim the code contradicts

**Currently says:** *"By default each customer's queries run on Bratrax's own
Anthropic account; customers who supply their own Anthropic API key run…"*

That was true until 2026-08-21. It is not true now.

`resolve_api_key` in [`slack/brain/loop.py`](../../bratrax/slack/brain/loop.py)
resolves in this order:

1. `SLACK_ANTHROPIC_API_KEY`
2. the client's stored BYOK key
3. `ANTHROPIC_API_KEY`

BYOK is **second**. Its own docstring says so explicitly — *"SLACK_ANTHROPIC_API_KEY
comes FIRST, ahead of the client's own BYOK key. That ordering is deliberate and
is specific to this service."* It was changed after a client's BYOK ran dry and
broke the assistant for whoever resolved to that client, and the platform key
sitting behind it was never reached.

So whenever the Slack key is set — which it is in production — **every Slack
question runs on Bratrax's account regardless of whether the customer has
supplied a key.** BYOK only decides the path in a deployment that sets no Slack
key at all.

Note `slack/config.py:32` still carries the old order in a comment. The comment
is stale; the code is authoritative.

The in-app AI sidebar *does* still prefer BYOK. That distinction is what makes
the current wording sound plausible, and it is why this is worth stating
carefully rather than trimming to a half-truth.

**Replace with:**

> Bratrax uses Anthropic's commercial API under its standard commercial terms.
> Inputs and outputs are not used to train models. Bratrax does not operate a
> dedicated or self-hosted model instance, does not fine-tune any model on
> customer data, and does not write customer data into any shared model, index,
> or vector store. Every request is independent: no customer's data is used to
> answer another customer's question. Slack assistant queries run on an Anthropic
> account operated by Bratrax.

---

## 2. Two required LLM fields are empty

### LLM data residency policy

> Customer Data is hosted on servers in the European Union (Finland), with
> encrypted backups in cloud storage in the United States. Anthropic PBC
> processes in the United States, so a question and the data needed to answer it
> are transferred to the US at the point the answer is generated. That transfer
> is covered by the European Commission's Standard Contractual Clauses, as
> incorporated into the Bratrax Data Processing Agreement at
> https://bratrax.com/data-processing-agreement.

### LLM retention settings — needs one fact first

The Bratrax half is verifiable and can be written now. The Anthropic half cannot
be answered from the repository.

> Bratrax retains no Slack message content. The Slack integration stores
> workspace and channel identifiers and the bot token, and nothing else;
> conversation context is rebuilt from Slack's API on each question and is
> discarded once the answer is sent. Question and answer text is not written to
> Bratrax's database.
>
> On the Anthropic side, inputs and outputs are handled under Anthropic's
> standard commercial API terms and are not used for model training.
> **[CONFIRM: whether the Bratrax account runs under Anthropic's standard
> retention window or a zero-retention arrangement, and state which.]**

Do not skip the bracket. "Not used for training" is a different question from
"how long is it kept", Slack asks both, and this field is the one that asks the
second.

---

## 3. Data center location omits the United States

The field lists Finland. Annex II says encrypted backups are held in cloud
storage in the United States, and Annex III lists Google Cloud (US) for exactly
that.

Add **United States**. Leaving it off makes the form narrower than the
publication it will be checked against, and backups are the first thing a
security reviewer asks about.

---

## 4. The three policy fields are bare URLs

They are textareas, not URL fields, and the LLM fields beside them carry prose
examples — the form expects an answer, with the link as the citation. A reviewer
should not have to leave the form to learn whether you have a retention policy.

All three currently point at the DPA. Two of them should point somewhere else:
storage is answered by Annex II at `/security`, and retention periods live in the
privacy policy as well as DPA §12.

### Data retention policy

> Customer Data is retained while the subscription is active. After cancellation
> or termination: a 30-day self-serve export window during which dashboards and
> queryable access remain available, then up to 150 days of cold retention during
> which data is not accessible but can be restored on written request, then
> permanent deletion at 180 days. Billing records are retained as required by tax
> and accounting law. For the Slack app specifically, no message content is
> retained at any point. Full terms:
> https://bratrax.com/data-processing-agreement (§12) and
> https://bratrax.com/privacy-policy.

### Data archival/removal policy

> On termination or expiry, Customer may direct Bratrax to return or delete
> Customer Personal Data, at any time and by written notice to
> legal@bratrax.com. Data is exportable in a structured, commonly used,
> machine-readable format throughout the Agreement. Backup copies are not deleted
> individually; they are removed as the backup set containing them ages out.
> Uninstalling the Slack app revokes the stored bot token immediately. Full
> terms: https://bratrax.com/data-processing-agreement (§12).

### Data storage policy

> Each customer's data is held in a dedicated logical data store, hosted on
> servers in the European Union (Finland), with encrypted backups in cloud
> storage in the United States. Data is encrypted in transit with TLS, and
> traffic between Bratrax systems runs over an encrypted private network not
> exposed to the public internet. For the Slack app, Bratrax stores metadata only
> — workspace and channel identifiers and the bot token — and no message content,
> thread history, or files. Technical and organizational measures in full:
> https://bratrax.com/security.

---

## 5. Two optional fields worth filling

Both are free marks. An empty optional field on a security form invites the
follow-up question that a filled one closes.

### How do you host your data?

> Cloud hosted. Primary infrastructure is operated by Hetzner Online GmbH in
> Finland (EU); encrypted backups are held in cloud storage in the United States.
> There is no on-premise or customer-hosted deployment option.

### LLM model(s) being used

The current answer is right. One refinement: name the family rather than pinning
a version, so a routine model upgrade does not silently make the disclosure
stale.

> Anthropic Claude, accessed through Anthropic's commercial API. The specific
> Claude model may be updated as Anthropic releases new versions; no other model
> provider is involved in the Slack assistant. Anthropic PBC is listed as a
> subprocessor at https://bratrax.com/subprocessors.

---

## Correct as they stand

Company name, headquarters, terms URL, data host company, sub-processors (Yes +
URL), and "exposes an LLM" (Yes). All three linked pages resolve publicly for a
logged-out reviewer, which is worth knowing because a gated legal page is a
common bounce.
