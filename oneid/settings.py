"""
Django settings for oneid project.

Generated by 'django-admin startproject' using Django 1.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import datetime
from kombu import Exchange, Queue

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'pueg+1f_su-h_=wxz98+gr9#f5_49f-267^%j^ry^pbcd4+wio'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TESTING = False  # always False

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_celery_results',
    'django_celery_beat',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'drf_expiring_authtoken',
    'coreapi',
    'tasksapp',
    'siteadmin',
    'siteapi',
    'oneid_meta',
    'oauth2_provider',
    'infrastructure',
    'captcha',
    'djangosaml2idp',
    # 'ldap.sql_backend',
    'webhook',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oneid.authentication.CustomExpiringTokenAuthentication',
        # 'oneid.authentication.SUDOExpiringTokenAuthentication',
        'oneid.authentication.HeaderArkerBaseAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
        'oneid.permissions.IsAdminUser',
    ),
}

AUTHENTICATION_BACKENDS = (
    'rules.permissions.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',  # 保留，用于登录django admin。注意：两个体系中账号密码一样会返回django_user
    'oneid.auth_backend.OneIDBasicAuthBackend',
)

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'common.django.middleware.CrequestMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'oneid.middleware.dynamic_custom_middleware',
]

TEMPLATE_CONTEXT_PROCESSORS = [
    'django.core.context_processors.i18n',
]

SITE_ID = 1
SITE_META = 'native'

ROOT_URLCONF = 'oneid.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'infrastructure', 'templates')],
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

# log
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
    },
}

WSGI_APPLICATION = 'oneid.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db', 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    #     'OPTIONS': {
    #         'min_length': 8,
    #     },
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
    {
        'NAME': 'oneid.password_validation.ComplexityValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True  # pylint: disable=invalid-name

USE_TZ = True

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

LANGUAGES = (
    ('en', ('English')),
    ('zh-hans', ('中文简体')),
    ('zh-hant', ('中文繁體')),
)

# CORS
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = ('*',)
CORS_ALLOW_METHODS = (
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS',
)

EXECUTERS = [  # 注意顺序
    'executer.RDB.RDBExecuter',
    'executer.log.rdb.RDBLogExecuter',
    'executer.cache.default.CacheExecuter',
    # 'executer.LDAP.LDAPExecuter',
    # 'executer.Ding.DingExecuter',
]

EXECUTER_WIP = False

# LDAP

LDAP_SERVER = 'ldap://localhost'
LDAP_CLUSTER_ADDR = ''
LDAP_BASE = 'dc=example,dc=org'
LDAP_USER = 'cn=admin,{}'.format(LDAP_BASE)
LDAP_USER_BASE = 'ou=people,{}'.format(LDAP_BASE)
LDAP_DEPT_BASE = 'ou=dept,{}'.format(LDAP_BASE)
LDAP_GROUP_BASE = 'cn=intra,ou=group,{}'.format(LDAP_BASE)
LDAP_PASSWORD = 'admin'

# PASSWORD
# one of 'MD5', 'SMD5', 'SHA', 'SSHA'
PASSWORD_ENCRYPTION = 'SMD5'

# Redis
REDIS_CONFIG = {
    'HOST': 'localhost',
    'PORT': 6379,
    'DB': 0,
    'PASSWORD': None,
}

REDIS_URL = (
    'redis://{}:{}/{}'.format(
        REDIS_CONFIG['HOST'], REDIS_CONFIG['PORT'], REDIS_CONFIG['DB']
    )
    if REDIS_CONFIG['PASSWORD'] is None
    else 'redis://:{}@{}:{}/{}'.format(
        REDIS_CONFIG['PASSWORD'],
        REDIS_CONFIG['HOST'],
        REDIS_CONFIG['PORT'],
        REDIS_CONFIG['DB'],
    )
)


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "TIMEOUT": 60 * 60 * 24 * 3,
        "OPTIONS": {
            "MAX_ENTRIES": None,
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

# CELERY
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = 'django-db'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
from celery_app import app  # pylint: disable=wrong-import-position,unused-import

CELERY_TASK_QUEUES = [
    Queue('default', Exchange('default'), routing_key='default'),
    Queue('perm', Exchange('perm'), routing_key='perm'),
    Queue('dept', Exchange('dept'), routing_key='dept'),
    Queue('group', Exchange('group'), routing_key='group'),
    Queue('sql_ldap', Exchange('sql_ldap'), routing_key='sql_ldap'),
]
CELERY_TASK_DEFAULT_QUEUE = 'default'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

UPLOAD_DIR = os.path.join(BASE_DIR, 'static', 'upload')
DOWNLOAD_URL = STATIC_URL + 'download'

PRIVATE_IP = '127.0.0.1'
PUBLIC_IP = ''
BASE_URL = 'http://localhost'

FE_TOKEN_URL = '/oauth/fe/token/'
SAML_LOGIN_URL = '/saml/fe/login/'
ALIYUN_ROLE_SSO_LOGIN_URL = '/saml/aliyun/sso-role/fe/login/'

# TODO
FE_EMAIL_REGISTER_URL = '/oneid#/oneid/signup'  # 邮件注册页面
FE_EMAIL_RESET_PWD_URL = '/oneid#/oneid/password'  # 邮件重置密码页面
FE_EMAIL_ACTIVATE_USER_URL = '/oneid#/oneid/activate'  # 邮件激活账号页面
FE_EMAIL_UPDATE_EMAIL_URL = '/oneid/#/reset_email_callback'  # 邮件重置邮箱页面
LOGIN_URL = '/#/oneid/login'
CREDIBLE_ARKERS = [
    'oneid_broker',
    'arkbe_broker',
    'noah',
    'wfe',
    'msghub',
    'oauth',
]

# Minio
MINIO_ENDPOINT = 'localhost:9000'
MINIO_ACCESS_KEY = ''
MINIO_SECRET_KEY = ''
MINIO_SECURE = True
MINIO_LOCATION = 'us-east-1'

MINIO_BUCKET = 'oneid'

# SMS
SMS_LIFESPAN = datetime.timedelta(seconds=120)


ACTIVE_USER_DATA_LIFEDAY = 30
ACTIVE_USER_REDIS_KEY_PREFIX = 'active-'

# 密码复杂度规则
# 值表示至少需包含的相应元素的个数，默认全部为0
PASSWORD_COMPLEXITY = {
    "LENGTH": 0,  # 密码的长度
    "UPPER": 0,  # 包含大写字母的个数
    "LOWER": 0,  # 包含小写字母的个数
    "LETTER": 0,  # 包含大写和小写字母的个数
    "DIGIT": 0,  # 包含数字的个数
    "SPECIAL": 0,  # 包含特殊字符的个数 (不是字母数字、空格或标点字符)
    "WORD": 0,  # 包含单词的个数 (由空格或标点分隔的字母数字序列)
}

WEB_ADMIN_PASSWORD = 'admin'

if os.path.exists(os.path.join(BASE_DIR, 'settings_local.py')):
    exec(open(os.path.join(BASE_DIR, 'settings_local.py')).read())

UPLOADFILES_PATH = BASE_DIR + '/upload/'

DINGDING_APP_VERSION = 2
