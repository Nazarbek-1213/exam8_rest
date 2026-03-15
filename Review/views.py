from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Review
from .serializers import ReviewSerializer, ReviewCreateSerializer
from Project.permissions import IsClient


class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsClient]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        review = serializer.save()
        return Response(ReviewSerializer(review).data, status=status.HTTP_201_CREATED)


class ReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        freelancer_id = self.kwargs.get('freelancer_id')
        if freelancer_id:
            return Review.objects.filter(freelancer_id=freelancer_id).select_related('reviewer', 'freelancer')
        return Review.objects.none()


class MyReviewsReceivedView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(freelancer=self.request.user).select_related('reviewer', 'freelancer')


class MyReviewsGivenView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsClient]

    def get_queryset(self):
        return Review.objects.filter(reviewer=self.request.user).select_related('reviewer', 'freelancer')


class ReviewDetailView(generics.RetrieveAPIView):
    queryset = Review.objects.select_related('reviewer', 'freelancer', 'contract')
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]