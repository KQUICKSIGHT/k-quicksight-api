from django.db import models
import uuid
from user.models import User
# Create your models here.
class ImageVisualize(models.Model):
    id = models.AutoField(primary_key=True)
    filename = models.CharField(max_length=200)
    file = models.CharField(max_length=200)
    created_by = models.ForeignKey(User,related_name="users_image_visualize", on_delete=models.CASCADE)
    _id = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    size = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)

