from core.utils.base_aboutsection_viewset import BaseAboutSectionViewSet
from about.models.history import AchievementStats
from about.serializers.history_serializers import AchievementStatsSerializer




class AchievementViewSet(BaseAboutSectionViewSet):
    serializer_class = AchievementStatsSerializer
    queryset = AchievementStats.objects.all()