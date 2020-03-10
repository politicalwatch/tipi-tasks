from os import environ as env


DEBUG = env.get('DEBUG', 'False') == 'True'
BROKER = env.get('BROKER', 'redis://redis:6379/2')
RESULT_BACKEND = env.get('RESULT_BACKEND', 'redis://redis:6379/3')

TIPI_NAME = env.get('TIPI_NAME', 'TIPI')
TIPI_DESCRIPTION = env.get('TIPI_DESCRIPTION', '')
TIPI_EMAIL = env.get('TIPI_EMAIL', 'tipi@ciecode.es')
TIPI_FRONTEND = env.get('TIPI_FRONTEND', 'http://localhost:8080')
TIPI_BACKEND = env.get('TIPI_BACKEND', 'http://localhost:5000')
TIPI_COLOR = env.get('TIPI_COLOR', '#000000')

MONGO_DB = env.get('MONGO_DB_NAME', 'tipi')
MONGO_HOST = env.get('MONGO_HOST', 'db')
MONGO_PORT = int(env.get('MONGO_PORT', '27017'))
MONGO_USER = env.get('MONGO_USER', '')
MONGO_PASSWORD = env.get('MONGO_PASSWORD', '')

VALIDATION_EMAIL_SUBJECT = env.get('VALIDATION_EMAIL_SUBJECT', 'Validación de alerta en {}').format(TIPI_NAME)
ALERT_EMAIL_SUBJECT = env.get('ALERT_EMAIL_SUBJECT', 'Hay nuevas alertas de {} para ti').format(TIPI_NAME)
SPARKPOST_API = env.get('SPARKPOST_API', 'XXXXXXXXXXXXXXXXXXXXXXX')
FROM_EMAIL = env.get('FROM_EMAIL', 'test@example.com')

TEMPLATE_DIR = env.get('TEMPLATE_DIR', None)
# validation timeout in days
VALIDATION_TIMEOUT = int(env.get('VALIDATION_TIMEOUT', '30'))
# Timeout to run the clean email task every X seconds
CLEAN_EMAILS_TIMEOUT = int(env.get('CLEAN_EMAILS_TIMEOUT', '300'))

ALERT_BANNER_URL = env.get('ALERT_BANNER_URL', '')

CACHE_REDIS_DB = int(env.get('CACHE_REDIS_DB_NAME', '8'))
CACHE_REDIS_HOST = env.get('CACHE_REDIS_HOST', 'redis')
CACHE_REDIS_PORT = int(env.get('CACHE_REDIS_PORT', '6379'))
