# Generated by Django 4.1.7 on 2023-05-01 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0021_payment_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='bias',
            field=models.FloatField(default=0),
        ),
    ]