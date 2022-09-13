from dataclasses import field
from enum import unique
from rest_framework import serializers

from .models import User
from ..main.utils import trim_spaces_from_data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
        ]
        extra_kwargs = {"password": {"write_only": True}, "id": {"read_only": True}}

    def create(self, validated_data):
        return User.objects.create_user(**trim_spaces_from_data(validated_data))


class CreateUserSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=256, allow_blank=False)
    first_name = serializers.CharField(max_length=30, allow_blank=False)
    last_name = serializers.CharField(max_length=30, allow_blank=False)
    password = serializers.CharField(min_length=8, max_length=64, allow_blank=False)
    confirm_password = serializers.CharField(
        min_length=8, max_length=64, allow_blank=False
    )
