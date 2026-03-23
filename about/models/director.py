from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q, Index
from media_config.models.image import Image
from about.utils.about_sections_model import AboutSectionUtilsModel


class DirectorMessage(AboutSectionUtilsModel):
    
    name = models.CharField(max_length=150)
    position = models.CharField(max_length=150)
    message = models.TextField()
    image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    is_active = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
      constraints = [
        models.UniqueConstraint(
            fields=["section_type"],
            condition=Q(is_active=True),
            name="about_dir_active_section_type_uniq",
        )
    ]
      indexes = [
        Index(
            fields=["section_type"],
            name="dir_sec_type_idx"
        ),
        Index(
            fields=["is_active"],
            name="dir_active_sec_idx",
            condition=Q(is_active=True)
        )
    ]

    def clean(self):
        if len(self.name.strip()) < 3:
            raise ValidationError("Name too short.")

        if len(self.position.strip()) < 3:
            raise ValidationError("Position too short.")

        if len(self.message.strip()) < 100:
            raise ValidationError("Director message must be meaningful.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
