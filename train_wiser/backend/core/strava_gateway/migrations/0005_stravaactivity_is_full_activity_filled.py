# Generated by Django 4.2.10 on 2024-07-15 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('strava_gateway', '0004_stravasettings_remove_stravaathlete_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='stravaactivity',
            name='is_full_activity_filled',
            field=models.BooleanField(default=False),
        ),
    ]
