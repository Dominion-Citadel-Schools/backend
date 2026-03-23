from requests import Response
from models.director import DirectorMessage
from serializers.director_serializer import DirectorSerializer
from services.director_service import DirectorService
from core.utils.base_aboutsection_viewset import BaseAboutSectionViewSet



class DirectorViewSet(BaseAboutSectionViewSet):
    queryset = DirectorMessage.objects.select_related("image")
    serializer_class = DirectorSerializer

    def list(self, request, *args, **kwargs):
        ''' Returns active director message data '''
        data =DirectorService.get_queryset()
        return Response(data)



    def perform_create(self, serializer):
        instance = serializer.save()
        DirectorService.activate(instance)

    def perform_update(self, serializer):
        instance = serializer.save()
        DirectorService.activate(instance)
