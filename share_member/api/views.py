from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser


from django.http import FileResponse
from django.shortcuts import render


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

from rest_framework import status, permissions
from share_member.models import UserFileShare
from share_member.api.serializers import SharedFileSerializer, SharedFileResponeSerializer, UserSerializer, FileResponeSerializer,UserFileShareSerializer
from user.models import User
from django.forms.models import model_to_dict
from account.api.utils import Util
from share_member.api.utils import get_email_body_dataset
from share_member.models import UserFileShare
from django.shortcuts import redirect


class ShareFileMemberView(APIView):

    def post(self, request, *args, **kwargs):

        serializer = SharedFileSerializer(data=request.data)

        if serializer.is_valid():

            members = serializer.validated_data.get("members")
            file = serializer.validated_data.get("file")
            exits_user = []
            new_user = []

            for member in members:

                isExists = UserFileShare.objects.filter(
                    member=member, file=file
                ).exists()

                if not isExists:

                    user_file_share = UserFileShare(member=member, file=file)
                    user_file_share.save()
                    uuid = user_file_share.uuid

                    email_body = get_email_body_dataset(
                        member_username=member.username,
                        owner_email=file.created_by.email,
                        uuid=uuid,
                        owner_name=file.created_by.username
                    )

                    data = {'email_body': email_body, 'to_email': member.email,
                            'email_subject': 'You have been added to a File Share'}
                    Util.send_email(data)
                    new_user.append(member.username)

                else:

                    exits_user.append(member.username)

            messages = None
            if exits_user and new_user:
                messages = {
                    "code":201,
                    "message": "You have been addeed "+str(new_user).replace("[", "").replace("]", "") + " and "+str(exits_user).replace("[", "").replace("]", "")+" already added."
                }
            elif exits_user:
                messages = {
                    "code":400,
                    "message": str(exits_user).replace("[", "").replace("]", "")+" already added."
                }
                return Response(messages, status=status.HTTP_400_BAD_REQUEST)

            elif new_user:
                messages = {
                    "code":201,
                    "message": str(new_user).replace("[", "").replace("]", "")+" has been added."
                }
            return Response(messages, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyAddMember(APIView):

    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):

        uuid = kwargs["uuid"]
        status = kwargs["status"]

        try:

            user_file_share = UserFileShare.objects.get(
                uuid=uuid, status="pending")

            if status == "accepted":
                user_file_share.status = "accepted"
                user_file_share.save()
                return redirect("https://photostad-api.istad.co/templates/accepted/")

            elif status == "rejected":
                user_file_share.status = "rejected"
                user_file_share.save()
                return redirect("https://photostad-api.istad.co/templates/rejected/")
            else:
                user_file_share.status = "pending"
            user_file_share.save()
            return redirect("https://photostad-api.istad.co/templates/not-found/")
        except UserFileShare.DoesNotExist:
            return redirect("https://istad.co/")


class UserFileShareListView(APIView):

    def get(self, request, *args, **kwargs):

        file_id = kwargs["file_id"]

        if UserFileShare.objects.filter(file_id=file_id, status="accepted", is_deleted=False).exists():
            userfiles = UserFileShare.objects.filter(
                file_id=file_id, status="accepted", is_deleted=False
            )
            list_members = []
            for userfile in userfiles:
                data = {
                    "username": userfile.member.username,
                    "shared_at": userfile.shared_at,
                }
                list_members.append(data)

            file = File.objects.get(id=file_id)
            file_serilizer = FileResponeSerializer(file)

            message = {
                "file": file_serilizer.data,
                "members": list_members,
                "status": "accepted",
                "is_deleted": False,
            }
            return Response(message, status=status.HTTP_200_OK)
        else:
            return Response({"message": "not found"}, status=status.HTTP_404_NOT_FOUND)


class ShareFileViewByIdView(APIView):

    def get(self, request, *args, **kwargs):

        user_id = kwargs.pop('user_id')
        if File.objects.filter(created_by=user_id, is_deleted=False).exists():

            files = File.objects.filter(created_by=user_id, is_deleted=False)
            messages = []
            for file in files:
                if UserFileShare.objects.filter(file_id=file.id, status="accepted", is_deleted=False).exists():
                    userfiles = UserFileShare.objects.filter(
                        file_id=file.id, status="accepted", is_deleted=False
                    )
                    list_members = []
                    for userfile in userfiles:
                        data = {
                            "username": userfile.member.username,
                            "avatar": userfile.member.avatar,
                            "shared_at": userfile.shared_at,
                        }
                        list_members.append(data)
                    # file
                    file_serilizer = FileResponeSerializer(file)

                    message = {
                        "file": file_serilizer.data,
                        "members": list_members,
                        "status": "accepted",
                        "is_deleted": False,
                    }
                    messages.append(message)
            return Response(messages)
        return Response({"message": "not found"}, status=status.HTTP_404_NOT_FOUND)


class SharedFileMemberView(APIView):

    def get(self, request, *args, **kwargs):
        member_id = kwargs.pop("user_id", None)
        shares = UserFileShare.objects.filter(member__id=member_id,status="accepted",is_deleted=False)
        serializer = UserFileShareSerializer(shares, many=True)
        return Response(serializer.data)
                
        # if UserFileShare.objects.filter(member_id=member_id,is_deleted=False,status="accepted").exists():
            
        #     members = UserFileShare.objects.filter(member_id=member_id,is_deleted=False,status="accepted").all()
            
        #     return Response(None)
        #     if serilizer.is_valid():
        #         return Response(serilizer.data,status=status.HTTP_200_OK)
        #     return Response(serilizer.errors,status=status.HTTP_400_BAD_REQUEST)
        # return Response({"message":"not found"},status=status.HTTP_404_NOT_FOUND)