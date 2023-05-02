# Generated by Django 4.1.7 on 2023-04-30 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_remove_sum_partial_paid_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='sum',
            name='payments',
            field=models.ManyToManyField(help_text='Create payments for this sum', to='home.payment'),
        ),
    ]