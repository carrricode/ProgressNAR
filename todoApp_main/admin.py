from django.contrib import admin

# Register your models here.

from .models import Task, SubTask, Projects



admin.site.register(SubTask)
admin.site.register(Projects)


@admin.register(Task)
class TaskAdmin (admin.ModelAdmin):
    list_display = ['title', 'status','description']
    list_editable = ('status','description')
    search_fields = ['title']
    # prepopulated_fields = {'slug': ('title',)}