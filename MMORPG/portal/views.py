from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView

from .forms import AnnouncementForm, ResponseForm
from .models import *


class AnnouncementsList(ListView):
    model = Announcement
    ordering = '-time_public'
    context_object_name = 'announcements'
    template_name = 'portal/announcements.html'


class AnnouncementDetail(DetailView):
    model = Announcement
    template_name = 'portal/announcement.html'
    context_object_name = 'announcement'


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


class AnnouncementResponse(LoginRequiredMixin, CreateView):
    form_class = ResponseForm
    model = Response
    template_name = 'portal/response.html'
    permission_required = ('news.add_post',)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.user = self.request.user
        comment.post = Announcement.objects.get(pk=self.kwargs['pk'])
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.kwargs['pk']})
