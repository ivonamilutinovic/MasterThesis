from datetime import datetime

import requests
from decouple import config
from django.http import HttpResponse

from .models import StravaAthlete


def refresh_access_token_if_needed(strava_athlete: StravaAthlete) -> bool:
    current_time = int(datetime.now().timestamp())
    time_delta = 30 * 60
    if strava_athlete.access_token_expires_at - time_delta <= current_time:
        post_config = {'client_id': config("CLIENT_ID"),
                       'client_secret': config("CLIENT_SECRET"),
                       'refresh_token': strava_athlete.refresh_token,
                       'grant_type': 'refresh_token'}
        response = requests.post(url="https://www.strava.com/api/v3/oauth/token", json=post_config)
        if response.status_code != 200:
            # TODO: Add logger message
            return False

        response_json = response.json()

        strava_athlete.access_token = response_json.get('access_token')
        strava_athlete.access_token_expires_at = response_json.get('expires_at')
        strava_athlete.refresh_token = response_json.get('refresh_token')
        strava_athlete.save()
        print(f"Refreshing token for user {strava_athlete}")
        # TODO: Add logger message

    return True
