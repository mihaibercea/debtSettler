# Generated by Django 4.1.7 on 2023-04-01 05:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_customuser_invites_received_customuser_invites_sent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='clubs',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='invites_received',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='invites_sent',
        ),
    ]
