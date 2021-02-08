from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth import login, logout, authenticate
# Create your views here.
from .models import *
from .forms import *
def user_login(request):
    if request.method == 'POST':
        username = request.POST['uname']
        password = request.POST['psw']
        print(username)
        print(password)
        user = authenticate(username = username, password = password)
        if user:
            login(request, user)
            return redirect('/userprofile')

    return render(request, 'login.html')

def user_profile(request):
    user = request.user
    print(user)
    userprofile = UserProfile.objects.get(user = user)
    context = {'userprofile':userprofile}
    return render(request, 'userprofile.html', context)


def add_leave_form(request):
    if request.method == 'POST':
        print(request.user)
        user = request.user
        form = LeaveApplicationForm(request.POST)
        print('startdate')
        print(request.POST['start_date'])
        print("enddate")
        print(request.POST['end_date'])

        # print(form)
        if form.is_valid():
            print(1)
            form = form.save(commit = False)
            print(2)
            form.user = request.user
            print(3)
            form.save()
            print(5)
            form = LeaveApplicationForm()
            context = {'msg':'Application Submitted Successfully!','form':form}
            return render(request, 'add_leave_form.html', context)
    else:
        user_application =LeaveApplication.objects.filter(checked = False, user = request.user)
        if user_application:
            context = {'msg':'You Have Already A Pending Application!'}
            return render(request, 'add_leave_form.html', context)
        else:
            form = LeaveApplicationForm()
            context = {'form':form}
            return render(request, 'add_leave_form.html', context)
    
    

def all_application(request):
    applications = LeaveApplication.objects.filter(checked = False)
    context = {'applications':applications}
    return render(request, 'all_application.html', context)


def application_approval(request, id, sts):
    application = LeaveApplication.objects.get(id = id)
    application.checked = True 
    if sts == 0:
        application.approved = False 
        application.save()
        return redirect('/all-application')
    else:
        application.approved = True
        application.save()
        return redirect('/all-application')
    return redirect('/all-application')