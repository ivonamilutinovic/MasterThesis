from django.db import models


class StravaAthlete(models.Model):
    athlete_id = models.PositiveBigIntegerField(primary_key=True)
    access_token_expires_at = models.PositiveIntegerField()
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    backfill_progress = models.PositiveIntegerField(default=0, null=True)  # TODO: Add description


class StravaActivity(models.Model):
    activity_id = models.PositiveBigIntegerField(primary_key=True)
    athlete_id = models.ForeignKey(StravaAthlete, on_delete=models.CASCADE, db_column='athlete_id')
    activity_type = models.CharField(max_length=255, null=True)
    distance = models.FloatField(null=True)
    moving_time = models.PositiveIntegerField(null=True)
    elapsed_time = models.PositiveIntegerField(null=True)
    total_elevation_gain = models.FloatField(null=True)
    sport_type = models.CharField(max_length=255, null=True)
    start_date = models.DateTimeField(null=True)
    trainer = models.BooleanField(null=True)
    average_speed = models.FloatField(null=True)  # in m/sec
    max_speed = models.FloatField(null=True)
    avg_heart_rate = models.PositiveIntegerField(null=True)
    is_activity_interval_training = models.BooleanField(null=True)


class StravaSettings(models.Model):
    setting_key = models.CharField(max_length=255, primary_key=True)
    setting_value = models.CharField(max_length=255, null=True)
