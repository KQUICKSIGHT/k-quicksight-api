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
from permissions.permissions import IsAdminUser
from dashboard.api.serializers import DashboardSerilizer,DashboardResponeSerilizer,UpdateDashboardSerilizer

from analysis.api.serializers import AnalysisSerializer,ExploratoryDataAnalysisSerializer,PerformAnalysisSerializer,AnalysisUpdateSerializer
from analysis.api.service.descriptive import (exploratory_data_analysis,perform_analysis)
from analysis.models import Analysis
from dashboard.models import Dashboard
from sample.api.serializers import SampleAnalysisSerializer,ResponeSampleAnalysisSerializer,SampleDashboardSerializer,ResponeSampleDashboardSerializer
from sample.models import SampleAnalysis,SampleDashboard
from permissions.permissions import IsAdminUser,IsSubscriberUser,IsAdminOrSubscriber


class SampleAnalysisApiView(APIView):
    
    pagination_class = Pagination

    def get_permissions(self):
        if self.request.method in ['GET']:
            return [permissions.AllowAny()]
        return [IsAdminOrSubscriber()]
    
    def post(self, request,*args,**kwargs):
        serilizer = SampleAnalysisSerializer(data=request.data)    
        if serilizer.is_valid():
            model = serilizer.save()
            respone = ResponeSampleAnalysisSerializer(model)
            return Response(respone.data)
        else:
            return Response(serilizer.errors)
        
    def get(self, request,*args,**kwargs):

        title = request.query_params.get('title')
        sample_analysis = None

        if title:
            sample_analysis = SampleAnalysis.objects.filter(
                analysis_uuid__title__icontains=title, is_deleted=False
            ).order_by('-created_at')

        else:
            sample_analysis = SampleAnalysis.objects.filter(
                is_deleted=False
            ).order_by('-created_at')

        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(sample_analysis, request)
        serializer = ResponeSampleAnalysisSerializer(result_page, many=True)
        
        return paginator.get_paginated_response(serializer.data)


class SampleDashboardApiView(APIView):

    pagination_class = Pagination
    
    def get_permissions(self):
        if self.request.method in ['GET']:
            return [permissions.AllowAny()]
        return [IsAdminOrSubscriber()]
    
    def post(self, request,*args,**kwargs):
        serilizer = SampleDashboardSerializer(data=request.data)    
        if serilizer.is_valid():
            model = serilizer.save()
            respone = ResponeSampleDashboardSerializer(model)
            return Response(respone.data)
        else:
            return Response(serilizer.errors)
        
    def get(self, request,*args,**kwargs):

        title = request.query_params.get('title')
        sample_dashboard = None

        if title:
            sample_dashboard = SampleDashboard.objects.filter(
                dashboard_uuid__title__icontains=title, is_deleted=False
            ).order_by('-created_at')

        else:
            sample_dashboard = SampleDashboard.objects.filter(
                is_deleted=False
            ).order_by('-created_at')

        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(sample_dashboard, request)
        serializer = ResponeSampleDashboardSerializer(result_page, many=True)
        
        return paginator.get_paginated_response(serializer.data)


class SampleDashboardDetail(APIView):

    def get(self, request,*args,**kwargs):

        sample_dashboard = get_object_or_404(SampleDashboard,id=kwargs.get("id"),is_deleted=False)
        serilizer = ResponeSampleDashboardSerializer(sample_dashboard)
        return Response(serilizer.data)
    
    def delete(self, request,*args,**kwargs):
        sample_dashboard = get_object_or_404(SampleDashboard,id=kwargs.get("id"),is_deleted=False)
        sample_dashboard.is_deleted = True
        sample_dashboard.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request,*args,**kwargs):
        sample_dashboard = get_object_or_404(SampleDashboard,id=kwargs.get("id"),is_deleted=False)
        serilizer = SampleDashboardSerializer(sample_dashboard, data=request.data)
        if serilizer.is_valid():
            serilizer.save()
            return Response(serilizer.data,status=status.HTTP_200_OK)
        return Response(serilizer.errors,status=status.HTTP_400_BAD_REQUEST)

class SampleAnalysisDetail(APIView):

    def get(self, request,*args,**kwargs):

        sample_analysis = get_object_or_404(SampleAnalysis,id=kwargs.get("id"),is_deleted=False)
        serilizer = ResponeSampleAnalysisSerializer(sample_analysis)
        return Response(serilizer.data)
    
    def delete(self, request,*args,**kwargs):
        sample_analysis = get_object_or_404(SampleAnalysis,id=kwargs.get("id"),is_deleted=False)
        sample_analysis.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request,*args,**kwargs):
        sample_analysis = get_object_or_404(SampleAnalysis,id=kwargs.get("id"),is_deleted=False)
        serilizer = SampleAnalysisSerializer(sample_analysis, data=request.data)
        if serilizer.is_valid():
            serilizer.save()
            return Response(serilizer.data,status=status.HTTP_200_OK)
        return Response(serilizer.errors,status=status.HTTP_400_BAD_REQUEST)


class SampleFileDetail(APIView):

    def get(self, request,*args,**kwargs):
        file = get_object_or_404(File,is_deleted=False,is_sample=True,id=kwargs.get("file_id"))
        return Response(model_to_dict(file))

    def delete(self, request,*args,**kwargs):
        file = get_object_or_404(File,is_deleted=False,is_sample=True,id=kwargs.get("file_id"))
        file.is_deleted = True
        file.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def put(self, request,*args,**kwargs):
        file = get_object_or_404(File,is_deleted=False,is_sample=True,id=kwargs.get("file_id"))
        serilizer = UpdateFileSerializer(file, data=request.data)
        if serilizer.is_valid():
            serilizer.save()
            return Response(serilizer.data,status=status.HTTP_200_OK)
        return Response(serilizer.errors,status=status.HTTP_400_BAD_REQUEST)


class FileUploadView(APIView):

    parser_class = (FileUploadParser,)
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):

        created_by = kwargs["created_by"]
        file_extension = file_util.get_file_extension(
            str(request.data['file']))

        if file_extension not in file_util.ALLOWED_EXTENSIONS_FILE:
            return Response(f"Invalid file extension '{file_extension}'. Allowed extensions are: {', '.join(file_util.ALLOWED_EXTENSIONS_IMAGE)}.",
                            status=status.HTTP_400_BAD_REQUEST)

        data = file_util.handle_uploaded_file(request.data['file'])
        data["created_by"] = created_by
        data["is_sample"] = True

        serializer = CreateUserSerializer(data=data)

        if serializer.is_valid():

            serializer.save()

            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ViewSampleFileApiView(APIView):

    pagination_class = Pagination
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):

        file_title = request.query_params.get('file_title')
        file = None

        if file_title:
            file = File.objects.filter(
                file__icontains=file_title, is_deleted=False
            ).order_by('-created_at')

        else:
            file = File.objects.filter(
                is_deleted=False
            ).order_by('-created_at')


        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(file, request)
        serializer = FileResponeSerializer(result_page, many=True)
        
        return paginator.get_paginated_response(serializer.data)
