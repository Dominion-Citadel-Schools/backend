from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.db import models
from media_config.models.base_media import BaseMedia


class Video(BaseMedia):

    VIDEO_EXTENSIONS = ["mp4", "mov", "avi"]
    MAX_SIZE = 50 * 1024 * 1024  # 50MB

    file = models.FileField(
        upload_to="videos/",
        validators=[FileExtensionValidator(allowed_extensions=VIDEO_EXTENSIONS)],
    )

    duration_seconds = models.PositiveIntegerField(null=True, blank=True)

    class Meta(BaseMedia.Meta):
        constraints = [
            models.UniqueConstraint(
                fields=["title"],
                name="unique_video_title"
            )
        ]

    def clean(self):
        self.clean_title()

        if self.file and self.file.size > self.MAX_SIZE:
            raise ValidationError({"file": "Video too large (max 50MB)."})
        
        if self.duration_seconds is not None and self.duration_seconds <= 0:
            raise ValidationError({"duration_seconds": "Duration must be positive."})
        
        
    def save(self, *args, **kwargs):
        self.full_clean()  
        super().save(*args, **kwargs)
