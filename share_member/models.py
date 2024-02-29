from django.db import models
from file.models import File
from user.models import User
import uuid
from account.api.utils import Util

# Create your models here.
ACCEPTED = 'accepted'
REJECTED = 'rejected'
PENDING = 'pending'
STATUS_CHOICES = [
    (ACCEPTED, 'Accepted'),
    (REJECTED, 'Rejected'),
    (PENDING, 'Pending'),
]

class UserFileShare(models.Model):
    
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)
    shared_at = models.DateTimeField(auto_now_add=True)
    
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=PENDING,
    )

    class Meta:
        verbose_name = 'user_file_share'
        verbose_name_plural = 'user_file_shares'
        db_table = "user_file_shares"
        unique_together = ('file',"member"
    )