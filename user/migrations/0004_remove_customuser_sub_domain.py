# Generated by Django 5.0.7 on 2024-07-30 10:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_customuser_sub_domain'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='sub_domain',
        ),
    ]
