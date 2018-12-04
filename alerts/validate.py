import os
from datetime import datetime
from datetime import timedelta

from celery import shared_task
from celery.decorators import periodic_task

from . import models
from .models import Alert
from .mail import send_email
from . import config


@shared_task
def send_validation_emails():
    if getattr(config, 'TEMPLATE_DIR') and config.TEMPLATE_DIR:
        dirname = config.TEMPLATE_DIR
    else:
        dirname = os.path.join(os.path.dirname(__file__), 'templates')

    tmpl = os.path.join(dirname, 'validation.html')
    template = open(tmpl).read()

    models.connect()

    # getting all users that've not validated searches
    alerts = Alert.objects.filter(searches__validated=False)
    for alert in alerts:
        searches = alert.searches.filter(validated=False)
        searches = searches.exclude(validation_email_sent=True)
        for search in searches:
            time_passed = (datetime.now() - search.created).days
            timeout = config.VALIDATION_TIMEOUT - time_passed
            context = {
                'hash': search.hash,
                'email_id': alert.id,
                'email': alert.email,
                'timeout': timeout,
            }
            send_email([alert.email],
                       config.VALIDATION_EMAIL_SUBJECT,
                       template,
                       context)
            search.validation_email_sent=True
            search.validation_email_sent_date=datetime.now()
        alert.save()


@periodic_task(run_every=timedelta(seconds=config.CLEAN_EMAILS_TIMEOUT))
def clean_emails():
    models.connect()

    alerts = Alert.objects.filter(searches__validated=False)
    timeout = datetime.now() - timedelta(days=config.VALIDATION_TIMEOUT)
    for alert in alerts:
        searches = alert.searches.filter(validated=False)
        for search in searches:
            if search.created > timeout:
                continue
            alerts.update(pull__searches__hash=search.hash)

    # Remove emails without searches
    Alert.objects.filter(searches__size=0).delete()
