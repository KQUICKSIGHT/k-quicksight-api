# Generated by Django 4.2.6 on 2023-12-28 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorial', '0002_alter_tutorial_thumbnail'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutorial',
            name='view',
            field=models.IntegerField(default=0),
        ),
    ]
