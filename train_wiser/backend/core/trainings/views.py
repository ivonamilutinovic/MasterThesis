from datetime import timedelta
from math import floor

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import F, Value, IntegerField
from django.db.models.functions import Abs

from strava_gateway.models import StravaActivity


class TrainingsView(APIView):
    def get(self, request):
        goal_time = request.query_params.get('goal_time')
        race_distance = request.query_params.get('race_distance')

        if not goal_time:
            return Response({'error': 'Race goal time not provided'}, status=status.HTTP_400_BAD_REQUEST)
        if not goal_time.isdigit():
            return Response({'error': 'Invalid type of race goal time'}, status=status.HTTP_400_BAD_REQUEST)
        goal_time = int(goal_time)

        if not race_distance:
            return Response({'error': 'Race distance not provided'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            race_distance = float(race_distance)
        except ValueError:
            return Response({'error': 'Invalid type of race distance'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            matching_races = get_matching_races_per_distance(race_distance)
            if not matching_races:
                return Response({'error': 'There are no trainings available for specified distance'},
                                status=status.HTTP_404_NOT_FOUND)

            closest_races = get_closest_races(matching_races, goal_time)

            training_plan_responses = {}
            training_plan_counter = 0
            number_of_training_days = race_dist_training_weeks[floor(race_distance)] * 7 - 1
            for closest_race in closest_races:
                first_training_day = (closest_race.start_date - timedelta(days=number_of_training_days)).date()
                current_date = first_training_day
                training_plan_response = []
                day_counter = 0
                week_counter = 0
                day_in_week_counter = 0

                try:
                    while current_date <= closest_race.start_date.date():
                        if day_in_week_counter % 7 == 0:
                            training_plan_response.append([])
                            day_in_week_counter = 0
                        training_plan_response[week_counter].append([])

                        if StravaActivity.objects.filter(athlete_id=closest_race.athlete_id,
                                                         start_date__date=current_date).exists():
                            trainings = StravaActivity.objects.filter(athlete_id=closest_race.athlete_id,
                                                          start_date__date=current_date)
                            for training in trainings:
                                (training_plan_response[week_counter][day_in_week_counter]
                                 .append({'activity_type': training.activity_type,
                                          'distance': round(training.distance, 2),
                                          'duration': training.moving_time,
                                          'avg_hr_zone': training.average_heartrate_zone}))
                        else:
                            (training_plan_response[week_counter][day_in_week_counter]
                             .append({'activity_type': 'RestDay',
                                      'distance': 0,
                                      'duration': 0,
                                      'avg_hr_zone': 0}))

                        current_date += timedelta(days=1)
                        day_counter += 1
                        day_in_week_counter += 1
                        if day_in_week_counter % 7 == 0:
                            week_counter += 1

                    calculate_difference = None
                    if request.user.strava_athlete_id:
                        calculate_difference = get_hr_zones_difference(request.user, closest_race.athlete_id)
                    calculate_difference = f" - HR Zones Dissimilarity {calculate_difference}%" \
                        if calculate_difference != "" else ""
                    tp_key = (f"Training Plan {training_plan_counter + 1} - "
                              f"{seconds_to_hms(closest_race.moving_time)}{calculate_difference}")
                    training_plan_responses[tp_key] = training_plan_response
                    training_plan_counter += 1
                except IndexError as error:
                    raise IndexError(f"{error} + indexes {training_plan_response} || {day_counter}  "
                                     f"{day_in_week_counter}  {week_counter}")
        except RuntimeError as error:
            return Response({'error': f"Error during training plan generation: {error}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(training_plan_responses, status=status.HTTP_200_OK)


race_dist_training_weeks = {
    5: 6,
    7: 8,
    10: 8,
    21: 12,
    42: 16
}

def get_matching_races_per_distance(race_distance: float):
    return StravaActivity.objects.filter(is_race=True, rounded_race_distance=race_distance)


def get_closest_races(matching_races, target_time):
    matching_races = matching_races.annotate(
        time_difference=Abs(F('moving_time') - Value(target_time, output_field=IntegerField()))
    )
    matching_races = matching_races.order_by('time_difference')
    closest_races = matching_races[:5]

    return closest_races

def seconds_to_hms(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"


def get_hr_zones_difference(current_user, athlete_user_id):
    if not (current_user.strava_athlete_id.hr_zones and athlete_user_id.hr_zones):
        return None

    current_user_zones = current_user.strava_athlete_id.hr_zones
    athlete_zones = athlete_user_id.hr_zones

    total_difference = 0.0
    num_keys = 0
    for key in ["2", "3", "4", "5"]:
        value_current_user_zones = current_user_zones[key][0]
        value_athlete_zones = athlete_zones[key][0]

        if value_current_user_zones == 0:
            continue

        difference = (value_athlete_zones - value_current_user_zones) / value_current_user_zones
        total_difference += difference
        num_keys += 1

    if num_keys == 0:
        return None

    average_difference = total_difference / num_keys
    percentage_difference = average_difference * 100

    return percentage_difference
