from rest_framework import serializers

from ..main.utils import get_random_string, trim_spaces_from_data
from .models import User
from .validators import (
    validate_old_password,
    validate_passwords_match,
    validate_picture,
)


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
        validate_passwords_match(attrs)
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

    class Meta:
        model = User
        fields = ["password", "confirm_password"]

    def validate(self, attrs):
        validate_passwords_match(attrs)
        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data.get("password"))
        instance.save()
        return instance

    def to_representation(self, instance):
        return {"message": "password changed successfully"}


class ChangePasswordSerializer(ResetPasswordSerializer):

    old_password = serializers.CharField(
        max_length=100,
    )

    class Meta:
        model = User
        fields = ["password", "confirm_password", "old_password"]

    def validate(self, attrs):
        validate_passwords_match(attrs)
        validate_old_password(attrs, self.context["user"])

        return attrs


class ResetPasswordEmailSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ["email"]


class SocialAuthSerializer(serializers.Serializer):
    access_token = serializers.CharField(max_length=250, allow_blank=False)


class AddChangePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["profile_avatar"]

    def validate(self, attrs):
        validate_picture(attrs.get("profile_avatar"))
        return attrs

    def save(self, **kwargs):
        name = self.initial_data.get("profile_avatar").name
        random = get_random_string(10)
        self.initial_data["profile_avatar"].name = f"{random}.{name.split('.')[-1]}"
        return super().save(**kwargs)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name"]
        extra_kwargs = {"email": {"read_only": True}}
