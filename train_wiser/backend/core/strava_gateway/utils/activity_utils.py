from typing import Dict

from strava_gateway.models import HeartRateZones

def is_run_activity_race(activity_details: Dict) -> bool:
    return activity_details.get('workout_type', -1) == 1


def set_activity_hr_zone(strava_activity, strava_athlete) -> None:
    return HeartRateZones.Z1
    # if not strava_activity.has_heartrate:
    #     return
    #
    # if StravaAthlete.objects.filter(athlete_id=athlete_id).exists():
    #     strava_athlete = StravaAthlete.objects.filter(athlete_id=athlete_id).get()
    #     activity_hr = strava_activity.avg_heart_rate
    #     for hr_zone in strava_athlete.hr_zones.items():
    #
    #     determine_hr_zone()
    #     strava_activity.update(activity_id=activity_id, athlete_id=strava_athlete)
    # else:
    #     pass
    #     # return JsonResponse(data={'message': f'Athlete with id {athlete_id} does not exists in database'},
    #     #                     status=200)
