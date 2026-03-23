from models.mission import Mission
from serializers.mission_serializer import MissionSerializer
from services.mission_service import MissionService
from core.utils.base_aboutsection_viewset import BaseAboutSectionViewSet


class MissionViewSet(BaseAboutSectionViewSet):
    queryset = Mission.objects.select_related("core_values").filter(is_active=True)
    serializer_class = MissionSerializer


    def perform_create(self, serializer):
        instance = serializer.save()
        MissionService.activate(instance)

    def perform_update(self, serializer):
        instance = serializer.save()
        MissionService.activate(instance)
