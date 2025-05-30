from rest_framework import permissions

class IsManagerUser(permissions.BasePermission):
    """
    Allows access only to users with user_type='manager'.
    """

    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.user_type == 'manager'
        )
