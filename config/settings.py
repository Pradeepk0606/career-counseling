"""
Django settings for career compass project.
"""

from pathlib import Path

from decouple import Csv, config
from django.contrib.messages import constants as messages

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config(
    "SECRET_KEY",
    default="django-insecure-career-compass-key-change-in-production-1234567890",
)

DEBUG = config("DEBUG", default=True, cast=bool)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="*,127.0.0.1,localhost", cast=Csv())

CSRF_TRUSTED_ORIGINS = config(
    "CSRF_TRUSTED_ORIGINS",
    default="http://127.0.0.1:8000,http://localhost:8000,https://*.vercel.app",
    cast=Csv(),
)

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "crispy_bootstrap5",
    "crispy_forms",
    "career.apps.CareerConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

import os
import shutil

IS_VERCEL = "VERCEL" in os.environ or "AWS_LAMBDA_FUNCTION_NAME" in os.environ

if IS_VERCEL:
    SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
    db_path = Path("/tmp") / "db.sqlite3"
    initial_db = BASE_DIR / "db.sqlite3"
    if initial_db.exists() and not db_path.exists():
        try:
            shutil.copyfile(initial_db, db_path)
        except Exception:
            pass
    target_db_name = str(db_path)
else:
    target_db_name = config("SQL_DATABASE", default=str(BASE_DIR / "db.sqlite3"))

DATABASES = {
    "default": {
        "ENGINE": config("SQL_ENGINE", default="django.db.backends.sqlite3"),
        "NAME": target_db_name,
        "USER": config("SQL_USER", default=""),
        "PASSWORD": config("SQL_PASSWORD", default=""),
        "HOST": config("SQL_HOST", default=""),
        "PORT": config("SQL_PORT", default=""),
    },
}



AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [BASE_DIR / "static"]

STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CRISPY_TEMPLATES_PACK = "bootstrap5"

MESSAGE_TAGS = {
    messages.ERROR: "danger",
}

LOGOUT_REDIRECT_URL = "home"

DATA_UPLOAD_MAX_NUMBER_FIELDS = None

DEFAULT_FROM_EMAIL = config("DEFAULT_EMAIL", default="admin@careercompass.com")
EMAIL_BACKEND = config("EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend")
EMAIL_HOST = config("EMAIL_HOST", default="")
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
EMAIL_USE_TLS = True

if DEBUG:
    CORS_REPLACE_HTTPS_REFERER = False
    HOST_SCHEME = "http://"
    SECURE_FRAME_DENY = False
    SECURE_PROXY_SSL_HEADER = None
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_HSTS_SECONDS = None
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
else:
    CORS_REPLACE_HTTPS_REFERER = True
    HOST_SCHEME = "https://"
    SECURE_FRAME_DENY = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_HSTS_SECONDS = 2592000
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_REDIRECT_EXEMPT = []

