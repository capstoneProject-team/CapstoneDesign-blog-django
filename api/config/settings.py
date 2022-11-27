
from pathlib import Path
import os
import datetime
import environ

# import my_settings


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env(DEBUG=(bool, True))
environ.Env.read_env(
    env_file=os.path.join(BASE_DIR, '.env')
)
# SECURITY WARNING: don't run with debug turned on in production!
# SECURITY WARNING: keep the secret key used in production secret!
# .env에 있음
SECRET_KEY = env('JWT_SECRET_KEY')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition
# 'rest_framework_simplejwt', 추가
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework_simplejwt',
    'debug_toolbar',
    'rest_framework',
    'post',
    'account',
    # 'post.apps.PostConfig',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': (
    'rest_framework.pagination.PageNumberPagination',
    'rest_framework.permissions.IsAuthenticated',
    ),
    'PAGE_SIZE': 7,
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),

}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(minutes=300),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': datetime.timedelta(minutes=300),
    'SLIDING_TOKEN_REFRESH_LIFETIME': datetime.timedelta(days=1),
}

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.backends.mysql',
        'NAME': 'hed',
        'USER': 'root',
        'PASSWORD': '1234',
        'HOST': 'localhost',
        'PORT': '3306'
    }
}

# DATABASES = my_settings.DATABASES
# SECRET_KEY = my_settings.SECRET_KEY
# print(SECRET_KEY)

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = "account.User"
# username 말고 email을 디폴트로 설정할 수 있는 방법?

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
INTERNAL_IPS = ['127.0.0.1']
# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

CORS_ORIGIN_WHITELIST = ['http://127.0.0.1:3000', 'http://3.36.254.187'
    , 'http://localhost:3000']
CORS_ALLOW_CREDENTIALS = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

