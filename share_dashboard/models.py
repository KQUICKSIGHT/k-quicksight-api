from django.db import models
from file.models import File
from user.models import User
import uuid
from account.api.utils import Util
from analysis.models import Analysis
from dashboard.models import Dashboard
# Create your models here.
ACCEPTED = 'accepted'
REJECTED = 'rejected'
PENDING = 'pending'
STATUS_CHOICES = [
    (ACCEPTED, 'Accepted'),
    (REJECTED, 'Rejected'),
    (PENDING, 'Pending'),
]

class ShareDashboard(models.Model):
    
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)
    shared_at = models.DateTimeField(auto_now_add=True)
    
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=PENDING,
    )

    class Meta:
        verbose_name = 'share_dashboard'
        verbose_name_plural = 'share_dashboard'
        db_table = "share_dashboard"
        unique_together = ('dashboard',"member"
    )