# Generated by Django 4.1.7 on 2023-02-16 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_alter_club_time_created_alter_invite_time_created'),
    ]

    operations = [
        migrations.RenameField(
            model_name='invite',
            old_name='club',
            new_name='parent_club',
        ),
        migrations.AddField(
            model_name='club',
            name='invites_sent',
            field=models.ManyToManyField(to='home.invite'),
        ),
    ]