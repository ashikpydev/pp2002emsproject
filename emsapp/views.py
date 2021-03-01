from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.
from .models import *
from .forms import *
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
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
    
    

@login_required(login_url='/')
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