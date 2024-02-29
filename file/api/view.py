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
from pagination.pagination import Pagination


class FileViewAllApiView(APIView):
    pagination_class = Pagination

    def get(self, request, *args, **kwargs):

        file_name = request.query_params.get('file')
        file = None
        
        if file_name :
            file = File.objects.filter(
                file__icontains=file_name,
                is_deleted=False,
                is_sample=False
            ).order_by("-created_at")
        else:
            file = File.objects.filter(
                is_deleted=False,
                is_sample=False
            ).order_by("-created_at")

        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(file, request)
        serializer = FileResponeSerializer(result_page, many=True)
        
        return paginator.get_paginated_response(serializer.data)

class FileUploadImageView(APIView):

    parser_class = (FileUploadParser,)
    permission_classes = [permissions.AllowAny]

    def post(self, request):

        file_extension = file_util.get_file_extension(
            str(request.data['file'])
        )

        # Convert both the file extension and the allowed extensions to lowercase before comparison
        if file_extension.lower() not in (allowed.lower() for allowed in file_util.ALLOWED_EXTENSIONS_IMAGE):
            return Response(f"Invalid file extension '{file_extension}'. Allowed extensions are: {', '.join(file_util.ALLOWED_EXTENSIONS_IMAGE)}.",
                            status=status.HTTP_400_BAD_REQUEST)


        data = file_util.handle_uploaded_file_image(request.data['file'])

        return Response(data=data, status=status.HTTP_200_OK)

class ViewHeaderView(APIView):

    permission_classes = [permissions.AllowAny]

    def get(self, request,*args, **kwargs):
        filename = kwargs["filename"]

        result = service.load_datasetHeader(filename=filename)
        return Response(result)

class FileUploadView(APIView):

    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):

        created_by = kwargs["created_by"]
        file_extension = file_util.get_file_extension(
            str(request.data['file']))

        if file_extension not in file_util.ALLOWED_EXTENSIONS_FILE:
            return Response(f"Invalid file extension '{file_extension}'. Allowed extensions are: {', '.join(file_util.ALLOWED_EXTENSIONS_IMAGE)}.",
                            status=status.HTTP_400_BAD_REQUEST)

        data = file_util.handle_uploaded_file(request.data['file'])
        data["created_by"] = created_by

        serializer = CreateUserSerializer(data=data)

        if serializer.is_valid():

            serializer.save()

            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FileViewImageByName(APIView):

    permission_classes = [permissions.AllowAny]

    def get(self, request, filename):

        image_path = os.path.join(file_util.get_file_server_path(), filename)

        if os.path.exists(image_path):

            return FileResponse(open(image_path, 'rb'), content_type='image/jpeg')

        else:

            return Response("Image not found", status=status.HTTP_404_NOT_FOUND)


class FindFileByUserView(APIView):

    pagination_class = Pagination

    def get(self, request, *args, **kwargs):

        query_serializer = FileQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        validated_data = query_serializer.validated_data

        filename = validated_data.get("filename")
        type_file = validated_data.get("type")

        file_queryset = File.objects.filter(
            created_by=kwargs["created_by"], is_deleted=False,
            is_sample=False
        ).order_by('-created_at')

        if filename:
            file_queryset = file_queryset.filter(file__icontains=filename)
        if type_file:
            file_queryset = file_queryset.filter(type=type_file)

        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(file_queryset, request)
        serializer = FileResponeSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class DownloadFileAPIview(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, *args, **kwargs):

        filename = kwargs.get("filename")
        
        file_model = get_object_or_404(
            File, filename=filename,is_deleted=False
        )  
        
        file = service.download_file(filename)

        if file:
    
            return file        
        
        return Response({"message":"file not found"}, status=status.HTTP_404_NOT_FOUND)



class FileDetailsViews(APIView):

    pagination_class = Pagination
    permission_classes = [permissions.AllowAny]


    def get(self, request, *args, **kwargs):

        uuid = kwargs.get("uuid")
        file = File.objects.get(uuid=uuid)
        filename = file.filename
        data = service.load_dataset(filename, file=file.file)

        data["id"]=file.id
        data["created_at"] = file.created_at
        data["filename"] = file.filename
        data["size"] = file.size
        data["uuid"] = file.uuid
        data["type"] = file.type

        if data:
            records = data.get("data", [])  # Extract the list of records

            paginator = self.pagination_class()
            result_page = paginator.paginate_queryset(records, request)            
            paginated_response = paginator.get_paginated_response(result_page).data
            paginated_response["id"]=file.id
            paginated_response["headers"] = list(data.get("header", [])) 
            paginated_response["file"]=data.get("file","")
            paginated_response["filename"]=filename
            paginated_response["total"]=data.get("total",None)
            
            return Response(paginated_response)

        return Response({
            "message": "Oops! The file you are looking for could not be found.",
            "advice": "Please check the file path or contact support for assistance."
        }, status=status.HTTP_404_NOT_FOUND)


class FileDetailsActionView(APIView):

    def put(self, request, *args, **kwargs):

        uuid = kwargs.get("uuid")
        file = File.objects.filter(uuid=uuid).first()
        if file:

            serilizer = UpdateFileSerializer(file, data=request.data)
            if serilizer.is_valid():
                serilizer.save()
                return Response(serilizer.data, status=status.HTTP_200_OK)

            return Response(serilizer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "message": "Oops! The file you are looking for could not be found.",
            "advice": "Please check the file path or contact support for assistance."
        }, status=status.HTTP_404_NOT_FOUND)


class DeleteFileView(APIView):

    # wait to process with server
    def delete(self, request, *args, **kwargs):

        uuid = kwargs.get('uuid')

        file = get_object_or_404(
            File, created_by=kwargs["created_by"], uuid=uuid, is_deleted=False,is_sample=False
        )

        if service.remove_file(file.filename):
            file.is_deleted = True
            file.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        else:
            return Response({"error": "File not found"}, status=status.HTTP_404_NOT_FOUND)


class GetAllImagesView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        image_folder_path = file_util.get_file_server_path()

        if os.path.exists(image_folder_path):
            
            image_files = [f for f in os.listdir(image_folder_path) if os.path.isfile(os.path.join(image_folder_path, f))]
            images_data = [
                {"_id": str(uuid.uuid4().hex), 
                 "img": f"https://photostad-api.istad.co/api/v1/files/{filename}"}
                   for filename in image_files]

            return Response(images_data, status=status.HTTP_200_OK)

        else:
            return Response("No Images", status=status.HTTP_404_NOT_FOUND)
        