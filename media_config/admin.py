from django.contrib import admin
from media_config.models.audio import Audio
from .base_admin import BaseValidatedAdmin
from media_config.models.image import Image
from media_config.models.video import Video


@admin.register(Audio)
class AudioAdmin(BaseValidatedAdmin):

    list_display = ("title", "duration_seconds", "is_active", "uploaded_at", "preview")
    list_filter = ("is_active",)
    search_fields = ("title",)
    readonly_fields = ("uploaded_at", "preview")





@admin.register(Image)
class ImageAdmin(BaseValidatedAdmin):

    list_display = ("title", "is_active", "uploaded_at", "preview")
    list_filter = ("is_active",)
    search_fields = ("title", "alt_text")
    readonly_fields = ("uploaded_at","preview")
    ordering = ("-uploaded_at",)

   


@admin.register(Video)
class VideoAdmin(BaseValidatedAdmin):

    list_display = ("title", "duration_seconds", "is_active", "uploaded_at", "preview")
    list_filter = ("is_active",)
    search_fields = ("title",)
    readonly_fields = ("uploaded_at", "preview")

