from rest_framework import serializers
from file.models import File
from contact_us.models import ContactUs


class CreateContactUsSerializer(serializers.ModelSerializer):

    class Meta:
        model= ContactUs
        exclude = [
            'id',
            'created_at',
            'is_read'
            ]
        
class ContactUsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model= ContactUs
        fields = '__all__'    

class UpdateContactUsSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = ContactUs
        fields = ['is_read']

