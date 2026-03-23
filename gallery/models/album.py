from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from media_config.models.image import Image
from core.models.audit import AuditFields


class GalleryAlbum(AuditFields):

    ALBUM_TYPE_CHOICES = (
        ("PICTURE", "Picture"),
        ("VIDEO", "Video"),
    )

    title = models.CharField(max_length=255)
    album_type = models.CharField(max_length=10, choices=ALBUM_TYPE_CHOICES)
    cover_image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="gallery_covers"
    )

    event_date = models.DateField()
    is_published = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-event_date"]
        indexes = [
            models.Index(fields=["album_type"]),
            models.Index(fields=["is_published"]),
        ]

    
    def clean(self):
        if not self.title.strip():
            raise ValidationError("Album title cannot be empty.")

        if self.event_date > timezone.now().date():
            raise ValidationError("Event date cannot be in the future.")

        if self.album_type == "VIDEO" and not self.cover_image:
            raise ValidationError("Video albums must have a cover image.")
        
        # Prevent publishing empty albums
        if self.pk and self.is_published:
          if not self.media_items.exists():
            raise ValidationError("Cannot publish album without media.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


    def __str__(self):
        return self.title
