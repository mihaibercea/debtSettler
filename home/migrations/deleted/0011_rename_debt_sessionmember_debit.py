# Generated by Django 4.1.7 on 2023-03-31 11:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_sessionmember_alter_session_members'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sessionmember',
            old_name='debt',
            new_name='debit',
        ),
    ]
