from django.views.generic.list import ListView

from .models import Record


class RecordListView(ListView):

    model = Record
    paginate_by = 50
