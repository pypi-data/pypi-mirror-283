import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', default='unsafe_secret_key')

DEBUG = os.getenv('DEBUG', default=False)

ALLOWED_HOSTS = [
    '*',
]


# Application definition

INSTALLED_APPS = [
    'news.apps.NewsConfig',
    'news_parsing.apps.NewsParsingConfig',
    # 'baton',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sorl.thumbnail',
    'tinymce',
    'rangefilter',
    'django_admin_listfilter_dropdown',
    # 'baton.autodiscover'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'csp.middleware.CSPMiddleware',
]

CSP_STYLE_SRC = ["'self'"]
CSP_SCRIPT_SRC = ["'self'"]
CSP_SCRIPT_SRC_ATTR = ["'self'"]
CSP_SCRIPT_SRC_ELEM = ["'self'"]

ROOT_URLCONF = 'news_bot.urls'

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

WSGI_APPLICATION = 'news_bot.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.getenv('DB_NAME', 'news'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'db'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': ('django.contrib.auth.password_validation.MinimumLengthValidator'),
    },
    {
        'NAME': ('django.contrib.auth.password_validation.CommonPasswordValidator'),
    },
    {
        'NAME': ('django.contrib.auth.password_validation.NumericPasswordValidator'),
    },
]


# Internationalization

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = os.getenv('TZ', default='Europe/Moscow')

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMPTY_ADMIN_VALUE = '-пусто-'

NEWS_DAYS = 7

DELETE_NEWS_AFTER_DAYS = 60

# Django-baton
# BATON = {
#     'SITE_HEADER': 'Панель управления парсингом новостей',
#     'SITE_TITLE': 'Панель управления парсингом новостей',
#     'INDEX_TITLE': 'Администрирование парсинга',
# }
