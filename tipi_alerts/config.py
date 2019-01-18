DEBUG = False
BROKER = 'redis://redis:6379/0'

TIPI_NAME = 'TIPI'
TIPI_DESCRIPTION = ''
TIPI_EMAIL = 'tipi@ciecode.es'
TIPI_FRONTEND = 'http://localhost:8080'
TIPI_BACKEND = 'http://localhost:5000'
TIPI_COLOR = '#000000'

MONGO_DB = 'tipi'
MONGO_HOST = 'db'
MONGO_PORT = 27017
MONGO_USER = ''
MONGO_PASSWORD = ''

VALIDATION_EMAIL_SUBJECT = 'Validación de alerta en {}'.format(TIPI_NAME)
ALERT_EMAIL_SUBJECT = 'Hay nuevas alertas de {} para ti'.format(TIPI_NAME)
SPARKPOST_API = 'XXXXXXXXXXXXXXXXXXXXXXX'
FROM_EMAIL = 'test@example.com'

TEMPLATE_DIR = None
# validation timeout in days
VALIDATION_TIMEOUT = 5
# Timeout to run the clean email task every X seconds
CLEAN_EMAILS_TIMEOUT = 300

ALERT_BANNER_URL = ''

try:
    from local_config import *
except:
    pass
