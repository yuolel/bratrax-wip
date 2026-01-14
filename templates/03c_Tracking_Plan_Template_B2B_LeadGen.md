# [CLIENT_NAME] Event Tracking Implementation Guide

**Version:** 1.0
**Date:** [DATE]
**Prepared by:** [YOUR_NAME]
**For:** Development Team
**Business Model:** B2B Lead Generation

---

## 1. Overview

This guide provides exact specifications for implementing event tracking for [CLIENT_NAME]'s B2B lead generation website. Every event documented here flows to BigQuery where it powers analytics dashboards and lead attribution metrics.

**Critical:** This is a technical specification. Event names, property names, and property types must be implemented **exactly as specified**. Even small deviations (typos, wrong types, extra nesting) will break downstream analytics.

---

## 2. Implementation Context

### 2.1 Tech Stack
- **Platform:** [WordPress / React / Next.js / Custom CMS]
- **Tracking method:** [Segment / Google Tag Manager / Custom]
- **Programming language:** [JavaScript / TypeScript / Python]
- **Analytics library:** [Segment Analytics.js 2.0 / Custom]
- **CRM/MAP:** [HubSpot / Salesforce / Marketo / Pardot]
- **Form platform:** [Native / Typeform / Gravity Forms / HubSpot Forms]

### 2.2 Before You Start

**Required reading:**
- [CLIENT_NAME] Analytics Ontology (defines what events mean)
- [CLIENT_NAME] Discovery Questionnaire (business context)

**Prerequisites:**
- [ ] Analytics script is installed on all pages
- [ ] You have access to test in a development/staging environment
- [ ] You can view events in [Segment debugger / BigQuery console]
- [ ] CRM/MAP integration is configured (for server-side events)

---

## 3. Global Implementation Rules

### 3.1 Event Naming Convention

**Format:** `{entity}_{activity}`

**Rules:**
1. All lowercase
2. Underscores only (no hyphens or spaces)
3. Past tense for activities (`captured`, `qualified`, `submitted`)
4. Be specific (`demo_scheduled` not just `scheduled`)

**Valid:** `lead_captured`, `form_submitted`, `mql_qualified`
**Invalid:** `Lead_Captured`, `form-submitted`, `capturedLead`

---

### 3.2 Property Naming Convention

**Rules:**
1. All lowercase with underscores
2. Use full words, not abbreviations (except common ones like `id`, `url`)
3. No nested objects (flat properties only)

**Valid:** `lead_id`, `form_type`, `company_size`, `is_first_form`
**Invalid:** `leadID`, `formType`, `companySize`, `lead.id`

---

### 3.3 Property Types

| Type | JavaScript | Example | Notes |
|------|------------|---------|-------|
| String | `'value'` | `form_type: 'demo_request'` | Always use quotes |
| Number | `123` or `45.67` | `lead_score: 75` | No quotes |
| Boolean | `true` / `false` | `is_first_form: true` | Lowercase, no quotes |
| ISO Date | `'2025-01-15T10:30:00Z'` | `qualified_at: '2025-01-15T10:30:00Z'` | ISO 8601 format in UTC |

**Common mistakes to avoid:**
- ❌ `lead_score: '75'` (string instead of number)
- ❌ `is_first_form: 'true'` (string instead of boolean)

---

### 3.4 Required vs Optional Properties

- **Required properties MUST be present** in every event call
- **Optional properties** can be omitted if not available
- Never send `null` or `undefined` for optional properties—omit them entirely

---

## 4. Identity Management

### 4.1 Lead Identification Flow

**Anonymous visitor → Submits form → Identified lead**

#### When lead submits first form (form_submitted event):
```javascript
// 1. Call identify() to set lead_id
analytics.identify(leadId, {
  email: 'john.doe@acmecorp.com',
  company_name: 'Acme Corp',
  job_title: 'Director of Marketing',
  company_size: '51-200'
});

// 2. Track the form submission
analytics.track('form_submitted', {
  form_id: 'form_sub_abc123',
  lead_id: leadId,
  form_type: 'demo_request',
  form_name: 'Homepage Demo Request',
  page_url: window.location.href,
  session_id: sessionId,
  is_first_form: true
});

// 3. Track lead_captured event (creates lead record)
analytics.track('lead_captured', {
  lead_id: leadId,
  email: 'john.doe@acmecorp.com',
  company_name: 'Acme Corp',
  job_title: 'Director of Marketing',
  company_size: '51-200',
  acquisition_source: getUtmSource() || 'direct',
  acquisition_campaign: getUtmCampaign() || null,
  utm_source: getUtmSource(),
  utm_medium: getUtmMedium(),
  utm_campaign: getUtmCampaign(),
  utm_content: getUtmContent(),
  landing_page: getLandingPage(),
  form_type: 'demo_request',
  lead_score: 0
});
```

#### For returning leads (subsequent form submissions):
```javascript
// They're already identified, just track the form submission
analytics.track('form_submitted', {
  form_id: 'form_sub_xyz456',
  lead_id: existingLeadId,
  form_type: 'content_download',
  form_name: 'Whitepaper Download',
  page_url: window.location.href,
  session_id: sessionId,
  is_first_form: false
});
```

---

### 4.2 Anonymous Session Tracking

**Before lead identification**, track sessions anonymously:

```javascript
// On page load
analytics.track('session_started', {
  session_id: sessionId, // Generate or retrieve from cookie
  lead_id: null, // Not identified yet
  utm_source: getUtmSource(),
  utm_medium: getUtmMedium(),
  utm_campaign: getUtmCampaign(),
  utm_content: getUtmContent(),
  landing_page: window.location.href,
  referrer: document.referrer,
  device_type: getDeviceType(), // 'desktop', 'mobile', 'tablet'
  ip_address: null // Captured server-side
});
```

**After lead identification**, include lead_id in session tracking:
```javascript
analytics.track('page_viewed', {
  session_id: sessionId,
  lead_id: leadId, // Now identified
  page_url: window.location.href,
  page_title: document.title
});
```

---

## 5. Tier 1 Events (Week 1 Implementation)

These are critical events that enable core dashboards. Implement these first.

---

### 5.1 `lead_captured`

**When:** A new lead is created (first form submission or identified visitor)

**Where:** Server-side (after form validation and lead creation in CRM/database)

**Code example (Node.js backend):**
```javascript
// After form submission is validated and lead created
const Analytics = require('analytics-node');
const analytics = new Analytics('YOUR_WRITE_KEY');

async function handleFormSubmission(formData) {
  // 1. Validate form data
  // 2. Create lead in CRM/database
  const leadId = await createLeadInCRM(formData);

  // 3. Track lead_captured event
  analytics.track({
    userId: leadId,
    event: 'lead_captured',
    properties: {
      lead_id: leadId,
      email: formData.email,
      company_name: formData.company_name || null,
      job_title: formData.job_title || null,
      company_size: formData.company_size || null,
      acquisition_source: formData.utm_source || 'direct',
      acquisition_campaign: formData.utm_campaign || null,
      utm_source: formData.utm_source || null,
      utm_medium: formData.utm_medium || null,
      utm_campaign: formData.utm_campaign || null,
      utm_content: formData.utm_content || null,
      landing_page: formData.landing_page,
      form_type: formData.form_type, // e.g., 'demo_request'
      lead_score: 0
    },
    timestamp: new Date().toISOString()
  });

  return leadId;
}
```

**Properties:**

| Property | Type | Required | Example | Notes |
|----------|------|----------|---------|-------|
| `lead_id` | string | Yes | `lead_a3b4c5d6` | Unique identifier from CRM |
| `email` | string | Yes | `john@acmecorp.com` | Lead email |
| `company_name` | string | No | `Acme Corp` | Organization name |
| `job_title` | string | No | `Director of Marketing` | Lead's role |
| `company_size` | string | No | `51-200` | Employee count bracket |
| `acquisition_source` | string | Yes | `linkedin`, `google_ads`, `direct` | First-touch source |
| `acquisition_campaign` | string | No | `q1_demo_campaign` | First-touch campaign |
| `utm_source` | string | No | `linkedin` | UTM parameter |
| `utm_medium` | string | No | `cpc` | UTM parameter |
| `utm_campaign` | string | No | `q1_demo_campaign` | UTM parameter |
| `utm_content` | string | No | `carousel_ad_v2` | UTM parameter |
| `landing_page` | string | Yes | `/solutions/marketing-automation` | First page viewed |
| `form_type` | string | Yes | `demo_request`, `contact_us`, `content_download` | Type of form submitted |
| `lead_score` | integer | Yes | `0` | Initial score (usually 0) |

---

### 5.2 `session_started`

**When:** Visitor lands on website (anonymous or identified)

**Where:** Client-side (browser JavaScript)

**Code example:**
```javascript
// On page load (first page of session)
const sessionId = getOrCreateSessionId(); // From cookie, generate if new
const leadId = getLeadId(); // From cookie/localStorage if identified

analytics.track('session_started', {
  session_id: sessionId,
  lead_id: leadId || null, // null if anonymous
  utm_source: getUtmParam('utm_source') || null,
  utm_medium: getUtmParam('utm_medium') || null,
  utm_campaign: getUtmParam('utm_campaign') || null,
  utm_content: getUtmParam('utm_content') || null,
  landing_page: window.location.href,
  referrer: document.referrer || null,
  device_type: getDeviceType(), // 'desktop', 'mobile', 'tablet'
  ip_address: null // Captured by analytics tool server-side
});

// Helper functions
function getOrCreateSessionId() {
  let sessionId = getCookie('session_id');
  if (!sessionId) {
    sessionId = 'sess_' + generateRandomId();
    setCookie('session_id', sessionId, 30); // 30 min expiry
  }
  return sessionId;
}

function getDeviceType() {
  const width = window.innerWidth;
  if (width < 768) return 'mobile';
  if (width < 1024) return 'tablet';
  return 'desktop';
}

function getUtmParam(param) {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get(param);
}
```

**Properties:**

| Property | Type | Required | Example | Notes |
|----------|------|----------|---------|-------|
| `session_id` | string | Yes | `sess_x7y8z9` | Generated or from cookie |
| `lead_id` | string | No | `lead_a3b4c5d6` | If visitor is identified |
| `utm_source` | string | No | `linkedin` | UTM parameter |
| `utm_medium` | string | No | `cpc` | UTM parameter |
| `utm_campaign` | string | No | `q1_demo_campaign` | UTM parameter |
| `utm_content` | string | No | `carousel_ad_v2` | UTM parameter |
| `landing_page` | string | Yes | `/solutions/marketing-automation` | Page URL |
| `referrer` | string | No | `https://linkedin.com` | Referring URL |
| `device_type` | string | Yes | `desktop`, `mobile`, `tablet` | Device category |
| `ip_address` | string | No | `null` | Captured server-side automatically |

---

### 5.3 `form_submitted`

**When:** User submits any form (demo request, contact, gated content, newsletter)

**Where:** Client-side (form submit handler) OR Server-side (after validation)

**Code example (client-side):**
```javascript
// Form submit handler
document.getElementById('demo-form').addEventListener('submit', function(e) {
  e.preventDefault();

  const formData = {
    email: document.getElementById('email').value,
    company_name: document.getElementById('company').value,
    job_title: document.getElementById('title').value
  };

  // Track form submission (client-side)
  analytics.track('form_submitted', {
    form_id: 'form_sub_' + generateRandomId(),
    lead_id: getLeadId() || null, // null if first form
    form_type: 'demo_request',
    form_name: 'Homepage Demo Request',
    page_url: window.location.href,
    session_id: getSessionId(),
    utm_source: getUtmParam('utm_source') || null,
    utm_campaign: getUtmParam('utm_campaign') || null,
    is_first_form: !getLeadId() // true if this is first form submission
  });

  // Submit to server
  submitFormToServer(formData);
});
```

**Properties:**

| Property | Type | Required | Example | Notes |
|----------|------|----------|---------|-------|
| `form_id` | string | Yes | `form_sub_abc123` | Unique submission ID |
| `lead_id` | string | No | `lead_a3b4c5d6` | If lead already exists |
| `form_type` | string | Yes | `demo_request`, `contact_us`, `content_download`, `newsletter` | Type of form |
| `form_name` | string | Yes | `Homepage Demo Request` | Descriptive form name |
| `page_url` | string | Yes | `/solutions/marketing-automation` | Where form was submitted |
| `session_id` | string | Yes | `sess_x7y8z9` | Current session |
| `utm_source` | string | No | `linkedin` | Attribution at submission |
| `utm_campaign` | string | No | `q1_demo_campaign` | Attribution at submission |
| `is_first_form` | boolean | Yes | `true` or `false` | True if this creates the lead |

---

### 5.4 `mql_qualified`

**When:** Lead reaches MQL (Marketing Qualified Lead) threshold

**Where:** Server-side (triggered by marketing automation platform or lead scoring logic)

**Code example (triggered by HubSpot workflow or Marketo smart campaign):**
```javascript
// HubSpot webhook handler or internal lead scoring service
async function handleMqlQualification(lead) {
  const Analytics = require('analytics-node');
  const analytics = new Analytics('YOUR_WRITE_KEY');

  // Calculate days to MQL
  const createdAt = new Date(lead.created_at);
  const mqlAt = new Date();
  const daysToMql = Math.floor((mqlAt - createdAt) / (1000 * 60 * 60 * 24));

  analytics.track({
    userId: lead.lead_id,
    event: 'mql_qualified',
    properties: {
      lead_id: lead.lead_id,
      lead_score: lead.current_score,
      qualification_criteria: 'score_threshold', // or 'manual_review'
      qualified_at: mqlAt.toISOString(),
      days_to_mql: daysToMql,
      touchpoints_to_mql: await countTouchpoints(lead.lead_id) // optional
    },
    timestamp: mqlAt.toISOString()
  });
}
```

**Properties:**

| Property | Type | Required | Example | Notes |
|----------|------|----------|---------|-------|
| `lead_id` | string | Yes | `lead_a3b4c5d6` | Lead identifier |
| `lead_score` | integer | Yes | `75` | Score at qualification |
| `qualification_criteria` | string | No | `score_threshold`, `manual_review` | How qualified |
| `qualified_at` | timestamp | Yes | `2025-01-16T14:22:00Z` | MQL timestamp |
| `days_to_mql` | integer | Yes | `3` | Days since lead created |
| `touchpoints_to_mql` | integer | No | `8` | Number of interactions |

---

### 5.5 `sql_qualified`

**When:** Lead reaches SQL (Sales Qualified Lead) status (sales team accepts)

**Where:** Server-side (triggered by CRM update, e.g., Salesforce workflow or manual log)

**Code example (Salesforce webhook):**
```javascript
// Salesforce webhook handler when Lead Status changes to "SQL"
async function handleSqlQualification(salesforceWebhookData) {
  const Analytics = require('analytics-node');
  const analytics = new Analytics('YOUR_WRITE_KEY');

  const lead = salesforceWebhookData.lead;
  const createdAt = new Date(lead.created_date);
  const sqlAt = new Date();
  const daysToSql = Math.floor((sqlAt - createdAt) / (1000 * 60 * 60 * 24));

  analytics.track({
    userId: lead.id,
    event: 'sql_qualified',
    properties: {
      lead_id: lead.id,
      lead_score: lead.score || null,
      qualified_by: lead.owner_email,
      qualification_reason: lead.qualification_notes || null,
      qualified_at: sqlAt.toISOString(),
      days_to_sql: daysToSql,
      assigned_to: lead.owner_email
    },
    timestamp: sqlAt.toISOString()
  });
}
```

**Properties:**

| Property | Type | Required | Example | Notes |
|----------|------|----------|---------|-------|
| `lead_id` | string | Yes | `lead_a3b4c5d6` | Lead identifier |
| `lead_score` | integer | No | `85` | Score at qualification |
| `qualified_by` | string | Yes | `sarah@company.com` | Sales rep who accepted |
| `qualification_reason` | string | No | `budget_confirmed, decision_maker` | Why qualified |
| `qualified_at` | timestamp | Yes | `2025-01-18T09:15:00Z` | SQL timestamp |
| `days_to_sql` | integer | Yes | `5` | Days since lead created |
| `assigned_to` | string | Yes | `sarah@company.com` | Sales rep assigned |

---

### 5.6 `email_clicked` (Optional Tier 1)

**When:** Lead clicks link in marketing email

**Where:** Server-side (email platform webhook, e.g., SendGrid, Mailchimp, HubSpot)

**Code example (SendGrid webhook):**
```javascript
// SendGrid webhook handler for click events
app.post('/webhooks/sendgrid', (req, res) => {
  const events = req.body;

  events.forEach(event => {
    if (event.event === 'click') {
      analytics.track({
        userId: event.lead_id || event.email, // Use lead_id if available
        event: 'email_clicked',
        properties: {
          email_id: event.sg_message_id,
          lead_id: event.lead_id || null,
          campaign_id: event.campaign_id || null,
          email_subject: event.subject || null,
          link_url: event.url,
          link_name: getLinkName(event.url), // Extract link name
          clicked_at: new Date(event.timestamp * 1000).toISOString()
        },
        timestamp: new Date(event.timestamp * 1000).toISOString()
      });
    }
  });

  res.sendStatus(200);
});
```

**Properties:**

| Property | Type | Required | Example | Notes |
|----------|------|----------|---------|-------|
| `email_id` | string | Yes | `msg_abc123` | Unique email message ID |
| `lead_id` | string | No | `lead_a3b4c5d6` | If lead is identified |
| `campaign_id` | string | No | `camp_q1_nurture` | Email campaign ID |
| `email_subject` | string | No | `5 Ways to Improve Lead Quality` | Subject line |
| `link_url` | string | Yes | `https://example.com/blog/post` | Clicked URL |
| `link_name` | string | No | `Read Blog Post` | Link text/name |
| `clicked_at` | timestamp | Yes | `2025-01-17T11:30:00Z` | Click timestamp |

---

## 6. Tier 2 Events (Week 3-4 Implementation)

Add these after Tier 1 is live and validated.

---

### 6.1 `page_viewed`

**When:** Lead or anonymous visitor views a key page

**Where:** Client-side (page load)

**Code example:**
```javascript
// Track page view for key pages (pricing, solutions, case studies)
const keyPages = ['/pricing', '/solutions', '/case-studies', '/customers'];
const currentPath = window.location.pathname;

if (keyPages.some(page => currentPath.includes(page))) {
  analytics.track('page_viewed', {
    session_id: getSessionId(),
    lead_id: getLeadId() || null,
    page_url: window.location.href,
    page_title: document.title,
    page_category: getPageCategory(currentPath), // 'pricing', 'solution', 'case_study'
    time_on_page: null // Will be updated on page exit
  });
}

function getPageCategory(path) {
  if (path.includes('/pricing')) return 'pricing';
  if (path.includes('/solutions')) return 'solution';
  if (path.includes('/case-studies') || path.includes('/customers')) return 'case_study';
  if (path.includes('/blog')) return 'blog';
  return 'other';
}
```

**Properties:**

| Property | Type | Required | Example |
|----------|------|----------|---------|
| `session_id` | string | Yes | `sess_x7y8z9` |
| `lead_id` | string | No | `lead_a3b4c5d6` |
| `page_url` | string | Yes | `/pricing` |
| `page_title` | string | Yes | `Pricing - Acme Software` |
| `page_category` | string | No | `pricing`, `solution`, `case_study`, `blog` |
| `time_on_page` | integer | No | `45` (seconds) |

---

### 6.2 `content_downloaded`

**When:** Lead downloads gated content

**Where:** Server-side (after form submission and file delivery)

**Code example:**
```javascript
// After content download form submission
async function handleContentDownload(formData, contentInfo) {
  const leadId = await getOrCreateLead(formData);

  analytics.track({
    userId: leadId,
    event: 'content_downloaded',
    properties: {
      lead_id: leadId,
      content_type: contentInfo.type, // 'whitepaper', 'case_study', 'template'
      content_title: contentInfo.title,
      content_id: contentInfo.id,
      session_id: formData.session_id,
      page_url: formData.page_url
    },
    timestamp: new Date().toISOString()
  });
}
```

**Properties:**

| Property | Type | Required | Example |
|----------|------|----------|---------|
| `lead_id` | string | Yes | `lead_a3b4c5d6` |
| `content_type` | string | Yes | `whitepaper`, `case_study`, `template`, `ebook` |
| `content_title` | string | Yes | `The Ultimate B2B Lead Gen Guide` |
| `content_id` | string | Yes | `content_123` |
| `session_id` | string | Yes | `sess_x7y8z9` |
| `page_url` | string | Yes | `/resources/whitepaper-b2b-guide` |

---

### 6.3 `demo_scheduled`

**When:** Lead books a demo or sales call

**Where:** Server-side (calendar integration webhook, e.g., Calendly, Chili Piper)

**Code example (Calendly webhook):**
```javascript
// Calendly webhook handler
app.post('/webhooks/calendly', async (req, res) => {
  const event = req.body.payload;

  if (event.event === 'invitee.created') {
    const invitee = event.invitee;
    const leadId = await findLeadByEmail(invitee.email);

    analytics.track({
      userId: leadId,
      event: 'demo_scheduled',
      properties: {
        lead_id: leadId,
        demo_type: 'live_demo', // or 'sales_call'
        scheduled_for: event.scheduled_event.start_time,
        scheduled_at: new Date().toISOString(),
        calendly_event_id: event.uri,
        meeting_duration: event.scheduled_event.duration // minutes
      },
      timestamp: new Date().toISOString()
    });
  }

  res.sendStatus(200);
});
```

**Properties:**

| Property | Type | Required | Example |
|----------|------|----------|---------|
| `lead_id` | string | Yes | `lead_a3b4c5d6` |
| `demo_type` | string | Yes | `live_demo`, `recorded_demo`, `sales_call` |
| `scheduled_for` | timestamp | Yes | `2025-01-20T14:00:00Z` |
| `scheduled_at` | timestamp | Yes | `2025-01-17T10:30:00Z` |
| `calendly_event_id` | string | No | `calendly.com/events/ABC123` |
| `meeting_duration` | integer | No | `30` (minutes) |

---

### 6.4 `demo_attended`

**When:** Lead attends or no-shows scheduled demo

**Where:** Server-side (sales rep logs in CRM or automated via meeting platform)

**Code example:**
```javascript
// Sales rep logs demo attendance in CRM
async function logDemoAttendance(demoData) {
  analytics.track({
    userId: demoData.lead_id,
    event: 'demo_attended',
    properties: {
      lead_id: demoData.lead_id,
      demo_type: demoData.demo_type,
      scheduled_for: demoData.scheduled_for,
      attended_at: new Date().toISOString(),
      duration: demoData.actual_duration, // actual minutes attended
      sales_rep: demoData.sales_rep_email,
      attended_status: demoData.status // 'attended', 'no_show', 'rescheduled'
    },
    timestamp: new Date().toISOString()
  });
}
```

**Properties:**

| Property | Type | Required | Example |
|----------|------|----------|---------|
| `lead_id` | string | Yes | `lead_a3b4c5d6` |
| `demo_type` | string | Yes | `live_demo`, `sales_call` |
| `scheduled_for` | timestamp | Yes | `2025-01-20T14:00:00Z` |
| `attended_at` | timestamp | Yes | `2025-01-20T14:05:00Z` |
| `duration` | integer | No | `28` (actual minutes) |
| `sales_rep` | string | Yes | `sarah@company.com` |
| `attended_status` | string | Yes | `attended`, `no_show`, `rescheduled` |

---

### 6.5 `webinar_registered`

**When:** Lead registers for webinar/event

**Where:** Server-side (webinar platform webhook, e.g., Zoom, Demio)

**Code example:**
```javascript
// Zoom webinar registration webhook
app.post('/webhooks/zoom', async (req, res) => {
  const event = req.body.event;

  if (event === 'webinar.registration_created') {
    const registrant = req.body.payload.object;
    const leadId = await getOrCreateLeadByEmail(registrant.email);

    analytics.track({
      userId: leadId,
      event: 'webinar_registered',
      properties: {
        lead_id: leadId,
        webinar_id: req.body.payload.object.webinar_id,
        webinar_title: req.body.payload.object.topic,
        webinar_date: req.body.payload.object.start_time,
        registered_at: new Date().toISOString(),
        registration_source: registrant.custom_questions?.source || null
      },
      timestamp: new Date().toISOString()
    });
  }

  res.sendStatus(200);
});
```

**Properties:**

| Property | Type | Required | Example |
|----------|------|----------|---------|
| `lead_id` | string | Yes | `lead_a3b4c5d6` |
| `webinar_id` | string | Yes | `webinar_123` |
| `webinar_title` | string | Yes | `Mastering B2B Lead Generation` |
| `webinar_date` | timestamp | Yes | `2025-01-25T15:00:00Z` |
| `registered_at` | timestamp | Yes | `2025-01-17T11:00:00Z` |
| `registration_source` | string | No | `landing_page`, `email_invite`, `linkedin_ad` |

---

### 6.6 `webinar_attended`

**When:** Lead attends webinar

**Where:** Server-side (webinar platform post-event data)

**Code example:**
```javascript
// Zoom webinar attendance report processing (batch)
async function processWebinarAttendance(attendanceData) {
  for (const attendee of attendanceData) {
    const leadId = await findLeadByEmail(attendee.email);

    const attendancePercentage = Math.round(
      (attendee.duration / webinarTotalDuration) * 100
    );

    analytics.track({
      userId: leadId,
      event: 'webinar_attended',
      properties: {
        lead_id: leadId,
        webinar_id: attendee.webinar_id,
        webinar_title: attendee.webinar_title,
        attended_at: new Date(attendee.join_time).toISOString(),
        attendance_duration: attendee.duration, // minutes
        attendance_percentage: attendancePercentage,
        polls_answered: attendee.polls_answered || null,
        questions_asked: attendee.questions_asked || null
      },
      timestamp: new Date(attendee.join_time).toISOString()
    });
  }
}
```

**Properties:**

| Property | Type | Required | Example |
|----------|------|----------|---------|
| `lead_id` | string | Yes | `lead_a3b4c5d6` |
| `webinar_id` | string | Yes | `webinar_123` |
| `webinar_title` | string | Yes | `Mastering B2B Lead Generation` |
| `attended_at` | timestamp | Yes | `2025-01-25T15:05:00Z` |
| `attendance_duration` | integer | Yes | `42` (minutes) |
| `attendance_percentage` | integer | Yes | `70` (% of webinar) |
| `polls_answered` | integer | No | `3` |
| `questions_asked` | integer | No | `1` |

---

### 6.7 `lead_scored`

**When:** Lead score changes due to activity

**Where:** Server-side (marketing automation platform or internal scoring engine)

**Code example:**
```javascript
// Lead scoring service
async function updateLeadScore(leadId, triggerEvent, scoreChange) {
  const lead = await getLeadById(leadId);
  const previousScore = lead.score;
  const newScore = previousScore + scoreChange;

  // Update lead score in database
  await updateLeadScoreInDb(leadId, newScore);

  // Track score change event
  analytics.track({
    userId: leadId,
    event: 'lead_scored',
    properties: {
      lead_id: leadId,
      previous_score: previousScore,
      new_score: newScore,
      score_change: scoreChange,
      trigger_event: triggerEvent, // e.g., 'content_downloaded', 'pricing_page_viewed'
      scored_at: new Date().toISOString()
    },
    timestamp: new Date().toISOString()
  });

  // Check if lead now qualifies as MQL
  if (previousScore < 50 && newScore >= 50) {
    await qualifyLeadAsMql(leadId);
  }
}
```

**Properties:**

| Property | Type | Required | Example |
|----------|------|----------|---------|
| `lead_id` | string | Yes | `lead_a3b4c5d6` |
| `previous_score` | integer | Yes | `45` |
| `new_score` | integer | Yes | `60` |
| `score_change` | integer | Yes | `15` |
| `trigger_event` | string | Yes | `content_downloaded`, `pricing_page_viewed` |
| `scored_at` | timestamp | Yes | `2025-01-17T14:20:00Z` |

---

### 6.8 `email_opened`

**When:** Lead opens marketing email

**Where:** Server-side (email platform webhook)

**Code example (HubSpot webhook):**
```javascript
// HubSpot email open webhook
app.post('/webhooks/hubspot/email', (req, res) => {
  const event = req.body[0]; // HubSpot sends array of events

  if (event.type === 'EMAIL.OPENED') {
    analytics.track({
      userId: event.contactId,
      event: 'email_opened',
      properties: {
        email_id: event.emailCampaignId,
        lead_id: event.contactId,
        campaign_id: event.campaignId || null,
        email_subject: event.subject,
        opened_at: new Date(event.occurredAt).toISOString(),
        opens_count: event.openCount || 1
      },
      timestamp: new Date(event.occurredAt).toISOString()
    });
  }

  res.sendStatus(200);
});
```

**Properties:**

| Property | Type | Required | Example |
|----------|------|----------|---------|
| `email_id` | string | Yes | `email_abc123` |
| `lead_id` | string | No | `lead_a3b4c5d6` |
| `campaign_id` | string | No | `camp_q1_nurture` |
| `email_subject` | string | No | `5 Ways to Improve Lead Quality` |
| `opened_at` | timestamp | Yes | `2025-01-17T09:15:00Z` |
| `opens_count` | integer | No | `2` (if opened multiple times) |

---

## 7. Tier 3 Events (Week 5+, Optional)

Implement selectively based on specific business needs.

### 7.1 `opportunity_created`
### 7.2 `deal_won`
### 7.3 `deal_lost`
### 7.4 `chatbot_conversation`
### 7.5 `ad_clicked`

See [CLIENT_NAME] Analytics Ontology for full specifications.

---

## 8. Testing & Validation

### 8.1 Testing Checklist

Before deploying to production:

- [ ] **Event names** match ontology exactly (lowercase, underscores, past tense)
- [ ] **Property names** match ontology exactly (lowercase, underscores)
- [ ] **Property types** are correct (string, number, boolean, not wrong types)
- [ ] **Required properties** are always present
- [ ] **Optional properties** are omitted (not sent as `null`) when unavailable
- [ ] **UTM parameters** are captured correctly on session start
- [ ] **lead_id** is generated and persisted correctly
- [ ] **session_id** is generated and persisted across pages

---

### 8.2 Testing Tools

**Segment Debugger:**
1. Go to Segment Debugger: https://app.segment.com/[workspace]/sources/[source]/debugger
2. Trigger events on staging site
3. Verify events appear in real-time with correct properties

**BigQuery Console:**
```sql
-- Verify lead_captured events
SELECT * FROM `project.dataset.lead_captured`
WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 HOUR)
ORDER BY timestamp DESC
LIMIT 10;
```

---

### 8.3 Common Issues & Fixes

| Issue | Symptom | Fix |
|-------|---------|-----|
| Events not appearing | No events in debugger | Check analytics script is loaded, check network tab for blocked requests |
| Wrong property types | Dashboards show zeros | Convert strings to numbers, booleans correctly |
| Missing lead_id | Events not tied to leads | Ensure identify() called before track() |
| UTM params not captured | Attribution shows "direct" | Capture UTMs on session_started, persist to all events in that session |
| Duplicate events | Same event appears multiple times | Debounce form submissions, check for double event calls |

---

## 9. Privacy & Compliance

### 9.1 GDPR/CCPA Compliance

**Do:**
- ✅ Get consent before tracking identified leads
- ✅ Provide cookie banner with opt-out
- ✅ Honor Do Not Track headers
- ✅ Anonymize IP addresses in analytics
- ✅ Provide data deletion upon request

**Don't:**
- ❌ Track leads without consent in EU/CA
- ❌ Store PII unnecessarily (only email, company, title needed)
- ❌ Share lead data with third parties without consent

---

### 9.2 Data Retention

- **Leads and events:** Retain for 24-36 months
- **PII (email, name):** Anonymize or delete upon request
- **Session data:** Retain for 12 months

---

## 10. Support & Questions

**Questions about implementation?**
Contact: [YOUR_EMAIL]

**Questions about what events mean?**
See: [CLIENT_NAME] Analytics Ontology

**Questions about dashboards/metrics?**
Contact: [ANALYTICS_TEAM_EMAIL]

---

## 11. Appendix: Code Snippets

### A. Session ID Management

```javascript
// Generate and persist session ID
function getOrCreateSessionId() {
  const SESSION_TIMEOUT = 30 * 60 * 1000; // 30 minutes

  let session = JSON.parse(localStorage.getItem('session') || '{}');
  const now = Date.now();

  // Check if session expired
  if (!session.id || (now - session.lastActivity) > SESSION_TIMEOUT) {
    session = {
      id: 'sess_' + Math.random().toString(36).substr(2, 9),
      lastActivity: now
    };
  } else {
    session.lastActivity = now;
  }

  localStorage.setItem('session', JSON.stringify(session));
  return session.id;
}
```

### B. UTM Parameter Capture

```javascript
// Capture and persist UTM parameters
function captureUtmParams() {
  const urlParams = new URLSearchParams(window.location.search);
  const utmParams = {
    utm_source: urlParams.get('utm_source') || null,
    utm_medium: urlParams.get('utm_medium') || null,
    utm_campaign: urlParams.get('utm_campaign') || null,
    utm_content: urlParams.get('utm_content') || null,
    utm_term: urlParams.get('utm_term') || null
  };

  // Only store if at least one UTM parameter exists
  if (Object.values(utmParams).some(v => v !== null)) {
    sessionStorage.setItem('utm_params', JSON.stringify(utmParams));
  }

  return utmParams;
}

function getStoredUtmParams() {
  const stored = sessionStorage.getItem('utm_params');
  return stored ? JSON.parse(stored) : {};
}
```

### C. Lead ID Persistence

```javascript
// Store lead ID after first form submission
function setLeadId(leadId) {
  localStorage.setItem('lead_id', leadId);
  analytics.identify(leadId);
}

function getLeadId() {
  return localStorage.getItem('lead_id');
}
```

---

## Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | [DATE] | [NAME] | Initial tracking plan created |
