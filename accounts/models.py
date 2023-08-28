from django.db import models
from django.conf import settings
from django.contrib.auth.hashers import is_password_usable
from django.contrib.auth.hashers import check_password, make_password

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password, **extra_fields):
        """
        Creates and saves a User with the given phone_number, password, and any extra fields.
        """

        if not phone_number:
            raise ValueError("Phone number is required")

        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        """
        Creates and saves a superuser with the given phone_number, password, and any extra fields.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_verified", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if extra_fields.get("is_active") is not True:
            raise ValueError("Superuser must have is_active=True.")
        if extra_fields.get("is_verified") is not True:
            raise ValueError("Superuser must have is_verified=True.")

        return self.create_user(phone_number, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=14, unique=True)
    email_address = models.EmailField(max_length=254, blank=True, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "phone_number"

    objects = CustomUserManager()

    def __str__(self):
        return self.phone_number

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"


# class UserProfile(models.Model):
#     user = models.OneToOneField(
#         CustomUser, on_delete=models.CASCADE, related_name="profile"
#     )
#     profile_picture = models.ImageField(
#         upload_to="profile_images/", default="avatar.png"
#     )

#     def __str__(self):
#         return self.user.first_name + " " + f"profile"
