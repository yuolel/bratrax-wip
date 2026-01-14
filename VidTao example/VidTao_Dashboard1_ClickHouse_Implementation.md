# VidTao Dashboard 1: Activation & Engagement
## Implementation Guide for ClickHouse + Lightdash

**Version:** 1.0
**Date:** 2025-01-14
**Dashboard Platform:** Lightdash
**Data Warehouse:** ClickHouse

---

## Overview

This guide provides step-by-step instructions to build **Dashboard 1: Activation & Engagement** for VidTao using ClickHouse and Lightdash.

**Purpose:** Understand user activation path and engagement patterns
**Key Question:** What drives users to activate (first value moment)?
**Priority:** Phase 1 - Build this first!

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [ClickHouse Schema Setup](#clickhouse-schema-setup)
3. [dbt Models](#dbt-models)
4. [Lightdash Configuration](#lightdash-configuration)
5. [Dashboard Build](#dashboard-build)
6. [Testing & Validation](#testing--validation)

---

## Prerequisites

### Required Access
- [x] ClickHouse database access with CREATE TABLE permissions
- [x] Segment events flowing to ClickHouse (18 VidTao events)
- [x] dbt installed and configured for ClickHouse
- [x] Lightdash installed and connected to dbt project

### Required Data
Your ClickHouse database should have these raw tables (populated by Segment):
- `segment_events` - All tracked events
- `segment_identifies` - User identity calls
- `users` - User dimension table (from your app database)
- `subscriptions` - Subscription data (from Stripe or your database)

---

## ClickHouse Schema Setup

### Step 1: Create Analytics Schema

```sql
-- Create analytics database (if doesn't exist)
CREATE DATABASE IF NOT EXISTS vidtao_analytics;

-- Use the analytics database
USE vidtao_analytics;
```

### Step 2: Create Materialized Views for Performance

ClickHouse is optimized for OLAP queries. For Dashboard 1, we'll create materialized views to pre-aggregate key metrics.

#### 2.1 User Activation Events (Materialized View)

```sql
-- Materialized view: Track first value moment for each user
CREATE MATERIALIZED VIEW IF NOT EXISTS mv_user_activation
ENGINE = ReplacingMergeTree(event_timestamp)
ORDER BY (user_id)
AS
SELECT
    user_id,
    min(timestamp) AS first_value_moment,
    multiIf(
        event = 'swipe_board_updated', 'saved_ad',
        event = 'ad_saved', 'saved_ad',
        'other'
    ) AS activation_type
FROM segment_events
WHERE event IN ('swipe_board_updated', 'ad_saved')
  AND user_id IS NOT NULL
  AND user_id != ''
GROUP BY user_id, activation_type;
```

#### 2.2 User Engagement Score (Materialized View)

```sql
-- Materialized view: Calculate weekly engagement scores
CREATE MATERIALIZED VIEW IF NOT EXISTS mv_user_engagement_weekly
ENGINE = SummingMergeTree()
ORDER BY (user_id, week_start)
AS
SELECT
    user_id,
    toStartOfWeek(timestamp) AS week_start,
    countIf(event = 'search_initiated') AS searches,
    countIf(event = 'ad_details_viewed') AS ad_views,
    countIf(event = 'swipe_board_updated') AS ads_saved,
    countIf(event = 'ad_saved') AS ads_saved_direct,
    countIf(event = 'search_refined') AS searches_refined
FROM segment_events
WHERE user_id IS NOT NULL
  AND user_id != ''
GROUP BY user_id, week_start;
```

---

## dbt Models

### Step 3: Set Up dbt Project Structure

```
models/
├── staging/
│   ├── stg_segment_events.sql
│   ├── stg_users.sql
│   └── stg_subscriptions.sql
├── intermediate/
│   ├── int_user_activation.sql
│   └── int_user_engagement_first_week.sql
└── marts/
    ├── dim_users.sql
    └── fct_user_activation.sql
```

### Step 4: Create Staging Models

#### `models/staging/stg_segment_events.sql`

```sql
{{
  config(
    materialized='view',
    tags=['staging', 'segment']
  )
}}

SELECT
    event AS event_name,
    user_id,
    anonymous_id,
    timestamp AS event_timestamp,
    properties,
    context_utm_source AS utm_source,
    context_utm_medium AS utm_medium,
    context_utm_campaign AS utm_campaign
FROM {{ source('segment', 'events') }}
WHERE user_id IS NOT NULL
  AND user_id != ''
```

#### `models/staging/stg_users.sql`

```sql
{{
  config(
    materialized='view',
    tags=['staging', 'core']
  )
}}

SELECT
    user_id,
    email,
    created_at,
    subscription_status,
    utm_source,
    utm_campaign,
    utm_medium
FROM {{ source('app_db', 'users') }}
WHERE user_id IS NOT NULL
```

### Step 5: Create Intermediate Models

#### `models/intermediate/int_user_activation.sql`

```sql
{{
  config(
    materialized='table',
    tags=['intermediate', 'activation']
  )
}}

WITH activation_events AS (
    SELECT
        user_id,
        min(event_timestamp) AS first_value_moment,
        minIf(event_timestamp, event_name = 'swipe_board_updated') AS first_swipe_board_update,
        minIf(event_timestamp, event_name = 'ad_saved') AS first_ad_saved
    FROM {{ ref('stg_segment_events') }}
    WHERE event_name IN ('swipe_board_updated', 'ad_saved')
    GROUP BY user_id
),

user_funnel_steps AS (
    SELECT
        user_id,
        minIf(event_timestamp, event_name = 'user_onboarding_completed') AS onboarding_completed_at,
        minIf(event_timestamp, event_name = 'search_initiated') AS first_search_at
    FROM {{ ref('stg_segment_events') }}
    WHERE event_name IN ('user_onboarding_completed', 'search_initiated')
    GROUP BY user_id
)

SELECT
    u.user_id,
    u.created_at AS signup_date,
    u.utm_source,
    u.utm_campaign,
    u.subscription_status,
    f.onboarding_completed_at,
    f.first_search_at,
    a.first_value_moment AS activation_date,

    -- Calculated fields
    IF(a.first_value_moment IS NOT NULL, 1, 0) AS is_activated,
    dateDiff('day', u.created_at, a.first_value_moment) AS days_to_activate,

    -- Funnel completion flags
    IF(f.onboarding_completed_at IS NOT NULL, 1, 0) AS completed_onboarding,
    IF(f.first_search_at IS NOT NULL, 1, 0) AS performed_search

FROM {{ ref('stg_users') }} u
LEFT JOIN user_funnel_steps f ON u.user_id = f.user_id
LEFT JOIN activation_events a ON u.user_id = a.user_id
```

#### `models/intermediate/int_user_engagement_first_week.sql`

```sql
{{
  config(
    materialized='table',
    tags=['intermediate', 'engagement']
  )
}}

WITH first_week_events AS (
    SELECT
        e.user_id,
        e.event_name,
        e.event_timestamp
    FROM {{ ref('stg_segment_events') }} e
    INNER JOIN {{ ref('stg_users') }} u ON e.user_id = u.user_id
    WHERE e.event_timestamp BETWEEN u.created_at AND u.created_at + INTERVAL 7 DAY
)

SELECT
    user_id,
    countIf(event_name = 'search_initiated') AS searches_first_week,
    countIf(event_name = 'ad_details_viewed') AS ad_views_first_week,
    countIf(event_name = 'swipe_board_updated') AS ads_saved_first_week,
    countIf(event_name = 'ad_saved') AS ads_saved_direct_first_week,
    countIf(event_name = 'search_refined') AS searches_refined_first_week,
    countIf(event_name = 'training_viewed') AS training_views_first_week,

    -- Engagement score (weighted)
    (
        countIf(event_name = 'search_initiated') * 1 +
        countIf(event_name = 'ad_details_viewed') * 1 +
        countIf(event_name = 'swipe_board_updated') * 2 +
        countIf(event_name = 'ad_saved') * 3 +
        countIf(event_name = 'search_refined') * 1
    ) AS engagement_score_first_week

FROM first_week_events
GROUP BY user_id
```

### Step 6: Create Mart Models

#### `models/marts/fct_user_activation.sql`

```sql
{{
  config(
    materialized='table',
    tags=['marts', 'activation']
  )
}}

SELECT
    a.user_id,
    a.signup_date,
    a.utm_source,
    a.utm_campaign,
    a.subscription_status,
    a.activation_date,
    a.is_activated,
    a.days_to_activate,
    a.completed_onboarding,
    a.performed_search,

    -- Add engagement metrics
    e.searches_first_week,
    e.ad_views_first_week,
    e.ads_saved_first_week,
    e.ads_saved_direct_first_week,
    e.engagement_score_first_week,

    -- Engagement bucket
    multiIf(
        e.engagement_score_first_week = 0, '0 - No Activity',
        e.engagement_score_first_week BETWEEN 1 AND 5, '1-5 - Low Engagement',
        e.engagement_score_first_week BETWEEN 6 AND 15, '6-15 - Moderate Engagement',
        e.engagement_score_first_week >= 16, '16+ - High Engagement',
        'Unknown'
    ) AS engagement_bucket

FROM {{ ref('int_user_activation') }} a
LEFT JOIN {{ ref('int_user_engagement_first_week') }} e ON a.user_id = e.user_id
```

### Step 7: Configure dbt Sources

Create `models/staging/sources.yml`:

```yaml
version: 2

sources:
  - name: segment
    description: Raw Segment events from ClickHouse
    database: vidtao_production
    schema: public
    tables:
      - name: events
        identifier: segment_events
        description: All tracked events from Segment
        columns:
          - name: user_id
            description: Unique user identifier
          - name: event
            description: Event name
          - name: timestamp
            description: Event timestamp

  - name: app_db
    description: Application database tables
    database: vidtao_production
    schema: public
    tables:
      - name: users
        description: User dimension table
        columns:
          - name: user_id
            description: Primary key
          - name: created_at
            description: User signup timestamp
```

### Step 8: Run dbt Models

```bash
# Install dbt-clickhouse adapter (if not already installed)
pip install dbt-clickhouse

# Test connection
dbt debug

# Run staging models
dbt run --models staging

# Run intermediate models
dbt run --models intermediate

# Run mart models
dbt run --models marts

# Generate documentation
dbt docs generate
```

---

## Lightdash Configuration

### Step 9: Define Dimensions and Metrics in dbt

Add schema.yml for the activation fact table:

#### `models/marts/schema.yml`

```yaml
version: 2

models:
  - name: fct_user_activation
    description: User activation and engagement metrics
    meta:
      label: "User Activation"
    columns:
      - name: user_id
        description: Unique user identifier
        meta:
          dimension:
            type: string
            label: "User ID"

      - name: signup_date
        description: Date user signed up
        meta:
          dimension:
            type: date
            label: "Signup Date"

      - name: utm_source
        description: Acquisition source
        meta:
          dimension:
            type: string
            label: "Source"

      - name: utm_campaign
        description: Acquisition campaign
        meta:
          dimension:
            type: string
            label: "Campaign"

      - name: subscription_status
        description: Current subscription status
        meta:
          dimension:
            type: string
            label: "Subscription Status"

      - name: is_activated
        description: Whether user has activated
        meta:
          dimension:
            type: boolean
            label: "Is Activated"
          metrics:
            activation_rate:
              type: average
              label: "Activation Rate"
              format: "percent"
              description: "% of users who activated"

      - name: days_to_activate
        description: Days from signup to activation
        meta:
          dimension:
            type: number
            label: "Days to Activate"
          metrics:
            avg_days_to_activate:
              type: average
              label: "Avg Days to Activate"
              format: "number"
              round: 1
            median_days_to_activate:
              type: median
              label: "Median Days to Activate"
              format: "number"

      - name: completed_onboarding
        description: Completed onboarding flag
        meta:
          dimension:
            type: boolean
            label: "Completed Onboarding"
          metrics:
            onboarding_completion_rate:
              type: average
              label: "Onboarding Completion Rate"
              format: "percent"

      - name: performed_search
        description: Performed search flag
        meta:
          dimension:
            type: boolean
            label: "Performed Search"
          metrics:
            search_rate:
              type: average
              label: "Search Rate"
              format: "percent"

      - name: engagement_score_first_week
        description: Engagement score in first 7 days
        meta:
          dimension:
            type: number
            label: "First Week Engagement Score"
          metrics:
            avg_engagement_score:
              type: average
              label: "Avg Engagement Score"
              format: "number"
              round: 1

      - name: engagement_bucket
        description: Engagement level category
        meta:
          dimension:
            type: string
            label: "Engagement Level"

    # Additional metrics
    meta:
      metrics:
        total_signups:
          type: count
          label: "Total Signups"
          description: "Total number of users who signed up"

        activated_users:
          type: count_distinct
          sql: ${TABLE}.user_id
          filters:
            - field: is_activated
              operator: equals
              value: true
          label: "Activated Users"
          description: "Number of users who activated"
```

### Step 10: Deploy to Lightdash

```bash
# Install Lightdash CLI (if not already installed)
npm install -g @lightdash/cli

# Login to Lightdash
lightdash login https://your-lightdash-instance.com

# Deploy dbt project to Lightdash
lightdash deploy

# This will:
# 1. Compile your dbt project
# 2. Upload dimensions and metrics to Lightdash
# 3. Make them available in the UI for dashboard building
```

---

## Dashboard Build

### Step 11: Create Dashboard in Lightdash UI

Now that dimensions and metrics are defined, build the dashboard in Lightdash:

#### Chart 1: Activation Funnel

1. **Create new chart** → Select `fct_user_activation` table
2. **Filter:** `signup_date` in last 30 days
3. **Metrics:**
   - Total Signups
   - Onboarding Completion Rate
   - Search Rate
   - Activation Rate
4. **Chart type:** Horizontal bar chart
5. **Title:** "Activation Funnel (Last 30 Days)"

**Expected output:**
```
Signed Up             ████████████████ 100% (1,000)
Completed Onboarding  █████████████    85% (850)
Performed Search      ██████████       60% (600)
Activated             ██████           40% (400)
```

#### Chart 2: Time to Activation

1. **Create new chart** → Select `fct_user_activation` table
2. **Filter:**
   - `is_activated` = true
   - `signup_date` in last 90 days
3. **Dimensions:** `days_to_activate` (bucketed: 0-1, 2-3, 4-7, 8-14, 15+)
4. **Metrics:** Count of users
5. **Chart type:** Histogram
6. **Title:** "Time to Activation Distribution"

#### Chart 3: Activation Rate by Source

1. **Create new chart** → Select `fct_user_activation` table
2. **Filter:** `signup_date` in last 30 days
3. **Dimensions:** `utm_source`
4. **Metrics:**
   - Total Signups
   - Activated Users
   - Activation Rate
5. **Chart type:** Table
6. **Sort by:** Activation Rate (descending)
7. **Title:** "Activation Rate by Source"

#### Chart 4: Engagement Score Distribution

1. **Create new chart** → Select `fct_user_activation` table
2. **Filter:** `signup_date` in last 30 days
3. **Dimensions:** `engagement_bucket`
4. **Metrics:** Total Signups
5. **Chart type:** Bar chart
6. **Title:** "First Week Engagement Distribution"

#### Chart 5: Retention Cohorts

For retention cohorts, create a custom SQL query in Lightdash:

```sql
WITH user_cohorts AS (
    SELECT
        user_id,
        toStartOfWeek(signup_date) AS cohort_week
    FROM {{ ref('fct_user_activation') }}
    WHERE signup_date >= today() - INTERVAL 90 DAY
),

user_activity AS (
    SELECT
        e.user_id,
        toStartOfWeek(e.event_timestamp) AS activity_week
    FROM {{ ref('stg_segment_events') }} e
    WHERE e.event_name IN ('search_initiated', 'ad_details_viewed', 'swipe_board_updated', 'ad_saved')
    GROUP BY e.user_id, activity_week
)

SELECT
    c.cohort_week,
    dateDiff('week', c.cohort_week, a.activity_week) AS weeks_since_signup,
    uniqExact(a.user_id) AS active_users,
    uniqExact(c.user_id) AS cohort_size,
    round(uniqExact(a.user_id) / uniqExact(c.user_id) * 100, 1) AS retention_pct
FROM user_cohorts c
LEFT JOIN user_activity a ON c.user_id = a.user_id
GROUP BY c.cohort_week, weeks_since_signup
ORDER BY c.cohort_week, weeks_since_signup
```

1. **Create custom SQL chart**
2. **Chart type:** Heatmap
3. **X-axis:** weeks_since_signup
4. **Y-axis:** cohort_week
5. **Values:** retention_pct
6. **Color scale:** 0% (light) to 100% (dark)
7. **Title:** "Weekly Retention Cohorts"

### Step 12: Arrange Dashboard

1. Go to **Dashboards** → **Create New Dashboard**
2. **Name:** "Activation & Engagement"
3. **Add charts in this layout:**

```
┌─────────────────────────────────────────┐
│  Activation Funnel (Last 30 Days)       │
│  [Bar chart]                            │
└─────────────────────────────────────────┘

┌────────────────────┬────────────────────┐
│ Time to Activation │ Engagement Score   │
│ [Histogram]        │ [Bar chart]        │
└────────────────────┴────────────────────┘

┌─────────────────────────────────────────┐
│  Activation Rate by Source              │
│  [Table]                                │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  Weekly Retention Cohorts               │
│  [Heatmap]                              │
└─────────────────────────────────────────┘
```

4. **Add filters:**
   - Date range (last 7/30/90 days)
   - Source
   - Subscription status

---

## Testing & Validation

### Step 13: Validate Data Quality

Run these validation queries in ClickHouse before trusting dashboard numbers:

#### Validation 1: Activation Count Matches

```sql
-- Compare activation count in dbt model vs raw events
SELECT
    'dbt model' AS source,
    countIf(is_activated = 1) AS activated_users
FROM vidtao_analytics.fct_user_activation
WHERE signup_date >= today() - INTERVAL 30 DAY

UNION ALL

SELECT
    'raw events' AS source,
    uniqExact(user_id) AS activated_users
FROM segment_events
WHERE event IN ('swipe_board_updated', 'ad_saved')
  AND user_id IN (
      SELECT user_id FROM users WHERE created_at >= today() - INTERVAL 30 DAY
  );

-- These numbers should match within 1-2%
```

#### Validation 2: No Orphaned Users

```sql
-- Check for users in activation table but not in users table
SELECT COUNT(*)
FROM vidtao_analytics.fct_user_activation a
LEFT JOIN users u ON a.user_id = u.user_id
WHERE u.user_id IS NULL;

-- Should return 0
```

#### Validation 3: Days to Activate is Logical

```sql
-- Check for negative or extremely large days_to_activate
SELECT
    user_id,
    signup_date,
    activation_date,
    days_to_activate
FROM vidtao_analytics.fct_user_activation
WHERE days_to_activate < 0 OR days_to_activate > 365;

-- Should return 0 rows
```

#### Validation 4: Engagement Scores are Reasonable

```sql
-- Check engagement score distribution
SELECT
    engagement_bucket,
    COUNT(*) AS user_count,
    round(COUNT(*) / SUM(COUNT(*)) OVER () * 100, 1) AS pct_of_total
FROM vidtao_analytics.fct_user_activation
WHERE signup_date >= today() - INTERVAL 30 DAY
GROUP BY engagement_bucket
ORDER BY engagement_bucket;

-- Expect bell curve distribution
```

### Step 14: Set Up Data Quality Alerts

Create dbt tests in `models/marts/schema.yml`:

```yaml
models:
  - name: fct_user_activation
    tests:
      - dbt_utils.expression_is_true:
          expression: "days_to_activate >= 0"
          where: "is_activated = 1"

      - dbt_utils.expression_is_true:
          expression: "engagement_score_first_week >= 0"

    columns:
      - name: user_id
        tests:
          - unique
          - not_null

      - name: signup_date
        tests:
          - not_null
```

Run tests:
```bash
dbt test --models fct_user_activation
```

---

## Performance Optimization

### ClickHouse Tuning Tips

#### 1. Use Sampling for Large Datasets

If you have millions of users, use ClickHouse's sampling for faster queries:

```sql
-- Add SAMPLE clause for 10% sample
SELECT
    utm_source,
    round(avg(is_activated) * 100, 1) AS activation_rate_pct
FROM vidtao_analytics.fct_user_activation SAMPLE 0.1
WHERE signup_date >= today() - INTERVAL 30 DAY
GROUP BY utm_source;
```

#### 2. Partition Large Tables by Month

```sql
-- Add partition key to fct_user_activation
ALTER TABLE vidtao_analytics.fct_user_activation
MODIFY PARTITION BY toYYYYMM(signup_date);
```

#### 3. Use Materialized Views for Heavy Aggregations

For retention cohorts (expensive query), create a materialized view:

```sql
CREATE MATERIALIZED VIEW IF NOT EXISTS mv_retention_cohorts
ENGINE = SummingMergeTree()
ORDER BY (cohort_week, weeks_since_signup)
AS
SELECT
    toStartOfWeek(u.created_at) AS cohort_week,
    dateDiff('week', toStartOfWeek(u.created_at), toStartOfWeek(e.timestamp)) AS weeks_since_signup,
    e.user_id
FROM users u
INNER JOIN segment_events e ON u.user_id = e.user_id
WHERE e.event IN ('search_initiated', 'ad_details_viewed', 'swipe_board_updated', 'ad_saved')
  AND u.created_at >= today() - INTERVAL 90 DAY;
```

---

## Troubleshooting

### Common Issues

#### Issue 1: Lightdash can't find dbt models

**Solution:** Ensure dbt project is compiled and deployed:
```bash
dbt compile
lightdash deploy --force
```

#### Issue 2: ClickHouse queries timing out

**Solution:**
- Check if indexes exist on `user_id` and `timestamp`
- Use materialized views for pre-aggregation
- Reduce date range in queries

#### Issue 3: Activation rate seems too low

**Check:**
1. Are events `swipe_board_updated` and `ad_saved` firing correctly in Segment?
2. Run this query to see recent activation events:
```sql
SELECT
    user_id,
    event,
    timestamp
FROM segment_events
WHERE event IN ('swipe_board_updated', 'ad_saved')
ORDER BY timestamp DESC
LIMIT 100;
```

#### Issue 4: Days to activate is NULL for activated users

**Solution:** Check join logic in `int_user_activation.sql`. Ensure `users.created_at` is not NULL.

---

## Next Steps

Once Dashboard 1 is live:

1. **Monitor for 1 week** - Validate numbers match your intuition
2. **Gather feedback** - What questions does the team have?
3. **Iterate** - Add/remove charts based on usage
4. **Build Dashboard 2** - Free Tier Analysis (follow similar process)

---

## Additional Resources

- [ClickHouse SQL Reference](https://clickhouse.com/docs/en/sql-reference/)
- [dbt-clickhouse Adapter](https://github.com/ClickHouse/dbt-clickhouse)
- [Lightdash Documentation](https://docs.lightdash.com/)
- [VidTao Dashboard Specifications](./VidTao_Dashboard_Specifications.md)

---

## Support

Questions or issues? Contact:
- **Data/Analytics:** [YOUR_EMAIL]
- **dbt/Lightdash:** [TEAM_EMAIL]
- **ClickHouse Performance:** [DB_ADMIN_EMAIL]
