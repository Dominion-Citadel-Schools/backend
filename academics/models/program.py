from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from media_config.models.image import Image

class Program(models.Model):
    CATEGORY_CHOICES = [
        ("ELEMENTARY", "Elementary Education"),
        ("MIDDLE", "Middle School"),
        ("HIGH", "High School"),
    ]

    title = models.CharField(max_length=120)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    grades = models.CharField(max_length=20)
    description = models.TextField()
    key_features = models.JSONField(default=list, help_text="List of program features")
     # 🔹 Controlled externally
    enrollment_capacity = models.PositiveIntegerField(
        null=True,
        blank=True,
        editable=False  # Not allow admin manual editing for now, but not via API
    )
    full_day = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        ordering = ["category", "title"]

    def clean(self):
        errors = {}

        self.title = self.title.strip()
        if not self.title:
            errors["title"] = "Program title cannot be empty."

        self.grades = self.grades.strip()
        if not self.grades:
            errors["grades"] = "Grades field cannot be empty."

        # JSON validation
        if not isinstance(self.key_features, list):
            errors["key_features"] = "Key features must be a list."
        else:
            cleaned = []
            for feature in self.key_features:
                if not isinstance(feature, str) or not feature.strip():
                    errors["key_features"] = "Each feature must be a non-empty string."
                    break
                cleaned.append(feature.strip())
            self.key_features = cleaned

        # External API validation
        if self.enrollment_capacity is not None:
            if self.enrollment_capacity <= 0:
                errors["enrollment_capacity"] = (
                    "Enrollment capacity must be greater than zero."
                )

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
