from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q, Index
from about.utils.about_sections_model import AboutSectionUtilsModel


class Mission(AboutSectionUtilsModel):
    statement = models.TextField()
    is_active = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
      constraints = [
        models.UniqueConstraint(
            fields=["section_type"],
            condition=Q(is_active=True),
            name="about_mission_active_section_type_uniq",
        )
    ]
      indexes = [
        Index(
            fields=["section_type"],
            name="mission_sec_type_idx"
        ),
        Index(
            fields=["is_active"],
            name="mission_active_sec_idx",
            condition=Q(is_active=True)
        )
    ]
    def clean(self):
        if not self.statement.strip():
            raise ValidationError("Mission statement cannot be empty.")

        if len(self.statement.strip()) < 30:
            raise ValidationError("Mission statement too short.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class CoreValue(models.Model):
    mission = models.ForeignKey(
        Mission,
        related_name="core_values",
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=100)
    description = models.TextField()

    def clean(self):
        if len(self.title.strip()) < 3:
            raise ValidationError("Core value title too short.")

        if len(self.description.strip()) < 10:
            raise ValidationError("Core value description too short.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
