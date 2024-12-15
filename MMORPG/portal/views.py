from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import *


class AnnouncementsList(ListView):
    model = Announcement
    ordering = '-time_public'
    context_object_name = 'announcements'


class AnnouncementDetail(DetailView):
    model = Announcement
    template_name = 'announcement.html'
    context_object_name = 'announcement'


class AnnouncementCreate(PermissionRequiredMixin, CreateView):
    form_class = AnnouncementForm
    model = Announcement
    template_name = 'announcement_create.html'
    permission_required = ('news.add_post',)


class AnnouncementUpdate(PermissionRequiredMixin, UpdateView):
    form_class = AnnouncementForm
    model = Announcement
    template_name = 'announcement_create.html'
    permission_required = ('news.change_post',)









