from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from .filters import ResponseFilter
from .forms import AnnouncementForm, ResponseForm
from .models import *
from django.conf import settings


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = Response.objects.filter(announcement__author_id=self.request.user.id)
        context['filterset'] = ResponseFilter(self.request.GET, queryset, request_user_id=self.request.user.id)
        return context


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
        send_mail("Отклик на объявление!",
                  f"Здравствуйте,{comment.announcement.author.username}! На ваше объявление был оставлен отклик: {comment.text}",
                  from_email=settings.DEFAULT_FROM_EMAIL,
                  recipient_list=[comment.announcement.author.email],
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('announcement_detail', kwargs={'pk': self.kwargs['pk']})


def response_accept(request, pk):
    response = Response.objects.get(pk=pk)
    response.response_accept = True
    response.save()
    send_mail(
        'Принятие отклика',
        f'Ваш отклик {response.text} был принят автором объявления!',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[response.user.email],
    )
    return redirect('profile')


def response_delete(request, pk):
    response = Response.objects.get(pk=pk)
    response.delete()

    return redirect('profile')


class CategoryListView(ListView):
    model = Announcement
    template_name = 'portal/category_list.html'
    context_object_name = 'category_list'

    def get_queryset(self):
        self.category = get_object_or_404(CategoryRole, id=self.kwargs['pk'])
        queryset = Announcement.objects.filter(category=self.category).order_by('-time_public')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    category = CategoryRole.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы успешно подписались на рассылку категориии '
    return render(request, 'portal/subscribe.html', {'category': category, 'message': message})


@login_required
def unsubscribe(request, pk):
    user = request.user
    category = CategoryRole.objects.get(id=pk)
    category.subscribers.remove(user)

    message = 'Вы успешно отписались от рассылки '
    return render(request, 'portal/unsubscribe.html', {'category': category, 'message': message})


def categories(request):
    cat = CategoryRole.objects.all()
    return render(request, 'portal/categories.html', {'cat': cat})



