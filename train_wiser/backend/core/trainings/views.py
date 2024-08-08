from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import random

class TrainingsView(APIView):
    def get(self, request):
        goal_time = request.query_params.get('goal_time')
        race_distance = request.query_params.get('race_distance')
        if not goal_time or not goal_time.isdigit():
            return Response({'error': 'Invalid goal_time'}, status=status.HTTP_400_BAD_REQUEST)

        if not race_distance:
            try:
                float(race_distance)
            except ValueError:
                return Response({'error': 'Invalid race_distance'}, status=status.HTTP_400_BAD_REQUEST)

        mock_data = [
            [[{'activity_type':'Run', 'distance': 5.0, 'duration': 3600, 'average_heartrate_zone': 4}],
             [{'activity_type':'WeightTraining', 'distance': 0, 'duration': 7200, 'average_heartrate_zone': 1}],
             [{'activity_type':'Rest day', 'distance': 0, 'duration': 0, 'average_heartrate_zone': 0}],
             [{'activity_type':'Ride', 'distance': 20.0, 'duration': 5400, 'average_heartrate_zone': 3}],
             [{'activity_type':'Run', 'distance': 10.0, 'duration': 7200, 'average_heartrate_zone': 4}],
             [{'activity_type':'Rest day', 'distance': 0, 'duration': 0, 'average_heartrate_zone': 0}],
             [{'activity_type':'Rest day', 'distance': 0, 'duration': 0, 'average_heartrate_zone': 0}]],
        ] * 8

        return Response(mock_data, status=status.HTTP_200_OK)
