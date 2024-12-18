from django import forms
from django.core.mail import send_mail
from django.conf import settings
from .models import Announcement, Response
from allauth.account.forms import SignupForm
import random
from string import hexdigits


class AnnouncementForm(forms.ModelForm):
    class Meta:
        mode = Announcement
        fields = [
            'author',
            'title',
            'text',
            'category',
        ]


class ResponseForm(forms.ModelForm):

    class Meta:
        model = Response
        fields = ['text']


class CommonSignupForm(SignupForm):
    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        user.is_active = False
        code = ''.join(random.sample(hexdigits, 5))
        user.code = code
        user.save()
        send_mail(
            subject=f'Код активации',
            message=f'Код активации аккунта {code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
        return user
