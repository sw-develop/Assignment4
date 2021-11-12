from .base   import *


ALLOWED_HOSTS = ['*']

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'secrect_key')
DEBUG      = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}