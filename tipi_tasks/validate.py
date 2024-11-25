import os
import json
from datetime import datetime, date, timedelta

from celery import shared_task
from celery.utils.log import get_task_logger

from tipi_data.models.alert import Alert

from .mail import send_email
from .sentence import make_sentence
from . import config


log = get_task_logger(__name__)


def get_project_name(kb):
    names = {"politicas": "QHLD", "ods": "Parlamento2030"}

    return names[kb]


@shared_task
def send_validation_emails():
    if getattr(config, "TEMPLATE_DIR") and config.TEMPLATE_DIR:
        dirname = config.TEMPLATE_DIR
    else:
        dirname = os.path.join(os.path.dirname(__file__), "templates")

    tmpl = os.path.join(dirname, "validation.html")
    template = open(tmpl).read()

    # getting all users that've not validated searches
    alerts = Alert.objects.filter(searches__validated=False)
    for alert in alerts:
        searches = alert.searches.filter(validated=False)
        searches = searches.exclude(validation_email_sent=True)
        for search in searches:
            time_passed = (datetime.now() - search.created).days
            timeout = config.VALIDATION_TIMEOUT - time_passed
            search_json = json.loads(search.search)
            kb = (
                search_json["knowledgebase"]
                if "knowledgebase" in search_json
                else "politicas"
            )
            mail_config = config.mail_config(kb)
            context = {
                "tipi_name": get_project_name(kb),
                "tipi_email": mail_config["FROM"],
                "search_sentence": make_sentence(search.search),
                "validate_url": "{}/emails/validate/{}/{}".format(
                    mail_config["BACKEND"], alert.id, search.hash
                ),
                "timeout": timeout,
            }
            send_email(
                [alert.email],
                mail_config["VALIDATION_SUBJECT"],
                template,
                mail_config,
                context,
            )
            search.validation_email_sent = True
            search.validation_email_sent_date = datetime.now()
        alert.save()


@shared_task
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


@shared_task
def clean_alerts_with_past_dates():
    alerts = Alert.objects.filter(searches__validated=True)
    for alert in alerts:
        searches = alert.searches.filter(validated=True)
        for search in searches:
            search_obj = json.loads(search.search)
            if "enddate" in search_obj.keys():
                if str(date.today()) < search_obj["enddate"]:
                    continue
                alerts.update(pull__searches__hash=search.hash)

    # Remove emails without searches
    Alert.objects.filter(searches__size=0).delete()
