from rest_framework import serializers
from dashboard.models import Dashboard
from user.models import User
from django.shortcuts import get_object_or_404
from file.models import File



class DashboardSerilizer(serializers.ModelSerializer):
    
    file_uuid = serializers.UUIDField(required=True)
    class Meta:

        model = Dashboard
        exclude = ["id","file"]

class CreatedBySerilizer(serializers.ModelSerializer):
    
    class Meta:
        
        model= User
        fields= ["username","full_name","avatar","uuid","is_deleted"]

class FileResponeSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = '__all__'


class DashboardResponeSerilizer(serializers.ModelSerializer):

    created_by = serializers.SerializerMethodField()
    file = serializers.SerializerMethodField()
    
    class Meta:

        model = Dashboard
        fields = '__all__'

    def get_created_by(self, obj):

        user = obj.created_by
        serializer = CreatedBySerilizer(user)

        return serializer.data
    def get_file(self,obj):
        
        serializer = FileResponeSerializer(obj.file)

        return serializer.data    
class UpdateDashboardSerilizer(serializers.ModelSerializer):
        
    class Meta:

        model = Dashboard
        exclude = ["id","created_by","file"]