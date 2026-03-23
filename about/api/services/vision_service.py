from django.db import transaction
from about.models.vision import Vision
from services.cache import clear_about_cache
from about.utils.base_sections_service import BaseSectionService
from about.serializers.vision_serializer import VisionSerializer


class VisionService(BaseSectionService):

    model = Vision
    serializer_class = VisionSerializer
    cache_key = "about:vision:active"


    @staticmethod
    @transaction.atomic
    def activate(instance):
        if instance.is_active:
            Vision.objects.filter(is_active=True)\
                .exclude(pk=instance.pk)\
                .update(is_active=False)

        instance.save()
        clear_about_cache()
        return instance
