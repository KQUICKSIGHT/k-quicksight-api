from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from analysis.models import Analysis
from django.forms.models import model_to_dict

from analysis.api.serializers import AnalysisSerializer,ExploratoryDataAnalysisSerializer,PerformAnalysisSerializer,AnalysisUpdateSerializer
from file.models import File
from analysis.api.service.descriptive import (exploratory_data_analysis,perform_analysis,recommendation)
from pagination.pagination import Pagination
from django.shortcuts import get_object_or_404
from permissions.permissions import IsAdminUser,IsSubscriberUser,IsAdminOrSubscriber
from rest_framework import status, permissions


class RecommnedationApiView(APIView):

    def post(self, request, *args, **kwargs):
        
        analysis = get_object_or_404(Analysis,is_deleted=False,is_sample=False,uuid=kwargs.get('uuid_analysis'))
        
        recommended = recommendation(
            model_name=analysis.model_name,
            filename=analysis.filename,
            results=analysis.analysis_data
        )

        if recommended:
            
            analysis.recommneded= recommended
            analysis.save()

        return Response({"result":recommended})

class AnalysisApiView(APIView):

    def post(self, request):

        serilizer = AnalysisSerializer(data=request.data)

        if serilizer.is_valid():

            file = serilizer.validated_data.get("file")
            filename = file.filename
            variable_one = str(serilizer.validated_data.get("variable_one"))
            variable_two = str(serilizer.validated_data.get("variable_two"))
            model_name = serilizer.validated_data.get("model_name")
            user = serilizer.validated_data.get("user")
            data = perform_analysis(
                filename=filename,
                degree=2,
                predict_values=200,
                dependent_variable=variable_two,
                multiple_variables=variable_one,
                independent_variable=variable_one,
                model_name=model_name
            )
            analysis_model = serilizer.save()
            print(model_to_dict(analysis_model))
            return Response(data=data, status=status.HTTP_200_OK)

        return Response(serilizer.errors, status=status.HTTP_400_BAD_REQUEST)

class ExploratoryDataAnalysis(APIView):

    def post(self, request, *args, **kwargs):

        serilizer = ExploratoryDataAnalysisSerializer(data=request.data)

        if serilizer.is_valid():

            filename = serilizer.validated_data.get("filename")
            visualize = serilizer.validated_data.get("visualizes")
            independent = serilizer.validated_data.get("independent_variable")
            dependent = serilizer.validated_data.get("dependent_variable")
            resuult = exploratory_data_analysis(filename,visualize,independent,dependent)

            return Response(resuult)
        return Response(serilizer.errors,status=status.HTTP_400_BAD_REQUEST)


class PerformAnalysisView(APIView):

    pagination_class = Pagination

    def get(self, request, *args, **kwargs):
        
        title = request.query_params.get('title')
        if title : 
            analysis = Analysis.objects.filter(
                is_deleted=False,
                title__icontains=title,
                is_sample=False
            ).order_by("-created_at")
        else :
            analysis = Analysis.objects.filter(
                is_deleted=False,
                is_sample=False
            ).order_by("-created_at")

        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(analysis, request)
        serializer = AnalysisSerializer(result_page, many=True)
        
        return paginator.get_paginated_response(serializer.data)
    

    def post(self, request, *args, **kwargs):

        serializer = PerformAnalysisSerializer(data=request.data)
        if serializer.is_valid():

            data = serializer.validated_data
            model_name = data['model_name']
            indepeden_vairable=None
        
            if model_name != "multiple_linear_regression" and model_name != "two_way_anova" and model_name != "two_sample_t_test":
                indepeden_vairable = data.get('independent_variable')
            else:
                indepeden_vairable = data.get('independent_variables')

            list_range_numeric = serializer.validated_data.get("list_range_numeric")

            hypothesis_mean_column= data.get("hypothesis_mean_column")
            sample_mean = data.get("sample_mean")
            list_paired_samples = data.get("list_paired_samples")

            number_of_day_to_forecast = data.get("number_of_day_to_forecast")
            column_date = data.get("column_date")
            number_column = data.get("number_column")

            response_data = perform_analysis(
                filename=data['filename'],
                model_name=model_name,
                independent_variable=indepeden_vairable,
                dependent_variable=data.get('dependent_variable'),
                list_range_numeric=list_range_numeric,
                hypothesis_mean_column= hypothesis_mean_column,
                sample_mean=sample_mean,
                list_paired_samples=list_paired_samples,
                number_of_day_to_forecast=number_of_day_to_forecast,
                column_date=column_date,
                number_column=number_column
            )
            
            user = request.data["user"]
            
            if response_data != None:
                analysis_count = Analysis.objects.filter(user=request.data["user"],  title__isnull=False,is_deleted=False,is_sample=False).count()
                title = "Untitled "+str(analysis_count)


                analysis_instance = Analysis(
                    model_name=model_name,
                    analysis_data=response_data,
                    user_id=user,
                    title=title,
                    dependent_variable=data.get('dependent_variable'),
                    independent_variable=str(indepeden_vairable),
                    filename=data['filename']
                )                
                analysis_instance.save()
                return Response({"model_name":model_name,model_name:response_data,"uuid":analysis_instance.uuid}, status=status.HTTP_200_OK)
            else:
                return Response({"message":"Something went wrong please try again"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class AnalysisListView(APIView):
    pagination_class = Pagination

    def get(self, request, *args, **kwargs):
        
        title = request.query_params.get('title')
        if title:
            analysis = Analysis.objects.filter(
                is_deleted=False,
                user=kwargs.get('user'),
                title__icontains=title,
                is_sample=False
            ).order_by("-created_at")
        else:
            analysis = Analysis.objects.filter(
                is_deleted=False,
                user=kwargs.get('user'),
                is_sample=False
            ).order_by("-created_at")
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(analysis, request)
        serializer = AnalysisSerializer(result_page, many=True)
        
        return paginator.get_paginated_response(serializer.data)
    

class AnalysisDetailView(APIView):

    def get_permissions(self):
        if self.request.method in ['GET']:
            return [permissions.AllowAny()]
        return [IsAdminOrSubscriber()]

    def get(self, request, *args, **kwargs):

        analysis = get_object_or_404(Analysis, uuid=kwargs.get('uuid'),is_deleted=False,is_sample=False)
        serializer = AnalysisSerializer(analysis)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def delete(self,request,*args,**kwargs):
        
        analysis = get_object_or_404(Analysis, uuid=kwargs.get('uuid'),is_deleted=False,is_sample=False)
        analysis.is_deleted=True
        analysis.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def put(self,request,*args,**kwargs):
        
        analysis = get_object_or_404(Analysis, uuid=kwargs.get('uuid'),is_deleted=False,is_sample=False)
        serilizer = AnalysisUpdateSerializer(analysis,data=request.data)
        if serilizer.is_valid():
            serilizer.save()
            return Response(serilizer.data,status=status.HTTP_200_OK)
        return Response(serilizer.errors,status=status.HTTP_400_BAD_REQUEST)        

class AnalysisDetailByIdApiView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):

        analysis = get_object_or_404(Analysis, id=kwargs.get('id'),is_deleted=False,is_sample=False)
        serializer = AnalysisSerializer(analysis)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def delete(self,request,*args,**kwargs):
        
        analysis = get_object_or_404(Analysis, id=kwargs.get('id'),is_deleted=False,is_sample=False)
        analysis.is_deleted=True
        analysis.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def put(self,request,*args,**kwargs):
        
        analysis = get_object_or_404(Analysis, id=kwargs.get('id'),is_deleted=False,is_sample=False)
        serilizer = AnalysisUpdateSerializer(analysis,data=request.data)
        if serilizer.is_valid():
            serilizer.save()
            return Response(serilizer.data,status=status.HTTP_200_OK)
        return Response(serilizer.errors,status=status.HTTP_400_BAD_REQUEST)   

