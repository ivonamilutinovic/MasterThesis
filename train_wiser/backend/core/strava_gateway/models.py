from django.db import models


class StravaAthlete(models.Model):
    athlete_id = models.PositiveBigIntegerField(primary_key=True)
    access_token_expires_at = models.PositiveIntegerField()
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    backfill_progress = models.PositiveIntegerField(default=0, null=True)  # TODO: Add description


class StravaSettings(models.Model):
    setting_key = models.CharField(max_length=255, primary_key=True)
    setting_value = models.CharField(max_length=255, null=True)
