from .models import *
from django import forms


class LeaveApplicationForm(forms.ModelForm):
    class Meta:
        model = LeaveApplication
        fields = ['cause_of_leave', 'start_date', 'end_date']

        widgets = {
            'cause_of_leave':forms.Textarea(attrs={'class':'form-control form'}),
             'start_date':forms.DateInput(attrs={'type':'date', 'class':'form form-control datepicker'}),
             'end_date':forms.DateInput(attrs={'type':'date', 'class':'form form-control datepicker'})
        }

