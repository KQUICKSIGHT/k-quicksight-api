from django.db import models
from user.models import User
# Create your models here.
class ContactUs(models.Model):

    id = models.AutoField(primary_key=True)

    email = models.EmailField(max_length=40, null=False)
    message = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    
    class Meta:
        verbose_name = 'contact_us'
        verbose_name_plural = 'contact_us'
        db_table="contact_us"
        