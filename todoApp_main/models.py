import uuid
from django.contrib.auth.models import User
from django.db import models
from django.db.models import ManyToManyField




class Projects(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)

    admin = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='admin_projects',
    )

    users = ManyToManyField(
        User,
        related_name='user_projects',
        blank=True
    )


    tasks = ManyToManyField(
        'Task',
        related_name='user_projects',
        blank=True
    )



    def __str__(self):
        return f"{self.name} ({self.admin})"


class Task(models.Model):
    class Status(models.TextChoices):
        BACKLOG = 'backlog', 'Backlog'
        IN_PROGRESS = 'in_progress', 'In Progress'
        DONE = 'done', 'Done'
        EXPIRED = 'expired', 'Expired'

    class Priority(models.TextChoices):
        LOW = 'low', 'Low'
        MEDIUM = 'medium', 'Medium'
        HIGH = 'high', 'High'

    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True)
    id = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    title = models.CharField(max_length = 100)
    description = models.TextField(null = False,blank = True)
    responsible_user = models.ManyToManyField(  # Изменил название поля
        User,
        blank=True,
        related_name='responsible_users',
    )





    status = models.CharField(
        max_length = 20,
        choices = Status.choices,
        default = Status.BACKLOG
    )

    priority = models.CharField(
        max_length = 20,
        choices = Priority.choices,
        default = Priority.MEDIUM
    )

    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f"{self.title} ({self.status})"

    class Meta:
        ordering = ['-updated_at']


class SubTask(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    parent_task = models.ForeignKey(Task, on_delete= models.CASCADE, related_name='subtasks')
    title = models.CharField(max_length=100)
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"


