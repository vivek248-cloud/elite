import os
import dj_database_url
from pathlib import Path
import environ
from decouple import config

# Initialize environment variables
env = environ.Env()
environ.Env.read_env()

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


# Security settings
SECRET_KEY = env('DJANGO_SECRET_KEY', default='your-secret-key-here')
DEBUG = env.bool('DEBUG', default=False)

# DEBUG = False

# ALLOWED_HOSTS = ['elite-2f67.onrender.com', 'localhost', '127.0.0.1']
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'elitedreambuilders.in',
    'www.elitedreambuilders.in',
    'theelitedreambuilders.in',
    'www.theelitedreambuilders.in',
    "*"
]




# Database configuration
import dj_database_url
from decouple import config



#for production database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'elite_db',
        'USER': 'elite_user',
        'PASSWORD': 'Admin123',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}


#for local mysql database
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'elite_db',
#         'USER': 'root',
#         'PASSWORD': 'Admin123',
#         'HOST': '127.0.0.1',
#         'PORT': '3306',
#     }
# }



# Installed apps
INSTALLED_APPS = [
    "admin_interface",
    "colorfield",

    # "jazzmin",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'cloudinary_storage',
    'cloudinary',
    'compressor',
    
    'index',
]


# JAZZMIN_SETTINGS = {
#     # -----------------------------------------
#     # APP & MODEL ICONS
#     # -----------------------------------------
#     "icons": {
#         "auth": "fas fa-users",
#         "auth.user": "fas fa-user",
#         "auth.Group": "fas fa-users-cog",

#         # Your models ↓↓
#         "index.Project": "fas fa-building",
#         "index.UpcomingProject": "fas fa-clock",
#         "index.GalleryImage": "fas fa-images",

#         "index.Video": "fas fa-video",
#         "index.ProjectVideo": "fas fa-film",
#         "index.YouTubeVideo": "fab fa-youtube",

#         "index.HomeSlider": "fas fa-sliders-h",
#         "index.SliderVideo": "fas fa-photo-video",
#         "index.AboutVideo": "fas fa-play-circle",
#         "index.AboutTitleVideo": "fas fa-heading",

#         "index.Review": "fas fa-star-half-alt",
#         "index.QuoteRequest": "fas fa-envelope-open-text",
#         "index.BudgetRange": "fas fa-rupee-sign",
#         "index.AboutSection": "fas fa-info-circle",
#     },

#     # Optional: Model order
#     "order_with_respect_to": [
#         "index.Project",
#         "index.UpcomingProject",
#         "index.GalleryImage",

#         "index.Video",
#         "index.ProjectVideo",
#         "index.YouTubeVideo",
#         "index.HomeSlider",
#         "index.SliderVideo",
#         "index.AboutVideo",
#         "index.AboutTitleVideo",

#         "index.Review",
#         "index.QuoteRequest",
#         "index.BudgetRange",
#         "index.AboutSection",
#     ],
# }









# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
# AWS_STORAGE_BUCKET_NAME = 'web'
# AWS_S3_ENDPOINT_URL = 'https://6f8ee577ee779928f03c50fd3fbd2988.r2.cloudflarestorage.com'
# AWS_S3_ADDRESSING_STYLE = "path"
# AWS_S3_FILE_OVERWRITE = False
# AWS_DEFAULT_ACL = 'public-read'

# MEDIA_URL = "https://media.elitedreambuilders.in/"





# Cloudinary media storage

# DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# CLOUDINARY_STORAGE = {
#     'CLOUD_NAME': config('CLOUDINARY_CLOUD_NAME', default='your-cloud-name'),
#     'API_KEY': config('CLOUDINARY_API_KEY', default='your-api-key'),
#     'API_SECRET': config('CLOUDINARY_API_SECRET', default='your-api-secret'),
#     'SECURE': True  # This forces HTTPS
# }

# Use Cloudinary for media URL
# MEDIA_URL = f'https://res.cloudinary.com/{config("CLOUDINARY_CLOUD_NAME")}/'


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Static files (CSS, JS)
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'elite', 'static'),  # Use only this
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]

COMPRESS_ENABLED = True  # Set to True in production
COMPRESS_OFFLINE = True # This is for production


# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URL Configuration
ROOT_URLCONF = 'elite.urls'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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
WSGI_APPLICATION = 'elite.wsgi.application'

# Logging
LOG_DIR = os.path.join(BASE_DIR, 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs/django_errors.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
ADMIN_EMAIL = config('ADMIN_EMAIL')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')


TWILIO_ACCOUNT_SID = config('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = config('TWILIO_AUTH_TOKEN')
TWILIO_WHATSAPP_NUMBER = config('TWILIO_WHATSAPP_NUMBER')
ADMIN_WHATSAPP_NUMBER = config('ADMIN_WHATSAPP_NUMBER')
TWILIO_TEMPLATE_SID = config('TWILIO_TEMPLATE_SID')
TWILIO_TEMPLATE_SID_TWO = config('TWILIO_TEMPLATE_SID_TWO')

WHATSAPP_PHONE_NUMBER_ID = '673301622532805'  # from Meta App
WHATSAPP_ACCESS_TOKEN = 'EAAY21HlH90YBO9ZB3N7d0IIvE95b4P3G8LhpdgQtlhmPfBGBT6EZAXgTCp0QH0k5YdzoacdlNYgEXQz2u13fYvrg2wHrZAnttU2GucGfUYgZB2tbC2YV1ll4ZBwWNNbHi4vZBCjqXW1xZAI0P2cZCRQxfOeEsTMXUd1ZC3PJO8TXGVE21BsqRuVZAABXyDXigUJN1JgrfUR8NT5GZBvXjeA1DFLHfxMybSvDDTdBaoQpSOiMOsZD'  # Graph API Token
ADMIN_WHATSAPP_NUMBER = '919786224099'  # in international format


# Security headers
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_HSTS_SECONDS = 31536000
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Security headers
if DEBUG:
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_HSTS_SECONDS = 0
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False
else:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True


# Auto field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


