"""
Django settings for blog project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*u(elr9%xm1_4!m$at8#a6f3un2mwlkc5(sdbju8gmr(ln*r%v'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',  # allauth 启动必须项
    'django.contrib.staticfiles',
    'password_reset',
    'article',
    # 标签
    'taggit',
    # user 扩展对象
    'userprofile',
    # 评论
    'comment',
    'mptt',
    # 自定义过滤器
    'article.templatetags',
    # 富文本编辑器
    'ckeditor',
    'ckeditor_uploader',
    'sendmail',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # 可添加需要的第三方登录
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.weixin',
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

ROOT_URLCONF = 'blog.urls'

AUTHENTICATION_BACKENDS = (
    # Django 后台可独立于 allauth 登录
    'django.contrib.auth.backends.ModelBackend',
    # 配置 allauth 独有的认证方法，如 email 登录
    'allauth.account.auth_backends.AuthenticationBackend',
)


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',  # allauth 启动必须项
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'blog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]



# 媒体文件保存地址
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
CKEDITOR_UPLOAD_PATH = 'upload/'
CKEDITOR_IMAGE_BACKEND = 'pillow'


# 富文本编辑器 Config

CKEDITOR_CONFIGS = {
    # django-ckeditor 默认使用 default 配置
    'default':{
        'width':'auto',
        'height':'200px',
        'tabSpace':4,
        'toolbar':'Custom',
        'toolbar_Custom':[
            ['Smiley', 'CodeSnippet'],
            ['Bold', 'Italic', 'Underline', 'RemoveFormat', 'Blockquote'],
            ['TextColor', 'BGColor'],
            ['Format', 'Font', 'FontSize'],
            ['Link', 'Unlink'],
            ['NumberedList', 'BulletedList'],
            ['Maximize']
        ],
        'extraPlugins': ','.join(['codesnippet', 'prism', 'widget', 'lineutils', 'uploadimage',]),
    }
}

# 日志文件的配置

'''
    django：将 django 产生的所有消息转交给 console 处理器
    django.request：将网络请求相关消息转交给 file、mail_admins 这两个处理器。
    注意这里的 'propagate': False 使得此记录器处理过的消息就不再让 django 记录器再次处理了
    自定义 log
    from my_blog.settings import LOGGING
    import logging

    logging.config.dictConfig(LOGGING)
    logger = logging.getLogger('django.request')

    def whatever(request):
        # do something
        logger.warning('Something went wrong!')
        # do something else
'''

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            # 详细的格式化器，依次输出：消息级别、发生时间、抛出模块、进程ID、线程ID、提示信息
            'format': '{asctime} {levelname} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        # 简要的格式化器，输出时间，消息级别和提示信息
        'simple': {
            'format': '{asctime} {levelname} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        # INFO 以上级别消息，输出简要信息到命令行中；此处理器仅在调试模式生效
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],  # 使用此过滤器的消息仅在调试时才会生效
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        # ERROR 以上级别消息，输出详细信息到 Email 中
        # 'mail_admins': {
        #     'level': 'ERROR',
        #     'class': 'django.utils.log.AdminEmailHandler',
        #     'formatter': 'verbose',
        # },
        # WARNING 以上级别消息，输出详细信息到文件中
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',  # Python 内置的随时间分割日志文件的模块
            'when': 'midnight',  # 分割时间为凌晨
            'backupCount': 30,  # 日志文件保存日期为30天
            'filename': os.path.join(BASE_DIR, 'logs/debug.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'propagate': True,
        },
        'django.request': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}


# 第三方登录 allauth 配置

# 设置站点
SITE_ID = 1

# 强制注册邮箱验证(注册成功后，会发送一封验证邮件，用户必须验证邮箱后，才能登陆)
ACCOUNT_EMAIL_VERIFICATION = 'none'
# 登录方式(选择用户名或者邮箱都能登录)
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
# 设置用户注册的时候必须填写邮箱地址
ACCOUNT_EMAIL_REQUIRED = True
# 用户登出(需要确认)
ACCOUNT_LOGOUT_ON_GET = False

# 登录成功后重定向地址
LOGIN_REDIRECT_URL = '/'



# 邮箱配置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# SMTP服务器
EMAIL_HOST = 'localhost'
# 邮箱名！
EMAIL_HOST_USER = 'Jing.Wang@smflc.co.jp'
# 邮箱密码
EMAIL_HOST_PASSWORD = '693477aaQ`'
# 发送邮件的端口
EMAIL_PORT = 587
# 是否使用 TLS
EMAIL_USE_TLS = True
# 默认的发件人
DEFAULT_FROM_EMAIL = 'Jing.Wang@smflc.co.jp'