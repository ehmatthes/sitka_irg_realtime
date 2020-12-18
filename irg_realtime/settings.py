"""
Django settings for irg_realtime project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'm*+^g4oo2^85re_37k&bmg@dq&#u=3c1(di!cb=2@r^uy#p=t='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    # My apps.
    'irg_viz',
    'accounts',

    # Third party apps.
    'bootstrap4',
    'django_extensions',
    'anymail',

    # Default apps.
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # django-allauth apps.
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
]

# django-allauth settings
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

SITE_ID = 1
ACCOUNT_EMAIL_VERIFICATION = 'none'
LOGIN_REDIRECT_URL = 'irg_viz:index'



ANYMAIL = {
    # Settings here for sendgrid.
}
DEFAULT_FROM_EMAIL = "eric@ehmatthes.com"
SERVER_EMAIL = "eric@ehmatthes.com"

if os.environ.get('SERVER_ENVIRONMENT') == 'local':
    print("Using local settings.")
    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
    EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'sent_emails')
    BASE_URL = 'http://localhost:8000'
elif os.environ.get('SERVER_ENVIRONMENT') == 'production':
    print("Using production settings.")
    EMAIL_BACKEND = "anymail.backends.sendgrid.EmailBackend"
    SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
    BASE_URL = 'http://localhost:8000'
else:
    raise Exception('Unknown production environment')



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'irg_realtime.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'irg_realtime.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

AUTH_USER_MODEL = 'accounts.CustomUser'

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

# These are the places Django will look for static files when running collectstatic.
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "irg_realtime/static/")
]

STATIC_URL = '/static/'

# This is where static files will be collected to.
#  This is the directory that will be overwritten on each collectstatic call.
if os.environ.get('ENVIRON') == 'LOCAL':
    STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
    print(f"STATIC_ROOT: {STATIC_ROOT}")
elif os.environ.get('ENVIRON') == 'DEPLOYED':
    STATIC_ROOT = '/srv/irg_realtime/static/'

# My settings.
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = 'media/'

LOGIN_URL = '/accounts/login/'

if os.environ.get('ENVIRON') == 'DEPLOYED':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'my_irg_db',
            'USER': 'my_irg_db_user',
            'PASSWORD': 'my_irg_db_wonder',
            'HOST': 'localhost',
            'PORT': '',
        }
    }

    STATIC_ROOT = '/home/ehmatthes/irg_realtime/static/'
    STATIC_URL = '/static/'

    ALLOWED_HOSTS = ['167.71.116.184']