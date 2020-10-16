from celery import shared_task
from tipi_data.models.scanned import Scanned

@periodic_task(run_every=timedelta(hours=12))
def clean_documents():
    scans = Scanned.objects.filter(expiration__lte=datetime.date.today())

    for scan in scans:
        scan.delete()
