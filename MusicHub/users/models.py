from uuid import uuid4

from authemail.models import EmailAbstractUser
from django.contrib.auth.models import BaseUserManager
from django.core.validators import (
    EmailValidator,
    FileExtensionValidator,
    RegexValidator,
)
from django.db import models


class CustomManager(BaseUserManager):
    def create_user(self, email, password, first_name, last_name, **kwargs):
        """
        Creates and saves a User with a given email and password.
        """
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
        user.is_verified = True
        user.save(using=self._db)

        return user

    def get_queryset_verified(self):
        return super(CustomManager, self).get_queryset().filter(is_verified=True)


class User(EmailAbstractUser):
    """
    Custom Abstract User Model that extends EmailAbstractUser
    """

    # custom fields
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)

    first_name = models.CharField(
        max_length=30,
        blank=False,
        null=False,
        validators=[
            RegexValidator(
                regex="^[a-zA-Z][a-zA-Z\-\s]*$",
                message="Name not valid: name must start and ends with letter and can contain only ' ' or '-' special characters ",
            )
        ],
    )
    last_name = models.CharField(
        max_length=30,
        blank=False,
        null=False,
        validators=[
            RegexValidator(
                regex="^[a-zA-Z][a-zA-Z\-\s]*$",
                message="Name not valid: name must start and ends with letter and can contain only ' ' or '-' special characters ",
            )
        ],
    )
    email = models.EmailField(
        verbose_name="email address",
        unique=True,
        max_length=256,
        validators=[
            EmailValidator(
                code="Invalid email", message="Please provide valid email address"
            )
        ],
    )
    password = models.CharField(
        max_length=100,  # this is for hash stored in database
        validators=[
            RegexValidator(
                regex="^.{8,64}$",
                message="Password must be beetween 8-64 characters and can include Upper/lower cases, digits and special characters",
            )
        ],
    )

    profile_avatar = models.ImageField(
        "Avatar",
        upload_to="users/avatar",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"])],
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

    def get_email_short(self):
        """
        Get first part of email example:
        for example@mail.com will return example
        """
        return self.email.split("@")[0]
