# Generated by Django 4.1.7 on 2023-02-20 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_rename_club_invite_parent_club_club_invites_sent'),
    ]

    operations = [
        migrations.AddField(
            model_name='invite',
            name='accepted',
            field=models.BooleanField(default=False),
        ),
    ]
