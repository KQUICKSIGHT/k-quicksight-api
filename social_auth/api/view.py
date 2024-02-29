from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from request_tutorial.models import RequestTutorial
from request_tutorial.api.serializers import RequestTutorialSerializer, CreateRequestTutorialSerializer
from pagination.pagination import Pagination
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from social_django.utils import load_strategy
from django.contrib.auth import login
from social_django.models import UserSocialAuth
import jwt
from rest_framework.generics import GenericAPIView
from social_auth.api.serializers import GoogleSocialAuthSerializer,GithubSocialAuthSerializer,FacebookSocialAuthSerializer


class GoogleSocialAuthView(GenericAPIView):

    serializer_class = GoogleSocialAuthSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """

        POST with "auth_token"

        Send an idtoken as from google to get user information

        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])
        return Response(data, status=status.HTTP_200_OK)

class GithubSocialAuthView(APIView):

    serializer_class = GithubSocialAuthSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])
        return Response(data, status=status.HTTP_200_OK)

class FacebookSocialAuthView(GenericAPIView):

    serializer_class = FacebookSocialAuthSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])
        return Response(data, status=status.HTTP_200_OK)