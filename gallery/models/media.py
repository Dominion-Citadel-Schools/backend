from django.db import models
from django.core.exceptions import ValidationError
from media_config.models.image import Image
from media_config.models.video import Video
from .album import GalleryAlbum


class GalleryMedia(models.Model):

    album = models.ForeignKey(
        GalleryAlbum,
        on_delete=models.CASCADE,
        related_name="media_items"
    )

    image = models.ForeignKey(
        Image,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    video = models.ForeignKey(
        Video,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("album", "image", "video")

    def clean(self):
        if not self.image and not self.video:
            raise ValidationError("Media must contain either image or video.")

        if self.image and self.video:
            raise ValidationError("Media cannot contain both image and video.")

        if self.album.album_type == "PICTURE" and not self.image:
            raise ValidationError("Picture album must contain images only.")

        if self.album.album_type == "VIDEO" and not self.video:
            raise ValidationError("Video album must contain videos only.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
