from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime, timedelta
from django.http import JsonResponse

from django.db.models import Sum, Avg
from strava_gateway.models import StravaActivity
import datetime


class TrainingStatsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, year, month):
        weeks = get_weeks_covered_by_month(year, month)
        activities = StravaActivity.objects.filter(start_date__year=year, start_date__week__in=weeks)

        weekly_data = {}
        for week in weeks:
            week_activities = activities.filter(start_date__week=week)
            activities_list = list(week_activities.values('activity_type', 'distance', 'moving_time', 'average_heartrate_zone'))

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
    start_date = datetime.datetime(year, month, 1)
    end_date = start_date + datetime.timedelta(days=31)
    end_date = end_date.replace(day=1) - datetime.timedelta(days=1)
    start_week = start_date.isocalendar()[1]
    end_week = end_date.isocalendar()[1]
    return list(range(start_week, end_week + 1))
