from django import forms
from .models import Announcement, Response


class AnnouncementForm(forms.ModelForm):
    class Meta:
        mode = Announcement
        fields = [
            'author',
            'title',
            'text',
            'image',
            'content',
            'category',
        ]


class ResponseForm(forms.ModelForm):

    class Meta:
        model = Response
        fields = ['text']
