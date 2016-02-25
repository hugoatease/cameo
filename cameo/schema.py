from mongoengine import fields, EmbeddedDocument, Document


class Instagram(EmbeddedDocument):
    number = fields.StringField()
    username = fields.StringField()
    fullname = fields.StringField()
    text = fields.StringField()


class Media(Document):
    date = fields.DateTimeField(required=True)
    url = fields.URLField(required=True)
    type = fields.StringField(required=True, choices=('photo', 'video'))
    thumbnail_url = fields.URLField()
    instagram = fields.EmbeddedDocumentField(Instagram)