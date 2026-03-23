from about.serializers.history_serializers import AchievementStatsSerializer, HistorySectionSerializer
from rest_framework import serializers



class HistoryNestedSerializer(serializers.Serializer):
    sections = HistorySectionSerializer(many=True)
    achievements = AchievementStatsSerializer(allow_null=True)
