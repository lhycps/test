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
import re

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
    # 'system.middleware.sessionlogout.MD1'
]

ROOT_URLCONF = 'crm.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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
        'HOST': 'localhost',
        'PORT': '3306',
        'USER': 'root',
        'PASSWORD': 'admin123'
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

# 设置邮件域名
EMAIL_HOST = 'smtp.163.com'
# 设置端口号，为数字
EMAIL_PORT = 25
# 设置发件人邮箱
EMAIL_HOST_USER = 'lihaiyan1029@163.com'
# 设置发件人 授权码
EMAIL_HOST_PASSWORD = 'ZSIJMTKPRHMKAYSV'
# 设置是否启用安全链接
EMAIL_USER_TLS = True

# session 设置
SESSION_COOKIE_AGE = 60 * 32  # 设置过期时间10分钟，默认为两周
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # 设置关闭浏览器时失效

# 配置登录的url
LOGIN_URL = '/user/signin/'

# 配置用户图像存放路径
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 权限相关的配置
PERMISSION_SESSION_KEY = 'permission_list'
# 菜单相关的配置
MENU_SESSION_KEY = 'menu_list'

# 合同模板路径
WORD_TEMPLATES_PATH = os.path.join(BASE_DIR, 'pro_tempaltes/contract/LISS-4109-02 网络安全等级保护测评服务合同模板.docx')
# 输出合同文件保存在服务器中的位置
OUTPUT_FILES_PATH = os.path.join(BASE_DIR, 'pro_output/contract')

# CNAS_编号申请模板文件路径
CNAS_FILES_PATH_PRONUM = os.path.join(BASE_DIR, 'pro_tempaltes/djcp/CNAS/001编号申请')
# CNAS_编号申请模板文件路径
CNAS_FILES_PATH_SIGNATURE = os.path.join(BASE_DIR, 'pro_tempaltes/djcp/CNAS/002签字盖章')
# CNAS_编号申请模板文件路径
CNAS_FILES_END = os.path.join(BASE_DIR, 'pro_tempaltes/djcp/CNAS/003收尾文件')

# 下载测评小助手
DOWNLOAD_Helper = os.path.join(BASE_DIR, 'pro_tempaltes/djcp/Helper/25测评小助手.zip')

# 输出CNAS文件保存在服务器中的位置
OUTPUT_CNAS_FILES_PATH = os.path.join(BASE_DIR, 'pro_output/djcp')

# 信息调查表模板路径
INFO_FILES_PATH = os.path.join(BASE_DIR, 'pro_tempaltes/info/LISS-4111-02 信息系统基本信息调查表V2.1.docx')
# 处理完的信息调查表保存路径位置
INFO_OUTPUT_PATH = os.path.join(BASE_DIR, 'pro_output/info')

# 测评方案相关
ASSET_NUM = os.path.join(BASE_DIR, 'pro_tempaltes/case/设备资产编号（勿动）')  # 设备资产的文件路径
ASSET_NUM = re.sub('\\\\', '/', ASSET_NUM)  # 路径符号转换
EVA_METHOD = os.path.join(BASE_DIR, 'pro_tempaltes/case/测评方法+测评依据/测评方法.docx')  # 测评方法
EVA_METHOD = re.sub('\\\\', '/', EVA_METHOD)  # 路径符号转换
STANDARD_PATH = os.path.join(BASE_DIR, 'pro_tempaltes/case/测评方法+测评依据/测评依据.docx')  # 测评依据存放位置
STANDARD_PATH = re.sub('\\\\', '/', STANDARD_PATH)  # 路径符号转换
CASE_SIGN = os.path.join(BASE_DIR, 'pro_tempaltes/case/测评方法+测评依据/方案签字页.docx')  # 方案签字
CASE_SIGN = re.sub('\\\\', '/', CASE_SIGN)  # 路径符号转换
CASE_OUTPUT_PATH = os.path.join(BASE_DIR, 'pro_output/case')  # 处理后的测评方案保存的位置
CASE_OUTPUT_PATH = re.sub('\\\\', '/', CASE_OUTPUT_PATH)  # 路径符号转换

# 存放合同金额的密钥
ENCRYPT_KEY = b'BYhmjGvhX-edHy9MlrVvu6Q9mUmSOVziCRi6Vbwmdi0='

'''白名单'''
VALID_URL_LIST = [
    '^/user/signin/$', '^/user/signup/$', '^/admin/.*', '^/user/active_account/$',
    '^/user/checkuname/$',
    MEDIA_URL
]

''''相关配置：需要登录但无需权限的URL'''

NO_PERMISSION_LIST = [
    '^/user/index/$',
    '^/user/chart/$',    '^/user/cake/$',
    '^/user/stream_video/$',
    '^/user/logout/$',
    '^/user/setting/$',
    '^/user/resetpassword/$',
    '^/user/conform_update/$',
]

#######日志相关内容###################
# LOGGING_DIR 日志文件存放目录
LOGGING_DIR = "logs"  # 日志存放路径
if not os.path.exists(LOGGING_DIR):
    os.mkdir(LOGGING_DIR)
import logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {  # 格式化器
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
            'filename': '%s/django.log' % LOGGING_DIR,  # 具体日志文件的名字
            'formatter': 'standard'
        },  # 用于文件输出
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {  # 日志分配到哪个handlers中
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
# 数字证书密码：123456
##########################################jar文件包的相关路径###############
jar_path = os.path.join(BASE_DIR, 'updateTOC/wordUtils.jar')
