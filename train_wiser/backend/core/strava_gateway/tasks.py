from datetime import datetime, timezone
from typing import List

import requests

from .models import StravaAthlete, StravaActivity
from .utils.activity_utils import is_run_activity_race, set_activity_hr_zone
from .utils.athlete_utils import refresh_access_token_if_needed, set_athlete_hr_zone
import logging


logger = logging.getLogger('django')

ACTIVITIES_OF_INTEREST = {'WeightTraining', 'Run', 'TrailRun', 'Ride', 'VirtualRide'}

def activity_backfill():

    """ Taking all past activities for new Train wiser app users """
    unsynced_users: List[StravaAthlete] = StravaAthlete.objects.exclude(backfill_progress__isnull=True)
    print(f"Unsync users: {unsynced_users}")
    for user in unsynced_users:
        page = 1
        new_backfill_progress = user.backfill_progress
        print(f"Backfill progress: {new_backfill_progress}")
        while True:
            if not refresh_access_token_if_needed(user):
                print("Error happen during access token update.")
                break

            response = requests.get(url="https://www.strava.com/api/v3/athlete/activities",
                                    params={'after': user.backfill_progress,
                                            'page': page,
                                            'per_page': 100},  # TODO: Add in settings.py
                                    headers={'Authorization': f'Bearer {user.access_token}'})

            if response.status_code != 200:
                print(f"status code {response.status_code}")
                break

            activities = response.json()
            if not activities:
                print("there is no activities")
                new_backfill_progress = None
                break
            else:
                print(f"there are activities!\n")
            for activity in activities:
                start_time = datetime.strptime(activity.get('start_date'), '%Y-%m-%dT%H:%M:%SZ') \
                             .replace(tzinfo=timezone.utc).timestamp()
                if start_time > new_backfill_progress:
                    new_backfill_progress = start_time
                # if activity.get('sport_type') in ACTIVITIES_OF_INTEREST:
                print(f"Type: {activity.get('sport_type')}\n")
                print(f"HR: {activity.get('avg_heart_rate')}\n")

                print(f"{activity}\n\n")

                # if StravaAthlete.objects.filter(athlete_id=athlete_id).exists():
                #     strava_athlete = StravaAthlete.objects.filter(athlete_id=athlete_id).get()
                #     StravaActivity.objects.create(activity_id=activity_id, athlete_id=strava_athlete)

                try:
                    strava_activity = StravaActivity.objects.create(
                        activity_id=activity.get('id'),
                        athlete_id=user,
                        is_full_activity_filled=True,
                        activity_type=activity.get('sport_type', None),
                        distance=activity.get('distance', None),
                        moving_time=activity.get('moving_time', None),
                        elapsed_time=activity.get('elapsed_time', None),
                        total_elevation_gain=activity.get('total_elevation_gain', None),
                        sport_type=activity.get('sport_type', None),
                        start_date=activity.get('start_date', None),
                        trainer=activity.get('trainer', None),
                        average_speed=activity.get('average_speed', None),
                        max_speed=activity.get('max_speed', None),
                        has_heartrate=activity.get('has_heartrate', None),
                        average_heartrate=activity.get('average_heartrate', None),
                        max_heartrate=activity.get('max_heartrate', None),
                        is_race=is_run_activity_race(activity))
                    strava_activity.update(average_heartrate_zone=set_activity_hr_zone(strava_activity, user))
                except Exception as e:
                    print(str(e))

            if page == 3:
                break  # TODO: Remove after testing
            page += 1

            # TODO: Filter type of activity
        user.backfill_progress = new_backfill_progress
        user.save()

# WeightTraining
#
# {'resource_state': 2, 'athlete': {'id': 43296965, 'resource_state': 1}, 'name': 'Night Weight Training',
# 'distance': 0.0, 'moving_time': 4320, 'elapsed_time': 4320, 'total_elevation_gain': 0, 'type': 'WeightTraining',
# 'sport_type': 'WeightTraining', 'id': 11905250368, 'start_date': '2024-07-16T19:01:14Z', 'start_date_local': '2024-07-16T21:01:14Z',
# 'timezone': '(GMT+02:00) Africa/Blantyre', 'utc_offset': 7200.0, 'location_city': None, 'location_state': None, 'location_country': None,
# 'achievement_count': 0, 'kudos_count': 5, 'comment_count': 0, 'athlete_count': 1, 'photo_count': 0, 'map': {'id': 'a11905250368',
# 'summary_polyline': '', 'resource_state': 2}, 'trainer': True, 'commute': False, 'manual': False, 'private': False, 'visibility': 'everyone',
# 'flagged': False, 'gear_id': None, 'start_latlng': [], 'end_latlng': [], 'average_speed': 0.0, 'max_speed': 0.0, 'has_heartrate': True,
# 'average_heartrate': 104.1, 'max_heartrate': 144.0, 'heartrate_opt_out': False, 'display_hide_heartrate_option': True, 'elev_high': 0.0,
# 'elev_low': 0.0, 'upload_id': 12694697192, 'upload_id_str': '12694697192', 'external_id': 'garmin_ping_355418859579', 'from_accepted_tag': False,
# 'pr_count': 0, 'total_photo_count': 0, 'has_kudoed': False}


# Run
#
# {'resource_state': 2, 'athlete': {'id': 43296965, 'resource_state': 1}, 'name': '15. Noćni maraton, 21k',
# 'distance': 21144.5, 'moving_time': 7553, 'elapsed_time': 7562, 'total_elevation_gain': 83.0, 'type': 'Run',
# 'sport_type': 'Run', 'workout_type': 1, 'id': 11715471519, 'start_date': '2024-06-22T20:00:02Z',
# 'start_date_local': '2024-06-22T22:00:02Z', 'timezone': '(GMT+01:00) Europe/Belgrade', 'utc_offset': 7200.0,
# 'location_city': None, 'location_state': None, 'location_country': None, 'achievement_count': 8, 'kudos_count': 22,
# 'comment_count': 4, 'athlete_count': 1, 'photo_count': 0, 'map': {'id': 'a11715471519',
# 'summary_polyline': '_scsGqvdxBc@O_@FUVc@~Ay@?iB}@GKQqASw@O]SAmFdD{K`GO[qAqGgB_IFQh@MhDN~MnA|Fv@nEfAzDlAbDnApD`
# {@VeBLmAASIU_Ak@', 'resource_state': 2}, 'trainer': False, 'commute': False, 'manual': False, 'private': False,
# 'visibility': 'everyone', 'flagged': False, 'gear_id': None, 'start_latlng': [45.243521109223366, 19.85401882790029],
# 'end_latlng': [45.243650525808334, 19.854087475687265], 'average_speed': 2.796, 'max_speed': 4.832, 'average_cadence': 83.1,
# 'average_temp': 30, 'average_watts': 227.2, 'max_watts': 448, 'weighted_average_watts': 237, 'kilojoules': 1716.3,
# 'device_watts': True, 'has_heartrate': True, 'average_heartrate': 169.5, 'max_heartrate': 184.0, 'heartrate_opt_out': False,
# 'display_hide_heartrate_option': True, 'elev_high': 96.4,
#  'elev_low': 71.8, 'upload_id': 12498765010, 'upload_id_str': '12498765010', 'external_id': 'garmin_ping_349725669800',
#  'from_accepted_tag': False, 'pr_count': 5, 'total_photo_count': 0, 'has_kudoed': False}


def fetch_activity_data():
    # Reading data from database with empty activities
    empty_activities = StravaActivity.objects.filter(is_full_activity_filled=False)

    for activity_to_fill in empty_activities:
        activity_details = requests.get(url="https://www.strava.com/api/v3/athlete/activities",
                                        params={'id': activity_to_fill.activity_id},
                                        headers={'Authorization': f'Bearer '
                                                                  f'{activity_to_fill.athlete_id.access_token}'}).json()
        if activity_details.get('activity_type') in ACTIVITIES_OF_INTEREST:
            # TOdo: gde ovde az access token
            activity_to_fill.update(is_full_activity_filled=True,
                                    activity_type=activity_details.get('activity_type'),
                                    distance=activity_details.get('distance'),
                                    moving_time=activity_details.get('moving_time'),
                                    elapsed_time=activity_details.get('elapsed_time'),
                                    total_elevation_gain=activity_details.get('total_elevation_gain'),
                                    sport_type=activity_details.get('sport_type'),
                                    start_date=activity_details.get('start_date'),
                                    trainer=activity_details.get('trainer'),
                                    average_speed=activity_details.get('average_speed'),
                                    max_speed=activity_details.get('max_speed'),
                                    average_heartrate=activity_details.get('average_heartrate'),
                                    is_race=is_run_activity_race(activity_details))
            activity_to_fill.save()
        else:
            activity_to_fill.delete()

def fill_athlete_hr_zone():
    athlete_id = 43296965
    if StravaAthlete.objects.filter(athlete_id=athlete_id).exists():
        print("nadjen atleta")
        strava_athlete = StravaAthlete.objects.filter(athlete_id=athlete_id).get()
        set_athlete_hr_zone(strava_athlete)
