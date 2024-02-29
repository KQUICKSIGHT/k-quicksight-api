from django.db import models
from simple_history.models import HistoricalRecords
from user.models import User
# Create your models here.
class History(models.Model):
    name = models.CharField(max_length=255,null=True)
    history_user = models.ForeignKey(User,  on_delete=models.CASCADE, null=True, blank=True)
    changed = models.CharField(max_length=255,null=True)
    history= HistoricalRecords()