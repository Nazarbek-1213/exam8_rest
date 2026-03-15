from rest_framework import serializers
from .models import Project
from User.serializers import UserSerializer


class ProjectSerializer(serializers.ModelSerializer):
    client = UserSerializer(read_only=True)
    bid_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'description', 'budget', 'deadline',
            'status', 'client', 'bid_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'status', 'client', 'created_at', 'updated_at']

    def get_bid_count(self, obj):
        return obj.bids.count()


class ProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'budget', 'deadline', 'status', 'created_at']
        read_only_fields = ['id', 'status', 'created_at']

    def validate_budget(self, value):
        if value <= 0:
            raise serializers.ValidationError("Budget must be a positive number.")
        return value

    def validate_deadline(self, value):
        from django.utils import timezone
        if value < timezone.now().date():
            raise serializers.ValidationError("Deadline cannot be in the past.")
        return value

    def create(self, validated_data):
        validated_data['client'] = self.context['request'].user
        validated_data['status'] = 'open'
        return super().create(validated_data)


class ProjectUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['title', 'description', 'budget', 'deadline']

    def validate(self, attrs):
        if self.instance.status != 'open':
            raise serializers.ValidationError("Only open projects can be edited.")
        return attrs
