from celery import shared_task

from .models import Alert


@shared_task
def send_validation_emails():
    # getting all users that've not validated searches
    alerts = Alert.objects.filter(searches__validated=False)
    for alert in alerts:
        searches = alert.searches.filter(validated=False)
        searches = searches.exclude(validation_email_sent=True)
        for search in searches:
            # TODO: send the email to validate
            print("Validating: {} -> {}".format(alert.email, search.hash))
            # TODO: mark as validation email sent
