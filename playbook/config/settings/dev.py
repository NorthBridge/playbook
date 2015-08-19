# Import base to override settings
from .base import *
from os import environ

# Override the email settings in the base.
EMAIL_USE_TLS = True
EMAIL_HOST = '<smtp_server>'
EMAIL_HOST_USER = '<user>'
EMAIL_HOST_PASSWORD = '<passwd>'
EMAIL_PORT = 587
EMAIL_RECIPIENT_LIST = ['EMAIL_HOST_USER']

# Override Github settings

GITHUB_OWNER = environ['PLAYBOOK_GITHUB_OWNER']
GITHUB_TOKEN = environ['PLAYBOOK_GITHUB_TOKEN']
GITHUB_WEBHOOK_SECRET = environ['PLAYBOOK_GITHUB_WEBHOOK_SECRET']
