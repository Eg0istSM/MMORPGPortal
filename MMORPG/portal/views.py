from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import request
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from .filters import ResponseFilter
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
    # permission_required = ('portal.add_announcement',)


class AnnouncementUpdate(LoginRequiredMixin, UpdateView):
    form_class = AnnouncementForm
    model = Announcement
    template_name = 'portal/announcement_create.html'
    # permission_required = ('portal.change_post',)


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

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     queryset = Response.objects.filter(announcement__author__User_id=request.user.id)
    #     context['filterset'] = ResponseFilter(self.request.GET, queryset, request=self.request.user.id)


class AnnouncementResponse(LoginRequiredMixin, CreateView):
    form_class = ResponseForm
    model = Response
    template_name = 'portal/response.html'
    permission_required = ('news.add_post',)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.user = self.request.user
        comment.announcement = Announcement.objects.get(pk=self.kwargs['pk'])
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('announcement_detail', kwargs={'pk': self.kwargs['pk']})
