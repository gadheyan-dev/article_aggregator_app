from djongo import models

class Domain(models.Model):
    _id = models.ObjectIdField()
    url = models.URLField(max_length=2000, null=False)
    last_crawled_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.DjongoManager()