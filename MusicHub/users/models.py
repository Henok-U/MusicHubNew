from uuid import uuid4
from django.db import models
from django.core.validators import (
    RegexValidator,
    EmailValidator,
    validate_image_file_extension,
)
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class CustomManager(BaseUserManager):
    def create_user(self, email, password, first_name, last_name, **kwargs):
        user = self.model(
            email=email, first_name=first_name, last_name=last_name, **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, first_name, last_name, **kwargs):
        user = self.model(
            email=email, first_name=first_name, last_name=last_name, **kwargs
        )
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom Abstract User Model"""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)

    first_name = models.CharField(max_length=25, blank=False, null=False)
    last_name = models.CharField(max_length=25, blank=False, null=False)
    email = models.EmailField(
        verbose_name="email address",
        unique=True,
        validators=[EmailValidator(code="Invalid email")],
    )  # required
    password = models.CharField(
        max_length=100,
        validators=[
            RegexValidator(regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*\\W).{8,}$")
        ],
    )
    profile_avatar = models.ImageField(
        "Avatar",
        upload_to="users/avatar",
        blank=True,
        null=True,
        validators=[validate_image_file_extension],
    )
    followers = models.ManyToManyField("users.User", blank=True, symmetrical=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = CustomManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "password"]

    def __str__(self):
        return self.email
