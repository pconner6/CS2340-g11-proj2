# Generated by Django 5.1.3 on 2024-12-01 17:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wrapped',
            name='user',
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.DeleteModel(
            name='Wrapped',
        ),
    ]
