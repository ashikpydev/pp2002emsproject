from django.db.models import fields
from django.forms import widgets
from .models import *
from django import forms
from django.contrib.auth.models import User, Group

class UserProfileForm(forms.ModelForm):
    department = forms.ModelChoiceField(widget = forms.Select(attrs={'class':'form-control bg-light',}), queryset=Department.objects.all())
    class Meta:
        model = UserProfile
        fields = ['address', 'department', 'designation', 'date_of_birth', 'email_address', 'mobile_number']

        widgets = {
            'address':forms.TextInput(attrs={'class':'bg-light form form-control'}),
            'designation':forms.TextInput(attrs={'class':'bg-light form form-control'}),
            'email_address':forms.TextInput(attrs={'class':'bg-light form form-control'}),
            'date_of_birth':forms.DateInput(attrs={'type':'date', 'class':'bg-light form form-control'}),
            'mobile_number':forms.TextInput(attrs={'class':'bg-light form form-control'}),
        }

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
        
        
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form rounded form-group col-md-2 mt-3 bg-light', 'placeholder':"Enter Password..."}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form rounded form-group col-md-2 mt-3 bg-light', 'placeholder':"Enter Password Again..."}))

    department = forms.ModelChoiceField(widget=forms.Select(attrs={'class':'rounded form form-group bg-light col-md-5',}), queryset = Department.objects.all())
    designation = forms.ModelChoiceField(widget=forms.Select(attrs={'class':'rounded form form-group bg-light col-md-5',}), queryset = Group.objects.all())
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password', 'confirm_password', 'department', 'designation']
        help_texts = {
            'username': None,
            'email':None,
            
        }

        widgets = {
            'username':forms.TextInput(attrs={'class':'form rounded form-group bg-light col-md-4 mt-3', 'placeholder':"Enter UserName..."}),
            'email':forms.TextInput(attrs={'class':'form form-control bg-light col-md-12', 'placeholder':"Enter Email..."}),
            'first_name':forms.TextInput(attrs={'class':'rounded form form-group bg-light col-md-5 mr-3', 'placeholder':"Enter First Name..."}),
            'last_name':forms.TextInput(attrs={'class':'rounded form form-group bg-light col-md-5', 'placeholder':"Enter Last Name..."}),

        }