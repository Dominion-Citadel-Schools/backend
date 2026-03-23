from rest_framework import serializers
from about.models.director import DirectorMessage


class DirectorSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = DirectorMessage
        fields = [
            "id",
            "section_type",
            "name",
            "message",
            "position",
            "image_url",
            "image_id",
            "is_active",
            "updated_at",
        ]

    def get_image_url(self, obj):
        if obj.image and obj.image.file:
            request = self.context.get("request")
            url = obj.image.file.url
            return request.build_absolute_uri(url) if request else url
        return None

    def validate_name(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Name too short.")
        return value

    def validate_message(self, value):
        if len(value.strip()) < 100:
            raise serializers.ValidationError("Message too short.")
        return value

    def validate(self, attrs):
        if attrs.get("is_active") and not attrs.get("message"):
            raise serializers.ValidationError({
                "message": "Active director must have message."
            })
        return attrs
