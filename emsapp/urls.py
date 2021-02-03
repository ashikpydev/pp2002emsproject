
from django.urls import path

from .views import *

urlpatterns = [
    path('userprofile', user_profile, name='user_profile'),
    path('add-leaveform', add_leave_form, name='add-leave-form'),
    path('user-login', user_login, name='user-login'),
]