# 🛡️ WeddingCraft Privacy Policy & Data Protection Framework
**Effective Date:** 1 November 2026  
**Governing Laws:** Digital Personal Data Protection Act, 2023 (DPDP Act, India) · Information Technology Act, 2000 & IT Rules, 2011 · General Data Protection Regulation (GDPR - EU) for international attendees.

---

## 1. Overview & Scope
This Privacy Policy outlines how **WeddingCraft** ("Platform", "we", "us", or "our"), functioning primarily as a **Data Processor** on behalf of the Wedding Host / Family ("Data Fiduciary"), processes, secures, and handles personal data submitted through our digital wedding invitation websites, standalone HTML packages, and RSVP modules.

---

## 2. Roles Under the DPDP Act, 2023
- **Data Fiduciary:** The Wedding Couple / Host Family (e.g., *Manish & Sakshi Family*) who determines the purpose and means of collecting guest attendance, greetings, and wedding logistics.
- **Data Processor:** WeddingCraft, which provides the technology platform, hosting infrastructure, and styling engine strictly upon the instructions of the Data Fiduciary.
- **Data Principals:** Wedding guests, invitees, and family members who access the invitation, view ceremonies, and submit RSVP confirmations or greetings.

---

## 3. Categories of Personal Data Processed

| Category | Data Elements | Source | Purpose of Processing |
| :--- | :--- | :--- | :--- |
| **Host / Couple Data** | Couple names, ancestral lineage, parental names, ceremony dates, addresses, contact numbers. | Host Family | Constructing the invitation card, timeline, and directions. |
| **Guest Salutation Data** | Guest name passed via URL parameters (e.g. `?guest=Sharma+Ji&fam=1`). | Host Family's broadcast list | Dynamic personalization on the virtual envelope and VIP pass. |
| **RSVP & Attendance Data** | Guest Name, Mobile Number, Attending Event(s), Headcount, Dietary Choice, DJ Song Request, Message. | Guest Submission | Headcount planning, catering logistics, seating, and family greetings. |
| **Technical Telemetry** | Viewport dimensions, browser type, anonymous love reaction count. | Client Device | Responsive layout rendering and animation performance (Zero third-party trackers). |

> [!IMPORTANT]
> **Zero Third-Party Advertising:** WeddingCraft **never** sells, rents, monetizes, or shares guest data with third-party advertisers, ad networks, or data brokers.

---

## 4. Lawful Basis & Explicit Consent
- **Host Consent:** Hosts enter into a service agreement and onboarding waiver authorizing the publication of their wedding itinerary and contact numbers.
- **Guest Consent:** When guests submit their RSVP or greetings, an explicit consent notice is presented: *"Your information is collected solely for host family event coordination in compliance with the DPDP Act, 2023."*
- **Notice & Withdrawal:** Any guest may withdraw their RSVP or request deletion of their submitted greetings at any time by contacting the Data Fiduciary or our Grievance Officer.

---

## 5. Data Storage, Security & Retention

### A. Hosting Infrastructure
- **Cloudflare Pages:** Hosted on Cloudflare's secure, enterprise-grade global edge network with TLS 1.3 encryption, DDoS mitigation, and HTTPS-only delivery.
- **Offline HTML Bundles:** Standalone `.html` files reside 100% locally on the recipient's mobile device with **zero server storage**.

### B. RSVP Data Architecture
- **WhatsApp RSVP (Default):** Guest RSVP submissions are transmitted directly to the host family's WhatsApp number via the WhatsApp Web API. WeddingCraft does not intercept, store, or have access to these RSVP messages. The host family is the sole custodian of RSVP data received via WhatsApp.
- **Google Sheets RSVP (Tier 2/3):** When a Google Sheets endpoint is configured by the host, RSVP submissions are logged to the host family's own Google Sheets document. WeddingCraft may have temporary access during setup but the spreadsheet is owned and controlled by the host family.
- **Guest Wishes / Guestbook:** Blessing messages submitted via the on-page guestbook are stored in the visitor's own browser (localStorage). They are not transmitted to any server. WeddingCraft has no access to locally stored wishes.

### C. Retention Policy
- Active wedding websites are maintained for the duration agreed with the host (typically 30 to 180 days post-wedding).
- Since WeddingCraft operates as a static hosting platform with no server-side database, guest RSVP records reside exclusively with the host family (via WhatsApp or Google Sheets). Unpublishing the wedding website removes the static site from Cloudflare Pages; no guest data is retained by WeddingCraft post-unpublish.

---

## 6. Rights of Data Principals (Guests & Hosts)
Under the DPDP Act, 2023, every user has the following statutory rights:
1. **Right to Access:** Request a summary of personal data held about you.
2. **Right to Correction & Erasure:** Request correction of inaccurate information or deletion of your RSVP / greetings.
3. **Right of Grievance Redressal:** Right to register a formal grievance with the designated Grievance Officer.
4. **Right to Nominate:** In the event of death or incapacity, nominate another individual to exercise data rights.

---

## 7. Compliance Contact & Grievance Officer
In accordance with Rule 3(11) of the Information Technology (Intermediaries Guidelines) Rules, 2011 and Section 10 of the DPDP Act, 2023, the Grievance Officer details are:

- **Designation:** Data Protection & Grievance Redressal Officer
- **Platform:** WeddingCraft Modular Platform Engine
- **Email:** `ay.yadav53@gmail.com` *(Interim contact until brand domain is registered)*
- **Jurisdiction:** Jaipur / Sikar, Rajasthan, India
- **Response Timeline:** Acknowledged within 24 hours; resolved within 7 business days.

> **Note for Operator:** Replace the interim email above with `privacy@weddingcraft.in` once the brand domain is registered and email forwarding is configured.
