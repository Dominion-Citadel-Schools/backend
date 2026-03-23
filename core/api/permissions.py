from rest_framework.permissions import BasePermission


class IsAdminOrReadOnly(BasePermission):
    """
    Public:
        - list
        - retrieve

    Staff:
        - create
        - update
        - partial_update
        - destroy
    """

    def has_permission(self, request, view):

        # Allow read-only actions
        if view.action in ["list", "retrieve"]:
            return True

        # Allow only staff users for write actions
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.is_staff
        )


class HasGroupPermission(BasePermission):
    """
    Base class for group-based permission control
    """

    required_groups = []

    def has_permission(self, request, view):

        if not request.user or not request.user.is_authenticated:
            return False

        return request.user.groups.filter(
            name__in=self.required_groups
        ).exists()


class IsMediaManager(HasGroupPermission):
    """
    Only users in MEDIA_MANAGER group
    """

    required_groups = ["MEDIA_MANAGER"]
