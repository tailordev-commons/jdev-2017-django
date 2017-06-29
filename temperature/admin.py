from django.contrib import admin

from .models import Country, Record


class RecordAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = ('country', 'date', 'temperature', 'uncertainty')
    list_filter = ('country', )


admin.site.register(Country)
admin.site.register(Record, RecordAdmin)
