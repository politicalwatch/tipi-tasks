import os
import ast
from datetime import datetime

from celery import shared_task

from tipi_data.models.alert import Alert, InitiativeAlert

from .mail import send_email
from .sentence import make_sentence
from . import config


@shared_task
def send_alerts():
    if getattr(config, 'TEMPLATE_DIR') and config.TEMPLATE_DIR:
        dirname = config.TEMPLATE_DIR
    else:
        dirname = os.path.join(os.path.dirname(__file__), 'templates')

    tmpl = os.path.join(dirname, 'alert.html')
    template = open(tmpl).read()

    alerts = Alert.objects.filter(searches__validated=True)
    for alert in alerts:
        alert_to_send = {
                'id': alert.id,
                'searches': []
                }
        searches = alert.searches.filter(validated=True)
        for search in searches:
            initiatives = InitiativeAlert.objects(
                    __raw__=ast.literal_eval(search.dbsearch)
                ).exclude('content')
            if initiatives.count():
                alert_to_send['searches'].append({
                    'hash': search.hash,
                    'search_sentence': make_sentence(search.search),
                    'initiatives': [
                        {'id': initiative.id, 'title': initiative.title}
                        for initiative in initiatives
                        ]
                    })
        if len(alert_to_send['searches']):
            context = {
                'tipi_name': config.TIPI_NAME,
                'tipi_description': config.TIPI_DESCRIPTION,
                'tipi_color': config.TIPI_COLOR,
                'tipi_email': config.TIPI_EMAIL,
                'tipi_frontend': config.TIPI_FRONTEND,
                'tipi_backend': config.TIPI_BACKEND,
                'banner_url': config.ALERT_BANNER_URL,
                'alert': alert_to_send
            }
            send_email([alert.email],
                       config.ALERT_EMAIL_SUBJECT,
                       template,
                       context)

    InitiativeAlert.drop_collection()
