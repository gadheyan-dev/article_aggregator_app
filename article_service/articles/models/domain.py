import mongoengine
import datetime
from mongoengine.errors import ValidationError


class Domain(mongoengine.Document):
    """
    Represents a domain document with crawling and categorization information.

    Attributes:
        - url (str): The URL of the domain.
        - feeds (list of str, optional): List of RSS feed URLs associated with the domain.
        - outbound_domains (list of str, optional): List of outbound domain URLs.
        - inbound_domains (list of str, optional): List of inbound domain URLs.
        - is_crawlable (bool): Indicates if the domain is crawlable.
        - non_crawlable_reason (str): Reason for non-crawlability (if is_crawlable is False).
        - last_crawled_at (datetime): Timestamp of the last crawl for the domain.
        - crawl_delay_in_minutes (int): The delay between crawls in minutes.
        - created_at (datetime): The timestamp when the domain document was created.
        - updated_at (datetime): The timestamp when the domain document was last updated.

    Example:
        domain = Domain(url="https://example.com", feeds=["https://example.com/feed"],
                        outbound_domains=["https://external1.com", "https://external2.com"],
                        is_crawlable=True, last_crawled_at=datetime.datetime.utcnow(),
                        crawl_delay_in_minutes=1440)
    """

    URL_MAX_LENGTH = 2000
    NON_CRAWLABLE_CHOICES = [
        ('SOCIAL_MEDIA', 'Social Media'),
        ('PERMISSION_DENIED', 'Permission Denied'),
        ('NOT_ARTICLE_WEBSITE', 'Not an Article Website'),
        ('NOT_REACHABLE', 'Website Not Reachable'),
        ('NOT_APPLICABLE', 'Not Applicable'),
    ]
    _id = mongoengine.fields.ObjectIdField()
    url = mongoengine.fields.URLField(max_length=URL_MAX_LENGTH, unique=True)
    feeds = mongoengine.fields.ListField(
        mongoengine.fields.URLField(max_length=URL_MAX_LENGTH), required=False)
    outbound_domains = mongoengine.fields.ListField(
        mongoengine.fields.URLField(max_length=URL_MAX_LENGTH), required=False)
    inbound_domains = mongoengine.fields.ListField(
        mongoengine.fields.URLField(max_length=URL_MAX_LENGTH), required=False)
    is_crawlable = mongoengine.fields.BooleanField(default=True)
    non_crawlable_reason = mongoengine.fields.StringField(
        max_length=50,
        choices=NON_CRAWLABLE_CHOICES,
        default='NOT_APPLICABLE'
    )
    last_crawled_at = mongoengine.fields.DateTimeField(
        default=datetime.datetime.utcnow)
    crawl_delay_in_minutes = mongoengine.fields.IntField(default=1440)
    created_at = mongoengine.fields.DateTimeField(
        default=datetime.datetime.utcnow)
    updated_at = mongoengine.fields.DateTimeField(
        default=datetime.datetime.utcnow)

    readonly_fields = ['_id', 'created_at', 'updated_at']

    def clean(self):
        if not self.is_crawlable and not self.non_crawlable_reason:
            raise ValidationError(
                "If not crawlable, a non-crawlable reason must be provided.")
