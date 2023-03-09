from rest_framework.serializers import ModelSerializer
from typing import Type
from django.db import transaction
from django.contrib.auth import get_user_model
from apps.users.models import UserModel as User
from .models import ProfileModel

UserModel: Type[User] = get_user_model()


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = ProfileModel
        fields = ('name', 'surname', 'age', 'phone')


class UserSerializer(ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = UserModel

        fields = (
            'id', 'email', 'password', 'is_staff', 'is_superuser',
            'is_active', 'created_at', 'updated_at', 'last_login', 'profile'
        )
        # прописуємо що Юзер не має права змінювати наступні параметри
        read_only_fields = ('id', 'is_staff', 'is_superuser', 'is_active', 'created_at', 'updated_at', 'last_login')
        # вказуємо що password буде використовуватися в Серіалайзері тільки для запису
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    # переоприділяємо метод create
    @transaction.atomic
    def create(self, validated_data):
        profile = validated_data.pop('profile')
        user = UserModel.objects.create_user(**validated_data)
        ProfileModel.objects.create(**profile, user=user)
        return user


class AvatarSerializer(ModelSerializer):
    class Meta:
        model = ProfileModel
        fields = ('avatar',)