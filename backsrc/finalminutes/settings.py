import datetime

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'c06bxt!5&^yk8h&3pt!qeki69+_42v0j^fnydk1b*4wd6l@p7l'

# print env variable debug
print(os.getenv('DEBUG'),"variabe debug")

# str to bool
DEBUG = os.getenv('DEBUG') == 'True'

#DEBUG = True
CORS_ORIGIN_ALLOW_ALL = True
ALLOWED_HOSTS = ['www.dialpro.net','dialpro.net','127.0.0.1','localhost','10.0.0.229','3.137.193.102','855rzntb47.execute-api.us-east-2.amazonaws.com','192.168.2.109','192.168.1.100','10.0.0.229','www.855rzntb47.execute-api.us-east-2.amazonaws.com','http://855rzntb47.execute-api.us-east-2.amazonaws.com','https://855rzntb47.execute-api.us-east-2.amazonaws.com']

INSTALLED_APPS = [
    "sslserver",
    'kamailio',
    'rest_framework',
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'corsheaders',
    'storages',
    'django_filters',
]

AUTH_USER_MODEL = 'kamailio.Customer'

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'finalminutes.urls'

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

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES':(
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS':('django_filters.rest_framework.DjangoFilterBackend',)
}

WSGI_APPLICATION = 'finalminutes.wsgi.application'


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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Santo_Domingo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

USE_S3 = os.getenv('USE_S3') == 'TRUE'


if not DEBUG:
   
    # aws settings
    AWS_ACCESS_KEY_ID = 'AKIA4WVCJI7F5ZJXWKHO'
    AWS_SECRET_ACCESS_KEY = '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'
    AWS_STORAGE_BUCKET_NAME = 'kamailiostatic2'
    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com'%(AWS_STORAGE_BUCKET_NAME)
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    # s3 static settings
    AWS_LOCATION = 'static'
    STATIC_URL = 'https://%s/%s/'%(AWS_S3_CUSTOM_DOMAIN,AWS_LOCATION)
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'kamailio',
        'USER': 'prietokamailio',
        'PASSWORD': 'T9Ybgq&NiwiV',
        'HOST': '170.75.165.97',
        'PORT': '3306',
    }
}

else:
    print('Debugging')
    STATIC_URL = '/static/'
    STATIC_ROOT = BASE_DIR + '\static'
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
        }
    }
#     DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'kamailio',
#         'USER': 'prietokamailio',
#         'PASSWORD': 'T9Ybgq&NiwiV',
#         'HOST': '170.75.165.97',
#         'PORT': '3306',
#     }
# }


# Print environment variables
# print('Environment variables:')
# for env_var in os.environ:
#     print(env_var, os.environ[env_var])

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.carly.do'
EMAIL_HOST_USER = 'admin@carly.do'
EMAIL_HOST_PASSWORD = 'xlzl!Mo5'
EMAIL_PORT = 587

CORS_ORIGIN_WHITE_LIST = 'www.dialpro.net','dialpro.net','127.0.0.1','localhost','10.0.0.229','3.137.193.102','10.0.0.229','www.dialpro.net','dialpro.net','127.0.0.1','localhost','carenproject.herokuapp.com','3.15.162.59','http://855rzntb47.execute-api.us-east-2.amazonaws.com','www.855rzntb47.execute-api.us-east-2.amazonaws.com','855rzntb47.execute-api.us-east-2.amazonaws.com','www.855rzntb47.execute-api.us-east-2.amazonaws.com',
CORS_ALLOW_CREDENTIALS = True
JWT_AUTH = {
    'JWT_RESPONSE_PAYLOAD_HANDLER' :   'kamailio.utils.custom_jwt_response_handler',
    'JWT_EXPIRATION_DELTA': datetime.timedelta(minutes=999999999)
}
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'


