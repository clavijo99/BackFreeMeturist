from .common import *
from .partials.util import get_secret

DEBUG = False

# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

ALLOWED_HOSTS = ['free-meturist-back.mi-server.cloud']
CSRF_TRUSTED_ORIGINS = ['https://free-meturist-back.mi-server.cloud']
SECRET_KEY = get_secret('DJANGO_SECRET_KEY')

if get_secret('DATABASE_URL'):
    import dj_database_url

    DATABASES = {
        'default': dj_database_url.config()
    }
else:
    POSTGRES_USER = get_secret('POSTGRES_USER')
    POSTGRES_PASSWORD = get_secret('POSTGRES_PASSWORD')

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'free-meturist-back',
            'USER': POSTGRES_USER,
            'PASSWORD': POSTGRES_PASSWORD,
            'HOST': 'db',
            'PORT': 5432,
        }
    }

# Email Config
"""
EMAIL_PASSWORD = get_secret('EMAIL_PASSWORD')
EMAIL_HOST = 'smtp.free-meturist-back.com'
EMAIL_HOST_USER = 'free-meturist-back'
EMAIL_HOST_PASSWORD = EMAIL_PASSWORD
"""
