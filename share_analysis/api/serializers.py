from rest_framework import serializers
from share_member.models import UserFileShare
from user.models import User
from file.models import File
from analysis.models import Analysis
from share_analysis.models import ShareAnalysis

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username","avatar"]


class AnalysisResponeSerializer(serializers.ModelSerializer):
    user =UserSerializer(read_only=True)
    class Meta:
        model = Analysis
        fields = '__all__'


class SharedAnalysisResponeSerializer(serializers.ModelSerializer):

    analysis = AnalysisResponeSerializer(read_only=True)
    member = UserSerializer(read_only=True)

    class Meta:
        model = ShareAnalysis
        exclude = ["id"]


class SharedAnalysisSerializer(serializers.ModelSerializer):

    members = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all(), write_only=True
    )

    class Meta:
        model = ShareAnalysis
        fields = ['members', 'analysis']  # 'members' is used for input

    def create(self, validated_data):
        members = validated_data.pop('members')
        file = validated_data.get('file')
        user_file_shares = []

        for member in members:
            # Check if the UserFileShare instance already exists
            user_file_share, created = UserFileShare.objects.get_or_create(
                member=member, file=file
            )
            if created:
                user_file_shares.append(user_file_share)

        return user_file_shares
    

class UserAnalysisShareSerializer(serializers.ModelSerializer):
    analysis = AnalysisResponeSerializer(read_only=True)
    member = UserSerializer(read_only=True)
    class Meta:
        model = ShareAnalysis
        fields = '__all__'  # You can specify individual fields here if needed