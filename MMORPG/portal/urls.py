from django.urls import path
from .views import *


urlpatterns = [
    path('confirm/', ConfirmUser.as_view(), name='confirm_user'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('announcements/', AnnouncementsList.as_view(), name='announcements'),
    path('announcement/create/', AnnouncementCreate.as_view(), name='announcementcreate'),
    path('announcement/<int:pk>/', AnnouncementDetail.as_view(), name='announcement_detail'),
    path('announcement/<int:pk>/edit/', AnnouncementUpdate.as_view(), name='announcement_update'),
    path('<int:pk>/response/', AnnouncementResponse.as_view(), name='announcement_response'),
    path('<int:pk>/response_accept/', response_accept, name='response_accept'),
    path('<int:pk>/response_delete/', respons_delete, name='respons_delete'),



]
