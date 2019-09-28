from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from taggit.managers import TaggableManager

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ArticlePost(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = TaggableManager(blank=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title

