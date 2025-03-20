import os
import pymysql
from pathlib import Path
from urllib.parse import urlparse

pymysql.install_as_MySQLdb()

# Ruta base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Seguridad
SECRET_KEY = os.getenv("SECRET_KEY", "DMcL1V8CwL1adJFPeJG0E9Qlpn740wpmW2cAcuSv_CDw1LX6UK1ZvIfLNPwzpvjJfHM")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Hosts permitidos
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1,maquina-production.up.railway.app").split(",")

# Aplicaciones Instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',  
 
]
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],  # 🔹 Verifica que esta línea esté correcta
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


# Middlewares (Seguridad y Manejo de Sesiones)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configuración de URLs
ROOT_URLCONF = 'maquina.urls'

# Configuración de Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],  # Carpeta de plantillas opcional
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

# Configuración de WSGI
WSGI_APPLICATION = 'maquina.wsgi.application'

# Configuración de la Base de Datos
DATABASE_URL = os.getenv("DATABASE_URL", "")
if DATABASE_URL:
    db_url = urlparse(DATABASE_URL)
    
    # Validar si el puerto es un número antes de convertirlo
    try:
        db_port = db_url.port if db_url.port else 3306
    except ValueError:
        db_port = 3306  # Usar un puerto por defecto si no es un número

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': db_url.path[1:],  # Quita la barra inicial
            'USER': db_url.username,
            'PASSWORD': db_url.password,
            'HOST': db_url.hostname,
            'PORT': db_port,
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
            }
        }
    }
else:
    print("⚠️ ERROR: No se encontró la variable de entorno DATABASE_URL")
    DATABASES = {}

# Validadores de Contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Configuración de Internacionalización
LANGUAGE_CODE = 'es'  # Cambiado a español
TIME_ZONE = 'America/Santiago'  # Ajustar según país
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Configuración de Archivos Estáticos
# Configuración de Archivos Estáticos
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"] if (BASE_DIR / "static").exists() else []
STATIC_ROOT = BASE_DIR / "staticfiles"

if not DEBUG:
    STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

# Configuración de Archivos de Medios
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"

# Configuración de Claves Primarias por Defecto
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 🔹 Configuración adicional para Railway
CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS", "https://maquina.up.railway.app,http://localhost").split(",")
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Configuración del puerto en Railway
PORT = os.getenv("PORT", "8000")

# 🔹 Agregando Logs en Producción
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
    STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
