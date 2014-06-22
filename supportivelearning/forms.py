from django import forms

class TimeTableUploadForm(forms.Form):
    file  = forms.FileField()
        