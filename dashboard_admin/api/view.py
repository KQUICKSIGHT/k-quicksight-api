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
from user.models import User
from dashboard.models import Dashboard
from file.models import File
from django.db.models import Count,Value
from django.db.models.functions import ExtractMonth,Coalesce
from django.forms.models import model_to_dict
from analysis.models import Analysis

class DashboardAdminApiView(APIView):
    permission_classes = [IsAdminUser]

    def get_monthly_data(self, model, all_months):

        
        MONTH_NAMES = {
            1: 'January',
            2: 'February',
            3: 'March',
            4: 'April',
            5: 'May',
            6: 'June',
            7: 'July',
            8: 'August',
            9: 'September',
            10: 'October',
            11: 'November',
            12: 'December'
        }
        result_queryset = model.objects \
            .annotate(month=ExtractMonth('created_at')) \
            .values('month') \
            .annotate(record_count=Coalesce(Count('id'), Value(0))) \
            .filter(month__in=all_months) \
            .order_by('month')

        result_dict = {entry['month']: entry['record_count'] for entry in result_queryset}

        final_result = [
            {
                'month_name': MONTH_NAMES[month],
                'record_count': result_dict.get(month, None)
            }
            for month in all_months
        ]

        return final_result

    def get(self, request):
        total_user = User.objects.filter(is_deleted=False).count()
        total_analysis = Analysis.objects.filter(is_deleted=False).count()
        total_dashboard = Dashboard.objects.filter(is_deleted=False).count()
        total_file = File.objects.filter(is_deleted=False).count()

        all_months = list(range(1, 13))

        activityy_dashboard = self.get_monthly_data(Dashboard, all_months)
        activityy_analysis = self.get_monthly_data(Analysis, all_months)
        acitvity_file = self.get_monthly_data(File, all_months)

        return Response({
            "total_userss": total_user,
            "total_dashboards": total_dashboard,
            "total_files": total_file,
            "total_analysis": total_analysis,
            "visualize_activity": activityy_dashboard,
            "analysis_activity": activityy_analysis,
            "file_activity": acitvity_file
        })