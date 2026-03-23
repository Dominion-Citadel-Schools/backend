from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAdminUser


class AdminWritePublicReadViewSet(ModelViewSet):
    """
    Base ViewSet:
    - Read operations → public
    - Write operations → admin only
    """

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAdminUser()]
        return [AllowAny()]
