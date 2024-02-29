from rest_framework import serializers
from tutorial.models import Tutorial
from user.api.serializers import UserSerializer


class TutorialSerializer(serializers.ModelSerializer):
   
   published_by  = UserSerializer(read_only=True)

   class Meta:
        model = Tutorial
        fields = '__all__'  # Include all fields


class CreateTutorialSerializer(serializers.ModelSerializer):

    class Meta:
    
        model = Tutorial
        fields = '__all__'  # Include all fields
        read_only_fields = ('id', 'uuid', 'created_at', 'updated_at')  # Make these fields read-only