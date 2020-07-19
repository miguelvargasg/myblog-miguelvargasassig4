from django.conf import settings
from django.db import models

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='blog_posts',
        null=True
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created']
