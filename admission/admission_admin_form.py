from django import forms
from django.core.exceptions import ValidationError
from admission.models.admission_models import Admission


class AdmissionAdminForm(forms.ModelForm):
    class Meta:
        model = Admission
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()

        status = cleaned_data.get("status")
        number_of_children = cleaned_data.get("number_of_children")
        instance = self.instance

        # 🚫 IMPORTANT: prevent checking relations before save
        if not instance.pk:
            if status in ["REVIEWED", "ACCEPTED", "REJECTED"]:
                raise ValidationError(
                    "You must save the admission before setting it to REVIEWED, ACCEPTED or REJECTED."
                )
            return cleaned_data

        # ✅ Now safe to check children
        actual_children = instance.children.count()

        if status == "REVIEWED":
            if number_of_children != actual_children:
                raise ValidationError(
                    f"You declared {number_of_children} children but provided {actual_children}."
                )

        if status == "ACCEPTED":
            if actual_children == 0:
                raise ValidationError(
                    "Cannot accept admission without at least one child."
                )
            
        if status == "REJECTED":
            if actual_children == 0:
                raise ValidationError(
                    "Cannot reject admission without at least one child."
                )

        return cleaned_data