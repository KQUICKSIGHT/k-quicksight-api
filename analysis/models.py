from file.models import File
from user.models import User
from django.db import models
import uuid
from django.db.models import JSONField 

from django.db import models


class Analysis(models.Model):
    MODEL_CHOICES = [
        ('descriptive_statistic', 'Descriptive Statistic'),
        ('random_number_generation', 'Random Number Generation'),
        ('correlation', 'Correlation'),
        ('covariance', 'Covariance'),
        ('simple_linear_regression', 'Simple Linear Regression'),
        ('non_linear_regression', 'Non-Linear Regression'),
        ('multiple_linear_regression', 'Multiple Linear Regression'),
    ]
    title = models.CharField(max_length=30,default="ANALYSIS",null=True)
    thumbnail = models.CharField(max_length=200,null=True)
    model_name = models.CharField(
        max_length=30,
        choices=MODEL_CHOICES,
    )
    analysis_data = JSONField()
    recommneded = models.TextField(max_length=500,null=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, related_name="users_analysis", on_delete=models.CASCADE, null=False, blank=False)
    independent_variable=models.CharField(max_length=200, null=True, blank=True)
    dependent_variable=models.CharField(max_length=200, null=True, blank=True)
    filename = models.CharField(max_length=250, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    is_sample = models.BooleanField(default=False)

    def __str__(self):
        return self.model_name
    class Meta:
        verbose_name = 'analysis'
        verbose_name_plural = 'analysis'
        db_table = "analysis"