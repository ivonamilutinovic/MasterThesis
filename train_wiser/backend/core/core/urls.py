"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from oauth2_provider import urls as oauth2_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('strava_gateway/', include('strava_gateway.urls')),
    path('api/users/', include('users.urls')),
    path('api/results_prediction/', include('results_predictor.urls')),
    path('api/stats/', include('stats.urls')),
    # path('api/activities/', include('activities.urls')),
    path('o/', include(oauth2_urls)),
]

# from django.contrib import admin
# from django.urls import include, path
# from oauth2_provider import urls as oauth2_urls
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('o/', include(oauth2_urls)),
# ]
