#!/usr/bin/env python3
"""
WeddingCraft Unified Server — Abstract Modular Wedding Platform Engine
Serves:
  • /               -> Abstract Capability Switchboard & Live Mobile Simulator
  • /w/<slug>       -> Dynamic Wedding Renderer (zero disk duplication)
  • /api/profiles   -> List of wedding profiles
  • /api/profile/:s -> GET / POST profile JSON & module toggles
  • /api/modules    -> Abstract module registry & schema
  • /api/export/:s  -> Downloadable standalone zero-dependency HTML bundle
"""

import os
import sys
import json
import shutil
import urllib.parse
import urllib.request
import re
from http.server import HTTPServer, SimpleHTTPRequestHandler

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PROFILES_DIR = os.path.join(ROOT_DIR, "profiles")
THEMES_DIR = os.path.join(ROOT_DIR, "themes")
ASSETS_DIR = os.path.join(ROOT_DIR, "assets")
SCHEMA_DIR = os.path.join(ROOT_DIR, "schema")
INDEX_PATH = os.path.join(ROOT_DIR, "index.html")
CATALOG_PATH = os.path.join(SCHEMA_DIR, "modules_catalog.json")

class WeddingCraftHandler(SimpleHTTPRequestHandler):
    def do_HEAD(self):
        self.do_GET()

    def translate_path(self, path):
        # Default translation relative to ROOT_DIR
        clean_path = urllib.parse.urlparse(path).path
        clean_path = clean_path.lstrip('/')
        return os.path.join(ROOT_DIR, clean_path)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = parsed.query

        # 1. Root -> Control Center Dashboard
        if path == "/" or path == "/index.html":
            cc_path = os.path.join(ROOT_DIR, "control_center.html")
            if os.path.exists(cc_path):
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                with open(cc_path, "rb") as f:
                    self.wfile.write(f.read())
                return

        # 2. Dynamic Wedding Engine -> /w/<slug> or /wedding/<slug>
        if path.startswith("/w/") or path.startswith("/wedding/"):
            parts = path.strip("/").split("/")
            slug = parts[1] if len(parts) > 1 else "manish-sakshi"
            profile_file = os.path.join(PROFILES_DIR, f"{slug}.json")

            if not os.path.exists(profile_file):
                self.send_error(404, f"Wedding profile not found: {slug}")
                return

            with open(profile_file, "r", encoding="utf-8") as f:
                cfg = json.load(f)

            with open(INDEX_PATH, "r", encoding="utf-8") as f:
                html = f.read()

            # Inject EMBEDDED_CONFIG and base tag
            injection = f"""<script>
window.EMBEDDED_CONFIG = {json.dumps(cfg, ensure_ascii=False)};
</script>
<base href="/">
"""
            if "</head>" in html:
                html = html.replace("</head>", f"{injection}\n</head>", 1)
            else:
                html = injection + html

            data = html.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return

        # 3. API: List all profiles -> /api/profiles
        if path == "/api/profiles":
            profiles = []
            if os.path.exists(PROFILES_DIR):
                for fname in sorted(os.listdir(PROFILES_DIR)):
                    if fname.endswith(".json"):
                        slug = fname[:-5]
                        try:
                            with open(os.path.join(PROFILES_DIR, fname), "r", encoding="utf-8") as f:
                                pdata = json.load(f)
                            couple = pdata.get("couple", {})
                            groom = couple.get("groom", {}).get("name", "Groom")
                            bride = couple.get("bride", {}).get("name", "Bride")
                            conn = couple.get("connector", "संग")
                            mods = pdata.get("modules", {})
                            active_mods = len(mods) if isinstance(mods, list) else sum(1 for v in mods.values() if v)
                            profiles.append({
                                "slug": slug,
                                "name": f"{groom} {conn} {bride}",
                                "date": pdata.get("date", {}).get("display", ""),
                                "theme": pdata.get("theme", "ivory"),
                                "active_modules": active_mods
                            })
                        except Exception as e:
                            pass

            self.send_json_response(profiles)
            return

        # 4. API: Get single profile -> /api/profile/<slug>
        if path.startswith("/api/profile/"):
            slug = path[len("/api/profile/"):]
            profile_file = os.path.join(PROFILES_DIR, f"{slug}.json")
            if not os.path.exists(profile_file):
                self.send_error(404, f"Profile not found: {slug}")
                return
            with open(profile_file, "r", encoding="utf-8") as f:
                cfg = json.load(f)
            self.send_json_response(cfg)
            return

        # 5. API: Modules catalog -> /api/modules
        if path == "/api/modules":
            if os.path.exists(CATALOG_PATH):
                with open(CATALOG_PATH, "r", encoding="utf-8") as f:
                    cat = json.load(f)
                self.send_json_response(cat)
            else:
                self.send_json_response({"modules": []})
            return

        # 6. API: Standalone bundle export -> /api/export/<slug>
        if path.startswith("/api/export/"):
            slug = path[len("/api/export/"):]
            profile_file = os.path.join(PROFILES_DIR, f"{slug}.json")
            if not os.path.exists(profile_file):
                self.send_error(404, f"Profile not found: {slug}")
                return

            with open(profile_file, "r", encoding="utf-8") as f:
                cfg = json.load(f)

            with open(INDEX_PATH, "r", encoding="utf-8") as f:
                html = f.read()

            theme_name = cfg.get("theme", "ivory")
            theme_file = os.path.join(THEMES_DIR, f"{theme_name}.css")
            theme_css = ""
            if os.path.exists(theme_file):
                with open(theme_file, "r", encoding="utf-8") as f:
                    theme_css = f.read()

            # Inline theme css
            inline_style = f"<style id=\"themeStylesheet\">\n/* Inlined Theme: {theme_name} */\n{theme_css}\n</style>"
            if "</head>" in html:
                html = html.replace("</head>", f"{inline_style}\n</head>", 1)

            # Inline embedded config
            embedded_script = f"""<script>
window.EMBEDDED_CONFIG = {json.dumps(cfg, ensure_ascii=False)};
</script>"""
            if "</head>" in html:
                html = html.replace("</head>", f"{embedded_script}\n</head>", 1)

            data = html.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Disposition", f"attachment; filename=\"wedding-{slug}-standalone.html\"")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return

        # 7. Fallback to standard static file serving (themes, assets, etc.)
        return super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # API: Save profile -> /api/profile/<slug>
        if path.startswith("/api/profile/"):
            slug = path[len("/api/profile/"):]
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")

            try:
                data = json.loads(body)
            except Exception as e:
                self.send_error(400, f"Invalid JSON body: {e}")
                return

            os.makedirs(PROFILES_DIR, exist_ok=True)
            profile_file = os.path.join(PROFILES_DIR, f"{slug}.json")
            with open(profile_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            self.send_json_response({"ok": True, "slug": slug, "path": profile_file})
            return

        # API: Scrape live card -> /api/scrape
        if path == "/api/scrape":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")

            try:
                payload = json.loads(body)
                card_url = payload.get("url", "").strip()
                custom_slug = payload.get("slug", "").strip()
                target_theme = payload.get("theme", "sindoori")
            except Exception as e:
                self.send_json_response({"ok": False, "error": f"Invalid payload: {e}"}, status=400)
                return

            if not card_url:
                self.send_json_response({"ok": False, "error": "URL is required"}, status=400)
                return

            try:
                # Use module-level urllib.request
                req = urllib.request.Request(card_url, headers={"User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36"})
                raw_html = urllib.request.urlopen(req, timeout=12).read().decode("utf-8")

                # If Next.js app (e.g. myshaadhilink)
                if "self.__next_f" in raw_html and "coupleDetails" in raw_html:
                    matches = re.findall(r"self\.__next_f\.push\(\[1,\"(.*?)\"\]\)", raw_html)
                    full_text = "".join(matches).replace("\\\"", "\"").replace("\\\\", "\\")
                    m = re.search(r"\"invitation\":(\{.*?\}(?=,\"(?:guestName|embed)\"))", full_text)
                    if not m:
                        m = re.search(r"\"coupleDetails\":(\{.*?\})", full_text)
                    
                    if m:
                        inv_data = json.loads(m.group(1))
                        # Use convert_myshaadhi logic
                        from convert_scraped import convert_myshaadhi_to_weddingcraft
                        temp_json_path = os.path.join(ROOT_DIR, "dist", "temp_scraped.json")
                        os.makedirs(os.path.dirname(temp_json_path), exist_ok=True)
                        with open(temp_json_path, "w", encoding="utf-8") as f:
                            json.dump(inv_data, f)
                        
                        slug = custom_slug or inv_data.get("slug", "scraped-wedding").replace("-wedding-invitation", "")
                        convert_myshaadhi_to_weddingcraft(temp_json_path, slug, target_theme)
                        self.send_json_response({"ok": True, "slug": slug})
                        return

                # Generic HTML scraper fallback using card_scraper
                from card_scraper import WeddingCardScraper
                scraper = WeddingCardScraper()
                config = scraper.scrape_url(card_url, custom_slug=custom_slug)
                if target_theme:
                    config["theme"] = target_theme
                
                slug = custom_slug or config.get("meta", {}).get("title", "scraped-card").lower().replace(" ", "-")
                slug = re.sub(r'[^a-zA-Z0-9\-]', '', slug) or "scraped-card"
                
                os.makedirs(PROFILES_DIR, exist_ok=True)
                p_file = os.path.join(PROFILES_DIR, f"{slug}.json")
                with open(p_file, "w", encoding="utf-8") as f:
                    json.dump(config, f, indent=2, ensure_ascii=False)

                self.send_json_response({"ok": True, "slug": slug})
                return

            except Exception as ex:
                self.send_json_response({"ok": False, "error": str(ex)}, status=500)
                return

        self.send_error(404, "Endpoint not found")

    def send_json_response(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

def run(port=8000):
    server_address = ("", port)
    httpd = HTTPServer(server_address, WeddingCraftHandler)
    print(f"\n✨ WeddingCraft Unified Abstract Platform Server")
    print(f"============================================================")
    print(f" • Control Center Switchboard: http://localhost:{port}/")
    print(f" • Dynamic Flagship Route:     http://localhost:{port}/w/manish-sakshi")
    print(f" • Dynamic Fusion Route:       http://localhost:{port}/w/arjun-ananya")
    print(f" • Dynamic Scraped Route:      http://localhost:{port}/w/rohit-priya")
    print(f"============================================================")
    print("Press Ctrl+C to stop.\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")

if __name__ == "__main__":
    port = 8000
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        port = int(sys.argv[1])
    run(port)
