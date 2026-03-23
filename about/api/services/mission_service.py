from django.db import transaction
from about.models.mission import Mission
from about.serializers.mission_serializer import MissionSerializer
from about.utils.base_sections_service import BaseSectionService


class MissionService(BaseSectionService):

    model = Mission
    serializer_class = MissionSerializer
    cache_key = "about:mission:active"
    prefetch_related_fields = ("core_values",)


    @classmethod
    def get_queryset(cls):
        return (
            cls.model.objects
            .filter(is_active=True)
            .select_related("core_values")
        )


    @staticmethod
    @transaction.atomic
    def activate(instance):
        if instance.is_active:
            Mission.objects.filter(is_active=True)\
                .exclude(pk=instance.pk)\
                .update(is_active=False)

        instance.save()
        BaseSectionService.clear_cache()
        return instance
