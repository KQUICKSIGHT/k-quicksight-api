from django.db import models

from user.models import User
import uuid

# Create your models here.
class RequestTutorial(models.Model):

    id = models.AutoField(primary_key=True)
    request_by = models.ForeignKey(
        User, related_name="request_tutorials", on_delete=models.CASCADE)     
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    subject = models.CharField(max_length=200,null=False)
    message = models.TextField(blank=False,null=False, max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:

        verbose_name = 'request_tutorial'
        verbose_name_plural = 'request_tutorials'
        db_table = "request_tutorials"