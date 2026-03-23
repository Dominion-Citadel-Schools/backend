from django.db import models
from django.core.exceptions import ValidationError
from admission.models.admission_models import Admission
from django.forms.models import model_to_dict


class ChildQuerySet(models.QuerySet):
    def delete(self):
        # Prevent bulk delete if any child has a locked admission
        locked_children = self.filter(admission__status__in=["REVIEWED", "ACCEPTED", "REJECTED"])
        if locked_children.exists():
            raise ValidationError("Cannot delete children whose admission is locked.")
        super().delete()

class Child(models.Model):

    class Gender(models.TextChoices):
        MALE = "MALE"
        FEMALE = "FEMALE"

    admission = models.ForeignKey(
        Admission,
        related_name="children",
        on_delete=models.CASCADE
    )

    full_name = models.CharField(max_length=255)

    age = models.PositiveIntegerField()

    date_of_birth = models.DateField()

    gender = models.CharField(
        max_length=10,
        choices=Gender.choices
    )

    class_seeking_admission = models.CharField(max_length=100)

    current_school = models.CharField(max_length=255)

    current_class_grade = models.CharField(max_length=100)

    proposed_term = models.CharField(max_length=100)

    campus = models.CharField(max_length=150)

    def clean(self):

        if self.age > 25:
            raise ValidationError("Invalid child age.")
        
    
         # Only block edits to *modified* fields after admission is locked
        if not self._state.adding and self.admission.status in ["REVIEWED", "ACCEPTED", "REJECTED"]:
            # Detect if any relevant field is actually being changed
            current_values = model_to_dict(self)
            previous_values = model_to_dict(type(self).objects.get(pk=self.pk))
            
            # Ignore changes to non-child fields if any
            changes = {k: v for k, v in current_values.items() if previous_values[k] != v}
            if changes:  # Only raise error if there are changes
                raise ValidationError("Cannot modify child when admission is reviewed, accepted, or rejected.")
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    objects = ChildQuerySet.as_manager()

    def __str__(self):
        return self.full_name