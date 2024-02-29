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
from share_analysis.api.serializers import ShareAnalysis,AnalysisResponeSerializer,UserAnalysisShareSerializer,SharedAnalysisSerializer,SharedAnalysisResponeSerializer
from user.models import User
from django.forms.models import model_to_dict
from account.api.utils import Util
from share_member.api.utils import get_email_body_analysis
from share_member.models import UserFileShare
from django.shortcuts import redirect


class ShareFileMemberView(APIView):

    def post(self, request, *args, **kwargs):

        serializer = SharedAnalysisSerializer(data=request.data)

        if serializer.is_valid():

            members = serializer.validated_data.get("members")
            analysis = serializer.validated_data.get("analysis")
            exits_user = []
            new_user = []

            for member in members:

                isExists = ShareAnalysis.objects.filter(
                    member=member, analysis=analysis
                ).exists()

                if not isExists:

                    user_file_share = ShareAnalysis(member=member, analysis=analysis)
                    user_file_share.save()
                    uuid = user_file_share.uuid

                    email_body = get_email_body_analysis(
                        member_username=member.username,
                        owner_email=analysis.user.email,
                        uuid=uuid,
                        owner_name=analysis.user.username,
                        text="Analysis"
                    )

                    data = {'email_body': email_body, 'to_email': member.email,
                            'email_subject': 'You have been added to a Analysis Share'}
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

from django.http import HttpResponse

class VerifyAddMember(APIView):

    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):

        uuid = kwargs["uuid"]
        status = kwargs["status"]

        try:
            user_file_share = ShareAnalysis.objects.get(
                uuid=uuid, status="pending")
            print(status)
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
            return HttpResponse("<h1>Something went wrong.</h1>")
        except ShareAnalysis.DoesNotExist:
            return HttpResponse("<h1>It Someting went wrong.</h1>")
        except Exception as e :
            return HttpResponse("<h1>You might be already accepted or rejected.</h1>")
from analysis.models import Analysis

class UserFileShareListView(APIView):

    def get(self, request, *args, **kwargs):

        file_id = kwargs["file_id"]

        if ShareAnalysis.objects.filter(analysis_id=file_id, status="accepted", is_deleted=False).exists():
            userfiles = ShareAnalysis.objects.filter(
                analysis_id=file_id, status="accepted", is_deleted=False
            )
            list_members = []
            for userfile in userfiles:
                data = {
                    "username": userfile.member.username,
                    "shared_at": userfile.shared_at,
                }
                list_members.append(data)

            file = Analysis.objects.get(id=file_id)
            file_serilizer = AnalysisResponeSerializer(file)

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

        if Analysis.objects.filter(user=user_id, is_deleted=False).exists():

            files = Analysis.objects.filter(user=user_id, is_deleted=False)
            messages = []
            for file in files:
                if ShareAnalysis.objects.filter(analysis_id=file.id, status="accepted", is_deleted=False).exists():
                    userfiles = ShareAnalysis.objects.filter(
                        analysis_id=file.id, status="accepted", is_deleted=False
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
                    file_serilizer = AnalysisResponeSerializer(file)

                    message = {
                        "analysis": file_serilizer.data,
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
        shares = ShareAnalysis.objects.filter(member_id=member_id,status="accepted",is_deleted=False)
        serializer = SharedAnalysisResponeSerializer(shares, many=True)
        return Response(serializer.data)
                
