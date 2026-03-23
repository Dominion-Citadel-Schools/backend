from media_config.models.image import Image
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from media_config.api.serializers.image_serializer import ImageSerializer
from media_config.api.services.image_service import ImageService
from core.utils.viewsets import AdminWritePublicReadViewSet



class ImageViewSet(AdminWritePublicReadViewSet):

    queryset = Image.objects.filter(is_active=True)
    serializer_class = ImageSerializer
    
    #def perform_create(self, serializer):
        #serializer.save()

    def get_queryset(self):
        return super().get_queryset().order_by("-uploaded_at")
    
    # POST /images/{id}/deactivate/
    @action(detail=True, methods=["post"])
    def deactivate(self, request, pk=None):
      ImageService.deactivate_image(pk)
      return Response({"detail": "Image deactivated successfully", "status": status.HTTP_200_OK})

