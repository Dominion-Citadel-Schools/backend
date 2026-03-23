from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db.models import Q
from django.core.cache import cache


class SiteStatistic(models.Model):
    label = models.CharField(max_length=50)
    value = models.CharField(max_length=50)
    icon = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Site Statistic"
        verbose_name_plural = "Site Statistics"
        constraints = [
    models.UniqueConstraint(fields=["label"], name="unique_label")
]

    def clean(self):
        self.label = self.label.strip().title()
        self.value = self.value.strip()

        if not self.label:
            raise ValidationError({"label": "Label cannot be empty."})

        if not self.value:
            raise ValidationError({"value": "Value cannot be empty."})

        # Basic icon validation
        if not self.icon.strip():
            raise ValidationError({"icon": "Icon reference cannot be empty."})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.label}: {self.value}"

