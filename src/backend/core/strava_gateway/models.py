from django.db import models


class StravaAthlete(models.Model):
    athlete_id = models.PositiveBigIntegerField()  # TODO: Set as primary key
    access_token_expires_at = models.PositiveIntegerField()
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    backfill_progress = models.PositiveIntegerField(default=0, null=True)  # TODO: Add description
