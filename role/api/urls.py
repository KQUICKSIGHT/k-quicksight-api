
from django.urls import path, include
from django.contrib import admin

from role.api.views import RoleView

urlpatterns = [


    path("", RoleView.as_view(), name="list-roles"),

]
