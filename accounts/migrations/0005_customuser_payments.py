# Generated by Django 4.1.7 on 2023-04-30 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_remove_sum_partial_paid_payment'),
        ('accounts', '0004_rename__sums_customuser_sums'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='payments',
            field=models.ManyToManyField(help_text='Payments involving this user', to='home.payment'),
        ),
    ]
