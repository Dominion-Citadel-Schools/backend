from django.db import models
from django.core.exceptions import ValidationError


class ActivityCategory(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "name"]
        verbose_name_plural = "Activity Categories"

    def __str__(self):
        return self.name

    def clean(self):
        """
        Object level validation
        """
        if self.name:
            self.name = self.name.title()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Activity(models.Model):

    STATUS_CHOICES = (
        ("ACTIVE", "Active"),
        ("INACTIVE", "Inactive"),
    )

    category = models.ForeignKey(
        ActivityCategory,
        related_name="activities",
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=100, blank=True)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="ACTIVE"
    )

    order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "name"]
        unique_together = ("category", "name")

    def __str__(self):
        return self.name

    def clean(self):
        """
        Object-level validation
        """
        if self.status == "ACTIVE" and not self.category.is_active:
            raise ValidationError(
                "Cannot activate activity under an inactive category."
            )
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)