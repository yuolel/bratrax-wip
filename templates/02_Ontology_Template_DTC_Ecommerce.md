# [CLIENT_NAME] Analytics Ontology

**Version:** 1.0
**Date:** [DATE]
**Business Model:** DTC E-commerce
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
**What they sell:** [Products/Services]

**Revenue model:** [One-time purchase / Subscription / Hybrid]

**Average order value:** $[AOV]

**Average customer lifetime:** [X] months

**Primary growth goal:** [Acquisition / Retention / AOV expansion / Profitability]

### 1.2 Key Business Questions
The dashboards must answer these questions:

1. [Question 1, e.g., "Which ad campaigns are driving profitable customers?"]
2. [Question 2, e.g., "What's our true CAC including all marketing spend?"]
3. [Question 3, e.g., "Which products have highest repeat purchase rate?"]
4. [Question 4]
5. [Question 5]

---

## 2. Entity Definitions

Entities are the "nouns" of the business—the things we track.

### 2.1 Core Entities

#### **User**
A person who has interacted with the brand.

| Property | Type | Definition | Example |
|----------|------|------------|---------|
| `user_id` | string | Unique identifier (primary key) | `usr_a3b4c5d6` |
| `email` | string | Email address | `customer@example.com` |
| `created_at` | timestamp | When user first identified | `2025-01-15T10:30:00Z` |
| `first_order_at` | timestamp | When they became a customer | `2025-01-16T14:22:00Z` |
| `acquisition_source` | string | First-touch marketing source | `facebook_ads`, `google_organic` |
| `acquisition_campaign` | string | First-touch campaign | `spring_sale_2025` |
| `total_orders` | integer | Lifetime order count | `3` |
| `total_revenue` | decimal | Lifetime revenue (gross) | `245.50` |
| `customer_status` | string | Current status | `active`, `lapsed`, `churned` |

**Business logic:**
- A user becomes a "customer" after first order
- `customer_status = active` if ordered in last 90 days
- `customer_status = lapsed` if last order 91-365 days ago
- `customer_status = churned` if last order >365 days ago

---

#### **Session**
A period of activity on the website/app.

| Property | Type | Definition | Example |
|----------|------|------------|---------|
| `session_id` | string | Unique identifier | `sess_x7y8z9` |
| `user_id` | string | Associated user (if known) | `usr_a3b4c5d6` |
| `started_at` | timestamp | Session start time | `2025-01-15T10:30:00Z` |
| `ended_at` | timestamp | Session end time (or timeout) | `2025-01-15T10:45:00Z` |
| `utm_source` | string | Marketing source parameter | `facebook` |
| `utm_medium` | string | Marketing medium parameter | `cpc` |
| `utm_campaign` | string | Campaign identifier | `spring_sale_2025` |
| `landing_page` | string | First page viewed | `/products/cleanser` |
| `referrer` | string | Referring URL | `https://facebook.com` |
| `device_type` | string | Device category | `mobile`, `desktop`, `tablet` |

**Business logic:**
- Session timeout: 30 minutes of inactivity
- UTM parameters captured at session start only

---

#### **Order**
A completed purchase transaction.

| Property | Type | Definition | Example |
|----------|------|------------|---------|
| `order_id` | string | Unique identifier | `ord_123456` |
| `user_id` | string | Customer who placed order | `usr_a3b4c5d6` |
| `session_id` | string | Session where order occurred | `sess_x7y8z9` |
| `created_at` | timestamp | Order placed time | `2025-01-15T10:45:00Z` |
| `total_amount` | decimal | Order total (gross) | `89.99` |
| `subtotal` | decimal | Pre-tax, pre-shipping amount | `75.00` |
| `discount_amount` | decimal | Total discounts applied | `10.00` |
| `shipping_amount` | decimal | Shipping cost | `8.99` |
| `tax_amount` | decimal | Tax amount | `6.00` |
| `order_number` | integer | Customer-facing order number | `1`, `2`, `3` (per user) |
| `is_first_order` | boolean | Is this their first order? | `true` / `false` |
| `attribution_source` | string | Marketing source credited | `facebook_ads` |
| `attribution_campaign` | string | Campaign credited | `spring_sale_2025` |

**Business logic:**
- `order_number` is sequential per user (1 = first order, 2 = second, etc.)
- `is_first_order = true` when `order_number = 1`
- Attribution determined by [attribution model chosen in Section 4]

---

#### **Product**
An item available for purchase.

| Property | Type | Definition | Example |
|----------|------|------------|---------|
| `product_id` | string | Unique identifier | `prod_789` |
| `product_name` | string | Display name | `Hydrating Cleanser` |
| `product_category` | string | Primary category | `Skincare` |
| `product_subcategory` | string | Subcategory | `Cleansers` |
| `price` | decimal | Current price | `25.00` |
| `cost` | decimal | Cost of goods sold | `8.50` |
| `sku` | string | Stock keeping unit | `SKU-CLEAN-001` |

---

#### **Order_Item**
Individual line items within an order.

| Property | Type | Definition | Example |
|----------|------|------------|---------|
| `order_item_id` | string | Unique identifier | `item_999` |
| `order_id` | string | Parent order | `ord_123456` |
| `product_id` | string | Product purchased | `prod_789` |
| `quantity` | integer | Units purchased | `2` |
| `unit_price` | decimal | Price per unit | `25.00` |
| `total_price` | decimal | Line item total | `50.00` |

---

#### **Marketing_Campaign**
A marketing initiative tracked for performance.

| Property | Type | Definition | Example |
|----------|------|------------|---------|
| `campaign_id` | string | Unique identifier | `camp_abc123` |
| `campaign_name` | string | Human-readable name | `Spring Sale 2025` |
| `channel` | string | Marketing channel | `facebook_ads`, `google_ads`, `email` |
| `start_date` | date | Campaign start | `2025-01-15` |
| `end_date` | date | Campaign end (if applicable) | `2025-01-31` |
| `total_spend` | decimal | Total ad spend | `5000.00` |
| `utm_campaign` | string | UTM parameter value | `spring_sale_2025` |

---

#### **Ad_Creative** (if tracking creative performance)
Individual ad creatives/variations.

| Property | Type | Definition | Example |
|----------|------|------------|---------|
| `creative_id` | string | Unique identifier | `cre_xyz789` |
| `campaign_id` | string | Parent campaign | `camp_abc123` |
| `creative_name` | string | Internal name | `Video_BenefitsDriven_V2` |
| `creative_type` | string | Format | `video`, `image`, `carousel` |
| `creative_concept` | string | Marketing concept | `benefits_driven`, `lifestyle`, `ugc` |
| `platform_creative_id` | string | Platform's ID (Meta, Google) | `23850234852345` |
| `impressions` | integer | Total impressions | `125000` |
| `clicks` | integer | Total clicks | `3500` |
| `spend` | decimal | Total spend on this creative | `850.00` |

---

### 2.2 Entity Relationships

```
User (1) ─────< Orders (many)
  │
  └────< Sessions (many)

Order (1) ─────< Order_Items (many)

Order_Item (many) >───── Product (1)

Session (many) >───── Marketing_Campaign (1)
  │
  └─> Order (1) [attribution relationship]

Marketing_Campaign (1) ─────< Ad_Creative (many)
```

---

## 3. Event Taxonomy

Events are the "verbs"—things that happen. Following the **entity_activity** naming convention.

### 3.1 Event Naming Rules
1. Format: `{entity}_{activity}`
2. All lowercase, underscores only
3. Past tense for activity (e.g., `viewed`, `created`, `completed`)
4. Be specific (e.g., `product_detail_viewed` not just `viewed`)

### 3.2 Event Complexity Guide

Based on business complexity, target these event counts:
- **Basic DTC:** 10-12 events (single channel, simple products)
- **Multi-Channel DTC:** 15-18 events (email + SMS + ads, attribution needed)
- **Subscription Business:** 18-22 events (retention focus, subscription lifecycle)
- **Complex/Enterprise:** 20-25 events (multiple business models, advanced analytics)

**Reference:** See Event Storming Workshop Guide for how to determine the right event set for your business.

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
- **Week 1:** Implement Tier 1 (4-5 events)
- **Week 2:** Launch initial dashboards, validate tracking
- **Week 3-4:** Add Tier 2 events (8 total) based on usage
- **Week 5+:** Add Tier 3 selectively as needed

**Exception - Implement all tiers at once only if:**
- Client has subscription/retention model requiring Tier 3 events from day 1
- Client is sophisticated and knows exactly which events they need
- Historical data for advanced events is critical (can't backfill later)

---

### 3.4 Core Events Catalog

Events are organized by implementation tier.

---

## **TIER 1: Critical Events (Implement First)**

These events are required to calculate core metrics (revenue, CAC, ROAS). Must be implemented before dashboard launch.

**Target: 4-5 events**
**Timeline: Week 1 of implementation**

---

#### **User Lifecycle Events**

##### `user_signed_up`
**When:** User creates an account
**Why critical:** Required for CAC calculation, user acquisition tracking

**Properties:**
| Property | Type | Required | Example |
|----------|------|----------|---------|
| `user_id` | string | Yes | `usr_a3b4c5d6` |
| `email` | string | Yes | `customer@example.com` |
| `signup_source` | string | Yes | `homepage`, `checkout`, `popup` |
| `utm_source` | string | No | `facebook` |
| `utm_medium` | string | No | `cpc` |
| `utm_campaign` | string | No | `spring_sale_2025` |

---

##### `session_started`
**When:** User begins a new session on the website
**Why critical:** Required for attribution, conversion rate calculation

**Properties:**
| Property | Type | Required | Example |
|----------|------|----------|---------|
| `session_id` | string | Yes | `sess_x7y8z9` |
| `user_id` | string | No | `usr_a3b4c5d6` |
| `utm_source` | string | No | `facebook` |
| `utm_medium` | string | No | `cpc` |
| `utm_campaign` | string | No | `spring_sale_2025` |
| `landing_page` | string | Yes | `/products/cleanser` |
| `referrer` | string | No | `https://facebook.com` |
| `device_type` | string | Yes | `mobile`, `desktop`, `tablet` |

---

#### **Purchase Events**

##### `order_completed` ⭐ **MOST CRITICAL**
**When:** Order is successfully placed and payment confirmed
**Why critical:** Revenue tracking, ROAS, all financial metrics

**Properties:**
| Property | Type | Required | Example |
|----------|------|----------|---------|
| `user_id` | string | Yes | `usr_a3b4c5d6` |
| `session_id` | string | Yes | `sess_x7y8z9` |
| `order_id` | string | Yes | `ord_123456` |
| `order_number` | integer | Yes | `1`, `2`, `3` (sequential per user) |
| `total_amount` | decimal | Yes | `89.99` |
| `subtotal` | decimal | Yes | `75.00` |
| `discount_amount` | decimal | Yes | `10.00` |
| `shipping_amount` | decimal | Yes | `8.99` |
| `tax_amount` | decimal | Yes | `6.00` |
| `currency` | string | Yes | `USD` |
| `is_first_order` | boolean | Yes | `true` / `false` |
| `payment_method` | string | Yes | `credit_card`, `paypal`, `apple_pay` |
| `products` | array | Yes | Array of product objects (see below) |

**Products array structure:**
```json
[
  {
    "product_id": "prod_789",
    "product_name": "Hydrating Cleanser",
    "product_category": "Skincare",
    "quantity": 2,
    "price": 25.00
  }
]
```

---

#### **Marketing Attribution Events**

##### `email_clicked`
**When:** User clicks a link in a marketing email
**Why critical:** Email attribution, measuring email marketing effectiveness

**Properties:**
| Property | Type | Required | Example |
|----------|------|----------|---------|
| `user_id` | string | Yes | `usr_a3b4c5d6` |
| `email_id` | string | Yes | `email_campaign_123` |
| `campaign_name` | string | Yes | `spring_sale_email` |
| `link_url` | string | Yes | `https://site.com/products/cleanser` |
| `email_subject` | string | No | `20% Off Spring Sale` |

---

**End of Tier 1 (4-5 core events)**

**Next step:** Validate Tier 1 tracking, launch initial dashboards, then proceed to Tier 2.

---

## **TIER 2: Attribution & Engagement Events (Implement Second)**

These events provide attribution detail and engagement metrics. Implement after Tier 1 is validated.

**Target: 6-8 events**
**Timeline: Week 3-4 of implementation**

**Before implementing Tier 2:**
- ✅ Tier 1 events validated and working
- ✅ Initial dashboards launched
- ✅ Revenue reconciliation passing (≤2% variance)
- ✅ Client has used dashboards for at least 1 week

---

#### **Product Discovery Events**

##### `product_viewed`
**When:** User views a product detail page
**Why matters:** Product engagement, conversion funnel analysis

**Properties:**
| Property | Type | Required | Example |
|----------|------|----------|---------|
| `user_id` | string | No | `usr_a3b4c5d6` |
| `session_id` | string | Yes | `sess_x7y8z9` |
| `product_id` | string | Yes | `prod_789` |
| `product_name` | string | Yes | `Hydrating Cleanser` |
| `product_category` | string | Yes | `Skincare` |
| `product_subcategory` | string | No | `Cleansers` |
| `price` | decimal | Yes | `25.00` |
| `currency` | string | Yes | `USD` |

---

##### `collection_viewed`
**When:** User views a product category or collection page
**Why matters:** Understand browsing behavior, popular categories

**Properties:**
| Property | Type | Required | Example |
|----------|------|----------|---------|
| `user_id` | string | No | `usr_a3b4c5d6` |
| `session_id` | string | Yes | `sess_x7y8z9` |
| `collection_id` | string | Yes | `col_skincare` |
| `collection_name` | string | Yes | `Skincare` |
| `product_count` | integer | No | `24` |

---

##### `search_initiated`
**When:** User performs a product search
**Why matters:** Understand what customers are looking for, search-driven conversions

**Properties:**
| Property | Type | Required | Example |
|----------|------|----------|---------|
| `user_id` | string | No | `usr_a3b4c5d6` |
| `session_id` | string | Yes | `sess_x7y8z9` |
| `search_term` | string | Yes | `vitamin c serum` |
| `search_results_count` | integer | Yes | `12` |

---

#### **Cart & Checkout Events**

##### `product_added_to_cart`
**When:** User adds product to shopping cart
**Why matters:** Add-to-cart rate, cart abandonment analysis

**Properties:**
| Property | Type | Required | Example |
|----------|------|----------|---------|
| `user_id` | string | No | `usr_a3b4c5d6` |
| `session_id` | string | Yes | `sess_x7y8z9` |
| `product_id` | string | Yes | `prod_789` |
| `product_name` | string | Yes | `Hydrating Cleanser` |
| `product_category` | string | Yes | `Skincare` |
| `quantity` | integer | Yes | `2` |
| `price` | decimal | Yes | `25.00` |
| `currency` | string | Yes | `USD` |

---

##### `cart_viewed`
**When:** User opens/views their shopping cart
**Why matters:** Cart engagement, cart abandonment funnel

**Properties:**
| Property | Type | Required | Example |
|----------|------|----------|---------|
| `user_id` | string | No | `usr_a3b4c5d6` |
| `session_id` | string | Yes | `sess_x7y8z9` |
| `cart_total` | decimal | Yes | `89.99` |
| `item_count` | integer | Yes | `3` |
| `currency` | string | Yes | `USD` |

---

##### `checkout_started`
**When:** User begins the checkout process
**Why matters:** Checkout conversion rate, abandonment analysis

**Properties:**
| Property | Type | Required | Example |
|----------|------|----------|---------|
| `user_id` | string | No | `usr_a3b4c5d6` |
| `session_id` | string | Yes | `sess_x7y8z9` |
| `cart_total` | decimal | Yes | `89.99` |
| `item_count` | integer | Yes | `3` |
| `currency` | string | Yes | `USD` |

---

#### **Additional Marketing Events**

##### `email_opened`
**When:** User opens a marketing email
**Why matters:** Email engagement metrics, open rate

**Properties:**
| Property | Type | Required | Example |
|----------|------|----------|---------|
| `user_id` | string | Yes | `usr_a3b4c5d6` |
| `email_id` | string | Yes | `email_campaign_123` |
| `campaign_name` | string | Yes | `spring_sale_email` |
| `email_subject` | string | No | `20% Off Spring Sale` |

---

##### `sms_clicked`
**When:** User clicks a link in an SMS message
**Why matters:** SMS attribution and effectiveness (if using SMS marketing)

**Properties:**
| Property | Type | Required | Example |
|----------|------|----------|---------|
| `user_id` | string | Yes | `usr_a3b4c5d6` |
| `sms_id` | string | Yes | `sms_campaign_456` |
| `campaign_name` | string | Yes | `flash_sale_sms` |
| `link_url` | string | Yes | `https://site.com/sale` |

---

**End of Tier 2 (8 additional events) → Total: 12-13 events**

**Next step:** Review dashboard usage with client. Only add Tier 3 events if they request specific functionality.

---

## **TIER 3: Advanced & Diagnostic Events (Future Enhancement)**

These events provide deeper insights for optimization. **Implement selectively based on client requests**, not automatically.

**Target: 3-5 events**
**Timeline: Week 5+ or on-demand**

**Only implement Tier 3 events when:**
- ✅ Client specifically requests the functionality
- ✅ Tier 1 + 2 dashboards are being actively used
- ✅ Client has demonstrated they need this level of detail

**Common scenarios for Tier 3:**
- Client says: "We need to understand why people remove items from cart" → Add `product_removed_from_cart`
- Client says: "Return rate is concerning, need to track it" → Add `order_refunded`
- Client launches subscription model → Add subscription events

---

#### **Cart Optimization**

##### `product_removed_from_cart`
**When:** User removes item from cart
**Why matters:** Understand why users change their mind

**Properties:**
| Property | Type | Required | Example |
|----------|------|----------|---------|
| `user_id` | string | No | `usr_a3b4c5d6` |
| `session_id` | string | Yes | `sess_x7y8z9` |
| `product_id` | string | Yes | `prod_789` |
| `product_name` | string | Yes | `Hydrating Cleanser` |
| `quantity` | integer | Yes | `2` |

---

#### **Post-Purchase Events**

##### `order_refunded`
**When:** Refund is processed for an order
**Why matters:** Return rate analysis, product quality issues

**Properties:**
| Property | Type | Required | Example |
|----------|------|----------|---------|
| `user_id` | string | Yes | `usr_a3b4c5d6` |
| `order_id` | string | Yes | `ord_123456` |
| `refund_amount` | decimal | Yes | `89.99` |
| `refund_reason` | string | No | `changed_mind`, `defective`, `wrong_item` |
| `currency` | string | Yes | `USD` |

---

##### `review_submitted`
**When:** Customer leaves a product review
**Why matters:** Customer satisfaction, social proof generation

**Properties:**
| Property | Type | Required | Example |
|----------|------|----------|---------|
| `user_id` | string | Yes | `usr_a3b4c5d6` |
| `product_id` | string | Yes | `prod_789` |
| `order_id` | string | No | `ord_123456` |
| `rating` | integer | Yes | `5` (1-5 scale) |
| `review_text` | string | No | `Love this cleanser!` |

---

#### **Subscription Events** (if applicable)

##### `subscription_created`
**When:** Customer starts a subscription
**Why matters:** Subscription acquisition, MRR growth

**Properties:**
| Property | Type | Required | Example |
|----------|------|----------|---------|
| `user_id` | string | Yes | `usr_a3b4c5d6` |
| `subscription_id` | string | Yes | `sub_999` |
| `plan_name` | string | Yes | `monthly_box` |
| `plan_price` | decimal | Yes | `29.99` |
| `billing_frequency` | string | Yes | `monthly`, `quarterly` |
| `currency` | string | Yes | `USD` |

---

##### `subscription_cancelled`
**When:** Customer cancels their subscription
**Why matters:** Churn analysis, retention efforts

**Properties:**
| Property | Type | Required | Example |
|----------|------|----------|---------|
| `user_id` | string | Yes | `usr_a3b4c5d6` |
| `subscription_id` | string | Yes | `sub_999` |
| `cancellation_reason` | string | No | `too_expensive`, `not_using`, `other` |
| `months_active` | integer | Yes | `6` |

---

**End of Tier 3 (5 additional events) → Total: 17-18 events**

---

### 3.5 Event Reduction Summary

After event storming workshop, document your final event set here:

**Total events identified in brainstorming:** [X]
**Final core events (all tiers):** [Y]

**Implementation approach:** ☑ Progressive (recommended) / ☐ All at once

**Tier 1 (Critical - Week 1):** [N] events
- [List tier 1 events selected for this client]

**Tier 2 (Attribution - Week 3-4):** [N] events
- [List tier 2 events selected for this client]

**Tier 3 (Advanced - On-demand):** [N] events
- [List tier 3 events that may be added later]

**Total implemented at initial launch:** [Tier 1 only or Tier 1 + Tier 2] events

**Events NOT tracked** (and why):
- [Event name]: [Reason for exclusion]
- Example: `page_scrolled` - Doesn't influence key decisions, adds noise
- Example: `collection_viewed` - Deprioritized, add in Tier 2 if client uses category performance metrics

**Phase gates:**
- ☐ Tier 1 validated before starting Tier 2
- ☐ Client has used Tier 1 dashboards for 1+ week
- ☐ Tier 3 events only added on client request

---

## 4. Metric Definitions

Metrics are calculated values that answer business questions.

### 4.1 Revenue Metrics

#### **Revenue (Gross)**
**Definition:** Total order value including tax and shipping

**Calculation:**
```sql
SUM(orders.total_amount)
```

**Filters:** Exclude canceled/refunded orders

---

#### **Revenue (Net)**
**Definition:** Revenue after discounts, refunds, and returns

**Calculation:**
```sql
SUM(orders.subtotal - orders.discount_amount) - SUM(refunds.amount)
```

---

#### **Average Order Value (AOV)**
**Definition:** Average revenue per order

**Calculation:**
```sql
SUM(orders.total_amount) / COUNT(DISTINCT orders.order_id)
```

**Typical range:** $[X] - $[Y]

---

### 4.2 Customer Metrics

#### **Customer Acquisition Cost (CAC)**
**Definition:** Cost to acquire one new customer

**Calculation:**
```sql
SUM(marketing_spend) / COUNT(DISTINCT first_time_customers)
```

**Notes:**
- Include all marketing spend: ads, email tools, attribution tools, agency fees
- Only count users who placed first order in the period
- Calculate monthly and overall

**Target:** $[X] or lower

---

#### **Lifetime Value (LTV)**
**Definition:** Average total revenue from a customer over their lifetime

**Calculation:**
```sql
SUM(orders.total_amount) / COUNT(DISTINCT users with orders)
```

**Cohort-based:** Calculate LTV by acquisition cohort (month/quarter)

**Target:** 3x CAC minimum

---

#### **LTV:CAC Ratio**
**Definition:** Relationship between customer value and acquisition cost

**Calculation:**
```sql
LTV / CAC
```

**Healthy ratio:** 3:1 or higher

---

#### **Repeat Purchase Rate**
**Definition:** Percentage of customers who make 2+ orders

**Calculation:**
```sql
COUNT(DISTINCT users with order_count >= 2) / COUNT(DISTINCT users with orders)
```

**Target:** [X]%

---

### 4.3 Marketing Performance Metrics

#### **Return on Ad Spend (ROAS)**
**Definition:** Revenue generated per dollar of ad spend

**Calculation:**
```sql
SUM(attributed_revenue) / SUM(ad_spend)
```

**Attribution window:** [X] days (e.g., 7-day click, 1-day view)

**Target:** [X]x or higher

---

#### **Cost Per Acquisition (CPA)**
**Definition:** Cost per order (not necessarily new customer)

**Calculation:**
```sql
SUM(ad_spend) / COUNT(attributed_orders)
```

**Differs from CAC:** CPA counts all orders, CAC counts first-time customers only

---

#### **Click-Through Rate (CTR)**
**Definition:** Percentage of ad impressions that result in clicks

**Calculation:**
```sql
SUM(clicks) / SUM(impressions)
```

**Benchmark:** [X]% (varies by channel)

---

#### **Conversion Rate (Website)**
**Definition:** Percentage of sessions that result in an order

**Calculation:**
```sql
COUNT(orders) / COUNT(sessions)
```

**Typical range:** [X]% - [Y]%

---

### 4.4 Product Performance Metrics

#### **Product Revenue**
**Definition:** Total revenue by product

**Calculation:**
```sql
SUM(order_items.total_price)
GROUP BY product_id
```

---

#### **Product Margin**
**Definition:** Profit per product after COGS

**Calculation:**
```sql
SUM((unit_price - cost) * quantity)
```

---

#### **Product Repeat Rate**
**Definition:** How often customers repurchase a specific product

**Calculation:**
```sql
COUNT(DISTINCT users who bought product 2+ times) / COUNT(DISTINCT users who bought product)
```

---

## 5. Attribution Logic

### 5.1 Attribution Model
**Model:** [Last-click / First-click / Multi-touch - choose one]

**Why this model:** [Explanation based on business model and customer journey length]

### 5.2 Attribution Window
- **Click attribution:** [X] days (e.g., 7 days)
- **View attribution:** [Y] days (e.g., 1 day)

**Logic:**
```
IF user clicked ad within [X] days of order → credit that campaign
ELSE IF user viewed ad within [Y] days of order → credit that campaign
ELSE → credit as "organic" or "direct"
```

### 5.3 Multi-Channel Logic
**When user interacts with multiple channels:**

[Describe how you handle this - e.g.:]
- Credit goes to last marketing touchpoint before purchase
- If both email and ad clicked same day, priority: [email > paid social > paid search]

---

## 6. Data Sources & Integration

### 6.1 Source Systems

| Source | Data Type | Integration Method | Refresh Frequency |
|--------|-----------|-------------------|-------------------|
| [Shopify] | Orders, customers, products | [API / Fivetran] | [Hourly / Daily] |
| [Stripe] | Payment transactions | [API / Fivetran] | [Hourly / Daily] |
| [Meta Ads] | Ad performance | [API / Custom script] | [Daily] |
| [Google Ads] | Ad performance | [API / Custom script] | [Daily] |
| [Klaviyo] | Email performance | [API / Fivetran] | [Daily] |
| [Website events] | User behavior | [Segment / Custom] | [Real-time] |

### 6.2 Data Flow

```
Source Systems → BigQuery Raw Tables → dbt Transformations → Production Tables → Lightdash Dashboards
```

---

## 7. Production Table Structure

### 7.1 Core Tables

**Schema: `[CLIENT_NAME]_production`**

| Table Name | Description | Primary Key | Grain |
|------------|-------------|-------------|-------|
| `dim_users` | User dimension | `user_id` | One row per user |
| `dim_products` | Product catalog | `product_id` | One row per product |
| `dim_campaigns` | Marketing campaigns | `campaign_id` | One row per campaign |
| `fact_orders` | Order transactions | `order_id` | One row per order |
| `fact_order_items` | Order line items | `order_item_id` | One row per line item |
| `fact_sessions` | Website sessions | `session_id` | One row per session |
| `fact_events` | Event stream | `event_id` | One row per event |

### 7.2 Aggregated Tables (for dashboard performance)

| Table Name | Description | Grain |
|------------|-------------|-------|
| `agg_daily_revenue` | Daily revenue rollup | One row per day |
| `agg_campaign_performance` | Campaign metrics | One row per campaign per day |
| `agg_product_performance` | Product metrics | One row per product per month |
| `agg_customer_cohorts` | Cohort analysis | One row per cohort per month |

---

## 8. Dashboard Structure

### 8.1 Dashboard Views

Based on the business questions in Section 1.2, we'll create [X] dashboard views:

#### **Dashboard 1: Executive Overview**
**Purpose:** Daily snapshot of business health

**Key metrics:**
- Revenue (today, MTD, vs. last month)
- Orders (count, AOV)
- New vs. returning customer split
- ROAS by channel
- Top products

**Filters:** Date range

---

#### **Dashboard 2: Marketing Attribution**
**Purpose:** Understand which channels drive profitable growth

**Key metrics:**
- Revenue by channel
- CAC by channel
- ROAS by channel
- LTV:CAC by acquisition channel
- Campaign performance comparison

**Filters:** Date range, channel, campaign

---

#### **Dashboard 3: [Custom Dashboard Name]**
**Purpose:** [Specific purpose]

**Key metrics:**
- [Metric 1]
- [Metric 2]

**Filters:** [Filters]

---

### 8.2 Visualization Guidelines
- **Trend charts:** Use line charts for time-series data
- **Comparison:** Use bar charts for comparing categories
- **Composition:** Use stacked bars or area charts for part-to-whole
- **Single metrics:** Use scorecards with comparison to prior period
- **Color palette:** [Define brand colors]
- **Date defaults:** Last 30 days, with comparison to previous 30 days

---

## 9. Data Quality & Validation

### 9.1 Validation Rules

**Orders validation:**
- `total_amount >= 0`
- `total_amount = subtotal + tax + shipping`
- `order_id` is unique
- `user_id` exists in users table

**Events validation:**
- Event names match taxonomy exactly
- Required properties are non-null
- Property types match specification

### 9.2 Reconciliation Targets

**Revenue reconciliation:**
- Bratrax dashboard revenue should match [Shopify/Stripe] within ±2%

**Order count reconciliation:**
- Bratrax order count should match source system exactly

---

## 10. Assumptions & Limitations

### 10.1 Known Limitations
- [e.g., "iOS 14+ attribution is limited due to Apple's privacy changes"]
- [e.g., "Historical data before [date] is incomplete"]
- [e.g., "Product cost data is estimated, not actual"]

### 10.2 Out of Scope
- [e.g., "Customer support ticket analysis"]
- [e.g., "Inventory forecasting"]

---

## 11. Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| [DATE] | 1.0 | Initial ontology | [YOUR_NAME] |

---

## Appendix A: Glossary

**First-time customer:** A user who has placed exactly one order (to date)

**Returning customer:** A user who has placed 2+ orders

**Active customer:** A customer who ordered in the last 90 days

**Session:** A period of website activity, timeout after 30 minutes of inactivity

**Attribution window:** The time period after an ad interaction during which an order can be credited to that ad

---

*End of Ontology Document*
