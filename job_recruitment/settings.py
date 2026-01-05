"""
Django settings for job_recruitment project.

Compatible with:
- Django REST Framework
- PostgreSQL
- JWT (SimpleJWT)
- Google OAuth
- React frontend (Vite)
"""

from pathlib import Path
import os
from datetime import timedelta
from dotenv import load_dotenv
import dj_database_url

# --------------------------------------------------
# BASE DIR & ENV
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


# --------------------------------------------------
# SECURITY
# --------------------------------------------------
SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "django-insecure-development-key-change-this"
)

DEBUG = True

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
]


# --------------------------------------------------
# APPLICATIONS
# --------------------------------------------------
INSTALLED_APPS = [
    # Django default
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'rest_framework',
    'corsheaders',
    'drf_yasg',

    # Local apps
    'accounts',
    'jobs',
    'applications',
]


# --------------------------------------------------
# MIDDLEWARE (ORDER MATTERS)
# --------------------------------------------------
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # MUST be first
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# --------------------------------------------------
# CORS & CSRF (REACT)
# --------------------------------------------------
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
]

CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
]


# --------------------------------------------------
# URL CONFIG
# --------------------------------------------------
ROOT_URLCONF = 'job_recruitment.urls'


# --------------------------------------------------
# TEMPLATES
# --------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
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


# --------------------------------------------------
# WSGI
# --------------------------------------------------
WSGI_APPLICATION = 'job_recruitment.wsgi.application'


# --------------------------------------------------
# DATABASE (POSTGRESQL)
# --------------------------------------------------
DATABASES = {
    'default': dj_database_url.parse(
        os.getenv("DATABASE_URL")
    )
}


# --------------------------------------------------
# PASSWORD VALIDATION
# --------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# --------------------------------------------------
# INTERNATIONALIZATION
# --------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# --------------------------------------------------
# STATIC FILES
# --------------------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"


# --------------------------------------------------
# DEFAULT PRIMARY KEY
# --------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# --------------------------------------------------
# DJANGO REST FRAMEWORK
# --------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
}


# --------------------------------------------------
# SIMPLE JWT
# --------------------------------------------------
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'AUTH_HEADER_TYPES': ('Bearer',),
}


# --------------------------------------------------
# GOOGLE OAUTH
# --------------------------------------------------
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

if not GOOGLE_CLIENT_ID:
    raise ValueError("❌ GOOGLE_CLIENT_ID is not set in .env")


# --------------------------------------------------
# LOGGING (OPTIONAL – GOOD FOR DEBUG)
# --------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}
