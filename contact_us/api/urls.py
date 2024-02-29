
from django.urls import path, include
from django.urls import path,include
from contact_us.api.view import ContatUsView,ContactUsDetailView
urlpatterns =   [

    path('', ContatUsView.as_view(), name='contact_us'),    
    path('<int:pk>/', ContactUsDetailView.as_view(), name='contact_us_detail'),
]