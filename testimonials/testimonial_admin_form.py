from django import forms
from testimonials.models import Testimonial

class TestimonialAdminForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()

        if self.instance.pk:
            old_obj = Testimonial.objects.get(pk=self.instance.pk)

            if old_obj.status in ["APPROVED", "REJECTED"]:
                raise forms.ValidationError(
                    "This testimonial has already been moderated and cannot be changed."
                )

        return cleaned_data