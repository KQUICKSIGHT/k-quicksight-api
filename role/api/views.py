from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.views import APIView
from django.core.exceptions import ValidationError

from django.shortcuts import get_object_or_404
from role.api.serializers import RoleSerializer
import os
from permissions.permissions import IsAdminUser, IsSubscriberUser


from role.models import Role

class RoleView(APIView):
    permission_classes=[IsAdminUser]
    def get(self, request):
        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)  # Ensure many=True is set here
        return Response(serializer.data, status=status.HTTP_200_OK)

        