from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.db import models

from strava_gateway.models import StravaAthlete


class CustomUser(AbstractUser):
    strava_athlete_id = models.ForeignKey(StravaAthlete, on_delete=models.CASCADE, db_column='strava_athlete_id',
                                          null=True)
    email = models.EmailField(blank=False)
    birth_date = models.DateField(null=True)
