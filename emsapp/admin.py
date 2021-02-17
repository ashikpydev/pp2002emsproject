from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(UserProfile)
admin.site.register(LeaveApplication)
admin.site.register(TodoList)
