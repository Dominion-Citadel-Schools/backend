from django_json_widget.widgets import JSONEditorWidget
from django.contrib import admin
from django.db import models
from .base_admin import BaseValidatedAdmin
from academics.models.co_curriculum import Activity, ActivityCategory
from academics.models.acadmic_year import AcademicYear, CalendarEvent
from .models.campuse import Campuse
from .models.program import Program, ProgramCampus


@admin.register(Campuse)
class CampuseAdmin(BaseValidatedAdmin):
    list_display = ("name", "location", "year_established", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "location")

    formfield_overrides = {
        models.JSONField: {
            "widget": JSONEditorWidget(
                options={
                    "mode": "tree",
                    "modes": ["tree", "code"],
                }
            )
        }
    }

class ProgramCampusInline(admin.TabularInline):
    model = ProgramCampus
    extra = 1
    ordering = ["order"]


@admin.register(Program)
class ProgramAdmin(BaseValidatedAdmin):
    list_display = (
        "title",
        "category",
        "enrollment_capacity",
        "full_day",
        "is_active",
    )

    list_filter = ("category", "is_active", "full_day")
    search_fields = ("title",)

    inlines = [ProgramCampusInline]


@admin.register(ProgramCampus)
class ProgramCampusAdmin(BaseValidatedAdmin):
    list_display = ("program", "campus_name", "order")
    list_filter = ("program",)
    search_fields = ("campus_name",)

    formfield_overrides = {
        models.JSONField: {
            "widget": JSONEditorWidget(
                options={
                    "mode": "tree",
                    "modes": ["tree", "code"],
                }
            )
        }
    }


@admin.register(ActivityCategory)
class ActivityCategoryAdmin(BaseValidatedAdmin):

    list_display = ("name", "order", "is_active", "created_at")
    search_fields = ("name",)
    list_filter = ("is_active",)
    ordering = ("order",)
    prepopulated_fields = {}


@admin.register(Activity)
class ActivityAdmin(BaseValidatedAdmin):

    list_display = (
        "name",
        "category",
        "status",
        "order",
        "created_at"
    )

    list_filter = ("status", "category")
    search_fields = ("name",)
    autocomplete_fields = ("category",)
    ordering = ("order",)




class CalendarEventInline(admin.TabularInline):

    model = CalendarEvent
    extra = 1


@admin.register(AcademicYear)
class AcademicYearAdmin(BaseValidatedAdmin):

    list_display = (
        "name",
        "start_date",
        "end_date",
        "is_active"
    )

    inlines = [CalendarEventInline]

    search_fields = ("name",)

    list_filter = ("is_active",)

    ordering = ("-start_date",)


@admin.register(CalendarEvent)
class CalendarEventAdmin(BaseValidatedAdmin):

    list_display = (
        "title",
        "date",
        "event_type",
        "academic_year"
    )

    list_filter = (
        "event_type",
        "academic_year"
    )

    search_fields = ("title",)

    ordering = ("date",)