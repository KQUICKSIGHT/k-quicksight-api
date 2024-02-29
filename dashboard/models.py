from django.db import models
import uuid
from django.db.models import JSONField 
from user.models import User
from file.models import File



class Dashboard(models.Model):

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200,null=True)
    file= models.ForeignKey(File,related_name="file_dasboard",on_delete=models.CASCADE)
    thumbnail = models.CharField(max_length=200,null=True)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    created_by = models.ForeignKey(User, related_name="users_dashboard", on_delete=models.CASCADE) 
    json_data = JSONField(default=None,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    is_sample = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'dashboards'
        verbose_name_plural = 'dashboards'
        db_table = "dashboards"