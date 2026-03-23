from django.core.cache import cache


class BaseSectionService:
    model = None
    serializer_class = None
    cache_key = None
    select_related_fields = ()
    prefetch_related_fields = ()
    timeout = 60 * 10

   
    @classmethod
    def get_queryset(cls):
        cached = cache.get(cls.cache_key)
        if cached:
            return cached
        
        queryset = cls.model.objects.filter(is_active=True)

        if cls.select_related_fields:
            queryset = queryset.select_related(*cls.select_related_fields)

        if cls.prefetch_related_fields:
            queryset = queryset.prefetch_related(*cls.prefetch_related_fields)
        
        data = cls.serializer_class(queryset, many=True).data
        cache.set(cls.cache_key, data, cls.timeout)

        return data
    
    @classmethod    
    def clear_cache(cls):
        cache.delete(cls.cache_key)