from typing import Dict

from strava_gateway.models import HeartRateZones

def is_run_activity_race(activity_details: Dict) -> bool:
    return activity_details.get('workout_type', -1) == 1


def set_activity_hr_zone(strava_activity, strava_athlete) -> HeartRateZones:
    if not strava_athlete.hr_zones or not strava_activity.has_heartrate:
        print(f"zones {strava_athlete.hr_zones} {strava_activity.has_heartrate}")
        return None
    def find_zone(avg_hr):
        if (strava_athlete.hr_zones[str(HeartRateZones.Z1.value)][0] <= avg_hr <
                strava_athlete.hr_zones[str(HeartRateZones.Z1.value)][1]):
            return HeartRateZones.Z1
        if (strava_athlete.hr_zones[str(HeartRateZones.Z2.value)][0] <= avg_hr <
                strava_athlete.hr_zones[str(HeartRateZones.Z2.value)][1]):
            return HeartRateZones.Z2
        if strava_athlete.hr_zones[str(HeartRateZones.Z3.value)][0] <= avg_hr < \
                strava_athlete.hr_zones[str(HeartRateZones.Z3.value)][1]:
            return HeartRateZones.Z3
        if strava_athlete.hr_zones[str(HeartRateZones.Z4.value)][0] <= avg_hr < \
                strava_athlete.hr_zones[str(HeartRateZones.Z4.value)][1]:
            return HeartRateZones.Z4
        if avg_hr >= strava_athlete.hr_zones[str(HeartRateZones.Z5.value)][0]:
            return HeartRateZones.Z5
        return None
    a = find_zone(strava_activity.average_heartrate)
    print(f"a: {a}")
    return find_zone(strava_activity.average_heartrate)
