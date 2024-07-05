from django.contrib import admin
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter

from news_bot.settings import EMPTY_ADMIN_VALUE
from news_parsing.models import Parsing


@admin.register(Parsing)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('last_start', 'last_end', 'last_log_renewal')
    readonly_fields = ('last_start', 'last_end', 'last_log_renewal')
    empty_value_display = EMPTY_ADMIN_VALUE
    list_filter = (
        ('last_start', DateTimeRangeFilter),
        ('last_end', DateTimeRangeFilter),
        ('last_log_renewal', DateRangeFilter),
    )
    search_fields = ('last_start', 'last_end', 'last_log_renewal')

    def has_delete_permission(self, request, obj=None):
        if not obj or obj.id != Parsing.objects.latest('id'):
            return True
        return False
