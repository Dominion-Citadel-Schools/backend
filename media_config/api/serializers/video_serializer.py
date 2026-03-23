from rest_framework import serializers
from media_config.models.video import Video
from media_config.api.services.video_service import VideoService


class VideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Video
        fields = "__all__"

    def validate_duration_seconds(self, value):
        if value and value <= 0:
            raise serializers.ValidationError("Duration must be positive.")
        return value
    
    def create(self, validated_data):
        return VideoService.create_video(**validated_data)
