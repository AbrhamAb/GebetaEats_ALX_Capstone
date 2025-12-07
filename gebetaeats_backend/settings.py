import os
from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'dev-secret-key-change-me')

DEBUG = True  # switch to False in production

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
        'django.contrib.admin',
            'django.contrib.auth',
                'django.contrib.contenttypes',
                    'django.contrib.sessions',
                        'django.contrib.messages',
                            'django.contrib.staticfiles',

                                'rest_framework',
                                    'rest_framework_simplejwt',

                                        # local apps
                                            'users',
                                                'vendors',
                                                    'menu',
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

ROOT_URLCONF = 'gebetaeats_backend.urls'

TEMPLATES = [
        {
                    'BACKEND': 'django.template.backends.django.DjangoTemplates',
                            'DIRS': [],  # add templates if needed
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

WSGI_APPLICATION = 'gebetaeats_backend.wsgi.application'

# Use sqlite for simplicity
DATABASES = {
        'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                            'NAME': BASE_DIR / 'db.sqlite3',
        }
}

# Custom user model
AUTH_USER_MODEL = 'users.User'

AUTH_PASSWORD_VALIDATORS = [
        {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
            {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 8}},
                {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
                    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Addis_Ababa'  # your timezone
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# DRF + JWT
REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': (
                    'rest_framework_simplejwt.authentication.JWTAuthentication',
        ),
            'DEFAULT_PERMISSION_CLASSES': (
                        'rest_framework.permissions.AllowAny',
            ),
}

SIMPLE_JWT = {
        'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
            'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
                'AUTH_HEADER_TYPES': ('Bearer',),
}
