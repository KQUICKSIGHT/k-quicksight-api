# Generated by Django 4.2.6 on 2023-12-27 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0006_analysis_is_sample'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analysis',
            name='dependent_variable',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='analysis',
            name='independent_variable',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]