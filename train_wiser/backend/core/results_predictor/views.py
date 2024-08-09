from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from transliterate import translit
from unidecode import unidecode

from .predict_results import predict_next_race_time, \
    NoRunnerNameInRaceResultsSet, NoRunnerDataInRaceResultsSet


class ResultPredictor(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        race_distance = request.query_params.get('race_distance')
        if type(race_distance) != str:
            return Response({'error': 'Invalid type of race distance'}, status=status.HTTP_400_BAD_REQUEST)

        runner_name = translate_to_unidecode_and_remove_spaces((request.user.first_name + request.user.last_name).lower().strip())
        try:
            response_text = predict_next_race_time(runner_name, race_distance)
        except NoRunnerNameInRaceResultsSet:
            response_text = "User has no history of races held in Serbia"
        except NoRunnerDataInRaceResultsSet:
            response_text = "User has no history for races of specified distance"

        return Response({"race_result": response_text}, status=status.HTTP_200_OK)

def translate_to_unidecode_and_remove_spaces(text: str):
    return unidecode(translit(text, 'sr', reversed=True).lower().replace(' ', ''))
