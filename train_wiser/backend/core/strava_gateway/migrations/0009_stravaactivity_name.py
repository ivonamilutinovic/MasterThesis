# Generated by Django 4.2.10 on 2024-07-23 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('strava_gateway', '0008_rename_avg_heart_rate_stravaactivity_average_heartrate_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='stravaactivity',
            name='name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
