from __future__ import division

import datetime

from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_jwt.serializers import JSONWebTokenSerializer

from api.models import *

class JWTSerializer(JSONWebTokenSerializer):
    def validate(self, attrs):
        validated_data = super().validate(attrs)
        update_last_login(None, validated_data["user"])
        return validated_data

class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username", "phone_number", "password")


class UserSerializer(serializers.ModelSerializer):
    profiles = serializers.SerializerMethodField()

    def get_profiles(self, obj):
        profiles = Profile.objects.filter(owner=obj)
        return ProfileSeriaizer(profiles, many=True).data

    def to_representation(self, instance):
        rep = super(UserSerializer, self).to_representation(instance)
        rep.pop("password", None)
        return rep

    class Meta:
        model = User
        fields = "__all__"
        write_only_fields = ("password",)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=120)
    new_password = serializers.CharField(max_length=120)

class ProjectTypeSeriaizer(serializers.ModelSerializer):
    class Meta:
        model = ProjectType
        fields = "__all__"

class ProfileSeriaizer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"






