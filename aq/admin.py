from django.contrib import admin
from aq.models import Answer, Question, Tag
# Register your models here.
admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(Tag)