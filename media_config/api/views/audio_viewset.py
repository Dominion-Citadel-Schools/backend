from media_config.models.audio import Audio
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from media_config.api.serializers.audio_serializer import AudioSerializer
from media_config.api.services.audio_service import AudioService
from core.utils.viewsets import AdminWritePublicReadViewSet


class AudioViewSet(AdminWritePublicReadViewSet):

    queryset = Audio.objects.filter(is_active=True)
    serializer_class = AudioSerializer

    def perform_create(self, serializer):
        serializer.save()
       

    # POST /audios/{id}/deactivate/
    @action(detail=True, methods=["post"])
    def deactivate(self, request, pk=None):
        AudioService.deactivate_audio(pk)
        return Response(
            {"detail": "Audio deactivated successfully"},
            status=status.HTTP_200_OK
        )
    