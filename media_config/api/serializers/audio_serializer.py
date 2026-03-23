from rest_framework import serializers
from media_config.models.audio import Audio
from media_config.api.services.audio_service import AudioService


class AudioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Audio
        fields = "__all__"

    def validate_duration_seconds(self, value):
        if value and value <= 0:
            raise serializers.ValidationError("Duration must be positive.")
        return value

    def create(self, validated_data):
        return AudioService.create_audio(**validated_data)
        