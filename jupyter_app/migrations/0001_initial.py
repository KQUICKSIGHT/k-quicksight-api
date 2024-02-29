# Generated by Django 4.2.6 on 2023-12-06 11:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='JupyterDocument',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('file', models.CharField(max_length=200)),
                ('filename', models.CharField(max_length=200)),
                ('size', models.IntegerField()),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_jupyrer', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'jupyter_document',
                'verbose_name_plural': 'jupyter_documents',
                'db_table': 'jupyter_documents',
            },
        ),
    ]
