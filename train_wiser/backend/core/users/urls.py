from django.urls import path

from .views import UserRegister, UserAccount

urlpatterns = [
    path('register/', UserRegister.as_view()),
    # path('account/<str:username>/', UserAccount.as_view()),
    path('me/', UserAccount.as_view()),
]
