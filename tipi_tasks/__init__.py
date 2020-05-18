from os import environ as env

import sentry_sdk
from celery import Celery
from sentry_sdk.integrations.celery import CeleryIntegration

from . import config


SENTRY_DSN = env.get('SENTRY_DSN', None)
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[CeleryIntegration()]
    )

app = Celery('tasks', broker=config.BROKER, backend=config.RESULT_BACKEND)


def init():
    global app
    app = Celery('tasks', broker=config.BROKER, backend=config.RESULT_BACKEND)


from .alerts import *
from .tagger import *
from .validate import *
