from rest_framework import serializers
from media_config.api.serializers.image_serializer import ImageSerializer
from ...models.program import  Program

class ProgramSerializer(serializers.ModelSerializer):
    image = ImageSerializer(many=False, read_only=True)
    enrollment_capacity = serializers.IntegerField(read_only=True)

    key_features = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=True
    )


    def validate_features(self, value):
        # API-specific validation only
        return [feature.strip().title() for feature in value]
    
    class Meta:
        model = Program
        fields = "__all__"
