from django.urls import path
from . import views

urlpatterns = [
    path('', views.ReviewCreateView.as_view(), name='review-create'),
    path('my/received/', views.MyReviewsReceivedView.as_view(), name='my-reviews-received'),
    path('my/given/', views.MyReviewsGivenView.as_view(), name='my-reviews-given'),
    path('<int:pk>/', views.ReviewDetailView.as_view(), name='review-detail'),
    path('freelancer/<int:freelancer_id>/', views.ReviewListView.as_view(), name='freelancer-reviews'),
]
