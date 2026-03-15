from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from .models import Project
from .serializers import ProjectSerializer, ProjectCreateSerializer, ProjectUpdateSerializer
from .permissions import IsClient, IsProjectOwner
from .filters import ProjectFilter


class ProjectListView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProjectFilter
    search_fields = ['title', 'description']
    ordering_fields = ['budget', 'deadline', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        return Project.objects.filter(status='open').select_related('client')


class ProjectAllListView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProjectFilter
    search_fields = ['title', 'description']
    ordering_fields = ['budget', 'deadline', 'created_at']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'client':
            return Project.objects.filter(client=user).select_related('client')
        return Project.objects.all().select_related('client')


class ProjectCreateView(generics.CreateAPIView):
    serializer_class = ProjectCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsClient]

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        project = serializer.save(client=request.user)
        return Response(ProjectSerializer(project).data, status=status.HTTP_201_CREATED)


class ProjectDetailView(generics.RetrieveAPIView):
    queryset = Project.objects.select_related('client')
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProjectUpdateView(generics.UpdateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsClient, IsProjectOwner]


class ProjectCancelView(generics.UpdateAPIView):
    queryset = Project.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsClient, IsProjectOwner]

    def patch(self, request, *args, **kwargs):
        project = self.get_object()
        if project.status not in ['open']:
            return Response({'error': 'Only open projects can be cancelled.'},
                            status=status.HTTP_400_BAD_REQUEST)
        project.status = 'cancelled'
        project.save()
        return Response({'message': 'Project cancelled successfully.', 'status': project.status})


class MyProjectsView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsClient]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProjectFilter
    search_fields = ['title']
    ordering_fields = ['budget', 'deadline', 'created_at']

    def get_queryset(self):
        return Project.objects.filter(client=self.request.user).select_related('client')