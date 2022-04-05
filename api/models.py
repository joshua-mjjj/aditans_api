import binascii
import os

from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Avg
from model_utils.models import TimeStampedModel
from rest_framework_jwt.settings import api_settings

GENDER_CHOICES = (("male", "Male"), ("female", "Female"))

CLASSES_CHOICES = (
    ("primary_one", "Primary one"), 
    ("primary_two", "Primary two"),
    ("primary_three", "Primary three"),
    ("primary_four", "Primary four"),
    ("primary_five", "Primary five"),
    ("primary_six", "Primary six"),
    ("primary_seven", "Primary seven"),
    ("secondary", "High school"),
)

class UserManager(BaseUserManager):
    def _create_user(self, username, password, is_staff, is_superuser, **extra_fields):
        if not username:
            raise ValueError("The given username must be set")
        # email = self.normalize_email(email)
        is_active = extra_fields.pop("is_active", True)
        user = self.model(
            username=username,
            is_staff=is_staff,
            is_active=is_active,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        is_staff = extra_fields.pop("is_staff", False)
        return self._create_user(username, password, is_staff, False, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        return self._create_user(username, password, True, True, **extra_fields)


class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True) # db_index=True
    email = models.EmailField(
        "email address", max_length=255, unique=False, blank=True, null=True
    )
    first_name = models.CharField(max_length=32, blank=True, null=True)
    last_name = models.CharField(max_length=32, blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True) # null=True
    
    is_staff = models.BooleanField("staff status", default=False)
    is_active = models.BooleanField("active", default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "username" # Making username the required field
    REQUIRED_FIELDS = []

    # Students Sponsored by a given sponsor
    @property
    def profiles(self):
        return Profile.objects.filter(owner=self)

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(self)
        token = jwt_encode_handler(payload)

        return token

def generate_password_reset_code():
    return binascii.hexlify(os.urandom(20)).decode("utf-8")


class ProjectType(TimeStampedModel):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


def upload_path(instance, filname):
    return '/'.join(['profile_pictures', str(instance.owner), filname])


class Profile(TimeStampedModel):
    project_type = models.ForeignKey(
        ProjectType, on_delete=models.CASCADE, blank=True, null=True
    )
    id_name = models.CharField(max_length=30)
    profile_image = models.ImageField(blank=True, null=True, upload_to=upload_path)
    investment_plan = models.IntegerField()
    latitude = models.FloatField(max_length=9)
    longitude = models.FloatField(max_length=9)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.id_name























