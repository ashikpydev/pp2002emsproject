
from django.urls import path

from .views import *

urlpatterns = [
    path('edit', edit, name='edit'),
    
    path('reset-password', reset_password, name='reset-password'),
    
    path('forgot-password', forgot_password, name='forgot-password'),
    path('change-password', change_password, name='change_password'),
    path('logout', user_logout, name='user_logout'),
    path('add-employee', add_employee, name='add_employee'),
    path('add-todo-list', add_todo_list, name='add_todo_list'),
    path('my-application/', my_application, name='my_application'),

    path('', user_login, name='user-login'),
    
    path('todo-ist-evaluation/<int:id>/<int:sts>', todo_list_evaluation, name='todo-list-evaluation'),


    path('application-approval/<int:id>/<sts>', application_approval, name='application_approval'),

    path('all-application', all_application, name='all_application'),
    path('userprofile', user_profile, name='user_profile'),
    path('add-leaveform', add_leave_form, name='add-leave-form'),
    
    path('todolist', to_do_list, name='todolist'),
]