# **VidTao Event Tracking**

# **Implementation Guide**

For Developers: Using Segment Analytics 2.0

# **1\. Overview**

This guide explains how to implement event tracking in VidTao using our Segment Analytics 2.0 script. Every event you implement will flow to our analytics platform where it powers metrics, funnels, and business insights.

**Why does this matter?**  
From the Analytics Implementation Workbook: "The worst ticket you can write is 'Add tracking for this event' \- a recipe for disaster. Take out as much guesswork as possible." This document provides that precision.

## **Client-Side vs Server-Side**

| Location | When to Use | Example Events |
| :---- | :---- | :---- |
| **Client-Side** | User interactions in browser | search\_initiated, ad\_details\_viewed |
| **Server-Side** | Data changes, payments, accounts | user\_created, subscription\_created |

**Rule of thumb:** If it touches the database or involves money → Server-side. If it's a UI interaction → Client-side.

# **2\. Event Naming Convention**

## **Format: {entity}\_{activity}**

All VidTao events follow this pattern:

* **entity** \= The thing being acted upon (user, search, swipe\_board, ad, subscription)  
* **activity** \= What happened to it (created, viewed, initiated, updated)

### **Examples**

| Event Name | Entity | Activity |
| :---- | :---- | :---- |
| user\_created | user | created |
| search\_initiated | search | initiated |
| swipe\_board\_updated | swipe\_board | updated |
| ad\_details\_viewed | ad | details\_viewed |
| subscription\_created | subscription | created |

### **Rules**

1. **All lowercase** \- Never User\_Created or userCreated  
2. **Underscores only** \- Never hyphens or spaces  
3. **Past tense for activities** \- created not create, viewed not view  
4. **Be specific** \- ad\_details\_viewed not just viewed

# **3\. The Track Method**

## **Basic Syntax**

analytics.track(eventName, properties, options, callback);

| Parameter | Type | Required | Description |
| :---- | :---- | :---- | :---- |
| eventName | string | Yes | The event name (e.g., 'search\_initiated') |
| properties | object | No | Key-value pairs of event data |

## **Simple Example**

// User initiates a search

analytics.track('search\_initiated', {

  search\_term: 'fitness supplements',

  search\_results\_count: 1523

});

# **4\. Property Types**

| Type | JavaScript | Example |
| :---- | :---- | :---- |
| String | 'value' | search\_term: 'fitness' |
| Number | 123 or 45.67 | results\_count: 1523 |
| Boolean | true / false | ad\_is\_affiliate: true |
| Date | ISO 8601 string | '2025-01-15T10:30:00Z' |

# **5\. Identity Management**

## **The User Lifecycle**

Anonymous Visitor → Signs Up → Logged In User → Logs Out → Anonymous Again

### **When User Signs Up or Logs In**

Call identify() to link anonymous activity to a known user:

// After successful signup/login

analytics.identify('usr\_12345', {

  email: user.email,

  user\_subscription\_status: 'free'

});

### **When User Logs Out**

analytics.reset();

**⚠️ IMPORTANT:** Always call identify() BEFORE track() for logged-in users.

# **6\. The 18 Core Events**

These are the only events you need to implement. We've reduced from 44 to 18 following the workbook's principle: "Track Airbnb business with only 8 events."

## **User Events (5)**

| Event | Trigger | Where |
| :---- | :---- | :---- |
| user\_homepage\_visited | User lands on homepage | Client |
| user\_created | Account registration completed | Backend |
| user\_onboarding\_completed | Questionnaire \+ tutorial done | Backend |
| user\_deleted | Account deleted | Backend |
| user\_support\_contacted | Support request submitted | Backend |

## **Search Events (2)**

| Event | Trigger | Where |
| :---- | :---- | :---- |
| search\_initiated | User performs search | Client |
| search\_refined | User filters or sorts results | Client |

## **Subscription Events (5)**

| Event | Trigger | Where |
| :---- | :---- | :---- |
| subscription\_trial\_started | 24-hour trial begins | Backend |
| subscription\_created | First payment completed | Backend |
| subscription\_renewed | Payment renewed | Backend |
| subscription\_payment\_failed | Payment failed | Backend |
| subscription\_cancelled | User cancels | Backend |

# **7\. Common Mistakes to Avoid**

### **❌ Misspelled Event Names**

// WRONG

analytics.track('search\_intiated', {...});  // Typo

// CORRECT

analytics.track('search\_initiated', {...});

### **❌ Wrong Property Types**

// WRONG \- String instead of number

{ search\_results\_count: '1523' }

// CORRECT \- Number

{ search\_results\_count: 1523 }

### **❌ Nested Objects**

// WRONG \- Nested object

{ filters: { category: 'health' } }

// CORRECT \- Flat properties

{ filter\_category: 'health' }

# **8\. Testing & Validation**

## **Enable Debug Mode**

analytics.debug(true);

## **Validation Checklist**

1. Event name is exact (copy from tracking plan)  
2. All required properties are present  
3. Property names are exact  
4. Property types are correct (string, number, boolean)  
5. No nested objects in properties  
6. identify() called before track() for logged-in users  
7. Event appears in Segment debugger

# **9\. Quick Reference**

## **Event Call Structure**

analytics.track('entity\_activity', {

  entity\_property: 'value',

  another\_property: 123

});

## **Identity Flow**

// On signup/login

analytics.identify('user\_id', { traits });

analytics.track('user\_created', { properties });

// On logout

analytics.reset();

—  
*Questions? Check the VidTao\_Tracking\_Plan\_v3\_LEAN.xlsx*  
*Remember: Accurate tracking → Better insights → Better product decisions*