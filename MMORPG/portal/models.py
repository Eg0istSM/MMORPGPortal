from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    code = models.CharField(max_length=15, blank=True, null=True)


class CategoryRole(models.Model):
    name = models.CharField(max_length=50, unique=True)
    subscribers = models.ManyToManyField(User, blank=True, null=True, related_name='categories')

    def __str__(self):
        return self.name.title()


class Announcement(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    title = models.CharField(max_length=250)
    category = models.ManyToManyField(CategoryRole, through='AnnouncementCategory')
    time_public = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title.title()}: {self.text[:20]}'


class AnnouncementCategory(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    category = models.ForeignKey(CategoryRole, on_delete=models.CASCADE)


class Response(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    time_response = models.DateTimeField(auto_now_add=True)
    response_accept = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} ({self.text[:30]}...)'


