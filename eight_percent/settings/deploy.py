from .base   import *


ALLOWED_HOSTS = ['*']

SECRET_KEY = get_env_variable('DJANGO_SECRET_KEY')
DEBUG      = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}