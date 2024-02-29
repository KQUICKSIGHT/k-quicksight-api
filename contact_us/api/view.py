from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from contact_us.models import ContactUs
from contact_us.api.serializers import CreateContactUsSerializer,ContactUsSerializer,UpdateContactUsSerializer
from utils import file_util
import pandas as pd
from pagination.pagination import Pagination
from django.shortcuts import get_object_or_404
from permissions.permissions import IsAdminUser,IsSubscriberUser


class ContatUsView(APIView):

    permission_classes = [permissions.AllowAny]
    pagination_class = Pagination
    
    def post(self, request):
        serializer = CreateContactUsSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
  
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):

        contact_us = ContactUs.objects.all()
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(contact_us, request)
        serializer = ContactUsSerializer(result_page, many=True)
        
        return paginator.get_paginated_response(serializer.data)

    
class ContactUsDetailView(APIView):

    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):

        contact_us = get_object_or_404(ContactUs, id=kwargs['pk'])
        contact_us_serilizer = ContactUsSerializer(contact_us)
        
        return Response(contact_us_serilizer.data, status=status.HTTP_200_OK)
        
    
    def put(self, request, *args, **kwargs):
        

        contact_us = get_object_or_404(ContactUs, id=kwargs['pk'])

        serilizer = UpdateContactUsSerializer(contact_us, data=request.data)
        
        if serilizer.is_valid():
        
            serilizer.save()
            return Response(serilizer.data, status=status.HTTP_200_OK)
        
        return Response(serilizer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    