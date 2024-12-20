from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView

from .forms import AnnouncementForm
from .models import *


class AnnouncementsList(ListView):
    model = Announcement
    ordering = '-time_public'
    context_object_name = 'announcements'
    template_name = 'portal/announcements.html'


# class AnnouncementDetail(DetailView):
#     model = Announcement
#     template_name = 'portal/announcements.html'
#     context_object_name = 'announcement'


class AnnouncementCreate(LoginRequiredMixin, CreateView):
    form_class = AnnouncementForm
    model = Announcement
    template_name = 'portal/announcement_create.html'
    permission_required = ('portal.add_post',)


class AnnouncementUpdate(LoginRequiredMixin, UpdateView):
    form_class = AnnouncementForm
    model = Announcement
    template_name = 'portal/announcement_create.html'
    permission_required = ('portal.change_post',)


class ConfirmUser(UpdateView):
    model = User
    context_object_name = 'confirm_user'

    def post(self, request, *args, **kwargs):
        if 'code' in request.POST:
            user = User.objects.filter(code=request.POST['code'])
            if user.exists():
                user.update(is_active=True)
                user.update(code=None)
            else:
                return render(self.request, 'users/invalid_code.html')
        return redirect('account_login')


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'


# class AnnouncementUserResponse(LoginRequiredMixin,ListView):
#     model = Response
#     template_name = 'announcement_user_response.html'
#     context_object_name = 'response'
#
#     def get_context_data(self, **kwargs):
#         queryset =
