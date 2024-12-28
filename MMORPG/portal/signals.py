from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.conf import settings
from .models import Announcement


def send_notifications(preview, pk, title, subscriber):
    html_content = render_to_string(
        'users/announcement_created_email.html',
        {
            'username': subscriber.username,
            'text': preview,
            'link': f'{settings.SITE_URL}/portal/announcement/{pk}',
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[subscriber.email],

    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@receiver(post_save, sender=Announcement)
def notify_about_new_post(sender, instance, created, **kwargs):
    if created:
        category_instance = instance.category
        subscribers_emails = []
        subscribers = category_instance.subscribers.all()
        for subscriber in subscribers:

            send_notifications(instance.preview(), instance.pk, instance.title, subscriber)





