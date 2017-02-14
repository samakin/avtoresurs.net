"""
Django settings for avtoresurs_new project.

Generated by 'django-admin startproject' using Django 1.10.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from avtoresurs_new.local_settings import DB

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'f9vp_6q99r9gk$ptg2j@8p0eifib+64)+6+i&g-5g5#7#1tfxk'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'main',
    # 'material',
    # 'material.admin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'account',
    'panel',
    'news',
    'shop',
    'cart',
    'order',
    # 'products',
    'tecdoc',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'avtoresurs_new.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'main', 'templates'), ],
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

WSGI_APPLICATION = 'avtoresurs_new.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = DB

DATABASE_ROUTERS = ['avtoresurs_new.routers.TecdocRouter']

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Kaliningrad'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, 'main', 'static'),
# )

# "Поисковики" статики. Первый ищет статику в STATICFILES_DIRS,
# второй в папках приложений.
# STATICFILES_FINDERS = (
#
#     'django.contrib.staticfiles.finders.FileSystemFinder',
#
#     'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#
# )


ACCOUNT_ACTIVATION_DAYS = 7
# Host for sending e-mail.
EMAIL_HOST = 'localhost'

# Port for sending e-mail.
EMAIL_PORT = 1025
DEFAULT_FROM_EMAIL = 'noreplyweb@gov39.ru'


# EMAIL_USE_TLS = True
EMAIL_HOST = '127.0.0.1'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'kashim'
EMAIL_HOST_PASSWORD = 'Kashim31337'
DEFAULT_FROM_EMAIL = 'no-reply@avtoresurs.net'