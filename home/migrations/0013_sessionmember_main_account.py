# Generated by Django 4.1.7 on 2023-04-24 05:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0012_alter_session_name_sum_club_sums'),
    ]

    operations = [
        migrations.AddField(
            model_name='sessionmember',
            name='main_account',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
