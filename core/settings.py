import os
from pathlib import Path
from configurations import Configuration
from dotenv import load_dotenv

load_dotenv()

# Global Settings
class Common(Configuration):
    """
    Configuración base común para todos los entornos.
    """
    
    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent.parent
    SECRET_KEY = os.getenv('SECRET_KEY', '')
    ALLOWED_HOSTS = []

    # SECURITY WARNING: keep the secret key used in production secret!
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'corsheaders', # Django Cors Headers
        'rest_framework',  # Django REST Framework para construir APIs
        'drf_yasg',  # Herramienta para generar documentación de API con Swagger
        '_apps.warehouse'
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
    ]

    ROOT_URLCONF = 'core.urls'

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

    WSGI_APPLICATION = 'core.wsgi.application'

    # Configuración de Loggin para registrar errores
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            # Handler para logs en consola
            'console': {
                'class': 'logging.StreamHandler',
            },
            # Handler para logs de errores
            'file_errors': {
                'level': 'ERROR',
                'class': 'logging.FileHandler',
                'filename': 'errors.log',
            },
            # Handler para logs de warnings específicos de la app warehouse
            'file_warnings': {
                'level': 'WARNING',
                'class': 'logging.FileHandler',
                'filename': 'warehouse.log',
            },
        },
        'loggers': {
            # Logger para la captura de errores de Django
            'django': {
                'handlers': ['file_errors'],  # Registrar los errores en errors.log
                'level': 'ERROR',
                'propagate': True,
            },
            # Logger específico para la app warehouse
            'warehouse': {
                'handlers': ['console', 'file_warnings'],  # Registrar warnings en warehouse.log y mostrarlos en consola
                'level': 'WARNING',
                'propagate': True,
            },
        },
    }

    # Configuración de la Base de Datos usando PostgreSQL
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.getenv('POSTGRES_DB', ''),
            'USER': os.getenv('POSTGRES_USER', ''),
            'PASSWORD': os.getenv('POSTGRES_PASSWORD', ''),
            'HOST': os.getenv('POSTGRES_HOST', ''),
            'PORT': os.getenv('POSTGRES_PORT', ''),
            'OPTIONS': {
                'options': '-c search_path=public'  # Define el esquema por defecto
            },
        }        
    }

    # Validación de contraseñas
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

    # Internacionalización
    LANGUAGE_CODE = 'en-us'
    TIME_ZONE = 'UTC'
    USE_I18N = True
    USE_TZ = True

    # Configuración de archivos estáticos
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# Configuración para entornos de desarrollo
class Dev(Common):
    """
    Configuración específica para el entorno de desarrollo.
    """
    CORS_ALLOWED_ORIGINS = ['http://localhost:5173', 'https://main.dlz6ua40g7mkh.amplifyapp.com']
    ALLOWED_HOSTS = ['localhost', 'flk-crud-backend.up.railway.app']
    DEBUG = True  # Habilita el modo de depuración

# Configuración para entornos de producción
class Prod(Common):
    """
    Configuración específica para el entorno de producción.
    """
    CORS_ALLOWED_ORIGINS = ['https://main.dlz6ua40g7mkh.amplifyapp.com']
    ALLOWED_HOSTS = ['flk-crud-backend.up.railway.app']
    DEBUG = True

    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
