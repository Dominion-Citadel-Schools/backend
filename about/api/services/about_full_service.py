from django.core.cache import cache
from about.models.vision import Vision
from about.models.history import AchievementStats, HistorySection
from about.models.mission import  Mission
from about.models.director import DirectorMessage
from about.models.school_tour import SchoolTour
from about.models.song import SchoolSong
from django.db.models import Count
from about.serializers.mission_serializer import MissionSerializer
from .cache import ABOUT_CACHE_KEY, TIMEOUT


class AboutFullService:

    @staticmethod
    def get_full_aggregation_data():

        cached = cache.get(ABOUT_CACHE_KEY)
        if cached:
            return cached

        mission_instance = (
        Mission.objects
       .filter(is_active=True)
       .prefetch_related("core_values")
       .first()
)

      # ✅ Serialize it immediately (IMPORTANT)
        mission_data = (
            MissionSerializer(mission_instance).data
            if mission_instance
            else None
        )

        history_queryset = (
            HistorySection.objects
            .filter(is_active=True)
            .select_related("image")
        )

        data = {
            "vision": Vision.objects.filter(is_active=True).first(),

            "mission": mission_data, 

            "director": DirectorMessage.objects
                .select_related("image")
                .filter(is_active=True)
                .first(),

            "school_tours": SchoolTour.objects
                .filter(is_published=True)
                .annotate(media_count=Count("school_tour_media_items"))
                .order_by("-created_at"),

            "school_song": SchoolSong.objects
                .select_related("audio")
                .filter(is_active=True)
                .first(),

            "history": {
                "sections": history_queryset,
                "achievements": AchievementStats.objects
                    .filter(is_active=True)
                    .first()
            }
        }

        cache.set(ABOUT_CACHE_KEY, data, TIMEOUT)
        return data