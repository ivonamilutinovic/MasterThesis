from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum, Avg
from strava_gateway.models import StravaActivity
from datetime import datetime, timedelta
import calendar


class TrainingStatsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, year, month):
        weeks = get_weeks_covered_by_month(year, month)
        activities = StravaActivity.objects.filter(start_date__year=year, start_date__week__in=weeks)

        weekly_data = {}
        for week in weeks:
            week_activities = activities.filter(start_date__week=week)
            activities_list = list(week_activities.values('activity_type', 'distance', 'moving_time',
                                                          'average_heartrate_zone', 'start_date'))

            summary = week_activities.values('activity_type').annotate(
                total_duration=Sum('moving_time'),
                total_distance=Sum('distance'),
                average_heartrate_zone=Avg('average_heartrate_zone')
            )

            weekly_data[week] = {
                'activities': [
                    {**activity,
                     'distance': round(activity['distance'], 2) if activity['distance'] else 0,
                     'duration': activity['moving_time'],
                     'start_date': activity['start_date'].date()
                    } for activity in activities_list
                ],
                'summary': {
                    entry['activity_type']: {
                        'total_duration': entry['total_duration'],
                        'total_distance': round(entry['total_distance'], 2) if entry['activity_type'] != 'WeightTraining' else 0,
                        'average_heartrate_zone': round(entry['average_heartrate_zone']) if entry['average_heartrate_zone'] else 0
                    } for entry in summary
                }
            }

        return Response({'training_weeks': weekly_data})


def get_weeks_covered_by_month(year, month):
    first_day_of_month = datetime(year, month, 1)
    last_day_of_month = datetime(year, month, calendar.monthrange(year, month)[1])

    # Start from the Monday of the week containing the first day of the month
    start_date = first_day_of_month - timedelta(days=first_day_of_month.weekday())
    # End on the Sunday of the week containing the last day of the month
    end_date = last_day_of_month + timedelta(days=(6 - last_day_of_month.weekday()))

    start_week = start_date.isocalendar()[1]
    end_week = end_date.isocalendar()[1]
    return list(range(start_week, end_week + 1))
