
from django.urls import path, include
from django.contrib import admin

from templates.api.views import not_found,rejected,accepted

urlpatterns = [


    path("not-found/",not_found, name="page-not-found"),
    path("rejected/",rejected, name="page-rejected"),
    path("accepted/",accepted, name="page-accepted")
]
