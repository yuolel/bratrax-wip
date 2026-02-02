# [CLIENT_NAME] Event Tracking Implementation Guide

**Version:** 1.0
**Date:** [DATE]
**Prepared by:** [YOUR_NAME]
**For:** Development Team

---

## 1. Overview

This guide provides exact specifications for implementing event tracking in [CLIENT_NAME]'s [website/app]. Every event documented here flows to BigQuery where it powers analytics dashboards and business metrics.

**Critical:** This is a technical specification. Event names, property names, and property types must be implemented **exactly as specified**. Even small deviations (typos, wrong types, extra nesting) will break downstream analytics.

---

## 2. Implementation Context

### 2.1 Tech Stack
- **Platform:** [Shopify / Custom / React app / etc.]
- **Tracking method:** [Segment / Google Tag Manager / Custom script]
- **Programming language:** [JavaScript / Python / etc.]
- **Analytics library:** [Segment Analytics.js 2.0 / etc.]

### 2.2 Before You Start

**Required reading:**
- [CLIENT_NAME] Analytics Ontology (defines what events mean)
- VidTao Implementation Guide (example implementation patterns)

**Prerequisites:**
- [ ] Analytics script is installed on all pages
- [ ] You have access to test in a development/staging environment
- [ ] You can view events in [Segment debugger / BigQuery console]

---

## 3. Global Implementation Rules

### 3.1 Event Naming Convention

**Format:** `{entity}_{activity}`

**Rules:**
1. All lowercase
2. Underscores only (no hyphens or spaces)
3. Past tense for activities (`viewed`, `created`, `completed`)
4. Be specific (`product_detail_viewed` not just `viewed`)

**Valid:** `product_added_to_cart`
**Invalid:** `Product_Added_To_Cart`, `product-added-to-cart`, `addToCart`

---

### 3.2 Property Naming Convention

**Rules:**
1. All lowercase with underscores
2. Use full words, not abbreviations (except common ones like `id`, `url`)
3. No nested objects (flat properties only)

**Valid:** `product_id`, `order_total`, `is_first_order`
**Invalid:** `productID`, `orderTotal`, `isFirstOrder`, `product.id`

---

### 3.3 Property Types

| Type | JavaScript | Example | Notes |
|------|------------|---------|-------|
| String | `'value'` | `product_name: 'Cleanser'` | Always use single or double quotes |
| Number | `123` or `45.67` | `quantity: 2`, `price: 25.99` | No quotes around numbers |
| Boolean | `true` / `false` | `is_first_order: true` | Lowercase, no quotes |
| ISO Date | `'2025-01-15T10:30:00Z'` | `order_date: '2025-01-15T10:30:00Z'` | ISO 8601 format in UTC |

**Common mistakes to avoid:**
- ❌ `quantity: '2'` (string instead of number)
- ❌ `is_first_order: 'true'` (string instead of boolean)
- ❌ `price: 25` (should be `25.00` for currency)

---

### 3.4 Required vs Optional Properties

- **Required properties MUST be present** in every event call
- **Optional properties** can be omitted if not available
- Never send `null` or `undefined` for optional properties—omit them entirely

---

## 4. Identity Management

### 4.1 User Identification Flow

**Anonymous visitor → Signs up/logs in → Identified user**

#### When user signs up or logs in:
```javascript
// Call identify() BEFORE any track() calls
analytics.identify('usr_12345', {
  email: 'customer@example.com',
  created_at: '2025-01-15T10:30:00Z'
});
```

#### When user logs out:
```javascript
analytics.reset();
```

**Critical:** Always call `identify()` before `track()` for logged-in users. This links their events to their user profile.

---

## 5. Event Specifications

Below are the exact events to implement, organized by user flow.

---

## 5.1 User Registration Events

### Event: `user_signed_up`

**When to fire:** User successfully creates an account

**Where to implement:** [Signup success callback / registration confirmation page]

**Properties:**

| Property | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| `user_id` | string | Yes | Unique user identifier | `usr_a3b4c5d6` |
| `email` | string | Yes | User's email address | `customer@example.com` |
| `signup_source` | string | Yes | Where signup happened | `homepage`, `checkout`, `popup` |
| `utm_source` | string | No | Marketing source (if present) | `facebook` |
| `utm_medium` | string | No | Marketing medium (if present) | `cpc` |
| `utm_campaign` | string | No | Campaign identifier (if present) | `spring_sale_2025` |

**Implementation example:**
```javascript
// After successful signup
analytics.identify(userId, {
  email: userEmail,
  created_at: new Date().toISOString()
});

analytics.track('user_signed_up', {
  user_id: userId,
  email: userEmail,
  signup_source: 'checkout',
  utm_source: sessionUTMSource || undefined,
  utm_campaign: sessionUTMCampaign || undefined
});
```

**Validation checklist:**
- [ ] Event name is exactly `user_signed_up`
- [ ] `user_id` and `email` are always present
- [ ] `signup_source` uses valid values only
- [ ] UTM parameters are captured from session (not invented)
- [ ] Event appears in Segment debugger with correct properties

---

### Event: `user_logged_in`

**When to fire:** User successfully logs into existing account

**Where to implement:** [Login success callback]

**Properties:**

| Property | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| `user_id` | string | Yes | User identifier | `usr_a3b4c5d6` |
| `login_method` | string | Yes | How they logged in | `email_password`, `social_google`, `social_facebook` |

**Implementation example:**
```javascript
analytics.identify(userId, {
  email: userEmail
});

analytics.track('user_logged_in', {
  user_id: userId,
  login_method: 'email_password'
});
```

---

## 5.2 Product Browsing Events

### Event: `product_viewed`

**When to fire:** User lands on a product detail page

**Where to implement:** [Product detail page load]

**Properties:**

| Property | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| `user_id` | string | No | User ID (if logged in) | `usr_a3b4c5d6` |
| `session_id` | string | Yes | Session identifier | `sess_x7y8z9` |
| `product_id` | string | Yes | Product identifier | `prod_789` |
| `product_name` | string | Yes | Product name | `Hydrating Cleanser` |
| `product_category` | string | Yes | Primary category | `Skincare` |
| `product_subcategory` | string | No | Subcategory | `Cleansers` |
| `price` | number | Yes | Current price | `25.00` |
| `currency` | string | Yes | Currency code | `USD` |
| `product_url` | string | No | Product page URL | `/products/hydrating-cleanser` |

**Implementation example:**
```javascript
// On product page load
analytics.track('product_viewed', {
  user_id: currentUserId || undefined,
  session_id: sessionId,
  product_id: product.id,
  product_name: product.name,
  product_category: product.category,
  price: parseFloat(product.price),
  currency: 'USD'
});
```

**Validation:**
- [ ] `price` is a number, not a string
- [ ] `user_id` is omitted (not null) if user not logged in

---

### Event: `product_added_to_cart`

**When to fire:** User clicks "Add to Cart" button and item is successfully added

**Where to implement:** [Add to cart success callback]

**Properties:**

| Property | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| `user_id` | string | No | User ID (if logged in) | `usr_a3b4c5d6` |
| `session_id` | string | Yes | Session identifier | `sess_x7y8z9` |
| `product_id` | string | Yes | Product identifier | `prod_789` |
| `product_name` | string | Yes | Product name | `Hydrating Cleanser` |
| `product_category` | string | Yes | Category | `Skincare` |
| `quantity` | number | Yes | Quantity added | `2` |
| `price` | number | Yes | Unit price | `25.00` |
| `currency` | string | Yes | Currency code | `USD` |

**Implementation example:**
```javascript
// After successful add to cart
analytics.track('product_added_to_cart', {
  session_id: sessionId,
  product_id: product.id,
  product_name: product.name,
  product_category: product.category,
  quantity: quantitySelected,
  price: parseFloat(product.price),
  currency: 'USD'
});
```

---

## 5.3 Checkout & Purchase Events

### Event: `checkout_started`

**When to fire:** User begins the checkout process (lands on first checkout page)

**Where to implement:** [Checkout page load or checkout button click]

**Properties:**

| Property | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| `user_id` | string | No | User ID (if logged in) | `usr_a3b4c5d6` |
| `session_id` | string | Yes | Session identifier | `sess_x7y8z9` |
| `cart_total` | number | Yes | Total cart value | `89.99` |
| `item_count` | number | Yes | Number of items in cart | `3` |
| `currency` | string | Yes | Currency code | `USD` |

**Implementation example:**
```javascript
analytics.track('checkout_started', {
  session_id: sessionId,
  cart_total: parseFloat(cart.total),
  item_count: cart.items.length,
  currency: 'USD'
});
```

---

### Event: `order_completed`

**When to fire:** Order is successfully placed and payment confirmed

**Where to implement:** [Order confirmation page / payment success webhook]

**This is the most critical event—it drives all revenue metrics.**

**Properties:**

| Property | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| `user_id` | string | Yes | Customer user ID | `usr_a3b4c5d6` |
| `session_id` | string | Yes | Session identifier | `sess_x7y8z9` |
| `order_id` | string | Yes | Unique order identifier | `ord_123456` |
| `order_number` | number | Yes | Sequential order # for this user | `1`, `2`, `3` |
| `total_amount` | number | Yes | Order total (gross) | `89.99` |
| `subtotal` | number | Yes | Pre-tax, pre-shipping | `75.00` |
| `discount_amount` | number | Yes | Total discounts (0 if none) | `10.00` |
| `shipping_amount` | number | Yes | Shipping cost | `8.99` |
| `tax_amount` | number | Yes | Tax amount | `6.00` |
| `currency` | string | Yes | Currency code | `USD` |
| `is_first_order` | boolean | Yes | Is this their first order? | `true` / `false` |
| `payment_method` | string | Yes | Payment method used | `credit_card`, `paypal`, `apple_pay` |
| `products` | array | Yes | List of products purchased | See below |

**Products array structure:**
Each item in the `products` array should be an object with:
```javascript
{
  product_id: 'prod_789',
  product_name: 'Hydrating Cleanser',
  product_category: 'Skincare',
  quantity: 2,
  price: 25.00
}
```

**Implementation example:**
```javascript
analytics.track('order_completed', {
  user_id: order.userId,
  session_id: sessionId,
  order_id: order.id,
  order_number: userOrderCount, // Calculate: how many orders has this user placed?
  total_amount: parseFloat(order.total),
  subtotal: parseFloat(order.subtotal),
  discount_amount: parseFloat(order.discount || 0),
  shipping_amount: parseFloat(order.shipping),
  tax_amount: parseFloat(order.tax),
  currency: 'USD',
  is_first_order: userOrderCount === 1,
  payment_method: order.paymentMethod,
  products: order.items.map(item => ({
    product_id: item.productId,
    product_name: item.name,
    product_category: item.category,
    quantity: item.quantity,
    price: parseFloat(item.price)
  }))
});
```

**Validation checklist:**
- [ ] `total_amount = subtotal + shipping + tax - discount` (verify math)
- [ ] `is_first_order` logic is correct (check user's order history)
- [ ] All amounts are numbers, not strings
- [ ] `products` array includes all items in order
- [ ] Event fires exactly once per order (not on page refresh)

---

## 5.4 Marketing Events (Email)

### Event: `email_opened`

**When to fire:** User opens a marketing email

**Where to implement:** [Email service provider webhook - Klaviyo/etc.]

**Properties:**

| Property | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| `user_id` | string | Yes | User identifier | `usr_a3b4c5d6` |
| `email_id` | string | Yes | Email identifier | `email_campaign_123` |
| `email_subject` | string | Yes | Email subject line | `20% Off Spring Sale` |
| `campaign_name` | string | Yes | Campaign name | `spring_sale_email` |

**Note:** This is typically implemented via server-side webhook, not client-side JavaScript.

---

### Event: `email_clicked`

**When to fire:** User clicks a link in an email

**Where to implement:** [Email service provider webhook OR UTM capture on landing]

**Properties:**

| Property | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| `user_id` | string | Yes | User identifier | `usr_a3b4c5d6` |
| `email_id` | string | Yes | Email identifier | `email_campaign_123` |
| `campaign_name` | string | Yes | Campaign name | `spring_sale_email` |
| `link_url` | string | Yes | URL clicked | `https://site.com/products/cleanser` |

---

## 6. Session & UTM Parameter Handling

### 6.1 Session Management

**Session definition:** A period of activity, expires after 30 minutes of inactivity

**Session ID generation:**
- Generate a unique session ID when user first lands
- Store in session storage (not local storage)
- Regenerate if expired

**Implementation:**
```javascript
function getOrCreateSessionId() {
  const SESSION_TIMEOUT = 30 * 60 * 1000; // 30 minutes
  const stored = sessionStorage.getItem('bratrax_session');

  if (stored) {
    const { sessionId, timestamp } = JSON.parse(stored);
    if (Date.now() - timestamp < SESSION_TIMEOUT) {
      return sessionId;
    }
  }

  // Create new session
  const newSessionId = 'sess_' + Date.now() + '_' + Math.random().toString(36);
  sessionStorage.setItem('bratrax_session', JSON.stringify({
    sessionId: newSessionId,
    timestamp: Date.now()
  }));

  return newSessionId;
}
```

---

### 6.2 UTM Parameter Capture

**Capture UTM parameters at session start:**
- Read from URL query string on landing
- Store in session storage
- Include in relevant events throughout session

**Parameters to capture:**
- `utm_source`
- `utm_medium`
- `utm_campaign`
- `utm_content` (optional)
- `utm_term` (optional)

**Implementation:**
```javascript
function captureUTMParameters() {
  const params = new URLSearchParams(window.location.search);
  const utmData = {
    utm_source: params.get('utm_source'),
    utm_medium: params.get('utm_medium'),
    utm_campaign: params.get('utm_campaign'),
    utm_content: params.get('utm_content'),
    utm_term: params.get('utm_term')
  };

  // Only store if at least one UTM parameter present
  if (Object.values(utmData).some(v => v !== null)) {
    sessionStorage.setItem('bratrax_utm', JSON.stringify(utmData));
  }
}

function getSessionUTM() {
  const stored = sessionStorage.getItem('bratrax_utm');
  return stored ? JSON.parse(stored) : {};
}
```

---

## 7. Testing & Validation

### 7.1 Development Testing

**Enable debug mode:**
```javascript
analytics.debug(true); // Logs all events to console
```

**Test checklist for each event:**
1. Trigger the event in your dev environment
2. Check browser console for debug output
3. Verify event name is exact (copy-paste from this doc)
4. Verify all required properties are present
5. Verify property names are exact
6. Verify property types are correct (number vs string vs boolean)
7. Verify no nested objects

---

### 7.2 Staging Validation

**Use [Segment Debugger / BigQuery Console] to validate:**

1. Event appears in the stream
2. Event name matches specification exactly
3. All required properties present
4. No extra/unexpected properties
5. Property types are correct
6. Values make sense (prices are reasonable, IDs are not null, etc.)

**SQL validation query example:**
```sql
-- Check order_completed events from last hour
SELECT
  event_timestamp,
  user_id,
  order_id,
  total_amount,
  is_first_order
FROM `project.dataset.events`
WHERE event_name = 'order_completed'
  AND event_timestamp > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 HOUR)
ORDER BY event_timestamp DESC
LIMIT 10;
```

---

### 7.3 Production Smoke Test

**After deploying to production:**

1. **Manual test:** Complete a full user flow yourself
   - Sign up
   - View products
   - Add to cart
   - Complete checkout

2. **Verify events in analytics platform** within 5 minutes

3. **Validate revenue reconciliation**
   - Compare total revenue in Bratrax dashboard vs. [Shopify/Stripe]
   - Should match within ±2% after 24 hours

---

## 8. Common Implementation Mistakes

### ❌ Mistake 1: Typos in Event Names
```javascript
// WRONG
analytics.track('order_complete', {...}); // Missing 'd'

// CORRECT
analytics.track('order_completed', {...});
```

### ❌ Mistake 2: Wrong Property Types
```javascript
// WRONG
{ quantity: '2', price: '25.00' }

// CORRECT
{ quantity: 2, price: 25.00 }
```

### ❌ Mistake 3: Nested Objects
```javascript
// WRONG
{ product: { id: 'prod_123', name: 'Cleanser' } }

// CORRECT
{ product_id: 'prod_123', product_name: 'Cleanser' }
```

### ❌ Mistake 4: Sending null for Optional Properties
```javascript
// WRONG
{ user_id: null } // Don't send null

// CORRECT
{ } // Omit the property entirely
```

### ❌ Mistake 5: Not Calling identify() Before track()
```javascript
// WRONG - track() before identify()
analytics.track('order_completed', {...});

// CORRECT
analytics.identify(userId, { email: userEmail });
analytics.track('order_completed', {...});
```

---

## 9. Rollback Plan

**If events are broken in production:**

1. **Immediate:** Roll back the deployment
2. **Identify issue:** Check error logs and Segment debugger
3. **Fix in dev/staging:** Don't fix in production directly
4. **Re-validate:** Complete full testing checklist
5. **Redeploy**

**Contact:** [YOUR_EMAIL] immediately if production tracking breaks

---

## 10. Event Summary Table

Quick reference of all events:

| Event Name | When | Where | Critical? |
|------------|------|-------|-----------|
| `user_signed_up` | Account created | Signup success | High |
| `user_logged_in` | User logs in | Login success | Medium |
| `product_viewed` | Product page viewed | PDP load | Medium |
| `product_added_to_cart` | Add to cart clicked | ATC success | High |
| `checkout_started` | Checkout begins | Checkout page | High |
| `order_completed` | Order placed | Order confirm | **CRITICAL** |
| `email_opened` | Email opened | ESP webhook | Low |
| `email_clicked` | Email link clicked | ESP webhook | Medium |

---

## 11. Questions & Support

**Technical questions:** [DEVELOPER_SLACK_CHANNEL or EMAIL]

**Analytics questions:** [YOUR_EMAIL]

**Validation queries not working?** Ping [DATA_ENGINEER_NAME]

---

## Appendix: Platform-Specific Notes

### [If Shopify]
- Use Shopify's `checkout.liquid` for order_completed event
- Capture order data from `{{ order }}` Liquid object
- Fire event on thank-you page only (not on page refresh)

### [If React/SPA]
- Don't fire `product_viewed` on component mount in all cases
- Use `useEffect` with proper dependencies
- Ensure events fire only once per actual user action

### [If using Segment]
- Segment Source: [SOURCE_NAME]
- Destinations enabled: BigQuery
- Verify in Segment Debugger before checking BigQuery

---

*Last updated: [DATE]*
*Version: 1.0*
*Questions? Contact [YOUR_EMAIL]*
