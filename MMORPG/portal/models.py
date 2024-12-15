from django.db import models
from django.contrib.auth.models import User


class Users(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class CategoryRole(models.Model):
    name = models.CharField(max_length=50, unique=True)
    subscribers = models.ManyToManyField(User, blank=True, null=True, related_name='categories')

    def __str__(self):
        return self.name.title()


class Announcement(models.Model):
    author = models.ForeignKey(Users, on_delete=models.CASCADE)
    text = models.TextField()
    title = models.CharField(max_length=250)
    content = models.FileField()
    category = models.ManyToManyField(CategoryRole, through='PostCategoryRole')
    time_public = models.DateTimeField(auto_now_add=True)


class AnnouncementCategory(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    category = models.ForeignKey(CategoryRole, on_delete=models.CASCADE)


class Response(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    time_response = models.DateTimeField(auto_now_add=True)

