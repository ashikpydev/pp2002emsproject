
from django.urls import path

from .views import *
urlpatterns = [
    path('application-approval/<int:id>/<sts>', application_approval, name='application_approval'),

    path('all-application', all_application, name='all_application'),
    path('userprofile', user_profile, name='user_profile'),
    path('add-leaveform', add_leave_form, name='add-leave-form'),
    path('user-login', user_login, name='user-login'),
]