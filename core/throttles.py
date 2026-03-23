from rest_framework.throttling import ScopedRateThrottle


class PublicContentThrottle(ScopedRateThrottle):
    scope = "public_content"