# Generated by Django 4.2.6 on 2023-11-21 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'role',
                'verbose_name_plural': 'roles',
                'db_table': 'roles',
            },
        ),
    ]
