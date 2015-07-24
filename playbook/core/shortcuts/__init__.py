import re
import json
from os.path import join
import logging

from django.core.mail import send_mail

from ...settings import CORE_PROJECT_DIR, EMAIL_HOST_USER, EMAIL_RECIPIENT_LIST


logger = logging.getLogger("playbook")


def get_single_config(key):
    config_path = join(CORE_PROJECT_DIR, 'CONFIG')
    with open(config_path, 'r') as jsonConfig:
        data = json.load(jsonConfig)
        for i, p in re.findall(r'(\d+)|(\w+)', key):
            data = data.get(p or int(i), None)
        return data


def get_config(*keys):
    values = []
    for key in keys:
        values.append(get_single_config(key))
    if len(values) == 1:
        return values[0]
    return tuple(values)


def send_email(subject, body, to=EMAIL_RECIPIENT_LIST):
    try:
        send_mail(subject, body, EMAIL_HOST_USER,
                  to, fail_silently=False)
    except:
        logger.exception("Error when trying to send email:\n" +
                         "\tSubject: %s\n" +
                         "\tBody: %s\n" +
                         "\tRecipient: %s", subject, body, to)


def create_json_message_object(message, field="__all__", code="invalid"):
    return json.dumps({field: [{"message": message, "code": code}]})
