from rest_framework import serializers
from about.models.history import HistorySection, AchievementStats
from media_config.api.serializers.image_serializer import ImageSerializer




class AchievementStatsSerializer(serializers.ModelSerializer):

    class Meta:
        model = AchievementStats
        fields = "__all__"

    def validate_college_acceptance_rate(self, value):
        if value > 100:
            raise serializers.ValidationError(
                "Acceptance rate cannot exceed 100%"
            )
        return value

    def validate(self, attrs):
        if attrs.get("graduates", 0) < 0:
            raise serializers.ValidationError({
                "graduates": "Graduates cannot be negative."
            })
        return attrs


class HistorySectionSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = HistorySection
        fields = [
            "id",
            "section_type",
            "title",
            "content",
            "founded_year",
            "is_active",
            "image_url",
            "image_id",
            "updated_at",
        ]
    def get_image_url(self, obj):
        if obj.image and obj.image.file:
            request = self.context.get("request")
            url = obj.image.file.url
            return request.build_absolute_uri(url) if request else url
        return None

    # Field-level validation
    def validate_title(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Title too short.")
        return value

    def validate_content(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Content too short.")
        return value

    # Object-level validation
    def validate(self, attrs):
        founded_year = attrs.get("founded_year")
        if founded_year and founded_year < 1800:
            raise serializers.ValidationError({
                "founded_year": "Founded year must be realistic."
            })
        return attrs
    
    # object-level validation for achievement stats
    def validate(self, attrs):
        achievement_stats = self.initial_data.get("achievement_stats", [])

        if len(achievement_stats) < 3:
            raise serializers.ValidationError({
                "achievement_stats": "At least 3 achievement stats required."
            })

        return attrs

class AchievementStatsSerializer(serializers.ModelSerializer):

    class Meta:
        model = AchievementStats
        fields = "__all__"

    def validate_college_acceptance_rate(self, value):
        if value > 100:
            raise serializers.ValidationError(
                "Acceptance rate cannot exceed 100%"
            )
        return value

    def validate(self, attrs):
        if attrs.get("graduates", 0) < 0:
            raise serializers.ValidationError({
                "graduates": "Graduates cannot be negative."
            })
        return attrs
