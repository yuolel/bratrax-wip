# Privacy policy amendment — Slack app + server-side AI

Proposed changes to `privacy/index.html` (effective July 29, 2026). **Drafted,
not applied** — this is legal text on a live page, so it needs your sign-off
before it goes in. Say the word and I'll apply all six.

Each change below is paste-ready HTML with the exact line anchor and the exact
current text to replace. There are no `href="#"` anchors anywhere in the file and
the only cross-references are to Sections 10 and 12, so the renumbering in change
**C** is safe.

## Why this is a submission blocker

Two things are wrong today, and one is worse than the Slack gap.

**The policy currently states something that is false.** Twice. The Slack
assistant answers questions by calling Anthropic's Claude from Bratrax's own
servers, on **Bratrax's API key** by default (per-client BYOK exists but is not
the default — key resolution is `rill_clients.anthropic_api_key` →
`SLACK_ANTHROPIC_API_KEY` → `ANTHROPIC_API_KEY`, first non-empty wins). The
policy says the opposite in the summary and again in §4.2.

**Anthropic is therefore an undisclosed subprocessor.** §4.2's "Bratrax is not a
subprocessor in that data flow" was accurate when MCP-with-your-own-key was the
only AI path. It is not accurate for a Bratrax-operated AI feature. This is a
larger disclosure gap than the Slack one and would matter to an EU customer's DPA
review independently of the Marketplace submission.

The Slack-specific gaps (§2.2 never names Slack; §4.1 doesn't list it) are what
Slack's reviewers check for. Both are fixed below.

---

## A. Summary bullet — the outright contradiction

**Line 255.** Replace:

```html
      <li><strong>Your LLM, your terms.</strong> If you connect Claude, ChatGPT, or another AI provider through the Model Context Protocol (MCP), data you query flows directly to that provider under its own terms. Bratrax does not route your data through any LLM.</li>
```

with:

```html
      <li><strong>AI features.</strong> When you use an AI feature we operate &mdash; such as the Bratrax assistant for Slack &mdash; your question and the data needed to answer it are sent to Anthropic (Claude) to generate the response. Anthropic is a named subprocessor and does not train on this data. If you instead connect your own AI provider through the Model Context Protocol (MCP), that data flows directly to your provider under your own contract with them.</li>
```

Keeping "does not train on this data" here means confirming it against your
Anthropic commercial terms first. It is true of the Anthropic API's standard
commercial terms; verify it applies to your account before publishing, or cut the
clause.

---

## B. Section 2.2 — refresh the stale platform list

**Line 286.** The "may be supported in the future" line is now out of date on its
own terms: TikTok Ads and Klaviyo both shipped. Replace:

```html
    <li>Additional platforms (including TikTok Ads and Klaviyo) may be supported in the future.</li>
```

with:

```html
    <li><strong>WooCommerce:</strong> store metadata, orders, customers, products, and revenue data.</li>
    <li><strong>Other advertising and marketing platforms:</strong> TikTok Ads, Microsoft Bing Ads, Pinterest, Taboola, Outbrain, and Klaviyo &mdash; each providing account information, campaign or campaign-equivalent structure, spend, and engagement or conversion events.</li>
    <li>Additional platforms may be supported in the future.</li>
```

---

## C. New Section 2.3 — Slack workspace data

Slack is a different kind of connection from the rest of §2.2: not a data source
you pull from, but a surface Bratrax reads from and writes into. It earns its own
subsection.

**Insert after line 288** (after §2.2's closing "You can revoke access at any
time from the source platform." paragraph, before the `2.3 Information collected
automatically` heading). Then **renumber** the two headings that follow:
`2.3 Information collected automatically` → **2.4**, and
`2.4 Information we do not collect` → **2.5**.

```html
  <h3>2.3 Information we collect from Slack</h3>
  <p>If you connect the Bratrax assistant to your Slack workspace, we collect and store the following:</p>
  <ul>
    <li><strong>Workspace and installation details:</strong> your Slack workspace (team) ID, enterprise ID where applicable, workspace name, the bot access token issued to us, the granted permission scopes, and the identity of the Bratrax user who performed the installation.</li>
    <li><strong>Channel links:</strong> where a specific channel is linked to a Bratrax account, the channel ID and name.</li>
  </ul>
  <p><strong>We do not store the content of your Slack messages.</strong> When you mention the assistant or send it a direct message, we read that message and, for follow-up questions, the recent messages in that conversation thread, in order to answer. That content is processed in memory to generate the reply and is not written to our database. Message content is sent to Anthropic to produce the answer, as described in Section 4.2.</p>
  <p>The assistant only reads conversations it participates in &mdash; channels it has been invited to and direct messages sent to it. It cannot read channels it is not a member of. It responds only when mentioned or messaged directly; it does not post on its own initiative.</p>
  <p>In the shared Bratrax community workspace, we read the email address associated with your Slack account in order to match you to your Bratrax account so the assistant answers with the right store's data.</p>
  <p>You can disconnect at any time from <strong>Settings &rarr; Slack</strong> in Bratrax, or by removing the app from your Slack workspace. Either action revokes the bot token with Slack and deletes the stored installation record and any associated channel links.</p>
```

That last paragraph is the one reviewers look for, and it is accurate: disconnect
revokes the token Slack-side, and an uninstall fires `app_uninstalled`, which
revokes automatically.

---

## D. Section 4.1 — add both subprocessors

**Line 340**, in the subprocessor table. Add two rows after the `Google Analytics`
row:

```html
        <tr><td><strong>Anthropic</strong> (United States)</td><td>Powers AI features we operate, including the Bratrax assistant for Slack</td><td>Your question and the store data needed to answer it</td></tr>
        <tr><td><strong>Slack</strong> (Salesforce, United States)</td><td>Delivers assistant responses into your Slack workspace, where you have connected one</td><td>Message content and any figures, tables, or charts in the reply</td></tr>
```

The Slack row matters for a reason that is easy to miss: when the bot posts
revenue figures into a channel, Customer Data flows to Slack. That is a genuine
new disclosure, not a formality.

Both are US vendors, which interacts with the EU-data-residency claim in §5 and
the summary. §5 already says Customer Data is "primarily" hosted in the EU, so it
is not contradicted — but if you want to be airtight, add to §5: *"Where you use
AI features or the Slack assistant, the data needed to answer a given question is
transmitted to service providers in the United States under standard contractual
clauses."*

---

## E. Section 4.2 — split customer-initiated from Bratrax-operated

**Lines 344–345.** Replace the heading and its paragraph:

```html
  <h3>4.2 LLM providers (customer-initiated)</h3>
  <p>If you connect an AI provider to Bratrax through the Model Context Protocol (MCP) — for example, Anthropic's Claude or OpenAI's ChatGPT — any data you query flows directly from Bratrax to that provider under your contract with that provider. <strong>Bratrax is not a subprocessor in that data flow.</strong> We do not send your data to any LLM unless you initiate the connection. The provider's own privacy terms govern what they do with the data. We are not responsible for their data practices.</p>
```

with:

```html
  <h3>4.2 AI providers</h3>
  <p>There are two distinct ways your data can reach an AI provider, and they carry different responsibilities.</p>
  <p><strong>AI features we operate.</strong> Some Bratrax features generate answers using a large language model on our infrastructure &mdash; today, the Bratrax assistant for Slack. When you ask it a question, your message, the recent context of that conversation thread, and the store data needed to answer are sent to <strong>Anthropic</strong> (Claude) to produce the response. Anthropic is a named subprocessor in Section 4.1 and processes this data on our instructions. These features are optional: they process data only when you use them, and only for the account they are connected to.</p>
  <p>Enterprise customers may supply their own Anthropic API key, in which case that traffic runs under your own contract with Anthropic rather than ours.</p>
  <p><strong>AI providers you connect yourself.</strong> If you connect an AI provider to Bratrax through the Model Context Protocol (MCP) &mdash; for example, Anthropic's Claude or OpenAI's ChatGPT &mdash; any data you query flows directly from Bratrax to that provider under your contract with that provider. <strong>Bratrax is not a subprocessor in that data flow.</strong> The provider's own privacy terms govern what they do with the data, and we are not responsible for their data practices.</p>
```

---

## F. Section 6 — retention for Slack data

**Line 375**, in the retention list. Add before the `Backups` item:

```html
    <li><strong>Slack connection data:</strong> workspace installation records and channel links are retained while the connection is active and deleted when you disconnect the app or remove it from your Slack workspace. We do not retain Slack message content.</li>
```

---

## G. Effective date

Bump the effective date at the top of the page when these land. A privacy policy
that gains a subprocessor without a date change is the kind of detail a
sharp-eyed reviewer or DPA-conscious customer notices.

---

## One thing I could not verify

Whether your Anthropic account is on terms that exclude training on API inputs.
The standard commercial terms do; I have no way to confirm your account from this
repo. Change **A** asserts it. Confirm or cut before publishing.
