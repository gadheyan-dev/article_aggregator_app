import mongoengine
import datetime



class Author(mongoengine.EmbeddedDocument):
    name = mongoengine.fields.StringField(max_length=512, required=True)
    email = mongoengine.fields.EmailField(required=False)

class Article(mongoengine.Document):
    _id = mongoengine.fields.ObjectIdField()
    title = mongoengine.fields.StringField(max_length=512, required=True)
    url = mongoengine.fields.URLField(max_length=2000, unique=True, required=True)
    top_image = mongoengine.fields.URLField(max_length=2000, required=False)
    authors = mongoengine.fields.ListField(mongoengine.fields.EmbeddedDocumentField(Author), required = False) 
    summary = mongoengine.fields.StringField(required=False)
    publish_date = mongoengine.fields.DateTimeField(required=False)
    created_at = mongoengine.fields.DateTimeField(default=datetime.datetime.utcnow)
    updated_at = mongoengine.fields.DateTimeField(default=datetime.datetime.utcnow)

