from django.urls import path
from . import views

urlpatterns = [
    path('', views.ContractListView.as_view(), name='contract-list'),
    path('<int:pk>/', views.ContractDetailView.as_view(), name='contract-detail'),
    path('<int:pk>/finish/', views.ContractFinishView.as_view(), name='contract-finish'),
    path('<int:pk>/cancel/', views.ContractCancelView.as_view(), name='contract-cancel'),
]
