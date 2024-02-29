
from django.urls import path, include
from django.contrib import admin
from django.urls import path,include
from file.api.view import FileUploadView,FileViewImageByName,FindFileByUserView,FileUploadImageView,FileDetailsViews,FileDetailsActionView,DeleteFileView,DownloadFileAPIview,GetAllImagesView,ViewHeaderView,FileViewAllApiView

urlpatterns =   [

    path('file-upload/<int:created_by>/', FileUploadView.as_view(), name='file-upload'),
    path("<str:filename>/",FileViewImageByName.as_view(), name='file-view-image'),
    path("user/<int:created_by>/",FindFileByUserView.as_view(), name='user-view-file'),
    path("user/<int:created_by>/<str:uuid>/",DeleteFileView.as_view(), name='user-uuid-file'),
    path("upload/images/", FileUploadImageView.as_view(), name='upload-image'),
    path("details/<str:uuid>/", FileDetailsViews.as_view(), name="details-file"),
    path("files-detail-dataset/<str:uuid>/", FileDetailsActionView.as_view(), name="files-detail-file"),
    path("download/<str:filename>/", DownloadFileAPIview.as_view(), name="download-file"),
    path('view/images/', GetAllImagesView.as_view(), name='get-all-images'),    
    path("headers/view/<str:filename>/",ViewHeaderView.as_view(), name='view-header'),
    path("",FileViewAllApiView.as_view(), name='view-all-file'),
]
# bedbd992f3284aedb7f79bb485688260