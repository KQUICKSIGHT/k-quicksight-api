
from django.urls import path, include
from django.contrib import admin
from django.urls import path,include
from dashboard.api.view import DashboardList,DashboardUUID,DashboardUserUUID,DashboardIDApiView

urlpatterns =   [

    path('', DashboardList.as_view(), name='dashboards'),
    path('<int:id>/', DashboardIDApiView.as_view(), name='dashboards-id-view'),
    path("detail_by_user/<str:uuid>/", DashboardUserUUID.as_view(),name='dashboard-user-uuid'),
    path('detail_by_uuid/<str:uuid>/', DashboardUUID.as_view(), name='dashboards-uuid'),

]
