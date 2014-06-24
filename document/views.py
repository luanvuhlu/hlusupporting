from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from supportivelearning.models import SubjectStudentYear, StudentYear, Subject
from document.models import Document, Week, DocumentLearning, Day, HomeWork
import re
URL_SESSION="url_previous_session"
APP_NAME='document'
# Create your views here.

# Import Subject Student Year Document
def subject_student_view(request, slug):
    template=APP_NAME+"/subject_student_year.html"
    try:
        id=int(re.search('^\d+', slug).group(0))
        subject=SubjectStudentYear.objects.get(id=id)
        document=Document.objects.get(subject=subject)
        document_learnings=DocumentLearning.objects.filter(document=document)
        weeks=Week.objects.filter(document=document)
        homeworks=HomeWork.objects.filter(document=document)
        weeks_obj=[]
        for week in weeks:
            days=Day.objects.filter(week=week)
            week_obj={'detail': week, 'days':days}
            weeks_obj.append(week_obj)
        context=RequestContext(
                           request,
                           {
                            'subject':subject,
                            'document_learnings':document_learnings,
                            'weeks':weeks_obj,
                            'homeworks':homeworks,
                            }
                           )
    except:
        errors=[]
        errors.append("Cannot find subject")
        context=RequestContext(
                           request,
                           {
                            'subject':subject,
                            'errors':errors,
                            }
                           )
    return render_to_response(template, context)
# End Import Subject Student Year Document
# Import week document
def import_week_document(request):
    # if request.method=='POST':
    # days=  request.POST.getlist('day')
    #     subject_name=request.POST.get('subject_name')
    #     student_year=StudentYear.objects.get(name=request.POST.get('student_year'))
    #     try:
    #         subject_student_year=SubjectStudentYear.objects.get(subject__name=subject_name, student_year=student_year)
    #     except SubjectStudentYear.DoesNotExist:
    #         return HttpResponse("Subject Student Year does not exist")
    #     weeks=[]
    #     day_count=subject_student_year.days_in_week
    #     if subject_student_year.week_number==15:
    #         week_range=range(subject_student_year.week_number)
    #     else:
    #         week_range=range(1, subject_student_year.week_number+1)
    #     for w in week_range:
    #         week={"number":w, "note":"", "require":"", "days":[]}
    #         try:
    #             week_document=Week.objects.get(document__subject=subject_student_year, number=w)
    #             week['number']=week_document.number
    #             week['note']=week_document.note
    #             week['require']=week_document.require
    #             days=[]
    #             try:
    #                 days_in_week=Day.objects.filter(week=week_document)
    #                 for day in days_in_week:
    #                     days.append({"type":day.type, "content":day.content, "note":day.note, "number":day.number})
    #                 if len(days) < day_count:
    #                     for blank_day in range(len(days)+1, day_count):
    #                         days.append({"type":0, "content":"", "note":"", "number":1})
    #                 week['days']=days
    #             except Day.DoesNotExist:
    #                 continue
    #         except Week.DoesNotExist:
    #             print "Week does not exist"
    #         weeks.append({"week":week})
    #     template=APP_NAME+"/__import_week_document.html"
    #     context=RequestContext(request, {
    #                                  'weeks':weeks,
    #                                  'subject_student_year':subject_student_year,
    #                                  })
    # else:
    subject_student_years = SubjectStudentYear.objects.all()
    template = APP_NAME + "/choice_import_week_document.html"
    context = RequestContext(request, {
        'subject_student_years': subject_student_years,
                                     })
    return render_to_response(template, context)
def get_subject_student_year_detail(request, subject_name, student_year, year):
    student_year=StudentYear.objects.get(name=student_year)
    try:
        subject_student_year = SubjectStudentYear.objects.get(subject__name=subject_name, student_year=student_year,
                                                              year__name=year)
    except SubjectStudentYear.DoesNotExist:
        return HttpResponse("Subject Student Year does not exist")
    weeks = []
    day_count = subject_student_year.days_in_week
    if subject_student_year.week_number == 15:
        week_range = range(subject_student_year.week_number + 1)
    else:
        week_range = range(1, subject_student_year.week_number + 1)
    for w in week_range:
        week = {"number": w, "note": "", "require": "", "days": []}
        days = []
        try:
            week_document = Week.objects.get(document__subject=subject_student_year, number=w)
            week['number'] = week_document.number
            week['note'] = week_document.note
            week['require'] = week_document.require
            try:
                days_in_week = Day.objects.filter(week=week_document)
                for day in days_in_week:
                    days.append({"type": day.type, "content": day.content, "note": day.note, "number": day.number})
                if len(days) < day_count:
                    for blank_day in range(len(days) + 1, day_count + 1):
                        days.append({"type": False, "content": "", "note": "", "number": 1})
            except Day.DoesNotExist:
                print "Day does not exist"
        except Week.DoesNotExist:
            print "Week does not exist"
            for blank_day in range(1, day_count + 1):
                days.append({"type": 0, "content": "", "note": "", "number": 1})
        week['days'] = days
        weeks.append(week)
    # subject_student_year=SubjectStudentYear.objects.get(subject__name=subject_name, student_year__name=student_year, year__name=year)
    template = APP_NAME + "/import_subject_document.html"
    context=RequestContext(request, {
                                         'subject_student_year':subject_student_year,
                                         'weeks':weeks,
                                         })
    return render_to_response(template, context)
def save_week_document_import(request):
    if request.method == "POST":
        # try:
        year_name = request.POST.get("year")
        student_year_name = request.POST.get("student_year")
        subject_name = request.POST.get("subject")

        weeks = request.POST.getlist("week")
        # except:
        # pass
        for w in weeks:
            day_types = request.POST.getlist("day_type" + str(w))
            day_numbers = request.POST.getlist("day_number" + str(w))
            day_contents = request.POST.getlist("day_content" + str(w))
            day_notes = request.POST.getlist("day_note" + str(w))
            week_require = request.POST.get("week_require" + str(w))
            # Find document
            subject_student_year = SubjectStudentYear.objects.get(subject__name=subject_name,
                                                                  student_year__name=student_year_name,
                                                                  year__name=year_name)
            try:
                document = Document.objects.get(subject=subject_student_year)
            except Document.DoesNotExist:
                document = Document()
            document.subject = subject_student_year
            document.save()
            # Find Week
            try:
                week_obj = Week.objects.get(document=document, number=w)
            except Week.DoesNotExist:
                print "Week does not exist"
                week_obj = Week()
            week_obj.number = w
            week_obj.document = document
            week_obj.require = week_require
            week_obj.save()
            for i in range(len(day_numbers)):
                if day_types[i] == u'None':
                    day_type = None
                elif day_types[i] == u'True':
                    day_type = True
                else:
                    day_type = False
                day_content = day_contents[i]
                day_number = day_numbers[i]
                day_note = day_notes[i]
                try:
                    day = Day.objects.get(week=week_obj, number=day_number, type=day_type)
                except Day.DoesNotExist:
                    print "Day does not exist"
                    day = Day()
                day.content = day_content
                day.number = day_number
                day.note = day_note
                day.type = day_type
                day.week = week_obj
                day.save()
        return HttpResponseRedirect("/import/week/document/")
    else:
        return HttpResponseRedirect("/import/week/document/")
    return HttpResponse("Saved")
# End Import week document