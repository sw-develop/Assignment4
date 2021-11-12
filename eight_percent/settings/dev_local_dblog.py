from .dev_local   import *


LOGGING = {
    'disable_existing_loggers': False,
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'duration',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        }
    },
    'formatters': {
        'duration': {
            'format': 'Time: {duration:.8f} s\nSQL: {sql}\nArgs: {params}',
            'style': '{'
        }
    }
}