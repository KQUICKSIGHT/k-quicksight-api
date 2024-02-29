
from django.urls import path, include
from analysis.api.views import RecommnedationApiView,AnalysisApiView,ExploratoryDataAnalysis,PerformAnalysisView,AnalysisListView,AnalysisDetailView,AnalysisDetailByIdApiView


urlpatterns =   [

    path("",PerformAnalysisView.as_view() , name="analysis-view"),
    path("<int:id>/",AnalysisDetailByIdApiView.as_view() , name="analysis-view-id"),
    path("eda/",ExploratoryDataAnalysis.as_view(),name="eda"),
    path("list/<int:user>/",AnalysisListView.as_view(),name="view-list-analysis"),
    path("detail/<str:uuid>/",AnalysisDetailView.as_view(),name="detail-detail-analysis"),
    path("recommendation/<str:uuid_analysis>/",RecommnedationApiView.as_view(),name="recommendation-view")

]