from better_profanity import profanity
import re



# Load once
profanity.load_censor_words()

# Add custom words
profanity.add_censor_words([
    # insults
    "idiot", "stupid", "dumb", "fool", "moron", "loser",

    # mild profanity
    "damn", "hell", "crap", "nonsense",

    # harassment
    "shut up", "go away", "nobody likes you",

    # toxic phrases
    "you are useless", "worthless", "hate you",

    # masked variants (common bypass tricks)
    "id!ot", "stup!d", "d@mn", "he11"
])



def normalize_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text

def clean_text(text):
    if not text:
        return text

    normalized = normalize_text(text)
    cleaned = profanity.censor(normalized, censor_char="#" )

    return cleaned