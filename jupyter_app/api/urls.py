from django.urls import path
from jupyter_app.api.view import notebook_view,UploadJypyterView,JupyterDocumentView,JupyterDocumentDetailView

urlpatterns = [
    path('notebook/<str:filename>/', notebook_view, name='notebook-view'),
    path("upload-jypyter/<int:created_by>/", UploadJypyterView.as_view(), name='upload-jypyter-view'),
    path("",JupyterDocumentView.as_view(),name="list-jupyter-document"),
    path("details/<int:jupyter_id>/", JupyterDocumentDetailView.as_view(), name='detail-jupyter-document')
]
