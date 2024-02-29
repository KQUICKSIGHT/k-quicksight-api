from rest_framework import serializers
from user.models import User
from share_dashboard.models import ShareDashboard
from dashboard.models import Dashboard

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username","avatar"]


class DashboardResponeSerializer(serializers.ModelSerializer):
    
    created_by =UserSerializer(read_only=True)

    class Meta:
        model = Dashboard
        fields = '__all__'


class SharedDashboardResponeSerializer(serializers.ModelSerializer):

    dashboard = DashboardResponeSerializer(read_only=True)
    member = UserSerializer(read_only=True)

    class Meta:
        model = ShareDashboard
        exclude = ["id"]


class SharedDashboardSerializer(serializers.ModelSerializer):

    members = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all(), write_only=True
    )

    class Meta:
        model = ShareDashboard
        fields = ['members', 'dashboard']  # 'members' is used for input

    def create(self, validated_data):
        members = validated_data.pop('members')
        file = validated_data.get('dashboard')
        user_file_shares = []

        for member in members:
            # Check if the UserFileShare instance already exists
            user_file_share, created = ShareDashboard.objects.get_or_create(
                member=member, dashboard=file
            )
            if created:
                user_file_shares.append(user_file_share)

        return user_file_shares
    

class UserDashboardShareSerializer(serializers.ModelSerializer):
    analysis = DashboardResponeSerializer(read_only=True)
    member = UserSerializer(read_only=True)
    class Meta:
        model = ShareDashboard
        fields = '__all__'  # You can specify individual fields here if needed