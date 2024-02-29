
from django.urls import path, include
from django.contrib import admin
from user_role.api.views import UserRoleView

urlpatterns = [


    path("", UserRoleView.as_view(), name="list-user-roles"),

]
