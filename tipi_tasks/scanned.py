from datetime import datetime, timedelta
import time
from celery import shared_task
from tipi_data.models.scanned import Scanned
from . import config
import os
from .mail import send_email


@shared_task
def clean_documents():
    scans = Scanned.objects.filter(expiration__lte=datetime.today())

    for scan in scans:
        scan.delete()


@shared_task
def notify_new_documents():
    ONE_DAY_IN_SECONDS = 60 * 60 * 24
    creation = time.mktime(datetime.now().timetuple()) - ONE_DAY_IN_SECONDS
    creation_date = datetime.fromtimestamp(creation)

    scans = Scanned.objects.filter(created__gte=creation_date, verified=False)

    if len(scans) == 0:
        return

    if getattr(config, "TEMPLATE_DIR") and config.TEMPLATE_DIR:
        dirname = config.TEMPLATE_DIR
    else:
        dirname = os.path.join(os.path.dirname(__file__), "templates")

    tmpl = os.path.join(dirname, "new_documents.html")
    template = open(tmpl).read()

    context = {
        "banner_url": config.ALERT_BANNER_URL,
        "tipi_frontend": config.TIPI_FRONTEND,
        "documents": scans,
    }

    send_email(
        ["info@politicalwatch.es"],
        "Nuevos documentos no verificados",
        template,
        context,
    )
