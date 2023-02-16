# Generated by Django 4.1.7 on 2023-02-15 12:25

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0003_club_sessions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='members',
            field=models.ManyToManyField(help_text='Add members to this club', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='club',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='club_owner', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='club',
            name='time_created',
            field=models.DateField(default=datetime.datetime(2023, 2, 15, 12, 25, 11, 500642, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='session',
            name='members',
            field=models.ManyToManyField(help_text='Add members to this session', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
