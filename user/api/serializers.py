from rest_framework import serializers
from user.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from role.models import Role
from user_role.models import UserRole

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename']  

class GroupRoleSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions']




class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = "__all__" 

class UserSerializer(serializers.ModelSerializer):
    
    roles = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = [
            'password',
            'verification_code',
            'is_active',
            'is_superuser',
            'is_staff',
            'date_joined',
            'last_login',
            'logged_in_at',
            'expired_at',
            'is_verified',
            "groups",
            "user_permissions"
        ]
    def get_roles(self, obj):
        # obj is the User instance
        user_roles = UserRole.objects.filter(user=obj)
        roles = [user_role.role for user_role in user_roles]
        return RoleSerializer(roles, many=True).data


PROCESS_CHOICES = [('1', '1'), ('2', '2')]

class CreateUserSerializer(serializers.ModelSerializer):

    roles = serializers.MultipleChoiceField(choices=[1, 2], required=True)

    
    class Meta:
        model = User
        exclude = [
            'verification_code',
            'is_deleted',
            'is_active',
            'is_superuser',
            'is_staff',
            'date_joined',
            'last_login',
            'created_at',
            'logged_in_at',
            'expired_at',
            'uuid',
        ]
    
    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError(
                self.default_error_messages)
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UpdateUserSerializer(serializers.ModelSerializer):


    class Meta:
        model = User
        exclude = [
            'verification_code',
            'is_active',
            'is_superuser',
            'is_staff',
            'date_joined',
            'last_login',
            'created_at',
            'logged_in_at',
            'expired_at',
            'uuid',
            "id",
            "email",
            "password",
        ]
    
