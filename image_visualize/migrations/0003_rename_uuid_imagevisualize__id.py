# Generated by Django 4.2.6 on 2023-12-19 01:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('image_visualize', '0002_imagevisualize_file'),
    ]

    operations = [
        migrations.RenameField(
            model_name='imagevisualize',
            old_name='uuid',
            new_name='_id',
        ),
    ]