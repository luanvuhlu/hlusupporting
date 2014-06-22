from django.contrib import admin
from datemanagement.models import Week, Holiday

class WeekAdmin(admin.ModelAdmin):
    ordering=('-semester', '-year', 'type', 'number', )
    list_display=('number', 'type_week', 'start', 'end', 'semester', 'year', )
    list_display_links=('number', 'type_week', 'start', 'end', 'semester', 'year', )
    radio_fields={'semester':admin.HORIZONTAL}
    def type_week(self, week):
        return week.get_type();
class HolidayAdmin(admin.ModelAdmin):
    list_display=('name', 'date', )
    list_display_links=('name', 'date', )
    ordering=('name', 'date', )
    pass
# Register your models here.
admin.site.register(Week, WeekAdmin)
admin.site.register(Holiday, HolidayAdmin)