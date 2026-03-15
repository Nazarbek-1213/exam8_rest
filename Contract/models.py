from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Contract(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('finished', 'Finished'),
        ('cancelled', 'Cancelled'),
    )

    project = models.OneToOneField('Project.Project', on_delete=models.CASCADE, related_name='contract')
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_contracts')
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='freelancer_contracts')
    agreed_price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Contract'
        verbose_name_plural = 'Contracts'
        ordering = ['-created_at']

    def __str__(self):
        return f"Contract: {self.project.title} | {self.client.username} ↔ {self.freelancer.username}"
