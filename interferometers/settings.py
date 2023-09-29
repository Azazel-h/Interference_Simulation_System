from pathlib import Path

import environ
import redis
from secret_key_generator import secret_key_generator

SECRET_KEY = secret_key_generator.generate()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    COMPOSE_PROFILES=(str, 'debug'),
    DJANGO_PORT=(int, 8000),
    WEB_DOMAIN=(str, '127.0.0.1'),
    NGINX_PORT=(int, 8020),
    LDAP_USERNAME=(str, ''),
    LDAP_PASSWORD=(str, ''),
)
environ.Env.read_env(str(BASE_DIR / '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('COMPOSE_PROFILES') == 'debug'

if DEBUG:
    ALLOWED_HOSTS = [
        '*',
    ]
else:
    ALLOWED_HOSTS = [
        env('WEB_DOMAIN'),
        'proxy.bmstu.ru',
    ]

# Application definition

INSTALLED_APPS = [
    # Main applications
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_cas_ng',
    'django.forms',
    'crispy_forms',
    'crispy_bootstrap4',
    # Project applications
    'accounts',
    'fabry_perot',
    'michelson',
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django_cas_ng.middleware.CASMiddleware',
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'accounts.backends.AuthBackend',
)

AUTH_USER_MODEL = 'accounts.CASUser'

ROOT_URLCONF = 'interferometers.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {
                'paginator_tags': 'templates.tags.paginator_tags',
                'list_tags': 'templates.tags.list_tags',
                'attribute_tags': 'templates.tags.attribute_tags',
            },
        },
    },
]

WSGI_APPLICATION = 'interferometers.wsgi.application'

# Cache

REDIS_CON = redis.Redis('redis')

try:
    REDIS_CON.ping()

    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': 'redis://redis/1',
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            },
        },
    }
except redis.ConnectionError:
    pass
finally:
    REDIS_CON.close()

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'CONN_MAX_AGE': 600,
    },
}

# Sessions

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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

# CAS config

CAS_SERVER_URL = 'https://proxy.bmstu.ru:8443/cas/'
CAS_VERSION = '3'

# LDAP config

LDAP_USERNAME = env('LDAP_USERNAME')
LDAP_PASSWORD = env('LDAP_PASSWORD')

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'

if DEBUG:
    STATICFILES_DIRS = [
        BASE_DIR / 'static',
    ]
else:
    STATIC_ROOT = BASE_DIR / 'static'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'
