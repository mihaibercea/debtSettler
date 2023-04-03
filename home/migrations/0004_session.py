# Generated by Django 4.1.7 on 2023-04-01 08:37

import datetime
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_sessionmember'),
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('time_created', models.DateField(default=datetime.date(2000, 1, 1))),
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this particular session across whole sessions list', primary_key=True, serialize=False)),
                ('name', models.CharField(default='New Session', max_length=200)),
                ('type', models.CharField(blank=True, choices=[('z', 'Zero Sum'), ('s', 'Split Sum')], default='z', help_text='Type of session', max_length=1)),
                ('status', models.CharField(blank=True, choices=[('o', 'open'), ('c', 'closed')], default='o', help_text='Status of the session', max_length=1)),
                ('member', models.ManyToManyField(help_text='Add members to this session', to='home.sessionmember')),
            ],
            options={
                'ordering': ['-time_created'],
            },
        ),
    ]
