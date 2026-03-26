from django.contrib import admin
from admission.models.child_model import Admission, Child
from admission.base_admin import BaseValidatedAdmin
from admission.models.admission_form_builder import AdmissionForm, AdmissionFormField
from admission.models.admisssion_document import AdmissionDocument
from django.utils.html import format_html
from django.contrib import admin, messages
from django_json_widget.widgets import JSONEditorWidget
from django.db import models
from django.urls import reverse
from admission.admission_admin_form import AdmissionAdminForm



@admin.register(Child)
class ChildAdmin(BaseValidatedAdmin):
    list_display = (
        "full_name",
        "admission",
        "age",
        "gender",
        "class_seeking_admission",
    )

    list_filter = ("gender", "admission__status")
    search_fields = ("full_name", "admission__parent_name")
    list_per_page = 10

    def has_delete_permission(self, request, obj=None):
        if obj and obj.admission.status in ["REVIEWED", "ACCEPTED", "REJECTED"]:
            return False
        return super().has_delete_permission(request, obj)

    def get_changeform_initial_data(self, request):
        return {
            "admission": request.GET.get("admission")
        }

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("admission")

    # 🚫 Prevent single delete
    def delete_model(self, request, obj):
        if obj.admission.status in ["REVIEWED", "ACCEPTED", "REJECTED"]:
            self.message_user(
                request,
                "Cannot delete this child because the admission is locked.",
                level=messages.ERROR
            )
            return
        super().delete_model(request, obj)

    # 🚫 Prevent bulk delete
    def delete_queryset(self, request, queryset):
        locked = queryset.filter(
            admission__status__in=["REVIEWED", "ACCEPTED", "REJECTED"]
        )

        if locked.exists():
            self.message_user(
                request,
                "Some children cannot be deleted because their admission is locked.",
                level=messages.ERROR
            )

        allowed = queryset.exclude(
            admission__status__in=["REVIEWED", "ACCEPTED", "REJECTED"]
        )

        super().delete_queryset(request, allowed)

@admin.register(Admission)
class AdmissionAdmin(BaseValidatedAdmin):
    change_list_template = "admin/admission_dashboard.html"
    form = AdmissionAdminForm 
    list_display = (
    "parent_name",
    "email",
    "phone",
    "number_of_children",
    "children_count",
    "view_children",
    "documents_count",
    "view_documents",
    "add_child",
    "add_document",
    "preferred_contact_method",
    "action_by",  
    "created_at",
    "status_badge",

    )

    readonly_fields = (
    "reviewed_by",
    "accepted_by",
    "rejected_by",
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


    ordering = ["-created_at"]

    list_per_page = 10


    def view_documents(self, obj):
        url = (
            reverse("admin:admission_admissiondocument_changelist")
            + f"?admission__id__exact={obj.id}"
        )
        return format_html('<a class="button" href="{}">View Documents</a>', url)

    view_documents.short_description = "Documents"

    def action_by(self, obj):
        if obj.status == "REVIEWED" and obj.reviewed_by:
            return format_html(
                '<span style="color:white;background:#3b82f6;padding:4px 8px;border-radius:6px;">Reviewed by {}</span>',
                obj.reviewed_by.get_full_name() or obj.reviewed_by.username
            )

        if obj.status == "ACCEPTED" and obj.accepted_by:
            return format_html(
                '<span style="color:white;background:#16a34a;padding:4px 8px;border-radius:6px;">Accepted by {}</span>',
                obj.accepted_by.get_full_name() or obj.accepted_by.username
            )

        if obj.status == "REJECTED" and obj.rejected_by:
            return format_html(
                '<span style="color:white;background:#dc2626;padding:4px 8px;border-radius:6px;">Rejected by {}</span>',
                obj.rejected_by.get_full_name() or obj.rejected_by.username
            )

        return "-"
    action_by.short_description = "Action By"


    def add_child(self, obj):
        url = (
            reverse("admin:admission_child_add")
            + f"?admission={obj.id}"
        )
        return format_html('<a class="button" href="{}">Add Child</a>', url)

    add_child.short_description = "Add Child"

    def add_document(self, obj):
        url = (
            reverse("admin:admission_admissiondocument_add")
            + f"?admission={obj.id}"
        )
        return format_html('<a class="button" href="{}">Add Document</a>', url)

    add_document.short_description = "Add Document"
    
    def children_count(self, obj):
        return obj.children.count()

    def documents_count(self, obj):
        return obj.documents.count()

    children_count.short_description = "Children"
    documents_count.short_description = "Documents"

    def view_children(self, obj):
        url = (
            reverse("admin:admission_child_changelist")
            + f"?admission__id__exact={obj.id}"
        )
        return format_html('<a class="button" href="{}">View Children</a>', url)

    view_children.short_description = "Children"

    def get_readonly_fields(self, request, obj=None):
        base_readonly = ["reviewed_by", "accepted_by", "rejected_by"]

        if not obj:
            return base_readonly

        # ACCEPTED or REJECTED → everything readonly
        if obj.status in ["ACCEPTED", "REJECTED"]:
            return [field.name for field in self.model._meta.fields]

        # REVIEWED → all readonly except status
        if obj.status == "REVIEWED":
            return [
            field.name for field in self.model._meta.fields
            if field.name != "status"
            ]

        # PENDING → only audit fields readonly
        return base_readonly
    

    def save_model(self, request, obj, form, change):
        if change:
            old_obj = Admission.objects.get(pk=obj.pk)

            # REVIEWED
            if obj.status == "REVIEWED" and old_obj.status != "REVIEWED":
                obj.reviewed_by = request.user

            # ACCEPTED
            if obj.status == "ACCEPTED" and old_obj.status != "ACCEPTED":
                obj.accepted_by = request.user

            # REJECTED
            if obj.status == "REJECTED" and old_obj.status != "REJECTED":
             obj.rejected_by = request.user

        super().save_model(request, obj, form, change)


    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "status":
            obj_id = request.resolver_match.kwargs.get("object_id")

            if not obj_id:
                # 🚫 NEW OBJECT → only allow PENDING
                kwargs["choices"] = [("PENDING", "PENDING")]
            else:
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

    def status_badge(self, obj):
        colors = {
            "PENDING": "#f59e0b",
            "REVIEWED": "#3b82f6",
            "ACCEPTED": "#16a34a",
            "REJECTED": "#dc2626",
        }
        return format_html(
            '<span style="color:white;background:{};padding:4px 8px;border-radius:6px;">{}</span>',
            colors[obj.status],
            obj.status
        )
    status_badge.short_description = "Status"

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

    fields = ("label", "field_type", "required", "options")

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
    list_filter = ("document_type", "admission__status")
    list_per_page = 10

    readonly_fields = ("file_link",)

    def get_changeform_initial_data(self, request):
        return {
            "admission": request.GET.get("admission")
    }

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

    def has_delete_permission(self, request, obj=None):
        if obj and obj.admission.status in ["REVIEWED", "ACCEPTED", "REJECTED"]:
            return False
        return super().has_delete_permission(request, obj)

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

    