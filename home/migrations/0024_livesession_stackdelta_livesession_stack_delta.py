# Generated by Django 4.2.3 on 2023-07-23 08:06

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0023_alter_payment_options_joinrequest_club_join_requests'),
    ]

    operations = [
        migrations.CreateModel(
            name='LiveSession',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this particular session across whole sessions list', primary_key=True, serialize=False)),
                ('result_sum', models.FloatField(default=0)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('casino', models.CharField(default='Casino name', max_length=200)),
                ('buy_in', models.FloatField(default=0)),
                ('stakes', models.CharField(blank=True, choices=[('1/2', '1/2'), ('1/3', '1/3'), ('2/5', '2/5'), ('5/10', '5/10'), ('5/5', '5/5'), ('5/10', '5/10'), ('10/10', '10/10'), ('10/20', '10/20'), ('10/25', '10/25'), ('25/50', '25/50'), ('50/100', '50/100'), ('100/100', '100/100'), ('Other', 'Other')], default='1/2', help_text='Stakes played', max_length=30)),
                ('game', models.CharField(blank=True, choices=[('NLHE', 'NLHE'), ('PLO4', 'PLO4'), ('PLO5', 'PLO5'), ('Pinapple', ' Pineapple'), ('Stud', 'Stud'), ('HORSE', 'HORSE'), ('Other', 'Other')], default='NLHE', help_text='Stakes played', max_length=30)),
                ('status', models.CharField(blank=True, choices=[('o', 'open'), ('c', 'closed')], default='o', help_text='Status of the session', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='StackDelta',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this particular sum', primary_key=True, serialize=False)),
                ('date_created', models.DateField(default=django.utils.timezone.now)),
                ('value', models.FloatField(default=0)),
                ('parent_session', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='home.livesession')),
            ],
        ),
        migrations.AddField(
            model_name='livesession',
            name='stack_delta',
            field=models.ManyToManyField(to='home.stackdelta'),
        ),
    ]
