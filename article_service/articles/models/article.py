from djongo import models
# import uuid


class Article(models.Model):
    _id = models.ObjectIdField()
    title = models.CharField(max_length=512, null=False)
    url = models.URLField(max_length=2000, null=False)
    top_image = models.URLField(max_length=2000, null=True)
    description = models.TextField(null=True)
    authors = models.JSONField() 
    summary = models.TextField(null=True)
    publish_date = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.DjongoManager()

