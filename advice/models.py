from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

class Question(models.Model):
    title = models.CharField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_published = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("question_detail", kwargs={'pk': self.pk})

class Advice(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    date_published = models.DateTimeField(default=timezone.now)       

    def __str__(self):
        return f"Advice by {self.author.username}"