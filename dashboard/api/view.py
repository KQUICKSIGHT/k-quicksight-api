from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser


import os
from utils import file_util
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django.http import FileResponse, Http404
import uuid
from rest_framework import status, permissions
from pagination.pagination import Pagination
from permissions.permissions import IsAdminUser,IsSubscriberUser,IsAdminOrSubscriber
from pagination.pagination import Pagination
from dashboard.models import Dashboard
from dashboard.api.serializers import DashboardSerilizer,DashboardResponeSerilizer,UpdateDashboardSerilizer
from user.models import User
from file.models import File
class DashboardList(APIView):

    permission_classes = [IsAdminOrSubscriber]
    pagination_class = Pagination

    def post(self, request):

        serilizer= DashboardSerilizer(data=request.data)
        if serilizer.is_valid():

            data = serilizer.validated_data

            dashboard_count = Dashboard.objects.filter(created_by=data.get("created_by"),  title__isnull=False,is_deleted=False,is_sample=False).count()
            title = "Untitled "+str(dashboard_count)

            dashboard = Dashboard(  
                created_by = data.get("created_by"),
                file=get_object_or_404(File,uuid=data.get("file_uuid"),is_deleted=False),
                title=title,
            )
            print(model_to_dict(dashboard))
            dashboard.save()
            dash_board_serilizer = DashboardResponeSerilizer(dashboard)
            return Response(dash_board_serilizer.data,status=status.HTTP_200_OK)
        
        return Response(serilizer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
    def get(self, request, *args, **kwargs):

        title = request.query_params.get('title')
        dashboards = None
        
        if title :
            dashboards = Dashboard.objects.filter(
                title__icontains=title,
                is_deleted=False,
                is_sample=False
            ).order_by("-created_at")
        else:
            dashboards = Dashboard.objects.filter(
                is_deleted=False,
                is_sample=False
            ).order_by("-created_at")

        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(dashboards, request)
        serializer = DashboardResponeSerilizer(result_page, many=True)
        
        return paginator.get_paginated_response(serializer.data)


class DashboardUUID(APIView):

    def get_permissions(self):
        if self.request.method in ['GET']:
            return [permissions.AllowAny()]
        return [IsAdminOrSubscriber()]
    
    def put(self, request, *args, **kwargs):

        dashboard = get_object_or_404(Dashboard, uuid=kwargs.get('uuid'), is_deleted=False,is_sample=False)
       
        serilizer = UpdateDashboardSerilizer(
                dashboard, data=request.data
        )

        if serilizer.is_valid():
            serilizer.save()
            return Response(serilizer.data,status=status.HTTP_200_OK)
        
        return Response(serilizer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, *args, **kwargs):
        
        dashboard = get_object_or_404(Dashboard, uuid=kwargs.get('uuid'), is_deleted=False,is_sample=False)
        dashboard.is_deleted=True
        dashboard.save()
        
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, *args, **kwargs):
        
        dashboard = get_object_or_404(Dashboard, uuid=kwargs.get('uuid'), is_deleted=False,is_sample=False)

        serilizer = DashboardResponeSerilizer(dashboard)

        return Response(data=serilizer.data,status=status.HTTP_200_OK)
    

class DashboardIDApiView(APIView):

    permission_classes = [IsAdminUser]


    def put(self, request, *args, **kwargs):

        dashboard = get_object_or_404(Dashboard, id=kwargs.get('id'), is_deleted=False,is_sample=False)
       
        serilizer = UpdateDashboardSerilizer(
                dashboard, data=request.data
        )

        if serilizer.is_valid():
            serilizer.save()
            return Response(serilizer.data,status=status.HTTP_200_OK)
        
        return Response(serilizer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, *args, **kwargs):
        
        dashboard = get_object_or_404(Dashboard, id=kwargs.get('id'), is_deleted=False,is_sample=False)
        dashboard.is_deleted=True
        dashboard.save()
        
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, *args, **kwargs):
        
        dashboard = get_object_or_404(Dashboard, id=kwargs.get('id'), is_deleted=False,is_sample=False)

        serilizer = DashboardResponeSerilizer(dashboard)

        return Response(data=serilizer.data,status=status.HTTP_200_OK)

class DashboardUserUUID(APIView):

    pagination_class = Pagination

    def get(self, request, *args, **kwargs):
        
        user = get_object_or_404(User, uuid=kwargs.get('uuid'), is_deleted=False)

        title = request.query_params.get('title')
        dashboards = None
        
        if title :
            dashboards = Dashboard.objects.filter(
                title__icontains=title,
                created_by=user,
                is_deleted=False,
                is_sample=False
            ).order_by("-created_at")
        else:
            dashboards = Dashboard.objects.filter(
                created_by=user,
                is_deleted=False,
                is_sample=False
            ).order_by("-created_at")

        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(dashboards, request)
        serializer = DashboardResponeSerilizer(result_page, many=True)
        
        return paginator.get_paginated_response(serializer.data)