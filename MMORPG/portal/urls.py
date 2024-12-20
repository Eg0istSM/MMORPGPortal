from django.urls import path
from .views import *


urlpatterns = [
    path('confirm/', ConfirmUser.as_view(), name='confirm_user'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('announcements/', AnnouncementsList.as_view(), name='announcements'),
    path('announcement/create/', AnnouncementCreate.as_view(), name='announcementcreate'),

]
