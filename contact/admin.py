from django.contrib import admin
from contact.models import ContactMessage
from .base_admin import BaseValidatedAdmin
from django.utils import timezone
from django.utils.html import format_html



@admin.register(ContactMessage)
class ContactAdmin(BaseValidatedAdmin):

    change_list_template = "admin/contact_dashboard.html"
    
    list_display = (
        "full_name",
        "email",
        "subject",
        "status_badge",
        "resolved_name",
        "created_at",
    )

    list_filter = (
        "subject",
        "is_resolved",
        "created_at",
    )

    actions = ["mark_as_resolved"]

    list_per_page = 10

    readonly_fields = (
        "created_at",
        "resolved_by",
        "resolved_at",
    )


    


    def get_readonly_fields(self, request, obj=None):

        readonly = list(self.readonly_fields)

        if obj and obj.is_resolved:
            readonly.extend([
            "full_name",
            "email",
            "phone_number",
            "subject",
            "campus",
            "message"
        ])

        return readonly


    def save_model(self, request, obj, form, change):

        if change:

            old = self.model.objects.get(pk=obj.pk)

            if not old.is_resolved and obj.is_resolved:

                obj.resolved_by = request.user
                obj.resolved_at = timezone.now()

            if old.is_resolved:
                obj.is_resolved = True

        super().save_model(request, obj, form, change)



    def mark_as_resolved(self, request, queryset):

        unresolved = queryset.filter(is_resolved=False)

        updated = unresolved.update(
            is_resolved=True,
            resolved_by=request.user,
            resolved_at=timezone.now()
        )

        self.message_user(
            request,
            f"{updated} messages successfully marked as resolved."
        )

    mark_as_resolved.short_description = "Mark selected as resolved"



    def status_badge(self, obj):

        color = "#16a34a" if obj.is_resolved else "#dc2626"
        label = "Resolved" if obj.is_resolved else "Unresolved"

        return format_html(
            '<span style="color:white;background:{};padding:4px 10px;border-radius:6px;">{}</span>',
            color,
            label
        )

    status_badge.short_description = "Status"

    

    def changelist_view(self, request, extra_context=None):

        total_messages = ContactMessage.objects.count()

        resolved_messages = ContactMessage.objects.filter(
            is_resolved=True
        ).count()

        unresolved_messages = ContactMessage.objects.filter(
            is_resolved=False
        ).count()

        context = {
            "total_messages": total_messages,
            "resolved_messages": resolved_messages,
            "unresolved_messages": unresolved_messages,
        }

        extra_context = extra_context or {}
        extra_context.update(context)

        return super().changelist_view(request, extra_context=extra_context)

    