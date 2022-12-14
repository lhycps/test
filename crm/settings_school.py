"""
Django settings for crm project.

Generated by 'django-admin startproject' using Django 2.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+b=4ms7_dn4#1q0uspeiha(il^ud%)-t^mz#rivtm1)@+v87tu'

# SECURITY WARNING: don't run with debug turned on in production!
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
    'system.apps.SystemConfig',
    'djcp',
    'sales',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'system.middleware.rbac.RbacMiddleware',
]

ROOT_URLCONF = 'crm.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'crm.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'crm',
        'HOST': '10.119.1.109',
        'PORT': '3306',
        'USER': 'root',
        'PASSWORD': 'Liss@2022'
    }
}

AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.AllowAllUsersModelBackend']

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'Zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

AUTH_USER_MODEL = 'system.UserInfo'

# ??????????????????
EMAIL_HOST = 'smtp.163.com'
# ???????????????????????????
EMAIL_PORT = 25
# ?????????????????????
EMAIL_HOST_USER = 'lihaiyan1029@163.com'
# ??????????????? ?????????
EMAIL_HOST_PASSWORD = 'ZSIJMTKPRHMKAYSV'
# ??????????????????????????????
EMAIL_USER_TLS = True

# session ??????
SESSION_COOKIE_AGE = 60 * 5  # ??????????????????10????????????????????????
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # ??????????????????????????????

# ???????????????url
LOGIN_URL = '/user/signin/'

# ??????????????????????????????
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ?????????????????????
PERMISSION_SESSION_KEY = 'permission_list'
# ?????????????????????
MENU_SESSION_KEY = 'menu_list'

# ??????????????????
WORD_TEMPLATES_PATH = os.path.join(BASE_DIR, 'pro_tempaltes/contract/LISS-4109-02 ????????????????????????????????????????????????.docx')
# ????????????????????????????????????????????????
OUTPUT_FILES_PATH = os.path.join(BASE_DIR, 'pro_output/contract')

# CNAS_??????????????????????????????
CNAS_FILES_PATH_PRONUM = os.path.join(BASE_DIR, 'pro_tempaltes/djcp/CNAS/001????????????')
# CNAS_??????????????????????????????
CNAS_FILES_PATH_SIGNATURE = os.path.join(BASE_DIR, 'pro_tempaltes/djcp/CNAS/002????????????')
# CNAS_??????????????????????????????
CNAS_FILES_END = os.path.join(BASE_DIR, 'pro_tempaltes/djcp/CNAS/003????????????')

# ?????????????????????
DOWNLOAD_Helper = os.path.join(BASE_DIR, 'pro_tempaltes/djcp/Helper/25???????????????.zip')

# ??????CNAS????????????????????????????????????
OUTPUT_CNAS_FILES_PATH = os.path.join(BASE_DIR, 'pro_output/djcp')

'''?????????'''
VALID_URL_LIST = [
    '^/user/signin/$', '^/user/signup/$', '^/admin/.*', '^/user/active_account/$',
    '^/user/checkuname/$',
    MEDIA_URL
]

''''?????????????????????????????????????????????URL'''

NO_PERMISSION_LIST = [
    '^/user/index/$',
    '^/user/chart/$',
    '^/user/cake/$',
    '^/user/stream_video/$',
    '^/user/logout/$',
    '^/user/setting/$',
    '^/user/resetpassword/$',
    '^/user/conform_update/$',
]

#######??????????????????###################
# LOGGING_DIR ????????????????????????
LOGGING_DIR = "logs"  # ??????????????????
if not os.path.exists(LOGGING_DIR):
    os.mkdir(LOGGING_DIR)
import logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {  # ????????????
        'standard': {
            'format': '[%(levelname)s][%(asctime)s][%(filename)s][%(funcName)s][%(lineno)d] > %(message)s'
        },
        'simple': {
            'format': '[%(levelname)s]> %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file_handler': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': '%s/django.log' % LOGGING_DIR,  # ???????????????????????????
            'formatter': 'standard'
        },  # ??????????????????
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {  # ?????????????????????handlers???
        'mydjango': {
            'handlers': ['console', 'file_handler'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        }
    }
}
