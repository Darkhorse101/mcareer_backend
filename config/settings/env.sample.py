from .base import *

INSTALLED_APPS += (
    'debug_toolbar',
    'drf_yasg',
    'django_extensions'
)

MIDDLEWARE += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "DEMO_TEST",
        "USER": "postgres",
        "PASSWORD": "hellonepal",
        "HOST": "localhost",
        "PORT": "5432",
        "CONN_MAX_AGE": 600,
    }
}

INTERNAL_IPS = ['127.0.0.1', ]

ALLOWED_HOSTS = ['*']

CORS_ORIGIN_ALLOW_ALL = True

EMAIL_HOST = 'your host'
EMAIL_HOST_USER = 'username'
EMAIL_HOST_PASSWORD = 'pasword'
EMAIL_PORT = '1234'
