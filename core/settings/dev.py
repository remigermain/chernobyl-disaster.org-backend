from .base import *

DEBUG = True

CORS_ORIGIN_ALLOW_ALL = True

ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

GRAPH_MODELS = {
  'all_applications': True,
  'group_models': True,
}
