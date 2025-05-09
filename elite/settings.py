import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'your-secret-key-here'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    "admin_interface",
    "colorfield",#FOR ADMIN INTERFACE
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'index',
   
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]


STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage" 
ROOT_URLCONF = 'elite.urls'

# LOGGINGS

LOG_DIR = os.path.join(BASE_DIR, 'logs')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

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
            'level': 'ERROR',  # Logs only ERROR messages
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs/django_errors.log',  # Saves logs in "logs" folder
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',  # Logs all messages to console
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

WSGI_APPLICATION = 'elite.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'elite_db',
        'USER': 'root',
        'PASSWORD': 'Admin123',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'elite', 'static',)]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

if not DEBUG:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

EMAIL_FILE_PATH = 'emails'  # Emails will be saved in this folder
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# for serve the mail

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = 'smtp.gmail.com'  # Use your SMTP provider
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'kuttyvivek248@gmail.com'
EMAIL_HOST_PASSWORD = 'obka rnfs hcag fsul'  # Use environment variables instead for security
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "kuttyvivek248@gmail.com")




DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# twillo for whats app messages

# TWILIO_ACCOUNT_SID = 'AC74fcc1e2b934f42c52c8827cc7f6a964' # Twilio account SID
# TWILIO_AUTH_TOKEN = 'f077f0d75005435e589d1d5dc36a715f'
# TWILIO_WHATSAPP_NUMBER = 'whatsapp:+14155238886'  
# ADMIN_WHATSAPP_NUMBER = 'whatsapp:+919786224099'  
# TWILIO_TEMPLATE_SID = 'HX9f214778f20b045c765f51aab1f6c9cc' 

# account_sid = 'AC74fcc1e2b934f42c52c8827cc7f6a964'
# auth_token = 'f077f0d75005435e589d1d5dc36a715f'
# HX47b8a9838ae239185bd97325963516b5 # Your approved template SID

TWILIO_ACCOUNT_SID = 'AC74fcc1e2b934f42c52c8827cc7f6a964'
TWILIO_AUTH_TOKEN = 'f077f0d75005435e589d1d5dc36a715f'
TWILIO_WHATSAPP_NUMBER = '+14155238886' # Twilio sandbox number
ADMIN_WHATSAPP_NUMBER = '+919786224099'  # Admin's number (with country code)
TWILIO_TEMPLATE_SID = 'HX9f214778f20b045c765f51aab1f6c9cc'  # Your approved template SID for message not quote request
