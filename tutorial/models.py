from django.db import models
from user.models import User
import uuid


class Tutorial(models.Model):

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, null=False)
    slug = models.CharField(max_length=200,null=True)
    published_by = models.ForeignKey(
        User, related_name="tutorials", on_delete=models.CASCADE) 
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    content = models.TextField(blank=False)
    description = models.TextField(blank=False,null=False)
    thumbnail = models.CharField(max_length=50,null=False)
    view = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:

        verbose_name = 'tutorial'
        verbose_name_plural = 'tutorials'
        db_table = "tutorials"
