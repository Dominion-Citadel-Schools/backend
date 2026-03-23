from django.db import transaction
from models.director import DirectorMessage
from about.serializers.director_serializer import DirectorSerializer
from about.utils.base_sections_service import BaseSectionService


class DirectorService(BaseSectionService):
    model = DirectorMessage
    serializer_class = DirectorSerializer
    cache_key = "about:director:active"
    select_related_fields = ("image",)
    

    @staticmethod
    @transaction.atomic
    def activate(instance):
        if instance.is_active:
            DirectorMessage.objects.filter(
                section_type=instance.section_type,
                is_active=True
            ).exclude(pk=instance.pk).update(is_active=False)

        instance.save()
        BaseSectionService.clear_cache()
        return instance
