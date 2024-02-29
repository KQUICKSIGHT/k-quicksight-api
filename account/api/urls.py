
from django.urls import path, include
from django.contrib import admin
from django.urls import path, include
from account.api.view import (
    RegisterView, LoginView ,VerifyEmail, LogoutAPIView, 
    get_profile, ChangePasswordView,RegisterWithGoogleView,
    ForgotPasswordView,VerifyForgotPasswordApiView,ChangeForgotPasswordApiView
)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from social_auth.api.view import GoogleSocialAuthView,GithubSocialAuthView,FacebookSocialAuthView



urlpatterns = [

    path("register/", RegisterView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify/', VerifyEmail.as_view(), name="email-verify"),
    path('logout/', LogoutAPIView.as_view(), name="logout"),
    path("me/", get_profile, name='get-me'),
    path('google/', GoogleSocialAuthView.as_view(), name="google"),
    path('github/', GithubSocialAuthView.as_view(), name="github"),
    path('facebook/', FacebookSocialAuthView.as_view(), name="facebook"),
    path("change-password/", ChangePasswordView.as_view(), name="chnage_password"),
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot_password"),
    path("verify-forgot-password/",VerifyForgotPasswordApiView.as_view(), name="verify_forgot_password"),
    path("change-forgot-password/",ChangeForgotPasswordApiView.as_view(), name="change_forgot_password"),

]
