from rest_framework import serializers
from file.models import File
from sample.models import SampleAnalysis,SampleDashboard
from analysis.models import Analysis
from user.models import User
from analysis.api.serializers import AnalysisSerializer
from dashboard.api.serializers import DashboardResponeSerilizer

class SampleDashboardSerializer(serializers.ModelSerializer):

    class Meta:
        model = SampleDashboard
        fields = '__all__'

class ResponeSampleDashboardSerializer(serializers.ModelSerializer):

    dashboard_uuid = DashboardResponeSerilizer(read_only=True)
    
    class Meta:
        model = SampleDashboard
        fields = '__all__'


class SampleAnalysisSerializer(serializers.ModelSerializer):

    class Meta:
        model = SampleAnalysis
        fields = '__all__'

class ResponeSampleAnalysisSerializer(serializers.ModelSerializer):
    analysis_uuid = AnalysisSerializer(read_only=True)

    class Meta:
        model = SampleAnalysis
        fields = '__all__'


class FileSerializer(serializers.ModelSerializer):

    file = serializers.FileField()

    class Meta:
        fields = ['file']


class FileResponeSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = '__all__'

class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = '__all__'    

class UpdateFileSerializer(serializers.ModelSerializer):
    
    file = serializers.CharField(max_length=100,required=True)
    class Meta:
        model = File
        fields= ("file",)

class FileQuerySerializer(serializers.Serializer):
    
    filename = serializers.CharField(required=False, allow_blank=True)
    type = serializers.CharField(required=False, allow_blank=True)


class DynamicRecordSerializer(serializers.Serializer):
    # Example of a static field
    # id = serializers.IntegerField()

    # Generic field for dynamic data
    dynamic_data = serializers.SerializerMethodField()

    def get_dynamic_data(self, obj):
        # 'obj' is a dictionary representing a record from your dataset
        # You can transform or return it as is
        return obj