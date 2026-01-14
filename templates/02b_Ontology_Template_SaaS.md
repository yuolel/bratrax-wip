# [CLIENT_NAME] Analytics Ontology

**Version:** 1.0
**Date:** [DATE]
**Business Model:** SaaS (Software as a Service)
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

**Revenue model:** [Freemium / Free trial / Paid only / Usage-based / Tiered plans]

**Pricing:**
- Free tier: [Features / Limitations]
- Paid tiers: [List tiers with pricing, e.g., Starter $29/mo, Pro $99/mo, Enterprise Custom]

**Average revenue per user (ARPU):** $[X]/month

**Average customer lifetime:** [X] months

**Primary growth goal:** [User acquisition / Activation / Retention / Expansion revenue / Reduce churn]

### 1.2 Key Business Questions
The dashboards must answer these questions:

1. [Question 1, e.g., "What's our activation rate and how quickly do users activate?"]
2. [Question 2, e.g., "Which features drive retention and which predict churn?"]
3. [Question 3, e.g., "What's our MRR growth rate and churn impact?"]
4. [Question 4, e.g., "Are free trial users converting to paid?"]
5. [Question 5, e.g., "Which acquisition channels bring highest LTV users?"]

---

## 2. Entity Definitions

Entities are the "nouns" of the business—the things we track.

### 2.1 Core Entities

#### **User**
A person who has signed up for the product.

| Property | Type | Definition | Example |
|----------|------|------------|---------|
| `user_id` | string | Unique identifier (primary key) | `usr_a3b4c5d6` |
| `email` | string | Email address | `user@example.com` |
| `created_at` | timestamp | When user signed up | `2025-01-15T10:30:00Z` |
| `activated_at` | timestamp | When user completed activation milestone | `2025-01-16T14:22:00Z` |
| `subscription_status` | string | Current subscription state | `trial`, `active`, `cancelled`, `churned` |
| `plan_tier` | string | Current pricing tier | `free`, `starter`, `pro`, `enterprise` |
| `mrr` | decimal | Monthly recurring revenue from this user | `99.00` |
| `acquisition_source` | string | First-touch marketing source | `google_ads`, `organic_search`, `referral` |
| `user_role` | string | Role in product | `admin`, `member`, `viewer` |

**Business logic:**
- `activated_at` is when user completes key activation milestone (e.g., completes onboarding, creates first project)
- `subscription_status = trial` during free trial period
- `subscription_status = active` for paying customers
- `subscription_status = cancelled` when user cancels but still has access until period ends
- `subscription_status = churned` when subscription period expires without renewal

---

#### **Account** (if B2B with team/workspace model)
An organization or workspace that contains multiple users.

| Property | Type | Definition | Example |
|----------|------|------------|---------|
| `account_id` | string | Unique identifier | `acc_xyz123` |
| `account_name` | string | Organization name | `Acme Corp` |
| `created_at` | timestamp | When account created | `2025-01-15T10:30:00Z` |
| `plan_tier` | string | Account's pricing tier | `team`, `business`, `enterprise` |
| `mrr` | decimal | Monthly recurring revenue from account | `499.00` |
| `seat_count` | integer | Number of users in account | `12` |
| `owner_user_id` | string | Primary account owner | `usr_a3b4c5d6` |

**Business logic:**
- For B2B products with team plans
- Account MRR is the sum of all seats or the flat subscription price
- Use this for team/enterprise SaaS; skip for individual B2C SaaS

---

#### **Subscription**
A billing relationship for a user or account.

| Property | Type | Definition | Example |
|----------|------|------------|---------|
| `subscription_id` | string | Unique identifier | `sub_999` |
| `user_id` | string | Associated user (or account_id for team plans) | `usr_a3b4c5d6` |
| `plan_name` | string | Plan name | `Pro Monthly` |
| `plan_tier` | string | Plan tier | `pro` |
| `billing_frequency` | string | Billing cycle | `monthly`, `annual` |
| `price` | decimal | Subscription price | `99.00` |
| `currency` | string | Currency code | `USD` |
| `status` | string | Subscription status | `trial`, `active`, `past_due`, `cancelled`, `expired` |
| `trial_start` | timestamp | Trial start date (if applicable) | `2025-01-15T10:30:00Z` |
| `trial_end` | timestamp | Trial end date | `2025-01-22T10:30:00Z` |
| `started_at` | timestamp | When subscription became active | `2025-01-22T10:30:00Z` |
| `current_period_start` | timestamp | Current billing period start | `2025-02-22T10:30:00Z` |
| `current_period_end` | timestamp | Current billing period end | `2025-03-22T10:30:00Z` |
| `cancelled_at` | timestamp | When user cancelled | `2025-03-01T15:00:00Z` |

**Business logic:**
- `status = trial` during free trial
- `status = active` when paid and current
- `status = past_due` when payment fails but retrying
- `status = cancelled` when cancelled but access remains until period end
- `status = expired` when subscription period ends without payment

---

#### **Session**
A period of activity in the app.

| Property | Type | Definition | Example |
|----------|------|------------|---------|
| `session_id` | string | Unique identifier | `sess_x7y8z9` |
| `user_id` | string | Associated user | `usr_a3b4c5d6` |
| `started_at` | timestamp | Session start time | `2025-01-15T10:30:00Z` |
| `ended_at` | timestamp | Session end time (or timeout) | `2025-01-15T10:45:00Z` |
| `duration_seconds` | integer | Session length | `900` |
| `utm_source` | string | Marketing source parameter | `google` |
| `utm_campaign` | string | Campaign identifier | `q1_product_launch` |
| `referrer` | string | Referring URL | `https://google.com/search` |
| `device_type` | string | Device category | `desktop`, `mobile`, `tablet` |

**Business logic:**
- Session timeout: 30 minutes of inactivity
- First session captures acquisition source
- Duration calculated from first to last event in session

---

#### **Feature_Usage**
Usage of specific product features.

| Property | Type | Definition | Example |
|----------|------|------------|---------|
| `usage_id` | string | Unique identifier | `usage_123` |
| `user_id` | string | User who used feature | `usr_a3b4c5d6` |
| `feature_name` | string | Feature used | `ad_saved`, `board_created`, `export_report` |
| `used_at` | timestamp | When feature was used | `2025-01-15T10:30:00Z` |
| `usage_count` | integer | Number of times used in session | `3` |

**Purpose:** Track which features drive engagement and retention

---

### 2.2 Entity Relationships

```
Account (1) ─────< Users (many)
  │
  └────< Subscription (1)

User (1) ────< Sessions (many)
  │
  ├────< Feature_Usage (many)
  └────< Subscription (1 or 0 for free users)

Subscription (1) ─────< Payment_Events (many)
```

---

## 3. Event Taxonomy

Events are the "verbs"—things that happen. Following the **entity_activity** naming convention.

### 3.1 Event Naming Rules
1. Format: `{entity}_{activity}`
2. All lowercase, underscores only
3. Past tense for activity (e.g., `created`, `activated`, `cancelled`)
4. Be specific (e.g., `user_onboarding_completed` not just `completed`)

### 3.2 Event Complexity Guide

Based on SaaS business complexity:
- **Simple B2C SaaS:** 12-15 events (individual users, simple feature set)
- **B2B with Teams:** 16-20 events (account management, team collaboration)
- **Freemium with Trials:** 18-22 events (trial → paid conversion, feature gating)
- **Usage-based Pricing:** 20-25 events (detailed usage tracking per feature)

**Reference:** See Event Storming Workshop Guide for how to determine the right event set.

---

### 3.3 Implementation Strategy

**Default approach: Progressive Implementation**

Events are organized into 3 tiers. **Implement progressively** (Tier 1 → validate → Tier 2 → validate → Tier 3 as needed) unless you have a specific reason to implement all at once.

**Why progressive?**
- Faster time to value (2 weeks vs 4+ weeks)
- Lower implementation risk (easier to debug)
- Validates business value before investing in advanced events
- Flexibility to adjust based on actual usage

**Timeline:**
- **Week 1:** Implement Tier 1 (5-6 events)
- **Week 2:** Launch initial dashboards, validate tracking
- **Week 3-4:** Add Tier 2 events (10-12 total) based on usage
- **Week 5+:** Add Tier 3 selectively as needed

**Exception - Implement all tiers at once only if:**
- Complex pricing model requiring detailed usage tracking from day 1
- Client is sophisticated and knows exactly which events they need
- Historical data for feature usage is critical (can't backfill later)

---

### 3.4 Core Events Catalog

Events are organized by implementation tier.

---

## **TIER 1: Critical Events (Implement First)**

These events are required to calculate core SaaS metrics (MRR, activation rate, churn). Must be implemented before dashboard launch.

**Target: 5-6 events**
**Timeline: Week 1 of implementation**

---

#### **User Lifecycle Events**

##### `user_created`
**When:** User completes account registration
**Why critical:** User acquisition tracking, activation funnel start

**Properties:**
| Property | Type | Required | Example |
|----------|------|----------|---------|
| `user_id` | string | Yes | `usr_a3b4c5d6` |
| `email` | string | Yes | `user@example.com` |
| `signup_source` | string | Yes | `homepage`, `pricing_page`, `referral` |
| `utm_source` | string | No | `google_ads` |
| `utm_medium` | string | No | `cpc` |
| `utm_campaign` | string | No | `q1_product_launch` |
| `user_role` | string | No | `admin`, `member` |

---

##### `user_activated`
**When:** User completes key activation milestone
**Why critical:** Activation rate tracking, predicts retention

**Define activation milestone based on product:**
- Example 1: User completes onboarding + creates first project
- Example 2: User invites team member + uses core feature
- Example 3: User completes profile + performs first search

**Properties:**
| Property | Type | Required | Example |
|----------|------|----------|---------|
| `user_id` | string | Yes | `usr_a3b4c5d6` |
| `activation_milestone` | string | Yes | `onboarding_completed`, `first_project_created` |
| `days_to_activate` | integer | Yes | `2` (days from signup to activation) |

---

#### **Subscription Events**

##### `subscription_trial_started` (if you offer trials)
**When:** User begins free trial
**Why critical:** Trial conversion funnel, trial-to-paid tracking

**Properties:**
| Property | Type | Required | Example |
|----------|------|----------|---------|
| `user_id` | string | Yes | `usr_a3b4c5d6` |
| `subscription_id` | string | Yes | `sub_999` |
| `plan_name` | string | Yes | `Pro - Trial` |
| `trial_duration_days` | integer | Yes | `14` |
| `trial_end_date` | timestamp | Yes | `2025-01-29T10:30:00Z` |

---

##### `subscription_created` ⭐ **MOST CRITICAL**
**When:** User becomes a paying customer (first payment)
**Why critical:** MRR tracking, revenue calculations, conversion tracking

**Properties:**
| Property | Type | Required | Example |
|----------|------|----------|---------|
| `user_id` | string | Yes | `usr_a3b4c5d6` |
| `subscription_id` | string | Yes | `sub_999` |
| `plan_name` | string | Yes | `Pro Monthly` |
| `plan_tier` | string | Yes | `pro` |
| `billing_frequency` | string | Yes | `monthly`, `annual` |
| `price` | decimal | Yes | `99.00` |
| `currency` | string | Yes | `USD` |
| `is_trial_conversion` | boolean | Yes | `true` (converted from trial) / `false` (direct purchase) |
| `payment_method` | string | Yes | `credit_card`, `paypal` |

---

##### `subscription_cancelled`
**When:** User cancels their subscription
**Why critical:** Churn tracking, retention analysis

**Properties:**
| Property | Type | Required | Example |
|----------|------|----------|---------|
| `user_id` | string | Yes | `usr_a3b4c5d6` |
| `subscription_id` | string | Yes | `sub_999` |
| `cancellation_reason` | string | No | `too_expensive`, `not_using_enough`, `missing_features`, `competitor` |
| `months_subscribed` | integer | Yes | `6` |
| `plan_tier` | string | Yes | `pro` |
| `churned_mrr` | decimal | Yes | `99.00` |

---

**End of Tier 1 (5-6 core events)**

**Next step:** Validate Tier 1 tracking, launch initial dashboards, then proceed to Tier 2.

---

## **TIER 2: Engagement & Feature Usage Events (Implement Second)**

These events provide product usage insights and activation/retention signals. Implement after Tier 1 is validated.

**Target: 5-7 events**
**Timeline: Week 3-4 of implementation**

**Before implementing Tier 2:**
- ✅ Tier 1 events validated and working
- ✅ Initial dashboards launched (MRR, activation, churn)
- ✅ MRR reconciliation passing (matches billing system ≤2%)
- ✅ Client has used dashboards for at least 1 week

---

#### **Product Engagement Events**

##### `user_onboarding_completed`
**When:** User finishes onboarding/tutorial
**Why matters:** Onboarding completion drives activation

**Properties:**
| Property | Type | Required | Example |
|----------|------|----------|---------|
| `user_id` | string | Yes | `usr_a3b4c5d6` |
| `onboarding_steps_completed` | integer | Yes | `5` |
| `onboarding_duration_minutes` | integer | Yes | `12` |

---

##### `feature_used` (Generic feature tracking)
**When:** User interacts with a key product feature
**Why matters:** Feature adoption, engagement patterns, retention signals

**Track your top 3-5 core features separately** (examples below)

**Properties:**
| Property | Type | Required | Example |
|----------|------|----------|---------|
| `user_id` | string | Yes | `usr_a3b4c5d6` |
| `session_id` | string | Yes | `sess_x7y8z9` |
| `feature_name` | string | Yes | `search_executed`, `ad_saved`, `report_generated` |
| `feature_category` | string | No | `core`, `premium`, `export` |

---

**Example SaaS-specific feature events (choose 3-5 that matter for YOUR product):**

##### `search_initiated` (if search is core feature)
**When:** User performs a search
**Why matters:** Core feature engagement, value realization

**Properties:**
| Property | Type | Required | Example |
|----------|------|----------|---------|
| `user_id` | string | Yes | `usr_a3b4c5d6` |
| `search_term` | string | Yes | `fitness supplements` |
| `search_results_count` | integer | Yes | `1523` |
| `filters_applied` | string | No | `category:health,date_range:30d` |

---

##### `item_saved` (or project_created, board_created, etc.)
**When:** User saves/creates primary content in your product
**Why matters:** Value creation, commitment signal

**Properties:**
| Property | Type | Required | Example |
|----------|------|----------|---------|
| `user_id` | string | Yes | `usr_a3b4c5d6` |
| `item_id` | string | Yes | `item_abc123` |
| `item_type` | string | Yes | `ad`, `project`, `board`, `document` |
| `item_name` | string | No | `Q1 Campaign Assets` |

---

##### `team_member_invited` (if collaboration feature exists)
**When:** User invites another person to their account
**Why matters:** Viral growth, account expansion, retention signal

**Properties:**
| Property | Type | Required | Example |
|----------|------|----------|---------|
| `user_id` | string | Yes | `usr_a3b4c5d6` (inviter) |
| `account_id` | string | No | `acc_xyz123` |
| `invited_email` | string | Yes | `teammate@example.com` |
| `role_assigned` | string | Yes | `admin`, `member`, `viewer` |

---

##### `export_generated` (if export/report feature exists)
**When:** User exports data or generates a report
**Why matters:** Power user behavior, value realization

**Properties:**
| Property | Type | Required | Example |
|----------|------|----------|---------|
| `user_id` | string | Yes | `usr_a3b4c5d6` |
| `export_type` | string | Yes | `csv`, `pdf`, `excel` |
| `export_category` | string | No | `report`, `data_export`, `analytics` |

---

#### **Subscription Management Events**

##### `subscription_renewed`
**When:** Subscription successfully renews (automatic payment)
**Why matters:** Retention confirmation, MRR stability

**Properties:**
| Property | Type | Required | Example |
|----------|------|----------|---------|
| `user_id` | string | Yes | `usr_a3b4c5d6` |
| `subscription_id` | string | Yes | `sub_999` |
| `plan_tier` | string | Yes | `pro` |
| `renewal_amount` | decimal | Yes | `99.00` |
| `months_retained` | integer | Yes | `7` (total months subscribed) |

---

##### `subscription_payment_failed`
**When:** Payment fails during renewal attempt
**Why matters:** Churn warning signal, recovery opportunity

**Properties:**
| Property | Type | Required | Example |
|----------|------|----------|---------|
| `user_id` | string | Yes | `usr_a3b4c5d6` |
| `subscription_id` | string | Yes | `sub_999` |
| `failure_reason` | string | No | `insufficient_funds`, `expired_card`, `fraud_detected` |
| `retry_count` | integer | Yes | `1` |

---

**End of Tier 2 (5-7 additional events) → Total: 10-13 events**

**Next step:** Review dashboard usage with client. Only add Tier 3 events if they request specific functionality.

---

## **TIER 3: Advanced & Optimization Events (Future Enhancement)**

These events provide deeper insights for optimization. **Implement selectively based on client requests**, not automatically.

**Target: 3-5 events**
**Timeline: Week 5+ or on-demand**

**Only implement Tier 3 events when:**
- ✅ Client specifically requests the functionality
- ✅ Tier 1 + 2 dashboards are being actively used
- ✅ Client has demonstrated they need this level of detail

**Common scenarios for Tier 3:**
- Client says: "We need to understand trial abandonment" → Add `subscription_trial_ended_no_conversion`
- Client says: "Need to track plan upgrades/downgrades" → Add plan change events
- Client says: "Support tickets predict churn" → Add `user_support_contacted`

---

#### **User Support & Feedback**

##### `user_support_contacted`
**When:** User submits a support request
**Why matters:** Dissatisfaction signal, potential churn predictor

**Properties:**
| Property | Type | Required | Example |
|----------|------|----------|---------|
| `user_id` | string | Yes | `usr_a3b4c5d6` |
| `ticket_id` | string | No | `ticket_999` |
| `issue_category` | string | No | `bug`, `feature_request`, `billing`, `how_to` |
| `priority` | string | No | `low`, `medium`, `high` |

---

##### `user_feedback_submitted`
**When:** User provides product feedback (NPS, survey, etc.)
**Why matters:** Product improvement signals, satisfaction tracking

**Properties:**
| Property | Type | Required | Example |
|----------|------|----------|---------|
| `user_id` | string | Yes | `usr_a3b4c5d6` |
| `feedback_type` | string | Yes | `nps`, `feature_request`, `bug_report` |
| `nps_score` | integer | No | `9` (0-10 scale) |
| `feedback_text` | string | No | `Would love to see X feature` |

---

#### **Advanced Subscription Events**

##### `subscription_upgraded`
**When:** User upgrades to higher plan tier
**Why matters:** Expansion MRR, product-market fit signal

**Properties:**
| Property | Type | Required | Example |
|----------|------|----------|---------|
| `user_id` | string | Yes | `usr_a3b4c5d6` |
| `subscription_id` | string | Yes | `sub_999` |
| `old_plan_tier` | string | Yes | `starter` |
| `new_plan_tier` | string | Yes | `pro` |
| `old_price` | decimal | Yes | `29.00` |
| `new_price` | decimal | Yes | `99.00` |
| `expansion_mrr` | decimal | Yes | `70.00` |

---

##### `subscription_downgraded`
**When:** User downgrades to lower plan tier
**Why matters:** Contraction MRR, churn warning signal

**Properties:**
| Property | Type | Required | Example |
|----------|------|----------|---------|
| `user_id` | string | Yes | `usr_a3b4c5d6` |
| `subscription_id` | string | Yes | `sub_999` |
| `old_plan_tier` | string | Yes | `pro` |
| `new_plan_tier` | string | Yes | `starter` |
| `contraction_mrr` | decimal | Yes | `-70.00` |

---

##### `subscription_trial_ended_no_conversion`
**When:** Trial ends without user converting to paid
**Why matters:** Trial conversion optimization

**Properties:**
| Property | Type | Required | Example |
|----------|------|----------|---------|
| `user_id` | string | Yes | `usr_a3b4c5d6` |
| `subscription_id` | string | Yes | `sub_999` |
| `trial_duration_days` | integer | Yes | `14` |
| `features_used_count` | integer | No | `3` |
| `reason_not_converted` | string | No | `price_too_high`, `missing_features`, `didnt_see_value` |

---

#### **Account Management** (B2B SaaS only)

##### `account_created`
**When:** New organizational account is created
**Why matters:** B2B acquisition tracking

**Properties:**
| Property | Type | Required | Example |
|----------|------|----------|---------|
| `account_id` | string | Yes | `acc_xyz123` |
| `account_name` | string | Yes | `Acme Corp` |
| `owner_user_id` | string | Yes | `usr_a3b4c5d6` |
| `plan_tier` | string | Yes | `team`, `business`, `enterprise` |

---

**End of Tier 3 (5 additional events) → Total: 15-18 events**

---

### 3.5 Event Reduction Summary

After event storming workshop, document your final event set here:

**Total events identified in brainstorming:** [X]
**Final core events (all tiers):** [Y]

**Implementation approach:** ☑ Progressive (recommended) / ☐ All at once

**Tier 1 (Critical - Week 1):** [N] events
- [List tier 1 events selected for this client]

**Tier 2 (Engagement - Week 3-4):** [N] events
- [List tier 2 events selected for this client]

**Tier 3 (Advanced - On-demand):** [N] events
- [List tier 3 events that may be added later]

**Total implemented at initial launch:** [Tier 1 only or Tier 1 + Tier 2] events

**Events NOT tracked** (and why):
- [Event name]: [Reason for exclusion]
- Example: `user_deleted` - Very rare event (<1% of users), not worth tracking
- Example: `feature_X_used` - Feature not yet launched, add when released

**Phase gates:**
- ☐ Tier 1 validated before starting Tier 2
- ☐ Client has used Tier 1 dashboards for 1+ week
- ☐ Tier 3 events only added on client request

---

## 4. Metric Definitions

Metrics are calculated values that answer business questions.

### 4.1 SaaS Financial Metrics

#### **Monthly Recurring Revenue (MRR)**
**Definition:** Total predictable monthly revenue from all active subscriptions

**Calculation:**
```sql
SUM(subscription.price / CASE
  WHEN billing_frequency = 'annual' THEN 12
  WHEN billing_frequency = 'quarterly' THEN 3
  ELSE 1
END)
WHERE subscription.status = 'active'
```

**Components:**
- New MRR: Revenue from new subscriptions this month
- Expansion MRR: Additional revenue from upgrades/upsells
- Contraction MRR: Lost revenue from downgrades
- Churned MRR: Lost revenue from cancellations

**Formula:** `MRR = Last Month MRR + New MRR + Expansion MRR - Contraction MRR - Churned MRR`

---

#### **Annual Recurring Revenue (ARR)**
**Definition:** Annualized MRR

**Calculation:**
```sql
MRR * 12
```

---

#### **Average Revenue Per User (ARPU)**
**Definition:** Average monthly revenue per paying customer

**Calculation:**
```sql
MRR / COUNT(DISTINCT users with active subscription)
```

---

### 4.2 SaaS Growth Metrics

#### **Activation Rate**
**Definition:** Percentage of signups who reach activation milestone

**Calculation:**
```sql
COUNT(DISTINCT users with user_activated event) / COUNT(DISTINCT users with user_created event)
```

**Time-bound:** Measure within first 7 days or 30 days of signup

**Target:** [X]% (industry benchmark: 20-40% for B2B SaaS)

---

#### **Trial Conversion Rate**
**Definition:** Percentage of trial users who become paying customers

**Calculation:**
```sql
COUNT(DISTINCT users with subscription_created where is_trial_conversion = true) /
COUNT(DISTINCT users with subscription_trial_started)
```

**Target:** [X]% (industry benchmark: 15-25%)

---

#### **Time to Activation**
**Definition:** Average days from signup to activation

**Calculation:**
```sql
AVG(days_to_activate) from user_activated events
```

**Target:** [X] days (faster is better)

---

### 4.3 SaaS Retention Metrics

#### **Churn Rate (Monthly)**
**Definition:** Percentage of customers who cancel each month

**Calculation:**
```sql
COUNT(DISTINCT users with subscription_cancelled in month) /
COUNT(DISTINCT users with active subscription at start of month)
```

**Target:** <5% monthly for healthy SaaS (varies by market)

---

#### **Revenue Churn Rate**
**Definition:** Percentage of MRR lost to churn each month

**Calculation:**
```sql
SUM(churned_mrr in month) / MRR at start of month
```

**Can be negative if expansion > churn (ideal state)**

---

#### **Net Revenue Retention (NRR)**
**Definition:** Revenue retention including expansion and contraction

**Calculation:**
```sql
(MRR at start + Expansion - Contraction - Churn) / MRR at start
```

**Interpretation:**
- NRR > 100% = Expansion offsets churn (excellent)
- NRR = 100% = Perfect retention
- NRR < 100% = Revenue declining from existing customers

**Target:** >100% for high-growth SaaS

---

#### **Customer Lifetime Value (LTV)**
**Definition:** Average total revenue from a customer over their lifetime

**Calculation:**
```sql
ARPU / Monthly Churn Rate
```

**Example:** If ARPU = $99 and monthly churn = 5%, then LTV = $99 / 0.05 = $1,980

**Cohort-based:** Calculate LTV by acquisition cohort for accuracy

---

### 4.4 SaaS Unit Economics

#### **Customer Acquisition Cost (CAC)**
**Definition:** Cost to acquire one new customer

**Calculation:**
```sql
(Sales & Marketing Spend) / New Customers Acquired
```

**Include:** Ad spend, sales salaries, marketing tools, agencies

**Target:** CAC < LTV / 3 (LTV:CAC ratio of 3:1 minimum)

---

#### **CAC Payback Period**
**Definition:** Months to recover CAC from customer revenue

**Calculation:**
```sql
CAC / ARPU
```

**Example:** If CAC = $300 and ARPU = $100, payback = 3 months

**Target:** <12 months

---

#### **LTV:CAC Ratio**
**Definition:** Relationship between customer value and acquisition cost

**Calculation:**
```sql
LTV / CAC
```

**Healthy ratio:** 3:1 or higher

---

### 4.5 Product Engagement Metrics

#### **Daily/Weekly/Monthly Active Users (DAU/WAU/MAU)**
**Definition:** Count of unique users active in time period

**Calculation:**
```sql
COUNT(DISTINCT user_id with any event in period)
```

**Stickiness:** DAU / MAU (higher = more engaged users)

---

#### **Feature Adoption Rate**
**Definition:** Percentage of users who use a specific feature

**Calculation:**
```sql
COUNT(DISTINCT users with feature_used event for feature_X) /
COUNT(DISTINCT active users)
```

---

## 5. Attribution Logic

### 5.1 Attribution Model
**Model:** First-touch (SaaS standard - credit goes to initial acquisition source)

**Why first-touch for SaaS:** Long consideration cycles mean first touch typically drives awareness and signup

### 5.2 Attribution Window
Not applicable for SaaS (track initial signup source indefinitely)

**Logic:**
```
acquisition_source = utm_source from first session
stored at user_created event
```

---

## 6. Data Sources & Integration

### 6.1 Source Systems

| Source | Data Type | Integration Method | Refresh Frequency |
|--------|-----------|-------------------|-------------------|
| [Application Database] | User data, subscriptions | Direct DB connection or API | Real-time / Hourly |
| [Stripe / Billing system] | Payment events, MRR | API / Webhook | Real-time |
| [Segment / Analytics] | User events | Event stream | Real-time |
| [Support tool (Zendesk, etc.)] | Support tickets | API | Daily |
| [Email tool (if applicable)] | Email engagement | API | Daily |

---

## 7. Production Table Structure

### 7.1 Core Tables

**Schema: `[CLIENT_NAME]_production`**

| Table Name | Description | Primary Key | Grain |
|------------|-------------|-------------|-------|
| `dim_users` | User dimension | `user_id` | One row per user |
| `dim_accounts` | Account/workspace dimension (B2B only) | `account_id` | One row per account |
| `fact_subscriptions` | Subscription history | `subscription_id` | One row per subscription |
| `fact_subscription_events` | Subscription state changes | `event_id` | One row per subscription event (created, renewed, cancelled) |
| `fact_sessions` | User sessions | `session_id` | One row per session |
| `fact_feature_usage` | Feature usage events | `usage_id` | One row per feature usage event |

### 7.2 Aggregated Tables (for dashboard performance)

| Table Name | Description | Grain |
|------------|-------------|-------|
| `agg_daily_mrr` | Daily MRR snapshot | One row per day |
| `agg_cohort_retention` | User cohort retention | One row per cohort per month |
| `agg_feature_adoption` | Feature adoption by user cohort | One row per feature per cohort |
| `agg_monthly_metrics` | Monthly SaaS metrics rollup | One row per month |

---

## 8. Dashboard Structure

### 8.1 Dashboard Views

Based on the business questions in Section 1.2, we'll create [X] dashboard views:

#### **Dashboard 1: MRR & Revenue**
**Purpose:** Financial health tracking

**Key metrics:**
- MRR (current, growth %)
- New MRR, Expansion MRR, Churned MRR
- ARR
- ARPU
- MRR by plan tier

**Filters:** Date range, plan tier

---

#### **Dashboard 2: Growth & Acquisition**
**Purpose:** User acquisition and activation

**Key metrics:**
- New signups (daily, weekly, monthly)
- Activation rate
- Time to activation
- Signups by source
- Trial conversion rate (if applicable)

**Filters:** Date range, acquisition source

---

#### **Dashboard 3: Retention & Churn**
**Purpose:** Customer retention and churn analysis

**Key metrics:**
- Monthly churn rate
- Revenue churn rate
- Net Revenue Retention (NRR)
- Cohort retention curves
- Churn reasons breakdown

**Filters:** Date range, plan tier, cohort

---

#### **Dashboard 4: Product Engagement**
**Purpose:** Feature usage and product health

**Key metrics:**
- DAU / WAU / MAU
- DAU/MAU stickiness
- Feature adoption rates
- Power user identification (top 10% by usage)

**Filters:** Date range, feature, user segment

---

### 8.2 Visualization Guidelines
- **MRR trends:** Line chart with components stacked (new, expansion, churn)
- **Cohort retention:** Heatmap or line chart
- **Feature adoption:** Bar chart or funnel
- **Churn reasons:** Pie chart or bar chart
- **Color palette:** [Define brand colors]
- **Date defaults:** Last 90 days with year-over-year comparison

---

## 9. Data Quality & Validation

### 9.1 Validation Rules

**MRR validation:**
- Dashboard MRR should match billing system (Stripe, etc.) within ±2%

**Subscription status validation:**
- Sum of active subscriptions should match billing system count

**User count validation:**
- Active users match application database count

---

## 10. Assumptions & Limitations

### 10.1 Known Limitations
- [e.g., "Feature usage before [date] not tracked, no historical data"]
- [e.g., "Trial users who don't activate are not included in activation rate"]

### 10.2 Out of Scope
- [e.g., "In-app messaging analytics"]
- [e.g., "A/B test tracking"]

---

## 11. Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| [DATE] | 1.0 | Initial ontology | [YOUR_NAME] |

---

## Appendix A: Glossary

**Activation:** User has completed key milestone that predicts retention (e.g., onboarding + first value moment)

**Churn:** When a paying customer cancels and subscription expires

**MRR:** Monthly Recurring Revenue - predictable monthly revenue from subscriptions

**NRR:** Net Revenue Retention - measures revenue retention including expansion and contraction

**ARPU:** Average Revenue Per User - average monthly revenue per paying customer

**Trial conversion:** When a trial user becomes a paying customer

---

*End of Ontology Document*
