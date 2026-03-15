from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProjectListView.as_view(), name='project-list'),
    path('all/', views.ProjectAllListView.as_view(), name='project-all-list'),
    path('create/', views.ProjectCreateView.as_view(), name='project-create'),
    path('my/', views.MyProjectsView.as_view(), name='my-projects'),
    path('<int:pk>/', views.ProjectDetailView.as_view(), name='project-detail'),
    path('<int:pk>/update/', views.ProjectUpdateView.as_view(), name='project-update'),
    path('<int:pk>/cancel/', views.ProjectCancelView.as_view(), name='project-cancel'),
]
