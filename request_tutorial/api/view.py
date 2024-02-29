from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from request_tutorial.models import RequestTutorial
from request_tutorial.api.serializers import RequestTutorialSerializer, CreateRequestTutorialSerializer,UpdateRequestTutorialSerializer
from pagination.pagination import Pagination
from django.http import Http404
from django.shortcuts import get_object_or_404
from permissions.permissions import IsAdminUser, IsSubscriberUser,IsAdminOrSubscriber


class RequestTutorialView(APIView):

    pagination_class = Pagination
    # permission_classes = [IsAdminUser]
    def get_permissions(self):

        if self.request.method in ["GET"]:
            return [IsAdminUser()]
        return [IsAdminOrSubscriber()]

    def get(self, request, *args, **kwargs):

        subject = request.query_params.get("subject")

        requestTutorial= None
        if subject:
            requestTutorial = RequestTutorial.objects.filter(is_deleted=False,subject__icontains=subject,is_read=False)

        else:
            requestTutorial = RequestTutorial.objects.filter(is_deleted=False,is_read=False)

            

        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(requestTutorial, request)
        serializer = RequestTutorialSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)

    def post(self, request):

        serializer = CreateRequestTutorialSerializer(data=request.data)

        if serializer.is_valid():

            instance = serializer.save()
            response_serializer = RequestTutorialSerializer(instance)

            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestTutorialDetailView(APIView):

    permission_classes=[IsAdminUser]


    def get(self, request, *args, **kw):
        reuqest_tutorial = get_object_or_404(
            RequestTutorial, id=kw['pk'], is_deleted=False)
        reuqest_tutorial_serilizer = RequestTutorialSerializer(
            reuqest_tutorial)

        return Response(reuqest_tutorial_serilizer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kw):

        reuqest_tutorial = get_object_or_404(
            RequestTutorial, id=kw['pk'], is_deleted=False)
        serializer = UpdateRequestTutorialSerializer(reuqest_tutorial,data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, *args, **kw):

        reuqest_tutorial = get_object_or_404(
            RequestTutorial, id=kw['pk'], is_deleted=False)

        reuqest_tutorial.is_deleted = True

        reuqest_tutorial.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
