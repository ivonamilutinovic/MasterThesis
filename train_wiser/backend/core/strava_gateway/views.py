import json
import logging
from typing import List

import requests
from decouple import config
from django.http import HttpRequest, JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import StravaAthlete, StravaSettings, StravaActivity
from .utils.athlete_utils import set_athlete_hr_zone

REQUIRED_SCOPE_TOKENS = ['read', 'activity:read_all', 'profile:read_all']

logger = logging.getLogger(__name__)


# TODO: Upgrade return response in case of errors
def token_exchange(request: HttpRequest):
    if request.method != 'GET':
        return HttpResponse("<p>Not allowed</p>", status=405)

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
                            f"in Train Wiser application.</p>")

    strava_athlete = StravaAthlete.objects.create(athlete_id=response_json.get('athlete').get('id'),
                                                  access_token_expires_at=response_json.get('expires_at'),
                                                  access_token=response_json.get('access_token'),
                                                  refresh_token=response_json.get('refresh_token'))

    set_athlete_hr_zone(strava_athlete)

    return HttpResponse(f"<p>Code: {request.GET.get('code')}, scope {scope_tokens}, response code: "
                        f"{response.status_code}, response content: {response.json()}\nTest {strava_athlete}\n"
                        f"{response_json.get('athlete').get('id')}.</p>")

@csrf_exempt
def webhook_subscription(request: HttpRequest):
    subscription_id = StravaSettings.objects.filter(setting_key='subscription_id')

    if subscription_id.exists() and subscription_id.setting_value is not None:
        return HttpResponse(content="<p>Subscription already exists.</p>")

    if request.method == 'POST':
        post_config = {'client_id': config("CLIENT_ID"),
                       'client_secret': config("CLIENT_SECRET"),
                       'callback_url': f"https://{config('HOSTNAME1')}/strava_gateway/{config('WEBHOOK_ENDPOINT')}",
                       'verify_token': 'STRAVA_WEBHOOK_SUBSCRIPTION'}

        response = requests.post(url="https://www.strava.com/api/v3/push_subscriptions", json=post_config)
        if response.status_code == 201:
            StravaSettings.objects.create(setting_key='subscription_id', setting_value=str(response.json().get('id')))

        return HttpResponse(content=response.content, status=response.status_code)


@csrf_exempt
def webhook_callback(request: HttpRequest):
    if request.method == "GET" and request.GET.get('hub.challenge') and request.GET.get('hub.mode') == 'subscribe' and \
            request.GET.get('hub.verify_token') == 'STRAVA_WEBHOOK_SUBSCRIPTION':
        return JsonResponse(data={'hub.challenge': request.GET.get('hub.challenge')}, status=200)
    elif request.method == 'POST':
        # We are only writing activity_id in database, full activity will be written separately with Cron job
        request_data = json.loads(request.body)
        subscription_id_from_request = request_data.get('subscription_id')
        subscription_id_in_db = StravaSettings.objects.filter(setting_key='subscription_id')

        is_subscription_id_valid = subscription_id_from_request == int(subscription_id_in_db.get().setting_value) \
            if subscription_id_in_db.exists() else False
        if not is_subscription_id_valid:
            return JsonResponse(data={'message': f'Subscription id is not valid, '
                                          f'subscription id from request: {subscription_id_from_request}, '
                                          f'subscription from db (value): {subscription_id_in_db.get().setting_value}, '
                                      },
                                status=200)

        object_type = request_data.get('object_type')
        if not object_type or object_type != 'activity':
            return JsonResponse(data={'message': 'Object type is not activity'}, status=200)
        activity_id = request_data.get('object_id')
        if not activity_id:
            return JsonResponse(data={'message': 'Activity id is not available'}, status=200)
        aspect_type = request_data.get('aspect_type')
        if not aspect_type or aspect_type != 'create':
            return JsonResponse(data={'message': 'Aspect type different than "create" are not relevant'}, status=200)
        athlete_id = request_data.get('owner_id')
        if not athlete_id:
            return JsonResponse(data={'message': 'Athlete id is not available'}, status=200)

        if StravaAthlete.objects.filter(athlete_id=athlete_id).exists():
            strava_athlete = StravaAthlete.objects.filter(athlete_id=athlete_id).get()
            StravaActivity.objects.create(activity_id=activity_id, athlete_id=strava_athlete)
            return JsonResponse(data={'message': 'Activity and athlete ids are read successfully'}, status=200)
        else:
            return JsonResponse(data={'message': f'Athlete with id {athlete_id} does not exists in database'},
                                status=200)
