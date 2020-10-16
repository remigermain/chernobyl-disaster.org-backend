from django.utils.translation import gettext_lazy as _
from django.core.management.utils import get_random_secret_key
from lib.utils import to_bool
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEBUG = to_bool(os.environ.get("DEBUG", "False"))

DEBUG_TOOLBAR = to_bool(os.environ.get("DEBUG_TOOLBAR", "False"))
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "")


SECRET_KEY = os.environ.get("SECRET_KEY", get_random_secret_key())

SITE_ID = 1

DOMAIN_NAME = os.environ.get("DOMAIN_NAME")
FRONTEND_URL = os.environ.get("FRONTEND_URL")

# SECURITY WARNING: don't run with debug turned on in production!

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # extra package
    'rest_framework',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth.registration',
    'django_filters',
    'corsheaders',
    'django_extensions',
    'imagekit',

    # chenobyl
    'common',
    'authentication',
    'timeline',
    'gallery',
    'populate',
    'utils',
    'lib',

    # extra package
    'dbbackup',
    'django_cleanup.apps.CleanupConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    # cors header
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware'
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

AUTH_USER_MODEL = "authentication.User"
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

MEDIA_URL = "media/"
STATIC_URL = "/static/"

STATIC_ROOT = os.path.join(BASE_DIR, "static")
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

#
# local i18n
#

TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
LANGUAGE_CODE = 'en'
LANGUAGES = [
    ('en', _('English')),
    ('fr', _('Français')),
    ('de', _('Deutsch')),
    ('it', _('Italiano')),
    ('es', _('Español')),
    # ukrainian
    ('uk', _('Українська')),
    # russia
    ('ru', _('русский')),
    # chinese
    ('zh', _('漢語')),
    # japan
    ('ja', _('日本語 (にほんご)')),
]
LANGUAGES.sort(key=lambda x: x[0])
LANGUAGES_DEFAULT = 'en'

#
# rest framework
#
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter',
        'rest_framework.filters.SearchFilter'
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

#
# rest auth / allauth
#

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

APPEND_SLASH = False
REST_AUTH_SERIALIZERS = {
    "USER_DETAILS_SERIALIZER": "authentication.serializers.UserDetailsSerializer",
}

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_AUTHENTICATION_METHOD = 'username'
OLD_PASSWORD_FIELD_ENABLED = True
LOGOUT_ON_PASSWORD_CHANGE = False
ACCOUNT_EMAIL_SUBJECT_PREFIX = ""
EMAIL_SUBJECT_PREFIX = ""

#
# email backend
#
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get("EMAIL_HOST", "localhost")
EMAIL_PORT = os.environ.get("EMAIL_PORT", 587)
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
EMAIL_USE_SSL = False
DEFAULT_FROM_EMAIL = f'Chernobyl disaster <no-reply@{DOMAIN_NAME}>'

GRAPH_MODELS = {
    'all_applications': True,
    'group_models': True,
}


# #-----------------------------------------
#   DEBUG
# #-----------------------------------------
if DEBUG:
    if DEBUG_TOOLBAR:
        INSTALLED_APPS += [
            'debug_toolbar'
        ]
        MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE
        DEBUG_TOOLBAR_PANELS = [
            'debug_toolbar.panels.timer.TimerPanel',
            'debug_toolbar.panels.settings.SettingsPanel',
            'debug_toolbar.panels.headers.HeadersPanel',
            'debug_toolbar.panels.request.RequestPanel',
            'debug_toolbar.panels.sql.SQLPanel',
            'debug_toolbar.panels.cache.CachePanel',
            'debug_toolbar.panels.signals.SignalsPanel',
            'debug_toolbar.panels.logging.LoggingPanel',
        ]
        SHOW_COLLAPSED = True
        SHOW_TEMPLATE_CONTEXT = False

    INTERNAL_IPS = [
        '127.0.0.1'
    ]

    CORS_ORIGIN_ALLOW_ALL = True

    ALLOWED_HOSTS = ['*']

    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    ACCOUNT_EMAIL_VERIFICATION = 'none'

    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'].append(
        'rest_framework.renderers.BrowsableAPIRenderer'
    )

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# # #-----------------------------------------
# #   PRODUCTION
# # #-----------------------------------------

else:
    CORS_ORIGIN_ALLOW_ALL = False
    origin = os.environ.get("CORS_ALLOWED_ORIGINS", None)
    if origin:
        CORS_ALLOWED_ORIGINS = origin.split(",")
    CORS_ALLOW_METHODS = [
        'DELETE',
        'GET',
        'OPTIONS',
        'PATCH',
        'POST',
    ]

    ALLOWED_HOSTS = [
        'localhost',
        '127.0.0.1',
        '[::1]',
        *os.environ.get("ALLOWED_HOSTS", "").split(",")
    ]
    INTERNAL_IPS = []

    DATABASES = {
        "default": {
            "ENGINE": os.environ.get("POSTGRES_ENGINE", "django.db.backends.postgresql"),
            "NAME": os.environ.get("POSTGRES_DB"),
            "USER": os.environ.get("POSTGRES_USER"),
            "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
            "HOST": os.environ.get("POSTGRES_HOST"),
            "PORT": os.environ.get("POSTGRES_PORT"),
        }
    }


# -----------------------------------------
#   BACKUP
# -----------------------------------------
DBBACKUP_GPG_RECIPIENT = os.environ.get("GPG_KEY")
DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {'location': './backup'}


# -----------------------------------------
#   LOGGIN
# -----------------------------------------

if not DEBUG:
    DEFAULT_LOG = ["file", "mail_admins"]
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'file': {
                'class': 'logging.FileHandler',
                'filename': './logs/django.log',
            },
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
            },
            'mail_admins': {
                'level': 'ERROR',
                'class': 'django.utils.log.AdminEmailHandler',
            }
        },
        'loggers': {
            'django': {
                'handlers': DEFAULT_LOG,
                'level': 'WARNING',
                'propagate': True,
            },
            'django.request': {
                'handlers': DEFAULT_LOG,
                'level': 'ERROR',
                'propagate': True,
            },
            'ParserMultiDimensional': {
                'handlers': DEFAULT_LOG,
                'level': 'WARNING',
                'propagate': True,
            },
        },
    }
