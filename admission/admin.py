from django.contrib import admin
from admission.models.child_model import Admission, Child
from admission.base_admin import BaseValidatedAdmin
from admission.models.admission_form_builder import AdmissionForm, AdmissionFormField
from admission.models.admisssion_document import AdmissionDocument
from django.utils.html import format_html
from django.contrib import admin, messages
from django_json_widget.widgets import JSONEditorWidget
from django.db import models
from admission.child_Inline_formset import ChildInlineFormSet



class ChildInline(admin.TabularInline):
    model = Child
    extra = 0
    formset = ChildInlineFormSet
    
    def get_readonly_fields(self, request, obj=None):
        if obj and obj.status in ["REVIEWED", "ACCEPTED", "REJECTED"]:
            return [field.name for field in self.model._meta.fields]
        return []

    def has_add_permission(self, request, obj):
        if obj and obj.status in ["ACCEPTED", "REJECTED"]:
            return False
        return super().has_add_permission(request, obj)

    def has_change_permission(self, request, obj=None):
        if obj and obj.status in ["ACCEPTED", "REJECTED"]:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj and obj.status in ["ACCEPTED", "REJECTED"]:
            return False
        return super().has_delete_permission(request, obj)
    


class AdmissionDocumentInline(admin.TabularInline):
    model = AdmissionDocument
    extra = 0
    readonly_fields = ("file_link",)

    def file_link(self, obj):
        if obj.file:
            return format_html(
                '<a href="{}" target="_blank">View</a>',
                obj.file.url
            )
        return "-"


@admin.register(Admission)
class AdmissionAdmin(BaseValidatedAdmin):
    change_list_template = "admin/admission_dashboard.html"
    list_display = (
        "parent_name",
        "email",
        "phone",
        "number_of_children",
        "preferred_contact_method",
        "created_at",
    )

    search_fields = (
        "parent_name",
        "email",
        "phone",
    )

    list_filter = (
        "preferred_contact_method",
        "created_at",
    )

    inlines = [ChildInline]
    inlines = [ChildInline, AdmissionDocumentInline]

    ordering = ["-created_at"]

    def get_readonly_fields(self, request, obj=None):
        if not obj:
            return []

        # ACCEPTED or REJECTED → everything readonly
        if obj.status in ["ACCEPTED", "REJECTED"]:
            return [field.name for field in self.model._meta.fields]

        # REVIEWED → all readonly except status
        if obj.status == "REVIEWED":
            return [
                field.name for field in self.model._meta.fields
                if field.name != "status"
            ]

        return []
    

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "status":
            obj_id = request.resolver_match.kwargs.get("object_id")

            if obj_id:
                obj = Admission.objects.get(pk=obj_id)

                if obj.status == "PENDING":
                    kwargs["choices"] = [
                        ("PENDING", "PENDING"),
                        ("REVIEWED", "REVIEWED"),
                    ]

                elif obj.status == "REVIEWED":
                    kwargs["choices"] = [
                        ("ACCEPTED", "ACCEPTED"),
                        ("REJECTED", "REJECTED"),
                    ]

                else:
                    kwargs["choices"] = [(obj.status, obj.status)]

        return super().formfield_for_choice_field(db_field, request, **kwargs)

    def has_change_permission(self, request, obj=None):
        if obj and obj.status in ["ACCEPTED", "REJECTED"]:
            return False
        return super().has_change_permission(request, obj)
    

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        extra_context = extra_context or {}

        obj = None
        if object_id:
            obj = self.get_object(request, object_id)

        if obj and obj.status in ["ACCEPTED", "REJECTED"]:
            extra_context["show_save"] = False
            extra_context["show_save_and_continue"] = False

        return super().changeform_view(request, object_id, form_url, extra_context)
    

    def changelist_view(self, request, extra_context=None):

        extra_context = extra_context or {}

        extra_context["total_admissions"] = Admission.objects.count()

        extra_context["accepted"] = Admission.objects.filter(
        status="ACCEPTED"
        ).count()

        extra_context["rejected"] = Admission.objects.filter(
        status="REJECTED"
        ).count()

        extra_context["pending"] = Admission.objects.filter(
        status="PENDING"
        ).count()

        return super().changelist_view(request, extra_context=extra_context)
    


class AdmissionFormFieldInline(admin.TabularInline):
    model = AdmissionFormField
    extra = 1

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

    class Media:
        js = ("admin/js/admission_form_field.js",)
        css = {
            "all": ("admin/css/admission_form_field.css",)
        }

@admin.register(AdmissionForm)
class AdmissionFormAdmin(BaseValidatedAdmin):

    list_display = ("name", "is_active", "created_at")

    inlines = [AdmissionFormFieldInline]


@admin.register(AdmissionDocument)
class AdmissionDocumentAdmin(BaseValidatedAdmin):
    list_display = ("admission", "document_type", "file_preview", "uploaded_at")
    fields = ("admission", "document_type", "file", "file_link")

    readonly_fields = ("file_link",)

    def file_link(self, obj):
        if obj.file:
            return format_html(
                '<a href="{}" target="_blank">Preview Document</a>',
                obj.file.url
            )
        return "No file uploaded"

    file_link.short_description = "Preview"

    def file_preview(self, obj):
        if obj.file:
            return format_html(
                '<a href="{}" target="_blank">View</a> | '
                '<a href="{}" download>Download</a>',
                obj.file.url,
                obj.file.url
            )
        return "No file"

    file_preview.short_description = "File"

    def delete_queryset(self, request, queryset):
        locked_docs = queryset.filter(
            admission__status__in=["REVIEWED", "ACCEPTED", "REJECTED"]
        )

        if locked_docs.exists():
            self.message_user(
                request,
                "Some documents cannot be deleted because their admission is locked.",
                level=messages.ERROR
            )

        # Only delete allowed ones
        allowed = queryset.exclude(
            admission__status__in=["REVIEWED", "ACCEPTED", "REJECTED"]
        )

        super().delete_queryset(request, allowed)

    def delete_model(self, request, obj):
        if obj.admission.status in ["REVIEWED", "ACCEPTED", "REJECTED"]:
            self.message_user(
                request,
                "Cannot delete this document because the admission is locked.",
                level=messages.ERROR
            )
            return

        super().delete_model(request, obj)

    def has_add_permission(self, request):
        return True  # keep add allowed globally

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "admission":
            kwargs["queryset"] = Admission.objects.exclude(
                status__in=["ACCEPTED", "REJECTED"]
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    