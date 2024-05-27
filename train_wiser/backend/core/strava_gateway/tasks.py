from datetime import datetime, timezone
from typing import List

import requests

from .models import StravaAthlete
from .utils import refresh_access_token_if_needed


def activity_backfill():
    # Taking all past activities for new Train wiser app users
    unsynced_users: List[StravaAthlete] = StravaAthlete.objects.exclude(backfill_progress__isnull=True)
    # 1 2 3 4 5 6 7
    for user in unsynced_users:

        page = 1
        new_backfill_progress = user.backfill_progress
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
                break  # TODO: Investigate logging

            activities = response.json()
            if not activities:
                new_backfill_progress = None
                break

            for activity in activities:
                start_time = datetime.strptime(activity.get('start_date'), '%Y-%m-%dT%H:%M:%SZ') \
                             .replace(tzinfo=timezone.utc).timestamp()
                if start_time > new_backfill_progress:
                    new_backfill_progress = start_time
                print(f"{activity.get('id')}     {activity.get('start_date')}")

            if page == 3:
                break  # TODO: Remove after testing
            page += 1

            # TODO: Filter type of activity
            # TODO [other]: make db with activities, webhooks
        user.backfill_progress = new_backfill_progress
        user.save()
