import logging
from typing import List

import requests
from decouple import config
from django.http import HttpRequest, JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import StravaAthlete

REQUIRED_SCOPE_TOKENS = ['read', 'activity:read_all']

logger = logging.getLogger(__name__)


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
                                                  access_token_expires_at=response_json.get('expires_at'),
                                                  access_token=response_json.get('access_token'),
                                                  refresh_token=response_json.get('refresh_token'))

    return HttpResponse(f"<p>Code: {request.GET.get('code')}, scope {scope_tokens}, response code: "
                        f"{response.status_code}, response content: {response.json()}\nTest {strava_athlete}\n"
                        f"{response_json.get('athlete').get('id')}.</p>")

@csrf_exempt
def webhook_subscription(request: HttpRequest):
    if request.method == 'POST':
        post_config = {'client_id': config("CLIENT_ID"),
                       'client_secret': config("CLIENT_SECRET"),
                       'callback_url': f"https://{config('HOSTNAME1')}/strava_gateway/{config('WEBHOOK_ENDPOINT')}",
                       'verify_token': 'STRAVA_WEBHOOK_SUBSCRIPTION'}  # TODO: Generate random token

        logger.info(str(post_config))
        response = requests.post(url="https://www.strava.com/api/v3/push_subscriptions", json=post_config)
        config['SUBSCRIPTION_ID'] = '123'

        return HttpResponse(content=response.content, status=response.status_code)


def webhook_callback(request: HttpRequest):
    if request.method == "GET" and request.GET.get('hub.challenge') and request.GET.get('hub.mode') == 'subscribe' and \
            request.GET.get('hub.verify_token') == 'STRAVA_WEBHOOK_SUBSCRIPTION':
        return JsonResponse(data={'hub.challenge': request.GET.get('hub.challenge')}, status=200)
    else:
        return JsonResponse(data={}, status=400)
