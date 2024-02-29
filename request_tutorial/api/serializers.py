from rest_framework import serializers
from request_tutorial.models import RequestTutorial
from user.api.serializers import UserSerializer


class RequestTutorialSerializer(serializers.ModelSerializer):
   
   request_by  = UserSerializer(read_only=True)

   class Meta:
        
        model = RequestTutorial
        fields = '__all__' 


class CreateRequestTutorialSerializer(serializers.ModelSerializer):

    class Meta:
    
        model = RequestTutorial
        fields = '__all__' 
        read_only_fields = ('id', 'uuid', 'created_at')  

class UpdateRequestTutorialSerializer(serializers.ModelSerializer):

    class Meta:
        model = RequestTutorial
        fields = ["is_read"] 