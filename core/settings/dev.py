from .base import *

DEBUG = True

CORS_ORIGIN_ALLOW_ALL = True

ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_USE_TLS = False

GRAPH_MODELS = {
  'all_applications': True,
  'group_models': True,
}

ACCOUNT_EMAIL_VERIFICATION = 'none'
