from rest_framework import serializers
from .models import Review
from User.serializers import UserSerializer


class ReviewSerializer(serializers.ModelSerializer):
    reviewer = UserSerializer(read_only=True)
    freelancer = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'contract', 'reviewer', 'freelancer', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'reviewer', 'freelancer', 'created_at']


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'contract', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_rating(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def validate_contract(self, value):
        request = self.context['request']


        if value.client != request.user:
            raise serializers.ValidationError("You are not the client of this contract.")


        if value.status != 'finished':
            raise serializers.ValidationError("You can only review a finished contract.")


        if hasattr(value, 'review'):
            raise serializers.ValidationError("You have already reviewed this contract.")

        return value

    def create(self, validated_data):
        request = self.context['request']
        contract = validated_data['contract']
        validated_data['reviewer'] = request.user
        validated_data['freelancer'] = contract.freelancer
        return super().create(validated_data)
