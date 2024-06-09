from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Разрешены GET, HEAD, OPTIONS запросы для всех
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user
