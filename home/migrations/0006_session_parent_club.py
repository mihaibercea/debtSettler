# Generated by Django 4.1.7 on 2023-04-01 08:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_club_invites_sent_club_sessions'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='parent_club',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='home.club'),
        ),
    ]
