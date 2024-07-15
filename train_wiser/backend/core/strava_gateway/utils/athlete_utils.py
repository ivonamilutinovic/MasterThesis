from datetime import datetime

import requests
from decouple import config

from strava_gateway.models import HeartRateZones


def refresh_access_token_if_needed(strava_athlete: 'StravaAthlete') -> bool:
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


def set_athlete_hr_zone(strava_athlete):
    print("usli u fju")
    if not refresh_access_token_if_needed(strava_athlete):
        print("Error happen during access token update.")
        return

    response = requests.get(url="https://www.strava.com/api/v3/athlete/zones",
                                   headers={'Authorization': f'Bearer '
                                            f'{strava_athlete.access_token}'})
    print(f"SC {response.status_code}")
    if response.status_code != 200:
        print(f"status code {response.status_code}")

    athlete_hr_zone = response.json()
    print(athlete_hr_zone)
    # # todo: fill in order with custom class
    # athlete_hr_zone = {HeartRateZones.Z1: [2, 7], }
    # # athlete_hr_zone = {HeartRateZones.Z1: [athlete_hr_zone.get(), athlete_hr_zone.get()], }
    # strava_athlete.update(athlete_hr_zone=athlete_hr_zone)
    # strava_athlete.save()
