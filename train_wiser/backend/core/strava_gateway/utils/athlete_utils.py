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
            print(f"Response status code is {response.status_code}, it is expected to be 200.")
            return False

        response_json = response.json()

        strava_athlete.access_token = response_json.get('access_token')
        strava_athlete.access_token_expires_at = response_json.get('expires_at')
        strava_athlete.refresh_token = response_json.get('refresh_token')
        strava_athlete.save()
        print(f"Refreshing token for user {strava_athlete}")

    return True


def set_athlete_hr_zone(strava_athlete):
    if not refresh_access_token_if_needed(strava_athlete):
        print("Error happen during access token update.")
        return

    response = requests.get(url="https://www.strava.com/api/v3/athlete/zones",
                                   headers={'Authorization': f'Bearer '
                                            f'{strava_athlete.access_token}'})

    if response.status_code != 200:
        print(f"status code {response.status_code}")
        return

    athlete_hr_zone = response.json()
    athlete_hr_zone = athlete_hr_zone.get('heart_rate', None)
    if not athlete_hr_zone:
        print("There is no 'heart_rate' field in the json response.")
        return
    athlete_hr_zone = athlete_hr_zone.get('zones', None)
    if not athlete_hr_zone:
        print("There is no 'zones' field in the json response.")
        return
    athlete_hr_zone_json = {}
    for i, zone_values in enumerate(athlete_hr_zone):
        zone = getattr(HeartRateZones, f"Z{i + 1}")
        athlete_hr_zone_json[zone] = [zone_values['min'], zone_values['max']]

    strava_athlete.hr_zones=athlete_hr_zone_json
    strava_athlete.save()
