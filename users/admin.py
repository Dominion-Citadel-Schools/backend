from django.contrib.auth.admin import UserAdmin
from django.db.models import Count

class CustomUserAdmin(UserAdmin):

    list_display = ("username", "email", "moderated_count")

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        return qs.annotate(
            moderated_count=Count("moderated_testimonials")
        )

    def moderated_count(self, obj):
        return obj.moderated_count