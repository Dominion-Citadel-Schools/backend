from django.contrib import admin
#from django.utils.html import format_html
from .models.herosection import HeroSection
from .models.sitestatistic import SiteStatistic
from .models.whychooseusitem import WhyChooseUsItem


@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ("headline", "is_active", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("headline",)
    readonly_fields = ("updated_at",)


@admin.register(SiteStatistic)
class SiteStatisticAdmin(admin.ModelAdmin):
    list_display = ("label", "value", "is_active")
    search_fields = ("label",)
    list_editable = ("is_active",)


@admin.register(WhyChooseUsItem)
class WhyChooseUsItemAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active")
    search_fields = ("title",)
    list_editable = ("is_active",)


'''@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ("title", "media_type", "is_active", "uploaded_at", "preview")
    list_filter = ("media_type", "is_active")
    readonly_fields = ("uploaded_at", "preview")

    def preview(self, obj):
        if obj.media_type == "IMAGE":
            return format_html(
                '<img src="{}" width="100" />',
                obj.file.url
            )
        return "No preview"

    preview.short_description = "Preview"'''
