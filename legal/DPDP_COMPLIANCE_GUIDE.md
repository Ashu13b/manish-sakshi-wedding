# 🛡️ Operator & Agency Guide: DPDP Act, 2023 Compliance
**For:** WeddingCraft Platform Operators, Wedding Planners & Agency Designers  
**Focus:** Handling Wedding Client Data, Guest Lists & RSVP Records Safely in India  

---

## 1. What is the DPDP Act, 2023?
The **Digital Personal Data Protection Act, 2023 (DPDP Act)** is India's principal data protection law. It governs any processing of digital personal data within India and applies directly to wedding websites, guest lists, and online RSVP platforms.

---

## 2. Practical "Do's and Don'ts" for WeddingCraft Operators

### ✅ DO:
1. **Always obtain the signed Client Onboarding Waiver:**  
   Before publishing any wedding website live on the web, ensure the family signs or digitally confirms the [`CLIENT_ONBOARDING_WAIVER.md`](file:///storage/emulated/0/workspace/wedding/legal/CLIENT_ONBOARDING_WAIVER.md).
2. **Use Synthetic / Fictional Personas for Public Demos:**  
   Never use living celebrity names or real past clients' personal phone numbers and home addresses in marketing materials, social media videos, or portfolio galleries. Use 100% synthetic/fictional personas for all demos (e.g., *Aarav & Diya*, *Kabir & Ananya*).
3. **Respect Purpose Limitation:**  
   Guest phone numbers gathered via the RSVP form or guest link generator must **only** be shared with the host family for wedding coordination. Never add them to agency marketing lists or resale databases.
4. **Offer Password / PIN Protection for Private Families:**  
   For HNI clients who do not want public internet discovery, offer PIN gating (`?pin=1234`) or deliver the offline standalone HTML bundle (`maker.py bundle-standalone`).
5. **Honor Guest Deletion Requests:**  
   If an invited guest asks to be removed from the public wishes/guestbook wall or RSVP records, delete their entry within 48 hours.

### ❌ DON'T:
1. **Never hotlink private cloud URLs:**  
   Do not hotlink to private cloud buckets or scrape live cards without scrubbing personal PII.
2. **Never expose administrative spreadsheets publicly:**  
   Ensure Google Sheets tracking RSVP headcounts are set to private view and shared strictly with the bride and groom's designated email addresses.
3. **Never include sensitive financial or Aadhaar data:**  
   Wedding websites must never solicit banking credentials, credit card numbers, or government IDs. Only standard public UPI IDs (`payee@upi`) for voluntary shagun gifting may be displayed if explicitly requested by the host.

---

## 3. Post-Wedding Archival & Deletion SOP
1. **At T + 30 Days post-wedding:**  
   Send the couple their complete RSVP export (CSV / PDF report).
2. **At T + 90 Days post-wedding:**  
   If the couple does not purchase extended hosting, unpublish the public subdomain on Cloudflare Pages and securely archive the project JSON.
