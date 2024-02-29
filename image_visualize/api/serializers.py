from rest_framework import serializers
from file.models import File
from user.models import User
from image_visualize.models import ImageVisualize

import os
import uuid
from dotenv import load_dotenv

dotenv_path_dev = '.env'
load_dotenv(dotenv_path=dotenv_path_dev)
file_base_url = os.getenv("BASE_URL_FILE")

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields=["username","uuid","full_name","avatar"]




class UploadImageVisualizeSerilizer(serializers.ModelSerializer):

    img = serializers.SerializerMethodField()

    class Meta:
        model = ImageVisualize
        exclude = ['id',"file","is_deleted","size","created_at","filename","created_by"]
    
    def get_img(self, obj):
        filename = obj.filename if obj.filename else None
        return file_base_url + filename+"/"