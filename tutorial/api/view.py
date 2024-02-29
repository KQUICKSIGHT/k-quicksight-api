from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework import status
from tutorial.models import Tutorial
from tutorial.api.serializers import TutorialSerializer, CreateTutorialSerializer
from pagination.pagination import Pagination
from django.http import Http404
from django.shortcuts import get_object_or_404
from permissions.permissions import IsAdminUser, IsSubscriberUser, IsAdminOrSubscriber


class TutorialView(APIView):

    pagination_class = Pagination

    def get_permissions(self):
        if self.request.method in ['POST']:
            return [IsSubscriberUser(), IsAdminUser()]
        return [permissions.AllowAny()]

    def get(self, request, *args, **kwargs):

        title = request.query_params.get('title')
        tutorials = None

        if title:
            tutorials = Tutorial.objects.filter(
                title__icontains=title, is_deleted=False
            ).order_by('updated_at')

        else:
            tutorials = Tutorial.objects.filter(
                is_deleted=False
            ).order_by('updated_at')

        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(tutorials, request)
        serializer = TutorialSerializer(result_page, many=True)
        
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, *args, **kwargs):

        serializer = CreateTutorialSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TutorialDetailView(APIView):

    permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            return [IsAdminUser()]
        return [permissions.AllowAny()]

    def get(self, request, *args, **kw):

        tutorial = get_object_or_404(Tutorial, id=kw['pk'], is_deleted=False)
        serializer = TutorialSerializer(tutorial)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kw):

        tutorial = get_object_or_404(Tutorial, id=kw['pk'], is_deleted=False)
        serializer = CreateTutorialSerializer(tutorial, data=request.data)

        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):

        tutorial = get_object_or_404(
            Tutorial, id=kwargs['pk'], is_deleted=False)
        tutorial.is_deleted = True
        tutorial.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

class TutorialUUIDDetailView(APIView):

    permission_classes = [permissions.AllowAny]


    def get(self, request, *args, **kwargs):

        tutorial = get_object_or_404(Tutorial, uuid=kwargs['uuid'], is_deleted=False)
        tutorial.view =tutorial.view + 1
        tutorial.save()
        serializer = TutorialSerializer(tutorial)

        return Response(serializer.data, status=status.HTTP_200_OK)
