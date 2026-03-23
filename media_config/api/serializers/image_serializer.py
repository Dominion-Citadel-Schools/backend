from rest_framework import serializers
from media_config.models.image import Image
#from media_config.api.services.image_service import ImageService



class ImageSerializer(serializers.ModelSerializer):
    file_size = serializers.SerializerMethodField()
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = "__all__"
        read_only_fields = ( "uploaded_at", "file_size")

    # Field-level validation
    def validate_title(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value
    
    def validate_width(self, value):
        if value < 300:
            raise serializers.ValidationError(
                "Minimum width is 300 pixels."
            )
        return value
    
    def validate_height(self, value):
        if value < 300:
            raise serializers.ValidationError(
                "Minimum height is 300 pixels."
            )
        return value

    # Object-level validation
    def validate(self, attrs):
        if not attrs.get("alt_text"):
            raise serializers.ValidationError({
                "alt_text": "Alt text is required."
            })
        return attrs
    
    def validate(self, attrs):

        width = attrs.get("width")
        height = attrs.get("height")

        if width and height:
            ratio = width / height

            if ratio < 0.5 or ratio > 2:
                raise serializers.ValidationError(
                    "Invalid aspect ratio."
                )

        return attrs
    
    #def create(self, validated_data):
        #return ImageService.create_image(**validated_data)
    
    def get_file_size(self, obj):
     if obj.file:
        return obj.file.size
     return None
    
    
    def get_file_url(self, obj):
     if obj.file:
      return obj.file.url
     return None
