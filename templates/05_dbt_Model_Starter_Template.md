# dbt Model Starter Templates for Bratrax

This document provides starter dbt SQL templates for transforming raw data into production-ready ontology tables.

---

## dbt Project Structure

Recommended directory structure:
```
dbt_project/
├── models/
│   ├── staging/          # Clean raw data
│   │   ├── stg_shopify_orders.sql
│   │   ├── stg_klaviyo_events.sql
│   │   └── stg_segment_events.sql
│   ├── intermediate/     # Business logic transformations
│   │   ├── int_user_first_orders.sql
│   │   └── int_session_attribution.sql
│   └── marts/            # Production tables (ontology)
│       ├── dim_users.sql
│       ├── dim_products.sql
│       ├── fact_orders.sql
│       └── fact_sessions.sql
├── tests/               # Custom data tests
└── dbt_project.yml
```

---

## 1. Staging Models

Staging models clean and standardize raw data from source systems.

### Template: `stg_shopify_orders.sql`

```sql
{{
  config(
    materialized='view',
    schema='staging'
  )
}}

with source as (
  select * from {{ source('shopify', 'orders') }}
),

cleaned as (
  select
    -- Primary key
    id as order_id,

    -- Foreign keys
    customer_id as user_id,

    -- Timestamps (standardize to UTC)
    cast(created_at as timestamp) as created_at,
    cast(updated_at as timestamp) as updated_at,

    -- Monetary values (standardize to decimal)
    cast(total_price as numeric) as total_amount,
    cast(subtotal_price as numeric) as subtotal,
    cast(total_discounts as numeric) as discount_amount,
    cast(total_shipping as numeric) as shipping_amount,
    cast(total_tax as numeric) as tax_amount,

    -- Other attributes
    order_number,
    currency,
    payment_gateway_names as payment_method,

    -- Status fields
    financial_status,
    fulfillment_status,
    cancelled_at,

    -- Remove canceled and test orders
    case
      when cancelled_at is not null then true
      when email like '%test%' then true
      when total_price = 0 then true
      else false
    end as is_excluded

  from source
)

select * from cleaned
where not is_excluded  -- Filter out canceled/test orders

```

**Key practices:**
- Rename fields to match ontology naming
- Cast to correct types
- Standardize timestamps to UTC
- Filter out invalid data
- Add `is_excluded` flag rather than filtering in staging (for auditability)

---

### Template: `stg_segment_events.sql`

```sql
{{
  config(
    materialized='incremental',
    unique_key='event_id',
    schema='staging'
  )
}}

with source as (
  select * from {{ source('segment', 'tracks') }}

  {% if is_incremental() %}
    where timestamp >= (select max(event_timestamp) from {{ this }})
  {% endif %}
),

cleaned as (
  select
    -- Event identifiers
    id as event_id,
    event as event_name,
    cast(timestamp as timestamp) as event_timestamp,

    -- User identifiers
    user_id,
    anonymous_id,

    -- Session tracking
    json_extract_scalar(context, '$.sessionId') as session_id,

    -- UTM parameters
    json_extract_scalar(context, '$.campaign.source') as utm_source,
    json_extract_scalar(context, '$.campaign.medium') as utm_medium,
    json_extract_scalar(context, '$.campaign.name') as utm_campaign,

    -- Device/context
    json_extract_scalar(context, '$.device.type') as device_type,
    json_extract_scalar(context, '$.page.url') as page_url,
    json_extract_scalar(context, '$.page.referrer') as referrer,

    -- Event properties (stored as JSON, extracted in intermediate models)
    properties as event_properties

  from source
)

select * from cleaned

```

**For incremental models:**
- Use `materialized='incremental'` for large event tables
- Define `unique_key` to handle duplicates
- Add incremental filter to only process new data

---

## 2. Intermediate Models

Intermediate models apply business logic and prepare data for final marts.

### Template: `int_user_first_orders.sql`

```sql
{{
  config(
    materialized='ephemeral',
    schema='intermediate'
  )
}}

-- Calculate each user's first order timestamp and attribution
with orders as (
  select * from {{ ref('stg_shopify_orders') }}
),

sessions as (
  select * from {{ ref('stg_segment_sessions') }}
),

user_first_order as (
  select
    o.user_id,
    min(o.created_at) as first_order_at,
    min_by(o.order_id, o.created_at) as first_order_id,
    min_by(s.utm_source, o.created_at) as acquisition_source,
    min_by(s.utm_campaign, o.created_at) as acquisition_campaign

  from orders o
  left join sessions s on o.session_id = s.session_id

  group by o.user_id
)

select * from user_first_order

```

**Key patterns:**
- Use `ephemeral` materialization for intermediate models (not stored, just CTEs)
- Use window functions and aggregations for complex logic
- Reference other models with `{{ ref('model_name') }}`

---

### Template: `int_order_attribution.sql`

```sql
{{
  config(
    materialized='table',
    schema='intermediate'
  )
}}

-- Apply attribution logic to determine which marketing source/campaign gets credit for each order

with orders as (
  select * from {{ ref('stg_shopify_orders') }}
),

sessions as (
  select * from {{ ref('stg_segment_sessions') }}
),

ad_clicks as (
  select * from {{ ref('stg_ad_clicks') }}  -- From Meta/Google Ads
),

order_attribution as (
  select
    o.order_id,
    o.user_id,
    o.session_id,
    o.created_at as order_timestamp,

    -- Last-click attribution logic
    -- Check if user clicked an ad within 7 days before order
    coalesce(
      -- Priority 1: Ad click within attribution window
      (select campaign_name
       from ad_clicks ac
       where ac.user_id = o.user_id
         and ac.click_timestamp <= o.created_at
         and ac.click_timestamp >= timestamp_sub(o.created_at, interval 7 day)
       order by ac.click_timestamp desc
       limit 1),

      -- Priority 2: Session UTM parameters
      s.utm_campaign,

      -- Priority 3: User acquisition campaign (first-touch)
      u.acquisition_campaign,

      -- Default: organic/direct
      'organic_direct'
    ) as attribution_campaign,

    coalesce(
      (select source
       from ad_clicks ac
       where ac.user_id = o.user_id
         and ac.click_timestamp <= o.created_at
         and ac.click_timestamp >= timestamp_sub(o.created_at, interval 7 day)
       order by ac.click_timestamp desc
       limit 1),
      s.utm_source,
      u.acquisition_source,
      'organic'
    ) as attribution_source

  from orders o
  left join sessions s on o.session_id = s.session_id
  left join {{ ref('dim_users') }} u on o.user_id = u.user_id
)

select * from order_attribution

```

**Attribution patterns:**
- Use `coalesce()` for fallback logic
- Subqueries for complex lookups
- Document attribution window in comments
- This logic should match ontology document exactly

---

## 3. Marts (Production Tables)

Marts are the final production tables that match your ontology.

### Template: `dim_users.sql`

```sql
{{
  config(
    materialized='table',
    schema='production'
  )
}}

-- User dimension table
-- Grain: One row per user

with base_users as (
  select
    customer_id as user_id,
    email,
    min(created_at) as created_at,
    first_name,
    last_name
  from {{ source('shopify', 'customers') }}
  group by customer_id, email, first_name, last_name
),

user_orders as (
  select
    user_id,
    count(*) as total_orders,
    sum(total_amount) as total_revenue,
    max(created_at) as last_order_at
  from {{ ref('stg_shopify_orders') }}
  group by user_id
),

user_first_orders as (
  select * from {{ ref('int_user_first_orders') }}
),

final as (
  select
    -- Identifiers
    u.user_id,
    u.email,
    u.first_name,
    u.last_name,

    -- Timestamps
    u.created_at,
    fo.first_order_at,
    uo.last_order_at,

    -- Acquisition
    fo.acquisition_source,
    fo.acquisition_campaign,

    -- Lifetime metrics
    coalesce(uo.total_orders, 0) as total_orders,
    coalesce(uo.total_revenue, 0) as total_revenue,

    -- Customer status logic (based on last order date)
    case
      when uo.last_order_at is null then 'never_purchased'
      when uo.last_order_at >= timestamp_sub(current_timestamp(), interval 90 day) then 'active'
      when uo.last_order_at >= timestamp_sub(current_timestamp(), interval 365 day) then 'lapsed'
      else 'churned'
    end as customer_status,

    -- Metadata
    current_timestamp() as dbt_updated_at

  from base_users u
  left join user_orders uo on u.user_id = uo.user_id
  left join user_first_orders fo on u.user_id = fo.user_id
)

select * from final

```

**Dimension table practices:**
- Grain documented in comment
- Include surrogate keys if needed
- Add `dbt_updated_at` timestamp
- Apply business logic (like customer_status)
- Left joins to preserve all users

---

### Template: `fact_orders.sql`

```sql
{{
  config(
    materialized='incremental',
    unique_key='order_id',
    schema='production'
  )
}}

-- Order fact table
-- Grain: One row per order

with orders as (
  select * from {{ ref('stg_shopify_orders') }}

  {% if is_incremental() %}
    where created_at >= (select max(created_at) from {{ this }})
  {% endif %}
),

order_attribution as (
  select * from {{ ref('int_order_attribution') }}
),

user_order_sequence as (
  -- Calculate order number (1st, 2nd, 3rd order) per user
  select
    order_id,
    user_id,
    row_number() over (partition by user_id order by created_at) as order_number
  from orders
),

final as (
  select
    -- Order identifiers
    o.order_id,
    o.order_number as shopify_order_number,
    seq.order_number,  -- Sequential order number per user

    -- Foreign keys
    o.user_id,
    o.session_id,

    -- Timestamps
    o.created_at,
    o.updated_at,

    -- Monetary values
    o.total_amount,
    o.subtotal,
    o.discount_amount,
    o.shipping_amount,
    o.tax_amount,
    o.currency,

    -- Order attributes
    o.payment_method,
    o.financial_status,
    o.fulfillment_status,

    -- Derived flags
    case when seq.order_number = 1 then true else false end as is_first_order,

    -- Attribution
    attr.attribution_source,
    attr.attribution_campaign,

    -- Metadata
    current_timestamp() as dbt_updated_at

  from orders o
  left join order_attribution attr on o.order_id = attr.order_id
  left join user_order_sequence seq on o.order_id = seq.order_id
)

select * from final

```

**Fact table practices:**
- Grain documented
- Foreign keys to dimension tables
- Timestamps preserved
- Calculated fields (like `is_first_order`)
- Use incremental for large tables
- Include attribution fields

---

### Template: `fact_order_items.sql`

```sql
{{
  config(
    materialized='incremental',
    unique_key='order_item_id',
    schema='production'
  )
}}

-- Order line items fact table
-- Grain: One row per product per order

with order_items as (
  select * from {{ source('shopify', 'order_lines') }}

  {% if is_incremental() %}
    where order_created_at >= (select max(order_created_at) from {{ this }})
  {% endif %}
),

products as (
  select * from {{ ref('dim_products') }}
),

final as (
  select
    -- Line item identifiers
    oi.id as order_item_id,
    oi.order_id,

    -- Product foreign key
    oi.product_id,

    -- Quantities and prices
    oi.quantity,
    cast(oi.price as numeric) as unit_price,
    cast(oi.price * oi.quantity as numeric) as total_price,

    -- Product attributes (denormalized for query performance)
    p.product_name,
    p.product_category,
    p.product_subcategory,
    p.cost as unit_cost,
    cast((oi.price - p.cost) * oi.quantity as numeric) as gross_profit,

    -- Metadata
    oi.order_created_at,
    current_timestamp() as dbt_updated_at

  from order_items oi
  left join products p on oi.product_id = p.product_id
)

select * from final

```

---

## 4. Aggregation Models (for Dashboard Performance)

Pre-aggregate data for faster dashboard queries.

### Template: `agg_daily_revenue.sql`

```sql
{{
  config(
    materialized='incremental',
    unique_key=['date', 'attribution_source'],
    schema='production'
  )
}}

-- Daily revenue aggregation by attribution source
-- Grain: One row per date per attribution source

with orders as (
  select * from {{ ref('fact_orders') }}

  {% if is_incremental() %}
    where date(created_at) >= date_sub(current_date(), interval 7 day)
  {% endif %}
),

daily_metrics as (
  select
    date(created_at) as date,
    attribution_source,

    -- Revenue metrics
    sum(total_amount) as total_revenue,
    sum(subtotal) as subtotal_revenue,
    sum(discount_amount) as total_discounts,

    -- Order metrics
    count(distinct order_id) as order_count,
    count(distinct user_id) as customer_count,
    count(distinct case when is_first_order then user_id end) as new_customer_count,

    -- Calculated metrics
    sum(total_amount) / count(distinct order_id) as avg_order_value,

    -- Metadata
    current_timestamp() as dbt_updated_at

  from orders
  group by date(created_at), attribution_source
)

select * from daily_metrics

```

**Aggregation patterns:**
- Pre-calculate common metrics
- Grain at day level for performance
- Include dimensions commonly filtered on
- Use incremental with lookback window for late-arriving data

---

## 5. dbt Tests

### Schema Tests (in `schema.yml`)

```yaml
version: 2

models:
  - name: fact_orders
    description: "Order transactions"
    columns:
      - name: order_id
        description: "Unique order identifier"
        tests:
          - unique
          - not_null

      - name: user_id
        description: "Customer who placed order"
        tests:
          - not_null
          - relationships:
              to: ref('dim_users')
              field: user_id

      - name: total_amount
        description: "Order total"
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 0
              inclusive: true

      - name: is_first_order
        description: "Is this the customer's first order?"
        tests:
          - not_null
          - accepted_values:
              values: [true, false]

  - name: dim_users
    description: "User dimension"
    columns:
      - name: user_id
        tests:
          - unique
          - not_null
```

### Custom Data Tests

Create `tests/fact_orders_math_check.sql`:

```sql
-- Test that order total math is correct

select
  order_id,
  total_amount,
  subtotal + tax_amount + shipping_amount - discount_amount as calculated_total,
  abs(total_amount - (subtotal + tax_amount + shipping_amount - discount_amount)) as difference

from {{ ref('fact_orders') }}

where abs(total_amount - (subtotal + tax_amount + shipping_amount - discount_amount)) > 0.01

-- If this query returns rows, the test fails
```

Create `tests/first_order_logic_check.sql`:

```sql
-- Test that is_first_order flag is correct

with order_sequence as (
  select
    order_id,
    user_id,
    is_first_order,
    row_number() over (partition by user_id order by created_at) as actual_order_number
  from {{ ref('fact_orders') }}
)

select *
from order_sequence
where
  (actual_order_number = 1 and not is_first_order)  -- Should be first order but isn't flagged
  or (actual_order_number > 1 and is_first_order)    -- Shouldn't be first order but is flagged

-- If this returns rows, the test fails
```

---

## 6. Common Patterns & Best Practices

### Date Handling
```sql
-- Always use UTC timestamps
cast(created_at as timestamp) as created_at

-- For date-based aggregations, extract date
date(created_at) as order_date

-- For timezone conversions (if needed)
timestamp(datetime(created_at, 'America/New_York')) as created_at_et
```

### Null Handling
```sql
-- Use coalesce for defaults
coalesce(discount_amount, 0) as discount_amount

-- Use nullif to convert empty strings to null
nullif(trim(email), '') as email
```

### JSON Extraction (for event properties)
```sql
-- BigQuery
json_extract_scalar(properties, '$.product_id') as product_id

-- For nested values
json_extract_scalar(properties, '$.items[0].name') as first_item_name
```

### Deduplication
```sql
-- Keep most recent record per unique key
with deduped as (
  select *,
    row_number() over (partition by order_id order by updated_at desc) as rn
  from source
)
select * from deduped where rn = 1
```

### Incremental Model Pattern
```sql
{{
  config(
    materialized='incremental',
    unique_key='id',
    incremental_strategy='merge'  -- or 'delete+insert'
  )
}}

select * from source

{% if is_incremental() %}
  where updated_at > (select max(updated_at) from {{ this }})
{% endif %}
```

---

## 7. Execution Commands

**Run all models:**
```bash
dbt run
```

**Run specific model:**
```bash
dbt run --select fact_orders
```

**Run model and downstream dependencies:**
```bash
dbt run --select fact_orders+
```

**Run tests:**
```bash
dbt test
```

**Generate documentation:**
```bash
dbt docs generate
dbt docs serve
```

**Full refresh (rebuild from scratch):**
```bash
dbt run --full-refresh
```

---

## 8. Next Steps

1. **Customize** these templates based on client's ontology
2. **Add** client-specific business logic
3. **Write tests** for critical calculations
4. **Document** models in `.yml` files
5. **Test locally** before deploying
6. **Schedule** daily runs in production

---

*dbt Model Templates v1.0*
*For questions: [YOUR_EMAIL]*
