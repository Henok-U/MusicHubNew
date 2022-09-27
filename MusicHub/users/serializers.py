from django.core.validators import EmailValidator
from rest_framework import serializers

from ..main.utils import get_random_string, trim_spaces_from_data
from .models import User
from .profile_service import validate_old_password, validate_passwords_match


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

    def validate(self, attrs):
        validate_passwords_match(attrs)
        return attrs

    class Meta:
        model = User
        fields = ["password", "confirm_password"]
        extra_kwargs = {
            "password": {"write_only": True},
            "confirm_password": {"write_only": True},
        }


class ChangePasswordSerializer(serializers.ModelSerializer):

    old_password = serializers.CharField(
        max_length=100,
    )
    confirm_password = serializers.CharField(
        max_length=100,
    )

    class Meta:
        model = User
        fields = ["password", "confirm_password", "old_password"]

    def validate(self, attrs):
        validate_passwords_match(attrs)
        validate_old_password(attrs, self.context["user"])

        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data["password"])
        instance.save()
        return instance


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


class AddChangePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["profile_avatar"]

    def validate(self, attrs):
        picture = attrs["profile_avatar"]
        # TODO Change this
        # picture.size is in bytes
        if picture.size > 3000000:
            raise serializers.ValidationError(
                "Picture size can not be greater than 3Mb"
            )
        return attrs

    def save(self, **kwargs):
        name = self.initial_data["profile_avatar"].name
        random = get_random_string(10)
        self.initial_data["profile_avatar"].name = f"{random}.{name.split('.')[-1]}"
        return super().save(**kwargs)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name"]
        extra_kwargs = {"email": {"read_only": True}}
