from django.contrib import admin
from django.contrib.gis import forms

from .models import CategoryRole, Announcement
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class AnnouncementAdminForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Announcement
        fields = '__all__'


admin.site.register(CategoryRole)
admin.site.register(Announcement, AnnouncementAdminForm)
