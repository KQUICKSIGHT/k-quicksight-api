from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.views import APIView
from django.core.exceptions import ValidationError

from django.shortcuts import get_object_or_404
from django.http import Http404


from user.models import User
from pagination.pagination import Pagination
from role.models import Role
from user_role.models import UserRole
from user.api.serializers import UserSerializer, CreateUserSerializer, UpdateUserSerializer, GroupRoleSerializer
from account.api.renderers import UserRenderer
from django.contrib.auth.models import Group
import os
from django.forms.models import model_to_dict

from permissions.permissions import IsAdminUser,IsSubscriberUser,IsAdminOrSubscriber
class GroupsRoleView(APIView):

    def get(self, request):

        groups = Group.objects.all()
        serializer = GroupRoleSerializer(groups, many=True)  # Corrected line
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserListView(APIView):

    renderer_classes = (UserRenderer,)
    permission_classes = [IsAdminUser]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAdminOrSubscriber()]
        elif self.request.method == 'POST':
            return [IsAdminUser()]
    
    def get(self, request, *args, **kwargs):

        username = request.query_params.get('username')
        users = None
        if username:
            users = User.objects.filter(
                username__icontains=username,
                is_deleted=False
            )

        else:
            users = User.objects.filter(is_deleted=False)
        
        serializer = UserSerializer(users, many=True)

        data = {
            "count": len(users),
            "data": serializer.data  # Use .data to get the serialized data
        }
        return Response(data=data, status=status.HTTP_200_OK)
    

    def post(self, request, *args, **kwargs):

        user_data = request.data
        user_data['is_verified'] = True
        serializer = CreateUserSerializer(data=user_data)
        
        
        if serializer.is_valid():
            roles = serializer.validated_data.pop('roles', None)
            user = serializer.save()            
            if roles:
                for role in roles:
                    role_instance = Role.objects.get(id=role)
                    user_role = UserRole()
                    user_role.user = user  # Assuming 'user' is an instance of the User model
                    user_role.role = role_instance  # Assuming 'role_instance' is an instance of the Role model
                    user_role.save()
                    user_data.pop('password', None)
                return Response(user_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):

    permission_classes = [IsAdminUser]
    def get_permissions(self):
        print(self)
        if self.request.method == 'delete':
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [IsAdminOrSubscriber]
        return [permission() for permission in permission_classes]

    def get(self, request, *args, **kwargs):

        user = get_object_or_404(User, pk=kwargs['pk'])
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kw):

        user = get_object_or_404(User, id=kw['pk'], is_deleted=False)

        user.is_deleted = True
        user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, *args, **kw):

        user = get_object_or_404(User, id=kw['pk'], is_deleted=False)

        serializer = UpdateUserSerializer(user, data=request.data)

        if serializer.is_valid():

            serializer.save()

            response_serializer = UserSerializer(user)

            return Response(response_serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailUUIDView(APIView):

    permission_classes = [IsAdminOrSubscriber]

    def get(self, request, *args, **kw):
        try:

            user = get_object_or_404(User, uuid=kw['uuid'], is_deleted=False)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ValidationError:

            raise Http404("No User matches the given query.")


    def put(self, request, *args, **kw):

        try:
            user = get_object_or_404(User, uuid=kw['uuid'], is_deleted=False)

            serializer = UpdateUserSerializer(
                user, data=request.data
            )

            if serializer.is_valid():
                serializer.save()

                response_data = serializer.data

                return Response(response_data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except ValidationError:

            raise Http404("No User matches the given query.")


class UserDetailEmailView(APIView):

    permission_classes = [permissions.AllowAny]
    def get(self, request, *args, **kw):

        user = get_object_or_404(User, email=kw['email'])
        userSerializer = UserSerializer(user)
        return Response(userSerializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kw):

        user = get_object_or_404(User, email=kw['email'])
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListUsersView(APIView):
    pagination_class = Pagination
    
    def get(self, request, *args, **kwargs):

        username = request.query_params.get('username')
        users = None
        
        if username :
            users = User.objects.filter(
                username__icontains=username,
                is_deleted=False,
            ).order_by("-created_at")
        else:
            users = User.objects.filter(
                is_deleted=False,
            ).order_by("-created_at")

        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(users, request)
        serializer = UserSerializer(result_page, many=True)
        
        return paginator.get_paginated_response(serializer.data)
