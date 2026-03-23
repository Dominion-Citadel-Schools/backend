from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db.models import Q
from django.core.cache import cache


class WhyChooseUsItem(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["title"]

    def clean(self):
        self.title = self.title.strip().title()

        if not self.title:
            raise ValidationError({"title": "Title cannot be empty."})

        if not self.description.strip():
            raise ValidationError({"description": "Description cannot be empty."})

        if not self.icon.strip():
            raise ValidationError({"icon": "Icon reference cannot be empty."})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title