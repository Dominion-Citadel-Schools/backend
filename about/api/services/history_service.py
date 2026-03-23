from functools import cache
from django.db import transaction
from about.models.history import HistorySection, AchievementStats
from serializers.history_serializers import HistorySectionSerializer, AchievementStatsSerializer
from about.utils.base_sections_service import BaseSectionService 



class HistoryService(BaseSectionService):

    model = HistorySection
    serializer_class = HistorySectionSerializer
    cache_key = "about:history:active"

    @classmethod
    def get_queryset(cls):
        cached = cache.get(cls.cache_key)
        if cached:
            return cached

        history_queryset = (
            cls.model.objects
            .filter(is_active=True)
            .select_related("image")
        )

        history_data = cls.serializer_class(
            history_queryset,
            many=True
        ).data

        achievements = AchievementStats.objects.filter(
            is_active=True
        ).first()

        achievements_data = (
            AchievementStatsSerializer(achievements).data
            if achievements else None
        )

        response_data = {
            "history_sections": history_data,
            "achievements": achievements_data,
        }

        cache.set(cls.cache_key, response_data, cls.timeout)

        return response_data

    @staticmethod
    @transaction.atomic
    def activate_section(instance):
        if instance.is_active:
            HistorySection.objects.filter(
                section_type=instance.section_type,
                is_active=True
            ).exclude(pk=instance.pk).update(is_active=False)

        instance.save()
        BaseSectionService.clear_cache()
        return instance

    @staticmethod
    @transaction.atomic
    def activate_achievement(instance):
        if instance.is_active:
            AchievementStats.objects.filter(
                is_active=True
            ).exclude(pk=instance.pk).update(is_active=False)

        instance.save()
        BaseSectionService.clear_cache()
        return instance
        
