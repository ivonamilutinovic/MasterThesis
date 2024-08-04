from django.db import models


class HeartRateZones(models.IntegerChoices):
    Z1 = 1, 'Z1'
    Z2 = 2, 'Z2'
    Z3 = 3, 'Z3'
    Z4 = 4, 'Z4'
    Z5 = 5, 'Z5'


class StravaAthlete(models.Model):
    athlete_id = models.PositiveBigIntegerField(primary_key=True)
    access_token_expires_at = models.PositiveIntegerField()
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    # scope_permissions = models.CharField(null=True)
    hr_zones = models.JSONField(null=True)
    backfill_progress = models.PositiveIntegerField(default=0, null=True)  # TODO: Add description


class StravaActivity(models.Model):
    activity_id = models.PositiveBigIntegerField(primary_key=True)
    athlete_id = models.ForeignKey(StravaAthlete, on_delete=models.CASCADE, db_column='athlete_id')
    is_full_activity_filled = models.BooleanField(default=False)
    name = models.CharField(max_length=255, null=True)
    activity_type = models.CharField(max_length=255, null=True)
    distance = models.FloatField(null=True)  # in kilometers
    moving_time = models.PositiveIntegerField(null=True)
    elapsed_time = models.PositiveIntegerField(null=True)
    total_elevation_gain = models.FloatField(null=True)
    sport_type = models.CharField(max_length=255, null=True)
    start_date = models.DateTimeField(null=True)
    trainer = models.BooleanField(null=True)
    average_speed = models.FloatField(null=True)  # in m/sec
    max_speed = models.FloatField(null=True)
    has_heartrate = models.BooleanField(null=True)
    average_heartrate = models.FloatField(null=True)
    average_heartrate_zone = models.IntegerField(choices=HeartRateZones.choices, null=True)
    max_heartrate = models.FloatField(null=True)
    is_race = models.BooleanField(null=True)


class StravaSettings(models.Model):
    setting_key = models.CharField(max_length=255, primary_key=True)
    setting_value = models.CharField(max_length=255, null=True)
