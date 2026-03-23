from rest_framework import serializers
from media_config.api.serializers.image_serializer import ImageSerializer
from ...models.campuse import Campuse

class CampuseSerializer(serializers.ModelSerializer):
    image = ImageSerializer(many=False, read_only=True)
    features = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=True
    )

    
    def validate_features(self, value):
        # API-specific validation only
        if not value:
            return value

        return [feature.strip().title() for feature in value]
    
    class Meta:
        model = Campuse
        fields = "__all__"



