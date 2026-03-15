from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Contract
from .serializers import ContractSerializer
from Project.permissions import IsClient


class ContractListView(generics.ListAPIView):
    serializer_class = ContractSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'client':
            return Contract.objects.filter(client=user).select_related('project', 'client', 'freelancer')
        return Contract.objects.filter(freelancer=user).select_related('project', 'client', 'freelancer')


class ContractDetailView(generics.RetrieveAPIView):
    serializer_class = ContractSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Contract.objects.filter(client=user) | Contract.objects.filter(freelancer=user)


class ContractFinishView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsClient]

    def post(self, request, pk):
        contract = get_object_or_404(Contract, pk=pk, client=request.user)

        if contract.status != 'active':
            return Response({'error': 'Only active contracts can be finished.'},
                            status=status.HTTP_400_BAD_REQUEST)

        contract.status = 'finished'
        contract.finished_at = timezone.now()
        contract.save()

        contract.project.status = 'completed'
        contract.project.save()

        return Response({
            'message': 'Contract finished successfully. Project marked as completed.',
            'contract': ContractSerializer(contract).data
        }, status=status.HTTP_200_OK)


class ContractCancelView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsClient]

    def post(self, request, pk):
        contract = get_object_or_404(Contract, pk=pk, client=request.user)

        if contract.status != 'active':
            return Response({'error': 'Only active contracts can be cancelled.'},
                            status=status.HTTP_400_BAD_REQUEST)

        contract.status = 'cancelled'
        contract.save()

        contract.project.status = 'cancelled'
        contract.project.save()

        return Response({
            'message': 'Contract cancelled successfully.',
            'contract': ContractSerializer(contract).data
        }, status=status.HTTP_200_OK)