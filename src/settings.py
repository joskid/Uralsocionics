# -*- coding: utf-8 -*-
# Django settings for perspectiva project.
import os, sys
import platform

DEBUG = False
TEMPLATE_DEBUG = False
APPEND_SLASH = False

ADMINS = (
    ('Glader', 'glader@glader.ru'),
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
SECRET_KEY = '(q3s-v$9jv#x&ow)w_+*vxyucyk#z&jb!j=*bgctzhivv#efmj'

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
    'tagging',
    'django_russian',
    'south',
    'core',
    'subscribe',
)

SMILES_URL = MEDIA_URL + "design/smiles/"
SMILES = [ [':\)+', SMILES_URL + 'smile3.gif' ],
           [':-\)+', SMILES_URL + 'smile3.gif' ],
           [';\)+', SMILES_URL + 'wink.gif' ],
           [';\-\)+', SMILES_URL + 'wink.gif' ],
           [':\(+', SMILES_URL + 'sad.gif' ],
           [':\-\(+', SMILES_URL + 'sad.gif' ],
           [':\-\[', SMILES_URL + 'blush2.gif' ],
           [':p', SMILES_URL + 'blum2.gif' ],
           [':-p', SMILES_URL + 'blum2.gif' ],
        ]

DEFAULT_FROM_EMAIL = 'robot@uralsocionics.ru'


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
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['special']
        }
    },
    'loggers': {
        'django': {
            'handlers':['null'],
            'propagate': True,
            'level':'INFO',
            },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
            },
        'myproject.custom': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
            'filters': ['special']
        }
    }
}


try:
    from local_settings import *
except ImportError:
    pass

EXCEPTION_LOG_FILE = os.path.join(LOG_PATH, 'exception.log')
TRACEBACK_LOG_FILE = os.path.join(LOG_PATH, 'traceback.log')

LOGGING_FORMAT = '%(asctime)s %(name)-15s %(levelname)s %(message)s'
LOGGING_MAX_FILE_SIZE = 1 * 1024 * 1024 #: Максимальный размер файла с логами в байтах.
LOGGING_MAX_FILES_COUNT = 10 #: Количество бекапов файлов с логами.

WARNING_LOG_PATH = os.path.join(LOG_PATH, 'warning.log')
ADMIN_LOG_PATH = os.path.join(LOG_PATH, 'admin.log')

LOG_SENDMAIL = os.path.join(LOG_PATH, 'email.log')

