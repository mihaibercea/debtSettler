# Generated by Django 4.1.7 on 2023-04-01 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_rename_member_session_members'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sessionmember',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]