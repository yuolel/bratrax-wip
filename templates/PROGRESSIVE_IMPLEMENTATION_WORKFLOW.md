# Progressive Implementation Workflow - Quick Reference

**Default approach for Bratrax client projects**

---

## Timeline Overview

```
Week 1      Week 2         Week 3-4           Week 5+
-------     -------        --------           -------
Tier 1      Launch         Tier 2             Tier 3
Events      Dashboards     Events             (On-demand)
↓           ↓              ↓                  ↓
4-5 events  Validate       +6-8 events        +3-5 events
Implement   & Go-Live      Enhance            As requested
```

---

## Week 1: Tier 1 Implementation

### **Goal:** Get critical revenue events tracked

**Events to implement (4-5):**
1. `user_signed_up` - CAC calculation
2. `session_started` - Attribution & conversion rate
3. `order_completed` - Revenue tracking (MOST CRITICAL)
4. `email_clicked` - Email attribution

**Deliverables:**
- [ ] Tracking plan (Tier 1 only)
- [ ] Events implemented in codebase
- [ ] Events validated in analytics platform
- [ ] Raw data flowing to BigQuery

**QA Checklist:**
- [ ] All 4-5 events fire correctly
- [ ] Property names/types match specification
- [ ] `order_completed` includes all required order properties
- [ ] Revenue reconciliation ready (will check in Week 2)

---

## Week 2: Dashboard Launch

### **Goal:** Get client using dashboards, validate tracking

**Activities:**
1. **Build dbt models for Tier 1**
   - `fact_orders` table
   - `dim_users` table
   - `fact_sessions` table

2. **Revenue reconciliation** (CRITICAL)
   - Compare Bratrax revenue vs Shopify/Stripe
   - Must be ≤2% variance
   - Debug discrepancies before launch

3. **Build initial dashboards**
   - Executive Overview (revenue, orders, AOV, CAC)
   - Marketing Attribution (ROAS by channel)

4. **Launch & training**
   - Client walkthrough (30 min)
   - Record demo video
   - Set up daily email with key metrics

**Deliverables:**
- [ ] 2-3 dashboards live
- [ ] Revenue reconciliation passed
- [ ] Client trained on dashboards
- [ ] Client using dashboards daily

**Phase gate:** Client must use dashboards for 1 week before proceeding to Tier 2

---

## Week 3-4: Tier 2 Enhancement

### **Goal:** Add attribution detail and engagement metrics

**Trigger:** Client has used Tier 1 dashboards for 1+ week

**Before starting Tier 2, ask:**
> "What questions can't you answer with the current dashboard? What would you like to see added?"

**Events to consider (select 6-8 based on client feedback):**
- `product_viewed` - Product engagement
- `product_added_to_cart` - Cart funnel
- `cart_viewed` - Cart abandonment
- `checkout_started` - Checkout funnel
- `collection_viewed` - Category performance
- `search_initiated` - Search behavior
- `email_opened` - Email engagement
- `sms_clicked` - SMS attribution (if applicable)

**Don't add blindly - prioritize based on:**
1. Client's actual questions from Week 2
2. Dashboard usage patterns
3. Business priorities

**Deliverables:**
- [ ] Updated tracking plan (Tier 2 events)
- [ ] Tier 2 events implemented
- [ ] Enhanced dashboards
- [ ] Product/funnel analysis views

---

## Week 5+: Tier 3 On-Demand

### **Goal:** Only add advanced events when specifically needed

**Trigger:** Client explicitly requests functionality

**Common scenarios:**

| Client Request | Event to Add | Why |
|---------------|--------------|-----|
| "Need to track refunds" | `order_refunded` | Return rate analysis |
| "Want to analyze cart abandonment deeper" | `product_removed_from_cart` | Understand why users remove items |
| "Started collecting reviews" | `review_submitted` | Customer satisfaction tracking |
| "Launching subscription model" | `subscription_created`, `subscription_cancelled` | Subscription analytics |

**Process:**
1. Client makes specific request
2. Evaluate if existing events can answer the question
3. If not, add Tier 3 event
4. Update tracking plan, implement, update dashboards

**Don't add Tier 3 events proactively** - wait for client need.

---

## Phase Gates & Validation

### **Gate 1: Tier 1 → Tier 2**
Must complete before adding Tier 2:
- ✅ Tier 1 events validated
- ✅ Revenue reconciliation ≤2% variance
- ✅ Dashboards launched
- ✅ Client has used dashboards for 1+ week
- ✅ Client feedback collected

### **Gate 2: Tier 2 → Tier 3**
Must complete before adding Tier 3:
- ✅ Tier 2 events validated
- ✅ Enhanced dashboards live
- ✅ Client actively using dashboards
- ✅ Client explicitly requests Tier 3 functionality

---

## Benefits of Progressive Approach

### **Speed**
- Dashboard live in 2 weeks vs 4+ weeks
- Client sees ROI immediately
- Faster feedback loop

### **Risk Mitigation**
- Easier to debug 4-5 events vs 17-18
- Revenue reconciliation simpler
- Can fix Tier 1 issues before they propagate

### **Flexibility**
- Adjust Tier 2/3 based on actual usage
- Skip events client doesn't need
- Add events client specifically requests

### **Cost Efficiency**
- Lower initial BigQuery costs
- Avoid building unused features
- Spread implementation cost over time

---

## When NOT to Use Progressive

**Use all-at-once implementation if:**

1. **Subscription business model**
   - Tier 3 subscription events are critical, not optional
   - Need churn analysis from day 1

2. **Sophisticated client**
   - Has run analytics before
   - Knows exactly which events they need
   - Low risk of unused features

3. **Historical data critical**
   - Must analyze Tier 3 events retroactively
   - Can't backfill data later
   - Example: Need 12 months of review history

4. **Single implementation window**
   - Client's dev team only available for 1 deployment
   - Can't revisit codebase later

---

## Communication Templates

### **Pitch to Client (Progressive)**
> "We'll get your revenue and acquisition dashboards live in 2 weeks with 4-5 critical events. You'll see ROI immediately. Then we'll add more detail based on what you actually need, rather than guessing upfront. This gets you value faster and ensures we build features you'll use."

### **Pitch to Client (All-at-once)**
> "We'll implement all 17 events upfront, giving you a complete analytics system from day 1. This takes 3-4 weeks but ensures no data gaps. You'll wait longer, but get everything at once with no historical gaps."

### **Setting Expectations**
> "We use a progressive implementation approach. You'll have dashboards in 2 weeks, then we'll enhance based on your feedback. This is faster and more flexible than building everything upfront and discovering you don't need half of it."

---

## Example: DTC Skincare Client

### **Week 1-2: Tier 1**
**Implemented:**
- user_signed_up
- session_started
- order_completed
- email_clicked

**Dashboards launched:**
- Revenue trends
- CAC by channel
- Email attribution

**Client reaction:** "This is great! Can we see which products are driving revenue?"

### **Week 3-4: Tier 2**
**Added based on feedback:**
- product_viewed
- product_added_to_cart
- checkout_started

**Dashboards enhanced:**
- Product performance
- Conversion funnel

**Client reaction:** "Perfect. We're not using SMS yet, so we don't need that tracking."

**Result:** Skipped `sms_clicked` - saved implementation time

### **Week 6: Tier 3 (on-demand)**
**Client request:** "Our return rate is high, we need to track it."

**Added:**
- order_refunded

**Dashboard added:**
- Return rate by product

**Result:** Built exactly what client needs, when they need it

---

## Quick Decision Tree

```
Is client new to analytics?
├─ Yes → Use Progressive ✅
└─ No → Does client have subscription model?
    ├─ Yes → Consider All-at-once
    └─ No → Use Progressive ✅

Is fast time-to-value important?
├─ Yes → Use Progressive ✅
└─ No → Can you wait 4+ weeks?
    ├─ Yes → Consider All-at-once
    └─ No → Use Progressive ✅

Are client's needs unclear?
├─ Yes → Use Progressive ✅
└─ No → Use Progressive anyway (validate assumptions)
```

**Result: Use Progressive in 90% of cases**

---

## Resources

- **Ontology Template Section 3.3:** Implementation strategy details
- **Event Storming Guide Part 7:** How to choose approach with client
- **QA Checklist:** Phase validation requirements
- **README:** Full workflow documentation

---

*Progressive Implementation Workflow v1.0*
*Last updated: 2025-01-14*
