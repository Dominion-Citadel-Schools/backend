from datetime import timedelta
from django.contrib import admin
from django.utils import timezone
from django.contrib import messages
from django.utils.html import format_html
from testimonials.testimonial_admin_form import TestimonialAdminForm
from .base_admin import BaseValidatedAdmin
from .models import Testimonial
from django.urls import path
from django.shortcuts import redirect



class TestimonialStatusFilter(admin.SimpleListFilter):
    title = "Testimonials Status"
    parameter_name = "testimonial_status"

    def lookups(self, request, model_admin):
        return (
            ("active", "Active Testimonials"),
            ("deleted", "Trash"),
        )

    def queryset(self, request, queryset):
        if self.value() == "active":
            return queryset.filter(is_deleted=False)

        if self.value() == "deleted":
            return queryset.filter(is_deleted=True)

        return queryset

@admin.register(Testimonial)
class TestimonialAdmin(BaseValidatedAdmin):
    list_display = (
        "full_name", "role", "preview",
        "rating_badge", "status_badge", 
        "moderator_name", "moderated_at",
        "moderation_actions", "spam_badge",
        "active_badge","delete_countdown",
    )
    list_filter = (
        TestimonialStatusFilter,
        "status",
        "rating",
        "moderated_at",
        "moderated_by",
    )

    date_hierarchy = "created_at"
    actions = [
    "approve_selected",
    "reject_selected",
    "soft_delete_selected",
    "restore_selected",
    "hard_delete_selected"
]
    readonly_fields = ("moderated_by", "moderated_at")
    list_per_page = 10
    form = TestimonialAdminForm
    change_list_template = "admin/testimonial_change_list.html"


     # APPROVE
    def approve_selected(self, request, queryset):
        count = 0

        for obj in queryset:

            if obj.status != "PENDING":
                self.message_user(
                    request,
                    f"{obj.full_name} already moderated.",
                    messages.WARNING,
                )
                continue

            obj.status = "APPROVED"
            obj.moderated_by = request.user
            obj.moderated_at = timezone.now()
            obj.save()

            count += 1

        self.message_user(request, f"{count} testimonials approved.")
    approve_selected.short_description = "Approve selected testimonials"

    # REJECT
    def reject_selected(self, request, queryset):
        count = 0

        for obj in queryset:

            if obj.status != "PENDING":
                self.message_user(
                    request,
                    f"{obj.full_name} already moderated.",
                    messages.WARNING,
                )
                continue

            obj.status = "REJECTED"
            obj.moderated_by = request.user
            obj.moderated_at = timezone.now()
            obj.save()

            count += 1

        self.message_user(request, f"{count} testimonials rejected.")
    reject_selected.short_description = "Reject selected testimonials"

    def soft_delete_selected(self, request, queryset):
        count = queryset.update(is_deleted=True, is_active=False, deleted_at=timezone.now())
        self.message_user(request, f"{count} testimonials moved to trash.")

    soft_delete_selected.short_description = "Move selected to trash"

    def restore_selected(self, request, queryset):
        count = queryset.update(is_deleted=False, is_active=True)
        self.message_user(request, f"{count} testimonials restored.")

    restore_selected.short_description = "Restore selected testimonials"

    def hard_delete_selected(self, request, queryset):
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f"{count} testimonials permanently deleted.")

    hard_delete_selected.short_description = "Permanently delete selected"

    def save_model(self, request, obj, form, change):

        if obj.status in ["APPROVED", "REJECTED"] and not obj.moderated_by:
            obj.moderated_by = request.user
            obj.moderated_at = timezone.now()

        super().save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.status in ["APPROVED", "REJECTED"]:
            # Make ALL fields readonly
            return [field.name for field in self.model._meta.fields]
        return super().get_readonly_fields(request, obj)
    

    def status_badge(self, obj):

        colors = {
        "PENDING": "#f0ad4e",
        "APPROVED": "#28a745",
        "REJECTED": "#dc3545",
        }

        return format_html(
        '<span style="padding:4px 10px;border-radius:12px;color:white;background:{};">{}</span>',
        colors[obj.status],
        obj.status,
    )

    status_badge.short_description = "Status"


    def moderation_actions(self, obj):

        if obj.is_deleted:
            return format_html(
                '<a class="button" href="restore/{}/">Restore</a>',
                obj.id
            )

        if obj.status != "PENDING":
            return "-"

        return format_html(
            '<a class="button" href="approve/{}/">Approve</a>&nbsp;'
            '<a class="button" style="background:#dc3545;color:white;" href="reject/{}/">Reject</a>&nbsp;'
            '<a class="button" style="background:#6c757d;color:white;" href="delete/{}/">Trash</a>',
            obj.id,
            obj.id,
            obj.id,
        )

    moderation_actions.short_description = "Actions"

    def delete_countdown(self, obj):
        if not obj.is_deleted or not obj.deleted_at:
            return "-"

        expiry_date = obj.deleted_at + timedelta(days=30)
        remaining = (expiry_date - timezone.now()).total_seconds() / 86400
        remaining = int(remaining)

        if remaining <= 0:
            return format_html(
                '<span style="background:#dc3545;color:white;padding:4px 8px;border-radius:10px;">Expired</span>'
            )

        color = "#f0ad4e" if remaining <= 7 else "#6c757d"

        return format_html(
            '<span style="background:{};color:white;padding:4px 8px;border-radius:10px;">Deletes in {} days</span>',
            color,
            remaining
        )

    delete_countdown.short_description = "Auto Delete"

    def get_urls(self):
        urls = super().get_urls()

        custom_urls = [
        path(
            "approve/<int:testimonial_id>/",
            self.admin_site.admin_view(self.approve_testimonial),
            ),
        path(
            "reject/<int:testimonial_id>/",
            self.admin_site.admin_view(self.reject_testimonial),
        ),
        path(
            "delete/<int:testimonial_id>/",
            self.admin_site.admin_view(self.soft_delete_single),
        ),
        path(
            "restore/<int:testimonial_id>/",
            self.admin_site.admin_view(self.restore_single),
        ),
    ]

        return custom_urls + urls
    
    def soft_delete_single(self, request, testimonial_id):
        obj = Testimonial.objects.get(pk=testimonial_id)
        obj.is_deleted = True
        obj.is_active = False
        obj.deleted_at = timezone.now()
        obj.save()
        return redirect(request.META.get("HTTP_REFERER"))


    def restore_single(self, request, testimonial_id):
        obj = Testimonial.objects.get(pk=testimonial_id)
        obj.is_active = True
        obj.is_deleted = False
        obj.save()
        return redirect(request.META.get("HTTP_REFERER"))
    
    def approve_testimonial(self, request, testimonial_id):

        obj = Testimonial.objects.get(pk=testimonial_id)

        if obj.status != "PENDING":
            self.message_user(request, "Already moderated")
            return redirect(request.META.get("HTTP_REFERER"))

        obj.status = "APPROVED"
        obj.moderated_by = request.user
        obj.moderated_at = timezone.now()
        obj.save()

        return redirect(request.META.get("HTTP_REFERER"))

    def delete_model(self, request, obj):
        obj.is_deleted = True
        obj.is_active = False
        obj.save()

    def delete_queryset(self, request, queryset):
        queryset.update(is_active=False, is_deleted=True)

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Default: hide deleted
        if not request.GET.get("testimonial_status"):
            return qs.filter(is_deleted=False)

        return qs
    
    def has_change_permission(self, request, obj=None):
        if obj and obj.is_deleted:
            return False
        return super().has_change_permission(request, obj)
    
    def reject_testimonial(self, request, testimonial_id):

        obj = Testimonial.objects.get(pk=testimonial_id)

        if obj.status != "PENDING":
            self.message_user(request, "Already moderated")
            return redirect(request.META.get("HTTP_REFERER"))

        obj.status = "REJECTED"
        obj.moderated_by = request.user
        obj.moderated_at = timezone.now()
        obj.save()

        return redirect(request.META.get("HTTP_REFERER"))
    
    def changelist_view(self, request, extra_context=None):

        extra_context = extra_context or {}

        extra_context["pending_count"] = Testimonial.objects.filter(status="PENDING").count()
        extra_context["approved_count"] = Testimonial.objects.filter(status="APPROVED").count()
        extra_context["rejected_count"] = Testimonial.objects.filter(status="REJECTED").count()

        return super().changelist_view(request, extra_context=extra_context)
    

    def rating_badge(self, obj):

        colors = {
        1: "#dc3545",   # red
        2: "#fd7e14",   # orange
        3: "#ffc107",   # yellow
        4: "#28a745",   # green
        5: "#007bff",   # blue
        }

        stars = "★" * obj.rating

        return format_html(
        '<span style="padding:4px 10px;border-radius:12px;color:white;background:{};">{}</span>',
        colors.get(obj.rating, "#6c757d"),
        stars
        )

    rating_badge.short_description = "Rating"

    def active_badge(self, obj):
        if obj.is_deleted:
            color = "#6c757d"
            label = "TRASH"
        elif obj.is_active:
            color = "#28a745"
            label = "ACTIVE"
        else:
            color = "#ffc107"
            label = "INACTIVE"

        return format_html(
            '<span style="background:{};color:white;padding:4px 8px;border-radius:10px;">{}</span>',
            color,
            label
    )
    active_badge.short_description = "State"

    def spam_badge(self, obj):

        if obj.is_spam is None:
            return format_html(
            '<span style="background:#6c757d;color:white;padding:4px 8px;border-radius:10px;">UNKNOWN</span>'
            )

        color = "#dc3545" if obj.is_spam else "#28a745"
        label = "SPAM" if obj.is_spam else "CLEAN"

        return format_html(
        '<span style="background:{};color:white;padding:4px 8px;border-radius:10px;">{}</span>',
        color,
        label
        )
    spam_badge.short_description = "Spam Status"