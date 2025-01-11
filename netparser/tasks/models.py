from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


User = get_user_model()


class Task(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='tasks'
    )
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=128)

    class Meta:
        ordering = ('-created',)

    def get_absolute_url(self):
        return reverse('tasks:detail', args=[self.id,])
