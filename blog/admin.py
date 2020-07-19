from django.contrib import admin
from . import models
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
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
    )

#admin.site.register(models.Post, PostAdmin)
