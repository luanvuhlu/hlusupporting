import sys
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login, logout
from supportivelearning.models import Student, TimeTable, TimeTableSubject, Day, SubjectStudentYear, Year
from document.models import Day as Day_Document
from document.models import Week as Week_Document
from document.models import Document
from datemanagement.models import Week as Week_Date
from datetime import date, timedelta, datetime
from django.http.response import Http404
from slugify import slugify
import re
from supportivelearning.forms import TimeTableUploadForm
from supportivelearning.data import TimeTableFile
import json
import logging

URL_SESSION = "url_previous_session"
APP_NAME = 'supportivelearning'
TIMETABLE_DATA_SESSION = "subject_data"


def index(request):
    template = loader.get_template(APP_NAME + "/index.html")
    context = RequestContext(
        request,
    )
    # time=datetime.today().strftime("%Y/%m/%d/")
    #     return HttpResponseRedirect("/timtetable/"+time)
    return HttpResponse(template.render(context))


# Login
def login_view(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/")
    errors = []
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if request.session.get(URL_SESSION):
                    return HttpResponseRedirect(request.session[URL_SESSION])
                return HttpResponseRedirect("/")
            else:
                errors.append("User is blocked !")
        else:
            errors.append("Your username and password didn't match. Please try again")
    template = loader.get_template(APP_NAME + "/login.html")
    context = RequestContext(
        request,
        {"errors": errors, }
    )
    return HttpResponse(template.render(context))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")


# End Login
# Timetable #
# def timetable_list_view(request):
#     if not request.user.is_authenticated():
#         save_url(request)
#         return HttpResponseRedirect("/login/")
#     timetables = TimeTable.objects.filter(student__user=request.user)
#     template = APP_NAME + '/timetable_list.html'
#     context = RequestContext(
#         request,
#         {'timetables': timetables}
#     )
#
#     return render_to_response(template, context)


def get_table_timetable(days, days_week, select_day):
    # check if user don't want view day follow document
    # day unfollow document
    # days_week=days
    # end
    today = date.today()
    start_week = select_day - timedelta(days=select_day.weekday())
    end_week = start_week + timedelta(days=5)
    table = []
    tr = []
    rowspans = []
    rowspan = {'tr': -1, 'td': -1}
    for hour_count in range(1, 16):
        for day_count in range(1, 7):
            td = {'value': '', 'slug': '', 'rowspan': 0, 'class': ''}
            for day_week in days_week:
                # day follow document
                day = day_week['day']
                # end
                # day unfollow document
                #                 day=day_week
                # end
                if day.week_day == day_count and day.start_hour == hour_count:
                    td['day'] = day
                    td['slug'] = slugify(
                        day.timetable_subject.subject.subject.name + " " + day.timetable_subject.subject.student_year.name)
                    if day.type == False:
                        td['class'] += td['class'] + ' theory_hour' + ' bg-success'
                    else:
                        td['class'] += td['class'] + ' seminar_hour' + ' bg-danger'
                    if today >= start_week and today <= end_week and today.weekday() == day_count - 1:
                        td['class'] += ' today'
                        # day follow document
                    if day_week['content']:
                        td['content'] = day_week['content'].split("\n")
                    if day_week['note']:
                        td['note'] = day_week['note'].split("\n")
                    # end
                    td['rowspan'] = day.end_hour - day.start_hour + 1
                    for i in range(1, td['rowspan']):
                        rowspan['tr'] = hour_count + i
                        rowspan['td'] = day_count
                        rowspans.append(rowspan)
                        rowspan = {'tr': -1, 'td': -1}
            cell = {'tr': hour_count, 'td': day_count}
            if cell not in rowspans:
                tr.append(td)
        table.append(tr)
        tr = []
    return table


def get_week_detail(days, select_day):
    days_week_detail = []
    week_infos = []
    start_week = select_day - timedelta(days=select_day.weekday())
    # end_week = start_week + timedelta(days = 5)
    prev_subject = ''
    for day in days:
        #         try:
        if day.timetable_subject.start > start_week or day.timetable_subject.end < start_week:
            continue
        if day.timetable_subject.subject.week_number == 5:
            type_subject = True  # 5 weeks
        else:
            type_subject = False  # than 5 weeks
        try:
            week_date = Week_Date.objects.get(start=start_week, type=type_subject,
                                              student_year=day.timetable_subject.subject.student_year)
        except Week_Date.DoesNotExist:
            print "Week Date does not exist"
            continue
        try:
            document = Document.objects.get(subject=day.timetable_subject.subject)
        except Document.DoesNotExist:
            print "Document does not exist"
            continue
        try:
            week_document = Week_Document.objects.get(document=document, number=week_date.number)
            subject = document.subject.subject.alias
            if prev_subject != subject and (week_document.note or week_document.require):
                prev_subject = subject
                week_infos.append({'subject': subject, 'note': week_document.note, 'require': week_document.require})
            days_document = Day_Document.objects.filter(week=week_document)
            for day_document in days_document:
                if day_document.type == day.type and day_document.number == day.number:
                    days_week_detail.append({'day': day, 'content': day_document.content, 'note': day_document.note})
        except Week_Document.DoesNotExist:
            print "Week Document does not exist"
            #         except:
            #             continue
    week_detail = {'week_infos': week_infos, 'days': days_week_detail}
    return week_detail


def timetable_detail(request, id, year, month, day):
    if not request.user.is_authenticated():
        save_url(request)
        return HttpResponseRedirect("/login/")
    timetable_subjects = TimeTableSubject.objects.filter(timetable=id)
    days = Day.objects.filter(timetable_subject=timetable_subjects)
    # try:
    select_day = date(year=int(year), month=int(month), day=int(day))
    #     except:
    #         return HttpResponse("Day is not valid")
    template = APP_NAME + "/timetable.html"
    if timetable_subjects:
        week_detail = get_week_detail(days, select_day)
        table = get_table_timetable(days, week_detail['days'], select_day)
    else:
        context = RequestContext(
            request,
        )
        return render_to_response(template, context)
    start = select_day - timedelta(days=select_day.weekday())
    end = start + timedelta(days=6)
    next = end + timedelta(days=1)
    prev = start - timedelta(days=1)
    days_in_week = []
    delta = timedelta(days=1)
    while start <= end:
        days_in_week.append({'date': start, 'name': start.strftime('%A')})
        start += delta
    context = RequestContext(
        request,
        {
            'table': table,
            'week_infos': week_detail['week_infos'],
            'days_in_week': days_in_week,
            'next': next,
            'prev': prev,
            'timetable_id': id,
        }
    )
    return render_to_response(template, context)


def quick_timetable(request):
    time = datetime.today().strftime("%Y/%m/%d/")
    if not request.user.is_authenticated():
        save_url(request)
        return HttpResponseRedirect("/login/")
    try:
        timetable = TimeTable.objects.filter(student__user=request.user)[0]
        id = str(timetable.id)
    except:
        return HttpResponse("You don't have timetable")
    return HttpResponseRedirect('/timetable/' + id + '/' + time)


# End Timetable #
def save_url(request):
    request.session[URL_SESSION] = request.path


# Upload TimeTable
def file_upload_view(request):
    template = APP_NAME + '/fileupload.html'
    if request.method == 'POST':
        form = TimeTableUploadForm(request.POST, request.FILES)
        if form.is_valid():
            timetable = TimeTableFile(request.FILES['file'].read())
            if timetable.subjects:
                template = APP_NAME + "/fileupload.html"
                request.session[TIMETABLE_DATA_SESSION] = json.dumps(timetable.subjects)
                alerts = []
                try:
                    student = Student.objects.get(user=request.user)
                except Student.DoesNotExist:
                    print "Student does not exist"
                    request.session[TIMETABLE_DATA_SESSION] = ''
                    # save_url(request)
                    # return HttpResponseRedirect("/login/")
                #
                if False and timetable.student_code != student.code:  # Check student code and student code in file
                    request.session[TIMETABLE_DATA_SESSION] = ""
                    form = TimeTableUploadForm()
                    print "Timetable code " + timetable.student_code
                    print "Student code " + student.code
                    alerts.append("Code in timetable not compair your code ! Please try again !")
                    context = RequestContext(
                        request,
                        {
                            'timetable': timetable,
                            'form': form,
                            'alerts': alerts,
                        }
                    )
                    return render_to_response(template, context)
                else:
                    return HttpResponseRedirect("/import/next/")
            else:
                return HttpResponse("Cannot find subjects")
    else:
        form = TimeTableUploadForm()
    return render_to_response(template,
                              {'form': form},
                              context_instance=RequestContext(request)
    )


def import_next(request):
    template = APP_NAME + '/upload_next.html'
    subjects_timetable = json.loads(request.session.get(TIMETABLE_DATA_SESSION))
    if subjects_timetable:
        all_subjects_select = []
        for sub in subjects_timetable:
            subjects = SubjectStudentYear.objects.filter(subject__name=sub['name'])
            select = {}
            select['name'] = sub['name']
            if subjects:
                options = []
                for s in subjects:
                    options.append(s.student_year.name)
                select['options'] = options
            all_subjects_select.append(select)
        years = Year.objects.all()
        year_now = date.today().year
    context = RequestContext(
        request,
        {
            'all_subjects_select': all_subjects_select,
            'years': years,
        }
    )
    return render_to_response(template, context)


def import_final(request):
    subjects = request.GET.getlist('subject')
    student_years = request.GET.getlist('student-year')
    subjects_timetable = json.loads(request.session.get(TIMETABLE_DATA_SESSION))
    student = Student.objects.get(user=request.user)
    # try:
    try:
        timetable = TimeTable.objects.filter(student=student, semester=1, year=1)[0]
    except:
        print "Not match timetable"
        timetable = TimeTable()
        timetable.student = student
        timetable.semester = 1
        timetable.year = Year.objects.get(id=1)
        timetable.save()

    if subjects:
        for i in range(len(subjects)):
            try:
                subject_year = SubjectStudentYear.objects.get(subject__name=subjects[i],
                                                              student_year__name=student_years[i])
            except:
                logging.error("SubjectStudentYear does not exist")
                continue
            for sub in subjects_timetable:
                try:
                    if sub['name'] == subjects[i]:
                        try:
                            subject_timetable = \
                            TimeTableSubject.objects.filter(subject=subject_year, timetable=timetable)[0]
                        except:
                            subject_timetable = TimeTableSubject()
                        subject_timetable.subject = subject_year
                        subject_timetable.timetable = timetable
                        # try:
                        start = datetime.strptime(sub['start'], '%d/%m/%Y')
                        end = datetime.strptime(sub['end'], '%d/%m/%Y:')
                        # except:
                        #                             start=datetime.today()
                        #                             end=datetime.today()
                        subject_timetable.start = start
                        subject_timetable.end = end
                        subject_timetable.save()
                        #                         try:
                        days = Day.objects.filter(timetable_subject=subject_timetable)
                        for day in days:
                            day.delete()
                            #                         except:
                            # print "Do not have day"
                        for i in range(len(sub['day_theories'])):
                            data = sub['day_theories'][i]
                            day = Day()
                            day.timetable_subject = subject_timetable
                            day.type = False  # Theory
                            day.start_hour = int(data['start'])
                            day.end_hour = int(data['end'])
                            day.location = data['location']
                            day.room = data['room']
                            # day.week_day=int(data['week_day'])
                            day.week_day = int(data['week_day']) - 1  # Day of week not match
                            day.number = i + 1
                            day.save()
                        for i in range(len(sub['day_seminars'])):
                            data = sub['day_seminars'][i]
                            day = Day()
                            day.timetable_subject = subject_timetable
                            day.type = True  # Seminar
                            day.start_hour = int(data['start'])
                            day.end_hour = int(data['end'])
                            day.location = data['location']
                            day.room = data['room']
                            day.number = i + 1
                            # if data['week_day']:
                            day.week_day = int(data['week_day']) - 1  #Day of week not match
                            day.save()
                            # else:
                            # print "Week day is None"
                except:
                    continue
    # except:
    # print sys.exc_info()[0]
    # request.session[TIMETABLE_DATA_SESSION]=None
    #     return HttpResponseRedirect("/import/upload/")
    request.session[TIMETABLE_DATA_SESSION] = None
    today = datetime.today()
    return HttpResponseRedirect(
        "/timetable/" + str(timetable.id) + "/" + str(today.year) + "/" + str(today.month) + "/" + str(today.day) + "/")


# End upload TimeTable
# Settings view
def settings_view(request):
    template = loader.get_template(APP_NAME + "/settings.html")
    context = RequestContext(
        request,
    )
    return HttpResponse(template.render(context))


# End Settings view
# Profile view
def profile_view(request):
    if not request.user.is_authenticated():
        save_url(request)
        return HttpResponseRedirect("/login/")
    user = request.user
    data = {}
    try:
        student = Student.objects.get(user=user)
        data['student'] = student
        data['follow_messages'] = student.follow_message
        data['follow_questions'] = student.follow_question
        timetables = TimeTable.objects.filter(student__user=request.user)
        data['timetables']=timetables
    except Student.DoesNotExist:
        logging.warning("Student does not exist")
    except Student.MultipleObjectsReturned:
        logging.warning("Have multiple student")
    template = loader.get_template(APP_NAME + "/profile.html")
    context = RequestContext(
        request,
        data
    )
    return HttpResponse(template.render(context))

# End Profile view
