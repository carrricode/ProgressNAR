from django.contrib import admin

# Register your models here.

from .models import Task, SubTask, Projects

admin.site.register(Task)
admin.site.register(SubTask)
admin.site.register(Projects)