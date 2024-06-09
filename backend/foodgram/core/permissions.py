from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Разрешены GET, HEAD, OPTIONS запросы для всех
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user


class IsOwnerOrAdminOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user or request.user.is_staff


class IsAuthenticatedAndReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user and request.user.is_authenticated
        return True
