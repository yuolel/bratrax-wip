# Bratrax QA & Validation Checklist

**Client:** [CLIENT_NAME]
**Project Phase:** [Discovery / Tracking / Pipeline / Dashboard]
**Date:** [DATE]
**QA Engineer:** [NAME]

---

## Purpose

This checklist ensures data quality and accuracy at each phase of the Bratrax implementation. Complete relevant sections based on current project phase.

**Sign-off required:** All "Critical" items must pass before advancing to next phase.

---

## Phase 1: Discovery & Ontology Validation

### Discovery Documentation ✓
- [ ] Discovery questionnaire completed by client
- [ ] Tech stack audit complete (all tools identified)
- [ ] API access confirmed for all data sources
- [ ] Key business questions documented (3-5 minimum)
- [ ] Top metrics identified and ranked
- [ ] Decision-makers and dashboard users identified
- [ ] Current reporting pain points documented

### Ontology Quality ✓
- [ ] All entities have clear definitions
- [ ] Entity relationships mapped and logical
- [ ] Event names follow `entity_activity` convention
- [ ] All events include required properties
- [ ] Property types specified for all properties
- [ ] No nested objects in event properties
- [ ] Metric calculations have clear formulas
- [ ] Attribution model defined and appropriate for business
- [ ] Attribution window specified
- [ ] All metrics tied to business questions

### Ontology Completeness ✓
- [ ] Can answer all client's key business questions with defined metrics
- [ ] No redundant or duplicate events
- [ ] Event count is reasonable (typically 12-20 core events)
- [ ] Data source for each entity identified
- [ ] Client has reviewed and approved ontology

**Critical blocker:** Cannot proceed to tracking implementation without approved ontology

---

## Phase 2: Tracking Implementation Validation

### Pre-Implementation ✓
- [ ] Tracking plan document created from ontology
- [ ] Platform-specific implementation notes added
- [ ] Development environment access confirmed
- [ ] Segment/analytics tool configured
- [ ] Debug mode enabled for testing

### Code Review ✓
For each event implementation:
- [ ] Event name matches tracking plan exactly (case-sensitive)
- [ ] All required properties implemented
- [ ] Property names match tracking plan exactly
- [ ] Property types correct (number vs string vs boolean)
- [ ] No nested objects in properties
- [ ] Optional properties omitted (not null) when not available
- [ ] `identify()` called before `track()` for logged-in users
- [ ] Events fire exactly once per user action (no duplicates on refresh)

### Event-Specific Validation

#### `user_signed_up` ✓
- [ ] Fires on successful account creation
- [ ] Includes `user_id` and `email`
- [ ] Captures UTM parameters if present
- [ ] Does not fire on page refresh

#### `order_completed` ✓ **CRITICAL**
- [ ] Fires exactly once per order
- [ ] `order_id` is unique
- [ ] Math is correct: `total = subtotal + tax + shipping - discount`
- [ ] `is_first_order` logic validated
- [ ] `order_number` is correct sequential count
- [ ] All amounts are numbers (not strings)
- [ ] Products array includes all items
- [ ] Products array objects are flat (not nested)

#### `product_added_to_cart` ✓
- [ ] Fires on successful add to cart
- [ ] Quantity matches user selection
- [ ] Price is unit price (not total)

*(Add checklist items for other events as needed)*

---

## Phase 3: Data Pipeline Validation

### Raw Data Ingestion ✓
For each data source:

**Source: [SOURCE_NAME]**
- [ ] API connection successful
- [ ] Credentials valid and not expiring soon
- [ ] Data is arriving in BigQuery raw tables
- [ ] Schema matches expected structure
- [ ] No critical fields are null
- [ ] Data freshness is acceptable (within SLA)
- [ ] Historical data backfill complete (if applicable)

**Repeat for each source:**
- [ ] [Shopify / Stripe / Meta Ads / Google Ads / Klaviyo / etc.]

### Event Data Quality ✓
**Query raw event table:**
```sql
SELECT
  event_name,
  COUNT(*) as event_count,
  COUNT(DISTINCT user_id) as unique_users
FROM `project.dataset.events`
WHERE event_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAYS)
GROUP BY event_name
ORDER BY event_count DESC;
```

- [ ] All expected events are present
- [ ] Event volumes are reasonable (no suspicious spikes or drops)
- [ ] No unexpected event names (typos)
- [ ] User IDs are present where expected

**Check for common data quality issues:**
```sql
-- Check for null required properties in order_completed
SELECT
  COUNT(*) as null_order_id_count
FROM `project.dataset.events`
WHERE event_name = 'order_completed'
  AND order_id IS NULL
  AND event_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAYS);
```
- [ ] Result should be 0

```sql
-- Check for string prices (should be numeric)
SELECT
  event_name,
  JSON_EXTRACT(event_properties, '$.price') as price_value
FROM `project.dataset.events`
WHERE event_name IN ('product_viewed', 'product_added_to_cart')
  AND event_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 DAY)
LIMIT 10;
```
- [ ] Prices are numeric, not strings in quotes

### dbt Transformation Validation ✓

**Models run successfully:**
- [ ] All dbt models compile without errors
- [ ] All models run without errors
- [ ] Execution time is reasonable (<10 min for full refresh)
- [ ] All dbt tests pass (schema tests, data tests)

**Production tables exist:**
- [ ] `dim_users` table created
- [ ] `dim_products` table created
- [ ] `fact_orders` table created
- [ ] `fact_order_items` table created
- [ ] `fact_sessions` table created
- [ ] [Other tables per ontology]

**Row count validation:**
```sql
-- Compare raw vs production table row counts
SELECT
  'raw_orders' as table_name,
  COUNT(*) as row_count
FROM `project.dataset.raw_orders`
UNION ALL
SELECT
  'fact_orders',
  COUNT(*)
FROM `project.dataset.fact_orders`;
```
- [ ] Row counts are similar (allowing for deduplication logic)
- [ ] Production table is not empty

**Data quality checks:**
```sql
-- Check for duplicate orders in fact_orders
SELECT
  order_id,
  COUNT(*) as duplicate_count
FROM `project.dataset.fact_orders`
GROUP BY order_id
HAVING COUNT(*) > 1;
```
- [ ] Result should be empty (no duplicates)

```sql
-- Validate order totals math
SELECT
  order_id,
  total_amount,
  subtotal,
  tax_amount,
  shipping_amount,
  discount_amount,
  (subtotal + tax_amount + shipping_amount - discount_amount) as calculated_total,
  ABS(total_amount - (subtotal + tax_amount + shipping_amount - discount_amount)) as difference
FROM `project.dataset.fact_orders`
WHERE ABS(total_amount - (subtotal + tax_amount + shipping_amount - discount_amount)) > 0.01
LIMIT 10;
```
- [ ] Result should be empty (all math correct within $0.01)

**User entity validation:**
```sql
-- Check that user first_order_at matches earliest order
SELECT
  u.user_id,
  u.first_order_at,
  MIN(o.created_at) as actual_first_order
FROM `project.dataset.dim_users` u
JOIN `project.dataset.fact_orders` o ON u.user_id = o.user_id
GROUP BY u.user_id, u.first_order_at
HAVING u.first_order_at != MIN(o.created_at);
```
- [ ] Result should be empty

---

## Phase 4: Metric Reconciliation

### Revenue Reconciliation ✓ **CRITICAL**

**Compare Bratrax vs Source System:**

```sql
-- Bratrax total revenue (last 30 days)
SELECT
  SUM(total_amount) as bratrax_revenue
FROM `project.dataset.fact_orders`
WHERE created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY);
```

**Source system revenue:** $_______ (from Shopify/Stripe report)
**Bratrax revenue:** $_______
**Difference:** _______
**% Difference:** _______

- [ ] Difference is ≤ 2%
- [ ] If > 2%, root cause identified and documented

**Known acceptable discrepancies:**
- [ ] Refunds not yet implemented (note value: $______)
- [ ] Canceled orders included/excluded differently
- [ ] [Other documented reason]

### Order Count Reconciliation ✓

**Source system order count:** _______
**Bratrax order count:** _______
**Difference:** _______

- [ ] Counts match exactly OR discrepancy explained

### Metric Spot Checks ✓

**Average Order Value (AOV):**
```sql
SELECT
  SUM(total_amount) / COUNT(DISTINCT order_id) as aov
FROM `project.dataset.fact_orders`
WHERE created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY);
```
**Result:** $_______
**Expected range:** $_______ - $_______
- [ ] Within expected range

**New vs Returning Customer Split:**
```sql
SELECT
  is_first_order,
  COUNT(*) as order_count,
  ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 1) as percentage
FROM `project.dataset.fact_orders`
WHERE created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
GROUP BY is_first_order;
```
**New customer %:** _______%
**Returning customer %:** _______%
- [ ] Percentages match client's expectation

### Attribution Validation ✓

**Check attribution is working:**
```sql
SELECT
  attribution_source,
  COUNT(*) as order_count,
  SUM(total_amount) as revenue
FROM `project.dataset.fact_orders`
WHERE created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
GROUP BY attribution_source
ORDER BY order_count DESC;
```
- [ ] Attribution sources are populated (not all NULL or 'direct')
- [ ] Distribution looks reasonable
- [ ] Known campaigns appear in results

---

## Phase 5: Dashboard Validation

### Visual Quality ✓
For each dashboard view:
- [ ] Charts render correctly (no errors)
- [ ] Chart types are appropriate for data (line for trends, bar for comparison, etc.)
- [ ] Colors are distinguishable and on-brand
- [ ] Axis labels are clear
- [ ] Numbers are formatted correctly (currency, percentages, etc.)
- [ ] Date ranges display correctly
- [ ] No overlapping text or truncated labels

### Interactivity ✓
- [ ] Filters work correctly
- [ ] Filter selections update all relevant charts
- [ ] Date range selector works
- [ ] Drill-down functionality works (if applicable)
- [ ] Dashboard loads in <5 seconds
- [ ] Mobile view is readable (if required)

### Data Accuracy ✓
For each key metric:
- [ ] Metric value matches SQL query result
- [ ] Comparison to previous period is correct
- [ ] Trend direction is correct (up/down)
- [ ] Percentages add up to 100% (where applicable)

**Spot check: Executive Overview Dashboard**
- [ ] Today's revenue matches BigQuery query
- [ ] MTD revenue matches BigQuery query
- [ ] Order count matches BigQuery query
- [ ] AOV = Revenue / Orders (math is correct)

### User Acceptance Testing ✓
- [ ] Client has viewed dashboards
- [ ] Client confirms numbers "feel right"
- [ ] Client can answer their key business questions
- [ ] Client understands how to use filters
- [ ] Client knows how to interpret each chart
- [ ] Client feedback incorporated

---

## Phase 6: Monitoring & Alerts

### Pipeline Monitoring ✓
- [ ] Data freshness alerts configured
- [ ] Alert thresholds set appropriately
- [ ] Alert notification channels configured (email/Slack)
- [ ] Test alert sent and received

**Alerts configured for:**
- [ ] Data source API failures
- [ ] BigQuery load job failures
- [ ] dbt model failures
- [ ] Data freshness SLA violations (>24 hours old)
- [ ] Unusual data volumes (>50% drop or >200% spike)

### Documentation ✓
- [ ] Runbook created for common issues
- [ ] Escalation contacts documented
- [ ] Client has access to support channel
- [ ] Handoff document created (if applicable)

---

## Phase 7: Go-Live Checklist

### Pre-Launch ✓
- [ ] All previous phase validations passed
- [ ] Revenue reconciliation ≤2% difference
- [ ] Client approval received
- [ ] Training session completed
- [ ] User guide provided
- [ ] Access credentials shared with all users

### Launch Day ✓
- [ ] Dashboard access confirmed for all users
- [ ] Client confirms they can log in
- [ ] Test a full data refresh
- [ ] Verify dashboards update with new data
- [ ] Send launch announcement email

### Post-Launch (Day 1-7) ✓
- [ ] Day 1: Check data freshness
- [ ] Day 1: Verify no alert fires
- [ ] Day 3: Follow up with client on usage
- [ ] Day 7: Review dashboard usage analytics
- [ ] Day 7: Collect initial feedback
- [ ] Day 7: Address any issues identified

---

## Known Issues & Risks Log

Document any issues that are known but accepted:

| Issue | Severity | Workaround | Resolution Plan |
|-------|----------|------------|-----------------|
| [Description] | High/Med/Low | [Temporary fix] | [Plan to fix permanently] |
| Example: iOS 14 attribution limited | Medium | Track overall channel, not device-level | Not fixable due to Apple privacy policy |

---

## Sign-Off

**Phase:** [PHASE_NAME]

**Status:** ✅ Pass / ⚠️ Pass with caveats / ❌ Fail

**QA Engineer:** _______________ Date: _______

**Project Lead:** _______________ Date: _______

**Client Approval:** _______________ Date: _______ *(for go-live only)*

**Notes:**

---

*Last updated: [DATE]*
*Bratrax QA Checklist v1.0*
