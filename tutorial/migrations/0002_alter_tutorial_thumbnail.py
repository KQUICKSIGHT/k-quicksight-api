# Generated by Django 4.2.6 on 2023-11-28 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorial', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutorial',
            name='thumbnail',
            field=models.CharField(max_length=50),
        ),
    ]