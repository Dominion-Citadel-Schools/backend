from rest_framework import serializers
from gallery.models.media import GalleryMedia


class GalleryMediaSerializer(serializers.ModelSerializer):

    image_url = serializers.SerializerMethodField()
    video_url = serializers.SerializerMethodField()

    class Meta:
        model = GalleryMedia
        fields = ["id", "image_url", "video_url"]
    
    def get_image_url(self, obj):
        if obj.image and obj.image.file:
            request = self.context.get("request")
            url = obj.image.file.url
            return request.build_absolute_uri(url) if request else url
        return None

    def get_video_url(self, obj):
        if obj.video:
            request = self.context.get("request")
            url = obj.video.url
            return request.build_absolute_uri(url) if request else url
        return None
    

    def validate(self, attrs):
        image = attrs.get("image") or getattr(self.instance, "image", None)
        video = attrs.get("video") or getattr(self.instance, "video", None)

        if not image and not video:
            raise serializers.ValidationError(
                "Media must have image or video."
            )

        if image and video:
            raise serializers.ValidationError(
                "Media cannot have both image and video."
            )

        return attrs
