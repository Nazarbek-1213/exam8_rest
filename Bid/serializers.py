from rest_framework import serializers
from .models import Bid
from User.serializers import UserSerializer
from Project.serializers import ProjectSerializer


class BidSerializer(serializers.ModelSerializer):
    freelancer = UserSerializer(read_only=True)
    project = ProjectSerializer(read_only=True)

    class Meta:
        model = Bid
        fields = ['id', 'project', 'freelancer', 'price', 'message', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'status', 'created_at', 'updated_at']


class BidCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = ['id', 'project', 'price', 'message', 'status', 'created_at']
        read_only_fields = ['id', 'status', 'created_at']

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be positive.")
        return value

    def validate(self, attrs):
        request = self.context['request']
        project = attrs['project']


        if project.status != 'open':
            raise serializers.ValidationError("You can only bid on open projects.")


        if project.client == request.user:
            raise serializers.ValidationError("You cannot bid on your own project.")


        if Bid.objects.filter(project=project, freelancer=request.user).exists():
            raise serializers.ValidationError("You have already placed a bid on this project.")

        return attrs

    def create(self, validated_data):
        validated_data['freelancer'] = self.context['request'].user
        return super().create(validated_data)


class BidUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = ['price', 'message']

    def validate(self, attrs):
        if self.instance.status != 'pending':
            raise serializers.ValidationError("Only pending bids can be edited.")
        if self.instance.project.status != 'open':
            raise serializers.ValidationError("Cannot edit bid on a non-open project.")
        return attrs




