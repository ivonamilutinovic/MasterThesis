from django.urls import path

from .views import ResultPredictor

urlpatterns = [
    path('', ResultPredictor.as_view()),
]