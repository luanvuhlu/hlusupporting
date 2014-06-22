from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from datetime import datetime, timedelta
from supportivelearning.models import Year, StudentYear
from datemanagement.models import Week
# Create your views here.
URL_SESSION="url_previous_session"
APP_NAME='datemanagement'

def import_week_view(request):
    template=APP_NAME+"/import_week.html"
    errors=[]
    weeks=[]
    try:
        year=Year.objects.all()[0]
    except:
        return HttpResponse("Don't have year ")
    try:
        student_years=StudentYear.objects.all()
    except:
        return HttpResponse("Don't have student year ")
    if request.method == 'POST':
        try:
            start=datetime.strptime(request.POST.get('start'), "%m/%d/%Y")
            end=datetime.strptime(request.POST.get('end'), "%m/%d/%Y")
            if start.weekday() != 0: # Monday
                return HttpResponse("Start day must be a Monday")
            if end < start + timedelta(days=34) : # less than 5 weeks
                return HttpResponse("Start must greater than end at least 5 weeks")
            type=request.POST.get('type')
            semester=request.POST.get('semester')
            student_year=request.POST.get('student_year')
            d6=timedelta(days=6)
            d1=timedelta(days=1)
            
            date=start
            while date < end:
                period={'start': date.strftime("%m/%d/%Y"), 'end': (date+d6).strftime("%m/%d/%Y")}
                date +=d6
                date+=d1
                weeks.append(period)
            
        except:
            errors.append("Datetime is not match")
            print errors
        context=RequestContext(
                           request,
                           {
                            "errors":errors,
                            "weeks":weeks,
                            'year':year,
                            'type':type,
                            'semester':semester,
                            'start':start.strftime("%m/%d/%Y"),
                            'end':end.strftime("%m/%d/%Y"),
                            'student_year':student_year,
                            }
                           )
    else:
        context=RequestContext(
                           request,
                           {
                            'year':year,
                            'student_years':student_years,
                            }
                           )
    return render_to_response(template, 
                              context,
                              )
def save_import_week(request):
    if request.method=='POST':
        starts=request.POST.getlist('start')
        ends=request.POST.getlist('end')
        weeks=request.POST.getlist('week')
        type=request.POST.get('type')
        semester=request.POST.get('semester')
        years=request.POST.get('years')
        yeare=request.POST.get('yeare')
        try:
            student_year=StudentYear.objects.get(name=request.POST.get('student_year'))
        except:
            return HttpResponse("Cannot find student year")
        try:
            year=Year.objects.get(start=years, end=yeare)
        except:
            return HttpResponse("Cannot find year")
        for i in range(len(starts)-1):
            try:
                week=Week()
                week.number=weeks[i]
                week.start=datetime.strptime(starts[i], "%m/%d/%Y")
                week.end=datetime.strptime(ends[i], "%m/%d/%Y")
                week.student_year=student_year
                week.year=year
                week.semester=semester
                if type=='1':
                    week.type=True
                else:
                    week.type=False
                week.save()
            except:
                return HttpResponse("Add week error")
        return HttpResponseRedirect("/import/week/")
    else:
        return HttpResponseRedirect("/import/week/")