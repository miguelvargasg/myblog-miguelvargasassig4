# blog/context_processors.py

from . import models
from django.db.models import Count


def base_context(request):
    authors = models.Post.objects.published() \
        .get_authors() \
        .order_by('first_name')
    topics = models.Topic.objects.all()
    topics_count = models.Topic.objects.annotate(Count('blog_posts'))

    return {'authors': authors,
            'topics': topics,
            'topics_count':topics_count,
        }
