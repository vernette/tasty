from rest_framework import status
from rest_framework.response import Response


class ReadOnlyOrAdminMixin:
    def check_permissions(self, request):
        if not request.user.is_staff:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def create(self, request, *args, **kwargs):
        response = self.check_permissions(request)
        if response:
            return response
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        response = self.check_permissions(request)
        if response:
            return response
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        response = self.check_permissions(request)
        if response:
            return response
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        response = self.check_permissions(request)
        if response:
            return response
        return super().destroy(request, *args, **kwargs)