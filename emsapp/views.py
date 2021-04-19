from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
import random
from.models import *
from django.db.models import Q

# Create your views here.
from .models import *
from .forms import *
def edit(request):
    user = request.user
    profile = UserProfile.objects.get(user = user)
    if request.method == 'POST':
        form = UserProfileForm(instance=profile, data = request.POST)
        if form.is_valid():
            form = form.save()
            return redirect('/userprofile')
        else:
            print("not ok")
    print(profile)
    form = UserProfileForm(instance=profile)
    print(form)
    context = {'form':form}
    return render(request, 'update.html', context)


def reset_password(request):
    if request.method == 'POST':
        otp = request.POST['otp']
        username = request.POST['username']
        np = request.POST['np']
        try:
            otp = OTP.objects.get(otp = otp)
            if otp.satus == True:
                try:
                    user = User.objects.get(username = username)
                    user.set_password(np)
                    user.save()
                    otp.status = False
                    otp.save()
                    return redirect('/')
                except:
                    context = {'msg':'invalid username'}
                    return render (request, 'forgot-password-with-otp.html', context)
            else:
                context = {'msg':'invalid username'}
                return render (request, 'forgot-password-with-otp.html', context)
        except:
            context = {'msg':'invalid OTP'}
            
            return render (request, 'forgot-password-with-otp.html', context)
    return render (request, 'forgot-password-with-otp.html')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        otp = random.randint(1000,9999)
        otp = str(otp)
        OTP.objects.create(otp = otp)
        print(otp)
        send_mail('forgot password', otp, 'alhasib097@gmail.com', [email])
        return render(request, 'forgot-password-with-otp.html')
    return render(request, 'forgot_password.html')

from datetime import date, datetime
# from django.utils.timezone import UTC

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username)
        print(password)
        user = authenticate(username = username, password = password)
        if user:
            login(request, user)
            # now = datetime.now()
            now = datetime.now()
            time = now.strftime("%I:%M:%P")
            print(time)
            if time > '04:20 PM':
                Attendance.objects.create(user = request.user)
                # Attendance.objects.create(user = user)
                return redirect('/userprofile')
            else:
                Attendance.objects.create(user = request.user, attendace_status = True)
                return redirect('/userprofile')
        else:
            messages = "Invalid Username Or Password"
            context = {'messages':messages}
            return render(request, 'login.html', context)

    return render(request, 'login.html')

def user_profile(request):
    user = request.user
    print(user)
    userprofile = UserProfile.objects.get(user = user)
    context = {'userprofile':userprofile, 'user':user}
    return render(request, 'userprofile.html', context)

@login_required(login_url='/')
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
    
    
from datetime import datetime

@login_required(login_url='/')
def all_application(request):
    if request.method == 'POST':
        search_data = request.POST['sform']
        s_date = request.POST['sdate']
        e_date = request.POST['edate']
        print(search_data)
        print(s_date)
        print(e_date)

        try:
            print(1)
            user = User.objects.get(username = search_data)

            applications = LeaveApplication.objects.filter(user = user, start_date__gte = s_date, checked = False)
            for i in applications:
                print(i.start_date)

            context = {'applications':applications}
            return render(request, 'all_application.html', context)
        except:
            msg = "No Data Fount"
            context = {'msg':msg}
            return render(request, 'all_application.html', context)

    else:
        applications = LeaveApplication.objects.filter(checked = False)
        context = {'applications':applications}
        return render(request, 'all_application.html', context)


def application_approval(request, id, sts):
    print(sts)
    print(type(sts))
    application = LeaveApplication.objects.get(id = id)
    application.checked = True 
    if int(sts) == 0:
        application.approved = False 
        application.save()
        return redirect('/all-application')
    else:
        application.approved = True
        application.save()
        return redirect('/all-application')
    return redirect('/all-application')



def to_do_list(request):
    my_todo_list_pending = TodoList.objects.filter(user = request.user, pending_status = True)
    my_todo_list_pending_count = my_todo_list_pending.count()
    
    working_todo_list = TodoList.objects.filter(user = request.user, working_status = True, pending_status = False)
    working_todo_list_count = working_todo_list.count()
    
    done_todo_list = TodoList.objects.filter(user = request.user, working_status = False, pending_status = False)
    done_todo_list_count = done_todo_list.count()
    
    form = TodoListForm()
    
    context = {'my_todo_list_pending':my_todo_list_pending, "my_todo_list_pending_count":my_todo_list_pending_count,
               'working_todo_list':working_todo_list, 'working_todo_list_count':working_todo_list_count,
               'done_todo_list':done_todo_list,
                'done_todo_list_count':done_todo_list_count,
                'form':form
}
    return render(request, 'todolist.html', context)


def todo_list_evaluation(request, id, sts):
    print(sts)
    print(id)
    my_to_list = TodoList.objects.get(id = id)
    if sts == 'working':
        my_to_list.working_status = True
        my_to_list.pending_status = False
        my_to_list.save()
        return redirect('/todolist')
    elif sts == 'done':
        my_to_list.working_status = False
        my_to_list.done_status = True
        my_to_list.save()
        return redirect('/todolist')
        

    return redirect('/todolist')

def add_todo_list(request):
    if request.method == 'POST':
        form = TodoListForm(request.POST)
        if form.is_valid():
            form = form.save(commit = False)
            form.user = request.user
            form.save()
            return redirect('/todolist')
    
    
def user_logout(request):
    logout(request)
    return redirect('/')

def add_employee(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            department_id = request.POST['department']
            email = request.POST['email']
            department = Department.objects.get(id = department_id)
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            
            designation_id = request.POST['designation']
            designation = Group.objects.get(id = designation_id)
            
            user = User.objects.create_user(username = username, password = password, first_name = first_name, last_name = last_name)
            profile = UserProfile.objects.create(user = user, department = department, email_address = email, designation = designation.name)
            form = UserForm()
            message = "Successfully Added!"
            status = 'success'
            context = {'form':form, 'message':message, 'sts':status}
            return render(request, 'add_employee.html', context)
        else:
            form = UserForm()
            message = "password not matched"
            status = 'danger'
            context = {'form':form, 'message':message,'sts':status}
            return render(request, 'add_employee.html', context)
    else:
        form = UserForm()
        context = {'form':form}
        return render(request, 'add_employee.html', context)

def my_application(request):
    user = request.user
    application = LeaveApplication.objects.filter(user = user)
    print(application)
    context = {'application':application}
    return render(request, 'my-application.html', context)

def change_password(request):
    if request.method == 'POST':
        old_password = request.POST['op']
        new_password = request.POST['np']
        retype_password = request.POST['rp']
        # print(old_password)
        # print(new_password)
        # print(retype_password)
        print(request.user.username)
        user = authenticate(username = request.user.username, password = old_password)
        if user:
            if new_password == retype_password:
                user = request.user
                user.set_password(new_password)
                user.save()
                messages = messages.success(request, 'Password has changed')
                return redirect('/')

            else:
                message = 'Password Not Matched!'
                context = {'message':message}
                return render(request, 'change_password.html', context)
        else:
            message = 'Invalid old Password'
            context = {'message':message}
            return render(request, 'change_password.html', context)
            
        # print(v)
        # # if old_password == request.user.password:
        # #     print("ok")
    return render(request, 'change_password.html')



def attendance_report(request):
    if request.method == 'POST':
        user = request.POST['user']
        s_date = request.POST['s_date']
        e_date = request.POST['e_date']
        print(user)
        print(s_date)
        print(e_date)
        user = User.objects.get(username = user)
        report = Attendance.objects.filter(user = user)
        late = 0
        intime = 0
        for i in report:
            if i.attendace_status == False:
                late = late + 1
            elif i.attendace_status == True:
                intime = intime+1
        print(report)
        context = {'report':report, 'late':late, 'intime':intime}
        return render(request, 'report.html', context)
    return render(request, 'report.html')