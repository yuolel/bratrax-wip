# [CLIENT_NAME] Event Tracking Implementation Guide

**Version:** 1.0
**Date:** [DATE]
**Business Model:** SaaS
**Prepared by:** [YOUR_NAME]
**For:** Development Team

---

## 1. Overview

This guide explains how to implement event tracking in [CLIENT_NAME]'s SaaS product using Segment Analytics 2.0. Every event flows to BigQuery where it powers SaaS metrics like MRR, churn rate, and activation rate.

**Critical:** Event names, property names, and property types must be implemented **exactly as specified**. Deviations break downstream analytics.

---

## 2. Implementation Context

### 2.1 Tech Stack
- **Application:** [React / Vue / Rails / Django / etc.]
- **Tracking method:** [Segment / Mixpanel / Custom]
- **Backend language:** [Node.js / Python / Ruby / etc.]
- **Analytics library:** Segment Analytics.js 2.0

### 2.2 Client-Side vs Server-Side

| Location | When to Use | Example Events |
|----------|-------------|----------------|
| **Client-Side** | User interactions in browser/app | `search_initiated`, `feature_used` |
| **Server-Side** | Data changes, payments, critical events | `user_created`, `subscription_created`, `subscription_cancelled` |

**Rule of thumb:**
- Payment/subscription events → Server-side (more reliable)
- UI interactions → Client-side
- Critical business events (activation, churn) → Server-side

---

## 3. Event Naming Convention

**Format: {entity}_{activity}**

**Rules:**
1. All lowercase
2. Underscores only (no hyphens)
3. Past tense (`created`, `activated`, `cancelled`)
4. Be specific (`user_onboarding_completed` not just `completed`)

**Valid:** `subscription_created`
**Invalid:** `Subscription_Created`, `subscription-created`, `createSubscription`

---

## 4. Identity Management

### 4.1 User Lifecycle

Anonymous → Signs Up → Identified User → Subscribes → Churns

### 4.2 When User Signs Up

```javascript
// After successful signup
analytics.identify(userId, {
  email: user.email,
  created_at: user.createdAt,
  plan_tier: 'free'  // or 'trial'
});

analytics.track('user_created', {
  user_id: userId,
  email: user.email,
  signup_source: 'homepage',
  utm_source: sessionUTM.source,
  utm_campaign: sessionUTM.campaign
});
```

### 4.3 When User Logs Out

```javascript
analytics.reset();
```

**⚠️ IMPORTANT:** Always call `identify()` before `track()` for logged-in users.

---

## 5. The Core Events

Organized by tier for progressive implementation.

---

## **TIER 1 EVENTS (Week 1 - Critical)**

### Event: `user_created`

**When to fire:** User completes account registration

**Where to implement:** Server-side (signup endpoint)

**Properties:**

| Property | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| `user_id` | string | Yes | Unique user identifier | `usr_a3b4c5d6` |
| `email` | string | Yes | User's email | `user@example.com` |
| `signup_source` | string | Yes | Where signup happened | `homepage`, `pricing_page`, `referral` |
| `utm_source` | string | No | Marketing source | `google_ads` |
| `utm_medium` | string | No | Marketing medium | `cpc` |
| `utm_campaign` | string | No | Campaign name | `q1_product_launch` |
| `user_role` | string | No | Initial role | `admin`, `member` |

**Server-side implementation (Node.js example):**
```javascript
// After user saved to database
await analytics.track({
  userId: user.id,
  event: 'user_created',
  properties: {
    user_id: user.id,
    email: user.email,
    signup_source: req.body.source || 'direct',
    utm_source: session.utmSource,
    utm_campaign: session.utmCampaign,
    user_role: user.role
  },
  timestamp: new Date()
});
```

---

### Event: `user_activated`

**When to fire:** User completes activation milestone

**Activation milestone for [CLIENT_NAME]:** [DEFINE SPECIFIC MILESTONE]
- Example: User completes onboarding AND creates first project
- Example: User invites team member AND uses core feature

**Where to implement:** Server-side (when activation condition met)

**Properties:**

| Property | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| `user_id` | string | Yes | User identifier | `usr_a3b4c5d6` |
| `activation_milestone` | string | Yes | What milestone was reached | `onboarding_completed`, `first_project_created` |
| `days_to_activate` | integer | Yes | Days from signup to activation | `2` |

**Implementation logic:**
```javascript
// Pseudo-code for activation detection
async function checkActivation(userId) {
  const user = await getUser(userId);
  const hasCompletedOnboarding = await checkOnboarding(userId);
  const hasCreatedProject = await checkFirstProject(userId);

  if (hasCompletedOnboarding && hasCreatedProject && !user.isActivated) {
    const daysToActivate = daysSince(user.createdAt);

    await analytics.track({
      userId: userId,
      event: 'user_activated',
      properties: {
        user_id: userId,
        activation_milestone: 'onboarding_and_first_project',
        days_to_activate: daysToActivate
      }
    });

    // Mark user as activated in database
    await markUserActivated(userId);
  }
}
```

---

### Event: `subscription_trial_started`

**When to fire:** User begins free trial

**Where to implement:** Server-side (trial creation endpoint)

**Properties:**

| Property | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| `user_id` | string | Yes | User identifier | `usr_a3b4c5d6` |
| `subscription_id` | string | Yes | Subscription identifier | `sub_999` |
| `plan_name` | string | Yes | Plan name | `Pro - 14 Day Trial` |
| `trial_duration_days` | integer | Yes | Trial length | `14` |
| `trial_end_date` | timestamp | Yes | When trial expires | `2025-01-29T10:30:00Z` |

**Implementation:**
```javascript
// When trial created
analytics.track({
  userId: user.id,
  event: 'subscription_trial_started',
  properties: {
    user_id: user.id,
    subscription_id: subscription.id,
    plan_name: subscription.planName,
    trial_duration_days: 14,
    trial_end_date: subscription.trialEndsAt.toISOString()
  }
});
```

---

### Event: `subscription_created` ⭐ **MOST CRITICAL**

**When to fire:** User becomes a paying customer (first successful payment)

**Where to implement:** Server-side (Stripe webhook or payment success handler)

**Properties:**

| Property | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| `user_id` | string | Yes | User identifier | `usr_a3b4c5d6` |
| `subscription_id` | string | Yes | Subscription identifier | `sub_999` |
| `plan_name` | string | Yes | Plan name | `Pro Monthly` |
| `plan_tier` | string | Yes | Plan tier | `pro` |
| `billing_frequency` | string | Yes | Billing cycle | `monthly`, `annual` |
| `price` | decimal | Yes | Subscription price | `99.00` |
| `currency` | string | Yes | Currency code | `USD` |
| `is_trial_conversion` | boolean | Yes | Did they convert from trial? | `true` / `false` |
| `payment_method` | string | Yes | Payment method | `credit_card`, `paypal` |

**Implementation (Stripe webhook example):**
```javascript
// Stripe webhook handler
stripe.webhooks.on('customer.subscription.created', async (event) => {
  const subscription = event.data.object;
  const user = await getUserByStripeId(subscription.customer);

  const hadTrial = subscription.status === 'active' && subscription.trial_end;

  analytics.track({
    userId: user.id,
    event: 'subscription_created',
    properties: {
      user_id: user.id,
      subscription_id: subscription.id,
      plan_name: subscription.items.data[0].plan.nickname,
      plan_tier: getPlanTier(subscription.items.data[0].plan.id),
      billing_frequency: subscription.items.data[0].plan.interval,
      price: parseFloat(subscription.items.data[0].plan.amount / 100),
      currency: subscription.currency.toUpperCase(),
      is_trial_conversion: hadTrial,
      payment_method: subscription.default_payment_method?.type || 'credit_card'
    }
  });
});
```

---

### Event: `subscription_cancelled`

**When to fire:** User cancels their subscription

**Where to implement:** Server-side (cancellation endpoint or Stripe webhook)

**Properties:**

| Property | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| `user_id` | string | Yes | User identifier | `usr_a3b4c5d6` |
| `subscription_id` | string | Yes | Subscription identifier | `sub_999` |
| `cancellation_reason` | string | No | Why they cancelled | `too_expensive`, `not_using_enough`, `missing_features` |
| `months_subscribed` | integer | Yes | Total months subscribed | `6` |
| `plan_tier` | string | Yes | Plan they were on | `pro` |
| `churned_mrr` | decimal | Yes | MRR lost | `99.00` |

**Implementation:**
```javascript
// When user cancels
analytics.track({
  userId: user.id,
  event: 'subscription_cancelled',
  properties: {
    user_id: user.id,
    subscription_id: subscription.id,
    cancellation_reason: cancellationForm.reason, // from user input
    months_subscribed: monthsBetween(subscription.createdAt, Date.now()),
    plan_tier: subscription.planTier,
    churned_mrr: parseFloat(subscription.monthlyPrice)
  }
});
```

---

**End of Tier 1 (5-6 events)**

---

## **TIER 2 EVENTS (Week 3-4 - Engagement)**

### Event: `user_onboarding_completed`

**When to fire:** User finishes onboarding/tutorial

**Where to implement:** Client-side (last onboarding step) or Server-side

**Properties:**

| Property | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| `user_id` | string | Yes | User identifier | `usr_a3b4c5d6` |
| `onboarding_steps_completed` | integer | Yes | Steps completed | `5` |
| `onboarding_duration_minutes` | integer | Yes | Time to complete | `12` |

**Client-side implementation:**
```javascript
// On last onboarding step completion
const onboardingStartTime = sessionStorage.getItem('onboarding_start');
const duration = Math.round((Date.now() - onboardingStartTime) / 60000);

analytics.track('user_onboarding_completed', {
  user_id: currentUser.id,
  onboarding_steps_completed: 5,
  onboarding_duration_minutes: duration
});
```

---

### Event: `search_initiated`

**When to fire:** User performs a search (if search is core feature)

**Where to implement:** Client-side (search submit)

**Properties:**

| Property | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| `user_id` | string | Yes | User identifier | `usr_a3b4c5d6` |
| `session_id` | string | Yes | Session identifier | `sess_x7y8z9` |
| `search_term` | string | Yes | What they searched | `fitness supplements` |
| `search_results_count` | integer | Yes | Number of results | `1523` |
| `filters_applied` | string | No | Filters used | `category:health,date:30d` |

**Implementation:**
```javascript
// On search submit
analytics.track('search_initiated', {
  user_id: currentUser.id,
  session_id: getSessionId(),
  search_term: searchInput.value,
  search_results_count: results.length,
  filters_applied: getActiveFilters().join(',')
});
```

---

### Event: `feature_used`

**When to fire:** User interacts with a key product feature

**Where to implement:** Client-side or Server-side depending on feature

**Properties:**

| Property | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| `user_id` | string | Yes | User identifier | `usr_a3b4c5d6` |
| `session_id` | string | Yes | Session identifier | `sess_x7y8z9` |
| `feature_name` | string | Yes | Feature used | `ad_saved`, `report_generated`, `export_created` |
| `feature_category` | string | No | Feature type | `core`, `premium`, `export` |

**Implementation:**
```javascript
// When user uses feature
function trackFeatureUsage(featureName, category = null) {
  analytics.track('feature_used', {
    user_id: currentUser.id,
    session_id: getSessionId(),
    feature_name: featureName,
    feature_category: category
  });
}

// Example usage
saveButton.onClick(() => {
  trackFeatureUsage('ad_saved', 'core');
  // ... save logic
});
```

---

### Event: `team_member_invited`

**When to fire:** User invites someone to their account

**Where to implement:** Server-side (invitation creation)

**Properties:**

| Property | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| `user_id` | string | Yes | Inviter user ID | `usr_a3b4c5d6` |
| `account_id` | string | No | Account ID (B2B) | `acc_xyz123` |
| `invited_email` | string | Yes | Invitee email | `teammate@example.com` |
| `role_assigned` | string | Yes | Role given | `admin`, `member`, `viewer` |

---

### Event: `subscription_renewed`

**When to fire:** Subscription successfully renews

**Where to implement:** Server-side (Stripe webhook)

**Properties:**

| Property | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| `user_id` | string | Yes | User identifier | `usr_a3b4c5d6` |
| `subscription_id` | string | Yes | Subscription ID | `sub_999` |
| `plan_tier` | string | Yes | Plan tier | `pro` |
| `renewal_amount` | decimal | Yes | Amount charged | `99.00` |
| `months_retained` | integer | Yes | Total months subscribed | `7` |

---

### Event: `subscription_payment_failed`

**When to fire:** Payment fails during renewal

**Where to implement:** Server-side (Stripe webhook)

**Properties:**

| Property | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| `user_id` | string | Yes | User identifier | `usr_a3b4c5d6` |
| `subscription_id` | string | Yes | Subscription ID | `sub_999` |
| `failure_reason` | string | No | Why it failed | `insufficient_funds`, `expired_card` |
| `retry_count` | integer | Yes | Retry attempt number | `1` |

---

**End of Tier 2 (5-7 additional events) → Total: 10-13 events**

---

## **TIER 3 EVENTS (Week 5+ - Advanced, On-Demand)**

### Event: `subscription_upgraded`

**Properties:**

| Property | Type | Required | Example |
|----------|------|----------|---------|
| `user_id` | string | Yes | `usr_a3b4c5d6` |
| `subscription_id` | string | Yes | `sub_999` |
| `old_plan_tier` | string | Yes | `starter` |
| `new_plan_tier` | string | Yes | `pro` |
| `expansion_mrr` | decimal | Yes | `70.00` |

---

### Event: `subscription_downgraded`

**Properties:**

| Property | Type | Required | Example |
|----------|------|----------|---------|
| `user_id` | string | Yes | `usr_a3b4c5d6` |
| `subscription_id` | string | Yes | `sub_999` |
| `old_plan_tier` | string | Yes | `pro` |
| `new_plan_tier` | string | Yes | `starter` |
| `contraction_mrr` | decimal | Yes | `-70.00` |

---

### Event: `user_support_contacted`

**Properties:**

| Property | Type | Required | Example |
|----------|------|----------|---------|
| `user_id` | string | Yes | `usr_a3b4c5d6` |
| `ticket_id` | string | No | `ticket_999` |
| `issue_category` | string | No | `bug`, `feature_request`, `billing` |

---

## 6. Testing & Validation

### 6.1 Enable Debug Mode

```javascript
analytics.debug(true);
```

### 6.2 Validation Checklist

For each event:
- [ ] Event name matches specification exactly
- [ ] All required properties present
- [ ] Property names match specification exactly
- [ ] Property types correct (number vs string vs boolean)
- [ ] No nested objects
- [ ] `identify()` called before `track()` for logged-in users
- [ ] Event appears in Segment debugger

### 6.3 Critical Validation: MRR Reconciliation

**After implementing subscription events, validate:**

```sql
-- BigQuery: Calculate MRR from events
SELECT
  SUM(price) as calculated_mrr
FROM `project.dataset.fact_subscriptions`
WHERE status = 'active';
```

**Compare to:** Stripe dashboard MRR

**Must match within ±2%**

---

## 7. Common Mistakes to Avoid

### ❌ Mistake 1: Firing subscription events on both client and server
```javascript
// WRONG - Don't track on client side
button.onClick(() => {
  analytics.track('subscription_created', {...}); // ❌ Never do this
});

// CORRECT - Only track on server after payment confirmed
// In your Stripe webhook handler
analytics.track('subscription_created', {...}); // ✅
```

### ❌ Mistake 2: Wrong property types
```javascript
// WRONG
{ months_subscribed: '6' }  // String

// CORRECT
{ months_subscribed: 6 }  // Number
```

### ❌ Mistake 3: Not tracking trial conversions correctly
```javascript
// WRONG - Can't tell if they had a trial
{ is_trial_conversion: false }  // for everyone

// CORRECT - Check if user had trial
{ is_trial_conversion: user.hadTrial }  // boolean
```

---

## 8. Platform-Specific Notes

### Stripe Integration

**Use webhooks for all subscription events:**
- `customer.subscription.created` → `subscription_created`
- `customer.subscription.updated` → Check for upgrades/downgrades
- `customer.subscription.deleted` → `subscription_cancelled`
- `invoice.payment_succeeded` → `subscription_renewed`
- `invoice.payment_failed` → `subscription_payment_failed`

**Test webhooks:**
```bash
stripe listen --forward-to localhost:3000/webhooks/stripe
stripe trigger customer.subscription.created
```

---

## 9. Event Summary Table

| Event | Tier | When | Where | Critical? |
|-------|------|------|-------|-----------|
| `user_created` | 1 | Signup complete | Server | High |
| `user_activated` | 1 | Activation milestone | Server | High |
| `subscription_trial_started` | 1 | Trial begins | Server | High |
| `subscription_created` | 1 | First payment | Server | **CRITICAL** |
| `subscription_cancelled` | 1 | User cancels | Server | **CRITICAL** |
| `user_onboarding_completed` | 2 | Onboarding done | Client/Server | Medium |
| `search_initiated` | 2 | Search performed | Client | Medium |
| `feature_used` | 2 | Feature interaction | Client/Server | Medium |
| `subscription_renewed` | 2 | Renewal payment | Server | High |
| `subscription_payment_failed` | 2 | Payment fails | Server | High |
| `subscription_upgraded` | 3 | Plan upgrade | Server | Medium |
| `subscription_downgraded` | 3 | Plan downgrade | Server | Medium |

---

## 10. Questions & Support

**Technical questions:** [SLACK_CHANNEL or EMAIL]

**Analytics questions:** [YOUR_EMAIL]

---

*Last updated: [DATE]*
*Version: 1.0*
*Questions? Contact [YOUR_EMAIL]*
