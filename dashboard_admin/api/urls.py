
from django.urls import path, include
from dashboard_admin.api.view import DashboardAdminApiView
urlpatterns =   [

    path('', DashboardAdminApiView.as_view(), name='dashboard_admin'),    

]