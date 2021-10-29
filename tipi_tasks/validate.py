import os
import json
from datetime import datetime, date, timedelta

from celery import shared_task
from celery.decorators import periodic_task

from tipi_data.models.alert import Alert

from .mail import send_email
from .sentence import make_sentence
from . import config


@shared_task
def send_validation_emails():
    if getattr(config, 'TEMPLATE_DIR') and config.TEMPLATE_DIR:
        dirname = config.TEMPLATE_DIR
    else:
        dirname = os.path.join(os.path.dirname(__file__), 'templates')

    tmpl = os.path.join(dirname, 'validation.html')
    template = open(tmpl).read()

    # getting all users that've not validated searches
    alerts = Alert.objects.filter(searches__validated=False)
    for alert in alerts:
        searches = alert.searches.filter(validated=False)
        searches = searches.exclude(validation_email_sent=True)
        for search in searches:
            time_passed = (datetime.now() - search.created).days
            timeout = config.VALIDATION_TIMEOUT - time_passed
            context = {
                'tipi_name': config.TIPI_NAME,
                'tipi_email': config.TIPI_EMAIL,
                'search_sentence': make_sentence(search.search),
                'validate_url': "{}/emails/validate/{}/{}".format(
                    config.TIPI_BACKEND,
                    alert.id,
                    search.hash
                    ),
                'timeout': timeout
            }
            search_json = json.loads(search.search)
            kb = search_json['knowledgebase']
            mail_config = config.mail_config(kb)
            send_email([alert.email],
                       config.VALIDATION_EMAIL_SUBJECT,
                       template,
                       mail_config,
                       context)
            search.validation_email_sent=True
            search.validation_email_sent_date=datetime.now()
        alert.save()


@periodic_task(run_every=timedelta(seconds=config.CLEAN_EMAILS_TIMEOUT))
def clean_emails():
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


@periodic_task(run_every=timedelta(seconds=config.CLEAN_EMAILS_TIMEOUT))
def clean_alerts_with_past_dates():
    alerts = Alert.objects.filter(searches__validated=True)
    for alert in alerts:
        searches = alert.searches.filter(validated=True)
        for search in searches:
            search_obj = json.loads(search.search)
            if 'enddate' in search_obj.keys():
                if str(date.today()) < search_obj['enddate']:
                    continue
                alerts.update(pull__searches__hash=search.hash)

    # Remove emails without searches
    Alert.objects.filter(searches__size=0).delete()
