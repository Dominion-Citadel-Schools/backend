from rest_framework.response import Response
from serializers.history_serializers import HistorySectionSerializer
from services.history_service  import HistoryService
from core.utils.base_aboutsection_viewset import BaseAboutSectionViewSet
from about.models.history import HistorySection




class HistorySectionViewSet(BaseAboutSectionViewSet):
    serializer_class = HistorySectionSerializer
    queryset = HistorySection.objects.select_related("image")
    

    def list(self, request, *args, **kwargs):
        """
        Returns fullHistory page data (sections + achievements)
        """
        data =HistoryService.get_queryset()
        return Response(data)


    def perform_create(self, serializer):
        instance = serializer.save()
        HistoryService.activate_section(instance)

    def perform_update(self, serializer):
        instance = serializer.save()
        HistoryService.activate_section(instance)

    def perform_create(self, serializer):
        instance = serializer.save()
        HistoryService.activate_achievement(instance)

    def perform_update(self, serializer):
        instance = serializer.save()
        HistoryService.activate_achievement(instance)
    