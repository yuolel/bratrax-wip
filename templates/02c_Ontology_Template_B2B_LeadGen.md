# [CLIENT_NAME] Analytics Ontology

**Version:** 1.0
**Date:** [DATE]
**Business Model:** B2B Lead Generation
**Prepared by:** [YOUR_NAME]

---

## Document Purpose

This ontology defines the data model, events, metrics, and business logic for [CLIENT_NAME]'s analytics dashboard. It serves as the single source of truth for:
- What entities exist in the data model
- What events we track
- How metrics are calculated
- How data relationships work

**All downstream work (tracking implementation, data pipelines, dashboards) references this document.**

---

## 1. Business Context

### 1.1 Business Model Summary
**What you offer:** [Product/Service description]

**Revenue model:** [Leads → Sales pipeline / Direct sales / Channel partners]

**Lead value:**
- Average deal size: $[X]
- Average sales cycle: [X] days
- Win rate: [X]%
- Average lead value: $[calculated: deal_size × win_rate]

**Lead sources:** [Paid ads / Content / Events / Partnerships / Referrals]

**Primary growth goal:** [Lead volume / Lead quality / Cost per SQL / Win rate / Sales cycle velocity]

### 1.2 Key Business Questions
The dashboards must answer these questions:

1. [Question 1, e.g., "Which channels generate the highest quality SQLs?"]
2. [Question 2, e.g., "What's our true cost per SQL by channel?"]
3. [Question 3, e.g., "How long does it take to nurture an MQL to SQL?"]
4. [Question 4, e.g., "Which content assets drive the most conversions?"]
5. [Question 5, e.g., "What lead scoring factors predict closed-won deals?"]

---

## 2. Entity Definitions

Entities are the "nouns" of the business—the things we track.

### 2.1 Core Entities

#### **Lead**
A person or organization that has expressed interest in your offering.

| Property | Type | Definition | Example |
|----------|------|------------|---------|
| `lead_id` | string | Unique identifier (primary key) | `lead_a3b4c5d6` |
| `email` | string | Lead email address | `john@acmecorp.com` |
| `company_name` | string | Organization name | `Acme Corp` |
| `created_at` | timestamp | When lead first captured | `2025-01-15T10:30:00Z` |
| `lead_status` | string | Current stage in funnel | `new`, `mql`, `sql`, `opportunity`, `won`, `lost` |
| `lead_score` | integer | Qualification score (0-100) | `75` |
| `acquisition_source` | string | First-touch marketing source | `google_ads`, `webinar`, `content_download` |
| `acquisition_campaign` | string | First-touch campaign | `q1_demo_campaign` |
| `job_title` | string | Lead's role | `Director of Marketing` |
| `company_size` | string | Employee count bucket | `1-10`, `11-50`, `51-200`, `201-500`, `500+` |
| `industry` | string | Industry vertical | `SaaS`, `Manufacturing`, `Healthcare` |
| `country` | string | Geographic location | `United States` |
| `phone` | string | Contact number | `+1-555-0123` |
| `mql_at` | timestamp | When qualified as MQL | `2025-01-16T14:22:00Z` |
| `sql_at` | timestamp | When qualified as SQL | `2025-01-18T09:15:00Z` |
| `assigned_to` | string | Sales rep assigned | `sarah@company.com` |

**Business logic:**
- **New Lead:** Just captured, not yet qualified
- **MQL (Marketing Qualified Lead):** Meets basic criteria (score threshold, engagement level, or ICP fit)
- **SQL (Sales Qualified Lead):** Sales team has vetted, ready for outreach/demo
- **Opportunity:** Active sales conversation, in CRM pipeline
- **Won:** Closed as customer
- **Lost:** Disqualified or lost deal

**Lead Scoring Example:**
- Downloaded whitepaper: +10 points
- Attended webinar: +20 points
- Visited pricing page: +15 points
- Opened 3+ emails: +10 points
- Company size 50+: +15 points
- Decision-maker title: +20 points
- MQL threshold: 50 points
- SQL threshold: Sales team manual qualification

---

#### **Session**
A period of website activity (for anonymous or identified visitors).

| Property | Type | Definition | Example |
|----------|------|------------|---------|
| `session_id` | string | Unique identifier | `sess_x7y8z9` |
| `lead_id` | string | Associated lead (if identified) | `lead_a3b4c5d6` |
| `started_at` | timestamp | Session start time | `2025-01-15T10:30:00Z` |
| `ended_at` | timestamp | Session end time | `2025-01-15T10:45:00Z` |
| `utm_source` | string | Marketing source parameter | `linkedin` |
| `utm_medium` | string | Marketing medium parameter | `cpc` |
| `utm_campaign` | string | Campaign identifier | `q1_demo_campaign` |
| `utm_content` | string | Ad/content variant | `carousel_ad_v2` |
| `landing_page` | string | First page viewed | `/solutions/marketing-automation` |
| `referrer` | string | Referring URL | `https://linkedin.com` |
| `device_type` | string | Device category | `desktop`, `mobile`, `tablet` |
| `pages_viewed` | integer | Total pages in session | `5` |

**Business logic:**
- Session timeout: 30 minutes of inactivity
- UTM parameters captured at session start only
- Attribution stored on first session (first-touch)

---

#### **Form Submission**
A completed lead capture form (contact, demo request, gated content, etc.).

| Property | Type | Definition | Example |
|----------|------|------------|---------|
| `form_id` | string | Unique submission identifier | `form_sub_abc123` |
| `lead_id` | string | Associated lead | `lead_a3b4c5d6` |
| `form_type` | string | Type of form | `contact_us`, `demo_request`, `content_download`, `newsletter` |
| `submitted_at` | timestamp | Submission timestamp | `2025-01-15T10:35:00Z` |
| `form_name` | string | Form identifier | `Homepage Demo Request` |
| `page_url` | string | Page where form submitted | `/solutions/marketing-automation` |
| `session_id` | string | Session when submitted | `sess_x7y8z9` |
| `utm_source` | string | Attribution at submission | `linkedin` |
| `utm_campaign` | string | Campaign at submission | `q1_demo_campaign` |

**Business logic:**
- First form submission creates the lead
- Subsequent submissions update lead profile and add to activity history
- Different forms have different lead scores

---

#### **Content Engagement**
Interaction with marketing content (blog, case study, video, etc.).

| Property | Type | Definition | Example |
|----------|------|------------|---------|
| `engagement_id` | string | Unique identifier | `eng_xyz789` |
| `lead_id` | string | Associated lead (if known) | `lead_a3b4c5d6` |
| `content_type` | string | Type of content | `blog_post`, `case_study`, `video`, `webinar`, `whitepaper` |
| `content_title` | string | Content name | `5 Ways to Improve B2B Conversion Rates` |
| `content_id` | string | Content identifier | `blog_post_123` |
| `engaged_at` | timestamp | Engagement timestamp | `2025-01-15T10:40:00Z` |
| `engagement_action` | string | Type of action | `viewed`, `downloaded`, `shared`, `completed` |
| `session_id` | string | Session when engaged | `sess_x7y8z9` |

**Business logic:**
- Tracks which content influences lead journey
- Used for content attribution and lead scoring
- "Completed" for webinars = attended full session

---

#### **Campaign**
A marketing initiative designed to generate leads.

| Property | Type | Definition | Example |
|----------|------|------------|---------|
| `campaign_id` | string | Unique identifier | `camp_q1_demo` |
| `campaign_name` | string | Campaign name | `Q1 2025 Demo Campaign` |
| `campaign_type` | string | Campaign category | `paid_ads`, `email`, `webinar`, `content`, `event` |
| `channel` | string | Primary channel | `linkedin`, `google_ads`, `email` |
| `started_at` | timestamp | Campaign start date | `2025-01-01T00:00:00Z` |
| `ended_at` | timestamp | Campaign end date | `2025-03-31T23:59:59Z` |
| `budget` | decimal | Total budget allocated | `50000.00` |
| `spend` | decimal | Actual spend to date | `32500.00` |
| `target_audience` | string | ICP description | `Marketing Directors at B2B SaaS companies, 50-200 employees` |

**Business logic:**
- Budget and spend tracked for ROI calculation
- Can have multiple ad sets or emails within one campaign

---

### 2.2 Relationship Diagram

```
Session → Lead → Form Submission → Campaign
   ↓         ↓
Content ← Lead
```

**Key relationships:**
- A **Session** can create or be associated with a **Lead**
- A **Lead** is created via **Form Submission**
- **Form Submissions** are attributed to **Campaigns** via UTM parameters
- **Content Engagement** influences **Lead** scoring and qualification
- Multiple **Sessions** can belong to one **Lead** (return visits)

---

## 3. Event Taxonomy

Events are the "verbs"—the actions that happen in the business.

### 3.1 Event Naming Convention

Format: `{entity}_{activity}`

Examples:
- ✅ `lead_captured`
- ✅ `form_submitted`
- ✅ `mql_qualified`
- ❌ `new_lead` (missing verb)
- ❌ `submit_form` (wrong order)

### 3.2 Event Catalog by Priority Tier

Events organized into 3 tiers for progressive implementation.

---

### **Tier 1: Critical Events (Week 1)** ⭐

Implement these first. They enable core lead gen dashboards.

#### Event Count: 5-6 events

---

##### `lead_captured` ⭐ **MOST CRITICAL**
**When:** A new lead is created (first form submission or identified visitor)

**Why critical:** Creates the lead record, tracks lead volume and acquisition sources

**Properties:**
- `lead_id` (string, required)
- `email` (string, required)
- `company_name` (string, optional)
- `job_title` (string, optional)
- `company_size` (string, optional)
- `acquisition_source` (string, required) - e.g., `google_ads`, `linkedin`, `organic`
- `acquisition_campaign` (string, optional)
- `utm_source`, `utm_medium`, `utm_campaign`, `utm_content` (strings, optional)
- `landing_page` (string, required)
- `form_type` (string, required) - e.g., `demo_request`, `contact_us`, `content_download`
- `lead_score` (integer, default: 0)

**Triggered by:** First form submission, chatbot conversion, or manual import

**Server-side or client-side?** Server-side (after form validation and lead creation in CRM)

---

##### `session_started`
**When:** Visitor lands on website (anonymous or identified)

**Why critical:** Traffic and attribution tracking

**Properties:**
- `session_id` (string, required)
- `lead_id` (string, optional) - if identified visitor
- `utm_source`, `utm_medium`, `utm_campaign`, `utm_content` (strings, optional)
- `landing_page` (string, required)
- `referrer` (string, optional)
- `device_type` (string, required)
- `ip_address` (string, for geo-location)

**Triggered by:** First page load in session

**Server-side or client-side?** Client-side (JavaScript)

---

##### `form_submitted`
**When:** User submits any form (demo request, contact, gated content, newsletter)

**Why critical:** Lead capture and conversion tracking

**Properties:**
- `form_id` (string, required)
- `lead_id` (string, required)
- `form_type` (string, required) - e.g., `demo_request`, `contact_us`, `whitepaper_download`
- `form_name` (string, required)
- `page_url` (string, required)
- `session_id` (string, required)
- `utm_source`, `utm_campaign` (strings, optional)
- `is_first_form` (boolean, required) - true if this creates the lead

**Triggered by:** Form submission success

**Server-side or client-side?** Server-side (after validation)

---

##### `mql_qualified`
**When:** Lead reaches MQL (Marketing Qualified Lead) threshold

**Why critical:** Measures marketing funnel effectiveness

**Properties:**
- `lead_id` (string, required)
- `lead_score` (integer, required)
- `qualification_criteria` (string, optional) - e.g., `score_threshold`, `manual_review`
- `qualified_at` (timestamp, required)
- `days_to_mql` (integer, required) - days since lead_captured
- `touchpoints_to_mql` (integer, optional) - number of interactions before MQL

**Triggered by:** Lead scoring automation or manual qualification

**Server-side or client-side?** Server-side (CRM/automation platform)

---

##### `sql_qualified`
**When:** Lead reaches SQL (Sales Qualified Lead) status (sales team accepts)

**Why critical:** Measures lead quality and marketing-to-sales handoff

**Properties:**
- `lead_id` (string, required)
- `lead_score` (integer, required)
- `qualified_by` (string, required) - sales rep email
- `qualification_reason` (string, optional) - e.g., `budget_confirmed`, `decision_maker`, `timeline_30_days`
- `qualified_at` (timestamp, required)
- `days_to_sql` (integer, required) - days since lead_captured
- `assigned_to` (string, required) - sales rep email

**Triggered by:** Sales rep accepts lead in CRM

**Server-side or client-side?** Server-side (CRM integration)

---

##### `email_clicked` (Optional Tier 1)
**When:** Lead clicks link in marketing email

**Why critical:** Email engagement and nurture effectiveness

**Properties:**
- `email_id` (string, required)
- `lead_id` (string, required)
- `campaign_id` (string, required)
- `email_subject` (string, required)
- `link_url` (string, required)
- `link_name` (string, optional)
- `clicked_at` (timestamp, required)

**Triggered by:** Email tracking pixel/redirect

**Server-side or client-side?** Server-side (email platform webhook)

---

### **Tier 2: Engagement Events (Week 3-4)**

Add after Tier 1 is live and validated. These provide deeper funnel insights.

#### Event Count: 6-8 events

---

##### `page_viewed`
**When:** Lead or anonymous visitor views a key page (pricing, solutions, case studies)

**Why useful:** Page-level engagement, intent signals

**Properties:**
- `session_id` (string, required)
- `lead_id` (string, optional)
- `page_url` (string, required)
- `page_title` (string, required)
- `page_category` (string, optional) - e.g., `pricing`, `solution`, `case_study`, `blog`
- `time_on_page` (integer, optional) - seconds

**Triggered by:** Page load for tracked pages

**Server-side or client-side?** Client-side

---

##### `content_downloaded`
**When:** Lead downloads gated content (whitepaper, case study, template)

**Why useful:** Content attribution, lead scoring

**Properties:**
- `lead_id` (string, required)
- `content_type` (string, required) - e.g., `whitepaper`, `case_study`, `template`, `ebook`
- `content_title` (string, required)
- `content_id` (string, required)
- `session_id` (string, required)
- `page_url` (string, required)

**Triggered by:** Successful download after form submission

**Server-side or client-side?** Server-side

---

##### `demo_scheduled`
**When:** Lead books a demo or sales call

**Why useful:** High-intent conversion event, pipeline prediction

**Properties:**
- `lead_id` (string, required)
- `demo_type` (string, required) - e.g., `live_demo`, `recorded_demo`, `sales_call`
- `scheduled_for` (timestamp, required)
- `scheduled_at` (timestamp, required)
- `calendly_event_id` (string, optional) - if using Calendly
- `meeting_duration` (integer, optional) - minutes

**Triggered by:** Calendar booking confirmation

**Server-side or client-side?** Server-side (calendar integration webhook)

---

##### `demo_attended`
**When:** Lead attends scheduled demo/call

**Why useful:** Demo attendance rate, qualification signal

**Properties:**
- `lead_id` (string, required)
- `demo_type` (string, required)
- `scheduled_for` (timestamp, required)
- `attended_at` (timestamp, required)
- `duration` (integer, optional) - actual minutes attended
- `sales_rep` (string, required)
- `attended_status` (string, required) - `attended`, `no_show`, `rescheduled`

**Triggered by:** Sales rep logs outcome in CRM

**Server-side or client-side?** Server-side (CRM)

---

##### `webinar_registered`
**When:** Lead registers for webinar/event

**Why useful:** Event marketing effectiveness

**Properties:**
- `lead_id` (string, required)
- `webinar_id` (string, required)
- `webinar_title` (string, required)
- `webinar_date` (timestamp, required)
- `registered_at` (timestamp, required)
- `registration_source` (string, optional) - e.g., `landing_page`, `email_invite`, `linkedin_ad`

**Triggered by:** Webinar registration confirmation

**Server-side or client-side?** Server-side (webinar platform webhook)

---

##### `webinar_attended`
**When:** Lead attends webinar

**Why useful:** Engagement quality, lead scoring

**Properties:**
- `lead_id` (string, required)
- `webinar_id` (string, required)
- `webinar_title` (string, required)
- `attended_at` (timestamp, required)
- `attendance_duration` (integer, required) - minutes
- `attendance_percentage` (integer, required) - % of webinar attended
- `polls_answered` (integer, optional)
- `questions_asked` (integer, optional)

**Triggered by:** Webinar platform data

**Server-side or client-side?** Server-side (webinar platform integration)

---

##### `lead_scored`
**When:** Lead score changes due to activity

**Why useful:** Score change tracking, trigger analysis

**Properties:**
- `lead_id` (string, required)
- `previous_score` (integer, required)
- `new_score` (integer, required)
- `score_change` (integer, required) - delta
- `trigger_event` (string, required) - what caused the change
- `scored_at` (timestamp, required)

**Triggered by:** Lead scoring automation

**Server-side or client-side?** Server-side (marketing automation)

---

##### `email_opened`
**When:** Lead opens marketing email

**Why useful:** Email engagement, nurture tracking

**Properties:**
- `email_id` (string, required)
- `lead_id` (string, required)
- `campaign_id` (string, required)
- `email_subject` (string, required)
- `opened_at` (timestamp, required)
- `opens_count` (integer, optional) - if opened multiple times

**Triggered by:** Email tracking pixel

**Server-side or client-side?** Server-side (email platform webhook)

---

### **Tier 3: Advanced Events (Week 5+, as needed)**

Implement selectively based on specific needs.

#### Event Count: 3-5 events

---

##### `opportunity_created`
**When:** Lead is converted to a sales opportunity in CRM

**Why useful:** Pipeline tracking, conversion rates

**Properties:**
- `lead_id` (string, required)
- `opportunity_id` (string, required)
- `opportunity_name` (string, required)
- `deal_value` (decimal, required)
- `expected_close_date` (timestamp, required)
- `stage` (string, required) - e.g., `discovery`, `proposal`, `negotiation`
- `created_at` (timestamp, required)

**Triggered by:** CRM integration

**Server-side or client-side?** Server-side (CRM)

---

##### `deal_won`
**When:** Opportunity closes as won (becomes customer)

**Why useful:** ROI calculation, attribution

**Properties:**
- `lead_id` (string, required)
- `opportunity_id` (string, required)
- `deal_value` (decimal, required)
- `closed_at` (timestamp, required)
- `days_in_pipeline` (integer, required)
- `acquisition_source` (string, required) - first-touch
- `acquisition_campaign` (string, optional)

**Triggered by:** CRM integration

**Server-side or client-side?** Server-side (CRM)

---

##### `deal_lost`
**When:** Opportunity closes as lost

**Why useful:** Loss analysis, funnel drop-off

**Properties:**
- `lead_id` (string, required)
- `opportunity_id` (string, required)
- `expected_deal_value` (decimal, optional)
- `closed_at` (timestamp, required)
- `loss_reason` (string, optional) - e.g., `price`, `competitor`, `timing`, `no_budget`
- `stage_lost_at` (string, required)

**Triggered by:** CRM integration

**Server-side or client-side?** Server-side (CRM)

---

##### `chatbot_conversation`
**When:** Lead engages with chatbot on website

**Why useful:** Chat-to-lead conversion, engagement quality

**Properties:**
- `lead_id` (string, optional) - if identified
- `session_id` (string, required)
- `conversation_id` (string, required)
- `started_at` (timestamp, required)
- `ended_at` (timestamp, optional)
- `messages_exchanged` (integer, required)
- `lead_captured` (boolean, required) - did chat result in lead creation?

**Triggered by:** Chatbot platform

**Server-side or client-side?** Server-side (chatbot integration)

---

##### `ad_clicked`
**When:** User clicks on paid ad (LinkedIn, Google, Facebook)

**Why useful:** Ad-level attribution, click-to-lead tracking

**Properties:**
- `ad_id` (string, required)
- `campaign_id` (string, required)
- `ad_platform` (string, required) - e.g., `google_ads`, `linkedin_ads`, `facebook_ads`
- `ad_name` (string, required)
- `clicked_at` (timestamp, required)
- `landing_page` (string, required)
- `cost_per_click` (decimal, optional)

**Triggered by:** Ad platform webhook or UTM tracking

**Server-side or client-side?** Server-side (ad platform API)

---

### 3.3 Implementation Strategy

**Default approach: Progressive Implementation**

Events are organized into 3 tiers. **Implement progressively** (Tier 1 → validate → Tier 2 → validate → Tier 3 as needed).

**Timeline:**
- **Week 1:** Implement Tier 1 (5-6 events)
- **Week 2:** Launch initial dashboards, validate tracking
- **Week 3-4:** Add Tier 2 events (11-14 total) based on usage
- **Week 5+:** Add Tier 3 selectively as needed

**Why progressive?**
- Get to value faster (2 weeks vs 4+ weeks)
- Validate data quality before expanding
- Focus on what matters most first
- Reduce implementation risk

**When to implement all at once?**
- Client explicitly requests it
- Technical implementation is very simple (all events via one CRM integration)
- You have high confidence in data quality

---

## 4. Key Metrics

Metrics are calculations derived from events and entities.

### 4.1 Lead Generation Metrics

#### **Lead Volume**
**Definition:** Total number of new leads created in time period

**Calculation:**
```sql
COUNT(DISTINCT lead_id)
WHERE created_at BETWEEN [start_date] AND [end_date]
```

**Displayed as:** Line chart by week/month, number

**Business logic:**
- Filter by `acquisition_source` or `acquisition_campaign` for channel-specific volume

---

#### **MQL Volume**
**Definition:** Total number of Marketing Qualified Leads

**Calculation:**
```sql
COUNT(DISTINCT lead_id)
WHERE mql_at BETWEEN [start_date] AND [end_date]
```

**Displayed as:** Line chart, number

---

#### **SQL Volume**
**Definition:** Total number of Sales Qualified Leads

**Calculation:**
```sql
COUNT(DISTINCT lead_id)
WHERE sql_at BETWEEN [start_date] AND [end_date]
```

**Displayed as:** Line chart, number

---

#### **Lead-to-MQL Conversion Rate**
**Definition:** Percentage of leads that become MQLs

**Calculation:**
```sql
(COUNT(DISTINCT leads with mql_at) / COUNT(DISTINCT lead_id)) * 100
WHERE created_at BETWEEN [start_date] AND [end_date]
```

**Displayed as:** Percentage, line chart over time

**Business logic:**
- Cohorted by lead creation date for accurate funnel tracking

---

#### **MQL-to-SQL Conversion Rate**
**Definition:** Percentage of MQLs that become SQLs

**Calculation:**
```sql
(COUNT(DISTINCT leads with sql_at) / COUNT(DISTINCT leads with mql_at)) * 100
WHERE mql_at BETWEEN [start_date] AND [end_date]
```

**Displayed as:** Percentage

---

### 4.2 Cost & Efficiency Metrics

#### **Cost Per Lead (CPL)**
**Definition:** Average cost to acquire one lead

**Calculation:**
```sql
SUM(campaign.spend) / COUNT(DISTINCT lead_id)
WHERE acquisition_campaign IN [campaigns] AND created_at BETWEEN [start_date] AND [end_date]
```

**Displayed as:** Currency amount, by channel/campaign

**Business logic:**
- Group by `acquisition_source` or `acquisition_campaign`
- Include all marketing spend (ads, events, tools)

---

#### **Cost Per MQL**
**Definition:** Average cost to acquire one MQL

**Calculation:**
```sql
SUM(campaign.spend) / COUNT(DISTINCT leads with mql_at)
WHERE acquisition_campaign IN [campaigns] AND mql_at BETWEEN [start_date] AND [end_date]
```

**Displayed as:** Currency amount

---

#### **Cost Per SQL**
**Definition:** Average cost to acquire one SQL

**Calculation:**
```sql
SUM(campaign.spend) / COUNT(DISTINCT leads with sql_at)
WHERE acquisition_campaign IN [campaigns] AND sql_at BETWEEN [start_date] AND [end_date]
```

**Displayed as:** Currency amount

**Business logic:**
- Most important efficiency metric for B2B lead gen
- Benchmark: should be 1/3 to 1/5 of expected deal value

---

### 4.3 Velocity Metrics

#### **Days to MQL**
**Definition:** Average time from lead creation to MQL

**Calculation:**
```sql
AVG(DATEDIFF(mql_at, created_at))
WHERE mql_at IS NOT NULL AND mql_at BETWEEN [start_date] AND [end_date]
```

**Displayed as:** Number of days

---

#### **Days to SQL**
**Definition:** Average time from lead creation to SQL

**Calculation:**
```sql
AVG(DATEDIFF(sql_at, created_at))
WHERE sql_at IS NOT NULL AND sql_at BETWEEN [start_date] AND [end_date]
```

**Displayed as:** Number of days

---

#### **MQL-to-SQL Time**
**Definition:** Average time from MQL to SQL qualification

**Calculation:**
```sql
AVG(DATEDIFF(sql_at, mql_at))
WHERE sql_at IS NOT NULL AND mql_at IS NOT NULL
```

**Displayed as:** Number of days

---

### 4.4 Attribution Metrics

#### **Leads by Source**
**Definition:** Lead volume broken down by acquisition source

**Calculation:**
```sql
COUNT(DISTINCT lead_id) GROUP BY acquisition_source
WHERE created_at BETWEEN [start_date] AND [end_date]
```

**Displayed as:** Bar chart, pie chart

---

#### **SQLs by Source**
**Definition:** SQL volume broken down by acquisition source

**Calculation:**
```sql
COUNT(DISTINCT lead_id) GROUP BY acquisition_source
WHERE sql_at BETWEEN [start_date] AND [end_date]
```

**Displayed as:** Bar chart

**Business logic:**
- Use first-touch attribution (acquisition_source from lead_captured event)

---

#### **Cost Per SQL by Channel**
**Definition:** Efficiency comparison across channels

**Calculation:**
```sql
SUM(spend) / COUNT(DISTINCT SQLs) GROUP BY acquisition_source
```

**Displayed as:** Bar chart, table

---

### 4.5 Engagement Metrics

#### **Form Conversion Rate**
**Definition:** Percentage of sessions that result in form submission

**Calculation:**
```sql
(COUNT(DISTINCT sessions with form_submitted) / COUNT(DISTINCT session_id)) * 100
WHERE session_started BETWEEN [start_date] AND [end_date]
```

**Displayed as:** Percentage

---

#### **Demo Attendance Rate**
**Definition:** Percentage of scheduled demos that are attended

**Calculation:**
```sql
(COUNT(demos with attended_status = 'attended') / COUNT(demo_scheduled)) * 100
WHERE scheduled_for BETWEEN [start_date] AND [end_date]
```

**Displayed as:** Percentage

---

#### **Content Downloads Per Lead**
**Definition:** Average number of content pieces downloaded per lead

**Calculation:**
```sql
COUNT(content_downloaded) / COUNT(DISTINCT lead_id)
WHERE downloaded_at BETWEEN [start_date] AND [end_date]
```

**Displayed as:** Number

---

### 4.6 Pipeline Metrics (if tracking opportunities)

#### **Win Rate**
**Definition:** Percentage of opportunities that close as won

**Calculation:**
```sql
(COUNT(opportunity with status = 'won') / COUNT(opportunity)) * 100
WHERE closed_at BETWEEN [start_date] AND [end_date]
```

**Displayed as:** Percentage

---

#### **Average Deal Size**
**Definition:** Average value of closed-won deals

**Calculation:**
```sql
AVG(deal_value)
WHERE status = 'won' AND closed_at BETWEEN [start_date] AND [end_date]
```

**Displayed as:** Currency amount

---

#### **Sales Cycle Length**
**Definition:** Average days from opportunity creation to close

**Calculation:**
```sql
AVG(DATEDIFF(closed_at, created_at))
WHERE status IN ('won', 'lost') AND closed_at BETWEEN [start_date] AND [end_date]
```

**Displayed as:** Number of days

---

#### **Lead-to-Customer Conversion Rate**
**Definition:** Percentage of leads that become customers

**Calculation:**
```sql
(COUNT(DISTINCT leads with deal_won) / COUNT(DISTINCT lead_id)) * 100
WHERE lead created_at BETWEEN [start_date] AND [end_date]
```

**Displayed as:** Percentage

**Business logic:**
- Use cohort analysis (group by lead creation date)
- May take 60-180 days to mature depending on sales cycle

---

## 5. Data Flow & Attribution

### 5.1 Attribution Model

**Default: First-Touch Attribution**

- `acquisition_source` and `acquisition_campaign` captured on `lead_captured` event
- All downstream metrics (MQL, SQL, opportunities) inherit first-touch attribution
- Rationale: In B2B lead gen, first touch is typically most impactful for reporting

**Multi-Touch Attribution (Optional Advanced):**
- Track all touchpoints in lead journey
- Weight: First touch 40%, Middle touches 20%, Last touch 40%
- Requires Tier 3 implementation

---

### 5.2 Data Integration Points

#### **Marketing Automation Platform** (e.g., HubSpot, Marketo, Pardot)
- **Events:** `lead_captured`, `mql_qualified`, `lead_scored`, `email_opened`, `email_clicked`
- **Entities:** Lead, Campaign
- **Integration:** Webhook or API sync

#### **CRM** (e.g., Salesforce, HubSpot CRM, Pipedrive)
- **Events:** `sql_qualified`, `opportunity_created`, `deal_won`, `deal_lost`, `demo_attended`
- **Entities:** Lead, Opportunity
- **Integration:** API sync or webhook

#### **Website Analytics** (Segment, Google Tag Manager)
- **Events:** `session_started`, `page_viewed`, `form_submitted`
- **Entities:** Session
- **Integration:** JavaScript tracking

#### **Ad Platforms** (Google Ads, LinkedIn Ads, Facebook Ads)
- **Entities:** Campaign (spend data)
- **Integration:** API sync for spend and performance data

#### **Calendar Tools** (Calendly, Chili Piper)
- **Events:** `demo_scheduled`, `demo_attended`
- **Integration:** Webhook

#### **Webinar Platforms** (Zoom, Demio, WebinarJam)
- **Events:** `webinar_registered`, `webinar_attended`
- **Integration:** API or webhook

---

### 5.3 Data Transformation Requirements

#### **Lead Status Transitions**
Track state changes in `dim_leads` table:
```sql
-- Calculate current status based on most recent timestamp
CASE
  WHEN deal_won_at IS NOT NULL THEN 'won'
  WHEN deal_lost_at IS NOT NULL THEN 'lost'
  WHEN opportunity_created_at IS NOT NULL THEN 'opportunity'
  WHEN sql_at IS NOT NULL THEN 'sql'
  WHEN mql_at IS NOT NULL THEN 'mql'
  ELSE 'new'
END AS lead_status
```

#### **Lead Scoring Aggregation**
Maintain current lead score in `dim_leads`:
```sql
-- Sum all scoring events
SUM(score_change) AS current_lead_score
FROM lead_scored_events
GROUP BY lead_id
```

#### **Cost Attribution**
Join campaign spend to leads:
```sql
-- Allocate spend to leads by campaign
campaign.spend / COUNT(DISTINCT leads in campaign) AS allocated_cost_per_lead
```

---

## 6. Dashboard & Reporting Requirements

### 6.1 Core Dashboards

#### **Dashboard 1: Lead Generation Overview**
**Audience:** Marketing team, leadership

**Metrics:**
- Lead volume (line chart, by week)
- Leads by source (bar chart)
- Lead-to-MQL conversion rate (%)
- MQL-to-SQL conversion rate (%)
- SQL volume (number)

**Filters:** Date range, Source, Campaign

---

#### **Dashboard 2: Channel Performance**
**Audience:** Demand gen team

**Metrics:**
- Leads by channel (table)
- MQLs by channel (table)
- SQLs by channel (table)
- Cost per lead by channel (bar chart)
- Cost per SQL by channel (bar chart)
- Conversion rates by channel (table)

**Filters:** Date range, Channel, Campaign

---

#### **Dashboard 3: Funnel Velocity**
**Audience:** Marketing ops, sales ops

**Metrics:**
- Days to MQL (average)
- Days to SQL (average)
- MQL-to-SQL time (average)
- Funnel visualization (sankey diagram: Leads → MQL → SQL → Opportunities)

**Filters:** Date range, Source

---

#### **Dashboard 4: Campaign ROI** (requires Tier 3 opportunity events)
**Audience:** Leadership, demand gen

**Metrics:**
- Campaign spend (bar chart)
- SQLs by campaign (bar chart)
- Cost per SQL by campaign (table)
- Pipeline generated by campaign (currency)
- Won deals by campaign (currency)
- ROI by campaign (%) = (won deal value - spend) / spend * 100

**Filters:** Date range, Campaign, Channel

---

#### **Dashboard 5: Lead Quality Analysis**
**Audience:** Sales team, marketing team

**Metrics:**
- Lead score distribution (histogram)
- SQL rate by score bracket (bar chart)
- Win rate by lead source (table)
- Average deal size by source (table)
- Days to close by source (table)

**Filters:** Date range, Source, Lead score range

---

### 6.2 Report Cadence

**Weekly Reports:**
- Lead volume and sources
- SQL volume
- Cost per SQL

**Monthly Reports:**
- Full funnel metrics (Lead → MQL → SQL → Won)
- Channel performance comparison
- Campaign ROI
- Velocity metrics

**Quarterly Reports:**
- Cohort analysis (lead vintage performance over time)
- Attribution model comparison
- Win rate and deal size trends

---

## 7. Implementation Notes

### 7.1 Data Quality Checks

**Critical validations:**

1. **Lead volume matches CRM/MAP**
   ```sql
   -- Dashboard lead count should equal source system
   SELECT COUNT(DISTINCT lead_id) FROM leads
   WHERE created_at BETWEEN [start_date] AND [end_date]
   ```

2. **No orphaned leads** (leads without acquisition source)
   ```sql
   SELECT COUNT(*) FROM leads WHERE acquisition_source IS NULL
   -- Should be 0 or <1%
   ```

3. **MQL/SQL dates are logical**
   ```sql
   SELECT COUNT(*) FROM leads
   WHERE sql_at < mql_at OR mql_at < created_at
   -- Should be 0
   ```

4. **Spend reconciliation**
   ```sql
   -- Total spend in dashboard should match ad platform spend
   SELECT SUM(spend) FROM campaigns
   WHERE started_at BETWEEN [start_date] AND [end_date]
   ```

5. **Form submission = lead created**
   ```sql
   -- Every lead should have at least one form submission
   SELECT COUNT(*) FROM leads l
   LEFT JOIN form_submissions f ON l.lead_id = f.lead_id AND f.is_first_form = true
   WHERE f.form_id IS NULL
   -- Should be 0 (unless imported leads)
   ```

---

### 7.2 Common Pitfalls

❌ **Not capturing UTM parameters correctly**
- Capture at session start, not on every event
- Store UTM in session, join to lead via session_id

❌ **Incorrect attribution logic**
- Use first-touch attribution for B2B lead gen (not last-touch)
- Attribute to campaign/source from `lead_captured` event

❌ **Double-counting leads**
- Ensure lead_id is unique
- If CRM allows duplicate emails, dedupe before analytics

❌ **Not accounting for sales cycle length**
- Cohort lead-to-customer rates by lead creation date
- Don't expect recent leads to have high win rates yet

❌ **Ignoring form spam**
- Filter out invalid emails (@test.com, role accounts, competitors)
- Track spam rate separately

---

### 7.3 Technical Implementation Tips

**Lead identification:**
- Use Segment or similar CDP to track anonymous → identified journey
- Cookie-to-user_id mapping on first form submission

**CRM/MAP sync:**
- Use webhooks for real-time events (`mql_qualified`, `sql_qualified`)
- Use daily batch sync for entity updates (lead properties, scores)

**Ad platform spend:**
- Automate daily spend import via APIs
- Store at campaign-day granularity for accurate CPL calculation

**Demo tracking:**
- Integrate Calendly/Chili Piper webhooks for scheduling
- Require sales reps to log attendance in CRM for tracking

---

### 7.4 Privacy & Compliance

**GDPR/CCPA considerations:**
- Do not track identified leads without consent
- Provide opt-out mechanism for tracking cookies
- Anonymize PII in analytics warehouse (hash emails, redact IP addresses)
- Right to deletion: provide process to remove lead data

**Data retention:**
- Keep lead and event data for 24-36 months
- Archive older data to cold storage
- Delete on user request per privacy regulations

---

## 8. Glossary

**Lead:** A person or organization that has expressed interest (submitted form, attended event, etc.)

**MQL (Marketing Qualified Lead):** A lead that meets basic criteria (score threshold, ICP fit, engagement level) indicating they're worth sales follow-up

**SQL (Sales Qualified Lead):** A lead that sales team has vetted and accepted as worth active outreach

**ICP (Ideal Customer Profile):** The type of company/person that is the best fit for your product (e.g., "B2B SaaS companies with 50-200 employees")

**First-touch attribution:** Assigning credit to the first marketing interaction that created the lead

**Lead score:** A numerical value (0-100) representing lead quality and engagement level

**Conversion rate:** Percentage of leads moving from one stage to next (e.g., Lead → MQL)

**Cost per SQL:** Total marketing spend divided by number of SQLs generated

**Win rate:** Percentage of opportunities that close as won deals

**Sales cycle:** Time from first contact to closed deal

---

## 9. Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | [DATE] | [NAME] | Initial ontology created |

---

## Appendix: Sample Event Payload

### `lead_captured` event
```json
{
  "event": "lead_captured",
  "timestamp": "2025-01-15T10:35:22Z",
  "properties": {
    "lead_id": "lead_a3b4c5d6",
    "email": "john.doe@acmecorp.com",
    "company_name": "Acme Corp",
    "job_title": "Director of Marketing",
    "company_size": "51-200",
    "acquisition_source": "linkedin",
    "acquisition_campaign": "q1_demo_campaign",
    "utm_source": "linkedin",
    "utm_medium": "cpc",
    "utm_campaign": "q1_demo_campaign",
    "utm_content": "carousel_ad_v2",
    "landing_page": "/solutions/marketing-automation",
    "form_type": "demo_request",
    "lead_score": 0
  }
}
```

### `sql_qualified` event
```json
{
  "event": "sql_qualified",
  "timestamp": "2025-01-18T09:15:00Z",
  "properties": {
    "lead_id": "lead_a3b4c5d6",
    "lead_score": 75,
    "qualified_by": "sarah@company.com",
    "qualification_reason": "budget_confirmed, decision_maker, timeline_30_days",
    "qualified_at": "2025-01-18T09:15:00Z",
    "days_to_sql": 3,
    "assigned_to": "sarah@company.com"
  }
}
```
