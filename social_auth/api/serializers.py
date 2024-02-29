from rest_framework import serializers
from request_tutorial.models import RequestTutorial
from user.api.serializers import UserSerializer

from rest_framework import serializers
from . import google,facebook
from .register import register_social_user
import os
from rest_framework.exceptions import AuthenticationFailed
from library.socialib import github


class GoogleSocialAuthSerializer(serializers.Serializer):

    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):

        user_data = google.Google.validate(auth_token)
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )

        if user_data['aud'] != os.environ.get('GOOGLE_CLIENT_ID'):

            raise AuthenticationFailed('oops, who are you?')

        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']
        provider = 'google'
        fullname = user_data["name"]
        avatar = user_data['picture']

        return register_social_user(
            provider=provider,
            user_id=user_id,
            email=email,
            name=name,
            fullname=fullname,
            avatar=avatar
        )


class GithubSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()


    def validate_auth_token(self, auth_token):
        user_data = github.Github.validate(auth_token)
        username= user_data["login"]
        avatar= user_data["avatar_url"]
        try:
            email = user_data['email']
            provider = 'github'
        except Exception as e:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )
        return register_social_user(
            provider=provider, user_id=None, email=email, name=username, avatar=avatar)

class FacebookSocialAuthSerializer(serializers.Serializer):

    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):

        user_data = facebook.Facebook.validate(auth_token)
        name = None
        avatar = None
        email = None
        try:
            
            email = user_data.get('email', '')
            name = user_data.get('name', '')
            provider = 'facebook'
            avatar = user_data.get('picture', {}).get('data', {}).get('url', '')

        except Exception as identifier:
            raise serializers.ValidationError(
                'The token  is invalid or expired. Please login again.'
            )
        return register_social_user(
                provider=provider,
                user_id=None,
                email=email,
                name=name,
                avatar=avatar,
            )
