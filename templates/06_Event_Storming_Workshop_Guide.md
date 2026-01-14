# Event Storming Workshop Guide

**For:** Bratrax Analytics Ontology Design
**Duration:** 90-120 minutes
**Participants:** Client stakeholders (marketing, ops, product)
**Facilitator:** [YOUR_NAME]

---

## What is Event Storming?

Event Storming is a collaborative workshop technique for discovering and mapping the critical events in a business. For Bratrax, it helps us identify:
- What actually happens in the customer journey
- What events drive business decisions
- What metrics we need to track
- What events we can safely ignore

**Core principle:** Start broad (brainstorm everything), then reduce ruthlessly to only events that matter.

---

## Pre-Workshop Preparation

### Client Homework (send 48 hours before)
- [ ] Review completed Discovery Questionnaire
- [ ] Prepare list of current reports/dashboards they use
- [ ] Bring examples of recent business decisions that needed data
- [ ] Think about customer journey from discovery to repeat purchase

### Facilitator Prep
- [ ] Review Discovery Questionnaire responses
- [ ] Identify business model type (basic DTC, multi-channel, subscription, etc.)
- [ ] Prepare virtual whiteboard (Miro/FigJam) or physical sticky notes
- [ ] Load customer journey template for their business model
- [ ] Prepare event naming convention guide
- [ ] Have VidTao example ready as reference

---

## Workshop Agenda

### Part 1: Frame the Session (10 min)

**Introduction:**
> "Today we're going to map out all the important things that happen in your business—from when someone first hears about you to when they become a repeat customer. We'll start by brainstorming everything, then we'll be ruthless about cutting down to only what matters for making decisions."

**Set expectations:**
- No wrong answers in brainstorming phase
- Focus on customer actions, not internal processes
- We'll reduce from 40-50 events down to 12-18
- Goal: events that drive decisions, not just interesting data

**Example to reference:**
> "VidTao started with 44 potential events and reduced to just 18. Airbnb runs their entire analytics on 8 core events. Less is more."

---

### Part 2: Customer Journey Mapping (20 min)

**Draw the journey on whiteboard:**

```
Awareness → Consideration → Purchase → Post-Purchase → Retention
    ↓            ↓              ↓            ↓              ↓
[Events]     [Events]       [Events]     [Events]       [Events]
```

**Facilitate discussion:**

**Q: "How do people first discover your brand?"**
- Google search
- Social media ad
- Friend referral
- Email from abandoned cart
- [Write each as a source on board]

**Q: "What do they do when they land on your site?"**
- Browse products
- Search for something specific
- Read about us
- Sign up for email
- [Capture as potential events]

**Q: "Walk me through a typical purchase flow."**
- View product → Add to cart → Checkout → Purchase
- [Map each step]

**Q: "What happens after they buy?"**
- Receive order confirmation
- Get shipping updates
- Leave a review
- Get marketing emails
- Repurchase

**Output:** Visual journey map with ~40-60 potential touchpoints

---

### Part 3: Brainstorm Events (25 min)

**Instructions:**
> "Now let's turn these touchpoints into specific events—things that happen that we could track. Don't filter yet, just brainstorm."

**Technique: Sticky note storm**
- Each participant writes events on sticky notes (1 event per note)
- Use "entity_activity" format where possible
- 10 minutes of individual writing
- 15 minutes sharing and clustering

**Example prompts:**
- "What action tells you someone is interested in buying?"
- "What action tells you someone is ready to buy again?"
- "What happens when your marketing is working?"
- "What happens that frustrates customers?"

**Common categories to cover:**

**User/Account:**
- user_signed_up
- user_logged_in
- user_subscribed_to_emails
- user_account_updated

**Discovery:**
- homepage_visited
- collection_viewed
- search_initiated
- product_list_filtered

**Product Engagement:**
- product_viewed
- product_image_zoomed
- product_reviews_viewed
- size_guide_viewed

**Cart:**
- product_added_to_cart
- cart_viewed
- product_removed_from_cart
- coupon_applied

**Checkout:**
- checkout_started
- checkout_info_entered
- checkout_shipping_selected
- checkout_payment_entered
- order_completed
- checkout_abandoned

**Post-Purchase:**
- order_shipped
- order_delivered
- order_refunded
- order_returned

**Engagement:**
- email_delivered
- email_opened
- email_clicked
- sms_sent
- sms_clicked

**Loyalty/Retention:**
- review_submitted
- referral_sent
- wishlist_created
- product_saved

**Subscriptions (if applicable):**
- subscription_created
- subscription_paused
- subscription_resumed
- subscription_cancelled
- subscription_renewed

**Typical output:** 40-60 events on the board

---

### Part 4: The Reduction Exercise (30 min)

**This is the most important part.** Reduce from 40-60 events to 12-18.

#### Step 1: Mark Critical Events (10 min)

**Ask: "Which events directly answer your key business questions?"**

Reference their top 5 metrics from Discovery Questionnaire:
- If they need CAC → Need user_signed_up and order_completed
- If they need ROAS → Need order_completed with attribution
- If they need repeat rate → Need order_completed with order_number

**Mark with ⭐ any event that:**
- Represents revenue (order_completed, subscription_created)
- Indicates acquisition (user_signed_up, first session)
- Shows engagement (product_viewed, email_clicked)
- Drives retention (subscription_renewed, repeat order)

**Typical result:** 8-12 critical events marked

---

#### Step 2: Identify Nice-to-Haves (10 min)

**Ask: "What would help explain *why* the critical metrics changed?"**

These provide diagnostic context when critical metrics move:
- Product category breakdowns
- Marketing channel details
- Checkout funnel steps

**Mark with ✓ any event that:**
- Helps diagnose drops in conversion
- Segments customers meaningfully
- Tracks marketing channel effectiveness

**Typical result:** Another 5-8 events marked

---

#### Step 3: Cut Everything Else (10 min)

**Be ruthless.** For each unmarked event, ask:

**"If we tracked this, what decision would it change?"**

If no clear answer → Cut it.

**Common events to cut:**

❌ **Pageview events** (unless they're key landing pages)
- Why: Google Analytics already tracks this
- Exception: Keep if you need attribution from specific landing pages

❌ **Micro-interactions** (image zoom, scroll depth, etc.)
- Why: Doesn't drive business decisions
- Exception: Keep if you're A/B testing UX and need to measure

❌ **Redundant events** (if you have order_completed, you don't need checkout_success)

❌ **Internal process events** (order_packed, invoice_generated)
- Why: Track in operations system, not analytics
- Exception: If it affects customer experience metrics

❌ **Vanity metrics** (social media follows, email list size)
- Why: Not actionable for optimization
- Exception: If it's a KPI you report to board

**Ask the hard question:**
> "You have 18 events maximum. If we track [event X], what are you willing to NOT track instead?"

**Target: 12-18 final events**

---

### Part 5: Validate Against Use Cases (15 min)

**Test your event set against real scenarios:**

**Scenario 1: Monthly business review**
> "It's the 1st of the month. You're reviewing performance. What questions do you ask?"

Walk through: Can you answer each question with your event set?

**Scenario 2: Campaign optimization**
> "You just launched a new Facebook ad campaign. After 3 days, how do you know if it's working?"

Check: Do you have the events to attribute orders to campaigns?

**Scenario 3: Product decisions**
> "Your team wants to discontinue a product. What data do you look at?"

Check: Can you see product-level performance?

**Scenario 4: Customer retention**
> "Repeat purchase rate is dropping. How do you investigate why?"

Check: Can you analyze customer cohorts and behavior patterns?

**If any scenario can't be answered:** You're missing a critical event. Add it back.

**If all scenarios are covered:** You have the right event set.

---

## Part 6: Document Event Taxonomy (15 min)

For each final event, document:

| Event Name | When It Fires | Why It Matters | Required Properties |
|------------|---------------|----------------|---------------------|
| order_completed | Payment confirmed | Revenue, ROAS, CAC | order_id, total_amount, user_id |

**Facilitator action:** Take notes directly into the Ontology Template Section 3.2

---

## Part 7: Choose Implementation Strategy (15 min)

**Decision point: Progressive vs. All-at-once implementation**

### **Default: Progressive Implementation** ⭐ **Recommended**

**What it means:**
- Week 1: Implement Tier 1 (4-5 events)
- Week 2: Launch dashboards, validate tracking
- Week 3-4: Add Tier 2 (8 total events)
- Week 5+: Add Tier 3 selectively based on client requests

**Benefits:**
- Faster time to value (2 weeks vs 4+ weeks)
- Lower risk (easier to debug)
- Flexibility to adjust based on actual usage
- Validates business value before investing in advanced events

**Use progressive when:**
- ✅ Client is new to analytics (most DTC clients)
- ✅ Fast time-to-value is important
- ✅ Budget/resources are constrained
- ✅ Client's needs are unclear
- ✅ This is your first time with this client

---

### **Alternative: All Tiers At Once**

**What it means:**
- Week 1-3: Implement all 17-18 events
- Week 4: Launch complete dashboards
- No phased rollout

**Benefits:**
- Complete data from day 1 (no historical gaps)
- Single implementation cycle
- Simpler stakeholder communication

**Only use all-at-once when:**
- ✅ Client has subscription/retention model (Tier 3 events critical)
- ✅ Client is sophisticated and knows exactly what they need
- ✅ Historical data for advanced events is critical
- ✅ Timeline is flexible (OK waiting 4+ weeks)

---

### **Facilitator Action: Make the Call**

**Ask the client:**
> "Would you rather see your revenue and acquisition dashboards live in 2 weeks with core events, then add more detail later? Or wait 4 weeks to get everything at once?"

**Most clients will choose progressive** when framed this way.

**Document in Ontology Section 3.3:**
- Selected approach: Progressive or All-at-once
- Justification: Why this approach fits this client

---

### **Tier Prioritization** (for progressive approach)

**Tier 1 (Critical - Week 1):**
- Events needed for core metrics (revenue, CAC, ROAS)
- Typically: order_completed, user_signed_up, session_started, email_clicked
- Target: 4-5 events
- **Must be live before dashboard launch**

**Tier 2 (Attribution - Week 3-4):**
- Events that provide attribution and segmentation
- Typically: product_viewed, product_added_to_cart, checkout_started, email_opened
- Target: 6-8 events
- **Add after Tier 1 validated and dashboards launched**

**Tier 3 (Advanced - Week 5+):**
- Events for advanced analysis
- Typically: product_removed_from_cart, order_refunded, review_submitted
- Target: 3-5 events
- **Add only on client request**

**Document the tiers in Ontology Section 3.4**

---

## Decision Framework by Business Complexity

Use this to set expectations before the workshop:

### **Basic DTC (10-12 events)**
**Profile:**
- Single sales channel (just e-commerce)
- Simple product catalog
- Email marketing only
- No subscription model

**Core events:**
- user_signed_up
- product_viewed
- product_added_to_cart
- checkout_started
- order_completed
- email_opened
- email_clicked

**Optional:**
- cart_viewed
- product_removed_from_cart
- collection_viewed
- search_initiated
- order_refunded

---

### **Multi-Channel DTC (15-18 events)**
**Profile:**
- E-commerce + marketplace (Amazon, etc.)
- Multiple marketing channels (email, SMS, ads)
- Affiliate or influencer programs
- Some complexity in customer journey

**Add to basic events:**
- session_started (for attribution)
- sms_delivered
- sms_clicked
- affiliate_click
- review_submitted
- checkout_abandoned

**Total: ~15-18 events**

---

### **Subscription Business (18-22 events)**
**Profile:**
- Subscription or membership model
- Retention is critical metric
- Churn prevention focus
- Free trial or tiered plans

**Add subscription-specific events:**
- subscription_trial_started
- subscription_created
- subscription_renewed
- subscription_payment_failed
- subscription_cancelled
- subscription_paused
- subscription_resumed
- plan_upgraded
- plan_downgraded

**Total: ~18-22 events**

---

### **Complex/Enterprise (20-25 events)**
**Profile:**
- Multiple product lines or business units
- B2B and B2C components
- Advanced personalization
- Multiple apps/platforms

**Add complexity events:**
- account_created (for B2B)
- user_invited (team accounts)
- feature_used (for product analytics)
- integration_connected
- custom_report_generated

**Total: ~20-25 events**

**⚠️ Warning:** If you need >25 events, split into multiple tracking domains or reconsider what's truly critical.

---

## Workshop Outputs & Next Steps

### Immediate deliverables:
- [ ] Visual customer journey map
- [ ] List of 12-18 final events with definitions
- [ ] Event properties documented
- [ ] Implementation tiers (1, 2, 3)

### Follow-up actions:
1. **Facilitator:** Complete Ontology Document Section 3 (Event Taxonomy)
2. **Facilitator:** Draft Tracking Plan based on events
3. **Client:** Review and approve event list within 3 days
4. **Team:** Begin Tier 1 implementation

---

## Common Pitfalls & How to Avoid

### ❌ Pitfall 1: "We need to track everything just in case"
**Solution:** Ask "just in case of what?" Make them name the specific decision. No decision = no event.

### ❌ Pitfall 2: Event names are inconsistent
**Solution:** Enforce entity_activity naming during brainstorm. Fix naming in real-time.

### ❌ Pitfall 3: Events are too granular
**Example:** Tracking every form field entry separately
**Solution:** Combine into milestone events (checkout_info_entered, not first_name_entered)

### ❌ Pitfall 4: Confusing events with entities
**Example:** "customer" is an entity, "customer_created" is an event
**Solution:** Every event must have an activity verb (created, viewed, clicked, etc.)

### ❌ Pitfall 5: Including internal operational events
**Example:** "order_packed", "invoice_sent"
**Solution:** Ask "Does this help optimize customer acquisition or retention?" If no → cut it.

### ❌ Pitfall 6: Can't reduce below 30 events
**Solution:** Use the tier system. Tier 1 must be ≤12 events. Park the rest in Tier 2/3.

---

## Facilitation Tips

### Keep energy high:
- Set a timer for each section
- Use visual tools (sticky notes, colors)
- Celebrate when they make tough cuts
- Share examples from other clients (anonymized)

### Handle disagreements:
- When stakeholders disagree on importance, ask: "What decision does this event inform?"
- Use voting: Each person gets 15 votes to distribute across events
- Defer edge cases to Tier 2/3

### Stay on track:
- Park detailed technical questions ("How do we track this?") for later
- Focus on *what* to track, not *how* to track
- Don't get stuck on event naming—can refine later

### Use the VidTao example:
> "VidTao is a successful product that runs on just 18 events. They started with 44. Here's how they thought about reduction..."

---

## Virtual Workshop Adaptations

**Tools:**
- Miro or FigJam for visual collaboration
- Shared Google Doc for note-taking
- Zoom with screen share

**Process changes:**
- Pre-populate journey template before workshop
- Use Miro templates with event categories
- Breakout rooms if >5 participants (each room tackles one journey stage)
- Use Miro voting feature for reduction exercise

**Timing:**
- Add 15 minutes for tech setup and breaks
- Consider splitting into two 60-minute sessions if remote fatigue is a concern

---

## Post-Workshop: Event Reduction Summary Template

Send this to client after workshop:

```
Event Storming Summary - [CLIENT_NAME]

Workshop Date: [DATE]
Participants: [NAMES]

Starting Point: [X] events brainstormed
Final Count: [Y] core events

EVENT LIST:
Tier 1 (Implement first - [N] events):
1. order_completed - Revenue tracking
2. user_signed_up - CAC calculation
[...]

Tier 2 (Implement second - [N] events):
[...]

Tier 3 (Future - [N] events):
[...]

EVENTS WE DECIDED NOT TO TRACK:
- [Event name] - Reason: [Already tracked in GA / Not actionable / etc.]
[...]

KEY BUSINESS QUESTIONS COVERED:
✓ Question 1: "What's our ROAS by channel?"
  → Answered by: order_completed (with attribution), session_started
✓ Question 2: [...]

NEXT STEPS:
1. Review and approve this list by [DATE]
2. Bratrax will draft Ontology Document
3. Begin Tier 1 tracking implementation
4. Build dummy dashboards

Questions? Reply to this email.
```

---

## Appendix: Sample Event Sets by Industry

### DTC Apparel (15 events)
- user_signed_up
- session_started
- collection_viewed
- product_viewed
- product_added_to_cart
- cart_viewed
- checkout_started
- order_completed
- order_refunded
- email_opened
- email_clicked
- sms_clicked
- review_submitted
- size_guide_viewed
- product_recommended

### DTC Beauty/Skincare (16 events)
- user_signed_up
- session_started
- quiz_completed (for product matching)
- product_viewed
- product_added_to_cart
- checkout_started
- order_completed
- subscription_created
- subscription_cancelled
- email_opened
- email_clicked
- review_submitted
- referral_sent
- auto_replenish_triggered
- ingredient_search_performed
- routine_created

### DTC Food/CPG (14 events)
- user_signed_up
- session_started
- product_viewed
- product_added_to_cart
- checkout_started
- order_completed
- subscription_created
- subscription_renewed
- subscription_paused
- order_refunded
- email_clicked
- recipe_viewed
- bundle_created
- auto_reorder_triggered

---

## Quick Reference: Event Reduction Formula

```
Minimum Events =
  Revenue events (1-2)
  + Acquisition events (1-2)
  + Engagement events (2-4)
  + Marketing attribution (2-4)
  + Critical funnel steps (3-5)
  + Retention events (1-3)

= 10-20 events total
```

**If you have more than 20:** You're likely tracking processes, not decisions. Cut ruthlessly.

**If you have fewer than 10:** You might be missing diagnostic context for when metrics change.

---

*Event Storming Workshop Guide v1.0*
*Questions? [YOUR_EMAIL]*
