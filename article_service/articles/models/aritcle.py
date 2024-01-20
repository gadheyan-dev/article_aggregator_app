from djongo import models
# import uuid


class Author(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=200)
    avatar = models.URLField(max_length=2000, blank=True)
    email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.DjongoManager()


class Article(models.Model):
    _id = models.ObjectIdField()
    title = models.CharField(max_length=512, null=False)
    url = models.URLField(max_length=2000, null=False)
    top_image = models.URLField(max_length=2000, null=True)
    description = models.TextField(null=True)
    authors = models.ArrayField(
        model_container=Author,
    )
    summary = models.TextField(null=True)
    publish_date = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.DjongoManager()

