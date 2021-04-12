from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class OTP(models.Model):
    otp = models.CharField(max_length=250)
    status = models.BooleanField(default=True)
    
    def __str__(self):
        return self.otp
    
class Department(models.Model):
    name = models.CharField(max_length=250)
    
    def __str__(self):
        return self.name
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    profile_image = models.ImageField(blank = True, null = True)
    address = models.CharField(max_length = 300, blank = True, null = True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True)
    designation = models.CharField(max_length = 300, blank = True, null = True)
    date_of_birth = models.DateField(blank = True, null = True)
    email_address = models.CharField(max_length = 300, blank = True, null = True)
    mobile_number = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return str(self.user)


class LeaveApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cause_of_leave = models.TextField(blank = True, null = True)
    start_date = models.DateField(blank = True, null = True)
    end_date = models.DateField(blank = True, null = True)
    checked = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)

    # date = models.DateField(auto_now_add=True, blank = True, null = True)

    def __str__(self):
        return str(self.user)


class TodoList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    what_to_do = models.TextField(blank=True, null=True,)
    when_to_do = models.DateField(blank=True, null=True)
    pending_status = models.BooleanField(default=True)
    working_status = models.BooleanField(default=False)
    done_status = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.user)


class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    attendace_status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.user)
    
    