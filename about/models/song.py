from django.db import models
from django.core.exceptions import ValidationError
from media_config.models.audio import Audio
from about.utils.about_sections_model import AboutSectionUtilsModel



class SchoolSong(AboutSectionUtilsModel):
    title = models.CharField(max_length=150)
    lyrics = models.TextField()
    audio = models.ForeignKey(
        Audio,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    is_active = models.BooleanField(default=True)

    def clean(self):
        if len(self.title.strip()) < 3:
            raise ValidationError("Title too short.")

        if len(self.lyrics.strip()) < 20:
            raise ValidationError("Lyrics too short.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
