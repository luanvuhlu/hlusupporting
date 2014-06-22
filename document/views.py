from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from supportivelearning.models import SubjectStudentYear, StudentYear, Subject
from document.models import Document, Week, DocumentLearning, Day, HomeWork
import re
URL_SESSION="url_previous_session"
APP_NAME='document'
# Create your views here.
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
def import_week_document(request):
    if request.method=='POST':
        days=  request.POST.getlist('day')
        subject_name=request.POST.get('subject_name')
        student_year=StudentYear.objects.get(name=request.POST.get('student_year'))
        subject_student_year=SubjectStudentYear.objects.get(subject__name=subject_name, student_year=student_year)
        
        if subject_student_year.type == 5: # 5 weeks
            weeks=5
        else:
            weeks=16
        template=APP_NAME+"/import_week_document.html"
        context=RequestContext(request, {
                                     'weeks':weeks,
                                     'days':days,
                                     'subject_student_year':subject_student_year,
                                     })
    else:
        subject_student_years=SubjectStudentYear.objects.all()
        template=APP_NAME+"/choice_import_week_document.html"
        context=RequestContext(request, {
                                         'subject_student_years':subject_student_years,
                                         })
    return render_to_response(template, context)
def get_subject_student_year_detail(request, subject_name, student_year, days_in_week):
    student_year=StudentYear.objects.get(name=student_year)
    subject_student_year=SubjectStudentYear.objects.get(subject__name=subject_name, student_year=student_year)
    if subject_student_year.week_number == 5: # 5 weeks
        weeks=range(1, 6)
    else:
        weeks=range(16)
    days_in_week=int(days_in_week)
    days=range(1, days_in_week+1)
    template=APP_NAME+"/import_subject_student_year.html"
    context=RequestContext(request, {
                                         'subject_student_year':subject_student_year,
                                         'weeks':weeks,
                                         'days':days,
                                         })
    return render_to_response(template, context)
def save_week_document_import(request):
    return HttpResponse("Saved")