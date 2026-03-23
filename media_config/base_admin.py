from django.contrib import admin
from core.utils.media_preview import media_preview


class BaseValidatedAdmin(admin.ModelAdmin):
    def preview(self, obj):
        return media_preview(obj)
    
    preview.short_description = "preview"

    def save_model(self, request, obj, form, change):
        obj.full_clean()
        super().save_model(request, obj, form, change)
