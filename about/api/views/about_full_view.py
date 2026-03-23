from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from about.api.services.about_full_service import AboutFullService
from about.serializers.about_full_serializer import AboutFullSerializer
from core.throttles import PublicContentThrottle


class AboutFullViewSet(ViewSet):

    permission_classes = [AllowAny]
    throttle_classes = [PublicContentThrottle]

    def list(self, request, *args, **kwargs):
        data = AboutFullService.get_full_aggregation_data()
        serializer = AboutFullSerializer(data)
        return Response(serializer.data)
