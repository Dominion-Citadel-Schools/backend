from django.db import models
from django.core.exceptions import ValidationError


class BaseMedia(models.Model):

    title = models.CharField(max_length=225, db_index=True)
    file = models.FileField(upload_to="media/")
    is_active = models.BooleanField(default=True, db_index=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )


    class Meta:
        abstract = True
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["is_active", "-created_at"]),
        ]

    def clean_title(self):
        if self.title:
            self.title = self.title.strip()

        if not self.title:
            raise ValidationError({"title": "Title cannot be empty."})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
