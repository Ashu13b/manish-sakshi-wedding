#!/usr/bin/env python3
"""
WeddingCraft CLI — Modular Wedding Website Maker & Deployment Engine
Folder-Per-Wedding Architecture ("One Person = One Deployable Folder")

Usage:
    python maker.py list
    python maker.py scaffold <wedding-slug>
    python maker.py build [--wedding <slug>] [--profile <path>] [--output <dir>]
    python maker.py bundle-standalone [--wedding <slug>] [--profile <path>] [--output <file>]
    python maker.py guests --list guests.txt [--wedding <slug>] [--url <base_url>]
    python maker.py serve [--wedding <slug>] [--port 8000]
    python maker.py deploy --wedding <slug> --target (github|cloudflare|vercel)
"""

import sys
import os
import json
import shutil
import argparse
import http.server
import socketserver
import urllib.parse

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PROFILES_DIR = os.path.join(ROOT_DIR, "profiles")
WEDDINGS_DIR = os.path.join(ROOT_DIR, "weddings")
THEMES_DIR = os.path.join(ROOT_DIR, "themes")
ASSETS_DIR = os.path.join(ROOT_DIR, "assets")

def resolve_wedding_profile(slug):
    if not slug:
        return os.path.join(PROFILES_DIR, "manish-sakshi.json")
    # Check if slug is a json file directly
    if slug.endswith(".json") and os.path.exists(slug):
        return slug
    # Check profiles/<slug>.json
    p = os.path.join(PROFILES_DIR, f"{slug}.json")
    if os.path.exists(p):
        return p
    # Check weddings/<slug>/config.json
    w = os.path.join(WEDDINGS_DIR, slug, "config.json")
    if os.path.exists(w):
        return w
    return p

def cmd_list(args):
    print("\n💍 WeddingCraft Available Profiles & Wedding Folders:")
    print("=" * 65)
    
    # 1. Profiles
    if os.path.exists(PROFILES_DIR):
        print("📁 Profiles (profiles/):")
        for p in sorted(os.listdir(PROFILES_DIR)):
            if p.endswith(".json"):
                path = os.path.join(PROFILES_DIR, p)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    groom = data.get("couple", {}).get("groom", {}).get("name", "Groom")
                    bride = data.get("couple", {}).get("bride", {}).get("name", "Bride")
                    conn = data.get("couple", {}).get("connector", "&")
                    date = data.get("date", {}).get("display", "N/A")
                    theme = data.get("theme", "ivory")
                    print(f"   • {p:<22} -> {groom} {conn} {bride} | {date} | Theme: {theme}")
                except Exception as e:
                    print(f"   • {p:<22} -> (Error reading file: {e})")

    # 2. Deployed Wedding Folders
    if os.path.exists(WEDDINGS_DIR):
        print("\n📦 Deployable Wedding Folders (weddings/):")
        for w in sorted(os.listdir(WEDDINGS_DIR)):
            w_dir = os.path.join(WEDDINGS_DIR, w)
            if os.path.isdir(w_dir):
                cfg_path = os.path.join(w_dir, "config.json")
                if os.path.exists(cfg_path):
                    try:
                        with open(cfg_path, "r", encoding="utf-8") as f:
                            data = json.load(f)
                        groom = data.get("couple", {}).get("groom", {}).get("name", "Groom")
                        bride = data.get("couple", {}).get("bride", {}).get("name", "Bride")
                        conn = data.get("couple", {}).get("connector", "&")
                        print(f"   • weddings/{w}/ -> {groom} {conn} {bride} (Ready to deploy)")
                    except Exception:
                        print(f"   • weddings/{w}/ -> (Custom site folder)")
                else:
                    print(f"   • weddings/{w}/ -> (Directory exists, no config.json)")
    print("=" * 65 + "\n")

def cmd_scaffold(args):
    slug = args.slug.strip().lower()
    target_dir = os.path.join(WEDDINGS_DIR, slug)
    if os.path.exists(target_dir):
        print(f"⚠️ Warning: Wedding folder already exists at: {target_dir}")
        ans = input("Overwrite? (y/N): ").strip().lower()
        if ans != 'y':
            print("Aborted.")
            return

    os.makedirs(target_dir, exist_ok=True)
    # Starter config
    starter_cfg = {
        "theme": "ivory",
        "lang": "hi",
        "meta": {
            "title": f"विवाह निमंत्रण | {slug.title()}",
            "description": "मांगलिक परिणयोत्सव का शुभ निमंत्रण।"
        },
        "modules": ["envelope", "hero", "countdown", "lineage", "events", "dress_code", "venue", "wishes", "family", "rsvp"],
        "couple": {
            "groom": { "name": "वर", "prefix": "चि.", "label": "वर", "lineage": "सुपुत्र..." },
            "bride": { "name": "वधू", "prefix": "सौ. कां.", "label": "वधू", "lineage": "सुपुत्री..." },
            "connector": "संग",
            "sealText": "💍"
        },
        "date": {
            "iso": "2026-12-01T20:00:00+05:30",
            "day": "01",
            "month": "दिसंबर 2026",
            "weekday": "मंगलवार",
            "display": "01 दिसंबर 2026"
        },
        "invocation": {
            "top": "॥ श्री गणेशाय नमः ॥",
            "shlok": "ॐ वक्रतुण्ड महाकाय सूर्यकोटिसमप्रभ ।\nनिर्विघ्नं कुरु मे देव सर्वकार्येषु सर्वदा ॥"
        },
        "events": [
            {
                "date": "01", "month": "दिसंबर", "name": "विवाह संस्कार",
                "time": "सायं 7:00 बजे", "location": "विवाह स्थल",
                "calendarStart": "20261201T190000", "calendarEnd": "20261202T010000",
                "main": True
            }
        ],
        "venue": {
            "name": "मैरिज गार्डन",
            "address": "शहर, राजस्थान",
            "mapUrl": "https://maps.google.com"
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
        "labels": {
            "countdown": "शुभ लग्न तक",
            "days": "दिन", "hours": "घंटे", "minutes": "मिनट", "seconds": "सेकंड",
            "welcome": "सस्नेह निमंत्रण"
        }
    }

    # Write config.json
    with open(os.path.join(target_dir, "config.json"), "w", encoding="utf-8") as f:
        json.dump(starter_cfg, f, ensure_ascii=False, indent=2)

    # Copy template index.html, themes, assets
    shutil.copy(os.path.join(ROOT_DIR, "index.html"), os.path.join(target_dir, "index.html"))
    if os.path.exists(THEMES_DIR):
        shutil.copytree(THEMES_DIR, os.path.join(target_dir, "themes"), dirs_exist_ok=True)
    if os.path.exists(ASSETS_DIR):
        shutil.copytree(ASSETS_DIR, os.path.join(target_dir, "assets"), dirs_exist_ok=True)

    print(f"\n🎉 Scaffolded new independent wedding folder: weddings/{slug}/")
    print(f" • Edit details in: weddings/{slug}/config.json")
    print(f" • Test locally:     python maker.py serve --wedding {slug}")
    print(f" • Deploy directly:  python maker.py deploy --wedding {slug} --target cloudflare\n")

def cmd_build(args):
    # Determine profile and destination
    if args.wedding:
        slug = args.wedding.strip().lower()
        profile_path = resolve_wedding_profile(slug)
        out_dir = os.path.join(WEDDINGS_DIR, slug)
    else:
        profile_path = os.path.abspath(args.profile)
        out_dir = os.path.abspath(args.output)

    if not os.path.exists(profile_path):
        print(f"❌ Error: Profile file not found: {profile_path}")
        sys.exit(1)

    print(f"\n🔨 Building WeddingCraft static site...")
    print(f" • Source Profile: {profile_path}")
    print(f" • Output Folder:  {out_dir}")

    os.makedirs(out_dir, exist_ok=True)

    # 1. Copy index.html
    shutil.copy(os.path.join(ROOT_DIR, "index.html"), os.path.join(out_dir, "index.html"))

    # 2. Copy themes/
    out_themes = os.path.join(out_dir, "themes")
    os.makedirs(out_themes, exist_ok=True)
    if os.path.exists(THEMES_DIR):
        for f in os.listdir(THEMES_DIR):
            if f.endswith(".css"):
                shutil.copy(os.path.join(THEMES_DIR, f), os.path.join(out_themes, f))

    # 3. Copy assets/
    out_assets = os.path.join(out_dir, "assets")
    os.makedirs(out_assets, exist_ok=True)
    if os.path.exists(ASSETS_DIR):
        for f in os.listdir(ASSETS_DIR):
            src_f = os.path.join(ASSETS_DIR, f)
            if os.path.isfile(src_f):
                shutil.copy(src_f, os.path.join(out_assets, f))

    # 4. Copy card images if present in root
    for img in ["card1.jpg", "card2.jpg"]:
        p = os.path.join(ROOT_DIR, img)
        if os.path.exists(p):
            shutil.copy(p, os.path.join(out_dir, img))

    # 5. Write selected profile as config.json in destination
    shutil.copy(profile_path, os.path.join(out_dir, "config.json"))

    print(f"✅ Build complete! Folder '{os.path.relpath(out_dir, ROOT_DIR)}' is 100% self-contained and ready to deploy.\n")

def cmd_bundle_standalone(args):
    if args.wedding:
        slug = args.wedding.strip().lower()
        profile_path = resolve_wedding_profile(slug)
        out_file = os.path.join(WEDDINGS_DIR, slug, "dist", "wedding-standalone.html")
    else:
        profile_path = os.path.abspath(args.profile)
        out_file = os.path.abspath(args.output)

    if not os.path.exists(profile_path):
        print(f"❌ Error: Profile not found: {profile_path}")
        sys.exit(1)

    with open(profile_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    theme_name = cfg.get("theme", "ivory")
    theme_file = os.path.join(THEMES_DIR, f"{theme_name}.css")
    theme_css = ""
    if os.path.exists(theme_file):
        with open(theme_file, "r", encoding="utf-8") as f:
            theme_css = f.read()

    index_file = os.path.join(ROOT_DIR, "index.html")
    with open(index_file, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Inline Theme CSS
    inline_theme_tag = f"<style id=\"standalone-theme\">\n{theme_css}\n</style>"
    html = html.replace("</head>", f"{inline_theme_tag}\n</head>")

    # 1b. Inline MIT QR Engine for 100% Offline Standalone Support
    qr_local_path = os.path.join(ASSETS_DIR, "qrcode.min.js")
    if os.path.exists(qr_local_path):
        with open(qr_local_path, "r", encoding="utf-8") as fqr:
            qr_code_js = fqr.read()
        html = html.replace(
            '<script src="https://cdnjs.cloudflare.com/ajax/libs/qrcode-generator/1.4.4/qrcode.min.js"></script>',
            f'<script>\n/* Inlined Kazuhiko Arase QR Engine (MIT License) - 100% Offline Ready */\n{qr_code_js}\n</script>'
        )

    # 2. Replace fetch('config.json') with direct inline synchronous boot
    cfg_json_str = json.dumps(cfg, ensure_ascii=False)
    fetch_replacement = f"""
// Standalone Mode — Inlined Configuration
var C = {cfg_json_str};
boot(C);
"""
    fetch_marker = "fetch(configFile)"
    if fetch_marker in html:
        start_idx = html.find("fetch(configFile)")
        end_marker = "});"
        end_idx = html.find(end_marker, start_idx) + len(end_marker)
        html = html[:start_idx] + fetch_replacement + html[end_idx:]

    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ Standalone bundle created: {out_file}")
    print(f" • File size: {os.path.getsize(out_file) / 1024:.1f} KB")
    print(f" • Single self-contained HTML file! Can be sent via WhatsApp or AirDrop and opened offline.\n")

def cmd_guests(args):
    if not os.path.exists(args.list):
        print(f"❌ Error: Guest list file not found: {args.list}")
        sys.exit(1)

    slug = args.wedding if args.wedding else None
    profile_path = resolve_wedding_profile(slug) if slug else os.path.abspath(args.profile)

    with open(profile_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    groom = cfg.get("couple", {}).get("groom", {}).get("name", "Groom")
    bride = cfg.get("couple", {}).get("bride", {}).get("name", "Bride")
    conn = cfg.get("couple", {}).get("connector", "संग")
    date_display = cfg.get("date", {}).get("display", "")
    base_url = args.url.rstrip("/") + "/"

    with open(args.list, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    print(f"\n💌 Generating Personalized Guest WhatsApp Invites for {groom} {conn} {bride}:")
    print("=" * 70)

    rows = []
    for line in lines:
        parts = [p.strip() for p in line.split(",") if p.strip()]
        name = parts[0]
        phone = parts[1] if len(parts) > 1 else ""

        invite_link = f"{base_url}?to={urllib.parse.quote(name)}&fam=1"
        wa_text = f"🙏 *शुभ विवाह आमंत्रण* 🙏\n\nआदरणीय *{name}* जी,\nचि. {groom} {conn} सौ. कां. {bride} के शुभ विवाह ({date_display}) में आपको सपरिवार सादर आमंत्रित करते हैं।\n\n💌 आपका व्यक्तिगत डिजिटल आमंत्रण पत्र:\n{invite_link}\n\n— समस्त परिवार"
        wa_url = f"https://api.whatsapp.com/send?text={urllib.parse.quote(wa_text)}"
        if phone:
            wa_url = f"https://api.whatsapp.com/send?phone={phone}&text={urllib.parse.quote(wa_text)}"

        rows.append((name, phone, invite_link, wa_url))
        print(f" • {name:<20} -> {invite_link}")

    out_html = os.path.join(ROOT_DIR, "dist", "guest_invites.html")
    if args.wedding:
        out_html = os.path.join(WEDDINGS_DIR, args.wedding, "guest_invites.html")
    os.makedirs(os.path.dirname(out_html), exist_ok=True)
    with open(out_html, "w", encoding="utf-8") as f:
        f.write("<!DOCTYPE html><html><head><meta charset='utf-8'><title>Guest Invites</title>")
        f.write("<style>body{font-family:sans-serif;padding:20px;background:#f9f9fb}table{width:100%;border-collapse:collapse;background:#fff}th,td{border:1px solid #ddd;padding:10px;font-size:14px}th{background:#f0f0f4}a{color:#0066cc;text-decoration:none}a.wa{color:#25d366;font-weight:bold}</style></head><body>")
        f.write(f"<h2>Personalized Invites ({len(rows)} Guests)</h2>")
        f.write("<table><tr><th>Guest Name</th><th>Phone</th><th>Personalized Link</th><th>Action</th></tr>")
        for name, phone, link, wa in rows:
            f.write(f"<tr><td><strong>{name}</strong></td><td>{phone}</td><td><a href='{link}' target='_blank'>{link}</a></td><td><a class='wa' href='{wa}' target='_blank'>📲 Send WhatsApp</a></td></tr>")
        f.write("</table></body></html>")

    print(f"\n✅ Generated guest invite dashboard at: {out_html}\n")

def cmd_deploy(args):
    target = args.target.lower()
    wedding_slug = args.wedding if args.wedding else "manish-sakshi"
    wedding_path = f"weddings/{wedding_slug}"
    
    print(f"\n🚀 Deployment Expert — Deploying Wedding Folder: '{wedding_path}' to {target.upper()}")
    print("=" * 65)

    if target == "github":
        wf_dir = os.path.join(ROOT_DIR, ".github", "workflows")
        os.makedirs(wf_dir, exist_ok=True)
        wf_path = os.path.join(wf_dir, f"deploy-{wedding_slug}.yml")
        content = f"""name: Deploy {wedding_slug} to GitHub Pages

on:
  push:
    branches: ["main"]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{{{ steps.deployment.outputs.page_url }}}}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Setup Pages
        uses: actions/configure-pages@v4
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: '{wedding_path}'
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
"""
        with open(wf_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Created GitHub Actions workflow targeting: '{wedding_path}'")
        print(f"   Workflow file: {wf_path}")
        print("   To deploy: Push to GitHub, then enable GitHub Pages -> Source: GitHub Actions.")

    elif target == "cloudflare":
        wrangler_path = os.path.join(ROOT_DIR, "wrangler.toml")
        content = f"""name = "{wedding_slug}-wedding"
compatibility_date = "2024-01-01"
pages_build_output_dir = "{wedding_path}"
"""
        with open(wrangler_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Created Cloudflare Pages config pointing to '{wedding_path}'")
        print(f"   Config file: {wrangler_path}")
        print(f"   To deploy: Run `npx wrangler pages deploy {wedding_path}`")

    elif target == "vercel":
        vercel_path = os.path.join(ROOT_DIR, "vercel.json")
        content = f"""{{
  "version": 2,
  "cleanUrls": true,
  "routes": [
    {{ "src": "/(.*)", "dest": "/{wedding_path}/$1" }}
  ]
}}
"""
        with open(vercel_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Created Vercel configuration routing to '{wedding_path}'")
        print(f"   Config file: {vercel_path}")

    print("=" * 65 + "\n")

def cmd_serve(args):
    port = args.port
    serve_dir = ROOT_DIR
    if args.wedding:
        slug = args.wedding.strip().lower()
        w_dir = os.path.join(WEDDINGS_DIR, slug)
        if os.path.exists(w_dir):
            serve_dir = w_dir
        else:
            print(f"❌ Error: Wedding folder not found: weddings/{slug}")
            sys.exit(1)

    os.chdir(serve_dir)
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"\n🌐 WeddingCraft Server running:")
        print(f" • Serving Directory: {serve_dir}")
        print(f" • Local URL:          http://localhost:{port}/\n")
        print("Press Ctrl+C to stop.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")

def main():
    parser = argparse.ArgumentParser(description="WeddingCraft CLI — Folder-Per-Wedding Architecture")
    subparsers = parser.add_subparsers(dest="command")

    # list
    subparsers.add_parser("list", help="List available wedding profiles and folders")

    # scaffold
    p_scaffold = subparsers.add_parser("scaffold", help="Scaffold a new independent wedding folder")
    p_scaffold.add_argument("slug", help="Unique slug for the wedding (e.g. rahul-priya)")

    # build
    p_build = subparsers.add_parser("build", help="Build / sync static production bundle")
    p_build.add_argument("--wedding", help="Wedding folder slug (e.g. manish-sakshi)")
    p_build.add_argument("--profile", default="profiles/manish-sakshi.json", help="Path to profile JSON")
    p_build.add_argument("--output", default="dist", help="Output directory")

    # bundle-standalone
    p_bundle = subparsers.add_parser("bundle-standalone", help="Bundle into 100% self-contained single HTML")
    p_bundle.add_argument("--wedding", help="Wedding folder slug (e.g. manish-sakshi)")
    p_bundle.add_argument("--profile", default="profiles/manish-sakshi.json", help="Path to profile JSON")
    p_bundle.add_argument("--output", default="dist/wedding-standalone.html", help="Output HTML file")

    # guests
    p_guests = subparsers.add_parser("guests", help="Generate personalized guest WhatsApp links")
    p_guests.add_argument("--list", required=True, help="Path to guest list file")
    p_guests.add_argument("--wedding", help="Wedding folder slug")
    p_guests.add_argument("--profile", default="profiles/manish-sakshi.json", help="Path to profile JSON")
    p_guests.add_argument("--url", default="https://manish-sakshi-wedding.pages.dev/", help="Base deployed website URL")

    # scrape
    p_scrape = subparsers.add_parser("scrape", help="Scrape digital wedding card via android-browser or web URL")
    p_scrape.add_argument("url", help="URL or file path of the digital wedding card")
    p_scrape.add_argument("--wedding", help="Custom wedding slug (e.g. rahul-priya)")

    # parse-text
    p_parse = subparsers.add_parser("parse-text", help="Parse raw WhatsApp invitation text/file into a deployable site")
    p_parse.add_argument("input", help="Text string or path to text file (e.g. invite.txt)")
    p_parse.add_argument("--wedding", help="Custom wedding slug")

    # deploy
    p_deploy = subparsers.add_parser("deploy", help="Configure deployment targets")
    p_deploy.add_argument("--wedding", default="manish-sakshi", help="Wedding slug to deploy")
    p_deploy.add_argument("--target", choices=["github", "cloudflare", "vercel"], required=True, help="Target host")

    # serve
    p_serve = subparsers.add_parser("serve", help="Run local preview web server")
    p_serve.add_argument("--wedding", help="Serve a specific wedding folder")
    p_serve.add_argument("--port", type=int, default=8000, help="Port number")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)

    if args.command == "list":
        cmd_list(args)
    elif args.command == "scaffold":
        cmd_scaffold(args)
    elif args.command == "build":
        cmd_build(args)
    elif args.command == "bundle-standalone":
        cmd_bundle_standalone(args)
    elif args.command == "guests":
        cmd_guests(args)
    elif args.command == "scrape":
        from card_scraper import WeddingCardScraper
        scraper = WeddingCardScraper()
        scraper.import_and_build(args.url, args.wedding)
    elif args.command == "parse-text":
        from card_scraper import WeddingCardScraper
        scraper = WeddingCardScraper()
        scraper.import_text_and_build(args.input, args.wedding)
    elif args.command == "deploy":
        cmd_deploy(args)
    elif args.command == "serve":
        cmd_serve(args)

if __name__ == "__main__":
    main()
