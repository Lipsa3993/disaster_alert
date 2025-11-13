# utils/translator.py
# Simple phrase mapping for critical messages (guaranteed quality).
translations = {
    "Heavy rainfall alert!": {"hi": "भारी वर्षा की चेतावनी!", "or": "ଭାରୀ ବର୍ଷା ସତର୍କତା!"},
    "Strong wind alert!": {"hi": "तेज़ हवा की चेतावनी!", "or": "ଜୋର ବାତାସ ସତର୍କତା!"},
    "Extreme heat alert!": {"hi": "अत्यधिक गर्मी की चेतावनी!", "or": "ଅତ୍ୟଧିକ ତାପ ସତର୍କତା!"},
    "Extreme cold alert!": {"hi": "अत्यधिक ठंड की चेतावनी!", "or": "ତିବ୍ର ଶୀତ ସତର୍କତା!"},
    "Severe Thunderstorm warning!": {"hi": "गंभीर तूफानी चेतावनी!", "or": "ତୀବ୍ର ଧଡ଼ି/ତୁଫାନ ସତର୍କତା!"},
    "Weather is stable. No alerts.": {"hi": "मौसम स्थिर है। कोई चेतावनी नहीं।", "or": "ଆବହାଓା ସ୍ଥିର ଅଛି। କouଣସି ସତର୍କତା ନାହିଁ।"}
}

def translate_alerts(alerts, lang_code):
    if lang_code not in ("hi", "or"):
        return alerts
    translated = []
    for a in alerts:
        key = a.replace("✅ ", "").replace("⚠️ ", "").replace("💧 ", "").replace("🔥 ", "").replace("💨 ", "")
        t = translations.get(key, {}).get(lang_code)
        translated.append(t if t else a)
    return translated
