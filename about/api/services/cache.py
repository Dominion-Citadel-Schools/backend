from django.core.cache import cache

ABOUT_CACHE_KEY = "about_full_page"
TIMEOUT = 60 * 10


def clear_about_cache():
    cache.delete(ABOUT_CACHE_KEY)
