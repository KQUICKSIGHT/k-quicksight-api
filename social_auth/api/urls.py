
from django.urls import path, include
from django.contrib import admin

from social_auth.api.view import GoogleSocialAuthView,GithubSocialAuthView

urlpatterns = [
    path('google/', GoogleSocialAuthView.as_view(), name="google"),
    path('github/', GithubSocialAuthView.as_view(),name="github"),

]
