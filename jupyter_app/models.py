from django.db import models
import uuid
from  user.models import User

# Create your models here.
class JupyterDocument(models.Model):

    id = models.AutoField(primary_key=True)
    file = models.CharField(max_length=200)
    filename = models.CharField(max_length=200)
    size = models.IntegerField()
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name="users_jupyrer", on_delete=models.CASCADE) 
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'jupyter_document'
        verbose_name_plural = 'jupyter_documents'
        db_table = "jupyter_documents"
    