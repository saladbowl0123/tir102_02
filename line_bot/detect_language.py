from google.cloud import language_v1

CHINESE_LIKE = [
    'zh', # Chinese (Simplified)
    'zh-Hant', # Chinese (Traditional)
    'ja', # Japanese
    'ko', # Korean
]

ENGLISH_LIKE = [
    'en', # English
    'nl', # Dutch
    'fr', # French
    'de', # German
    'id', # Indonesian
    'it', # Italian
    'pt', # Portuguese (Brazilian & Continental)
    'es', # Spanish
    'tr', # Turkish
]

OTHER_LIKE = [
    'ar', # Arabic
    'th', # Thai
    'ru', # Russian
]

def detect_language(text):
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=text,
        type_=language_v1.Document.Type.PLAIN_TEXT,
    )

    response = client.analyze_entities(document=document)

    language = response.language

    return language

def chinese_like(text):
    return detect_language(text) in CHINESE_LIKE

def english_like(text):
    return detect_language(text) in ENGLISH_LIKE

def other_like(text):
    return detect_language(text) in OTHER_LIKE
