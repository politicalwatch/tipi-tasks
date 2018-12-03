import os
from datetime import datetime

from celery import shared_task

from .models import Alert
from .mail import send_email


@shared_task
def send_validation_emails():
    dirname = os.path.dirname(__file__)
    tmpl = os.path.join(dirname, 'templates', 'validation.html')
    template = open(tmpl).read()

    # getting all users that've not validated searches
    alerts = Alert.objects.filter(searches__validated=False)
    for alert in alerts:
        searches = alert.searches.filter(validated=False)
        searches = searches.exclude(validation_email_sent=True)
        for search in searches:
            context = {
                'hash': search.hash,
            }
            send_email([alert.email],
                       "Validación de alerta",
                       template,
                       context)
            search.validation_email_sent=True
            search.validation_email_sent_date=datetime.now()
        alert.save()

