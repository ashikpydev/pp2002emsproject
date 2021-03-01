from django.contrib import admin

# Register your models here.
from .models import *
class TodoListAdmin(admin.ModelAdmin):
    list_display = ('user', 'pending_status', 'working_status', 'done_status')


admin.site.register(UserProfile)
admin.site.register(LeaveApplication)
admin.site.register(TodoList, TodoListAdmin)
admin.site.register(Department)
