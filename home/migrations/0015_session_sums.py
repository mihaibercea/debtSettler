# Generated by Django 4.1.7 on 2023-04-26 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_alter_invite_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='sums',
            field=models.ManyToManyField(to='home.sum'),
        ),
    ]
