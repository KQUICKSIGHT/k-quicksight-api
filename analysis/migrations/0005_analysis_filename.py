# Generated by Django 4.2.6 on 2023-12-08 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0004_analysis_thumbnail_analysis_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='analysis',
            name='filename',
            field=models.CharField(default='6de266b08494422a9ec8fb3aa7a7c34b.xlsx', max_length=250),
            preserve_default=False,
        ),
    ]
