from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.conf import settings
from core.utils.text_filters import clean_text


class Admission(models.Model):

    class ContactMethod(models.TextChoices):
        PHONE = "PHONE", "Phone"
        EMAIL = "EMAIL", "Email"
        WHATSAPP = "WHATSAPP", "WhatsApp"

    class Status(models.TextChoices):
        PENDING = "PENDING"
        REVIEWED = "REVIEWED"
        ACCEPTED = "ACCEPTED"
        REJECTED = "REJECTED"

    parent_name = models.CharField(max_length=255)

    email = models.EmailField()

    phone = models.CharField(
        max_length=15,
        validators=[RegexValidator(r"^\+?\d{7,15}$", "Invalid phone number")]
    )

    residential_address = models.TextField()

    preferred_contact_method = models.CharField(
        max_length=20,
        choices=ContactMethod.choices
    )

    number_of_children = models.PositiveIntegerField()

    additional_information = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    created_at = models.DateTimeField(auto_now_add=True)

    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="reviewed_admissions"
    )

    accepted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="accepted_admissions"
    )

    rejected_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="rejected_admissions"
    )

    class Meta:
        ordering = ["-created_at"]

    def clean(self):

        # children validation
        if self.number_of_children < 1:
            raise ValidationError("At least one child must be included.")
        
        if self.pk:
            actual_children = self.children.count()

            if actual_children != self.number_of_children:
             raise ValidationError(
                f"You declared {self.number_of_children} children but provided {actual_children}."
                )

        # workflow validation
        allowed = {
            "PENDING": ["REVIEWED"],
            "REVIEWED": ["ACCEPTED", "REJECTED"],
            "ACCEPTED": [],
            "REJECTED": [],
        }

        if self.pk:
            old = Admission.objects.get(pk=self.pk)

            if self.status not in allowed.get(old.status, []):
                raise ValidationError(
                    f"Invalid transition from {old.status} to {self.status}"
                )

    def save(self, *args, **kwargs):
        self.message = clean_text(self.additional_information)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.parent_name} - {self.email}"