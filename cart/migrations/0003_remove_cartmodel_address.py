# Generated by Django 4.1.2 on 2023-06-08 06:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_alter_cartmodel_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartmodel',
            name='address',
        ),
    ]
