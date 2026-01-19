from rest_framework.permissions import BasePermission


class IsAdminOrEmployer(BasePermission):
    """
    Admin (is_superuser) OR Employer (is_staff)
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and (request.user.is_superuser or request.user.is_staff)
        )
