from django.core.mail import send_mail
from django.conf import settings

import logging

logger = logging.getLogger(__name__)

def send_notification_email(subject, message, recipient_list):
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,  
        recipient_list,  
        fail_silently=False,  
    )
