from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q, Index
from about.utils.about_sections_model import AboutSectionUtilsModel


class Vision(AboutSectionUtilsModel):
    headline = models.CharField(max_length=255)
    description = models.TextField()

    academic_excellence = models.TextField()
    character_development = models.TextField()
    global_citizenship = models.TextField()
    innovation = models.TextField()

    is_active = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
      constraints = [
        models.UniqueConstraint(
            fields=["section_type"],
            condition=Q(is_active=True),
            name="about_vision_active_section_type_uniq",
        )
    ]
      indexes = [
        Index(
            fields=["section_type"],
            name="vision_sec_type_idx"
        ),
        Index(
            fields=["is_active"],
            name="vision_active_sec_idx",
            condition=Q(is_active=True)
        )
    ]

    def clean(self):
        if len(self.headline.strip()) < 10:
            raise ValidationError("Headline too short.")

        if not self.description.strip():
            raise ValidationError("Description cannot be empty.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
