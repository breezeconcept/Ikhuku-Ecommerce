"""
Django settings for ecommerce project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
from datetime import timedelta

import os
from dotenv import load_dotenv
import dj_database_url

# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = bool(int(os.environ.get('DEBUG', default=0)))
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    # 'rest_framework.authtoken',
    'drf_yasg',
    'django_filters',
    'corsheaders',
    # 'axes',
    # 'csp',


    'Accounts',
    'Products',
    'Carts',
    'History',
    'Whishlist',
    'Payment',
]
    # 'django.middleware.security.SecurityMiddleware',
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # 'djangosecure.middleware.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # 'csp.middleware.CSPMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'axes.middleware.AxesMiddleware',
]

ROOT_URLCONF = 'ecommerce.urls'

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

WSGI_APPLICATION = 'ecommerce.wsgi.application'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'rest_framework.authentication.TokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # Other authentication classes can be added here if needed
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 15,  # Set the number of items per page here
    # 'DEFAULT_RENDERER_CLASSES': [
    #     # 'ecommerce/utils/CustomRenderer',
    #     'rest_framework.renderers.JSONRenderer',
    # ],

}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=int(os.environ.get('ACCESS_TOKEN_LIFETIME'))),  # Customize token expiration
    'REFRESH_TOKEN_LIFETIME': timedelta(days=int(os.environ.get('REFRESH_TOKEN_LIFETIME'))),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}


# Example logging configuration
# LOGGING = {
#     'version': 1,
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#     },
# }



# SIMPLE_JWT = {
#     'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),  # Set the token expiration time
#     # ... other JWT settings
# }

# SIMPLE_JWT = {
#     'ACCESS_TOKEN_LIFETIME': timedelta(days=15),
#     'REFRESH_TOKEN_LIFETIME': timedelta(days=15),
# }


# AXES_ENABLED = False

# AUTHENTICATION_BACKENDS = [
#     'axes.backends.AxesStandaloneBackend',
#     # Other authentication backends
# ]

# if os.environ.get('DJANGO_ENV') is not None:
#     SECURE_SSL_REDIRECT = False
#     SESSION_COOKIE_SECURE = False
#     CSRF_COOKIE_SECURE = False
# else:
#     SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
#     SECURE_SSL_REDIRECT = True
#     SESSION_COOKIE_SECURE = True
#     CSRF_COOKIE_SECURE = True

AUTH_USER_MODEL = 'Accounts.CustomUser'


# Authentication backends (if needed)
# AUTHENTICATION_BACKENDS = [
#     'django.contrib.auth.backends.ModelBackend',
#     # Add your custom authentication backends here if any
# ]

# Login and Logout URLs
# LOGIN_URL = '/login/'
# LOGOUT_URL = '/logout/'

# Password reset timeout in days
# PASSWORD_RESET_TIMEOUT_DAYS = 1  # Modify according to your requirements

# EMAIL_FIELD = 'email'
# USERNAME_FIELD = 'email'




# # set this to False if you want to turn off pyodbc's connection pooling
# DATABASE_CONNECTION_POOLING = False

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
	"default": dj_database_url.parse(os.environ.get("DATABASE_URL"))
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        'OPTIONS': {
            'user_attributes': ['username', 'email'],
        },
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
]

# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# AWS_LOCATION = 'static'
# After that, open up your Command Line Interface (CLI) and run this command:
# python manage.py collectstatic --noinput


STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # Define the directory to store uploaded media files
# MEDIA_URL = '/media/'  # Define the URL prefix for media files
# MEDIA_URL = 'https://breezeconceptbucket.s3.amazonaws.com/'
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
MEDIA_URL = 'https://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
 
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'  # Example for Amazon S3 storage

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_SIGNATURE_NAME = os.environ.get('AWS_S3_SIGNATURE_NAME')
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME')
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_S3_VERITY = True
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'


# STORAGES = {
#     "default": {
#         "BACKEND": "django.core.files.storage.FileSystemStorage",
#     },
#     "staticfiles": {
#         "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
#     },
# }

# STORAGES = {
#     # "default": {
#     #     "BACKEND": "django.core.files.storage.FileSystemStorage",
#     # },
#     # ...
#     "staticfiles": {
#         "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
#     },
# }


# Example configuration for using Amazon S3
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# AWS_ACCESS_KEY_ID = 'your_access_key_id'
# AWS_SECRET_ACCESS_KEY = 'your_secret_access_key'
# AWS_STORAGE_BUCKET_NAME = 'your_bucket_name'
# AWS_S3_REGION_NAME = 'your_region_name'
# AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOW_ALL_ORIGINS = True  # Allow all origins for testing, but restrict this in production

# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:3000",  # Replace with your frontend URL
#     "https://ikhuku.vercel.app",  # Add additional allowed origins if needed
# ]

BASE_URL = os.environ.get('BASE_URL')


# Optional: Additional CORS settings
# CORS_ALLOW_HEADERS
# CORS_ALLOW_METHODS
# CORS_ALLOW_CREDENTIALS
# CORS_EXPOSE_HEADERS
# CORS_PREFLIGHT_MAX_AGE
# CORS_ALLOW_ALL_ORIGINS
# CORS_ALLOW_ALL_HEADERS = True
# CORS_ALLOW_ALL_METHODS = True




# Email configuration for sending verification emails
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND')
EMAIL_HOST = os.environ.get('EMAIL_HOST')  
EMAIL_PORT = os.environ.get('EMAIL_PORT')   
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL')
# EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS')

# Additional email settings if required
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')  # Replace with your default sender email


FLW_SEC_KEY = os.environ.get('FLW_SEC_KEY')


# Use secure session cookies (HTTPS-only)
# SESSION_COOKIE_SECURE = False
# CSRF_COOKIE_SECURE = False
# Set session expiry time
# SESSION_COOKIE_AGE = 3600  # Set the session timeout in seconds


# Set login failure limits and lockout duration
# AXES_FAILURE_LIMIT = 3
# AXES_LOCK_OUT_AT_FAILURE = True
# AXES_COOLOFF_TIME = 60  # Lockout duration in seconds


PASSWORD_MIN_LENGTH = 8  # Minimum password length
PASSWORD_MAX_LENGTH = 50 #(Maximum 50 characters)
PASSWORD_MIN_CLASSES = 4 #(Requires passwords to contain characters from at least 3 different classes) Character classes often include lowercase letters, uppercase letters, digits, and special characters.
PASSWORD_COMMON_SEQUENCES = ['123', 'password', 'qwerty'] #(Avoids passwords containing these common sequences)
PASSWORD_RESET_TIMEOUT_DAYS = 1 #(Password reset links expire after 1 day)
# PASSWORD_CHANGE_REQUIRED_AFTER_LOGIN = 3 #(Requires password change after 3 logins)
# PASSWORD_EXPIRY = 90 #(Passwords expire every 90 days)
# PASSWORD_HISTORY = 5 #(Remembers the last 5 passwords to prevent reuse)

# Configure other password policy settings as needed






# CSP_DEFAULT_SRC = ("'self'",)
# CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")
# CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'", "'unsafe-eval'")
# Configure other directives as needed based on your application requirements.



# Force HTTPS on all connections
# SECURE_SSL_REDIRECT = True
# Enable HSTS (HTTP Strict Transport Security)
# SECURE_HSTS_SECONDS = 31536000  # 1 year
# Enable browser XSS filtering
# SECURE_BROWSER_XSS_FILTER = True
# Prevent content type sniffing
# SECURE_CONTENT_TYPE_NOSNIFF = True
# Configure other security-related settings as required





PAYSTACK_SECRET_KEY = os.environ.get('PAYSTACK_SECRET_KEY')
PAYSTACK_PUBLIC_KEY = os.environ.get('PAYSTACK_PUBLIC_KEY')