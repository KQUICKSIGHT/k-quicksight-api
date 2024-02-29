from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser


from django.http import FileResponse
from django.shortcuts import render

from file.api.serializers import FileResponeSerializer, CreateUserSerializer, UpdateFileSerializer, FileQuerySerializer

import os
from utils import file_util
import pandas as pd
from file.models import File
from django.shortcuts import get_object_or_404
import file.api.service as service
import json
from django.http import JsonResponse
from django.forms.models import model_to_dict
from scrape.api.service import scrape_to_csv, save_file, remove_file,load_dataset
from scrape.api.serializers import ScrapeDataByUrlSerializer, ConfirmDataSetSerializer
from user.models import User
from django.http import Http404
from pagination.pagination import Pagination


class ScraperDataByUrlView(APIView):

    def post(self, request, *args, **kwargs):

        serilaizer = ScrapeDataByUrlSerializer(data=request.data)

        if serilaizer.is_valid():

            result = scrape_to_csv(serilaizer.validated_data.get("url"))
            return Response(result, status=status.HTTP_200_OK)

        return Response(serilaizer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmDataSetView(APIView):

    def post(self, request, *args, **kwargs):

        created_by = kwargs.get("created_by")
        serilizer = ConfirmDataSetSerializer(data=request.data)

        if User.objects.filter(id=created_by, is_deleted=False).exists():

            if serilizer.is_valid():

                confirmed = save_file(
                    serilizer.validated_data.get("confirmed_filename"),
                    User.objects.get(id=created_by, is_deleted=False)
                )

                rejected = remove_file(
                    serilizer.validated_data.get("rejected_filename")
                )

                return Response(
                    {
                        "code": 200,
                        "confirmed_message": confirmed,
                        "rejected_message": rejected
                    }, status=status.HTTP_200_OK)

            return Response(serilizer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"detail": "User not found."},
            status=status.HTTP_404_NOT_FOUND
        )

class ViewDataSetByFilenameView(APIView):
    pagination_class = Pagination

    def get(self, request, *args, **kwargs):
        
        data = load_dataset(filename=kwargs.get('filename'))
        records = data.get("data", [])  # Extract the list of records

        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(records, request)
        records = data.get("data", [])  # Extract the list of records
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(records, request)            
        paginated_response = paginator.get_paginated_response(result_page).data
        paginated_response["headers"] = list(data.get("header", [])) 
        paginated_response["file"]=data.get("file","")
        paginated_response["total"]=data.get("total",None)
        paginated_response["filename"]=kwargs.get('filename')

        return Response(paginated_response)
