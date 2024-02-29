from django.contrib import admin
from django.urls import path, include
from django.conf import settings


from rest_framework import permissions
from django.conf.urls.static import static
from social_django.views import auth as social_auth_views

API_V1 = "api/v1/"

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@local.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [

    path(API_V1+"accounts/", include("account.api.urls")),
    path(API_V1+"users/", include("user.api.urls")),
    path(API_V1+"files/", include("file.api.urls")),
    path(API_V1+"data-clean/", include("cleansing.api.urls")),
    path(API_V1+"tutorials/", include("tutorial.api.urls")),
    path(API_V1+"request_tutorials/", include("request_tutorial.api.urls")),
    path(API_V1+"contact_us/", include("contact_us.api.urls")),
    path(API_V1+'social_auth/', include('social_auth.api.urls')),
    path(API_V1+'roles/', include('role.api.urls')),
    path(API_V1+'user_roles/', include('user_role.api.urls')),
    path(API_V1+'share-dataset/', include('share_member.api.urls')),
    path(API_V1+'analysis/', include('analysis.api.urls')),
    path(API_V1+'scrape/', include('scrape.api.urls')),
    path(API_V1+"jupyter/",include('jupyter_app.api.urls')),
    path(API_V1+"visualize/",include('visualization.api.urls')),
    path(API_V1+"dashboards/",include('dashboard.api.urls')),
    path(API_V1+"image-visualizes/",include('image_visualize.api.urls')),
    path(API_V1+"dashboard-admin/",include('dashboard_admin.api.urls')),
    path(API_V1+"sample/",include('sample.api.urls')),
    path(API_V1+"share-analysis/",include('share_analysis.api.urls')),
    path(API_V1+"share-dashboard/",include('share_dashboard.api.urls')),


    path("templates/", include('templates.api.urls')),
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
