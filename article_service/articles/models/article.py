import mongoengine
import datetime


class Author(mongoengine.EmbeddedDocument):
    """
    Represents an author of an article.

    Attributes:
        - name (str): The name of the author.
        - email (str): The email address of the author (optional).

    Example:
        author = Author(name="John Doe", email="john.doe@example.com")
    """
    name = mongoengine.fields.StringField(max_length=512, required=True)
    email = mongoengine.fields.EmailField(required=False)


class Keyword(mongoengine.EmbeddedDocument):
    """
    Represents keywords of an article.

    Attributes:
        - text (str): The text of the keyword.
        - rank (str): A rank to represent how well a keyword is present in the article.
        - count (str): Number of occurences in the keyword.

    Example:
        author = Author(name="John Doe", email="john.doe@example.com")
    """
    text = mongoengine.fields.StringField(max_length=2000, required=True)
    rank = mongoengine.fields.DecimalField(
        required=False, precision=20, rounding='ROUND_HALF_UP')
    count = mongoengine.fields.IntField(required=False)



class Article(mongoengine.Document):
    """
    Represents an article with metadata.

    Attributes:
        - title (str): The title of the article.
        - url (str): The URL of the article.
        - source (str, optional): The source URL of the article.
        - top_image (str, optional): The URL of the top image associated with the article.
        - authors (list of Author, optional): List of authors contributing to the article.
        - categories (list of str, optional): List of categories associated with the article.
        - summary (str, optional): A summary of the article.
        - word_count (int, optional): The word count of the article.
        - read_time_in_minutes (float, optional): The estimated reading time in minutes.
        - publish_date (datetime, optional): The publish date of the article.
        - created_at (datetime): The timestamp when the article document was created.
        - updated_at (datetime): The timestamp when the article document was last updated.

    Example:
        article = Article(title="Sample Article", url="https://example.com/sample",
                        authors=[Author(name="John Doe")], categories=["Technology"],
                        summary="A brief summary of the article.", word_count=500,
                        read_time_in_minutes=25, publish_date=datetime.datetime.utcnow())
    """
    _id = mongoengine.fields.ObjectIdField()
    title = mongoengine.fields.StringField(max_length=512, required=True)
    url = mongoengine.fields.URLField(max_length=2000, required=True)
    source = mongoengine.fields.URLField(max_length=2000, required=False)
    top_image = mongoengine.fields.URLField(max_length=2000, required=False)
    authors = mongoengine.fields.ListField(
        mongoengine.fields.EmbeddedDocumentField(Author), required=False)
    keywords = mongoengine.fields.ListField(
        mongoengine.fields.EmbeddedDocumentField(Keyword), required=False)
    categories = mongoengine.fields.ListField(
        mongoengine.fields.StringField(), required=False)
    summary = mongoengine.fields.StringField(required=False)
    word_count = mongoengine.fields.IntField(required=False)
    read_time_in_minutes = mongoengine.fields.DecimalField(required=False)
    publish_date = mongoengine.fields.DateTimeField(required=False)
    created_at = mongoengine.fields.DateTimeField(
        default=datetime.datetime.utcnow)
    updated_at = mongoengine.fields.DateTimeField(
        default=datetime.datetime.utcnow)