from django_filters import FilterSet
from .models import Response, Announcement


# class ResponseFilter(FilterSet):
#     class Meta:
#         model = Response
#         fields = [
#             'announcement'
#         ]
#
#     def __init__(self, *args, **kwargs):
#         super(ResponseFilter, self).__init__(*args, **kwargs)
#         self.filters['announcement'].quryset = Announcement.objects.filter(user__user__User_id=kwargs['request'])
