import os
from celery import Celery

from . import config


BROKER = os.environ.get('BROKER_URL', config.BROKER)
app = Celery('tasks', broker=BROKER)


def init():
    global app
    app = Celery('tasks', broker=BROKER)


from .alerts import *
from .validate import *
