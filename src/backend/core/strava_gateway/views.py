from typing import List
import requests
from django.http import HttpRequest
from django.http import HttpResponse

from decouple import config

from .models import StravaAthlete

REQUIRED_SCOPE_TOKENS = ['read', 'activity:read_all']


# TODO: Upgrade return response in case of errors
def token_exchange(request: HttpRequest):
    if request.method != 'GET':
        return HttpResponse("<p>Not allowed</p>")  # TODO: Return 405 status code

    if request.GET.get('error'):
        return HttpResponse(f"<p>Error: {request.GET.get('error')}.</p>")

    scope: str = request.GET.get('scope')
    scope_tokens: List[str] = scope.split(',')

    for required_scope_token in REQUIRED_SCOPE_TOKENS:
        if required_scope_token not in scope_tokens:
            return HttpResponse(f"<p>Error: Required scope is {REQUIRED_SCOPE_TOKENS}.</p>")

    post_config = {'client_id': config("CLIENT_ID"),
                   'client_secret': config("CLIENT_SECRET"),
                   'code': request.GET.get('code'),
                   'grant_type': 'authorization_code'}
    response = requests.post(url="https://www.strava.com/api/v3/oauth/token", json=post_config)
    if response.status_code != 200:
        return HttpResponse(f"<p>Error: Status code should be 200, instead it is {response.status_code}.</p>")

    response_json = response.json()

    athlete_id = response_json.get('athlete').get('id')
    if StravaAthlete.objects.filter(athlete_id=athlete_id).exists():
        return HttpResponse(f"<p>Error: Athlete with id {athlete_id} is already registered "
                            f"in Train wiser app.</p>")
        # TODO: Maybe handle this by updating data

    strava_athlete = StravaAthlete.objects.create(athlete_id=response_json.get('athlete').get('id'),
                                                  expires_at=response_json.get('expires_at'),
                                                  access_token=response_json.get('access_token'),
                                                  refresh_token=response_json.get('refresh_token'))

    return HttpResponse(f"<p>Code: {request.GET.get('code')}, scope {scope_tokens}, response code: "
                        f"{response.status_code}, response content: {response.json()}\nTest {strava_athlete}\n"
                        f"{response_json.get('athlete').get('id')}.</p>")

