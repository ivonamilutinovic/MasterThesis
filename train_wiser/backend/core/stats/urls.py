from django.urls import path

from .views import TrainingStatsAPIView

urlpatterns = [
    path('<int:year>/<int:month>/', TrainingStatsAPIView.as_view()),
]