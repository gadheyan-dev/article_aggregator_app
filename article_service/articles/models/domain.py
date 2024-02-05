import mongoengine
import datetime
from mongoengine.errors import ValidationError


    
class Domain(mongoengine.Document):
    
    URL_MAX_LENGTH = 2000
    NON_CRAWLABLE_CHOICES = [
        ('SOCIAL_MEDIA', 'Social Media'),
        ('PERMISSION_DENIED', 'Permission Denied'),
        ('NOT_ARTICLE_WEBSITE', 'Not an Article Website'),
    ]
    _id = mongoengine.fields.ObjectIdField()
    url = mongoengine.fields.URLField(max_length=URL_MAX_LENGTH, unique=True)
    feeds = mongoengine.fields.ListField(mongoengine.fields.URLField(max_length=URL_MAX_LENGTH), required=False)
    is_crawlable = mongoengine.fields.BooleanField(default=True)
    non_crawlable_reason = mongoengine.fields.StringField(
        max_length=50,
        choices=NON_CRAWLABLE_CHOICES,
    )
    last_crawled_at = mongoengine.fields.DateTimeField(default=datetime.datetime.utcnow)
    crawl_delay_in_minutes = mongoengine.fields.IntField(default=1440)
    created_at = mongoengine.fields.DateTimeField(default=datetime.datetime.utcnow)
    updated_at = mongoengine.fields.DateTimeField(default=datetime.datetime.utcnow)

    def clean(self):
        if not self.is_crawlable and not self.non_crawlable_reason:
            raise ValidationError("If not crawlable, a non-crawlable reason must be provided.")