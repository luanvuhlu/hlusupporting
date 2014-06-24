from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from supportivelearning.views import index, login_view, logout_view, \
    timetable_detail, \
    quick_timetable, file_upload_view, \
    import_next, import_final, settings_view, profile_view
from document.views import subject_student_view
from datemanagement.views import import_week_view, save_import_week
from document.views import import_week_document, get_subject_student_year_detail, save_week_document_import
admin.autodiscover()
from notification.views import notification_count, notification_view

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hlusupporting.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', index, name='home'),
    url(r'^login/$', login_view),
    url(r'^logout/$', logout_view),
    url(r'^profile/$', profile_view),
    # url(r'^timetable/list/$', timetable_list_view),
    url(r'^timetable/(?P<id>\d+)/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', timetable_detail),
    url(r'^tt/$', quick_timetable),
    url(r'^subject/(?P<slug>(([0-9a-z-]+)\.html))/$', subject_student_view),
    url(r'^import/upload/$', file_upload_view),
    url(r'^import/next/$', import_next),
    url(r'^import/final/$', import_final),
    url(r'^import/week/$', import_week_view),
    url(r'^import/week/save/$', save_import_week),
    url(r'^import/week/document/$', import_week_document),
    url(r'^import/week/document/loadsubject/(?P<subject_name>.+)/(?P<student_year>.+)/(?P<year>.+)/$',
        get_subject_student_year_detail),
    url(r'^import/week/document/save/$', save_week_document_import),
    url(r'^settings/$', settings_view),
    url(r'^notification_count/$', notification_count),
    url(r'^notification_view/$', notification_view),

)
urlpatterns += staticfiles_urlpatterns()
