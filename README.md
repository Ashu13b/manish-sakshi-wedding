# 🌸 विवाह परियोजना कार्यशाला (Manish & Sakshi Wedding Platform)

**वर-वधू:** चि. मनीष संग सौ. कां. साक्षी  
**शुभ विवाह तिथि:** 21 नवम्बर 2026, शनिवार  
**प्रीतिभोज:** 19 नवम्बर 2026, गुरूवार (लक्ष्मी मैरिज गार्डन, गुर्जर कॉलोनी, छावनी, नीमकाथाना)  
**मुख्य स्थल:** ग्राम-भांडाला (हसामपुर), जिला-सीकर (राज.)  

---

## 🏛️ द्वि-स्तरीय परियोजना विभाजन (Two-Part Architecture)

यह परियोजना दो पूर्णतः स्वतंत्र एवं विशिष्ट भागों (Two Distinct Parts) में विभाजित है:

```text
/storage/emulated/0/workspace/wedding/
│
├── 📂 01-wedding-card/          --> [PART 1] भौतिक विवाह पत्रिका एवं पेजमेकर/ऑफ़सेट पैकेज
│   ├── pagemaker_and_press_package/ (पेजमेकर KrutiDev 010, RTF, PTX, 300 DPI PDF, ब्लैक प्लेट्स)
│   ├── generate_mobile_proof_pdf.py (मोबाइल प्रूफ PDF ~540 KB)
│   ├── generate_original_enhanced_press_ready.py (मूल सममितीय प्रेस मास्टर)
│   ├── elite_print_preview.html (प्रिंट प्रिव्यू एवं डाउनलोड हब)
│   └── README.md
│
└── 📂 02-wedding-website/       --> [PART 2] इंटरैक्टिव वेडिंग वेबसाइट एवं डिजिटल आमंत्रण प्लेटफॉर्म
    ├── index.html (मुख्य सिंगल-पेज वेब एप्लिकेशन: शहनाई, लिफ़ाफ़ा, मैप, RSVP)
    ├── control_center.html (वेडिंगक्राफ्ट मॉड्यूलर कंट्रोल सेंटर व सिम्युलेटर)
    ├── studio.html (विज़ुअल थीम डिज़ाइन स्टूडियो)
    ├── maker.py (वेबसाइट सीएलआई इंजन)
    ├── server.py (डायनामिक मल्टी-वेडिंग सर्वर)
    ├── profiles/ (विवाह डेटा प्रोफाइल)
    ├── themes/ (सीएसएस थीम)
    └── README.md
```

---

## 🖨️ भाग १: भौतिक विवाह पत्रिका (Part 1: Wedding Card & Prepress Suite)

भौतिक पत्रिका मुद्रण (ऑफसेट प्रिंटिंग, पेजमेकर 7.0, स्क्रीन प्रिंटिंग) हेतु समर्पित:

- **लोकेशन:** [`01-wedding-card/`](file:///storage/emulated/0/workspace/wedding/01-wedding-card/README.md)
- **मोबाइल संदर्भ PDF (~540 KB):** [`MANISH_SAKSHI_MOBILE_CARD_3PAGES.pdf`](file:///storage/emulated/0/workspace/wedding/01-wedding-card/pagemaker_and_press_package/MANISH_SAKSHI_MOBILE_CARD_3PAGES.pdf) *(मुद्रक ऑपरेटर हेतु WhatsApp फ्रेंडली)*
- **वाणिज्यिक ऑफ़सेट मास्टर PDF:** [`MANISH_SAKSHI_ORIGINAL_ENHANCED_PRESS_READY.pdf`](file:///storage/emulated/0/workspace/wedding/01-wedding-card/pagemaker_and_press_package/MANISH_SAKSHI_ORIGINAL_ENHANCED_PRESS_READY.pdf) *(लीगल कवर 8.5"×14" + A3 इनर स्प्रेड 8"×12.5")*
- **स्क्रीन प्रिंटिंग बटर पेपर प्लेट्स:** [`ORIGINAL_ENHANCED_BLACK_PLATES_ONLY.pdf`](file:///storage/emulated/0/workspace/wedding/01-wedding-card/pagemaker_and_press_package/ORIGINAL_ENHANCED_MASTER/ORIGINAL_ENHANCED_BLACK_PLATES_ONLY.pdf) *(100% सॉलिड ब्लैक)*
- **पेजमेकर ऑपरेटर फ़ाइलें:** [`manish_sakshi_pagemaker_krutidev.txt`](file:///storage/emulated/0/workspace/wedding/01-wedding-card/pagemaker_and_press_package/1_PAGEMAKER_FILES/manish_sakshi_pagemaker_krutidev.txt) | [`PRINTER_INSTRUCTIONS.txt`](file:///storage/emulated/0/workspace/wedding/01-wedding-card/pagemaker_and_press_package/PRINTER_INSTRUCTIONS.txt)
- **वेब पूर्वावलोकन:** [`elite_print_preview.html`](file:///storage/emulated/0/workspace/wedding/01-wedding-card/elite_print_preview.html)

---

## 🌐 भाग २: इंटरैक्टिव वेडिंग वेबसाइट (Part 2: Wedding Website & RSVP Engine)

डिजिटल आमंत्रण, व्हाट्सएप शेयरिंग एवं मेहमानों के इंटरैक्शन हेतु समर्पित:

- **लोकेशन:** [`02-wedding-website/`](file:///storage/emulated/0/workspace/wedding/02-wedding-website/README.md)
- **लाइव वेबसाइट URL:** `http://localhost:8000/w/manish-sakshi` (या `http://localhost:8000/index.html`)
- **कंट्रोल सेंटर:** `http://localhost:8000/control_center.html` (या `http://localhost:8000/`)
- **वैयक्तिकृत अतिथि लिंक:** `?guest=Sharma+Family&fam=1` (डिजिटल लिफ़ाफ़ा ओपनिंग एनीमेशन सहित)
- **विशेषताएं:** पारम्परिक शहनाई संगीत (`shehnai-loop.mp3`), लाइव उल्टी गिनती, गूगल मैप्स नेविगेशन, व्हाट्सएप 1-क्लिक आरएसवीपी, फोटो गैलरी।

---

## 🚀 क्विक कमांड्स (Quick Commands)

```bash
# 1. सर्वर प्रारंभ करें (Port 8000)
python3 server.py 8000

# 2. भाग १ कार्ड PDF पुनः जनरेट करें
cd 01-wedding-card && python3 generate_mobile_proof_pdf.py && python3 generate_original_enhanced_press_ready.py

# 3. भाग २ वेबसाइट बिल्ड करें
cd 02-wedding-website && python3 maker.py build --slug manish-sakshi
```
