from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from users.models import UserAvatar
from users.serializers import UserAvatarSerializer


class AvatarView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserAvatarSerializer

    def get_object(self):
        return UserAvatar.objects.get_or_create(user=self.request.user)[0]

    def patch(self, request, *args, **kwargs):
        profile_image = self.get_object()
        serializer = self.get_serializer(
            profile_image,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        user_avatar = self.get_object()
        user_avatar.avatar.delete(save=False)
        user_avatar.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
