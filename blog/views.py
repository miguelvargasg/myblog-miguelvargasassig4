from django.shortcuts import render

from . import models
from django.db.models import Count


# Create your views here.

def home(request):
    """
    The Blog homepage
    """
    latest_posts = models.Post.objects.all()
    authors = models.Post.objects.get_authors()
    #topics = models.Post.objects.get_topics()
    topics = models.Topic.objects.all()
    topics_count = models.Topic.objects.annotate(Count('blog_posts'))


    context = {
        'authors': authors,
        'latest_posts': latest_posts,
        'topics': topics,
        'topics_count':topics_count,
        
    }
    return render(request, 'blog/home.html', context)
