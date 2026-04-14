from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError
from gallery.models.album import GalleryAlbum
from django.forms.models import BaseInlineFormSet


class GalleryAlbumAdminForm(forms.ModelForm):

    class Meta:
        model = GalleryAlbum
        fields = "__all__"

    def clean_event_date(self):
        event_date = self.cleaned_data.get("event_date")

        if not event_date:
            raise forms.ValidationError("Event date is required.")

        if event_date > timezone.now().date():
            raise forms.ValidationError("Event date cannot be in the future.")

        return event_date

    def clean(self):
        cleaned_data = super().clean()

        is_published = cleaned_data.get("is_published")

        if is_published and not self.instance.pk:
            raise ValidationError(
                "You must save the album before publishing."
            )

        return cleaned_data
    




class GalleryMediaInlineFormSet(BaseInlineFormSet):

    def clean(self):
        super().clean()

        if any(self.errors):
            return

        parent = self.instance
        total_media = 0

        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get("DELETE", False):
                total_media += 1

        if parent.is_published and total_media == 0:
            raise ValidationError(
                "Cannot publish album without media."
            )

