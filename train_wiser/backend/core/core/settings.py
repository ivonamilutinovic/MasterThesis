"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.2.10.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path

from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['feasible-brightly-cobra.ngrok-free.app', 'localhost', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 3rd party
    "rest_framework",
    "corsheaders",
    "django_crontab",
    "oauth2_provider",
    #"rest_framework.authtoken",
    # local
    "strava_gateway.apps.StravaGatewayConfig",
    "users.apps.UsersConfig",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'oauth2_provider.middleware.OAuth2TokenMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'users.CustomUser'
LOGIN_URL = '/admin/login/'

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        'rest_framework.permissions.IsAuthenticated',
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    ],
}


OAUTH2_PROVIDER = {
    'OAUTH2_BACKEND_CLASS': 'oauth2_provider.oauth2_backends.JSONOAuthLibCore',
    'ACCESS_TOKEN_EXPIRE_SECONDS': 3600
}


CRONJOBS = [
    ('* */1 * * *', 'strava_gateway.tasks.activity_backfill',
     '>> ' + os.path.join('/home/hp/Desktop', 'train_wiser_crontab.log' + ' 2>&1 ')),
    # ('* */1 * * *', 'strava_gateway.tasks.fill_athlete_hr_zone',
    #  '>> ' + os.path.join('/home/hp/Desktop', 'train_wiser_hr_zone.log' + ' 2>&1 ')),
    # ('* */1 * * *', 'strava_gateway.tasks.fill_activity_hr_zone',
    #  '>> ' + os.path.join('/home/hp/Desktop', 'train_wiser_hr_zone_act.log' + ' 2>&1 ')),
    # ('30 */1 * * *', 'strava_gateway.tasks.fetch_activity_data')
]


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'train_wiser_django.log',
            'formatter': 'verbose'
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'scraper_file' : {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'scraping.log',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'scraper': {
            'handlers': ['scraper_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django_crontab': {
            'handlers': ['scraper_file'],
            'level': 'DEBUG',
            'propagate': True,
        },

        'django_crontab.crontab': {
            'handlers': ['scraper_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'crontab': {
            'handlers': ['scraper_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'scraper.django_crontab.crontab': {
            'handlers': ['scraper_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'scraper.tasks': {
            'handlers': ['scraper_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
