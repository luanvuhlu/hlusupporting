from django.contrib import admin
from document.models import Day, DocumentLearning, HomeWork, Week, Document
# Create your models here.

class DocumentLearningAdmin(admin.ModelAdmin):
    list_display = ('subject', 'type', 'name', )

    def subject(self, obj):
        return obj.document.subject


class DocumentAdmin(admin.ModelAdmin):
    pass


class WeekAdmin(admin.ModelAdmin):
    list_display = ('subject', 'number', 'note', )

    def subject(self, obj):
        return obj.document.subject


class DayAdmin(admin.ModelAdmin):
    list_display = ('subject', 'week', 'type', 'number',)

    def subject(self, obj):
        return obj.week.document.subject


class HomeWorkAdmin(admin.ModelAdmin):
    list_display = ('subject', 'type', 'require', 'pages', )

    def subject(self, obj):
        return obj.document.subject

# Register your models here.
admin.site.register(Document, DocumentAdmin)
admin.site.register(DocumentLearning, DocumentLearningAdmin)
admin.site.register(Week, WeekAdmin)
admin.site.register(Day, DayAdmin)
admin.site.register(HomeWork, HomeWorkAdmin)