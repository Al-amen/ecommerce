
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-pkx@xv^+aw9)-hmdt!ewy7qv&9s^0m*16r(psznlr@exc2d=dt'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

AUTH_USER_MODEL ='account.User'
# AUTHENTICATION_BACKENDS = ['account.backend.UsernameOrEmailBackend']
AUTHENTICATION_BACKENDS = [
    'account.backend.UsernameOrEmailBackend',  # Correct path to the custom backend
    'django.contrib.auth.backends.ModelBackend',  # Default Django authentication backend
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
     'crispy_forms',
     'crispy_bootstrap5',
     'account',
     'store',
     'order',
     'coupon',
     'payment',
     'django_cleanup.apps.CleanupConfig',
     'notification',
     'dashboard',
     'review',
     'invoice',
    
]

CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

ROOT_URLCONF = 'ecommerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR,'templates')
        ],
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


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',

        'ENGINE': 'django.db.backends.postgresql',
        'NAME': "eshop",
        'USER': "postgres",
        'PASSWORD': "1234",
        'HOST': "localhost",
        'PORT': "5432",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]





# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

PAYPAL_CLIENT_ID = "AdM4NaJNZRLWC2JcPhoVa2GAd2sKYhfB4HruwejmLW3TmtkAZ-1JV5yLV7Pm_4emBha3y5_4PoFalIaz"
PAYPAL_CLIENT_SECRET = "EEASkz36yUXjS33UOiEodYtY58-I4m3pVDRo7T_jPFDcQqbs-JKHZiHe8oSdPOP6ZPOoUhlPyj4NA_7M"

SSL_STORE_ID = "pstu67116a930985c"
SSL_PASS = "pstu67116a930985c@ssl"



#email access
LOGIN_REDIRECT_URL = '/account/'

SESSION_ENGINE = 'django.contrib.sessions.backends.db'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = "alamen1170@gmail.com"
EMAIL_HOST_PASSWORD = "nykh nlqa axvq nyzh"