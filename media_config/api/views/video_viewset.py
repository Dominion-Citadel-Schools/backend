from media_config.models.video import Video
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from media_config.api.serializers.video_serializer import VideoSerializer
from media_config.api.services.video_service import VideoService
from core.utils.viewsets import AdminWritePublicReadViewSet


class VideoViewSet(AdminWritePublicReadViewSet):

    queryset = Video.objects.filter(is_active=True)
    serializer_class = VideoSerializer

    def perform_create(self, serializer):
        serializer.save()

    # POST /videos/{id}/deactivate/
    @action(detail=True, methods=["post"])
    def deactivate(self, request, pk=None):
      VideoService.deactivate_video(pk)
      return Response({"detail": "Video deactivated successfully", "status": status.HTTP_200_OK})
