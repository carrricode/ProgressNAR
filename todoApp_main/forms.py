from django.forms import ModelForm
from .models import Task,Projects
from django.contrib.auth.models import User
from django import forms


class TaskForm(ModelForm):
    # responsible_user = forms.ModelChoiceField(
    #     queryset=User.objects.none(),  # Изначально пустой queryset
    #     required=False,  # Сделать необязательным, если задача может быть без ответственного
    #     label='Responsible User'
    # )


    class Meta:
        model = Task
        fields = '__all__'
        exclude = ['user']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    # def __init__(self, *args, **kwargs):
    #     project = kwargs.pop('project', None)  # Получаем объект проекта из kwargs
    #     super().__init__(*args, **kwargs)
    #
    #     if project:
    #         # Получаем всех пользователей, которые являются участниками этого проекта
    #         # Это включает admin и users (Many-to-Many)
    #         project_users = User.objects.filter(
    #             id__in=project.users.all().values_list('id', flat=True)
    #         ) | User.objects.filter(id=project.admin.id)
    #         self.fields['responsible_user'].queryset = project_users.distinct().order_by('username')


class ProjectsForm(ModelForm):
    class Meta:
        model = Projects
        fields = '__all__'
        exclude =['admin','tasks']