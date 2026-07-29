from pathlib import Path
import os
import dj_database_url


# ==========================
# RUTAS DEL PROYECTO
# ==========================

BASE_DIR = Path(__file__).resolve().parent.parent


# ==========================
# SEGURIDAD
# ==========================

SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-cambia-esta-clave-en-render"
)

DEBUG = False

ALLOWED_HOSTS = ["*"]


# ==========================
# APLICACIONES
# ==========================

INSTALLED_APPS = [

    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",


    # Aplicaciones Material Control CM
    "accounts",
    "dashboard",
    "inventory",
    "materials",
    "movements",
    "projects",
    "people",
]


# ==========================
# MIDDLEWARE
# ==========================

MIDDLEWARE = [

    "django.middleware.security.SecurityMiddleware",

    # Archivos estáticos producción
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",

    "django.middleware.common.CommonMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",

    "django.contrib.messages.middleware.MessageMiddleware",

    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ==========================
# URL PRINCIPAL
# ==========================

ROOT_URLCONF = "config.urls"


# ==========================
# TEMPLATES
# ==========================

TEMPLATES = [

    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",

        "DIRS": [
            BASE_DIR / "templates"
        ],

        "APP_DIRS": True,

        "OPTIONS": {

            "context_processors": [

                "django.template.context_processors.request",

                "django.contrib.auth.context_processors.auth",

                "django.contrib.messages.context_processors.messages",

            ],
        },
    },
]


# ==========================
# WSGI
# ==========================

WSGI_APPLICATION = "config.wsgi.application"


# ==========================
# BASE DE DATOS
# PostgreSQL Render
# ==========================

DATABASES = {

    "default": dj_database_url.config(

        default=os.environ.get(
            "DATABASE_URL"
        ),

        conn_max_age=600

    )

}


# ==========================
# VALIDACIÓN PASSWORD
# ==========================

AUTH_PASSWORD_VALIDATORS = [

    {
        "NAME":
        "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },

    {
        "NAME":
        "django.contrib.auth.password_validation.MinimumLengthValidator",
    },

    {
        "NAME":
        "django.contrib.auth.password_validation.CommonPasswordValidator",
    },

    {
        "NAME":
        "django.contrib.auth.password_validation.NumericPasswordValidator",
    },

]


# ==========================
# IDIOMA Y ZONA HORARIA
# ==========================

LANGUAGE_CODE = "es-co"

TIME_ZONE = "America/Bogota"

USE_I18N = True

USE_TZ = True



# ==========================
# ARCHIVOS ESTÁTICOS
# CSS JS IMÁGENES LOGO
# ==========================

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [

    BASE_DIR / "static"

]


# ==========================
# MEDIA
# Fotografías de materiales
# ==========================

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"



# ==========================
# ARCHIVOS PDF / REPORTES
# ==========================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"



# ==========================
# LOGIN
# ==========================

LOGIN_URL = "/login/"

LOGIN_REDIRECT_URL = "/"

LOGOUT_REDIRECT_URL = "/login/"



# ==========================
# SEGURIDAD HTTPS RENDER
# ==========================

SECURE_PROXY_SSL_HEADER = (
    "HTTP_X_FORWARDED_PROTO",
    "https"
)


CSRF_TRUSTED_ORIGINS = [

    "https://*.onrender.com"

]