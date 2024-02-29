from pathlib import Path
import os
import datetime
from dotenv import load_dotenv

dotenv_path_dev = '.env.development'
load_dotenv(dotenv_path=dotenv_path_dev)

file_server_path_jupyter = os.getenv("FILE_SERVER_PATH_JUPYTER")


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-q359v@=&64%omv^gs1@)nurb=5_r*_q@jb^biz#paha=z7-g25'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost']


# Application definition
AUTH_USER_MODEL = 'user.User'


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework_simplejwt.token_blacklist',
    'rest_framework',
    'rest_framework.authtoken',
    'simple_history',
    'social_django',
    'drf_yasg',
    'rest_framework_swagger',
    'django_filters',
    'account',
    'file',
    'user',
    'tutorial',
    'history',
    'request_tutorial',
    'corsheaders',
    'contact_us',
    'social_auth',
    'role',
    'user_role',
    'share_member',
    'templates',
    "analysis",
    "scrape",
    "jupyter_app",
    "django_extensions",
    "visualization",
    "dashboard",
    "image_visualize",
    "dashboard_admin",
    "sample",
    "share_analysis",
    "share_dashboard"
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True


ROOT_URLCONF = 'k_qicksight_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Adjust this line as needed
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',    #add this

            ],
        },
    },
]

WSGI_APPLICATION = 'k_qicksight_app.wsgi.application'

# DATABASE
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_USER_NAME = os.getenv("DATABASE_USER_NAME")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DATABASE_NAME,
        'USER': DATABASE_USER_NAME,
        'PASSWORD': DATABASE_PASSWORD,
        'HOST': DATABASE_HOST,
        'PORT': DATABASE_PORT,
    }
}
# DEBUG = False


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 9,
        }
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.github.GithubOAuth2',

]


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 2
}


SIMPLE_JWT = {
    'ALGORITHM': 'HS256',
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=1),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'id',
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

# google
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ.get('CLIENT_ID_GOOGLE_AUTH')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ.get('CLIENT_SECRET_GOOGLE_AUTH')

# github
GITHUB_CLIENT_ID  = os.environ.get('GITHUB_CLIENT_ID')
SOCIAL_SECRET  = os.environ.get('GITHUB_SECRET')

# date
USE_TZ = True
TIME_ZONE = 'Asia/Phnom_Penh'


# email
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

# file
MEDIA_URL = '/media/'
STATIC_ROOT = os.environ.get('static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')


# # jupyter
# NOTEBOOK_ARGUMENTS = [
#     '--ip', '0.0.0.0',
#     '--port', '8888',
# ]

# IPYTHON_KERNEL_DISPLAY_NAME = 'Django Kernel'
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "K_QUICKSIGHT.settings")
# import django
# django.setup()