from dataclasses import fields
from django.core.validators import EmailValidator
from rest_framework import serializers

from ..main.utils import trim_spaces_from_data
from .models import User


class SignupSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(
        min_length=8, max_length=64, allow_blank=False
    )

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "password",
            "confirm_password",
            "first_name",
            "last_name",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "confirm_password": {"write_only": True},
            "id": {"read_only": True},
        }

    def validate(self, attrs):
        if not attrs["password"] == attrs["confirm_password"]:
            raise serializers.ValidationError("Passwords does not match")
        return attrs

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "email": instance.email,
            "first_name": instance.first_name,
            "last_name": instance.last_name,
        }

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        return User.objects.create_user(**trim_spaces_from_data(validated_data))


class SigninSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=256, allow_blank=False)
    password = serializers.CharField(min_length=8, max_length=64, allow_blank=False)


class ResetPasswordSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(
        max_length=100,
    )

    def validate(self, attrs):
        if not attrs["password"] == attrs["confirm_password"]:
            raise serializers.ValidationError("Passwords does not match")
        return attrs

    class Meta:
        model = User
        fields = ["password", "confirm_password"]
        extra_kwargs = {
            "password": {"write_only": True},
            "confirm_password": {"write_only": True},
        }


class ResetPasswordEmailSerializer(serializers.Serializer):

    email = serializers.CharField(
        max_length=256,
        validators=[
            EmailValidator(
                code="Invalid email", message="Please provide valid email address"
            )
        ],
    )


class SocialAuthSerializer(serializers.Serializer):
    access_token = serializers.CharField(max_length=250, allow_blank=False)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name"]
        extra_kwargs = {"email": {"read_only": True}}
