# Generated by Django 4.1.7 on 2023-04-25 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_sessionmember_main_account'),
        ('accounts', '0002_customuser_clubs_customuser_invites_received_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='_sums',
            field=models.ManyToManyField(help_text='Sums assinged to this user', to='home.sum'),
        ),
    ]
