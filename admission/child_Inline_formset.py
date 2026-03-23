from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError


class ChildInlineFormSet(BaseInlineFormSet):

    def clean(self):
        super().clean()

        total_children = 0

        for form in self.forms:
            if not form.cleaned_data.get("DELETE", False) and form.cleaned_data:
                total_children += 1

        declared_children = self.instance.number_of_children

        if total_children != declared_children:
            raise ValidationError(
                f"You declared {declared_children} children but provided {total_children}."
            )