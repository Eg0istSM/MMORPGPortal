from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse


class User(AbstractUser):
    code = models.CharField(max_length=15, blank=True, null=True)


class CategoryRole(models.Model):
    name = models.CharField(max_length=50, unique=True)
    subscribers = models.ManyToManyField(User, related_name='categories')

    def __str__(self):
        return f'{self.name.title()}'


class Announcement(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = RichTextUploadingField()
    title = models.CharField(max_length=250)
    category = models.ForeignKey(CategoryRole, on_delete=models.CASCADE)
    time_public = models.DateTimeField(auto_now_add=True)

    def preview(self):
        preview_text = self.text[0:30] + '...'
        return preview_text

    def __str__(self):
        return f'{self.title.title()}'

    def get_absolute_url(self):
        return reverse('announcement_detail', args=[str(self.id)])


class Response(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    time_response = models.DateTimeField(auto_now_add=True)
    response_accept = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} ({self.text[:30]}...)'


