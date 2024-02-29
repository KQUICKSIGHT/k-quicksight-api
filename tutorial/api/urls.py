
from django.urls import path, include
from django.contrib import admin
from django.urls import path,include
from tutorial.api.view import TutorialView,TutorialDetailView,TutorialUUIDDetailView

urlpatterns =   [

    path('', TutorialView.as_view(), name='tutorial_list'),
    path('<int:pk>/', TutorialDetailView.as_view(), name='tutorial_detail'),
    path("view-details/<str:uuid>/", TutorialUUIDDetailView.as_view(), name='tutorial_detail_uuid')
    
]