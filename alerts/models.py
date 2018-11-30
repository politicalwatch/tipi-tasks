import mongoengine as db
from . import config


db.connect(config.MONGO_DB, host=config.MONGO_HOST, port=config.MONGO_PORT,
           username=config.MONGO_USER, password=config.MONGO_PASSWORD)


class Search(db.EmbeddedDocument):
    hash = db.StringField(unique=True)
    search = db.StringField()
    created = db.DateTimeField()
    validated = db.BooleanField()
    validation_email_sent = db.BooleanField()
    validation_email_sent_date = db.DateTimeField()

    def __str__(self):
        return self.hash


class Alert(db.Document):
    id = db.StringField(db_field='_id', primary_key=True)
    email = db.StringField()
    searches = db.EmbeddedDocumentListField(Search)

    meta = {
        'collection': 'alerts',
    }

    def __str__(self):
        return self.email
