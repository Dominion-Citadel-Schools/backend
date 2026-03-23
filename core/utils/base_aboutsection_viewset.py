from core.throttles import PublicContentThrottle
from core.utils.viewsets import AdminWritePublicReadViewSet
from django_filters.rest_framework import DjangoFilterBackend


class BaseAboutSectionViewSet(AdminWritePublicReadViewSet):
    throttle_classes = [PublicContentThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["category"]
