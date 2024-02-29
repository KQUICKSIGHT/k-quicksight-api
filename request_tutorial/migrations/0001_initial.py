# Generated by Django 4.2.6 on 2023-12-15 08:13

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
            name='RequestTutorial',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('subject', models.CharField(max_length=200)),
                ('message', models.TextField(max_length=250)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('request_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request_tutorials', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'request_tutorial',
                'verbose_name_plural': 'request_tutorials',
                'db_table': 'request_tutorials',
            },
        ),
    ]