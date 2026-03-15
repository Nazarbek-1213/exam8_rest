from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Bid
from .serializers import BidSerializer, BidCreateSerializer, BidUpdateSerializer
from Project.models import Project
from Project.permissions import IsClient, IsFreelancer
from Contract.models import Contract


class BidCreateView(generics.CreateAPIView):
    serializer_class = BidCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsFreelancer]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        bid = serializer.save()
        return Response(BidSerializer(bid).data, status=status.HTTP_201_CREATED)


class BidListView(generics.ListAPIView):
    serializer_class = BidSerializer
    permission_classes = [permissions.IsAuthenticated, IsClient]

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        project = get_object_or_404(Project, pk=project_id, client=self.request.user)
        return Bid.objects.filter(project=project).select_related('freelancer', 'project')


class MyBidsView(generics.ListAPIView):
    serializer_class = BidSerializer
    permission_classes = [permissions.IsAuthenticated, IsFreelancer]

    def get_queryset(self):
        return Bid.objects.filter(freelancer=self.request.user).select_related('project', 'freelancer')


class BidDetailView(generics.RetrieveAPIView):
    serializer_class = BidSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'freelancer':
            return Bid.objects.filter(freelancer=user)
        return Bid.objects.filter(project__client=user)


class BidUpdateView(generics.UpdateAPIView):
    serializer_class = BidUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsFreelancer]

    def get_queryset(self):
        return Bid.objects.filter(freelancer=self.request.user)


class BidDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsFreelancer]

    def get_queryset(self):
        return Bid.objects.filter(freelancer=self.request.user, status='pending')

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status != 'pending':
            return Response({'error': 'Only pending bids can be deleted.'}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_destroy(instance)
        return Response({'message': 'Bid deleted successfully.'}, status=status.HTTP_200_OK)


class AcceptBidView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsClient]

    def post(self, request, bid_id):
        bid = get_object_or_404(Bid, pk=bid_id)

        if bid.project.client != request.user:
            return Response({'error': 'You are not the owner of this project.'}, status=status.HTTP_403_FORBIDDEN)

        if bid.project.status != 'open':
            return Response({'error': 'Project is not open for accepting bids.'}, status=status.HTTP_400_BAD_REQUEST)

        if bid.status != 'pending':
            return Response({'error': 'Only pending bids can be accepted.'}, status=status.HTTP_400_BAD_REQUEST)

        bid.status = 'accepted'
        bid.save()

        Bid.objects.filter(project=bid.project).exclude(pk=bid.pk).update(status='rejected')

        project = bid.project
        project.status = 'in_progress'
        project.save()

        contract = Contract.objects.create(
            project=project,
            client=request.user,
            freelancer=bid.freelancer,
            agreed_price=bid.price,
            status='active'
        )

        from Contract.serializers import ContractSerializer
        return Response({
            'message': 'Bid accepted successfully. Contract created.',
            'contract': ContractSerializer(contract).data
        }, status=status.HTTP_200_OK)