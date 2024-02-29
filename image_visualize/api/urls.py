
from django.urls import path, include
from django.contrib import admin

from image_visualize.api.views import UploadImageVisualize,ImageVisualizeDetailApiView

urlpatterns = [

    path("<str:uuid_created_by>/", UploadImageVisualize.as_view(), name="upload-image-users"),
    path("<str:uuid_updated_by>/<str:uuid_image>/", ImageVisualizeDetailApiView.as_view(),name="image-visualize-detail")
]
