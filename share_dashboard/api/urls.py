
from django.urls import path, include
from django.contrib import admin
from django.urls import path,include
from share_dashboard.api.views import ShareFileMemberView,VerifyAddMember,UserFileShareListView,ShareFileViewByIdView,SharedFileMemberView

urlpatterns =   [

    path('', ShareFileMemberView.as_view(), name='share-file'),
    path('verify/<str:uuid>/<str:status>/', VerifyAddMember.as_view(), name='verfy-file'),
    path("list/<int:file_id>/",UserFileShareListView.as_view(),name="share-file-member"),
    path("owner/<int:user_id>/",ShareFileViewByIdView.as_view(),name="share-file-owner"),
    path("member/<int:user_id>/",SharedFileMemberView.as_view(),name="share-file-memnber-view")

]