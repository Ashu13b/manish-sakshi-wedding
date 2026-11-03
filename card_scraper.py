#!/usr/bin/env python3
"""
WeddingCraft Card Scraper & Importer Bridge
Connects to sibling 'android-browser' (OpenScrape) to scrape live digital wedding cards,
or falls back to direct HTTP extraction, parsing raw wedding pages into deployable WeddingCraft sites.

Usage:
    python card_scraper.py <url> [--wedding <slug>] [--deploy]
"""

import sys
import os
import re
import json
import shutil
import urllib.request
import urllib.parse
from html.parser import HTMLParser
from typing import Dict, Any, Optional, List

# Add sibling android-browser library to path
SIBLING_BROWSER_DIR = "/storage/emulated/0/workspace/android-browser"
if os.path.exists(SIBLING_BROWSER_DIR) and SIBLING_BROWSER_DIR not in sys.path:
    sys.path.append(SIBLING_BROWSER_DIR)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PROFILES_DIR = os.path.join(ROOT_DIR, "profiles")
WEDDINGS_DIR = os.path.join(ROOT_DIR, "weddings")

class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.in_title = False
        self.meta = {}
        self.json_ld = []
        self.in_script = False
        self.script_type = ""
        self.script_buf = []
        self.images = []
        self.text_chunks = []
        self.links = []
        self.ignore_tags = {'script', 'style', 'noscript', 'svg', 'iframe'}
        self.current_tag = None

    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        attr_dict = dict(attrs)

        if tag == "title":
            self.in_title = True
        elif tag == "meta":
            prop = attr_dict.get("property") or attr_dict.get("name")
            content = attr_dict.get("content")
            if prop and content:
                self.meta[prop.lower()] = content
        elif tag == "script":
            stype = attr_dict.get("type", "").lower()
            if "application/ld+json" in stype:
                self.in_script = True
                self.script_type = stype
                self.script_buf = []
        elif tag == "img":
            src = attr_dict.get("src")
            if src and not src.startswith("data:"):
                self.images.append(src)
        elif tag == "a":
            href = attr_dict.get("href")
            if href:
                self.links.append(href)

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        elif tag == "script" and self.in_script:
            self.in_script = False
            raw_json = "".join(self.script_buf).strip()
            try:
                self.json_ld.append(json.loads(raw_json))
            except Exception:
                pass
        self.current_tag = None

    def handle_data(self, data):
        text = data.strip()
        if not text:
            return
        if self.in_title:
            self.title += " " + text
        elif self.in_script:
            self.script_buf.append(data)
        elif self.current_tag not in self.ignore_tags:
            self.text_chunks.append(text)

class WeddingCardScraper:
    def __init__(self):
        self.browser_client = None
        self._init_browser_client()

    def _init_browser_client(self):
        try:
            from openscrape_client import MobileBrowserClient
            client = MobileBrowserClient(timeout=4)
            # Quick ping
            status = client.get_status()
            if status.get("status") == "ok":
                self.browser_client = client
                print("📱 OpenScrape Mobile Browser Bridge: CONNECTED (Port 38765)")
            else:
                print("ℹ️ OpenScrape browser RPC is idle. Using direct HTTP scraper engine.")
        except Exception:
            print("ℹ️ OpenScrape client offline. Using direct HTTP scraper engine.")

    def parse_whatsapp_invite(self, text: str, custom_slug: Optional[str] = None):
        """Parses a structured WhatsApp wedding invitation text into a WeddingCraft configuration."""
        print("💬 Parsing WhatsApp invitation text...")
        curated_photos = {
            "haldi": "https://images.unsplash.com/photo-1610030469983-98e550d6193c?auto=format&fit=crop&w=700&q=80",
            "bhaat": "https://images.unsplash.com/photo-1607190074257-dd4b7af0309f?auto=format&fit=crop&w=700&q=80",
            "preetibhoj": "https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=700&q=80",
            "sangeet": "https://images.unsplash.com/photo-1545232979-8bf68ee9b1af?auto=format&fit=crop&w=700&q=80",
            "barat": "https://images.unsplash.com/photo-1511285560929-80b456fea0bc?auto=format&fit=crop&w=700&q=80",
            "panigrahan": "https://images.unsplash.com/photo-1583939003579-730e3918a45a?auto=format&fit=crop&w=700&q=80",
            "wedding": "https://images.unsplash.com/photo-1583939003579-730e3918a45a?auto=format&fit=crop&w=700&q=80"
        }

        # 1. Groom
        g_name = "मनीष"
        m_groom = re.search(r'🤵\s*(?:चि\.\s*)?([^\n\(\)]+)', text)
        if m_groom:
            g_name = m_groom.group(1).strip()
        g_lineage = ""
        m_gl1 = re.search(r'\(सुपौत्र:?\s*([^\)]+)\)', text)
        m_gl2 = re.search(r'\(सुपुत्र:?\s*([^\)]+)\)', text)
        if m_gl1 or m_gl2:
            parts = []
            if m_gl1: parts.append(f"सुपौत्र — <strong>{m_gl1.group(1).strip()}</strong>")
            if m_gl2: parts.append(f"सुपुत्र — <strong>{m_gl2.group(1).strip()}</strong>")
            g_lineage = "<br>".join(parts)

        # 2. Bride
        b_name = "साक्षी"
        m_bride = re.search(r'👰\s*(?:सौ\.\s*कां\.\s*)?([^\n\(\)]+)', text)
        if m_bride:
            b_name = m_bride.group(1).strip()
        b_lineage = ""
        m_bl1 = re.search(r'\(सुपौत्री:?\s*([^\)]+)\)', text)
        m_bl2 = re.search(r'\(सुपुत्री:?\s*([^\)]+)\)', text)
        if m_bl1 or m_bl2:
            parts = []
            if m_bl1: parts.append(f"सुपौत्री — <strong>{m_bl1.group(1).strip()}</strong>")
            if m_bl2: parts.append(f"सुपुत्री — <strong>{m_bl2.group(1).strip()}</strong>")
            b_lineage = "<br>".join(parts)

        # 3. Date
        day, month, year, weekday = "21", "नवंबर 2026", "2026", "शनिवार"
        m_date = re.search(r'दिनांक\s*(\d{1,2})\s*([^\s,]+)\s*(202\d)(?:[,\s]+([^\s]+वार))?', text)
        if m_date:
            day = m_date.group(1).zfill(2)
            month = f"{m_date.group(2)} {m_date.group(3)}"
            year = m_date.group(3)
            if m_date.group(4):
                weekday = m_date.group(4).replace(",", "").strip()

        # 4. Ceremonies (Events)
        events = []
        ev_matches = re.findall(r'[🌿🌸🍽️🎶🐎🚌🔥\*\-•]?\s*([^:\-\n]+)[:\-]\s*(\d{1,2}\s*[^\s,]+(?:\s*202\d)?)[,\s]+([^\s\-]+)?\s*[-–]\s*([^\n]+)', text)
        for ev_name, ev_date_str, ev_day, ev_time in ev_matches:
            ev_name = ev_name.strip()
            ev_time = ev_time.strip()
            d_parts = ev_date_str.strip().split()
            e_day = d_parts[0] if len(d_parts) > 0 else day
            e_mon = d_parts[1] if len(d_parts) > 1 else "नवंबर"

            img = curated_photos["wedding"]
            dcode = None
            is_main = False

            if "हल्दी" in ev_name:
                img = curated_photos["haldi"]
                dcode = { "title": "पीत परिधान (Haldi Yellow)", "palette": ["#ffd54f", "#fbc02d", "#fff9c4"] }
            elif "लग्न" in ev_name or "भात" in ev_name:
                img = curated_photos["bhaat"]
            elif "प्रीतिभोज" in ev_name:
                img = curated_photos["preetibhoj"]
                dcode = { "title": "उत्सव परिधान (Festive Traditional)", "palette": ["#8a7850", "#a05050", "#f6f2ea"] }
            elif "संगीत" in ev_name:
                img = curated_photos["sangeet"]
                dcode = { "title": "चटक व सतरंगी (Vibrant Folk)", "palette": ["#e91e63", "#9c27b0", "#ff9800"] }
            elif "निकासी" in ev_name or "बारात" in ev_name:
                img = curated_photos["barat"]
            elif "पाणिग्रहण" in ev_name or "विवाह" in ev_name:
                img = curated_photos["panigrahan"]
                dcode = { "title": "राजपूती/शाही पोशाक (Royal Elegance)", "palette": ["#800020", "#d4af37", "#fdfbf7"] }
                is_main = True

            events.append({
                "date": e_day,
                "month": e_mon,
                "name": ev_name,
                "time": (f"{ev_day} · " if ev_day else "") + ev_time,
                "location": "भांडाला / नीमकाथाना",
                "image": img,
                "dressCode": dcode,
                "main": is_main
            })

        if not events:
            events = self._extract_events(text, [])

        # 5. Venue
        v_name = "लक्ष्मी मैरिज गार्डन"
        v_addr = "गुर्जर कॉलोनी, छावनी, नीमकाथाना"
        m_venue = re.search(r'📍\s*([^:\n]+)[:\s]*\n([^\n]+)', text)
        if m_venue:
            v_name = m_venue.group(1).replace("स्थल", "").strip()
            v_addr = m_venue.group(2).strip()

        m_map = re.search(r'(?:Google Maps|Maps)[:\s]*(https?://[^\s]+)', text)
        map_url = m_map.group(1).strip() if m_map else "https://maps.google.com"

        # 6. Manuhaar
        manuhaar = None
        m_man = re.search(r'👶\s*बाल मनुहार:?\s*\n"([^"]+)"\s*\n\s*[-–]\s*([^\n]+)', text)
        if m_man:
            verse = m_man.group(1).replace("\n", "<br>")
            kids = [k.strip() for k in m_man.group(2).split(",") if k.strip()]
            manuhaar = { "verse": f'"{verse}"', "kids": kids }

        # 7. Hosts
        hosts_names = []
        m_host = re.search(r'🙏\s*निमंत्रक:?\s*\n((?:[^\n]+\n?)+)', text)
        if m_host:
            raw_lines = [l.strip() for l in m_host.group(1).strip().split("\n") if l.strip()]
            hosts_names = raw_lines[:2] if len(raw_lines) >= 2 else raw_lines

        slug = custom_slug or f"{g_name.lower()}-{b_name.lower()}".replace(" ", "-")
        slug = re.sub(r'[^a-zA-Z0-9\-\u0900-\u097F]', '', slug) or "whatsapp-wedding"

        config = {
            "theme": "ivory",
            "lang": "hi",
            "meta": {
                "title": f"{g_name} संग {b_name} — राजसी विवाह निमंत्रण",
                "description": f"चि. {g_name} संग सौ. कां. {b_name} के मंगल परिणयोत्सव का शुभ निमंत्रण।",
                "ogTitle": f"{g_name} ❤ {b_name} — शुभ विवाह",
                "ogDescription": f"{day} {month} · आपको सपरिवार सादर आमंत्रित करते हैं।"
            },
            "modules": ["envelope", "hero", "countdown", "lineage", "events", "dress_code", "venue", "wishes", "family", "manuhaar", "rsvp"],
            "couple": {
                "groom": { "name": g_name, "prefix": "चि.", "label": "वर", "lineage": g_lineage },
                "bride": { "name": b_name, "prefix": "सौ. कां.", "label": "वधू", "lineage": b_lineage },
                "connector": "संग",
                "sealText": f"{g_name[0]}❤{b_name[0]}"
            },
            "date": {
                "iso": f"{year}-11-{day}T20:00:00+05:30",
                "day": day,
                "month": month,
                "weekday": weekday,
                "display": f"{day} {month}"
            },
            "invocation": {
                "top": "॥ श्री गणेशाय नमः ॥",
                "shlok": "ॐ वक्रतुण्ड महाकाय सूर्यकोटिसमप्रभ ।<br>निर्विघ्नं कुरु मे देव सर्वकार्येषु सर्वदा ॥"
            },
            "invitation": {
                "prelude": "मान्यवर, परमपिता परमात्मा की असीम अनुकम्पा से",
                "closing": "के <strong>मंगल परिणयोत्सव</strong> की मधुर बेला पर<br>आपको सपरिवार सादर आमंत्रित करते हैं।"
            },
            "events": events,
            "venue": {
                "name": v_name,
                "address": v_addr,
                "badge": f"{day} {month} · {weekday}",
                "mapUrl": map_url,
                "uberUrl": "https://m.uber.com/ul/?action=setPickup&pickup=my_location"
            },
            "manuhaar": manuhaar,
            "hosts": {
                "label": "निमंत्रक",
                "names": hosts_names or ["समस्त परिवार"],
                "address": "राजस्थान",
                "footer": "दर्शनाभिलाषी — समस्त परिवार व स्नेहीजन"
            },
            "music": {
                "src": "assets/shehnai.mp3",
                "label": "शहनाई",
                "stopLabel": "रोकें",
                "autoplay": False,
                "volume": 0.25
            },
            "rsvp": {
                "enabled": True,
                "mode": "whatsapp",
                "whatsappPhone": "",
                "heading": "क्या आप आ रहे हैं?"
            },
            "guestbook": {
                "enabled": True,
                "heading": "वर-वधू को शुभ आशीर्वाद"
            },
            "labels": {
                "countdown": "शुभ लग्न तक",
                "days": "दिन", "hours": "घंटे", "minutes": "मिनट", "seconds": "सेकंड",
                "eventsLabel": "卐 संस्कार बेलाएं 卐",
                "eventsHeading": "शुभ कार्यक्रम",
                "welcome": "सस्नेह निमंत्रण"
            }
        }
        return slug, config

    def import_text_and_build(self, text_or_path: str, custom_slug: Optional[str] = None) -> str:
        """Parses a WhatsApp invite or raw text and automatically builds a deployable site."""
        raw_text = text_or_path
        if os.path.exists(text_or_path) and os.path.isfile(text_or_path):
            print(f"📂 Reading WhatsApp invite from file: {text_or_path}")
            with open(text_or_path, "r", encoding="utf-8") as f:
                raw_text = f.read()

        slug, config = self.parse_whatsapp_invite(raw_text, custom_slug)

        # 1. Save Profile JSON
        profile_file = os.path.join(PROFILES_DIR, f"{slug}.json")
        os.makedirs(PROFILES_DIR, exist_ok=True)
        with open(profile_file, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        print(f"✅ Saved profile: profiles/{slug}.json")

        # 2. Build standalone Wedding Folder
        wedding_dir = os.path.join(WEDDINGS_DIR, slug)
        os.makedirs(wedding_dir, exist_ok=True)

        shutil.copy(os.path.join(ROOT_DIR, "index.html"), os.path.join(wedding_dir, "index.html"))
        shutil.copy(profile_file, os.path.join(wedding_dir, "config.json"))

        themes_src = os.path.join(ROOT_DIR, "themes")
        if os.path.exists(themes_src):
            shutil.copytree(themes_src, os.path.join(wedding_dir, "themes"), dirs_exist_ok=True)
        assets_src = os.path.join(ROOT_DIR, "assets")
        if os.path.exists(assets_src):
            shutil.copytree(assets_src, os.path.join(wedding_dir, "assets"), dirs_exist_ok=True)

        print(f"🎉 Fully generated deployable wedding site: weddings/{slug}/")
        print(f" • Couple:  {config['couple']['groom']['name']} संग {config['couple']['bride']['name']}")
        print(f" • Date:    {config['date']['display']}")
        print(f" • Events:  {len(config['events'])} ceremonies parsed with photos & dress codes")
        print(f" • Preview: python maker.py serve --wedding {slug}\n")
        return slug

    def fetch_page(self, url: str) -> Dict[str, Any]:
        """Fetches page content via android-browser, local file, or direct HTTP fallback."""
        print(f"🌐 Fetching wedding card from: {url}")

        # 0. Check if it's a local file path
        local_path = url.replace("file://", "") if url.startswith("file://") else url
        if os.path.exists(local_path) and os.path.isfile(local_path):
            print(f" 📂 Reading from local wedding card file: {local_path}")
            with open(local_path, "r", encoding="utf-8", errors="replace") as f:
                html = f.read()
            parser = PageParser()
            parser.feed(html)
            return {
                "html": html,
                "text": "\n".join(parser.text_chunks),
                "title": parser.title.strip(),
                "meta": parser.meta,
                "json_ld": parser.json_ld,
                "images": parser.images,
                "links": parser.links,
                "source": "local-file"
            }
        
        # 1. Try via Android Browser RPC if active
        if self.browser_client:
            try:
                print(" • Navigating via OpenScrape mobile browser...")
                self.browser_client.navigate(url)
                dom = self.browser_client.extract_dom(
                    include_text=True,
                    include_html=True,
                    include_links=True,
                    include_meta=True
                )
                if dom and (dom.get("html") or dom.get("text")):
                    print(" ✅ Successfully captured via OpenScrape Android Browser!")
                    return {
                        "html": dom.get("html", ""),
                        "text": dom.get("text", ""),
                        "meta": dom.get("meta", {}),
                        "links": dom.get("links", []),
                        "source": "android-browser"
                    }
            except Exception as e:
                print(f" ⚠️ Android Browser capture failed ({e}), falling back to HTTP...")

        # 2. Resilient Direct HTTP GET with realistic Mobile Headers
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "hi,en-US;q=0.9,en;q=0.8"
        }
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as res:
            raw_bytes = res.read()
            encoding = res.headers.get_content_charset() or "utf-8"
            html = raw_bytes.decode(encoding, errors="replace")

        parser = PageParser()
        parser.feed(html)
        page_text = "\n".join(parser.text_chunks)

        return {
            "html": html,
            "text": page_text,
            "title": parser.title.strip(),
            "meta": parser.meta,
            "json_ld": parser.json_ld,
            "images": [urllib.parse.urljoin(url, img) for img in parser.images],
            "links": [urllib.parse.urljoin(url, l) for l in parser.links],
            "source": "http-engine"
        }

    def parse_wedding_data(self, page_data: Dict[str, Any], url: str) -> Dict[str, Any]:
        """Parses extracted content into a WeddingCraft schema configuration."""
        text = page_data.get("text", "")
        meta = page_data.get("meta", {})
        title = page_data.get("title", "") or meta.get("og:title", "")

        print("🔍 Parsing wedding details (Couple, Date, Ceremonies, Venues)...")

        # 1. Detect Couple Names
        groom_name, bride_name, connector = self._extract_couple(title, text)

        # 2. Detect Wedding Date
        date_info = self._extract_date(text)

        # 3. Detect Events / Ceremonies
        events = self._extract_events(text, page_data.get("images", []))

        # 4. Detect Venue & Maps
        venue = self._extract_venue(text, page_data.get("links", []))

        # 5. Language detection (Hindi / English)
        has_devanagari = bool(re.search(r'[\u0900-\u097F]', text))
        lang = "hi" if has_devanagari else "en"
        theme = "ivory" if lang == "hi" else "pichwai"

        slug = f"{groom_name.lower()}-{bride_name.lower()}".replace(" ", "-")
        slug = re.sub(r'[^a-zA-Z0-9\-\u0900-\u097F]', '', slug) or "scraped-wedding"

        # Assemble config
        config = {
            "theme": theme,
            "lang": lang,
            "meta": {
                "title": f"{groom_name} {connector} {bride_name} — Wedding Celebration",
                "description": f"Wedding invitation of {groom_name} & {bride_name}.",
                "ogTitle": f"{groom_name} ❤ {bride_name}",
                "ogDescription": f"Join us to celebrate our wedding on {date_info.get('display', '')}.",
                "url": url
            },
            "modules": ["envelope", "hero", "countdown", "lineage", "events", "dress_code", "venue", "wishes", "rsvp"],
            "couple": {
                "groom": { "name": groom_name, "prefix": "चि." if lang == "hi" else "Mr.", "label": "वर" if lang == "hi" else "Groom" },
                "bride": { "name": bride_name, "prefix": "सौ. कां." if lang == "hi" else "Ms.", "label": "वधू" if lang == "hi" else "Bride" },
                "connector": connector,
                "sealText": f"{groom_name[0]}❤{bride_name[0]}"
            },
            "date": date_info,
            "invocation": {
                "top": "॥ श्री गणेशाय नमः ॥" if lang == "hi" else "Together with our families",
                "shlok": "मंगलम् भगवान विष्णु, मंगलम् गरूड़ध्वजः ।\nमंगलम् पुण्डरीकाक्षः, मंगलाय तनो हरिः ॥" if lang == "hi" else "Two lives, two hearts, joined together in friendship, united forever in love."
            },
            "events": events,
            "venue": venue,
            "music": {
                "src": "assets/shehnai.mp3",
                "label": "शहनाई" if lang == "hi" else "Melody",
                "stopLabel": "रोकें" if lang == "hi" else "Pause",
                "autoplay": False,
                "volume": 0.25
            },
            "rsvp": {
                "enabled": True,
                "mode": "whatsapp",
                "whatsappPhone": "",
                "heading": "क्या आप आ रहे हैं?" if lang == "hi" else "Will You Be Attending?"
            },
            "labels": {
                "countdown": "शुभ लग्न तक" if lang == "hi" else "Countdown to the Big Day",
                "days": "दिन" if lang == "hi" else "Days",
                "hours": "घंटे" if lang == "hi" else "Hours",
                "minutes": "मिनट" if lang == "hi" else "Minutes",
                "seconds": "सेकंड" if lang == "hi" else "Seconds",
                "welcome": "सस्नेह निमंत्रण" if lang == "hi" else "Wedding Invitation"
            }
        }
        return slug, config

    def _extract_couple(self, title: str, text: str):
        # Check patterns in title: "Name & Name", "Name संग Name", "Name weds Name"
        patterns = [
            r'([A-Za-z\u0900-\u097F]+)\s*(?:&|and|संग|weds|विवाह)\s*([A-Za-z\u0900-\u097F]+)',
            r'([A-Za-z\u0900-\u097F]+)\s*❤\s*([A-Za-z\u0900-\u097F]+)'
        ]
        for p in patterns:
            m = re.search(p, title, re.IGNORECASE)
            if m:
                g = m.group(1).strip()
                b = m.group(2).strip()
                conn = "संग" if "संग" in m.group(0) else ("weds" if "weds" in m.group(0).lower() else "&")
                return g, b, conn

        # Fallback to search in top text
        for p in patterns:
            m = re.search(p, text[:1000], re.IGNORECASE)
            if m:
                return m.group(1).strip(), m.group(2).strip(), "&"

        return "Groom", "Bride", "&"

    def _extract_date(self, text: str):
        # Look for dates like 21 November 2026, 21-11-2026, etc.
        m = re.search(r'(\d{1,2})\s+([A-Za-z\u0900-\u097F]+)\s+(202[4-9])', text)
        if m:
            day = m.group(1).zfill(2)
            month = m.group(2)
            year = m.group(3)
            return {
                "iso": f"{year}-11-{day}T19:00:00+05:30",
                "day": day,
                "month": f"{month} {year}",
                "weekday": "Saturday",
                "display": f"{day} {month} {year}"
            }
        return {
            "iso": "2026-11-21T19:00:00+05:30",
            "day": "21",
            "month": "नवंबर 2026",
            "weekday": "शनिवार",
            "display": "21 नवंबर 2026"
        }

    def _extract_events(self, text: str, images: List[str]):
        curated_photos = {
            "haldi": "https://images.unsplash.com/photo-1610030469983-98e550d6193c?auto=format&fit=crop&w=700&q=80",
            "sangeet": "https://images.unsplash.com/photo-1545232979-8bf68ee9b1af?auto=format&fit=crop&w=700&q=80",
            "wedding": "https://images.unsplash.com/photo-1583939003579-730e3918a45a?auto=format&fit=crop&w=700&q=80",
            "reception": "https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=700&q=80"
        }

        # Check for Indian ceremonies in text
        ceremonies = []
        if re.search(r'हल्दी|haldi', text, re.IGNORECASE):
            ceremonies.append({
                "date": "18", "month": "Nov", "name": "हल्दी उत्सव (Haldi)",
                "time": "10:00 AM", "location": "Home / Banquet",
                "image": curated_photos["haldi"],
                "dressCode": { "title": "Haldi Yellow", "palette": ["#ffd54f", "#fbc02d", "#fff9c4"] },
                "main": False
            })
        if re.search(r'संगीत|sangeet', text, re.IGNORECASE):
            ceremonies.append({
                "date": "19", "month": "Nov", "name": "महिला संगीत (Sangeet)",
                "time": "7:00 PM", "location": "Ballroom",
                "image": curated_photos["sangeet"],
                "dressCode": { "title": "Festive Glam", "palette": ["#9c27b0", "#e91e63", "#ffd700"] },
                "main": False
            })

        # Main wedding ceremony always included
        ceremonies.append({
            "date": "21", "month": "Nov", "name": "शुभ विवाह (Wedding Ceremony)",
            "time": "7:00 PM", "location": "Marriage Garden",
            "image": curated_photos["wedding"],
            "dressCode": { "title": "Royal Heritage", "palette": ["#800020", "#d4af37", "#fdfbf7"] },
            "main": True
        })

        if re.search(r'प्रीतिभोज|reception', text, re.IGNORECASE):
            ceremonies.append({
                "date": "22", "month": "Nov", "name": "प्रीतिभोज (Reception)",
                "time": "7:30 PM", "location": "Grand Lawn",
                "image": curated_photos["reception"],
                "main": False
            })

        return ceremonies

    def _extract_venue(self, text: str, links: List[str]):
        # Look for Google Maps link in hrefs
        map_url = "https://maps.google.com"
        for l in links:
            if "maps.google" in l or "goo.gl" in l:
                map_url = l
                break

        venue_name = "मैरिज गार्डन (Wedding Venue)"
        m = re.search(r'(?:venue|स्थल|स्थान|at)[:\s]+([^\n\r,\.]+)', text, re.IGNORECASE)
        if m:
            venue_name = m.group(1).strip()

        return {
            "name": venue_name,
            "address": "गुर्जर कॉलोनी, राजस्थान",
            "mapUrl": map_url,
            "uberUrl": "https://m.uber.com/ul/?action=setPickup&pickup=my_location"
        }

    def import_and_build(self, url: str, custom_slug: Optional[str] = None) -> str:
        """Executes full scrape -> parse -> profile -> wedding folder pipeline."""
        page_data = self.fetch_page(url)
        slug, config = self.parse_wedding_data(page_data, url)
        if custom_slug:
            slug = custom_slug.strip().lower()

        # 1. Save Profile JSON
        profile_file = os.path.join(PROFILES_DIR, f"{slug}.json")
        os.makedirs(PROFILES_DIR, exist_ok=True)
        with open(profile_file, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        print(f"✅ Saved scraped profile: {os.path.relpath(profile_file, ROOT_DIR)}")

        # 2. Build standalone Wedding Folder
        wedding_dir = os.path.join(WEDDINGS_DIR, slug)
        os.makedirs(wedding_dir, exist_ok=True)

        # Copy assets, themes, index.html, and config
        shutil.copy(os.path.join(ROOT_DIR, "index.html"), os.path.join(wedding_dir, "index.html"))
        shutil.copy(profile_file, os.path.join(wedding_dir, "config.json"))

        themes_src = os.path.join(ROOT_DIR, "themes")
        if os.path.exists(themes_src):
            shutil.copytree(themes_src, os.path.join(wedding_dir, "themes"), dirs_exist_ok=True)

        assets_src = os.path.join(ROOT_DIR, "assets")
        if os.path.exists(assets_src):
            shutil.copytree(assets_src, os.path.join(wedding_dir, "assets"), dirs_exist_ok=True)

        print(f"🎉 Fully generated deployable wedding site: weddings/{slug}/")
        print(f" • Couple:  {config['couple']['groom']['name']} {config['couple']['connector']} {config['couple']['bride']['name']}")
        print(f" • Date:    {config['date']['display']}")
        print(f" • Preview: python maker.py serve --wedding {slug}\n")
        return slug

def main():
    if len(sys.argv) < 2:
        print("Usage: python card_scraper.py <url> [--wedding <slug>]")
        sys.exit(1)

    url = sys.argv[1]
    custom_slug = None
    if "--wedding" in sys.argv:
        idx = sys.argv.index("--wedding")
        if idx + 1 < len(sys.argv):
            custom_slug = sys.argv[idx + 1]

    scraper = WeddingCardScraper()
    scraper.import_and_build(url, custom_slug)

if __name__ == "__main__":
    main()
