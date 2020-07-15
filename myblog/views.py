# myblog/views.py

from django.http import HttpResponse


def index(request):
    return HttpResponse('Welcome to MyBlog! miguelvargasg Assignement 1...adding tester1/tester1')
