from rest_framework.permissions import BasePermission, IsAuthenticated, AllowAny


class IsAdminAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return True
        return False
