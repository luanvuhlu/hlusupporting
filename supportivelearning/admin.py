from django.contrib import admin
from supportivelearning.models import Student, Day, Faculity, Year, TimeTableSubject, TimeTable, SubjectStudentYear, Subject, StudentYear, FaculitySubject, Notification

class StudentAdmin(admin.ModelAdmin):
    list_display=('code', 'first_name', 'last_name', 'student_year', )
    list_display_links=('code','first_name', 'last_name',)
    search_fields=['code']
    def first_name(self, student):
        return student.user.first_name;
    def last_name(self, student):
        return student.user.last_name;
    
class DayAdmin(admin.ModelAdmin):
    list_display=('student', 'subject', 'week_day', 'type', 'number',)
    list_display_links=('student', 'subject', 'week_day', 'type', 'number', )
    radio_fields={'location':admin.HORIZONTAL, 'number':admin.HORIZONTAL}
    def student(self, day):
        return day.timetable_subject.timetable.student
    def subject(self, day):
        return day.timetable_subject.subject.subject.alias
class FaculityAdmin(admin.ModelAdmin):
    list_display=('first_name', 'last_name', )
    list_display_links=('first_name', 'last_name', )
# class MessageAdmin(admin.ModelAdmin):
#     list_display=('content', 'type', 'actived', )
#     list_display_links=('content', 'type', 'actived', )
#     radio_fields={'type':admin.HORIZONTAL}
class YearAdmin(admin.ModelAdmin):
    pass
class TimeTableSubjectAdmin(admin.ModelAdmin):
    list_display=('timetable', 'subject', )
    list_display_links=('timetable', 'subject', )
class TimeTableAdmin(admin.ModelAdmin):
    list_display=('student', 'semester' ,'year', 'created_time', )
    list_display_links=('student', 'semester' , 'year', 'created_time', )
    radio_fields={'semester':admin.HORIZONTAL}
class SubjectStudentYearAdmin(admin.ModelAdmin):
    ordering=('subject', 'student_year', )
    list_display=('subject', 'student_year' ,'week_number', )
    list_display_links=('subject', 'student_year' ,'week_number', )
    radio_fields={'week_number':admin.HORIZONTAL}
class SubjectAdmin(admin.ModelAdmin):
    ordering=('alias', 'name', )
    list_display=('alias', 'name', )
    list_display_links=('alias', 'name', )
class StudentYearAdmin(admin.ModelAdmin):
    list_display=('name', 'student_sum',)
    list_display_links=('name', 'student_sum', )
    def student_sum(self, studentyear):
        return len(Student.objects.filter(student_year=studentyear.id))     
class FaculitySubjectAdmin(admin.ModelAdmin):
    ordering=('-subject', )
    list_display=('subject', 'faculity', )
    list_display_links=('subject', 'faculity', )
class NotificationAdmin(admin.ModelAdmin):
    pass
# Register your models here.
admin.site.register(Student, StudentAdmin)
admin.site.register(Day, DayAdmin)
admin.site.register(Faculity, FaculityAdmin)
# admin.site.register(Message, MessageAdmin)
admin.site.register(Year, YearAdmin)
admin.site.register(TimeTableSubject, TimeTableSubjectAdmin)
admin.site.register(SubjectStudentYear, SubjectStudentYearAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(StudentYear, StudentYearAdmin)
admin.site.register(TimeTable, TimeTableAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(FaculitySubject, FaculitySubjectAdmin)