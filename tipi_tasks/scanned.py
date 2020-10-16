from datetime import datetime, timedelta
from celery.decorators import periodic_task
from tipi_data.models.scanned import Scanned

@periodic_task(run_every=timedelta(hours=12))
def clean_documents():
    scans = Scanned.objects.filter(expiration__lte=datetime.today())

    for scan in scans:
        scan.delete()
