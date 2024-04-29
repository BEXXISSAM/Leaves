from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import Employee, Department
from .models import Leaves
from django.contrib.auth.decorators import login_required
from datetime import timedelta, datetime


@login_required
def add_leave(request):
    if request.method == 'POST':
        employee_id = request.user.employee
        leave_date = request.POST.get('leaveDate')
        duration = request.POST.get('duration')  # Set default to 0 if missing
        leave_date = datetime.strptime(leave_date, '%Y-%m-%d').date()
        end_of_leave = 0 ;
        if duration == "24":
            end_of_leave = leave_date + timedelta(days=24)
        elif duration == "30":
            end_of_leave = leave_date + timedelta(days=30)
        elif duration == "54":
            end_of_leave = leave_date + timedelta(days=54)

        leave_count = Leaves.objects.filter(employeeId=employee_id).count()

        leave = Leaves.objects.create(
            employeeId=employee_id,
            leaveDate=leave_date,
            duration=duration,
            endOfLeave=end_of_leave,
            leaveNumber=leave_count + 1,
            isDelayed=False
        )
        leave.save()

        return redirect('add_leave')  # Redirect to a success page

    return render(request, 'addLeave.html')

def add_employee(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        department_id = request.POST.get('department')
        password = request.POST.get('password')
        isAdmin = request.POST.get('isAdmin') == 'TRUE'
        if User.objects.filter(username=username).exists():
            messages.error(request, 'هذا الموظف يمتلك حسابا بالفعل')
            return redirect('add_employee')

        user = User.objects.create_user(username, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        department = Department.objects.get(pk=department_id)
        employee = Employee.objects.create(
            username=user,
            department=department,
            isAdmin=isAdmin
        )
        messages.success(request, ' تم اضافة الموظف بنجاح')
        departments = Department.objects.all()
        context = {'departments': departments, 'success_message': ' تم اضافة الموظف بنجاح'}
        return render(request, 'addEmployee.html', context)
    else:
        departments = Department.objects.all()
        context = {'departments': departments}
        return render(request, 'addEmployee.html', context)


# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#
#         user = authenticate(request, username=username, password=password)
#
#         if user is not None:
#             login(request, user)
#             return redirect('home')
#         else:
#             error = "Invalid username or password."
#             return render(request, 'login.html', {'error': error})
#     else:
#         return render(request, 'login.html')
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user against the Employee model
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # If authentication succeeds, log in the user
            login(request, user)
            return redirect('home')  # Redirect to the home page upon successful login
        else:
            error = "Invalid username or password."
            return render(request, 'login.html', {'error': error})
    else:
        return render(request, 'login.html')


def home_view(request):
    employees = Employee.objects.all()
    context = {
        'employees': employees,
        'username': request.user.username if request.user.is_authenticated else None
    }
    return render(request, 'home.html', context)


def add_department(request):
    departments = Department.objects.all()
    context = {
        'department': departments
    }

    if request.method == 'POST':
        name = request.POST.get('name')

        if Department.objects.filter(name=name).exists():
            messages.error(request, 'هذه الشعبة موجودة بالفعل')
            return redirect('add_department')

        department = Department.objects.create(name=name)
        messages.success(request, 'تم اضافة الشعبة بنجاح.')

        return redirect('add_department')

    else:
        return render(request, 'addDepartment.html', context)
