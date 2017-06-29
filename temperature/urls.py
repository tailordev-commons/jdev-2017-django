from django.conf.urls import url

from .views import RecordListView

urlpatterns = [
    url(r'^$', RecordListView.as_view(), name='record_list'),
]
