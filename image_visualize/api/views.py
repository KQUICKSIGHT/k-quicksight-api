from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.views import APIView
from django.core.exceptions import ValidationError

from django.shortcuts import get_object_or_404
from django.http import Http404

from rest_framework.parsers import FileUploadParser
from pagination.pagination import Pagination

from image_visualize.api.serializers import UploadImageVisualizeSerilizer
from django.contrib.auth.models import Group
import os
from django.forms.models import model_to_dict
from utils import file_util
from image_visualize.models import ImageVisualize
from user.models import User

class UploadImageVisualize(APIView):

    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):

        file_extension = file_util.get_file_extension(
            str(request.data['file'])
        )
        
        if file_extension not in file_util.ALLOWED_EXTENSIONS_IMAGE:
            return Response(f"Invalid file extension '{file_extension}'. Allowed extensions are: {', '.join(file_util.ALLOWED_EXTENSIONS_IMAGE)}.",
                            status=status.HTTP_400_BAD_REQUEST)

        data = file_util.handle_uploaded_file_image(request.data['file'])

        image_visualize = ImageVisualize(
            file = str(request.data['file']),
            filename = data["filename"],
            size = int(str(data["size"]).strip().replace("bytes","")),
            created_by = get_object_or_404(User,uuid=kwargs.get("uuid_created_by"),is_deleted=False)
        )

        image_visualize.save()
        serilizer = UploadImageVisualizeSerilizer(image_visualize)

        return Response(data=serilizer.data, status=status.HTTP_200_OK)

    pagination_class = Pagination

    def get(self, request, *args, **kwargs):

        created_by = get_object_or_404(User,uuid=kwargs.get("uuid_created_by"),is_deleted=False)

        image_visualize = ImageVisualize.objects.filter(created_by=created_by,is_deleted=False).order_by("-created_at")


        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(image_visualize, request)
        serializer = UploadImageVisualizeSerilizer(result_page, many=True)
            
        return paginator.get_paginated_response(serializer.data)



class ImageVisualizeDetailApiView(APIView):

    def get(self, request, *args, **kwargs):

        created_by = get_object_or_404(User,uuid=kwargs.get("uuid_created_by"),is_deleted=False)
        image_visualize = get_object_or_404(ImageVisualize,uuid=kwargs.get("uuid_image"),created_by=created_by)

        return Response(model_to_dict(image_visualize))

    def delete(self, request, *args, **kwargs):

        created_by = get_object_or_404(User,uuid=kwargs.get("uuid_created_by"),is_deleted=False)
        image_visualize = get_object_or_404(ImageVisualize,uuid=kwargs.get("uuid_image"),created_by=created_by)
        image_visualize.is_deleted=True
        image_visualize.save()
        return Response(status=status.HTTP_204_NO_CONTENT   )

