from abc import ABC, abstractmethod

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from apps.users.models import UserModel as User
from .permissions import IsSuperUser
from .serializers import UserSerializer
UserModel: User = get_user_model()


class UserListAPIView(ListAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser, )


class UserCreateView(CreateAPIView):
    serializer_class = UserSerializer
    #  створювати юзерів може лише super_user
    permission_classes = (IsSuperUser,)


class AdminTools(GenericAPIView, ABC):
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        # всі залогінені користувачі крім мене
        return UserModel.objects.exclude(pk=self.request.user.id)

    @abstractmethod
    def patch(self, *args, **kwargs):
        pass


class SuperUserTools(AdminTools, ABC):
    permission_classes = (IsSuperUser,)


class UserActivateView(AdminTools):
    def patch(self, *args, **kwargs):
        user: User = self.get_object()

        if not user.is_active:
            user.is_active = True
            user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class UserDeactivateView(AdminTools):
    def patch(self, *args, **kwargs):
        user: User = self.get_object()

        if user.is_active:
            user.is_active = False
            user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class UserToAdminView(SuperUserTools):
    def patch(self, *args, **kwargs):
        user: User = self.get_object()

        if not user.is_staff:
            user.is_staff = True
            user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class AdminToUserView(SuperUserTools):
    def patch(self, *args, **kwargs):
        user: User = self.get_object()

        if user.is_staff:
            user.is_staff = False
            user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)