# 💍 WeddingCraft (विवाह-शिल्प)
### *Modular Wedding Website Maker & Multi-Platform Deployment Engine*

**WeddingCraft** transforms traditional static digital wedding cards into a **modular, themeable, zero-cost wedding website platform**. 

> **Note:** The wedding celebration of **चि. मनीष संग सौ. कां. साक्षी** serves as the flagship reference profile for this platform. Anyone can use WeddingCraft to generate and host a bespoke wedding website in minutes.

---

## 🌟 Key Highlights & Capabilities

- 🎨 **6 Cultural & Royal Theme Presets**:
  - `ivory`: Light, minimal royal cream & gold
  - `kesariya`: Festive marigold yellow & saffron
  - `pichwai`: Traditional lotus sage green & gold
  - `rajasthani`: Regal midnight palace navy & gold
  - `sindoori`: Auspicious traditional vermilion & gold
  - `emerald`: Luxury deep emerald & champagne gold

- 🏛️ **Visual Architecture & Design Archetypes (6-Axis Studio)**:
  - **Hero Layouts**:
    - `haveli`: Royal Rajputi / Mughal Jharokha arch with Sanskrit invocation.
    - `vogue`: High-fashion magazine cover with masthead typography & full-bleed couple portrait.
    - `cinema`: 16:9 cinematic video reel with letterboxing, aura glow & subtitle ticker.
    - `split`: Dual arched groom & bride windows with central interlocking monogram seal.
  - **Ceremony Itinerary Formats**:
    - `timeline`: Royal golden spine thread with alternating ceremony cards.
    - `carousel`: Storybook 3D swipeable coverflow cards with touch/button controls.
    - `grid`: Asymmetric high-fashion editorial lookbook grid with watermark numerals (`01`, `02`).
  - **Photo Gallery Presentations**:
    - `polaroid`: Vintage polaroid cards with organic randomized tilt and handwritten captions.
    - `filmstrip`: 35mm cinematic film reel with sprocket perforations and vignette shading.
    - `masonry`: Editorial lookbook multi-column grid.
  - **Typography Pairing Systems**:
    - `heritage`: Royal Classical (Yatra One / Tiro Devanagari Hindi).
    - `editorial`: High-Fashion Vogue (Cormorant Garamond / Cinzel Decorative).
    - `romantic`: Romantic Calligraphy (Great Vibes / Playfair Display).
    - `minimal`: Contemporary Minimal (Montserrat Clean).
  - **Volumetric Lighting & Atmospheric Shading**:
    - `spotlight`: Focused golden stage spotlighting with radial depth.
    - `candlelight`: Warm flickering palace candlelight glow.
    - `golden_hour`: Radiant sunset amber haze.
    - `velvet`: Midnight jewel-tone deep velvet ambiance.
  - **Atmosphere Particle Dynamics (After Effects-grade Canvas Physics)**:
    - `gold_dust`: Shimmering multi-layer bokeh dust with sinusoidal glow.
    - `petals`: 3D tumbling rose/marigold petals with rotation and sway physics.
    - `lanterns`: Warm glowing diya lanterns gently floating upward.

- 🧩 **27 Modular Block Capabilities**:
  - **Envelope & Wax Seal**: Interactive 3D flap opening, flower shower, and personalized seal monogram.
  - **Muhurat & Auspicious Countdown**: Live countdown timer with auspicious Hindu muhurat tags.
  - **Personalized Guest Salutations (`?to=Guest+Name&fam=1`)**: Welcomes specific guests by name upon opening.
  - **Multi-day Events Itinerary**: Expandable ceremonies with direct **"Add to Google Calendar"** & Apple Calendar sync.
  - **Attire & Dress Code**: Visual color palette circles for every ceremony.
  - **Logistics & 1-Tap Cab Ride**: Direct Google Maps direction links, venue QR codes, and **Uber/Ola 1-tap ride buttons**.
  - **Dual-Mode RSVP**:
    - **1-Click WhatsApp RSVP**: Instant pre-filled confirmation sent directly to the host's WhatsApp.
    - **Serverless Endpoint RSVP**: For Google Sheets or custom webhooks.
  - **Live Blessings & Guestbook**: Interactive wishes board with emoji/shloka reactions and local storage persistence.
  - **Floating Ambient Audio**: Romantic Shehnai & Indian classical melodies with smooth auto-fade volume controls.

---

## 🛠️ Quickstart

### 1. Launch In-Browser Visual Studio & Control Center
Run the local unified server:

```bash
python server.py 8000
```
- **Unified Control Center & Design Studio:** `http://localhost:8000/` (or `http://localhost:8000/control_center.html`)
- **Direct Live Invitation:** `http://localhost:8000/w/manish-sakshi`
- **Dynamic Profile Preview:** `http://localhost:8000/w/aarav-diya`
- **Guest Personalized Preview:** `http://localhost:8000/w/manish-sakshi?to=Sharma+Ji&fam=1`
- **Classic Visual Studio:** `http://localhost:8000/studio.html`

---

## 💻 CLI Commands (`maker.py`)

WeddingCraft comes with a zero-dependency Python 3 CLI tool:

| Command | Description | Example |
| :--- | :--- | :--- |
| `python maker.py list` | Lists all available wedding profiles and deployable folders | `python maker.py list` |
| `python maker.py scaffold <slug>` | Scaffolds a new independent wedding folder | `python maker.py scaffold rahul-priya` |
| `python maker.py parse-text <file>` | Converts raw WhatsApp invite text into an instant live site | `python maker.py parse-text whatsapp_invite.txt --wedding manish-sakshi` |
| `python maker.py scrape <url>` | Scrapes any digital wedding card via android-browser or URL | `python maker.py scrape https://example.com/card --wedding rohit-priya` |
| `python maker.py build --wedding <slug>` | Builds a self-contained deployable wedding folder | `python maker.py build --wedding manish-sakshi` |
| `python maker.py bundle-standalone --wedding <slug>` | Packages into a single 100% offline HTML file | `python maker.py bundle-standalone --wedding manish-sakshi` |
| `python maker.py guests --wedding <slug> --list guests.txt` | Generates individualized WhatsApp broadcast links | `python maker.py guests --wedding manish-sakshi --list sample_guests.txt` |
| `python maker.py deploy --wedding <slug> --target (github\|cloudflare)` | Generates deployment configuration for that specific folder | `python maker.py deploy --wedding manish-sakshi --target cloudflare` |
| `python maker.py serve --wedding <slug>` | Serves only that specific wedding folder | `python maker.py serve --wedding manish-sakshi --port 8000` |

---

## 🚀 Deployment Options (Zero Cost Hosting)

### 1. GitHub Pages (Automated Push-to-Deploy)
The repository includes a ready-to-run GitHub Actions workflow:
- Path: [`.github/workflows/deploy-pages.yml`](file:///storage/emulated/0/workspace/wedding/.github/workflows/deploy-pages.yml)
- To activate:
  1. Push code to your GitHub repo on branch `main`.
  2. In your repo on GitHub: **Settings -> Pages -> Build and deployment -> Source: GitHub Actions**.
  3. Your wedding website is live with HTTPS and custom domain support!

### 2. Cloudflare Pages
- Connect your GitHub repository to Cloudflare Pages.
- Build command: *(leave empty)*.
- Output directory: `.` or `dist`.

### 3. Standalone Offline HTML Bundle
Generate a single self-contained HTML file:
```bash
python maker.py bundle-standalone --profile profiles/manish-sakshi.json --output dist/invite.html
```
The resulting `dist/invite.html` file requires no web server and can be sent over WhatsApp, Telegram, or AirDrop to open directly on any smartphone!

---

## 📁 Repository Structure

```
wedding/
├── weddings/                      # Independent, self-contained wedding sites
│   ├── manish-sakshi/             # Manish & Sakshi deployable folder
│   └── arjun-ananya/              # Arjun & Ananya deployable folder
├── profiles/                      # Source wedding profiles (JSON)
│   ├── manish-sakshi.json         # Flagship Rajasthani Vedic wedding
│   └── arjun-ananya.json          # Contemporary Udaipur fusion wedding
├── schema/
│   └── wedding.schema.json        # Formal JSON Schema specification
├── themes/                        # CSS design tokens & cultural styles
│   ├── ivory.css                  # Light minimal elegance (default)
│   ├── kesariya.css               # Marigold festive
│   ├── pichwai.css                # Lotus pink & sage
│   ├── rajasthani.css             # Midnight palace & gold
│   ├── sindoori.css               # Auspicious vermilion
│   └── emerald.css                # Royal emerald & champagne gold
├── index.html                     # Modular client engine & invite viewer
├── studio.html                    # In-browser visual customizer & previewer
├── maker.py                       # CLI builder, bundler & deployment expert
├── config.json                    # Active profile config
├── .github/workflows/             # Automated deployment workflows
└── dist/                          # Generated bundles & standalone builds
```

---

## 📑 Complete Functions & Modules Reference List

| Module / Function | Key Config Parameters | Description |
| :--- | :--- | :--- |
| **`envelope`** | `couple.sealText`, `labels.welcome`, `labels.sealHint` | 3D wax-seal envelope opener with flower shower animation and monogram. |
| **`text_stream`** | Invocation, couple names, prelude, manuhaar | Kinetic grapheme calligraphy stream with glowing gold caret cursor and tap-to-complete. |
| **`hero`** | `couple.groom`, `couple.bride`, `date` | Royal hero presentation with shimmering gold lettering and auspicious date badge. |
| **`countdown`** | `date.iso`, `labels.countdown` | Real-time live countdown timer (days, hours, minutes, seconds) with pulse animation. |
| **`guest_personalizer`** | URL params `?to=Name&fam=1` | Dynamic guest greeting card: *"आदरणीय [Guest Name] जी, आपको सपरिवार सादर आमंत्रित करते हैं"*. |
| **`lineage` / `story`** | `couple.groom.lineage`, `couple.bride.lineage` | Traditional ancestry lineage cards in Rajasthan palace haveli arches. |
| **`events`** | `events[].name, time, location, image, dressCode` | Interactive ceremony cards featuring high-res occasion photos, date badge, and expandable drawer. |
| **`calendar_sync`** | `calendarStart`, `calendarEnd` | Direct 1-tap "Add to Google Calendar" & Apple Calendar sync for each ceremony. |
| **`dress_code`** | `events[].dressCode.title, palette[]` | Color palette swatches for ceremony dress codes (e.g. Haldi yellow, Sangeet glam, Wedding silk). |
| **`venue`** | `venue.name, address, mapUrl, uberUrl, barat, stay` | Interactive haveli venue frame with live Google Maps link, venue QR code, and transit instructions. |
| **`uber_shortcuts`** | `venue.uberUrl` | 1-tap **"Book Uber / Ride to Venue"** deep-link with destination preset. |
| **`gallery`** | `gallery[].src, caption` | Responsive photo grid with tap-to-zoom full-screen lightbox. |
| **`wishes` (Guestbook)** | `guestbook.enabled, heading` | Live blessings message wall with celebratory emoji buttons (`💐`, `🙏`, `✨`, `💖`, `卐`) and local storage. |
| **`family`** | `family[].title, members` | Multi-column grid of respected family elders, hosts, and relatives. |
| **`manuhaar`** | `manuhaar.verse, kids[]` | Traditional kids' welcoming verse and blessings from the little ones. |
| **`rsvp`** | `rsvp.whatsappPhone, endpoint` | Dual-mode RSVP: **1-Click WhatsApp RSVP** to host's phone + Serverless endpoint. |
| **`music_player`** | `music.src, autoplay, volume` | Ambient Shehnai & Indian classical melodies with gentle volume control (default 0.25). |
| **`standalone_bundler`**| `maker.py bundle-standalone` | Compiles CSS, JS, and config into a single zero-dependency offline HTML file. |
| **`guest_link_maker`** | `maker.py guests --list guests.txt` | Generates individualized WhatsApp broadcast links for every guest. |
