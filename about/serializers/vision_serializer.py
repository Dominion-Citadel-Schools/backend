from rest_framework import serializers
from about.models.vision import Vision


class VisionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vision
        fields = "__all__"

    def validate_headline(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Headline too short.")
        return value

    def validate(self, attrs):
        if attrs.get("is_active"):
            if Vision.objects.filter(is_active=True).exists():
                pass  # service handles deactivation
        return attrs
