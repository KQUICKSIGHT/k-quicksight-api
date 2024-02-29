
from rest_framework import serializers
from user.models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework_simplejwt.tokens import BlacklistedToken
from rest_framework import status, exceptions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth import get_user_model
import logging
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken
from user.api.serializers import PermissionSerializer, GroupRoleSerializer
from user_role.models import UserRole
from role.models import Role
from django.forms.models import model_to_dict
from analysis.models import Analysis
from dashboard.models import Dashboard
from .utils import Util
import random
from django.utils import timezone


class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = [
            'verification_code',
            'is_deleted',
            'is_active',
            'is_superuser',
            'is_staff',
            'date_joined',
            'last_login',
            'groups',
            'created_at',
            'logged_in_at',
            'expired_at',
            'uuid',
        ]

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError(
                self.default_error_messages)
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class RegisterSerializer(serializers.ModelSerializer):


    class Meta:
        model = User
        fields = ['email', 'username', 'password',
                  'verification_code', 'is_confirmed',]

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError(
                self.default_error_messages)
        return attrs

    def create(self, validated_data):
        print(validated_data)
        return User.objects.create_user(**validated_data)

class RegisterithGoogleSerializer(serializers.ModelSerializer):
    roles = serializers.MultipleChoiceField(choices=[1, 2], required=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password',
                  'verification_code', 'is_confirmed', 'roles']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError(
                self.default_error_messages)
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']  # Include fields that you want to serialize for the role



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = [
            'id',
            'password',
            'verification_code',
            'is_active',
            'is_superuser',
            'is_staff',
            'date_joined',
            'last_login',
            'groups',
            'expired_at',
            'logged_in_at',
            'is_verified',
        ]


class EmailVerificationSerializer(serializers.ModelSerializer):
    verification_code = serializers.CharField(max_length=6, required=True)

    class Meta:
        model = User
        fields = ['verification_code']


class LogoutSerializer(serializers.Serializer):

    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:

            refresh_token = RefreshToken(self.token)
            # Create an instance of BlacklistedToken to blacklist the token
            BlacklistedToken.objects.create(token=refresh_token)

        except TokenError:
            self.fail('bad_token')


class ResetPasswordEmailRequestSerializer(serializers.ModelSerializer):
    
    old_password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    confirmed_password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    email = serializers.CharField(max_length=250, required=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'confirmed_password', 'old_password']

    def validate(self, attrs):
        if attrs['password'] != attrs['confirmed_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def create(self, validated_data):
        # Remove 'confirmed_password' and 'old_password' from the data
        validated_data.pop('confirmed_password', None)
        validated_data.pop('old_password', None)

        user = User.objects.create_user(**validated_data)

        return user

    def update(self, instance, validated_data):
        # Your existing update logic
        instance.set_password(validated_data['password'])
        instance.save()

        return instance



class AnalysisSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Analysis
        fields=("__all__")


class ForgotPasswordSerilizer(serializers.Serializer):

    email = serializers.CharField(max_length=200,required=True)
    message = serializers.CharField(max_length=200,required=False)

    def validate_email(self, obj):
        try:

            user = User.objects.get(email=obj,is_deleted=False)
            if user :
                verification_code = ''.join(random.choices('0123456789', k=6))

                email_body = Util.get_html_verify(verification_code)
                data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Verify your email'}
                # logic verify 
                user.verification_code=verification_code
                user.expired_at=timezone.now() + timezone.timedelta(minutes=30)
                user.save()
                Util.send_email(data)
                
        except User.DoesNotExist :
            raise serializers.ValidationError({"message": "Email is not found."})

class VerifycationEmailPasswordSerializer(serializers.Serializer):
    
    email = serializers.CharField(max_length=200,required=True)
    verification_code = serializers.CharField(max_length=200,required=True)

class ChangePasswordByForgotPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    confirmed_password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    email = serializers.EmailField(max_length=250, required=True)



class ChangePasswordByForgotPasswordSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    confirmed_password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    email = serializers.EmailField(max_length=250, required=True)
    uid_base64 = serializers.CharField(max_length=250, required=True)
    token = serializers.CharField(max_length=250, required=True)
    class Meta:
        model = User
        fields = ['email', 'password', 'confirmed_password','uid_base64','token']

    def validate(self, attrs):
        try:
            password = attrs.get('password')

            if attrs['password'] != attrs['confirmed_password']:
                raise serializers.ValidationError({"password": "Password fields didn't match."})
            token = attrs.get('token')
            uidb64 = attrs.get('uid_base64')
            print("token: %s" % token)
            print("uidb64: %s" % uidb64)
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)
            return attrs
        except Exception as e:
            print(e)
            raise AuthenticationFailed('The reset link is invalid', 401)
    
    def create(self, validated_data):
        # Remove 'confirmed_password' and 'old_password' from the data
        validated_data.pop('confirmed_password', None)

        user = User.objects.create_user(**validated_data)

        return user

    def update(self, instance, validated_data):
        # Your existing update logic
        instance.set_password(validated_data['password'])
        instance.save()

        return instance


class DashboardResponeSerilizer(serializers.ModelSerializer):


    class Meta:

        model = Dashboard
        exclude = ["id","created_by"]


class ProfileSerializer(serializers.ModelSerializer):

    roles = serializers.SerializerMethodField()
    analysis = serializers.SerializerMethodField() 
    dashboards = serializers.SerializerMethodField() 

    class Meta:
        model = User
        fields = [
            'id', 'username', 'gender', 'dob', 'uuid', 'email',
            'phone_number', 'full_name', 'address', 'biography', 'avatar',
            'storage_data', 'created_at', 'logged_in_at', 'expired_at',
            'auth_provider', 'is_verified', 'is_confirmed',"roles","analysis","dashboards"
        ]


    def get_roles(self, obj):

        user_roles = UserRole.objects.filter(user=obj)
        roles = []
        if user_roles:
            for user_role  in user_roles:
                roles.append(user_role.role)                
        return RoleSerializer(roles, many=True).data
    
    def get_analysis(self, obj):

        analysis_data = Analysis.objects.filter(user_id=obj,is_deleted=False)
        return AnalysisSerializer(analysis_data, many=True).data

    def get_dashboards(self, obj):

        dashboard = Dashboard.objects.filter(created_by=obj,is_deleted=False)
        return DashboardResponeSerilizer(dashboard, many=True).data

class UpdateUserLoggedInAtSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["logged_in_at"]


User = get_user_model()


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        user_id = data.get('user_id')
        logging.debug(f"User ID from token: {user_id}")

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            logging.error(f"User with ID {user_id} does not exist.")
            raise ValidationError(
                {'detail': 'User not found', 'code': 'user_not_found'})

        return data


class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = None

    def validate(self, attrs):
        attrs['refresh'] = self.context['request'].COOKIES.get('refresh')
        if attrs['refresh']:
            return super().validate(attrs)
        else:
            raise InvalidToken(
                'No valid token found in cookie \'refresh_token\'')
