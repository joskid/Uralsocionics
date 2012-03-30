# -*- coding: utf-8 -*-
# Django settings for uralsocionics project.
import os

DEBUG = False
TEMPLATE_DEBUG = False
APPEND_SLASH = False

ADMINS = (
    ('Glader', 'glader.ru@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'NAME': 'uralsocionics',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'uralsocionics',
        'PASSWORD': ''
    }
}

LOGIN_REDIRECT_URL = '/'

AUTH_PROFILE_MODULE = 'core.Profile'

PROJECT_PATH = os.path.dirname(__file__)
data_images_path = './media/data/'
FORCE_SCRIPT_NAME = ""

TIME_ZONE = 'Asia/Yekaterinburg'
LANGUAGE_CODE = 'ru-ru'
SITE_ID = 1
USE_I18N = True

MEDIA_ROOT = PROJECT_PATH + '/media/'
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/admin/media/'
SECRET_KEY = '12345'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.app_directories.load_template_source',
    'django.template.loaders.filesystem.load_template_source'
)

TEMPLATE_DIRS = (
    PROJECT_PATH
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'django.core.context_processors.csrf',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
)

ROOT_URLCONF = 'urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'pytils',
    'tagging',
    'south',
    'core',
    'django_subscribe',
)

SERVER_EMAIL = DEFAULT_FROM_EMAIL = 'glader.ru@gmail.com'

LOG_PATH = '/var/log/projects/uralsocionics'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(name)-15s %(levelname)s %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_PATH, 'traceback.log'),
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'file'],
            'level': 'WARNING',
            'propagate': True,
        },
    }
}

try:
    from local_settings import *
except ImportError:
    pass
