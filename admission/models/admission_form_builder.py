from django.db import models
from django.core.exceptions import ValidationError


class AdmissionForm(models.Model):

    name = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class AdmissionFormField(models.Model):

    class FieldType(models.TextChoices):
        TEXT = "TEXT"
        NUMBER = "NUMBER"
        SELECT = "SELECT"
        DATE = "DATE"
        TEXTAREA = "TEXTAREA"

    form = models.ForeignKey(
        AdmissionForm,
        related_name="fields",
        on_delete=models.CASCADE
    )

    label = models.CharField(max_length=255)

    field_type = models.CharField(
        max_length=20,
        choices=FieldType.choices
    )

    required = models.BooleanField(default=True)

    options = models.JSONField(
    default=list,
    help_text="Only required for SELECT field type (e.g. ['Option 1', 'Option 2'])"
    )
    
    

    def clean(self):
        if self.field_type == "SELECT":
            if not self.options or not isinstance(self.options, list):
                raise ValidationError({
                    "options": "Options are required for SELECT fields."
                })
        else:
            if self.options:
                raise ValidationError({
                    "options": "Options should only be set for SELECT fields."
                })
            
    def save(self, *args, **kwargs):
        self.full_clean()  
        super().save(*args, **kwargs)


class AdmissionFormResponse(models.Model):

    admission = models.ForeignKey(
        "Admission",
        related_name="responses",
        on_delete=models.CASCADE
    )

    field = models.ForeignKey(
        AdmissionFormField,
        on_delete=models.CASCADE
    )

    value = models.TextField()