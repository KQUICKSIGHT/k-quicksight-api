from rest_framework import serializers
from user.models import User
from role.models import Role

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__" 