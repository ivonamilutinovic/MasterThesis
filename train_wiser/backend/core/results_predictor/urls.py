from django.urls import path

from .views import ResultPredictor

urlpatterns = [
    path('result_prediction/', ResultPredictor.as_view()),
]