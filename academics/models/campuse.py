from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from media_config.models.image import Image

class Campuse(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=150)
    description = models.TextField()
    year_established = models.PositiveIntegerField()
    features = models.JSONField(
    default=list,
    help_text="List of campus features"
)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
    
     #✅ Domain-level validation
    def clean(self):
        errors = {}

        # features validation
        if not isinstance(self.features, list):
            errors["features"] = "Features must be a list."
        else:
            cleaned = []
            for feature in self.features:
                if not isinstance(feature, str) or not feature.strip():
                    errors["features"] = "Each feature must be a non-empty string."
                    break
                cleaned.append(feature.strip())

            self.features = cleaned  # normalize once

        # year validation
        if self.year_established > now().year:
            errors["year_established"] = "Year established cannot be in the future."

        if errors:
            raise ValidationError(errors)

    # ✅ Enforce validation globally
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)



