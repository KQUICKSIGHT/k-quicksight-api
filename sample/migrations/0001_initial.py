# Generated by Django 4.2.6 on 2024-01-01 15:49

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('analysis', '0010_alter_analysis_recommneded'),
    ]

    operations = [
        migrations.CreateModel(
            name='SampleAnalysis',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('analysis', models.ForeignKey(db_column='analysis_uuid', on_delete=django.db.models.deletion.CASCADE, related_name='sample_analysis', to='analysis.analysis', to_field='uuid')),
            ],
            options={
                'verbose_name': 'sample_analysis',
                'verbose_name_plural': 'sample_analysis',
                'db_table': 'sample_analysis',
            },
        ),
    ]
