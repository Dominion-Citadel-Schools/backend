from media_config.api.serializers.image_serializer import ImageSerializer
from media_config.models.image import Image
from core.utils.viewsets import AdminWritePublicReadViewSet



class MediaViewSet(AdminWritePublicReadViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

