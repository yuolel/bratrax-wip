# Bratrax Templates - Usage Guide

This directory contains foundational templates for executing repeatable Bratrax client projects.

---

## What's Inside

| Template | Purpose | When to Use |
|----------|---------|-------------|
| **01_Discovery_Questionnaire** | Client intake form | Send to new clients before discovery call |
| **02_Ontology_Template** | Data model & event taxonomy (DTC E-commerce) | After discovery, before implementation |
| **02b_Ontology_Template_SaaS** | Data model & event taxonomy (SaaS) | After discovery, for SaaS businesses |
| **02c_Ontology_Template_B2B_LeadGen** | Data model & event taxonomy (B2B Lead Gen) | After discovery, for lead generation businesses |
| **03_Tracking_Plan** | Developer implementation guide (DTC) | After ontology approval, for engineering team |
| **03b_Tracking_Plan_SaaS** | Developer implementation guide (SaaS) | After ontology approval, for SaaS products |
| **03c_Tracking_Plan_B2B_LeadGen** | Developer implementation guide (B2B Lead Gen) | After ontology approval, for lead gen businesses |
| **04_QA_Validation_Checklist** | Quality assurance checklist | Throughout project, at phase gates |
| **05_dbt_Model_Starter** | Data transformation SQL patterns | When building data pipelines |
| **06_Event_Storming_Workshop** | Event discovery workshop guide | During ontology phase to identify events |
| **PROGRESSIVE_IMPLEMENTATION_WORKFLOW** | Quick reference for progressive approach | Phase-by-phase implementation guide |

---

## How to Use These Templates

### For a New Client Project

**Phase 1: Discovery**
1. Copy `01_Discovery_Questionnaire_Template.md` → `[ClientName]_Discovery.md`
2. Send to client to complete before discovery call
3. Review responses, schedule 60-90 min discovery call
4. After call, create Discovery Summary document (2-3 pages)

**Phase 2: Ontology Design**
1. **Run Event Storming Workshop**
   - Use `06_Event_Storming_Workshop_Guide.md` to facilitate
   - Duration: 90-120 minutes with client stakeholders
   - Output: 12-18 prioritized events organized into tiers
2. Copy `02_Ontology_Template_DTC_Ecommerce.md` → `[ClientName]_Ontology_v1.md`
3. Fill in all sections based on discovery + event storming:
   - Section 1: Business Context (from discovery questionnaire)
   - Section 2: Entity Definitions (customize entities per their business)
   - Section 3: Event Taxonomy (use events from workshop, organized by tier)
   - Section 4: Metric Definitions (define how to calculate each metric)
   - Section 5: Attribution Logic (choose model, define windows)
   - Section 8: Dashboard Structure (specify 3-5 dashboard views)
4. Review with client, get approval before proceeding

**Phase 3: Tracking Implementation (Progressive Approach)**

**Default: Implement in phases - Tier 1 first, then Tier 2, then Tier 3 on-demand**

**Week 1: Implement Tier 1 Events**
1. Copy `03_Tracking_Plan_Template.md` → `[ClientName]_Tracking_Plan_Tier1_v1.md`
2. Include ONLY Tier 1 events from ontology (4-5 events):
   - user_signed_up
   - session_started
   - order_completed
   - email_clicked
3. Share with development team
4. Implement and validate using `04_QA_Validation_Checklist.md` Phase 2

**Week 2: Launch Initial Dashboards**
1. Validate Tier 1 tracking (revenue reconciliation must pass)
2. Build initial dashboards (Executive Overview + Attribution)
3. Client UAT and feedback
4. Let client use dashboards for 1 week

**Week 3-4: Add Tier 2 Events (if needed)**
1. Based on client usage, add Tier 2 events (6-8 additional events)
2. Update tracking plan with Tier 2 specifications
3. Implement, validate, update dashboards
4. Client reviews enhanced dashboards

**Week 5+: Add Tier 3 Selectively**
1. Only add Tier 3 events when client specifically requests functionality
2. Examples: "We need refund tracking" → add order_refunded
3. Update tracking plan and dashboards as needed

**Phase 4: Data Pipeline**
1. Use `05_dbt_Model_Starter_Template.md` as reference
2. Create staging models for each data source
3. Create intermediate models for business logic (attribution, aggregations)
4. Create mart models matching ontology table structure
5. Write dbt tests for data quality
6. Use `04_QA_Validation_Checklist.md` Phase 3 section to validate pipelines

**Phase 5: Quality Assurance**
1. Work through `04_QA_Validation_Checklist.md` systematically
2. Focus on Phase 4: Metric Reconciliation (critical!)
3. Document any discrepancies in "Known Issues" section
4. Get sign-off before building dashboards

**Phase 6: Dashboard Build**
1. Build dashboards per ontology Section 8 specifications
2. Use `04_QA_Validation_Checklist.md` Phase 5 to validate
3. Client UAT and feedback
4. Iterate and finalize

**Phase 7: Go-Live**
1. Complete `04_QA_Validation_Checklist.md` Phase 7
2. Training session with client
3. Handoff and ongoing monitoring

---

---

## Implementation Strategy: Progressive vs All-at-Once

### **Default: Progressive Implementation** (Recommended for most clients)

**Use progressive when:**
- Client is new to analytics
- Fast time-to-value needed (2 weeks vs 4+ weeks)
- Budget/resources constrained
- Client's exact needs are unclear
- First time working with this client

**Timeline:**
- Week 1: Tier 1 events (4-5 events)
- Week 2: Launch dashboards
- Week 3-4: Add Tier 2 (8 total events)
- Week 5+: Add Tier 3 on-demand

### **Exception: All Tiers At Once**

**Only use when:**
- Client has subscription/retention model (Tier 3 critical from day 1)
- Client is sophisticated and knows exactly what they need
- Historical data gaps are unacceptable
- Timeline is flexible (OK waiting 4+ weeks)

**Reference:** See Ontology Template Section 3.3 and Event Storming Guide Part 7 for decision framework.

---

## Business Model: Choosing the Right Template

### **When to Use B2B Lead Gen Templates** 🆕

Use `02c_Ontology_Template_B2B_LeadGen.md` and `03c_Tracking_Plan_B2B_LeadGen.md` when:
- Client generates leads for sales pipeline (not direct transactions)
- Revenue comes from sales team closing deals (not self-service checkout)
- Key metrics are Cost per SQL, MQL-to-SQL rate, lead quality, pipeline value
- Product requires demos, sales calls, or consultations before purchase
- Examples: B2B software, professional services, high-ticket B2C (real estate, education), agencies

**B2B Lead Gen Template Highlights:**
- **Events:** lead_captured, form_submitted, mql_qualified, sql_qualified, demo_scheduled (15-18 events)
- **Metrics:** Cost per SQL, Lead-to-MQL rate, MQL-to-SQL rate, days to SQL, win rate, pipeline value
- **Entities:** Lead, Session, Form_Submission, Content_Engagement, Campaign, Opportunity
- **Focus:** Lead Capture → Qualification (MQL → SQL) → Pipeline → Win/Loss
- **Attribution:** First-touch (default for B2B lead gen)

---

### **When to Use SaaS Templates**

Use `02b_Ontology_Template_SaaS.md` and `03b_Tracking_Plan_SaaS.md` when:
- Client sells software/subscription service (like VidTao)
- Revenue model is recurring (MRR/ARR)
- Key metrics are activation, churn, NRR
- Product has user accounts, trials, subscriptions
- Examples: VidTao, productivity tools, B2B software, consumer apps with subscriptions

**SaaS Template Highlights:**
- **Events:** user_created, user_activated, subscription_created, subscription_cancelled (15-18 events)
- **Metrics:** MRR, ARR, churn rate, activation rate, trial conversion rate, LTV:CAC
- **Entities:** User, Subscription, Account (for B2B), Feature_Usage
- **Focus:** Activation → Conversion → Retention → Expansion

---

### **When to Use DTC E-commerce Templates**

Use `02_Ontology_Template_DTC_Ecommerce.md` and `03_Tracking_Plan_Template.md` when:
- Client sells physical products online
- Revenue model is transactional (one-time purchases or subscription boxes)
- Key metrics are ROAS, CAC, AOV, repeat purchase rate
- Product has shopping cart, checkout flow
- Examples: Skincare brands, apparel, CPG, subscription boxes

**DTC Template Highlights:**
- **Events:** order_completed, product_viewed, product_added_to_cart (15-18 events)
- **Metrics:** ROAS, CAC, LTV, AOV, repeat purchase rate
- **Entities:** User, Order, Product, Marketing_Campaign, Ad_Creative
- **Focus:** Acquisition → Conversion → Repeat Purchase → Attribution

---

### **Hybrid Businesses**

If client has multiple revenue models (e.g., B2B SaaS with sales-assisted deals, or e-commerce with membership):
1. **Start with primary revenue model** template
2. **Add entities/events** from secondary template as needed
3. **Merge metric definitions** carefully (don't double-count revenue)

**Examples:**
- **Subscription box** → Start with DTC template, add subscription events from SaaS template
- **B2B SaaS with sales team** → Start with SaaS template, add lead_captured, sql_qualified from B2B Lead Gen template
- **E-commerce with lead gen form** → Start with DTC template, add form_submitted and lead tracking from B2B Lead Gen
- **High-touch SaaS sales** → Use B2B Lead Gen template for top-of-funnel, merge with SaaS template for post-sale

---

## Template Customization Tips

### Discovery Questionnaire
- **Adjust Section 2.1** to include/exclude platforms relevant to your typical clients
- **Add industry-specific questions** if you specialize (e.g., subscription metrics for SaaS)
- **Modify Section 4.2** metric list to match your common use cases

### Ontology Template
- **Choose the right template:**
  - Use `02_Ontology_Template_DTC_Ecommerce.md` for e-commerce businesses
  - Use `02b_Ontology_Template_SaaS.md` for SaaS/software businesses
  - Use `02c_Ontology_Template_B2B_LeadGen.md` for lead generation businesses
- **Start with the provided structure** and customize
- **Add entities specific to their business** (e.g., Swipe_Board for VidTao-style apps, or Lead_Score_History for sophisticated B2B)
- **Focus on Section 3.2 event catalog** - organize events into Tier 1, Tier 2, Tier 3
- **Event count target:** 15-18 total events (4-5 in Tier 1, 6-8 in Tier 2, 3-5 in Tier 3)
- **Use VidTao as reference** - they reduced from 44 to 18 events

### Tracking Plan
- **Section 2.1 Tech Stack** - Update with client's actual platform
- **Section 4 & 5** - Delete events not in their ontology, add any custom events
- **Section 6** - Customize session/UTM logic if they use different parameters
- **Section 9** - Add platform-specific notes (Shopify, React, etc.)

### QA Checklist
- **Adjust SQL queries** to match your BigQuery project/dataset names
- **Add client-specific validation checks** based on their unique requirements
- **Update Phase 4 reconciliation targets** with their acceptable error ranges

### dbt Templates
- **Rename tables/fields** to match ontology exactly
- **Adjust materialization strategies** based on data volume (view vs table vs incremental)
- **Copy attribution logic** from ontology Section 5 into `int_order_attribution.sql`
- **Add custom business logic** as intermediate models

---

## Placeholder Reference

When customizing templates, replace these placeholders:

| Placeholder | Replace With | Example |
|-------------|--------------|---------|
| `[CLIENT_NAME]` | Client company name | `Lumina Skincare` |
| `[DATE]` | Current date | `2025-01-15` |
| `[YOUR_NAME]` | Your name | `Alex Chen` |
| `[YOUR_EMAIL]` | Your email | `alex@bratrax.com` |
| `[SOURCE_NAME]` | Data source name | `Shopify`, `Klaviyo` |
| `[AOV]` | Average order value | `$85` |

**Pro tip:** Use find-and-replace to update all placeholders at once after copying.

---

## File Naming Convention

**For client deliverables:**
```
[ClientName]_[DocumentType]_[Version].md

Examples:
LuminaSkincare_Discovery_v1.md
LuminaSkincare_Ontology_v2.md
LuminaSkincare_TrackingPlan_v1.md
```

**For dbt models:**
```
[layer]_[source]_[entity].sql

Examples:
stg_shopify_orders.sql
int_user_first_orders.sql
fact_orders.sql
dim_users.sql
```

---

## Version Control

**For ontology and tracking plan documents:**
- Create v1 for initial version
- Increment version (v2, v3) for significant changes after client review
- Add change log at bottom of document noting what changed

**For dbt models:**
- Version control via git (no version numbers in filename)
- Use git commit messages to track changes

---

## Collaboration with Claude (Me!)

### When You Need Help

**Starting a new client:**
> "New client: [ClientName]. Business model: [DTC/SaaS/etc]. Tech stack: [list tools]. I've completed the discovery questionnaire. Help me draft their ontology."

Then share the completed discovery questionnaire responses.

**Reviewing a deliverable:**
> "Review this ontology document for [ClientName]. Check for: completeness, event naming consistency, metric formula accuracy, and any gaps."

Attach or paste the document.

**Generating tracking plan:**
> "Generate the tracking plan for [ClientName] based on this ontology document."

Share the approved ontology.

**Writing dbt models:**
> "Write dbt models for [ClientName]. Here's their ontology and raw data schema from [Shopify/etc]."

Share ontology + sample of raw data structure.

**Troubleshooting:**
> "Revenue reconciliation failing for [ClientName]. Bratrax shows $X, Shopify shows $Y. Help debug."

Share the discrepancy details and any relevant SQL queries.

---

## Quality Checklist Before Client Handoff

Before sharing any deliverable with a client, verify:

- [ ] All `[PLACEHOLDER]` values replaced with actual values
- [ ] Client name spelled correctly throughout
- [ ] No internal notes or TODOs left in document
- [ ] Metric definitions match their business definitions
- [ ] Attribution logic appropriate for their customer journey
- [ ] Dashboard views answer their stated business questions
- [ ] All sections relevant to their business (delete N/A sections)
- [ ] Professional formatting (consistent headers, no typos)
- [ ] Version number and date updated

---

## Template Improvement Process

As you complete client projects, improve these templates:

**What to capture:**
- Common questions clients ask → Add to Discovery Questionnaire
- New event patterns → Add to Ontology Template
- Implementation gotchas → Add to Tracking Plan
- Data quality issues → Add to QA Checklist
- Reusable SQL patterns → Add to dbt Templates

**How to update:**
1. Make changes to the template files
2. Add a note in the template's change log
3. Version the templates (e.g., add "v1.1" to README)
4. Share updates with team

---

## Additional Resources

**Reference materials in this project:**
- `VidTao example/` - Real-world implementation example
- `resources and references/` - Design principles, analytics workbooks
- `frameworks/Bratrax Onboarding Process Framework v1 Draft.md` - Process overview

**External resources:**
- [dbt Documentation](https://docs.getdbt.com/)
- [Segment Spec](https://segment.com/docs/connections/spec/)
- [BigQuery Standard SQL](https://cloud.google.com/bigquery/docs/reference/standard-sql/)

---

## Getting Started - Quick Start

**If this is your first time:**

1. **Read** the VidTao Implementation Guide (`VidTao example/VidTao_Implementation_Guide.md`)
2. **Skim** all 5 templates to understand what's in each
3. **Copy** the Discovery Questionnaire for your first client
4. **Send** it to them to fill out
5. **Review** with them, then come back and use the Ontology Template

**If you're mid-project:**
- Jump to the relevant template for your current phase
- Use the QA Checklist to validate before moving to next phase

---

## Questions?

If you have questions about:
- **Using these templates** → Reference this README or ask Claude (me!)
- **Client-specific implementation** → Provide context and ask Claude for help
- **Process improvements** → Document and discuss with team

---

## Template Versions

| Date | Version | Changes |
|------|---------|---------|
| 2025-01-13 | 1.0 | Initial template set created |

---

*Built with the Dummy-First methodology: Design first, wire later.*
