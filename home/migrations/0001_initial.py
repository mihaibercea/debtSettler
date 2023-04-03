# Generated by Django 4.1.7 on 2023-04-01 08:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_created', models.DateField(default=django.utils.timezone.now)),
                ('name', models.CharField(help_text='Enter a club name', max_length=200)),
                ('members', models.ManyToManyField(help_text='Add members to this club', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='club_owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-time_created'],
            },
        ),
    ]
