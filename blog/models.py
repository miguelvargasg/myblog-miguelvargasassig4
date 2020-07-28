from django.conf import settings
from django.db import models
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth import get_user_model

# Create your models here.
class TopicQuerySet(models.QuerySet):
    def get_topics(self):
        return self.all()
        #Topic.objects.annotate(total_posts=Count('blog_posts')).values('name','total_posts')


class Topic(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True  # No duplicates!
    )
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

    objects = TopicQuerySet.as_manager()

class CommentQuerySet(models.QuerySet):
    def approved(self):
        return self.filter(approved=self.model.APPROVED)
    def notapproved(self):
        return self.filter(approved=self.model.NOTAPPROVED)


class PostQuerySet(models.QuerySet):
    def get_authors(self):
        User = get_user_model()
        return User.objects.filter(blog_posts__in=self).distinct()

    def published(self):
        return self.filter(status=self.model.PUBLISHED)

    def drafts(self):
        return self.filter(status=self.model.DRAFT)

    def find(self):
        expression = 'Hello'
        return self.filter(Q(title__icontains=expression) | Q(content__icontains=expression))



class Post(models.Model):

    title = models.CharField(max_length=255)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='blog_posts',
        null=False,
    )
    DRAFT = 'draft'
    PUBLISHED = 'published'
    STATUS_CHOICES = [
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published')
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=DRAFT,
        help_text='Set to "published" to make this post publicly visible',
    )


    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created']
    published = models.DateTimeField(
        null=True,
        blank=True,
        help_text='The date & time this article was published',
    )
    slug = models.SlugField(
        null=False,
        help_text='The date & time this article was published',
        unique_for_date='published',  # Slug is unique for publication date
    )
    topics = models.ManyToManyField(
        Topic,
        related_name='blog_posts'
    )

    def publish(self):
        """Publishes this post"""
        self.status = self.PUBLISHED
        self.published = timezone.now()  # The current datetime with timezone

    objects = PostQuerySet.as_manager()


class Comment(models.Model):
    """
    Represents a Blog Comment
    """
    #post = models.CharField(null=True, max_length=255,)
    post = models.ForeignKey(
        Post,  # The Django auth user model
        on_delete=models.PROTECT,  # Prevent posts from being deleted
        related_name='blogs_comments',  # "This" on the user model
        null=True
    )
    name = models.CharField(null=True, max_length=255,)
    email = models.CharField(null=True, max_length=255,)
    text = models.CharField(max_length=500)
    #approved = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # The Django auth user model
        on_delete=models.PROTECT,  # Prevent posts from being deleted
        related_name='blogs_comments',  # "This" on the user model
        null=True
    )


    def __str__(self):
        return self.text
    class Meta:
        ordering = ['-created']

    APPROVED = 'approved'
    NOTAPPROVED = 'notapproved'
    APPROVED_CHOICES = [
        (APPROVED, 'approved'),
        (NOTAPPROVED, 'notapproved')
    ]

    approved = models.CharField(
        max_length=20,
        choices=APPROVED_CHOICES,
        default=APPROVED,
        help_text='Set to "approved" to make this post publicly visible'
    )

    #approved = models.BooleanField()
    objects = CommentQuerySet.as_manager()
    #objects = CommentManager()
