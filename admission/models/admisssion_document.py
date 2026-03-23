from django.db import models
from django.core.exceptions import ValidationError
from admission.models.admission_models import Admission
from django.forms.models import model_to_dict


class AdmissionDocumentQuerySet(models.QuerySet):
    def delete(self):
        locked_docs = self.filter(admission__status__in=["REVIEWED", "ACCEPTED", "REJECTED"])
        if locked_docs.exists():
            raise ValidationError("Cannot delete documents whose admission is locked.")
        super().delete()

class AdmissionDocument(models.Model):

    class DocumentType(models.TextChoices):
        BIRTH_CERTIFICATE = "BIRTH_CERTIFICATE"
        PASSPORT_PHOTO = "PASSPORT_PHOTO"

    admission = models.ForeignKey(
        Admission,
        related_name="documents",
        on_delete=models.CASCADE
    )

    document_type = models.CharField(
        max_length=50,
        choices=DocumentType.choices
    )

    def validate_file(file):

            allowed = ["pdf", "jpg", "png"]

            ext = file.name.split(".")[-1].lower()

            if ext not in allowed:
                raise ValidationError("Unsupported file format")

    file = models.FileField(
    upload_to="admissions/documents/",
    validators=[validate_file]
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)   
     
    def clean(self):
        super().clean()

         # Only block edits if the admission is locked and the document is being modified
        if not self._state.adding and self.admission.status in ["REVIEWED", "ACCEPTED", "REJECTED"]:
            current_values = model_to_dict(self)
            previous_values = model_to_dict(type(self).objects.get(pk=self.pk))
            changes = {k: v for k, v in current_values.items() if previous_values[k] != v}
            if changes:
                raise ValidationError(
                    "Cannot modify document when admission is reviewed, accepted, or rejected."
                )

        # Optionally, block new uploads for fully locked admissions
        if self._state.adding and self.admission.status in ["ACCEPTED", "REJECTED"]:
            raise ValidationError(
                "Cannot upload documents for accepted or rejected admissions."
            )
    objects = AdmissionDocumentQuerySet.as_manager()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)