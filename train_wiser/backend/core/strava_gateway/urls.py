from decouple import config
from django.urls import path

from .views import token_exchange, webhook_subscription, webhook_callback

urlpatterns = [
    path("token_exchange/", token_exchange, name="token_exchange"),
    path("webhook_subscription/", webhook_subscription, name="webhook_subscription"),
    path(config("STRAVA_WEBHOOK_ENDPOINT"), webhook_callback, name="webhook_callback")
]
