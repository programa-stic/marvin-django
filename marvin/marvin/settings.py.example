"""
Django settings for marvin project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SITE_ID = 1

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'EDITME'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True # You will have to serve static files from outside Django if DEBUG=False

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]
TEMPLATE_DEBUG = True
TEMPLATE_CONTEXT_PROCESSORS = ("django.contrib.auth.context_processors.auth",
"django.core.context_processors.debug",
"django.core.context_processors.i18n",
"django.core.context_processors.media",
"django.core.context_processors.static",
"django.core.context_processors.tz",
"django.contrib.messages.context_processors.messages")

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bungiesearch',
#    'djgpa',
    'preferences',
    'django.contrib.sites',
    'frontpage',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'marvin.urls'

WSGI_APPLICATION = 'marvin.wsgi.application'

BUNGIESEARCH = {
               'URLS': ['172.30.0.5'], # No leading http:// or the elasticsearch client will complain.
               'INDICES': {'apps2': 'frontpage.myindices'}, # Must be a module path.
               #'ALIASES': {'bsearch': 'marvin.search_aliases'},
               'SIGNALS': {'BUFFER_SIZE': 1},
               'TIMEOUT': 5
               }

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
         'ENGINE': 'django.db.backends.mysql',
         'NAME': 'marvin',
         'USER': 'marvin',
         'PASSWORD': 'pelucidar',
         'HOST': '172.30.0.3',
	 'PORT': '3306'
    }
}

DEFAULT_INDEX_TABLESPACE=''

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
LOGIN_URL = '/frontpage/login'

