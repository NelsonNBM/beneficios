import os
import pymysql
from pathlib import Path
from urllib.parse import urlparse

pymysql.install_as_MySQLdb()

# Ruta base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Seguridad
SECRET_KEY = os.getenv("SECRET_KEY", "DMcL1V8CwL1adJFPeJG0E9Qlpn740wpmW2cAcuSv_CDw1LX6UK1ZvIfLNPwzpvjJfHM")
DEBUG = os.getenv("DEBUG", "true").lower() == "true"

# Hosts permitidos
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1,web-beneficios.up.railway.app").split(",")

# 🔹 Confianza en dominios CSRF
CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS", "https://web-beneficios.up.railway.app").split(",")

# Aplicaciones instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
]

# Middleware (agregamos WhiteNoise para producción)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Necesario para producción
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configuración de URLs
ROOT_URLCONF = 'beneficios.urls'

# Configuración de plantillas
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
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

# WSGI
WSGI_APPLICATION = 'beneficios.wsgi.application'

# Base de datos (MySQL desde variable DATABASE_URL)
DATABASE_URL = os.getenv("DATABASE_URL", "")
if DATABASE_URL:
    db_url = urlparse(DATABASE_URL)
    
    try:
        db_port = db_url.port if db_url.port else 3306
    except ValueError:
        db_port = 3306

    try:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': db_url.path[1:] if db_url.path else os.getenv("DATABASE_NAME", "railway"),
                'USER': db_url.username if db_url.username else os.getenv("DATABASE_USER", "root"),
                'PASSWORD': db_url.password if db_url.password else os.getenv("DATABASE_PASSWORD", ""),
                'HOST': db_url.hostname if db_url.hostname else os.getenv("DATABASE_HOST", "localhost"),
                'PORT': db_port if db_url.port else int(os.getenv("DATABASE_PORT", "3306")),
                'OPTIONS': {
                    'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
                }
            }
        }
    except Exception as e:
        print(f"⚠️ ERROR: No se pudo configurar la base de datos correctamente: {e}")
        DATABASES = {}
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / "db.sqlite3",
        }
    }

# Validadores de contraseña
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internacionalización
LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Archivos estáticos
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"] if (BASE_DIR / "static").exists() else []
STATIC_ROOT = BASE_DIR / "staticfiles"

# Producción
if not DEBUG:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Archivos multimedia
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"

# ID por defecto
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# SSL para Railway
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Puerto Railway
PORT = os.getenv("PORT", "8000")

# Logging
if not DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'file': {
                'level': 'ERROR',
                'class': 'logging.FileHandler',
                'filename': BASE_DIR / 'django_error.log',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['file'],
                'level': 'ERROR',
                'propagate': True,
            },
        },
    }