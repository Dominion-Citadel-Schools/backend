import re

SPAM_PATTERNS = [
    r"http[s]?://",          # links
    r"www\.",                # websites
    r"\b\d{10,}\b",          # long numbers (phones)
    r"\$\d+",                # money amounts
    r"(free|win|earn).*(money|cash)",  # combinations
]


SPAM_WORDS = [
    # money scams
    "free money", "earn money fast", "work from home", "make money online",
    "get rich quick", "double your income", "financial freedom",

    # urgency / manipulation
    "act now", "limited time offer", "urgent response needed",
    "claim now", "exclusive deal",

    # phishing / fraud
    "verify your account", "confirm your password",
    "bank alert", "security notice",

    # adult / explicit
    "adult dating", "xxx", "porn", "sex chat", "nude",

    # crypto scams
    "bitcoin investment", "crypto giveaway", "send crypto",
    "double your bitcoin",

    # marketing spam
    "buy now", "order now", "cheap price", "discount offer",
    "best price guaranteed",

    # backlinks / SEO spam
    "visit my website", "check out my site", "click here",
    "boost your seo", "increase traffic",

    # loans / finance spam
    "instant loan", "no credit check", "apply now",
    "fast cash", "easy loan",

    # fake jobs
    "job offer", "hiring now", "no experience needed",

    # gambling
    "casino", "bet now", "win big", "jackpot",

    # common spam patterns
    "http://", "https://", "www.", ".com", ".xyz", ".ru"
]

def detect_spam(text):

    text_lower = text.lower()

    # keyword check
    if any(word in text_lower for word in SPAM_WORDS):
        return True

    # pattern check
    if any(re.search(pattern, text_lower) for pattern in SPAM_PATTERNS):
        return True

    # excessive links
    if text_lower.count("http") > 2:
        return True

    # too many uppercase words
    if sum(1 for w in text.split() if w.isupper()) > 5:
        return True

    return False