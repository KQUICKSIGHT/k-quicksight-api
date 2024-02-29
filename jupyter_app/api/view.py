from django.shortcuts import render
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser


from django.http import FileResponse
from django.shortcuts import render

from file.api.serializers import FileResponeSerializer, CreateUserSerializer, UpdateFileSerializer, FileQuerySerializer,DynamicRecordSerializer
from django.http import HttpResponse

import os
from utils import file_util
import pandas as pd
from file.models import File
from django.shortcuts import get_object_or_404
import file.api.service as service
import json
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.http import FileResponse, Http404
import uuid
from rest_framework import status, permissions
# Create your views here.
from django.shortcuts import render
import os
import uuid
from dotenv import load_dotenv
from jupyter_app.models import JupyterDocument
from user.models import User
from pagination.pagination import Pagination
from jupyter_app.api.serializers import JupyterSerializer
from django.shortcuts import get_object_or_404


dotenv_path_dev = '.env'
load_dotenv(dotenv_path=dotenv_path_dev)
file_server_path_jupyter = os.getenv("FILE_SERVER_PATH_JUPYTER")

def notebook_view(request, filename):

    file_path = os.path.join(file_server_path_jupyter, filename)
    
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    response = HttpResponse(html_content, content_type='text/html')
    
    # Allow iframe embedding
    response["X-Frame-Options"] = "ALLOWALL"

    # If dealing with cross-origin, set appropriate CORS headers
    # response["Access-Control-Allow-Origin"] = "*"

    return response


class UploadJypyterView(APIView):

    parser_class = (FileUploadParser,)
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args,**kwargs):

        file_extension = file_util.get_file_extension(
            str(request.data['file'])
        )

        if file_extension !=  ".ipynb":
            return Response(f"Invalid file extension '{file_extension}'. Allowed extensions are ipynb.",
                            status=status.HTTP_400_BAD_REQUEST)

        data = file_util.upload_jupyter(request.data['file'])

        insert_data={
            "filename": data["filename"],
            "file":  str(request.data['file']),
        }
        jupyter_document =JupyterDocument(
            file=str(request.data['file']),
            filename=data["filename"],
            size=data["size"].split()[0],
            created_by=User.objects.get(id=kwargs.get("created_by"))
        )
        jupyter_document.save()
        dict_jypyter=model_to_dict(jupyter_document)
        dict_jypyter["jypyter_url"]=data["url"]
        dict_jypyter.pop("created_by", None)

        # Create and save the JupyterDocument instance
        return Response(data=dict_jypyter, status=status.HTTP_200_OK)
    
class JupyterDocumentView(APIView):
    
    pagination_class = Pagination
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):

        file = request.query_params.get('file')
        jupyter_document = None

        if file :
            jupyter_document = JupyterDocument.objects.filter(
                file__icontains=file,
                is_deleted=False,
            ).order_by("-created_at")
        else:
            jupyter_document = JupyterDocument.objects.filter(
                is_deleted=False,
            ).order_by("-created_at")
        
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(jupyter_document, request)
        serializer = JupyterSerializer(result_page, many=True)
        
        return paginator.get_paginated_response(serializer.data)

class JupyterDocumentDetailView(APIView):

    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        
        jupyter = get_object_or_404(JupyterDocument,id=kwargs.get("jupyter_id"))
        serilizer = JupyterSerializer(jupyter)
        return Response(serilizer.data,status=status.HTTP_200_OK)
    
    def delete(self, request, *args, **kwargs):

        jupyter = get_object_or_404(JupyterDocument,id=kwargs.get("jupyter_id"))

        if file_util.remove_file_juypyter(jupyter.filename):
            jupyter.is_deleted=True
            jupyter.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)
        
