from django.db import models
import uuid
from analysis.models import Analysis
from dashboard.models import Dashboard
# Create your models here.

class SampleAnalysis(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    analysis_uuid = models.OneToOneField(Analysis, to_field='uuid', unique=True,db_column='analysis_uuid', related_name="sample_analysis", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'sample_analysis'
        verbose_name_plural = 'sample_analysis'
        db_table = "sample_analysis"
        constraints = [
            models.UniqueConstraint(
                fields=['analysis_uuid', 'is_deleted'], 
                condition=models.Q(is_deleted=False), 
                name='unique_analysis_uuid_not_deleted'
            )
        ]


class SampleDashboard(models.Model):
    
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    dashboard_uuid = models.OneToOneField(Dashboard, to_field='uuid',unique=True, db_column='dashboard_uuid', related_name="sample_dashboard", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    class Meta:
        verbose_name = 'sample_dashboard'
        verbose_name_plural = 'sample_dashboard'
        db_table = "sample_dashboard"