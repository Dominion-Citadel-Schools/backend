from django.utils import timezone
from django.db import models
from django.core.exceptions import ValidationError
from media_config.models.image import Image
from about.utils.about_sections_model import AboutSectionUtilsModel
from core.models.audit import AuditFields



class SchoolTour(AboutSectionUtilsModel, AuditFields):
    ALBUM_TYPE_CHOICES = (
         ("PICTURE", "Picture"),
         ("VIDEO", "Video"),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    album_type = models.CharField(max_length=10, choices=ALBUM_TYPE_CHOICES, default="PICTURE")
    cover_image = models.ForeignKey(
        Image,
         on_delete=models.SET_NULL,
         null=True,
         blank=True,
         related_name="school_tour_covers"
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
        errors = {}

        if not self.title or not self.title.strip():
            errors["title"] = "Album title cannot be empty."

        if not self.description or not self.description.strip():
            errors["description"] = "Description cannot be empty."

        if not self.event_date:
            errors["event_date"] = "Event date is required."
        elif self.event_date > timezone.now().date():
            errors["event_date"] = "Event date cannot be in the future."

        if self.album_type == "VIDEO" and not self.cover_image:
            errors["cover_image"] = "Video albums must have a cover image."

        if self.pk and self.is_published:
            if not self.school_tour_media_items.exists():
                errors["is_published"] = "Cannot publish album without media."

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


    def __str__(self):
        return self.title

