from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db.models import Q
from django.core.cache import cache



class HeroSection(models.Model):
    headline = models.CharField(max_length=200)
    subheadline = models.TextField()
    primary_cta_text = models.CharField(max_length=50)
    primary_cta_url = models.URLField()
    secondary_cta_text = models.CharField(max_length=50, blank=True)
    secondary_cta_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Hero Section"
        verbose_name_plural = "Hero Section"
        constraints = [
            models.UniqueConstraint(
                fields=["is_active"],
                condition=Q(is_active=True),
                name="only_one_active_hero_section"
            )
        ]

    def clean(self):
        # Normalize text
        self.headline = self.headline.strip()
        self.primary_cta_text = self.primary_cta_text.strip()

        if not self.headline:
            raise ValidationError({"headline": "Headline cannot be empty."})

        if not self.primary_cta_text:
            raise ValidationError({"primary_cta_text": "Primary CTA text cannot be empty."})

        # Secondary CTA consistency
        if self.secondary_cta_text and not self.secondary_cta_url:
            raise ValidationError({
                "secondary_cta_url": "Secondary CTA URL is required if text is provided."
            })

        if self.secondary_cta_url and not self.secondary_cta_text:
            raise ValidationError({
                "secondary_cta_text": "Secondary CTA text is required if URL is provided."
            })

    def save(self, *args, **kwargs):
        if self.is_active:
         self.__class__.objects.filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.headline