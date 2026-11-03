# Google Sheets RSVP Backend — Setup Guide

## 5-Minute Setup (per wedding)

### Step 1: Create a Google Sheet
1. Go to [sheets.new](https://sheets.new) — creates a blank spreadsheet
2. Name it: `RSVP — Manish & Sakshi` (or the couple's names)

### Step 2: Add the Apps Script
1. In the Sheet, go to **Extensions → Apps Script**
2. Delete any existing code in `Code.gs`
3. Paste the entire contents of `google-sheets-rsvp.gs` from this project
4. Click **💾 Save** (Ctrl+S)

### Step 3: Deploy as Web App
1. Click **Deploy → New deployment**
2. Click the gear icon ⚙️ → select **Web app**
3. Set:
   - **Description:** `RSVP Backend`
   - **Execute as:** `Me` (your Google account)
   - **Who has access:** `Anyone`
4. Click **Deploy**
5. Authorize access when prompted (Google will warn about unverified app — click Advanced → Go to project)
6. **Copy the Web App URL** — it looks like:
   ```
   https://script.google.com/macros/s/AKfycb.../exec
   ```

### Step 4: Configure the Wedding
Paste the URL into the wedding's `config.json`:
```json
{
  "rsvp": {
    "enabled": true,
    "endpoint": "https://script.google.com/macros/s/AKfycb.../exec",
    "whatsappPhone": "919414972688"
  }
}
```

With both `endpoint` and `whatsappPhone` set:
- The **Submit button** sends data to Google Sheets (silent, instant)
- The **WhatsApp button** still works as a direct confirmation channel
- Guests can use either or both

### Step 5: Test It
1. Open the wedding website
2. Fill in the RSVP form and click Submit
3. Check your Google Sheet — a new row should appear with all fields:
   - Timestamp, Guest Name, Phone, Guest Count, Events, Diet, Song Request, Message, Wedding

## What Gets Logged

| Column | Source |
|--------|--------|
| Timestamp | Auto-generated ISO timestamp |
| Guest Name | `rName` input (pre-filled from `?to=` URL param) |
| Phone | `rPhone` input |
| Guests Count | `rGuests` dropdown (1-5+) |
| Attending Events | Checked ceremony checkboxes |
| Dietary Preference | `rDiet` dropdown |
| Song Request | `rSong` input |
| Message | `rMsg` textarea |
| Wedding | Couple names from config |

## Per-Tier Usage

| Tier | RSVP Mode | Config |
|------|-----------|--------|
| **Tier 1** (WhatsApp Express) | WhatsApp only | `endpoint: ""` + `whatsappPhone: "91..."` |
| **Tier 2** (Royal Interactive) | Both Sheets + WhatsApp | `endpoint: "https://..."` + `whatsappPhone: "91..."` |
| **Tier 3** (Imperial Bespoke) | Both Sheets + WhatsApp | Same as Tier 2, dedicated sheet per wedding |

## Sharing the Sheet with Clients
1. In Google Sheets, click **Share**
2. Add the couple/family's email as **Viewer** (or **Editor** if they want to manage it)
3. The family can see RSVPs in real-time on their phone via the Google Sheets app

## Updating the Script
If you redeploy after changes:
1. In Apps Script, click **Deploy → Manage deployments**
2. Click ✏️ edit on the active deployment
3. Set version to **New version**
4. Click **Deploy**
5. The URL stays the same — no config change needed
