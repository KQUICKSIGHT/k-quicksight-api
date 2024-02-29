
from django.urls import path, include
from django.contrib import admin
from django.urls import path,include
from request_tutorial.api.view import RequestTutorialView,RequestTutorialDetailView

urlpatterns =   [

    path('', RequestTutorialView.as_view(), name='request_tutorial_list'),
    path('<int:pk>/', RequestTutorialDetailView.as_view(), name='request_tutorial_detail'),
    
]