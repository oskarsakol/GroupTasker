from django.contrib.auth.models import User, Group
from django.db import models


class Task(models.Model):
    creator = models.CharField(max_length=20)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # groups = models.OneToOneField(Group, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    description = models.TextField(max_length=200)
    completed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s" % self.name
