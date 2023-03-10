from django.db import models
from django.contrib.auth.models import User

class Tasks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} - {self.create}'

    class Meta:
        order_with_respect_to = 'user'
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

