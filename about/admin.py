from django.contrib import admin
from about.school_tour_media_adminform import SchoolTourAlbumAdminForm, SchoolTourMediaInlineFormSet
from about.models.school_tour_media import SchoolTourMedia
from .models.history import HistorySection, AchievementStats
from .models.mission import CoreValue, Mission
from .models.director import DirectorMessage
from .models.vision import Vision
from .models.school_tour import SchoolTour
from .models.song import SchoolSong
from .base_admin import BaseValidatedAdmin
from django.core.exceptions import ValidationError
from django.utils.html import format_html
from django.db.models import Count
from core.utils.media_preview import media_preview
from core.utils.func_create_update_delete import (
    set_created_by,
    set_deleted_by,
    set_updated_by,
    bulk_delete_with_audit
)


@admin.register(HistorySection)
class HistorySectionAdmin(BaseValidatedAdmin):

    list_display = (
        "section_type",
        "title",
        "is_active",
        "updated_at",
        "preview",
    )

    autocomplete_fields = ("image",)
    readonly_fields = ("updated_at", "preview")

    fieldsets = (
        ("Basic Info", {
            "fields": ("section_type", "title", "content", "founded_year")
        }),
        ("Image", {
            "fields": ("image", "preview")
        }),
        ("Status", {
            "fields": ("is_active",)
        }),
        ("System", {
            "fields": ("updated_at",)
        }),
    )



@admin.register(AchievementStats)
class AchievementStatsAdmin(BaseValidatedAdmin):
    list_display = (
        "years_of_excellence",
        "graduates",
        "faculty_members",
        "college_acceptance_rate",
        "is_active",
        "updated_at",
    )
    list_filter = ("is_active",)
    readonly_fields = ("updated_at",)

    fieldsets = (
        ("Statistics", {
            "fields": (
                "years_of_excellence",
                "graduates",
                "faculty_members",
                "college_acceptance_rate",
            )
        }),
        ("Status", {
            "fields": ("is_active",)
        }),
        ("System", {
            "fields": ("updated_at",)
        }),
    )


class CoreValueInline(admin.TabularInline):
    model = CoreValue
    extra = 1

@admin.register(Vision)
class VisionAdmin(BaseValidatedAdmin):
    list_display = ("headline", "is_active", "updated_at")
    list_filter = ("is_active",)


@admin.register(Mission)
class MissionAdmin(BaseValidatedAdmin):
    list_display = ("statement", "is_active")
    inlines = [CoreValueInline]



class SchoolTourMediaInline(admin.TabularInline):
    model = SchoolTourMedia
    formset = SchoolTourMediaInlineFormSet
    extra = 1
    fields = ("image", "video", "preview")
    readonly_fields = ("preview",)

    def preview(self, obj):
        return media_preview(obj)
    preview.short_description = "Preview"


class AlbumStatusFilter(admin.SimpleListFilter):
    title = "Album Status"
    parameter_name = "album_status"

    def lookups(self, request, model_admin):
        return (
            ("active", "Active Albums"),
            ("deleted", "Deleted Albums"),
        )

    def queryset(self, request, queryset):
        if self.value() == "active":
            return queryset.filter(is_deleted=False)

        if self.value() == "deleted":
            return queryset.filter(is_deleted=True)

        return queryset

@admin.register(SchoolTour)
class SchoolTourAlbumAdmin(BaseValidatedAdmin):

    change_list_template = "admin/schooltour_dashboard.html"
    form =  SchoolTourAlbumAdminForm
    inlines = [SchoolTourMediaInline]


    list_display = (
        "title",
        "album_type",
        "status_badge",
        "event_date",
        "created_at",
        "created_name",
        "updated_name",
        "deleted_name",

    )

    list_filter = (
        "album_type",
        "is_published",
        "event_date",
        AlbumStatusFilter,
    )

    search_fields = ("title",)

    ordering = ("-event_date",)

    readonly_fields = ("created_at", "updated_at", "created_by","updated_by","deleted_by")

    def changelist_view(self, request, extra_context=None):

        if not request.GET.get("album_status"):
            request.GET = request.GET.copy()
            request.GET["album_status"] = "active"

        extra_context = extra_context or {}

        extra_context["total_albums"] = SchoolTour.objects.count()

        extra_context["published_albums"] = SchoolTour.objects.filter(
            is_published=True,
            is_deleted=False
        ).count()

        extra_context["draft_albums"] = SchoolTour.objects.filter(
            is_published=False,
            is_deleted=False
        ).count()

        extra_context["Deleted_ablums"] = SchoolTour.objects.filter(
             is_deleted=True
        ).count()

        extra_context["media_total"] = SchoolTourMedia.objects.count()

        return super().changelist_view(request, extra_context=extra_context)

    # Performance optimization
    def get_queryset(self, request):

        qs = super().get_queryset(request)

        return qs.prefetch_related(
            "school_tour_media_items"
        ).annotate(
            media_total=Count("school_tour_media_items")
        )

    # Media count column
    def media_count(self, obj):
        return obj.media_total
    
    media_count.admin_order_field = "media_total"
    media_count.short_description = "Media Count"

    def status_badge(self, obj):

        if obj.is_deleted:
            color = "#dc2626"
            label = "Deleted"

        elif obj.is_published:
            color = "#16a34a"
            label = "Published"

        else:
            color = "#f59e0b"
            label = "Draft"

        return format_html(
            '<span style="color:white;background:{};padding:4px 8px;border-radius:6px;">{}</span>',
            color,
            label
        )
    status_badge.short_description = "Status"
    
    

    # Prevent publishing empty album in admin
    def save_model(self, request, obj, form, change):

        if obj.is_deleted:
            raise ValidationError(
            "Deleted albums cannot be modified. They exist for audit purposes only."
            )

        if obj.is_published and not obj.pk:
            raise ValidationError("Save album before publishing.")

        if not change:
            set_created_by(obj, request.user)

        set_updated_by(obj, request.user)

        super().save_model(request, obj, form, change)

    
    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)

        album = form.instance
        if album.is_published and not album.school_tour_media_items.exists():
            raise ValidationError("Cannot publish album without media.")

    actions = ["publish_albums", "unpublish_albums",
               "restore_albums",
                "permanently_delete_albums"
               ]

    def has_change_permission(self, request, obj=None):

        if obj and obj.is_deleted:
            return False

        return super().has_change_permission(request, obj)

    
    def delete_model(self, request, obj):

        set_deleted_by(obj, request.user)
        obj.save()


    # Bulk publish
    def publish_albums(self, request, queryset):
        updated = 0

        for album in queryset:
            if album.school_tour_media_items.exists():
                album.is_published = True
            album.save()
            updated += 1

        self.message_user(request, f"{updated} albums published.")

    def permanently_delete_albums(self, request, queryset):

        deleted = queryset.delete()

        self.message_user(
            request,
            f"{deleted[0]} albums permanently deleted."
        )

    permanently_delete_albums.short_description = "Permanently delete selected albums"

    def delete_queryset(self, request, queryset):

        bulk_delete_with_audit(queryset, request.user)

        self.message_user(request, "Selected albums deleted with audit.")

    delete_queryset.short_description = "Delete selected albums"

    publish_albums.short_description = "Publish selected albums"

    def restore_albums(self, request, queryset):

        queryset.update(
        is_deleted=False,
        deleted_at=None,
        deleted_by=None
        )

        self.message_user(request, "Albums restored successfully.")

    restore_albums.short_description = "Restore deleted albums"

    def get_readonly_fields(self, request, obj=None):

        if obj and obj.is_deleted:
            return [field.name for field in obj._meta.fields]

        return super().get_readonly_fields(request, obj)

    # Bulk unpublish
    def unpublish_albums(self, request, queryset):
        queryset.update(is_published=False)
        self.message_user(request, "Selected albums unpublished.")

    unpublish_albums.short_description = "Unpublish selected albums"



@admin.register(SchoolTourMedia)
class SchoolTourMediaAdmin(BaseValidatedAdmin):
    list_display = ("album", "image", "video", "created_at")
    list_filter = ("album__album_type",)
    search_fields = ("album__title",)



@admin.register(SchoolSong)
class SchoolSongAdmin(BaseValidatedAdmin):
    list_display = ("title", "is_active")
    readonly_fields = ("is_active","preview",)




@admin.register(DirectorMessage)
class DirectorAdmin(BaseValidatedAdmin):
    list_display = ("name", "position", "is_active","preview", "updated_at")
    autocomplete_fields = ("image",)
    readonly_fields = ("updated_at", "preview")

   
