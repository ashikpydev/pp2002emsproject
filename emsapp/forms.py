from .models import *
from django import forms


class LeaveApplicationForm(forms.ModelForm):
    class Meta:
        model = LeaveApplication
        fields = ['cause_of_leave', 'start_date', 'end_date']

        widgets = {
            'cause_of_leave':forms.Textarea(attrs={'class':'bg-light form-control form'}),
             'start_date':forms.DateInput(attrs={'type':'date', 'class':'bg-light form form-control datepicker'}),
             'end_date':forms.DateInput(attrs={'type':'date', 'class':'bg-light form form-control datepicker'})
        }


class TodoListForm(forms.ModelForm):
    class Meta:
        model = TodoList
        fields = '__all__'
        exclude= ('user','pending_status', 'working_status', 'done_status')
        
        widgets = {
            'what_to_do':forms.TextInput(attrs={'class':'form-group form bg-light col-md-5 p-3'}),
            'when_to_do':forms.DateInput(attrs={'type':'date','class':'p-3 form-group bg-light datepicker form col-md-3'})
        }