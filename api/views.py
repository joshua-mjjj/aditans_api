import datetime
import hashlib
import json
import os
import random

from rest_framework import status, serializers
from rest_framework.generics import GenericAPIView, ListAPIView, get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import permission_classes, api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework_jwt.views import ObtainJSONWebToken
from django.core.paginator import Paginator 
from django.http import JsonResponse, HttpResponse 
import xlwt 
from vippu_backend.settings import unique_token
from .algorithmn import Cluster_Algorithmn


from api.models import *
from api.serializers import *


class AccountLoginAPIView(ObtainJSONWebToken):
    serializer_class = JWTSerializer

class SignUp(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SignUpSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = True
            user.set_password(serializer.validated_data["password"])
            user.save()

            username = serializer.data["username"]

            # Get user by username
            user = User.objects.get(username=username)

            return Response(
                UserSerializer(user, many=False).data, status=status.HTTP_200_OK
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfile(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    # Run algorithmn whenever a user calls loadUser i.e /users/me
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user, many=False)
        account_type = serializer.data['account_type']
        print(serializer.data['account_type'])
        if account_type == 'normal_user':
            for profile in serializer.data['profiles']:
                cordinate_profile = profile # got one of user's profile
                cordinate_profile_lat = profile['latitude']
                cordinate_profile_lon = profile['longitude']
                profile_project_type = profile['project_type'] 
                print(profile_project_type)
                Cluster_Algorithmn(cordinate_profile_lat, cordinate_profile_lon, profile_project_type)
               
            # pass
            # get your cordinates ==> cordinate(lat, lon)
            # get you profile and try to cluster 
            # get other cordinates that have same location and investiment plan ==> get_neighbours(dataset)
            # form a cluster 
            # Let the mentors know of that cluster ==> Don't need mentors location
            # try to get profiles he can mentor.

        return Response(serializer.data, status=status.HTTP_200_OK)

    # No listing user data
    def list(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # properties 
    @action(detail=True, methods=["GET"])
    def profiles(self, request, *args, **kwargs):
        user = self.get_object()
        queryset = Profile.objects.filter(sponsor=user)
        profiles = self.paginate_queryset(queryset)
        serializer = ProfileSeriaizer(profiles, many=True)
        return self.get_paginated_response(serializer.data)

    # properties 
    @action(detail=True, methods=["GET"])
    def mentor_profiles(self, request, *args, **kwargs):
        user = self.get_object()
        queryset = MentorProfile.objects.filter(sponsor=user)
        profiles = self.paginate_queryset(queryset)
        serializer = MentorProfileSeriaizer(profiles, many=True)
        return self.get_paginated_response(serializer.data)


class ChangePasswordApi(GenericAPIView):
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            old_password = serializer.data["old_password"]
            new_password = serializer.data["new_password"]

            user = self.request.user

            if not user.check_password(old_password):
                content = {"detail": "Invalid Password"}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            else:
                user.set_password(new_password)
                user.save()
                content = {"success": "Password Changed"}
                return Response(content, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectTypeList(ListAPIView):
    serializer_class = ProjectTypeSeriaizer
    queryset = ProjectType.objects.all()

class ProfileViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSeriaizer
    queryset = Profile.objects.all()

class MentorProfileViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = MentorProfileSeriaizer
    queryset = MentorProfile.objects.all()

class ClusterViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ClusterSeriaizer
    queryset = Cluster.objects.all()
