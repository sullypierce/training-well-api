# Generated by Django 4.0.1 on 2022-02-04 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainingwellapi', '0003_trainingplan_session_loggedexercise_goal'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='time_completed',
            field=models.TimeField(null=True),
        ),
    ]
