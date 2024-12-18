from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('confirm/', ConfirmUser.as_view(), name='confirm_user'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('announcement/', AnnouncementsList.as_view(), name='announcements'),
    path('login/', LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='account/logout.html'), name='logout'),



]
