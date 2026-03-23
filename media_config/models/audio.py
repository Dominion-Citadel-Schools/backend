from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.db import models
from media_config.models.base_media import BaseMedia


class Audio(BaseMedia):

    AUDIO_EXTENSIONS = ["mp3", "wav", "ogg", "m4a"]
    MAX_SIZE = 15 * 1024 * 1024  # 15MB

    file = models.FileField(
        upload_to="audio/",
        validators=[FileExtensionValidator(allowed_extensions=AUDIO_EXTENSIONS)],
    )

    duration_seconds = models.PositiveIntegerField(null=True, blank=True)


    class Meta(BaseMedia.Meta):
        constraints = [
            models.UniqueConstraint(
                fields=["title"],
                name="unique_audio_title"
            )
        ]

    def clean(self):
        self.clean_title()

        if self.file and self.file.size > self.MAX_SIZE:
            raise ValidationError({"file": "Audio too large (max 15MB)."})
        
        if self.duration_seconds is not None and self.duration_seconds <= 0:
            raise ValidationError({"duration_seconds": "Duration must be positive."})
        
        
    def save(self, *args, **kwargs):
        self.full_clean()  
        super().save(*args, **kwargs)