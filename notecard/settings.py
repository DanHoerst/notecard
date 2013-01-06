# Django settings for notecard project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('dan hoerst', 'dhoerst1@gmail.com'),
    )

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'notecard', # Or path to database file if using sqlite3.
        'USER': 'root', # Not used with sqlite3.
        'PASSWORD': 'administrator', # Not used with sqlite3.
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

STATIC_ROOT = '/'

STATIC_URL = '/static/'

ADMIN_MEDIA_PREFIX = '/static/admin/'

STATICFILES_DIRS = (
    'C:/Users/Dan Hoerst/Documents/notecard/notecard/templates/static/',
    '/home/dan/notecard/notecard/templates/static/',
    )

# Storage for S3
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

AWS_ACCESS_KEY_ID = 'AKIAIAW7ZKU5GJYIONQA '
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'notecard-static'

STATIC_URL = 'http://notecard-static.s3.amazonaws.com/templates/static'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    )

secret_KEY='6TPymdgH5mPRh1ijNu6UXGsM1Ajju7VLC5YJgt62Yys5kh1Xcj'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #     'django.template.loaders.eggs.Loader',
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
    '/app/notecard/templates',
    '/home/dan/notecard/notecard/templates/',
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


## Memcached
CACHES = {
    'default': {
        'BACKEND': 'django_pylibmc.memcached.PyLibMCCache'
   }
}

# Heroku deprecated settings.py injection
import dj_database_url
DATABASES['default'] =  dj_database_url.config()