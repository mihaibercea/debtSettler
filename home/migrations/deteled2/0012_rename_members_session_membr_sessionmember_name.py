# Generated by Django 4.1.7 on 2023-04-01 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_sessionmember_session_parent_club_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='session',
            old_name='members',
            new_name='membr',
        ),
        migrations.AddField(
            model_name='sessionmember',
            name='name',
            field=models.CharField(default='New Member', max_length=200),
        ),
    ]
