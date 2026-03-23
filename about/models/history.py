from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q, Index
from media_config.models.image import Image
from about.utils.about_sections_model import AboutSectionUtilsModel


class AchievementStats(models.Model):
    years_of_excellence = models.PositiveIntegerField()
    graduates = models.PositiveIntegerField()
    faculty_members = models.PositiveIntegerField()
    college_acceptance_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    is_active = models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
     constraints = [
        models.UniqueConstraint(
            fields=["is_active"],
            condition=Q(is_active=True),
            name="only_one_active_achievement_stats",
        )
    ]
    indexes = [
        Index(
            fields=["is_active"],
            name="idx_active_achievement",
            condition=Q(is_active=True)
        )
    ]

    def clean(self):
        if self.college_acceptance_rate > 100:
            raise ValidationError("Acceptance rate cannot exceed 100%.")

        if self.years_of_excellence < 0:
            raise ValidationError("Years of excellence cannot be negative.")
        
    def save(self, *args, **kwargs):
     self.full_clean()
     super().save(*args, **kwargs)

    def __str__(self):
        return "Achievement Statistics"


class HistorySection(AboutSectionUtilsModel):
  
    title = models.CharField(max_length=255)
    content = models.TextField()
    founded_year = models.PositiveIntegerField(null=True, blank=True)

    is_active = models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True)

    image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )



    class Meta:
      constraints = [
        models.UniqueConstraint(
            fields=["section_type"],
            condition=Q(is_active=True),
            name="about_history_active_section_type_uniq",
        )
    ]
      indexes = [
        Index(
            fields=["section_type"],
            name="history_sec_type_idx"
        ),
        Index(
            fields=["is_active"],
            name="history_active_sec_idx",
            condition=Q(is_active=True)
        )
    ]

    def clean(self):
        # Field level validation
        if self.founded_year:
            if self.founded_year < 1800:
                raise ValidationError("Founded year cannot be before 1800.")
            if self.founded_year > 2100:
                raise ValidationError("Founded year is invalid.")

        if not self.title.strip():
            raise ValidationError("Title cannot be empty.")

        if not self.content.strip():
            raise ValidationError("Content cannot be empty.")
        
        if self.section_type == "history" and not self.founded_year:
         raise ValidationError("History section requires founded year.")
        
    def save(self, *args, **kwargs):
     self.full_clean()
     super().save(*args, **kwargs)

    
    def __str__(self):
        return f"{self.section_type} - {self.title}"
    
