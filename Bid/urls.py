from django.urls import path
from . import views

urlpatterns = [
    path('', views.BidCreateView.as_view(), name='bid-create'),
    path('my/', views.MyBidsView.as_view(), name='my-bids'),
    path('<int:pk>/', views.BidDetailView.as_view(), name='bid-detail'),
    path('<int:pk>/update/', views.BidUpdateView.as_view(), name='bid-update'),
    path('<int:pk>/delete/', views.BidDeleteView.as_view(), name='bid-delete'),
    path('<int:bid_id>/accept/', views.AcceptBidView.as_view(), name='bid-accept'),
    path('project/<int:project_id>/', views.BidListView.as_view(), name='project-bids'),
]
