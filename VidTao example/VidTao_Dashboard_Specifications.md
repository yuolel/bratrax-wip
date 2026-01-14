# VidTao Dashboard Specifications

**Version:** 1.0
**Date:** 2025-01-14
**Business Model:** SaaS - Ad Research Tool
**Prepared by:** Bratrax

---

## Document Purpose

This document defines the exact dashboards, metrics, and visualizations needed for VidTao's analytics platform. Each dashboard is designed to answer specific business questions and drive decision-making.

**Business Priorities:**
1. **Revenue expansion** through activation and acquisition
2. Understand **what makes users activate** (first value moment)
3. Determine if **free tier is too generous**
4. Identify **what features are sticky** (predict retention)
5. Understand **why new users drop off**

---

## Dashboard Overview

| Dashboard | Primary Audience | Key Question Answered | Update Frequency |
|-----------|-----------------|----------------------|------------------|
| **1. Activation & Engagement** | Product, Growth | What drives users to activate and stay engaged? | Daily |
| **2. Free Tier Analysis** | Product, Finance | Is our free tier too generous? When should we gate features? | Weekly |
| **3. Revenue & Conversion** | Finance, Leadership | What's our MRR, conversion rates, and churn? | Daily |
| **4. Feature Stickiness** | Product | Which features predict retention and drive upgrades? | Weekly |
| **5. Executive Overview** | Leadership | High-level business health at a glance | Daily |

---

## Dashboard 1: Activation & Engagement

**Purpose:** Understand the path from signup to "first value moment" and ongoing engagement

**Primary Audience:** Product team, Growth team

**Key Questions:**
- What % of new users activate (save or download their first ad)?
- How long does it take users to activate?
- What actions correlate with activation?
- Which user cohorts have highest activation rates?

---

### Metrics & Visualizations

#### **1.1 Activation Funnel (Bar Chart)**

**Metric:** User progression through activation stages

**Calculation:**
```sql
-- Cohort: Users created in last 30 days
WITH users AS (
  SELECT
    user_id,
    created_at,
    utm_source,
    utm_campaign
  FROM users
  WHERE created_at >= CURRENT_DATE - INTERVAL '30 days'
),
activation_events AS (
  SELECT
    user_id,
    MIN(timestamp) as first_value_moment
  FROM events
  WHERE event_name IN ('swipe_board_updated', 'ad_saved')
  GROUP BY user_id
)
SELECT
  COUNT(DISTINCT u.user_id) as total_signups,
  COUNT(DISTINCT CASE WHEN u.user_id IN (SELECT user_id FROM events WHERE event_name = 'user_onboarding_completed') THEN u.user_id END) as completed_onboarding,
  COUNT(DISTINCT CASE WHEN u.user_id IN (SELECT user_id FROM events WHERE event_name = 'search_initiated') THEN u.user_id END) as performed_search,
  COUNT(DISTINCT a.user_id) as activated_users
FROM users u
LEFT JOIN activation_events a ON u.user_id = a.user_id
```

**Visualization:**
```
Bar chart showing drop-off:
[===== 1000 users =====] Signed Up
[==== 850 users ====]    Completed Onboarding (85%)
[=== 600 users ===]      Performed Search (60%)
[== 400 users ==]        Activated (40%)
```

**Business Logic:**
- Activation = First `swipe_board_updated` (ad saved) OR `ad_saved` event
- Measure conversion rate at each step
- Identify biggest drop-off point

---

#### **1.2 Time to Activation (Histogram)**

**Metric:** Distribution of days from signup to first value moment

**Calculation:**
```sql
WITH activation AS (
  SELECT
    u.user_id,
    u.created_at as signup_date,
    MIN(e.timestamp) as activation_date,
    DATE_DIFF(MIN(e.timestamp), u.created_at, DAY) as days_to_activate
  FROM users u
  JOIN events e ON u.user_id = e.user_id
  WHERE e.event_name IN ('swipe_board_updated', 'ad_saved')
  AND u.created_at >= CURRENT_DATE - INTERVAL '90 days'
  GROUP BY u.user_id, u.created_at
)
SELECT
  days_to_activate,
  COUNT(*) as user_count
FROM activation
GROUP BY days_to_activate
ORDER BY days_to_activate
```

**Visualization:**
```
Histogram:
Users
 |
 |  ████
 |  ████ ███
 |  ████ ███ ██
 |  ████ ███ ██ █  █
 |_____________________
    0-1  2-3 4-7 8-14 15+ Days
```

**Insights to surface:**
- Median time to activation
- % who activate in first 24 hours
- % who activate in first 7 days
- Target: Get >50% to activate in first 24 hours

---

#### **1.3 Activation Rate by Source (Table)**

**Metric:** Conversion rate from signup to activation by acquisition channel

**Calculation:**
```sql
WITH user_activation AS (
  SELECT
    u.user_id,
    u.utm_source,
    u.utm_campaign,
    CASE
      WHEN EXISTS (
        SELECT 1 FROM events e
        WHERE e.user_id = u.user_id
        AND e.event_name IN ('swipe_board_updated', 'ad_saved')
      ) THEN 1
      ELSE 0
    END as is_activated
  FROM users u
  WHERE u.created_at >= CURRENT_DATE - INTERVAL '30 days'
)
SELECT
  utm_source,
  COUNT(*) as total_signups,
  SUM(is_activated) as activated_users,
  ROUND(AVG(is_activated) * 100, 1) as activation_rate_pct
FROM user_activation
GROUP BY utm_source
ORDER BY activation_rate_pct DESC
```

**Visualization:**
```
Table:
┌─────────────────┬────────────┬───────────────┬─────────────────┐
│ Source          │ Signups    │ Activated     │ Activation Rate │
├─────────────────┼────────────┼───────────────┼─────────────────┤
│ organic         │ 450        │ 225           │ 50.0%           │
│ youtube_ad      │ 320        │ 144           │ 45.0%           │
│ google_ads      │ 180        │ 63            │ 35.0%           │
│ facebook_ad     │ 50         │ 10            │ 20.0%           │
└─────────────────┴────────────┴───────────────┴─────────────────┘
```

**Action:** Focus acquisition spend on channels with highest activation rates

---

#### **1.4 Engagement Score Distribution (Histogram)**

**Metric:** User engagement in first 7 days (# of key actions)

**Calculation:**
```sql
WITH user_first_week AS (
  SELECT
    u.user_id,
    u.created_at,
    COUNT(CASE WHEN e.event_name = 'search_initiated' THEN 1 END) as searches,
    COUNT(CASE WHEN e.event_name = 'ad_details_viewed' THEN 1 END) as ad_views,
    COUNT(CASE WHEN e.event_name = 'swipe_board_updated' THEN 1 END) as ads_saved,
    COUNT(CASE WHEN e.event_name = 'ad_saved' THEN 1 END) as downloads
  FROM users u
  LEFT JOIN events e ON u.user_id = e.user_id
    AND e.timestamp BETWEEN u.created_at AND u.created_at + INTERVAL '7 days'
  WHERE u.created_at >= CURRENT_DATE - INTERVAL '30 days'
  GROUP BY u.user_id, u.created_at
)
SELECT
  user_id,
  (searches + ad_views + (ads_saved * 2) + (downloads * 3)) as engagement_score
FROM user_first_week
```

**Visualization:**
```
Histogram grouped by score buckets:
[0 actions]     ████████ 35% (Drop-offs)
[1-5 actions]   ████████████ 40% (Low engagement)
[6-15 actions]  ██████ 18% (Moderate engagement)
[16+ actions]   ███ 7% (High engagement - likely to convert)
```

**Weighting logic:**
- Search: 1 point
- Ad view: 1 point
- Ad saved: 2 points (stronger intent)
- Download: 3 points (strongest intent)

**Action:** Users with <5 points in first week = at-risk for churn

---

#### **1.5 Retention Cohorts (Heatmap)**

**Metric:** Weekly retention by signup cohort

**Calculation:**
```sql
WITH user_cohorts AS (
  SELECT
    user_id,
    DATE_TRUNC('week', created_at) as cohort_week
  FROM users
  WHERE created_at >= CURRENT_DATE - INTERVAL '90 days'
),
user_activity AS (
  SELECT
    e.user_id,
    DATE_TRUNC('week', e.timestamp) as activity_week
  FROM events e
  WHERE e.event_name IN ('search_initiated', 'ad_details_viewed', 'swipe_board_updated', 'ad_saved')
  GROUP BY e.user_id, DATE_TRUNC('week', e.timestamp)
)
SELECT
  c.cohort_week,
  DATE_DIFF(a.activity_week, c.cohort_week, WEEK) as weeks_since_signup,
  COUNT(DISTINCT a.user_id) as active_users,
  COUNT(DISTINCT c.user_id) as cohort_size,
  ROUND(COUNT(DISTINCT a.user_id) / COUNT(DISTINCT c.user_id) * 100, 1) as retention_pct
FROM user_cohorts c
LEFT JOIN user_activity a ON c.user_id = a.user_id
GROUP BY c.cohort_week, weeks_since_signup
ORDER BY c.cohort_week, weeks_since_signup
```

**Visualization:**
```
Heatmap (darker = higher retention):
              Week 0  Week 1  Week 2  Week 3  Week 4
Dec 18-24     ████    ███     ██      ██      █
Dec 25-31     ████    ███     ██      ██
Jan 1-7       ████    ███     ██
Jan 8-14      ████    ███
```

**Target:**
- Week 1 retention >60%
- Week 4 retention >40%

---

### Filters for Dashboard 1
- Date range (last 7/30/90 days)
- Acquisition source (organic, paid, referral)
- Campaign
- User subscription status (free, trial, paid)

---

## Dashboard 2: Free Tier Analysis

**Purpose:** Determine if free tier is too generous and when to gate features

**Primary Audience:** Product, Finance

**Key Questions:**
- How much are free users using the product?
- When do free users hit limits and what do they do?
- What features drive free-to-paid conversion?
- Is free tier cannibalizing paid conversions?

---

### Metrics & Visualizations

#### **2.1 Free User Engagement Distribution (Box Plot)**

**Metric:** Distribution of monthly activity by free users

**Calculation:**
```sql
WITH free_user_activity AS (
  SELECT
    u.user_id,
    COUNT(CASE WHEN e.event_name = 'search_initiated' THEN 1 END) as monthly_searches,
    COUNT(CASE WHEN e.event_name = 'ad_details_viewed' THEN 1 END) as monthly_ad_views,
    COUNT(CASE WHEN e.event_name = 'swipe_board_updated' THEN 1 END) as monthly_saves,
    COUNT(CASE WHEN e.event_name = 'ad_saved' THEN 1 END) as monthly_downloads
  FROM users u
  JOIN events e ON u.user_id = e.user_id
  WHERE u.subscription_status = 'free'
  AND e.timestamp >= CURRENT_DATE - INTERVAL '30 days'
  GROUP BY u.user_id
)
SELECT
  PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY monthly_searches) as searches_p25,
  PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY monthly_searches) as searches_median,
  PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY monthly_searches) as searches_p75,
  PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY monthly_searches) as searches_p90
FROM free_user_activity
```

**Visualization:**
```
Box plot showing distribution:
Searches:      [====|====|====]  (0, 5, 12, 25 at p25/p50/p75/p90)
Ad Views:      [========|====]   (0, 15, 40, 80)
Saves:         [==|==|==]        (0, 2, 6, 15)
Downloads:     [=|=|=]           (0, 0, 2, 8)
```

**Action:** If p75 of free users are staying well below limits, limits might be too high

---

#### **2.2 Power Users on Free Tier (Table)**

**Metric:** Free users with highest engagement (potential conversion targets)

**Calculation:**
```sql
WITH free_user_usage AS (
  SELECT
    u.user_id,
    u.email,
    u.created_at,
    DATE_DIFF(CURRENT_DATE, u.created_at, DAY) as days_on_free,
    COUNT(CASE WHEN e.event_name = 'search_initiated' THEN 1 END) as total_searches,
    COUNT(CASE WHEN e.event_name = 'swipe_board_updated' THEN 1 END) as total_saves,
    COUNT(CASE WHEN e.event_name = 'ad_saved' THEN 1 END) as total_downloads,
    MAX(e.timestamp) as last_activity
  FROM users u
  JOIN events e ON u.user_id = e.user_id
  WHERE u.subscription_status = 'free'
  AND e.timestamp >= CURRENT_DATE - INTERVAL '30 days'
  GROUP BY u.user_id, u.email, u.created_at
)
SELECT
  user_id,
  email,
  days_on_free,
  total_searches,
  total_saves,
  total_downloads,
  (total_searches + total_saves * 2 + total_downloads * 3) as engagement_score,
  DATE_DIFF(CURRENT_DATE, last_activity, DAY) as days_since_active
FROM free_user_usage
WHERE days_on_free >= 14 -- Been on free tier for 2+ weeks
ORDER BY engagement_score DESC
LIMIT 100
```

**Visualization:**
```
Table:
┌──────────────────────┬────────────┬──────────┬───────┬───────────┬─────────────────┐
│ Email                │ Days Free  │ Searches │ Saves │ Downloads │ Engagement Score│
├──────────────────────┼────────────┼──────────┼───────┼───────────┼─────────────────┤
│ john@agency.com      │ 45         │ 85       │ 28    │ 12        │ 177             │
│ sarah@brand.com      │ 30         │ 62       │ 22    │ 8         │ 130             │
│ mike@startup.io      │ 60         │ 55       │ 18    │ 6         │ 109             │
└──────────────────────┴────────────┴──────────┴───────┴───────────┴─────────────────┘
```

**Action:**
- Top 100 power users on free tier = immediate upgrade campaign targets
- If someone has >100 engagement score and still on free for 30+ days, free tier is likely too generous

---

#### **2.3 Free-to-Paid Conversion Trigger Analysis (Sankey Diagram)**

**Metric:** What feature usage predicts trial start?

**Calculation:**
```sql
WITH user_actions_before_trial AS (
  SELECT
    u.user_id,
    COUNT(CASE WHEN e.event_name = 'search_initiated' AND e.timestamp < t.trial_start THEN 1 END) as searches_before_trial,
    COUNT(CASE WHEN e.event_name = 'swipe_board_updated' AND e.timestamp < t.trial_start THEN 1 END) as saves_before_trial,
    COUNT(CASE WHEN e.event_name = 'ad_saved' AND e.timestamp < t.trial_start THEN 1 END) as downloads_before_trial,
    COUNT(CASE WHEN e.event_name = 'training_viewed' AND e.timestamp < t.trial_start THEN 1 END) as training_views
  FROM users u
  JOIN (
    SELECT user_id, MIN(timestamp) as trial_start
    FROM events
    WHERE event_name = 'subscription_trial_started'
    GROUP BY user_id
  ) t ON u.user_id = t.user_id
  LEFT JOIN events e ON u.user_id = e.user_id
  WHERE u.created_at >= CURRENT_DATE - INTERVAL '90 days'
  GROUP BY u.user_id
)
SELECT
  CASE
    WHEN searches_before_trial >= 10 THEN 'High Search (10+)'
    WHEN searches_before_trial >= 5 THEN 'Medium Search (5-9)'
    ELSE 'Low Search (0-4)'
  END as search_usage,
  CASE
    WHEN saves_before_trial >= 5 THEN 'High Saves (5+)'
    WHEN saves_before_trial >= 2 THEN 'Medium Saves (2-4)'
    ELSE 'Low Saves (0-1)'
  END as save_usage,
  COUNT(*) as users_converted
FROM user_actions_before_trial
GROUP BY search_usage, save_usage
ORDER BY users_converted DESC
```

**Visualization:**
```
Sankey/Flow diagram:
Free Users (1000)
    ├─ High Search (10+) ──────┬─→ Started Trial (450)
    │                           │
    ├─ Medium Search (5-9) ─────┤
    │                           │
    └─ Low Search (0-4) ────────┴─→ Stayed Free (550)

Among trial starters:
    ├─ High Saves (5+) ────────→ 65% start trial
    ├─ Medium Saves (2-4) ─────→ 35% start trial
    └─ Low Saves (0-1) ────────→ 15% start trial
```

**Insight:** If users with "Low Search + Low Saves" rarely convert, those are candidates for stricter limits

---

#### **2.4 Free Tier Limits Hit Rate (Line Chart)**

**Metric:** % of free users hitting usage limits over time

**Calculation:**
```sql
-- Assumes free tier limits: 10 searches/month, 5 saves/month, 2 downloads/month
WITH monthly_free_usage AS (
  SELECT
    u.user_id,
    DATE_TRUNC('month', e.timestamp) as usage_month,
    COUNT(CASE WHEN e.event_name = 'search_initiated' THEN 1 END) as monthly_searches,
    COUNT(CASE WHEN e.event_name = 'swipe_board_updated' THEN 1 END) as monthly_saves,
    COUNT(CASE WHEN e.event_name = 'ad_saved' THEN 1 END) as monthly_downloads
  FROM users u
  JOIN events e ON u.user_id = e.user_id
  WHERE u.subscription_status = 'free'
  AND e.timestamp >= CURRENT_DATE - INTERVAL '6 months'
  GROUP BY u.user_id, DATE_TRUNC('month', e.timestamp)
)
SELECT
  usage_month,
  COUNT(*) as total_free_users,
  COUNT(CASE WHEN monthly_searches >= 10 THEN 1 END) as hit_search_limit,
  COUNT(CASE WHEN monthly_saves >= 5 THEN 1 END) as hit_save_limit,
  COUNT(CASE WHEN monthly_downloads >= 2 THEN 1 END) as hit_download_limit,
  ROUND(COUNT(CASE WHEN monthly_searches >= 10 THEN 1 END) / COUNT(*) * 100, 1) as pct_hit_search_limit
FROM monthly_free_usage
GROUP BY usage_month
ORDER BY usage_month
```

**Visualization:**
```
Line chart over 6 months:
% Users Hitting Limit
  |
40|                               ╱─ Search limit
  |                         ╱───╱
30|                   ╱───╱
  |             ╱───╱
20|       ╱───╱        ╱─────── Save limit
  | ╱───╱        ╱───╱
10|         ╱───╱           ──── Download limit
  |_____________________________________________
   Aug  Sep  Oct  Nov  Dec  Jan
```

**Action:**
- If <20% of free users hit limits, limits are too high
- If >50% hit limits, consider if that's driving conversions or frustration

---

#### **2.5 Free User Lifetime Value (LTV) Projection (KPI Card)**

**Metric:** Estimated revenue loss from free tier (if limits were tighter)

**Calculation:**
```sql
WITH free_power_users AS (
  SELECT
    u.user_id,
    COUNT(CASE WHEN e.event_name IN ('search_initiated', 'swipe_board_updated', 'ad_saved') THEN 1 END) as total_actions
  FROM users u
  JOIN events e ON u.user_id = e.user_id
  WHERE u.subscription_status = 'free'
  AND e.timestamp >= CURRENT_DATE - INTERVAL '30 days'
  GROUP BY u.user_id
  HAVING COUNT(CASE WHEN e.event_name IN ('search_initiated', 'swipe_board_updated', 'ad_saved') THEN 1 END) >= 20
)
SELECT
  COUNT(*) as high_engagement_free_users,
  COUNT(*) * 87 as potential_monthly_revenue, -- If 100% converted at $87/mo
  COUNT(*) * 87 * 0.25 as realistic_revenue_at_25pct_conversion -- Assume 25% would convert if forced
FROM free_power_users
```

**Visualization:**
```
KPI Cards:
┌────────────────────────────────┐  ┌────────────────────────────────┐
│ High-Engagement Free Users     │  │ Potential Monthly Revenue      │
│ 347 users                      │  │ $7,540 (if 25% converted)      │
│ ↑ 12% vs last month            │  │                                │
└────────────────────────────────┘  └────────────────────────────────┘
```

**Action:** If potential revenue >$5k/month, consider tightening limits

---

### Filters for Dashboard 2
- Date range
- Days on free tier (0-7, 8-30, 31-90, 90+)
- Engagement level (low/medium/high)

---

## Dashboard 3: Revenue & Conversion

**Purpose:** Track MRR, churn, and conversion funnel health

**Primary Audience:** Finance, Leadership

**Key Questions:**
- What's our MRR and how is it trending?
- What's our free → trial → paid conversion rate?
- What's our churn rate and why are users churning?
- What's our revenue by acquisition channel?

---

### Metrics & Visualizations

#### **3.1 MRR Trend (Line Chart)**

**Metric:** Monthly Recurring Revenue over time

**Calculation:**
```sql
WITH daily_mrr AS (
  SELECT
    DATE(d.date) as date,
    SUM(
      CASE
        WHEN s.billing_frequency = 'yearly' THEN s.amount / 12
        WHEN s.billing_frequency = 'monthly' THEN s.amount
        ELSE 0
      END
    ) as mrr
  FROM (
    SELECT GENERATE_DATE_ARRAY(CURRENT_DATE - INTERVAL '12 months', CURRENT_DATE) as dates
  ) date_array, UNNEST(dates) as d(date)
  JOIN subscriptions s
    ON d.date BETWEEN DATE(s.created_at) AND COALESCE(DATE(s.canceled_at), CURRENT_DATE)
  WHERE s.status IN ('active', 'trialing')
  GROUP BY d.date
)
SELECT
  DATE_TRUNC('month', date) as month,
  AVG(mrr) as avg_monthly_mrr
FROM daily_mrr
GROUP BY month
ORDER BY month
```

**Visualization:**
```
Line chart:
MRR ($)
   |
30k|                               ╱────
   |                         ╱────╱
25k|                   ╱────╱
   |             ╱────╱
20k|       ╱────╱
   | ╱────╱
15k|________________________________
    Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec Jan
```

**Additional metrics to display:**
- Current MRR: $28,450
- MoM growth: +8.2%
- New MRR (from new subscriptions): +$3,200
- Churned MRR: -$1,100
- Net New MRR: +$2,100

---

#### **3.2 Conversion Funnel (Sankey Diagram)**

**Metric:** User journey from signup → trial → paid

**Calculation:**
```sql
WITH user_stages AS (
  SELECT
    u.user_id,
    u.created_at,
    MIN(CASE WHEN e.event_name = 'subscription_trial_started' THEN e.timestamp END) as trial_started_at,
    MIN(CASE WHEN e.event_name = 'subscription_created' THEN e.timestamp END) as paid_started_at
  FROM users u
  LEFT JOIN events e ON u.user_id = e.user_id
  WHERE u.created_at >= CURRENT_DATE - INTERVAL '90 days'
  GROUP BY u.user_id, u.created_at
)
SELECT
  COUNT(*) as total_signups,
  COUNT(CASE WHEN trial_started_at IS NOT NULL THEN 1 END) as started_trial,
  COUNT(CASE WHEN paid_started_at IS NOT NULL THEN 1 END) as converted_to_paid,
  ROUND(COUNT(CASE WHEN trial_started_at IS NOT NULL THEN 1 END) / COUNT(*) * 100, 1) as free_to_trial_rate,
  ROUND(COUNT(CASE WHEN paid_started_at IS NOT NULL THEN 1 END) / COUNT(CASE WHEN trial_started_at IS NOT NULL THEN 1 END) * 100, 1) as trial_to_paid_rate,
  ROUND(COUNT(CASE WHEN paid_started_at IS NOT NULL THEN 1 END) / COUNT(*) * 100, 1) as overall_conversion_rate
FROM user_stages
```

**Visualization:**
```
Sankey Diagram:
                    ┌─→ Started Trial (320) ──→ Converted to Paid (96)
Signed Up (1000) ───┤                              (30% trial-to-paid)
                    └─→ Stayed Free (680)
                        (32% free-to-trial rate)

Overall conversion: 9.6% (signup to paid)
```

**Benchmarks:**
- Free-to-trial: Target >30%
- Trial-to-paid: Target >25%
- Overall: Target >8%

---

#### **3.3 Churn Analysis (Waterfall Chart)**

**Metric:** Monthly subscription changes

**Calculation:**
```sql
WITH monthly_changes AS (
  SELECT
    DATE_TRUNC('month', e.timestamp) as month,
    COUNT(CASE WHEN e.event_name = 'subscription_created' THEN 1 END) as new_subscriptions,
    COUNT(CASE WHEN e.event_name = 'subscription_cancelled' THEN 1 END) as cancellations,
    COUNT(CASE WHEN e.event_name = 'subscription_renewed' THEN 1 END) as renewals
  FROM events e
  WHERE e.event_name IN ('subscription_created', 'subscription_cancelled', 'subscription_renewed')
  AND e.timestamp >= CURRENT_DATE - INTERVAL '6 months'
  GROUP BY month
)
SELECT
  month,
  new_subscriptions,
  cancellations,
  (new_subscriptions - cancellations) as net_change
FROM monthly_changes
ORDER BY month
```

**Visualization:**
```
Waterfall chart:
Subscribers
   |
350|      ████        ████
   |      ████   ████ ████        ████
300|████  ████   ████ ████   ████ ████
   |████  ████   ████ ████   ████ ████
250|████  ████   ████ ████   ████ ████
   |_____________________________________
    Aug   Sep    Oct   Nov   Dec   Jan
   (300) (+45)  (+30) (-10) (+25) (+50)
```

---

#### **3.4 Churn Reasons (Pie Chart)**

**Metric:** Why users are canceling

**Calculation:**
```sql
SELECT
  cancel_reason,
  COUNT(*) as cancellations,
  ROUND(COUNT(*) / SUM(COUNT(*)) OVER () * 100, 1) as pct_of_total
FROM events
WHERE event_name = 'subscription_cancelled'
AND timestamp >= CURRENT_DATE - INTERVAL '90 days'
GROUP BY cancel_reason
ORDER BY cancellations DESC
```

**Visualization:**
```
Pie chart:
┌─────────────────────────────┐
│ Too expensive: 35%          │
│ Not using enough: 28%       │
│ Missing features: 18%       │
│ Found alternative: 12%      │
│ Other: 7%                   │
└─────────────────────────────┘
```

**Action:** Address top 2 churn reasons to reduce churn by ~60%

---

#### **3.5 Revenue by Channel (Stacked Bar Chart)**

**Metric:** MRR attributed to acquisition source

**Calculation:**
```sql
SELECT
  u.utm_source,
  SUM(
    CASE
      WHEN s.billing_frequency = 'yearly' THEN s.amount / 12
      WHEN s.billing_frequency = 'monthly' THEN s.amount
      ELSE 0
    END
  ) as mrr
FROM users u
JOIN subscriptions s ON u.user_id = s.user_id
WHERE s.status = 'active'
GROUP BY u.utm_source
ORDER BY mrr DESC
```

**Visualization:**
```
Stacked bar chart (by month):
MRR ($)
   |
30k|████████████████████████████
   |████████████████████████████
25k|████████████████████████████
   |████ Organic
20k|████ YouTube Ads
   |████ Google Ads
15k|████ Other
   |_______________________________
    Aug Sep Oct Nov Dec Jan
```

---

#### **3.6 Customer Lifetime Value (LTV) (KPI Cards)**

**Metric:** Average revenue per customer over lifetime

**Calculation:**
```sql
WITH customer_ltv AS (
  SELECT
    u.user_id,
    SUM(
      CASE
        WHEN e.event_name = 'subscription_created' THEN e.amount
        WHEN e.event_name = 'subscription_renewed' THEN e.amount
        ELSE 0
      END
    ) as total_revenue,
    DATE_DIFF(
      COALESCE(MAX(CASE WHEN e.event_name = 'subscription_cancelled' THEN e.timestamp END), CURRENT_TIMESTAMP),
      MIN(CASE WHEN e.event_name = 'subscription_created' THEN e.timestamp END),
      MONTH
    ) as lifetime_months
  FROM users u
  JOIN events e ON u.user_id = e.user_id
  WHERE e.event_name IN ('subscription_created', 'subscription_renewed', 'subscription_cancelled')
  GROUP BY u.user_id
)
SELECT
  AVG(total_revenue) as avg_ltv,
  AVG(lifetime_months) as avg_lifetime_months,
  PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY total_revenue) as median_ltv
FROM customer_ltv
WHERE lifetime_months >= 3 -- Only customers with 3+ months history
```

**Visualization:**
```
KPI Cards:
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│ Average LTV      │  │ Median LTV       │  │ Avg Lifetime     │
│ $487             │  │ $348             │  │ 8.2 months       │
└──────────────────┘  └──────────────────┘  └──────────────────┘
```

---

### Filters for Dashboard 3
- Date range
- Acquisition source
- Plan type (monthly vs yearly)
- Cohort (by signup month)

---

## Dashboard 4: Feature Stickiness

**Purpose:** Identify which features predict retention and drive upgrades

**Primary Audience:** Product team

**Key Questions:**
- Which features do retained users use most?
- Which features are underutilized?
- What feature usage predicts churn?
- What features drive free → paid conversion?

---

### Metrics & Visualizations

#### **4.1 Feature Usage by User Segment (Heatmap)**

**Metric:** Average monthly usage of each feature by user type

**Calculation:**
```sql
WITH user_segments AS (
  SELECT
    u.user_id,
    CASE
      WHEN s.status = 'active' AND s.billing_frequency = 'yearly' THEN 'Paid - Annual'
      WHEN s.status = 'active' AND s.billing_frequency = 'monthly' THEN 'Paid - Monthly'
      WHEN s.status = 'trialing' THEN 'Trial'
      ELSE 'Free'
    END as user_segment
  FROM users u
  LEFT JOIN subscriptions s ON u.user_id = s.user_id
),
feature_usage AS (
  SELECT
    us.user_segment,
    COUNT(CASE WHEN e.event_name = 'search_initiated' THEN 1 END) / COUNT(DISTINCT e.user_id) as avg_searches,
    COUNT(CASE WHEN e.event_name = 'search_refined' THEN 1 END) / COUNT(DISTINCT e.user_id) as avg_refined_searches,
    COUNT(CASE WHEN e.event_name = 'ad_details_viewed' THEN 1 END) / COUNT(DISTINCT e.user_id) as avg_ad_views,
    COUNT(CASE WHEN e.event_name = 'swipe_board_created' THEN 1 END) / COUNT(DISTINCT e.user_id) as avg_boards_created,
    COUNT(CASE WHEN e.event_name = 'swipe_board_updated' THEN 1 END) / COUNT(DISTINCT e.user_id) as avg_ads_saved,
    COUNT(CASE WHEN e.event_name = 'ad_saved' THEN 1 END) / COUNT(DISTINCT e.user_id) as avg_downloads,
    COUNT(CASE WHEN e.event_name = 'training_viewed' THEN 1 END) / COUNT(DISTINCT e.user_id) as avg_training_views
  FROM user_segments us
  JOIN events e ON us.user_id = e.user_id
  WHERE e.timestamp >= CURRENT_DATE - INTERVAL '30 days'
  GROUP BY us.user_segment
)
SELECT * FROM feature_usage
ORDER BY user_segment
```

**Visualization:**
```
Heatmap (darker = higher usage):
                    Searches  Refine  Ad Views  Boards  Saves  Downloads  Training
Free              │  ██       █       ███       █       ██     █          █
Trial             │  ████     ██      █████     ██      ████   ██         ██
Paid - Monthly    │  ██████   ███     ███████   ███     ██████ ████       ███
Paid - Annual     │  ████████ █████   █████████ █████   ██████ ██████     ████

Scale: █ = 0-5, ██ = 6-15, ███ = 16-30, ████ = 31-50, ██████ = 51+
```

**Insights:**
- Features used MORE by paid users = value drivers (focus here)
- Features used LESS by paid vs free = not driving conversions (deprioritize)
- Huge gaps = feature education opportunity

---

#### **4.2 Feature Adoption Rate (Funnel)**

**Metric:** % of users who have EVER used each feature

**Calculation:**
```sql
WITH total_users AS (
  SELECT COUNT(DISTINCT user_id) as total
  FROM users
  WHERE created_at >= CURRENT_DATE - INTERVAL '90 days'
)
SELECT
  COUNT(DISTINCT CASE WHEN e.event_name = 'search_initiated' THEN e.user_id END) / t.total * 100 as pct_used_search,
  COUNT(DISTINCT CASE WHEN e.event_name = 'search_refined' THEN e.user_id END) / t.total * 100 as pct_used_refine,
  COUNT(DISTINCT CASE WHEN e.event_name = 'swipe_board_created' THEN e.user_id END) / t.total * 100 as pct_created_board,
  COUNT(DISTINCT CASE WHEN e.event_name = 'swipe_board_updated' THEN e.user_id END) / t.total * 100 as pct_saved_ad,
  COUNT(DISTINCT CASE WHEN e.event_name = 'ad_saved' THEN e.user_id END) / t.total * 100 as pct_downloaded,
  COUNT(DISTINCT CASE WHEN e.event_name = 'training_viewed' THEN e.user_id END) / t.total * 100 as pct_viewed_training
FROM events e, total_users t
WHERE e.timestamp >= CURRENT_DATE - INTERVAL '90 days'
```

**Visualization:**
```
Horizontal bar chart:
Used Search          ████████████████████ 82%
Viewed Ads           ███████████████ 68%
Saved Ads            ██████████ 45%
Created Board        ████████ 38%
Used Filters/Refine  ██████ 28%
Downloaded Assets    ████ 18%
Viewed Training      ███ 12%
```

**Action:** Features with <30% adoption need better onboarding or are not valuable

---

#### **4.3 Retention by Feature Usage (Grouped Bar Chart)**

**Metric:** Week 4 retention rate by whether user used feature

**Calculation:**
```sql
WITH user_cohorts AS (
  SELECT
    u.user_id,
    DATE_TRUNC('week', u.created_at) as cohort_week,
    EXISTS(SELECT 1 FROM events WHERE user_id = u.user_id AND event_name = 'swipe_board_updated') as used_save,
    EXISTS(SELECT 1 FROM events WHERE user_id = u.user_id AND event_name = 'ad_saved') as used_download,
    EXISTS(SELECT 1 FROM events WHERE user_id = u.user_id AND event_name = 'search_refined') as used_refine,
    EXISTS(SELECT 1 FROM events WHERE user_id = u.user_id AND event_name = 'training_viewed') as used_training
  FROM users u
  WHERE u.created_at >= CURRENT_DATE - INTERVAL '8 weeks'
  AND u.created_at < CURRENT_DATE - INTERVAL '4 weeks' -- Only cohorts at least 4 weeks old
),
week4_activity AS (
  SELECT
    e.user_id
  FROM events e
  WHERE e.timestamp BETWEEN
    (SELECT MIN(created_at) + INTERVAL '21 days' FROM users WHERE user_id = e.user_id)
    AND
    (SELECT MIN(created_at) + INTERVAL '28 days' FROM users WHERE user_id = e.user_id)
  GROUP BY e.user_id
)
SELECT
  'Used Save Feature' as feature,
  COUNT(CASE WHEN uc.used_save = true THEN 1 END) as users_used,
  COUNT(CASE WHEN uc.used_save = true AND w4.user_id IS NOT NULL THEN 1 END) as retained_week4,
  ROUND(COUNT(CASE WHEN uc.used_save = true AND w4.user_id IS NOT NULL THEN 1 END) / COUNT(CASE WHEN uc.used_save = true THEN 1 END) * 100, 1) as retention_rate
FROM user_cohorts uc
LEFT JOIN week4_activity w4 ON uc.user_id = w4.user_id
WHERE uc.used_save = true
UNION ALL
SELECT
  'Did NOT Use Save' as feature,
  COUNT(CASE WHEN uc.used_save = false THEN 1 END),
  COUNT(CASE WHEN uc.used_save = false AND w4.user_id IS NOT NULL THEN 1 END),
  ROUND(COUNT(CASE WHEN uc.used_save = false AND w4.user_id IS NOT NULL THEN 1 END) / COUNT(CASE WHEN uc.used_save = false THEN 1 END) * 100, 1)
FROM user_cohorts uc
LEFT JOIN week4_activity w4 ON uc.user_id = w4.user_id
WHERE uc.used_save = false
```

**Visualization:**
```
Grouped bar chart:
Week 4 Retention
  |
70|     ████
  |     ████
60|     ████     ████
  |     ████     ████     ████
50|     ████     ████     ████
  |     ████     ████     ████     ████
40|     ████     ████     ████     ████
  |_______________________________________
       Save     Download  Refine   Training
       Feature  Feature   Feature  Feature

      Used Feature: ████ 65%
      Did NOT Use:  ░░░░ 38%
```

**Insight:** Features with biggest retention gap = most critical for stickiness

---

#### **4.4 Feature Correlation Matrix (Heatmap)**

**Metric:** Which features are used together?

**Calculation:**
```sql
WITH user_feature_usage AS (
  SELECT
    user_id,
    MAX(CASE WHEN event_name = 'search_refined' THEN 1 ELSE 0 END) as used_refine,
    MAX(CASE WHEN event_name = 'swipe_board_updated' THEN 1 ELSE 0 END) as used_save,
    MAX(CASE WHEN event_name = 'ad_saved' THEN 1 ELSE 0 END) as used_download,
    MAX(CASE WHEN event_name = 'training_viewed' THEN 1 ELSE 0 END) as used_training
  FROM events
  WHERE timestamp >= CURRENT_DATE - INTERVAL '30 days'
  GROUP BY user_id
)
SELECT
  CORR(used_refine, used_save) as refine_save_corr,
  CORR(used_refine, used_download) as refine_download_corr,
  CORR(used_save, used_download) as save_download_corr,
  CORR(used_training, used_save) as training_save_corr
FROM user_feature_usage
```

**Visualization:**
```
Correlation matrix (1.0 = perfect correlation):
              Refine  Save   Download  Training
Refine         1.00   0.72   0.58      0.45
Save           0.72   1.00   0.85      0.52
Download       0.58   0.85   1.00      0.38
Training       0.45   0.52   0.38      1.00

High correlation (>0.7): Users who refine searches also save ads frequently
                         Users who save ads also download assets
Low correlation (<0.4):  Training is independent (not blocking other features)
```

**Action:** Features with low correlation = potential to drive adoption of other features

---

#### **4.5 Power User Feature Usage (Bar Chart)**

**Metric:** What do your most retained users do differently?

**Calculation:**
```sql
-- Define "power users" as users active 4+ weeks in a row
WITH power_users AS (
  SELECT DISTINCT e.user_id
  FROM events e
  WHERE e.timestamp >= CURRENT_DATE - INTERVAL '30 days'
  GROUP BY e.user_id, DATE_TRUNC('week', e.timestamp)
  HAVING COUNT(DISTINCT DATE_TRUNC('week', e.timestamp)) >= 4
),
feature_comparison AS (
  SELECT
    'Power Users' as user_type,
    COUNT(CASE WHEN e.event_name = 'search_refined' THEN 1 END) / COUNT(DISTINCT e.user_id) as avg_refines,
    COUNT(CASE WHEN e.event_name = 'swipe_board_updated' THEN 1 END) / COUNT(DISTINCT e.user_id) as avg_saves,
    COUNT(CASE WHEN e.event_name = 'ad_saved' THEN 1 END) / COUNT(DISTINCT e.user_id) as avg_downloads,
    COUNT(CASE WHEN e.event_name = 'training_viewed' THEN 1 END) / COUNT(DISTINCT e.user_id) as avg_training
  FROM events e
  JOIN power_users pu ON e.user_id = pu.user_id
  WHERE e.timestamp >= CURRENT_DATE - INTERVAL '30 days'
  UNION ALL
  SELECT
    'Regular Users',
    COUNT(CASE WHEN e.event_name = 'search_refined' THEN 1 END) / COUNT(DISTINCT e.user_id),
    COUNT(CASE WHEN e.event_name = 'swipe_board_updated' THEN 1 END) / COUNT(DISTINCT e.user_id),
    COUNT(CASE WHEN e.event_name = 'ad_saved' THEN 1 END) / COUNT(DISTINCT e.user_id),
    COUNT(CASE WHEN e.event_name = 'training_viewed' THEN 1 END) / COUNT(DISTINCT e.user_id)
  FROM events e
  LEFT JOIN power_users pu ON e.user_id = pu.user_id
  WHERE pu.user_id IS NULL
  AND e.timestamp >= CURRENT_DATE - INTERVAL '30 days'
)
SELECT * FROM feature_comparison
```

**Visualization:**
```
Grouped bar chart:
Avg Monthly Usage
  |
45|            ████
  |            ████
40|            ████
  |     ████   ████
35|     ████   ████
  |     ████   ████   ████
30|     ████   ████   ████
  |     ████   ████   ████        ████
25|     ████   ████   ████   ████ ████
  |___________________________________________
       Refine  Save   Download    Training

      Power Users:   ████ (45, 42, 35, 28)
      Regular Users: ░░░░ (12, 15, 8, 5)
```

**Insight:** Power users use refine searches 3.7x more → make refinement easier/more discoverable

---

### Filters for Dashboard 4
- Date range
- User segment (Free / Trial / Paid Monthly / Paid Annual)
- Cohort age (new vs mature users)

---

## Dashboard 5: Executive Overview

**Purpose:** High-level business health at a glance for leadership

**Primary Audience:** CEO, Leadership team

**Key Questions:**
- How is the business performing overall?
- Are we on track for growth goals?
- What needs attention this week?

---

### Metrics & Visualizations

#### **5.1 Key Metrics (KPI Cards)**

**Metrics:** Top-line numbers

**Visualization:**
```
KPI Grid:
┌─────────────────────────┐  ┌─────────────────────────┐  ┌─────────────────────────┐
│ MRR                     │  │ Active Subscribers      │  │ Free Users              │
│ $28,450                 │  │ 327                     │  │ 1,847                   │
│ ↑ +8.2% MoM             │  │ ↑ +12 this month        │  │ ↑ +145 this month       │
└─────────────────────────┘  └─────────────────────────┘  └─────────────────────────┘

┌─────────────────────────┐  ┌─────────────────────────┐  ┌─────────────────────────┐
│ Churn Rate              │  │ Avg LTV                 │  │ Trial Conversion        │
│ 4.2%                    │  │ $487                    │  │ 28.5%                   │
│ ↓ -0.8% vs last month   │  │ ↑ +$32 vs last month    │  │ ↓ -2.1% vs last month   │
└─────────────────────────┘  └─────────────────────────┘  └─────────────────────────┘
```

---

#### **5.2 Growth Trend (Line Chart)**

**Metric:** MRR + Active Subscribers over time

**Visualization:**
```
Dual-axis line chart:
MRR ($)                                      Active Subscribers
   |                                                          |
30k|                             ╱───────                   350
   |                       ╱────╱
25k|                 ╱────╱                                 300
   |           ╱────╱                    ╱────────
20k|     ╱────╱                    ╱───╱                   250
   |────╱                     ╱───╱
15k|_______________________________________                 200
    Aug Sep Oct Nov Dec Jan

    ──── MRR
    ---- Active Subscribers
```

---

#### **5.3 Funnel Health (Mini Funnel)**

**Metric:** This month's conversion rates

**Visualization:**
```
┌───────────────────────────────────────┐
│ New Signups:          1,145           │
│    ↓ 32.5%                            │
│ Started Trial:        372             │
│    ↓ 28.5%                            │
│ Converted to Paid:    106             │
│                                       │
│ Overall Conversion:   9.3%            │
└───────────────────────────────────────┘
```

---

#### **5.4 Revenue Breakdown (Donut Chart)**

**Metric:** MRR by plan type

**Visualization:**
```
Donut chart:
        Annual Plans
          $18,200
           (64%)
    ╱──────────────╲
   │                │
   │    $28,450     │
   │    Total MRR   │
   │                │
    ╲──────────────╱
      Monthly Plans
        $10,250
         (36%)
```

---

#### **5.5 This Week's Highlights (Scorecard)**

**Metrics:** Auto-generated insights

**Visualization:**
```
┌─────────────────────────────────────────────────────────────┐
│ 🟢 MRR grew 8.2% this month (target: 7%)                    │
│ 🟡 Trial conversion dropped to 28.5% (below 30% target)     │
│ 🔴 Churn spiked to 4.2% (above 3.5% target) - investigate! │
│ 🟢 Free-to-trial rate at 32.5% (above 30% target)           │
└─────────────────────────────────────────────────────────────┘
```

---

#### **5.6 Top Acquisition Channels (Bar Chart)**

**Metric:** New subscriptions by source this month

**Visualization:**
```
Bar chart:
New Paid Subscribers This Month
  |
40|████████
  |████████
35|████████
  |████████     ████
30|████████     ████
  |████████     ████     ████
25|████████     ████     ████
  |████████     ████     ████     ████
20|████████     ████     ████     ████
  |_________________________________________
     Organic  YouTube  Google   Referral
       (38)     (28)    (24)     (16)
```

---

### Filters for Dashboard 5
- Date range (This month / Last month / Last quarter)
- No other filters needed (executive view should be simple)

---

## Implementation Priority

**Phase 1 (Weeks 1-2):** Build dashboards in this order
1. Dashboard 3: Revenue & Conversion (finance needs this first)
2. Dashboard 5: Executive Overview (leadership visibility)

**Phase 2 (Weeks 3-4):** Add activation insights
3. Dashboard 1: Activation & Engagement (product focus)

**Phase 3 (Weeks 5-6):** Deep dives
4. Dashboard 2: Free Tier Analysis
5. Dashboard 4: Feature Stickiness

---

## Data Requirements

### Required Tables/Events
- `users` table (user_id, created_at, subscription_status, utm_source, utm_campaign)
- `subscriptions` table (subscription_id, user_id, status, billing_frequency, amount, created_at, canceled_at)
- `events` table (event_name, user_id, timestamp, properties)

### Event Tracking Required
From VidTao's 18 events, these are CRITICAL for dashboards:
1. ✅ user_created
2. ✅ user_onboarding_completed
3. ✅ search_initiated
4. ✅ search_refined
5. ✅ ad_details_viewed
6. ✅ swipe_board_created
7. ✅ swipe_board_updated (activation marker!)
8. ✅ ad_saved (activation marker!)
9. ✅ subscription_trial_started
10. ✅ subscription_created
11. ✅ subscription_cancelled (with cancel_reason property!)
12. ✅ subscription_renewed
13. ✅ training_viewed

**Optional but helpful:**
- user_support_contacted (for churn prediction)
- subscription_payment_failed (for at-risk alerts)

---

## Dashboard Platform Recommendation

Based on your needs, I recommend:

**Option A: Lightdash** (Recommended)
- Open-source, dbt-native
- Fast SQL-based dashboards
- Self-hosted or cloud
- Cost: $50-200/month

**Option B: Metabase**
- Open-source, easy for non-technical users
- Good for quick iteration
- Cost: Free (self-hosted) or $85/month (cloud)

**Option C: Grafana + Postgres**
- Great for real-time dashboards
- More technical setup
- Cost: Free (self-hosted)

**NOT recommended:**
- Amplitude/Mixpanel: Too expensive for your stage ($1k+/month)
- Tableau/Looker: Overkill and expensive

---

## Next Steps

1. **Review & Approve Dashboards:** Which dashboards are highest priority?
2. **Validate Data Sources:** Do you have access to users, subscriptions, and events tables?
3. **Choose Platform:** Lightdash, Metabase, or Grafana?
4. **Build Phase 1:** Start with Revenue & Executive dashboards (2 weeks)
5. **Iterate:** Add more dashboards based on usage and feedback

---

## Questions for You

Before building, I need to clarify:

1. **Do you have a data warehouse?** (BigQuery, Postgres, Snowflake?)
2. **Is your event tracking live?** (Are the 18 events firing to Segment?)
3. **Dashboard refresh frequency?** (Real-time, hourly, daily?)
4. **User access?** (Who needs access to which dashboards?)
5. **Any other metrics not covered here** that you need?

Let me know and I can refine these specs or start building!
