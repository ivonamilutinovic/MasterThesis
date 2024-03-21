from django.urls import path
from . import views

urlpatterns = [
    path('signup-account/', views.signup_account, name='signup-account'),
]
