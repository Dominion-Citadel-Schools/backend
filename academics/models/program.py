from django.db import models
from django.core.exceptions import ValidationError
from media_config.models.image import Image


class Program(models.Model):
    CATEGORY_CHOICES = [
        ("ELEMENTARY", "Elementary Education"),
        ("MIDDLE", "Middle School"),
        ("HIGH", "High School"),
    ]

    title = models.CharField(max_length=120)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()

    enrollment_capacity = models.PositiveIntegerField(
        null=True,
        blank=True,
        editable=False
    )

    full_day = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["category", "title"]

    def clean(self):
        if not self.title.strip():
            raise ValidationError({"title": "Title cannot be empty"})

    def __str__(self):
        return self.title
    

class ProgramCampus(models.Model):
    program = models.ForeignKey(
        Program,
        related_name="campuses",
        on_delete=models.CASCADE
    )

    campus_name = models.CharField(max_length=100)

    features = models.JSONField(
        default=list,
        help_text="List of features for this campus"
    )

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def clean(self):
        errors = {}

        if not self.campus_name.strip():
            errors["campus_name"] = "Campus name cannot be empty."

        if not isinstance(self.features, list):
            errors["features"] = "Features must be a list."
        else:
            cleaned = []
            for f in self.features:
                if not isinstance(f, str) or not f.strip():
                    errors["features"] = "Each feature must be a non-empty string."
                    break
                cleaned.append(f.strip())
            self.features = cleaned

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return f"{self.program.title} - {self.campus_name}"
