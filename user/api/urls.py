
from django.urls import path, include
from django.contrib import admin

from user.api.view import UserListView, UserDetailView, UserDetailUUIDView,UserDetailEmailView,GroupsRoleView,ListUsersView

urlpatterns = [


    path("", UserListView.as_view(), name="list-users"),
    path("<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    path("uuid/<str:uuid>/", UserDetailUUIDView.as_view(), name="user-detail-uuid"),
    path("email/<str:email>/", UserDetailEmailView.as_view(), name="user-email-detail"),
    path("groups/",GroupsRoleView.as_view(),name="groups-role-detail"),
    path("list/",ListUsersView.as_view(),name="list-users")
]
