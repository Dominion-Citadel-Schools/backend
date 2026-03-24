import hashlib
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.conf import settings
from core.utils.text_filters import clean_text
from core.utils.spam_filters import detect_spam
from media_config.models.image import Image


class Testimonial(models.Model):
    ROLE_CHOICES = [
        ("PARENT", "Parent"),
        ("ALUMNI", "Alumni"),
        ("STUDENT", "Student"),
    ]

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    ]

    full_name = models.CharField(max_length=225)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    class_level = models.CharField(max_length=40, null=True, blank=True)

    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )

    message = models.TextField()
    message_hash = models.CharField(
        max_length=64, 
        editable=False, 
        db_index=True, 
        null=True
        )
    graduation_year = models.PositiveIntegerField(null=True, blank=True)

    status = models.CharField(
            max_length=10, 
            choices=STATUS_CHOICES, 
            default="PENDING", 
    )

    image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="testimonials"
    )

    is_spam = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    moderated_at = models.DateTimeField(null=True, blank=True)

    moderated_by = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="moderated_testimonials"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
        models.UniqueConstraint(
            fields=["full_name", "message_hash"],
            name="unique_testimonial_hash",
            violation_error_message="This testimonial already exists."
        )
        ]
        indexes = [
            models.Index(fields=["status"], name="status_idx"),
            models.Index(fields=["role"], name="role_idx"),
        ]

    
    def clean(self):
        current_year = timezone.now().year

        # Normalize
        self.full_name = self.full_name.strip().title()
        self.message = self.message.strip()

        if not self.full_name:
            raise ValidationError({"full_name": "Full name cannot be empty."})

        if not self.message:
            raise ValidationError({"message": "Message cannot be empty."})

        # Graduation year rules
        if self.role == "ALUMNI":
            if not self.graduation_year:
                raise ValidationError({
                    "graduation_year": "Graduation year is required for alumni."
                })

            if self.graduation_year > current_year:
                raise ValidationError({
                    "graduation_year": "Graduation year cannot be in the future."
                })

        # If not alumni, graduation_year must be empty
        if self.role != "ALUMNI" and self.graduation_year:
            raise ValidationError({
                "graduation_year": "Only alumni can have a graduation year."
            })
        
        # class_level rules
        if self.role == "STUDENT":
            if not self.class_level:
                raise ValidationError({
                    "class_level": "class_level is required for STUDENT."
                })

        

        # If not STUDENT, class_level must be empty
        if self.role != "STUDENT" and self.class_level:
            raise ValidationError({
                "class_level": "Only students can have a class_level."
            })
        
        if not self.message_hash:
            self.message_hash = hashlib.sha256(self.message.encode()).hexdigest()

        if Testimonial.objects.filter(
            full_name=self.full_name,
            message_hash=self.message_hash
        ).exclude(pk=self.pk).exists():
            raise ValidationError(
                "Testimonial with this Full name and Message hash already exists."
            )

    def save(self, *args, **kwargs):
          # Validate model fields
        self.full_clean()
          # Mark as rejected if spam
        self.is_spam = detect_spam(self.message)
        # Bad word
        self.message = clean_text(self.message)
        # Save to database
        super().save(*args, **kwargs)

    def approve(self, user):
        self.status = "APPROVED"
        self.moderated_by = user
        self.moderated_at = timezone.now()
        self.save()

    def reject(self, user):
        self.status = "REJECTED"
        self.moderated_by = user
        self.moderated_at = timezone.now()
        self.save()

    @property
    def moderator_name(self):
        if self.moderated_by:
            return f"{self.moderated_by.first_name}  {self.moderated_by.last_name}".strip()
        return "-"

    def __str__(self):
        return f"{self.full_name} ({self.role})"
