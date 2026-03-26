from django.contrib import admin
from django.utils.html import format_html


class BaseValidatedAdmin(admin.ModelAdmin):
    
    def preview(self, obj):
        try:
            # IMAGE PREVIEW
            image = getattr(obj, "image", None)
            if image and hasattr(image, 'file') and image.file:
                return format_html(
                    '<img src="{}" width="120" style="border-radius:6px;" />',
                    image.file.url
                )

            # VIDEO PREVIEW
            video = getattr(obj, "video", None)
            if video and hasattr(video, 'file') and video.file:
                return format_html(
                    '<video width="180" controls style="border-radius:6px;">'
                    '<source src="{}" type="video/mp4">'
                    '</video>',
                    video.file.url
                )

            # AUDIO PREVIEW ✅
            audio = getattr(obj, "audio", None)
            if audio and hasattr(audio, 'file') and audio.file:
                return format_html(
                    '<audio controls style="width:180px;">'
                    '<source src="{}" type="audio/mpeg">'
                    'Your browser does not support the audio element.'
                    '</audio>',
                    audio.file.url
                )

            return "No Preview"

        except Exception as e:
            return f"No Preview ({e})"
        
    preview.short_description = "preview"
    

    def save_model(self, request, obj, form, change):
        obj.full_clean()
        super().save_model(request, obj, form, change)
