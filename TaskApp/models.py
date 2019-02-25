from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

from django.db import models

User = get_user_model()


class Task(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks')
    completed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return f'{self.name}'


class Comment(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    description = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='assigned_comment')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.description}'

