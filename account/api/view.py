# from rest framework
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, status, views, permissions
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase
from django.db.models import Sum

# from django
from django.contrib.auth import authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils import timezone
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework import exceptions, status

from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.state import token_backend
# from user building
from account.api.serializers import RegisterSerializer,ForgotPasswordSerilizer, ChangePasswordByForgotPasswordSerializer,VerifycationEmailPasswordSerializer,RegisterithGoogleSerializer,UserSerializer, CreateUserSerializer, EmailVerificationSerializer, LogoutSerializer, ResetPasswordEmailRequestSerializer, ProfileSerializer, UpdateUserLoggedInAtSerializer, CustomTokenRefreshSerializer, CookieTokenRefreshSerializer
from account.api.renderers import UserRenderer
from user.models import User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.conf import settings
from django.shortcuts import redirect

# from other
import uuid
from .utils import Util
import jwt
from datetime import datetime
import random
from account.api.service import AccountService
import os
from user_role.models import UserRole
from django.forms.models import model_to_dict
from role.models import Role
from file.models import File


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    return Response({"message": "Hello, user!"})


class CheckVerifyCodeEmail(APIView):

    def post(self, request):
        
        return Response(None)


class ForgotPasswordView(APIView):

    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        
        serializer = ForgotPasswordSerilizer(data=request.data)
        if serializer.is_valid():
            return Response({"message":"Please check your email to verify code."})
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class VerifyForgotPasswordApiView(APIView):

    permission_classes = [permissions.AllowAny]

    def post(self, request):

        serializer = VerifycationEmailPasswordSerializer(data=request.data)  
        
        if serializer.is_valid():
            
            user = get_object_or_404(User,
                                     email=serializer.validated_data.get("email"),
                                     is_deleted=False
                                     )
            

            if not user.expired_at and not user.verification_code:
                return Response({"message":"Please verify with your email first."})
            
            if user.verification_code == serializer.validated_data.get("verification_code"):
                if user.expired_at >= timezone.now():

                    user.expired_at = None
                    user.verification_code = None
                    uid_base64 = urlsafe_base64_encode(smart_bytes(user.id))
                    token = PasswordResetTokenGenerator().make_token(user)
                    user.token=token
                    user.uid_base64=uid_base64
                    
                    return Response(
                        {
                            "message":"Please Change your password.",
                            "token":token,
                            "uid_base64":uid_base64
                        })
                else:
                    return Response({"message":"Your verification code is expired. Please try again."})
            else:
                return Response({"message":"Your verification code is incorrect. Please try again."})


        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ChangeForgotPasswordApiView(APIView):

    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):

        user = get_object_or_404(User,email = request.data.get('email'),is_deleted=False)
        serilaizer =ChangePasswordByForgotPasswordSerializer(user,data=request.data)

        if serilaizer.is_valid():
            serilaizer.save()
            return Response({"message":"You have successfully changed your password."})
        return Response(serilaizer.errors,status=status.HTTP_200_OK)


class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):

        user_data = request.data
        virified_code = ''.join(random.choices('0123456789', k=6))

        user_data['verification_code'] = virified_code
        user_data["is_deleted"] = True


        serializer = self.serializer_class(data=user_data)
        

        
        if serializer.is_valid():

            user = serializer.save()
            role_instance = Role.objects.get(id=2)
            user_role = UserRole()
            user_role.user = user  # Assuming 'user' is an instance of the User model
            user_role.role = role_instance  # Assuming 'role_instance' is an instance of the Role model
            user_role.save()

            email_body = Util.get_html_verify(virified_code)
            data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Verify your email'}

            Util.send_email(data)
            user_data.pop('password',  )
            return Response(user_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class RegisterWithGoogleView(APIView):

    serializer_class = RegisterithGoogleSerializer
    renderer_classes = (UserRenderer,)
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):

        user = request.data
        user['is_verified'] = True
        user["is_deleted"] = False

        serializer = CreateUserSerializer(data=user)

        if serializer.is_valid():
            user = serializer.save()
            role_instance = Role.objects.get(id=2)
            user_role = UserRole()
            user_role.user = user  # Assuming 'user' is an instance of the User model
            user_role.role = role_instance  # Assuming 'role_instance' is an instance of the Role model
            user_role.save()
            user_serializer = UserSerializer(user)
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):

    permission_classes = [permissions.AllowAny]

    def post(self, request):

        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)

        if user:

            if not user.is_deleted:

                user.logged_in_at = timezone.now()
                user.save(update_fields=['logged_in_at'])

                refresh = RefreshToken.for_user(user)

                return Response({

                    "data": {

                        'refresh': str(refresh),

                        'access': str(refresh.access_token)

                    }

                })

        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class RefreshView(TokenRefreshView):

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        # Add custom behavior here. For example, adding additional response data:
        response.data['custom'] = 'Custom data'

        return response


class VerifyEmail(views.APIView):

    serializer_class = EmailVerificationSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        verification_code = serializer.validated_data.get("verification_code")
        user_email = request.data.get("email")

        user = None
        # find user by email
        try:
            user = User.objects.get(email=user_email)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # check expired
        if user:
            if user.expired_at:
                if user.expired_at < timezone.now():
                    return Response({"error": "Verification code is expired!"}, status=status.HTTP_400_BAD_REQUEST)
                # check verification code
                if user.verification_code == verification_code:

                    user.verification_code = None
                    user.expired_at = None
                    user.is_verified = True
                    user.is_deleted = False
                    user.save()

                    return Response({"success": "Verification code is correct!"}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Verification code is incorrect!"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "not found."}, status=status.HTTP_404_NOT_FOUND)

    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:

            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload['id'])

            if not user.is_verified:
                user.is_verified = True
                user.save()

            return redirect('https://istad.co/')

        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class ResendVerificationCodeAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            if user.email_verified:
                return Response({'message': 'Email already verified'}, status=status.HTTP_400_BAD_REQUEST)

            # Generate a new code and send email
            user.verification_code = str(uuid.uuid4())
            user.verification_code_created = timezone.now()
            user.save()

            virified_code = ''.join(random.choices('0123456789', k=6))

            email_body = 'Hi '+user.username + \
                ' Here your verified code :  \n' + str(virified_code)

            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Verify your email'}

            Util.send_email(data)

            return Response({'message': 'Verification code resent'}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):

        refresh_token = request.data['refresh']
        token = RefreshToken(refresh_token)
        token.blacklist()  # This will add the token to the blacklist
        return Response(status=status.HTTP_205_RESET_CONTENT)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):

    user = request.user
    total_sum = File.objects.filter(is_deleted=False,created_by=user.id).aggregate(sum_size=Sum('size'))
    user.storage_data=total_sum["sum_size"]

    serializer = ProfileSerializer(user)
    return Response({"data": serializer.data}, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        # user = User.objects.get(email=email, is_deleted=False)
        user = get_object_or_404(User,email=email, is_deleted=False )

        serializer = ResetPasswordEmailRequestSerializer(
            user, data=request.data, context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class CookieTokenRefreshView(TokenRefreshView):
    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('refresh'):
            cookie_max_age = 3600 * 24 * 14  # 14 days
            response.set_cookie(
                'refresh_token', response.data['refresh'], max_age=cookie_max_age, httponly=True)
            del response.data['refresh']
        return super().finalize_response(request, response, *args, **kwargs)
    serializer_class = CookieTokenRefreshSerializer
