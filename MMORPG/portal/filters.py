from django_filters import FilterSet
from .models import Response, Announcement


class ResponseFilter(FilterSet):
    class Meta:
        model = Response
        fields = [
            'announcement'
        ]

    def __init__(self, *args, request_user_id=None, **kwargs):
        self.request_user_id = request_user_id
        super(ResponseFilter, self).__init__(*args, **kwargs)
        self.filters['announcement'].queryset = Announcement.objects.filter(author_id=self.request_user_id)
