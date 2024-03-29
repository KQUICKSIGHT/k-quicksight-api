# Generated by Django 4.2.6 on 2024-01-02 19:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0004_dashboard_is_sample'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShareDashboard',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('shared_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('accepted', 'Accepted'), ('rejected', 'Rejected'), ('pending', 'Pending')], default='pending', max_length=10)),
                ('dashboard', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.dashboard')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'share_dashboard',
                'verbose_name_plural': 'share_dashboard',
                'db_table': 'share_dashboard',
                'unique_together': {('dashboard', 'member')},
            },
        ),
    ]
