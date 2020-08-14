from django.shortcuts import render

from . import models
from django.db.models import Count
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView



# Create your views here.
'''
class ContextMixin:
    """
    Provides common context variables for blog views
    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['authors'] = models.Post.objects.published() \
            .get_authors() \
            .order_by('first_name')

        context['topics'] = models.Topic.objects.all()
        context['topics_count'] = models.Topic.objects.annotate(Count('blog_posts'))

        return context
'''

class HomeView(TemplateView):
    template_name = 'blog/home.html'

    def get_context_data(self, **kwargs):
        # Get the parent context
        context = super().get_context_data(**kwargs)
        latest_posts = models.Post.objects.published() \
            .order_by('-published')[:3]

        context.update({'latest_posts': latest_posts})
        return context


class AboutView(TemplateView):
    template_name = 'blog/about.html'
#class AboutView(View):
#    def get(self, request):
#        return render(request, 'blog/about.html')

def terms_and_conditions(request):
   return render(request, 'blog/terms_and_conditions.html')
"""
def home(request):
    #The Blog homepage
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
"""
class TopicListView(ListView):
    model = models.Topic
    context_object_name = 'topics'
    queryset = models.Topic.objects.all()  # Customized queryset


class PostListView(ListView):
    model = models.Post
    context_object_name = 'posts'
    queryset = models.Post.objects.published().order_by('-published')  # Customized queryset

class PostDetailView(DetailView):
    model = models.Post

    def get_queryset(self):
        queryset = super().get_queryset().published()

        # If this is a `pk` lookup, use default queryset
        if 'pk' in self.kwargs:
            return queryset

        # Otherwise, filter on the published date
        return queryset.filter(
            published__year=self.kwargs['year'],
            published__month=self.kwargs['month'],
            published__day=self.kwargs['day'],
        )
