from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.conf import settings
from core.utils.text_filters import clean_text

class ContactMessage(models.Model):

    SUBJECT_CHOICES = (
        ("GENERAL", "General Inquiry"),
        ("ADMISSION", "Admission Inquiry"),
        ("ACADEMICS", "Academics"),
        ("SUPPORT", "Support"),
    )

    full_name = models.CharField(max_length=150)

    email = models.EmailField()

    phone_number = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\+?[0-9]{7,15}$',
                message="Enter a valid phone number."
            )
        ],
        blank=True,
        null=True
    )

    subject = models.CharField(
        max_length=20,
        choices=SUBJECT_CHOICES
    )

    campus = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )
    

    is_resolved = models.BooleanField(default=False)

    resolved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="resolved_contacts"
    )

    resolved_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    message = models.TextField()

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["subject"]),
            models.Index(fields=["created_at"]),
        ]

    def clean(self):

        if not self.full_name.strip():
            raise ValidationError("Full name cannot be empty.")

        if len(self.message) < 10:
            raise ValidationError("Message must be at least 10 characters.")
        

    def save(self, *args, **kwargs):
        self.message = clean_text(self.message)
        super().save(*args, **kwargs)

    @property
    def resolved_name(self):
        if self.resolved_by:
            return f"{self.resolved_by.first_name} {self.resolved_by.last_name}".strip()
        return "-"

    def __str__(self):
        return f"{self.full_name} - {self.subject}"