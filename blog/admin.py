from django.contrib import admin
from . import models
# Register your models here.

class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'post',
        'name',
        'email',
        'text',
        'approved',
        'created',
        'updated',
        'author',
    )
    search_fields = (
        'text',
        'name',
        'email',
    )
    list_filter = (
        'approved',
    )
admin.site.register(models.Comment, CommentAdmin)

@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'created',
        'updated',
        'author',
    )

    search_fields = [
        'title',
        'author__username',
        'author__first_name',
        'author__last_name',
    ]
    list_filter = (
        'status',
        'topics'
    )
    prepopulated_fields = {'slug': ('title',)}



@admin.register(models.Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    prepopulated_fields = {'slug': ('name',)}
