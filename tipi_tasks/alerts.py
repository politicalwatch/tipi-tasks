import os
import ast
import json
import logging
from datetime import datetime

from celery import shared_task

from tipi_data.repositories.alerts import Alerts, InitiativeAlerts

from .mail import send_email
from .sentence import make_sentence
from . import config


log = logging.getLogger(__name__)


@shared_task
def send_alerts():
    if getattr(config, 'TEMPLATE_DIR') and config.TEMPLATE_DIR:
        dirname = config.TEMPLATE_DIR
    else:
        dirname = os.path.join(os.path.dirname(__file__), 'templates')

    tmpl = os.path.join(dirname, 'alert.html')
    template = open(tmpl).read()

    alerts = Alerts.get_validated()
    for alert in alerts:
        alert_to_send = {}
        searches = alert.searches.filter(validated=True)
        for search in searches:
            try:
                search_json = json.loads(search.search)
                kb = search_json['knowledgebase']
                initiatives = InitiativeAlerts.by_search(ast.literal_eval(search.dbsearch), kb).exclude('content')
                if kb not in alert_to_send:
                    alert_to_send[kb] = {
                        'id': alert.id,
                        'searches': []
                    }
                if initiatives.count():
                    alert_to_send[kb]['searches'].append({
                        'hash': search.hash,
                        'search_sentence': make_sentence(search.search),
                        'initiatives': [
                            {'id': initiative.id, 'title': initiative.title}
                            for initiative in initiatives
                            ]
                        })
            except Exception as e:
                log.error(f"{alert.email}: {e}")

        for kb in alert_to_send:
            try:
                if not len(alert_to_send[kb]['searches']):
                    continue

                mail_config = config.mail_config(kb)
                context = {
                    'tipi_name': mail_config['NAME'],
                    'tipi_description': mail_config['DESCRIPTION'],
                    'tipi_color': mail_config['COLOR'],
                    'tipi_email': mail_config['EMAIL'],
                    'tipi_frontend': mail_config['FRONTEND'],
                    'tipi_backend': mail_config['BACKEND'],
                    'banner_url': mail_config['BANNER_URL'],
                    'alert': alert_to_send[kb]
                }
                send_email([alert.email],
                           mail_config['ALERT_SUBJECT'],
                           template,
                           mail_config,
                           context)
            except Exception as e:
                log.error(f"{alert.email}: {e}")

    InitiativeAlerts.clear()
