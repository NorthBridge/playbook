import json
from django.core.mail import send_mail
from django.conf import settings


def create_json_message_object(message, field='__all__', code='invalid'):
    return json.dumps({field: [{'message': message, 'code': code}]})

def send_email(subject, to=settings.EMAIL_RECIPIENT_LIST):
    try:
        send_mail(subject, body, EMAIL_HOST_USER, to, fail_silently=False)
    except:
        logger.exception('Error when trying to send email:\n' +
                         '\tSubject: %s\n' +
                         '\tBody: %s\n' +
                         '\tRecipient: %s', subject, body, to)
