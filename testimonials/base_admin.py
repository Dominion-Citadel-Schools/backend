from django.contrib import admin
from django.utils.html import format_html

class BaseValidatedAdmin(admin.ModelAdmin):
    
    def preview(self, obj):
        if not obj.image:
            return "No Image"

        try:
            return format_html(
            '<img src="{}" width="120" style="border-radius:6px;" />',
            obj.image.file.url
        )
        except Exception:
            return "No Preview"
    preview.short_description = "preview"
    

    def save_model(self, request, obj, form, change):
        obj.full_clean()
        super().save_model(request, obj, form, change)