

# **Understanding the VidTao Ontology**

A Business Guide to Our Data Architecture

*What it is, why it matters, and how it powers our analytics*

Version 1.0 | December 2025

# **Executive Summary**

This document explains VidTao's ontology — a structured map of our business domain that serves as the foundation for all our data and analytics. Think of it as the 'dictionary' that defines what things exist in our business and how they relate to each other.

**Why does this matter?**

* **Shared Language:** Everyone in the company uses the same definitions for 'User', 'Subscription', 'Churn', etc.  
* **Better Analytics:** Our tracking and metrics are built on a solid foundation, not ad-hoc definitions.  
* **Faster Development:** Engineers know exactly what data exists and how to access it.  
* **Reliable Reporting:** Finance, Product, and Marketing all work from the same source of truth.

# **What is an Ontology?**

An ontology is a formal description of knowledge within a domain. In simple terms, it answers two questions:

1. **What things exist in our world?** (Users, Subscriptions, Ads, etc.)  
2. **How do they relate to each other?** (A User owns a Subscription, a User creates Swipe Boards, etc.)

***A Simple Analogy***

*Think of the ontology like a city map. The map shows what buildings exist (schools, hospitals, shops) and how roads connect them. The map doesn't contain the actual buildings — it describes what exists and how to navigate between them. Similarly, our ontology describes our data landscape without containing the actual data.*

# **The Palantir Foundry Approach**

We follow the Palantir Foundry methodology for building our ontology. This is an industry-leading approach used by Fortune 500 companies to organize their data. It has four core concepts:

## **1\. Object Types (The 'Nouns')**

Object types represent real-world entities in our business. These are the 'things' that exist.

| Object Type | What It Represents |
| :---- | :---- |
| **User** | A person who has created an account on VidTao |
| **Subscription** | The billing relationship between a User and VidTao (via Stripe) |
| **Swipe Board** | A collection/folder of saved ads created by a User |
| **Ad** | A YouTube video advertisement in our database |
| **Search** | A search query performed by a User against our ad database |
| **Training** | Educational content (tutorials, guides) for users |

## **2\. Properties (The 'Attributes')**

Properties describe the characteristics of each object type. For example, a User has:

* **user\_id** — Unique identifier  
* **email** — Contact information  
* **subscription\_status** — Current state (free, trial, active, churned)  
* **monthly\_adspend** — Self-reported ad budget (from onboarding)  
* **first\_value\_moment** — When they first saved or downloaded an ad

## **3\. Link Types (The 'Relationships')**

Link types describe how object types connect to each other:

* User **OWNS** Subscription (1 user has 0 or 1 subscription)  
* User **CREATES** Swipe Board (1 user can create many boards)  
* Swipe Board **CONTAINS** Ad (boards contain many ads, ads can be in many boards)  
* User **DOWNLOADS** Ad (users can download many ads)

## **4\. Action Types (The 'Verbs')**

Action types describe how objects can be modified. These map directly to our analytics events:

| Action | What Happens | Tracked As |
| :---- | :---- | :---- |
| Create User | New account created | user\_created |
| Start Trial | User begins 24h trial | subscription\_trial\_started |
| Add Ad to Board | User saves an ad | swipe\_board\_updated |
| Download Ad | User downloads asset | ad\_downloaded |
| Cancel Subscription | User cancels | subscription\_cancelled |

# **How It Works in Practice**

## **The Two Layers**

Our data architecture has two complementary layers:

### **Semantic Layer (The Ontology)**

This is the 'state' layer — it describes what exists *right now*. If you ask 'How many active subscribers do we have today?' — the ontology answers this.

* Stored in: Database tables, Stripe  
* Updated: Continuously as things change  
* Example: User John has subscription\_status \= 'active'

### **Kinetic Layer (The Tracking Plan)**

This is the 'behavior' layer — it describes what *happened*. If you ask 'How did our conversion rate change this month?' — tracking answers this.

* Stored in: Analytics platform (Amplitude, Mixpanel)  
* Captured: When actions occur (events)  
* Example: John triggered 'subscription\_created' on Jan 15, 2025

  ***Key Insight:** The ontology tells you WHAT a user IS (subscriber). Tracking tells you WHAT a user DID (subscribed). Together, they give you the complete picture.*

## **Example: Following a User Journey**

Let's trace Sarah's journey through VidTao using both layers:

1. **Sarah finds VidTao via Google Ads**  
   *Tracking:* user\_homepage\_visited (utm\_source='google', utm\_medium='cpc')  
2. **Sarah creates an account**  
   *Ontology:* New User object created (user\_id='usr\_sarah', subscription\_status='free')  
   *Tracking:* user\_created  
3. **Sarah searches for 'fitness supplements' and saves 3 ads**  
   *Ontology:* New Search object, new Swipe\_Board object, 3 Ad links created  
   *Tracking:* search\_initiated, swipe\_board\_created, swipe\_board\_updated (x3)  
4. **Sarah starts her 24-hour trial**  
   *Ontology:* User.subscription\_status changes to 'trial', Subscription object created  
   *Tracking:* subscription\_trial\_started  
5. **Sarah converts to paid monthly**  
   *Ontology:* User.subscription\_status changes to 'active', Subscription.status='active'  
   *Tracking:* subscription\_created (plan='monthly', amount=99.00)

# **Business Benefits**

## **For Finance**

* **MRR Calculation:** Clear definition of which subscriptions count toward MRR  
* **Churn Analysis:** subscription\_cancelled event with cancel\_reason property  
* **Revenue Attribution:** subscription\_created links back to User with original utm\_source

## **For Product**

* **Feature Usage:** How many users create Swipe Boards? How many ads per board?  
* **Activation Metrics:** first\_value\_moment property shows when users find value  
* **Engagement Depth:** Searches per user, downloads per user, boards per user

## **For Marketing**

* **Acquisition Analysis:** utm\_source, utm\_medium, utm\_campaign on every User  
* **Funnel Metrics:** Homepage → Signup → Trial → Paid conversion rates  
* **Cohort Analysis:** Compare behavior of users from different campaigns

## **For Engineering**

* **Clear Data Model:** Know exactly what tables exist and how they relate  
* **Source Mapping:** Know where each data point comes from (Stripe, internal DB, etc.)  
* **Consistent Naming:** user\_id everywhere, not id, userId, user\_identifier

# **Key Business Definitions**

The ontology establishes these official definitions:

| Term | Official Definition |
| :---- | :---- |
| **Active Subscriber** | User where Subscription.status \= 'active' AND Subscription.cancel\_at\_period\_end \= false |
| **Churned User** | User who had Subscription.status \= 'active' and now has 'canceled' or no active subscription |
| **First Value Moment** | Timestamp of first swipe\_board\_updated (ad\_added) OR ad\_downloaded event for a User |
| **Activated User** | User who has first\_value\_moment IS NOT NULL (has saved or downloaded at least one ad) |
| **At-Risk User** | Active Subscriber with: payment\_failed in last 30 days OR no value actions in last 14 days |
| **MRR** | SUM of (Subscription.amount / 12 if yearly else Subscription.amount) for all active subscriptions |

# **Related Documents**

This guide works together with these other documents:

| Document | Purpose |
| :---- | :---- |
| [**VidTao\_Ontology\_Document.xlsx**](https://docs.google.com/spreadsheets/d/1EpdollO4iObtjuoCIx6LD4ZL1OMKxxEC/edit?gid=588887392#gid=588887392) | Full technical specification of all object types, properties, links, actions, and source mappings |
| [**VidTao\_Tracking\_Plan\_v3.xlsx**](https://docs.google.com/spreadsheets/d/16UVyCf1zMXmrNoa_So5SVdr_N16RhjTw/edit?gid=2111675562#gid=2111675562) | Event tracking specification — all 18 core events with properties |
| [**VidTao\_Implementation\_Guide.docx**](https://docs.google.com/document/d/1bvrX-3DCdNwQ-Kg3OlnAFm0pC4I-gsUT/edit) | Developer guide for implementing event tracking with code examples |

# **Questions?**

If you have questions about the ontology or need help understanding how data is organized:

* For business definitions: Contact Product team  
* For data sources: Contact Data/Engineering team  
* For analytics questions: Contact Analytics team

—  
*The ontology is a living document. As our business evolves, so will our data model.*