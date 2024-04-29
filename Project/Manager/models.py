from django.db import models
from django.contrib.auth.models import User


class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Employee(models.Model):
    username = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    isAdmin = models.BooleanField(default=False)

    def __str__(self):
        return str(self.username)


class Leaves(models.Model):
    employeeId = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leaveDate = models.DateField()
    duration = models.IntegerField()
    endOfLeave = models.DateField()
    leaveNumber = models.IntegerField()
    isDelayed = models.BooleanField(default=False)

    def __str__(self):
        return ' leave ' + str(self.employeeId)


class holidays(models.Model):
    name = models.CharField(max_length=100)
    holidayStartingDay = models.DateField()
    duration = models.IntegerField()

    def __str__(self):
        return str(self.name)

