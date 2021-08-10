"""
Django settings for passport project.

Generated by 'django-admin startproject' using Django 2.2.18.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
import os.path
import tempfile
import ldap
import dj_database_url

from django_auth_ldap.config import LDAPSearch, GroupOfNamesType

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.environ.get('DRYCC_DEBUG', True))

# If set to True, Django's normal exception handling of view functions
# will be suppressed, and exceptions will propagate upwards
# https://docs.djangoproject.com/en/2.2/ref/settings/#debug-propagate-exceptions
DEBUG_PROPAGATE_EXCEPTIONS = True

# Silence two security messages around SSL as router takes care of them
# https://docs.djangoproject.com/en/2.2/ref/checks/#security
SILENCED_SYSTEM_CHECKS = [
    'security.W004',
    'security.W008'
]

CONN_MAX_AGE = 60 * 3

# SECURITY: change this to allowed fqdn's to prevent host poisioning attacks
# https://docs.djangoproject.com/en/2.2/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = os.environ.get('TZ', 'UTC')

USE_I18N = False

USE_L10N = False

USE_TZ = True

# Passport templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.request",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages"
            ],
        },
    },
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'api.middleware.APIVersionMiddleware',
]

ROOT_URLCONF = 'passport.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'api.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    # Third-party apps
    'corsheaders',
    'guardian',
    'gunicorn',
    'jsonfield',
    'rest_framework',
    'rest_framework.authtoken',
    'oauth2_provider',
    # passport apps
    'api'
)

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "guardian.backends.ObjectPermissionBackend",
)

ANONYMOUS_USER_ID = -1
LOGIN_URL = '/user/login/'
LOGIN_REDIRECT_URL = '/'

# Security settings
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
)
CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'content-type',
    'accept',
    'origin',
    'Authorization',
    'Host',
    'user-agent',
    'x-csrftoken',
    'DRYCC_API_VERSION',
    'DRYCC_PLATFORM_VERSION',
)
CORS_EXPOSE_HEADERS = (
    'DRYCC_API_VERSION',
    'DRYCC_PLATFORM_VERSION',
)

X_FRAME_OPTIONS = 'DENY'
# todo debug oauth2
# CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SAMESITE = None
# SESSION_COOKIE_SECURE = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

# Honor HTTPS from a trusted proxy
# see https://docs.djangoproject.com/en/2.2/ref/settings/#secure-proxy-ssl-header
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# standard datetime format used for logging, model timestamps, etc.
DRYCC_DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
# django admin datetime format
DATETIME_FORMAT = "Y-m-d H:i:s e"

REST_FRAMEWORK = {
    'DATETIME_FORMAT': DRYCC_DATETIME_FORMAT,
    'DEFAULT_MODEL_SERIALIZER_CLASS': 'rest_framework.serializers.ModelSerializer',
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 30,
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'EXCEPTION_HANDLER': 'api.exceptions.custom_exception_handler'
}

# URLs that end with slashes are ugly
APPEND_SLASH = False

# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {'level': 'DEBUG' if DEBUG else 'WARN'},
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'filters': ['require_debug_true'],
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'WARNING',
            'filters': ['require_debug_true'],
            'propagate': True,
        },
        'api': {
            'handlers': ['console'],
            'propagate': True,
        },
        'registry': {
            'handlers': ['console'],
            'propagate': True,
        },
        'scheduler': {
            'handlers': ['console'],
            'propagate': True,
        },
    }
}
# TEST_RUNNER = 'api.tests.SilentDjangoTestSuiteRunner'

# default drycc passport settings
LOG_LINES = 100
TEMPDIR = tempfile.mkdtemp(prefix='drycc')

# names which apps cannot reserve for routing
DRYCC_RESERVED_NAMES = os.environ.get('RESERVED_NAMES', '').\
    replace(' ', '').split(',')

# security keys and auth tokens
random_secret = ')u_jckp95wule8#wxd8sm!0tj2j&aveozu!nnpgl)2x&&16gfj'
SECRET_KEY = os.environ.get('DRYCC_SECRET_KEY', random_secret)

# database setting
DRYCC_DATABASE_URL = os.environ.get('DRYCC_DATABASE_URL', 'postgres://postgres:123456@192.168.6.50:5432/drycc_passport')
DATABASES = {
    'default': dj_database_url.config(default=DRYCC_DATABASE_URL,
                                      conn_max_age=600)
}

# Redis Configuration
DRYCC_REDIS_ADDRS = os.environ.get('DRYCC_REDIS_ADDRS', '127.0.0.1:6379').split(
    ",")
DRYCC_REDIS_PASSWORD = os.environ.get('DRYCC_REDIS_PASSWORD', '')

# Cache Configuration
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": ['redis://:{}@{}'.format(DRYCC_REDIS_PASSWORD, DRYCC_REDIS_ADDR) \
                     for DRYCC_REDIS_ADDR in DRYCC_REDIS_ADDRS],  # noqa
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.ShardClient",
        }
    }
}

# LDAP settings taken from environment variables.
LDAP_ENDPOINT = os.environ.get('LDAP_ENDPOINT', '')
LDAP_BIND_DN = os.environ.get('LDAP_BIND_DN', '')
LDAP_BIND_PASSWORD = os.environ.get('LDAP_BIND_PASSWORD', '')
LDAP_USER_BASEDN = os.environ.get('LDAP_USER_BASEDN', '')
LDAP_USER_FILTER = os.environ.get('LDAP_USER_FILTER', 'username')
LDAP_GROUP_BASEDN = os.environ.get('LDAP_GROUP_BASEDN', '')
LDAP_GROUP_FILTER = os.environ.get('LDAP_GROUP_FILTER', '')
LDAP_ACTIVE_GROUP = os.environ.get('LDAP_ACTIVE_GROUP', '')
LDAP_STAFF_GROUP = os.environ.get('LDAP_STAFF_GROUP', '')
LDAP_SUPERUSER_GROUP = os.environ.get('LDAP_SUPERUSER_GROUP', '')

# Django LDAP backend configuration.
# See https://pythonhosted.org/django-auth-ldap/reference.html
# for variables' details.
# In order to debug LDAP configuration it is possible to enable
# verbose logging from auth-ldap plugin:
# https://pythonhosted.org/django-auth-ldap/logging.html

if LDAP_ENDPOINT:
    AUTHENTICATION_BACKENDS = ("django_auth_ldap.backend.LDAPBackend",) + AUTHENTICATION_BACKENDS  # noqa
    AUTH_LDAP_SERVER_URI = LDAP_ENDPOINT
    AUTH_LDAP_BIND_DN = LDAP_BIND_DN
    AUTH_LDAP_BIND_PASSWORD = LDAP_BIND_PASSWORD
    AUTH_LDAP_USER_SEARCH = LDAPSearch(
        base_dn=LDAP_USER_BASEDN,
        scope=ldap.SCOPE_SUBTREE,
        filterstr="%s" % LDAP_USER_FILTER
    )
    AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
        base_dn=LDAP_GROUP_BASEDN,
        scope=ldap.SCOPE_SUBTREE,
        filterstr="%s" % LDAP_GROUP_FILTER
    )
    AUTH_LDAP_USER_FLAGS_BY_GROUP = {
        'is_active': LDAP_ACTIVE_GROUP,
        'is_staff': LDAP_STAFF_GROUP,
        'is_superuser': LDAP_SUPERUSER_GROUP,
    }
    AUTH_LDAP_GROUP_TYPE = GroupOfNamesType()
    AUTH_LDAP_USER_ATTR_MAP = {
        "first_name": "givenName",
        "last_name": "sn",
        "email": "mail",
        "username": LDAP_USER_FILTER,
    }
    AUTH_LDAP_GLOBAL_OPTIONS = {
        ldap.OPT_X_TLS_REQUIRE_CERT: False,
        ldap.OPT_REFERRALS: False
    }
    AUTH_LDAP_ALWAYS_UPDATE_USER = True
    AUTH_LDAP_MIRROR_GROUPS = True
    AUTH_LDAP_FIND_GROUP_PERMS = True
    AUTH_LDAP_CACHE_GROUPS = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, 'static'))

# see: https://django-oauth-toolkit.readthedocs.io/en/latest/oidc.html?highlight=oidc.key#creating-rsa-private-key  # noqa
with open('/var/run/secrets/drycc/passport/oidc-rsa-private-key') as f:
    OIDC_RSA_PRIVATE_KEY = f.read()
OAUTH2_PROVIDER = {
    "OIDC_ENABLED": True,
    "OIDC_RSA_PRIVATE_KEY": OIDC_RSA_PRIVATE_KEY,
    "OAUTH2_VALIDATOR_CLASS": "api.serializers.CustomOAuth2Validator",
    "PKCE_REQUIRED": False,
    "ALLOWED_REDIRECT_URI_SCHEMES": ["http", "https"],
    "ACCESS_TOKEN_EXPIRE_SECONDS": int(os.environ.get('ACCESS_TOKEN_EXPIRE_SECONDS', 30 * 86400)),  # noqa
    "ID_TOKEN_EXPIRE_SECONDS": int(os.environ.get('ID_TOKEN_EXPIRE_SECONDS', 30 * 86400)),  # noqa
    "AUTHORIZATION_CODE_EXPIRE_SECONDS": int(os.environ.get('AUTHORIZATION_CODE_EXPIRE_SECONDS', 600)),  # noqa
    "CLIENT_SECRET_GENERATOR_LENGTH": int(os.environ.get('CLIENT_SECRET_GENERATOR_LENGTH', 64)),  # noqa
    "REFRESH_TOKEN_EXPIRE_SECONDS": int(os.environ.get('REFRESH_TOKEN_EXPIRE_SECONDS', 60 * 86400)),  # noqa
    "ROTATE_REFRESH_TOKEN": True,
    "SCOPES": {
        "profile": "Profile",
        "openid": "OpenID Connect scope",
    },
    "DEFAULT_SCOPES": ['openid', ],
    "DEFAULT_CODE_CHALLENGE_METHOD": 'S256',
}
REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] = (
    'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    'rest_framework.authentication.SessionAuthentication',
    'rest_framework.authentication.BasicAuthentication',
)

EMAIL_HOST = os.environ.get('EMAIL_HOST', '')
EMAIL_PORT = os.environ.get('EMAIL_PORT', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', '')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', True)
EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL', True)
