from django.urls import path

from .views import TrainingsView

urlpatterns = [
    path('', TrainingsView.as_view()),
]
