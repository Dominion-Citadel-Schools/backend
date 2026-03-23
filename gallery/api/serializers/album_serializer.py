from django.utils import timezone
from rest_framework import serializers
from gallery.models.album import GalleryAlbum
from .media_serializer import GalleryMediaSerializer


class GalleryAlbumSerializer(serializers.ModelSerializer):

    media_items = serializers.SerializerMethodField()
    media_count = serializers.IntegerField(read_only=True)
    cover_image_url = serializers.SerializerMethodField()

    class Meta:
        model = GalleryAlbum
        fields = [
            "id",
            "title",
            "album_type",
            "cover_image_url",
            "event_date",
            "media_items",
            "media_count",
            "is_published",
        ]

    def get_media_items(self, obj):
        media = getattr(obj, "filtered_media_items", [])
        return GalleryMediaSerializer(
            media,
            many=True
        ).data

    def get_cover_image_url(self, obj):
        if obj.cover_image and obj.cover_image.file:
            request = self.context.get("request")
            url = obj.cover_image.file.url
            return request.build_absolute_uri(url) if request else url
        return None

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "Title cannot be blank."
            )
        return value

    def validate(self, attrs):
        event_date = attrs.get("event_date")

        if event_date and event_date > timezone.now().date():
            raise serializers.ValidationError(
                "Event date cannot be in the future."
            )

        return attrs
