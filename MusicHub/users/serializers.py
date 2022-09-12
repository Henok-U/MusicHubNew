from dataclasses import field
from rest_framework import serializers

from .models import User
from ..main.utlis import trim_spaces_from_data


class CreateUserSerializer(serializers.ModelSerializer):
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
