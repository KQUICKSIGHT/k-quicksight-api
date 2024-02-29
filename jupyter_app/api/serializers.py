from rest_framework import serializers
from request_tutorial.models import RequestTutorial
from jupyter_app.models import JupyterDocument

class JupyterSerializer(serializers.ModelSerializer):
   

   class Meta:
        
        model = JupyterDocument
        exclude = ["created_by"]
