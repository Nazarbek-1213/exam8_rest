from rest_framework import serializers
from .models import Contract
from User.serializers import UserSerializer
from Project.serializers import ProjectSerializer


class ContractSerializer(serializers.ModelSerializer):
    client = UserSerializer(read_only=True)
    freelancer = UserSerializer(read_only=True)
    project = ProjectSerializer(read_only=True)

    class Meta:
        model = Contract
        fields = [
            'id', 'project', 'client', 'freelancer',
            'agreed_price', 'status', 'created_at', 'finished_at'
        ]
        read_only_fields = ['id', 'project', 'client', 'freelancer', 'agreed_price', 'created_at', 'finished_at']


