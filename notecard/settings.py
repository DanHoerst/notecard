# Django settings for notecard project.
import os

DEBUG = bool(os.environ.get('DJANGO_DEBUG', ''))
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('dan hoerst', 'dhoerst1@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('db_ENGINE'), # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.environ.get('db_NAME'), # Or path to database file if using sqlite3.
        'USER': os.environ.get('db_USER'), # Not used with sqlite3.
        'PASSWORD': '', # Not used with sqlite3.
        'HOST': '', # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '', # Set to empty string for default. Not used with sqlite3.
    }
}

TIME_ZONE = 'America/Chicago'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

MEDIA_ROOT = ''

MEDIA_URL = ''

STATIC_ROOT = ''

STATIC_URL = os.environ.get('static_URL')

ADMIN_MEDIA_PREFIX = os.environ.get('admin_MEDIA')

STATICFILES_DIRS = (
    'C:/Users/Dan Hoerst/Documents/notecard/notecard/templates/static/',
)

# Storage for S3
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

AWS_ACCESS_KEY_ID = os.environ.get('aws_KEYID')
AWS_SECRET_ACCESS_KEY = os.environ.get('aws_ACCESSKEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('s3_BUCKET')

STATIC_URL = os.environ.get('s3_URL')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

secret_KEY=os.environ.get('secret_KEY')

TEMPLATE_LOADERS = (
# 'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'notecard.urls'

TEMPLATE_DIRS = (
    os.environ.get('template_DIR')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'notecards',
    'registration',
    'markdown',
    'south',
    'search',
    'storages',
    'django.contrib.admin',
    'django.contrib.admindocs',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

## Memcached
CACHES = {
    'default': {
        'BACKEND': os.environ.get('cache_BACKEND')
   }
}

# Heroku deprecated settings.py injection
import dj_database_url
DATABASES = {'default': dj_database_url.config(default=os.environ.get('dj_DBURL'))}