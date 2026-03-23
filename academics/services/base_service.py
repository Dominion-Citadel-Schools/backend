from django.core.cache import cache


class BaseService:
    model = None
    serializer_class = None
    cache_key = None
    timeout = 60 * 15

    @classmethod
    def get_data(cls):
        cached = cache.get(cls.cache_key)
        if cached:
            return cached

        queryset = cls.model.objects.filter(is_active=True)
        data = cls.serializer_class(queryset, many=True).data

        cache.set(cls.cache_key, data, cls.timeout)
        return data

    @classmethod
    def clear_cache(cls):
        cache.delete(cls.cache_key)