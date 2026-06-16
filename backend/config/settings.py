import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'dev-insecure-change-me')
DEBUG = os.environ.get('DJANGO_DEBUG', '1') == '1'
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '*').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'pgvector',
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'acp'),
        'USER': os.environ.get('POSTGRES_USER', 'acp'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'acp'),
        'HOST': os.environ.get('POSTGRES_HOST', 'db'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
]

LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOW_ALL_ORIGINS = DEBUG
CORS_ALLOWED_ORIGINS = [
    o.strip()
    for o in os.environ.get('CORS_ALLOWED_ORIGINS', 'http://localhost:28433,http://localhost:5173').split(',')
    if o.strip()
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50,
}

# MinIO / Archive (DoRaGi-LM 패턴: /ARCHIVE/{project}/minio|data|models)
ARCHIVE_PROJECT = os.environ.get('ARCHIVE_PROJECT', 'acp').strip('/')
ARCHIVE_BASE = os.environ.get('ARCHIVE_BASE', f'/ARCHIVE/{ARCHIVE_PROJECT}')
MINIO_ENDPOINT = os.environ.get('MINIO_ENDPOINT', 'minio:9000')
MINIO_ACCESS_KEY = os.environ.get('MINIO_ACCESS_KEY', 'acp')
MINIO_SECRET_KEY = os.environ.get('MINIO_SECRET_KEY', 'acpminio123')
MINIO_BUCKET = os.environ.get('MINIO_BUCKET', 'acp')
MINIO_SECURE = os.environ.get('MINIO_SECURE', '0') == '1'
ARCHIVE_PREFIX = os.environ.get('ARCHIVE_PREFIX', 'data').strip('/')
ARCHIVE_ROOT = os.environ.get('ARCHIVE_ROOT', f'{ARCHIVE_BASE}/data')
ARCHIVE_MODELS_ROOT = os.environ.get('ARCHIVE_MODELS_ROOT', f'{ARCHIVE_BASE}/models')

# Gemini
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
GEMINI_EMBED_MODEL = os.environ.get('GEMINI_EMBED_MODEL', 'gemini-embedding-2')
GEMINI_LLM_MODEL = os.environ.get('GEMINI_LLM_MODEL', 'gemini-3.1-flash-lite')
GEMINI_EMBED_DIM = int(os.environ.get('GEMINI_EMBED_DIM', '768'))

# Firebase Auth (Google 로그인 ID 토큰 검증)
FIREBASE_PROJECT_ID = os.environ.get('FIREBASE_PROJECT_ID', '')
FIREBASE_SERVICE_ACCOUNT_JSON = os.environ.get('FIREBASE_SERVICE_ACCOUNT_JSON', '')
FIREBASE_SERVICE_ACCOUNT_PATH = Path(
    os.environ.get('FIREBASE_SERVICE_ACCOUNT_PATH', BASE_DIR / 'secrets' / 'firebase-service-account.json')
)
