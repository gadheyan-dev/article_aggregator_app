from django.db import models
import uuid


class Author(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    avatar = models.URLField(max_length=2000, blank=True)
    email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Article(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=512, null=False)
    url = models.URLField(max_length=2000, null=False)
    top_image = models.URLField(max_length=2000, null=True)
    description = models.TextField(null=True)
    authors = models.ManyToManyField(Author)
    summary = models.TextField(null=True)
    publish_date = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

