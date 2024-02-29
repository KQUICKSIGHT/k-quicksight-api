
from django.urls import path, include
from django.contrib import admin
from django.urls import path,include
from sample.api.view import (FileUploadView,SampleFileDetail,ViewSampleFileApiView,
                             SampleAnalysisApiView,SampleAnalysisDetail,
                             SampleDashboardApiView,SampleDashboardDetail)

urlpatterns =   [

    path("upload-sample-file/<int:created_by>/",FileUploadView.as_view(),name="upload-file-sample"),
    path("view-sample-file/",ViewSampleFileApiView.as_view(),name="view-file-sample"),
    path("sample-file/detail/<int:file_id>/",SampleFileDetail.as_view(),name="sample-file-detail"),

    path("analysis/",SampleAnalysisApiView.as_view(),name="sample-analysis"),
    path("analysis/<int:id>/",SampleAnalysisDetail.as_view(),name="sample-analysis-details"),

    path("dashboard/",SampleDashboardApiView.as_view(),name="sample-dashboard"),
    path("dashboard/<int:id>/",SampleDashboardDetail.as_view(),name="sample-dashboard-details"),


]
