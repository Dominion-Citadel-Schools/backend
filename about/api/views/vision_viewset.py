from requests import Response
from models.vision import Vision
from serializers.vision_serializer import VisionSerializer
from services.vision_service import VisionService
from core.utils.base_aboutsection_viewset import BaseAboutSectionViewSet


class VisionViewSet(BaseAboutSectionViewSet):
    queryset = Vision.objects.filter(is_active=True)
    serializer_class = VisionSerializer

    def list(self, request, *args, **kwargs):
        ''' Returns active school vision data '''
        data =VisionService.get_queryset()
        return Response(data)

    def perform_create(self, serializer):
        instance = serializer.save()
        VisionService.activate(instance)

    def perform_update(self, serializer):
        instance = serializer.save()
        VisionService.activate(instance)
