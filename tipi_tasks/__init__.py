from os import environ as env

from celery import Celery

from . import config


app = Celery('tasks', broker=config.BROKER, backend=config.RESULT_BACKEND)


def init():
    global app
    app = Celery('tasks', broker=config.BROKER, backend=config.RESULT_BACKEND)


from .alerts import *
from .tagger import *
from .validate import *
from .scanned import *
