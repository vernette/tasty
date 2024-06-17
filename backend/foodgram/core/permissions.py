from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.exceptions import MethodNotAllowed


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


class ReadOnlyOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE'] and not request.user.is_staff:
            raise MethodNotAllowed(request.method)
        return True

    def has_object_permission(self, request, view, obj):
        return True
