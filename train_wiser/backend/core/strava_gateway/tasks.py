import math
from datetime import datetime, timezone
from typing import List, Union

import requests

from .models import StravaAthlete, StravaActivity
from .utils.activity_utils import is_run_activity_race, get_activity_hr_zone
from .utils.athlete_utils import refresh_access_token_if_needed
import logging

logger = logging.getLogger('django')

ACTIVITIES_OF_INTEREST = {'WeightTraining', 'Run', 'TrailRun', 'Ride', 'VirtualRide', 'Swim'}

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
                new_backfill_progress = None
                break

            for activity in activities:
                start_time = datetime.strptime(activity.get('start_date'), '%Y-%m-%dT%H:%M:%SZ') \
                             .replace(tzinfo=timezone.utc).timestamp()
                if start_time > new_backfill_progress:
                    new_backfill_progress = start_time
                if activity.get('sport_type') in ACTIVITIES_OF_INTEREST:
                    try:
                        is_race = is_run_activity_race(activity)
                        rounded_race_distance = None
                        distance = activity.get('distance', 0) / 1000.0
                        if is_race and distance and is_race_distance_of_relevant_type(distance):
                            rounded_race_distance = round_race_distance(distance)

                        strava_activity = StravaActivity.objects.create(
                            activity_id=activity.get('id'),
                            athlete_id=user,
                            is_full_activity_filled=True,
                            name=activity.get('name', None),
                            activity_type=activity.get('sport_type', None),
                            distance=distance,
                            rounded_race_distance = rounded_race_distance,
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
                        strava_activity.average_heartrate_zone=get_activity_hr_zone(strava_activity, user)
                        strava_activity.save()
                    except Exception as e:
                        print(str(e))

            page += 1

        user.backfill_progress = new_backfill_progress
        user.save()


def fetch_activity_data():
    # Reading data from database with empty activities
    empty_activities = StravaActivity.objects.filter(is_full_activity_filled=False)

    for activity_to_fill in empty_activities:
        activity_details = requests.get(url="https://www.strava.com/api/v3/athlete/activities",
                                        params={'id': activity_to_fill.activity_id},
                                        headers={'Authorization': f'Bearer '
                                                                  f'{activity_to_fill.athlete_id.access_token}'}).json()
        if activity_details.get('activity_type') in ACTIVITIES_OF_INTEREST:

            is_race = is_run_activity_race(activity_details)
            rounded_race_distance = None
            distance = activity_details.get('distance', 0) / 1000.0
            if is_race and distance and is_race_distance_of_relevant_type(distance):
                rounded_race_distance = round_race_distance(distance)

            activity_to_fill.is_full_activity_filled=True
            activity_to_fill.activity_type=activity_details.get('activity_type')
            activity_to_fill.distance=distance
            activity_to_fill.rounded_race_distance = rounded_race_distance
            activity_to_fill.moving_time=activity_details.get('moving_time')
            activity_to_fill.elapsed_time=activity_details.get('elapsed_time')
            activity_to_fill.total_elevation_gain=activity_details.get('total_elevation_gain')
            activity_to_fill.sport_type=activity_details.get('sport_type')
            activity_to_fill.start_date=activity_details.get('start_date')
            activity_to_fill.trainer=activity_details.get('trainer')
            activity_to_fill.average_speed=activity_details.get('average_speed')
            activity_to_fill.max_speed=activity_details.get('max_speed')
            activity_to_fill.average_heartrate=activity_details.get('average_heartrate')
            activity_to_fill.is_race=is_race
            activity_to_fill.save()
        else:
            activity_to_fill.delete()


def round_race_distance(race_distance: float) -> Union[int, float]:
    if math.floor(race_distance) == 7:
        difference_to_7 = abs(race_distance - 7)
        difference_to_7_7 = abs(race_distance - 7.7)
        if difference_to_7 <= difference_to_7_7:
            race_distance = 7
        elif difference_to_7 > difference_to_7_7:
            race_distance = 7.7
    else:
        race_distance = math.floor(race_distance)

    return race_distance


def is_race_distance_of_relevant_type(race_distance: float) -> bool:
    relevant_distances = [5, 7, 7.7, 10, 21, 42]
    return round_race_distance(race_distance) in relevant_distances