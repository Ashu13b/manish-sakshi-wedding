import json
import re

def convert_myshaadhi_to_weddingcraft(src_path, out_slug, theme_override=None):
    with open(src_path, "r", encoding="utf-8") as f:
        d = json.load(f)

    c_det = d.get("coupleDetails", {})
    w_det = d.get("weddingDetails", {})
    evs_raw = d.get("events", {})
    ven_raw = d.get("venue", {})
    sec_vis = d.get("sectionVisibility", {})
    gal_raw = d.get("gallery", {})

    g_first = c_det.get("groomFirstName", "Groom")
    g_full = c_det.get("groomFullName", g_first)
    b_first = c_det.get("brideFirstName", "Bride")
    b_full = c_det.get("brideFullName", b_first)

    g_parents = c_det.get("groomParents", "")
    g_p_lbl = c_det.get("groomParentLabel", "Son of")
    b_parents = c_det.get("brideParents", "")
    b_p_lbl = c_det.get("brideParentLabel", "Daughter of")

    g_photo = c_det.get("groomPhoto", {}).get("node", {}).get("sourceUrl") if c_det.get("groomPhoto") else None
    b_photo = c_det.get("bridePhoto", {}).get("node", {}).get("sourceUrl") if c_det.get("bridePhoto") else None

    # Parse Events
    events = []
    curated_photos = {
        "haldi": "https://images.unsplash.com/photo-1610030469983-98e550d6193c?auto=format&fit=crop&w=700&q=80",
        "mehendi": "https://images.unsplash.com/photo-1560969184-10fe8719e047?auto=format&fit=crop&w=700&q=80",
        "sangeet": "https://images.unsplash.com/photo-1545232979-8bf68ee9b1af?auto=format&fit=crop&w=700&q=80",
        "wedding": "https://images.unsplash.com/photo-1583939003579-730e3918a45a?auto=format&fit=crop&w=700&q=80",
        "reception": "https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=700&q=80",
        "engagement": "https://images.unsplash.com/photo-1607190074257-dd4b7af0309f?auto=format&fit=crop&w=700&q=80",
        "other": "https://images.unsplash.com/photo-1511285560929-80b456fea0bc?auto=format&fit=crop&w=700&q=80"
    }

    for i in range(1, 11):
        prefix = f"event{i}"
        if not evs_raw.get(f"{prefix}Enabled"):
            continue
        ename = evs_raw.get(f"{prefix}Name")
        if not ename:
            continue
        
        edate_str = evs_raw.get(f"{prefix}Date") or ""
        etime = evs_raw.get(f"{prefix}Time") or ""
        evenue = evs_raw.get(f"{prefix}Venue") or ""
        emap = evs_raw.get(f"{prefix}MapLink") or ""
        etypes = evs_raw.get(f"{prefix}Type") or ["other"]
        etype = etypes[0] if etypes else "other"

        m_day = re.search(r"(\d+)(?:st|nd|rd|th)?\s+([A-Za-z]+)", edate_str)
        day_val = m_day.group(1) if m_day else "01"
        mon_val = m_day.group(2) if m_day else "May"

        dress_enabled = evs_raw.get(f"{prefix}DressCode", False)
        dress_text = evs_raw.get(f"{prefix}DressCodeText") or ""
        dcode = None
        if dress_enabled and dress_text:
            dcode = {
                "title": dress_text,
                "palette": ["#ffd700", "#ff6f00", "#ffffff"],
                "description": f"Suggested attire: {dress_text}"
            }

        img = curated_photos.get(etype.lower(), curated_photos["other"])
        ename_low = ename.lower()
        if "haldi" in ename_low:
            img = curated_photos["haldi"]
        elif "mehendi" in ename_low or "mehndi" in ename_low:
            img = curated_photos["mehendi"]
        elif "sangeet" in ename_low or "music" in ename_low:
            img = curated_photos["sangeet"]
        elif "wedding" in ename_low or "muhurtham" in ename_low or "kalyanam" in ename_low or "phera" in ename_low:
            img = curated_photos["wedding"]
        elif "reception" in ename_low or "dinner" in ename_low or "preeti" in ename_low:
            img = curated_photos["reception"]
        elif "engagement" in ename_low or "ring" in ename_low or "roka" in ename_low:
            img = curated_photos["engagement"]

        events.append({
            "date": day_val,
            "month": mon_val,
            "name": ename,
            "time": etime,
            "location": evenue,
            "detail": evenue,
            "mapUrl": emap,
            "image": img,
            "dressCode": dcode,
            "main": (etype.lower() == "wedding" or "wedding" in ename.lower() or "muhurtham" in ename.lower())
        })

    # Parse Gallery
    gallery = []
    for i in range(1, 11):
        gkey = f"galleryPhoto{i}"
        gnode = gal_raw.get(gkey)
        if gnode and isinstance(gnode, dict) and gnode.get("node"):
            s_url = gnode["node"].get("sourceUrl")
            if s_url:
                gallery.append({
                    "src": s_url,
                    "caption": f"Moments of Love · {g_first} & {b_first}"
                })

    # Theme selection
    tpl = d.get("templateDesign", {}).get("invitationTemplate", "royal-premium")
    theme = theme_override or ("sindoori" if "royal" in tpl else ("kesariya" if "south" in tpl else "ivory"))

    music_url = "assets/shehnai.mp3"
    b_music = d.get("backgroundMusic", {}).get("musicFile")
    if b_music and isinstance(b_music, dict) and b_music.get("node", {}).get("mediaItemUrl"):
        music_url = b_music["node"]["mediaItemUrl"]

    date_display = w_det.get("weddingDateDisplay", "10th May 2026")
    m_wday = re.search(r"(\d+)(?:st|nd|rd|th)?\s+([A-Za-z]+)", date_display)
    w_day = m_wday.group(1) if m_wday else "10"
    w_mon = m_wday.group(2) if m_wday else "May"
    w_time = w_det.get("weddingTime", "Auspicious Muhurtham")
    vname = ven_raw.get("venueName", "Sri Vaibhavam Banquet Hall")
    vaddr = ven_raw.get("venueAddress", "Sangareddy Road, Shankarpally")
    vmap = ven_raw.get("venueDirectionsUrl") or ven_raw.get("venueMapEmbed") or "https://maps.google.com"

    profile = {
        "theme": theme,
        "lang": "en",
        "meta": {
            "title": f"{g_first} & {b_first} — Royal Wedding Invitation",
            "description": f"You are cordially invited to celebrate the wedding of {g_full} and {b_full} on {date_display}.",
            "ogTitle": f"{g_first} ❤ {b_first} — Wedding Celebration",
            "ogDescription": f"{date_display} · {vname}"
        },
        "modules": {
            "envelope": True,
            "music": sec_vis.get("showMusic", True),
            "guest_personalization": True,
            "hero": sec_vis.get("showHero", True),
            "kinetic_stream": True,
            "countdown": sec_vis.get("showCountdown", True),
            "story": True,
            "lineage": sec_vis.get("showCouple", True),
            "events": sec_vis.get("showEvents", True),
            "event_photos": True,
            "dress_code": True,
            "calendar_sync": True,
            "venue": sec_vis.get("showVenue", True),
            "ride_booking": True,
            "stay": True,
            "venue_qr": True,
            "gallery": (len(gallery) > 0 and sec_vis.get("showGallery", True)),
            "wishes": True,
            "family": True,
            "manuhaar": False,
            "rsvp": sec_vis.get("showRsvp", True),
            "shagun_upi": False,
            "livestream": d.get("livestream", {}).get("livestreamEnabled", False),
            "theme_drawer": True
        },
        "couple": {
            "connector": "&",
            "sealText": f"{g_first[0]}❤{b_first[0]}",
            "groom": {
                "name": g_full,
                "prefix": "Mr.",
                "label": "Groom",
                "lineage": f"{g_p_lbl} <strong>{g_parents}</strong>",
                "photo": g_photo
            },
            "bride": {
                "name": b_full,
                "prefix": "Ms.",
                "label": "Bride",
                "lineage": f"{b_p_lbl} <strong>{b_parents}</strong>",
                "photo": b_photo
            }
        },
        "date": {
            "iso": w_det.get("weddingDate", "2026-05-10T09:50:00+05:30"),
            "day": w_day,
            "month": f"{w_mon} 2026",
            "weekday": date_display.split(",")[0] if "," in date_display else "Sunday",
            "display": date_display,
            "muhurat": w_time
        },
        "invocation": {
            "top": "॥ ॐ श्री गणेशाय नमः ॥",
            "shlok": w_det.get("blessingText", "With the blessings of the Almighty, we invite you to celebrate our union.")
        },
        "events": events,
        "venue": {
            "label": "Wedding Venue",
            "name": vname,
            "address": vaddr,
            "badge": f"{date_display} · {w_time}",
            "mapUrl": vmap,
            "mapLabel": "Open in Google Maps",
            "uberUrl": f"https://m.uber.com/ul/?action=setPickup&pickup=my_location&dropoff[formatted_address]={vname}",
            "stay": "Nearest Railway / Transit: Hyderabad Deccan / Secunderabad Station. Accommodations reserved for outstation guests."
        },
        "gallery": gallery,
        "story": {
            "enabled": True,
            "label": "✦ Our Journey ✦",
            "title": "Two Hearts, One Celebration",
            "subtitle": f"Celebrating the beginning of a lifelong union of {g_first} & {b_first}",
            "items": [
                {
                    "date": "2024",
                    "title": "First Meeting & New Beginnings",
                    "desc": "With the affectionate blessings of both families, a wonderful journey was set in motion."
                },
                {
                    "date": "2025",
                    "title": "Formal Engagement & Ring Ceremony",
                    "desc": "Exchanging rings and promising a lifetime of companionship, love, and laughter."
                },
                {
                    "date": date_display,
                    "title": "The Sacred Vows & Muhurtham",
                    "desc": "Stepping into forever under the sacred mandap surrounded by our loved ones."
                }
            ]
        },
        "music": {
            "src": music_url,
            "label": "Melody",
            "stopLabel": "Pause",
            "autoplay": False,
            "volume": 0.25
        },
        "livestream": {
            "enabled": d.get("livestream", {}).get("livestreamEnabled", False),
            "label": "✦ Virtual Ceremony ✦",
            "title": "Live Wedding Webcast",
            "desc": "For distant relatives and international friends unable to attend in person, join us virtually.",
            "url": d.get("livestream", {}).get("livestreamUrl", "https://youtube.com/live"),
            "buttonText": "Watch Live Stream 🔴"
        },
        "rsvp": {
            "enabled": True,
            "mode": "both",
            "whatsappPhone": "919414972688",
            "heading": "RSVP — Will You Be Attending?",
            "fields": {
                "name": "Full Name",
                "phone": "Mobile Number",
                "guests": "Number of Guests",
                "message": "Message for the Couple"
            },
            "submit": "Confirm RSVP via WhatsApp 🙏"
        },
        "labels": {
            "countdown": "Countdown to Auspicious Muhurtham",
            "days": "Days",
            "hours": "Hours",
            "minutes": "Minutes",
            "seconds": "Seconds",
            "lineageHeading": "With Joyful Hearts",
            "lineageLabel": "The Couple & Families",
            "eventsLabel": "✦ Sacred Ceremonies ✦",
            "eventsHeading": "Wedding Itinerary",
            "venueLabel": "Venue & Directions",
            "galleryLabel": "Pre-Wedding Moments",
            "galleryHeading": "Photo Gallery",
            "galleryTapHint": "Tap any photo to view full-screen",
            "rsvpLabel": "Guest Attendance",
            "calendarAdd": "Calendar Sync",
            "qrCaption": "Venue Location QR",
            "reminder": "Set Reminder",
            "share": "Share Invitation",
            "welcome": "Cordial Wedding Invitation",
            "sealHint": "Break Seal to Open Invitation",
            "musicError": "Audio currently unavailable",
            "dressCodeHeading": "Dress Code & Attire"
        }
    }

    out_file = f"profiles/{out_slug}.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2, ensure_ascii=False)
    print(f"✅ Converted and saved profile: {out_file} (Theme: {theme}, Events: {len(events)}, Photos: {len(gallery)})")

convert_myshaadhi_to_weddingcraft("scraped_laxmikanth.json", "laxmikanth-manisha", "sindoori")
convert_myshaadhi_to_weddingcraft("scraped_mahesh_saisree.json", "mahesh-saisree", "kesariya")
