from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.views import APIView
from django.core.exceptions import ValidationError

from django.shortcuts import get_object_or_404
from role.api.serializers import RoleSerializer
import os

from user_role.models import UserRole

class UserRoleView(APIView):

    def get(self, request):

        roles = UserRole.objects.all()
        
        serilizer = RoleSerializer(roles)

        if serilizer.is_valid():
            return Response(serilizer.data,status=status.HTTP_200_OK)
        return Response(serilizer.errors,status=status.HTTP_400_BAD_REQUEST)
        