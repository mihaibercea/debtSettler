# Generated by Django 4.1.7 on 2023-04-26 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_session_sums'),
    ]

    operations = [
        migrations.AddField(
            model_name='sum',
            name='partial_paid',
            field=models.FloatField(default=0),
        ),
    ]