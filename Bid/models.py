from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Bid(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )

    project = models.ForeignKey('Project.Project', on_delete=models.CASCADE, related_name='bids')
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    price = models.DecimalField(max_digits=12, decimal_places=2)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Bid'
        verbose_name_plural = 'Bids'
        ordering = ['-created_at']
        unique_together = ['project', 'freelancer']  # bitta freelancer bitta projectga 1 bid

    def __str__(self):
        return f"Bid by {self.freelancer.username} on {self.project.title} - ${self.price}"
