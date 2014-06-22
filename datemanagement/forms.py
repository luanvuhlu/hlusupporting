from django import forms

class ImportWeekForm(forms.Form):
    type=forms.Select()
    start=forms.DateField()
    end=forms.DateField()
    
        