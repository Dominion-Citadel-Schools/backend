from core.utils.user import get_user_full_name


class AuditViewSetMixin:

    def perform_create(self, serializer):
        serializer.save(created_by=get_user_full_name(self.request.user))

    def perform_update(self, serializer):
        serializer.save(updated_by=get_user_full_name(self.request.user))

    def perform_destroy(self, instance):
        instance.deleted_by = get_user_full_name(self.request.user)
        instance.save()
        instance.delete()