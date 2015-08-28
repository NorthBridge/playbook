# Import base to override settings
from .base import *
import os

# Override the email settings in the base.
#EMAIL_USE_TLS = True
#EMAIL_HOST = '<smtp_server>'
#EMAIL_HOST_USER = '<user>'
#EMAIL_HOST_PASSWORD = '<passwd>'
#EMAIL_PORT = 587
#EMAIL_RECIPIENT_LIST = ['EMAIL_HOST_USER']

# Override Github settings

GITHUB_OWNER = os.getenv('PLAYBOOK_GITHUB_OWNER')
GITHUB_TOKEN = os.getenv('PLAYBOOK_GITHUB_TOKEN')
GITHUB_WEBHOOK_SECRET = os.getenv('PLAYBOOK_GITHUB_WEBHOOK_SECRET')
DEBUG = os.getenv('DEBUG', True)

DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME':     'playbook_dev',
    'USER':     'postgres',
    'PASSWORD': 'postgres',
    'HOST':     'localhost',
    'PORT':     '5432',
    }
}
