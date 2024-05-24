from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import *
from .models import holidays
from django.contrib.auth.decorators import login_required
from datetime import timedelta, datetime
from calendar import SUNDAY, SATURDAY
from django.urls import reverse
from django.http import HttpResponseRedirect
from datetime import date
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import user_passes_test


def admin_required(function):
    def wrapper(request, *args, **kwargs):
        def is_admin(request):
            return request.user.is_authenticated and request.user.employee.is_admin

        if user_passes_test(is_admin)(request):
            return function(request, *args, **kwargs)
        else:
            return redirect('not_admin')

    return wrapper


@login_required
def add_leave(request):
    if request.method == 'POST':
        employee_id = request.user.employee
        leave_date = request.POST.get('leaveDate')
        duration = request.POST.get('duration')
        leave_date = datetime.strptime(leave_date, '%Y-%m-%d').date()

        end_of_leave = leave_date + timedelta(days=int(duration) - 1)
        current_date = leave_date

        while current_date <= end_of_leave:
        	if holidays.objects.filter(holidayStartingDay=current_date).exists():
                	end_of_leave += timedelta(days=1)
		current_date += timedelta(days=1)

        leave_count = Leaves.objects.filter(employeeId=employee_id).count()
        leave = Leaves.objects.create(
            employeeId=employee_id,
            leaveDate=leave_date,
            duration=duration,
            endOfLeave=end_of_leave + timedelta(days=1),
            leaveNumber=leave_count + 1,
            isDelayed=False
        )
        leave.save()
        messages.success(request, 'تمت إضافة الرخصة بنجاح')

        return redirect('add_leave')

    return render(request, 'addLeave.html')


def add_leave_by_id(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)

    if request.method == 'POST':
        leave_date = request.POST.get ('leaveDate')
        duration = request.POST.get('duration')
        leave_date = datetime.strptime(leave_date, '%Y-%m-%d').date ()

        end_of_leave = leave_date + timedelta(days=int(duration) - 1)
        current_date = leave_date

        while current_date <= end_of_leave:
        	if holidays.objects.filter(holidayStartingDay=current_date).exists ():
                	end_of_leave += timedelta(days=1)

        	current_date += timedelta(days=1)

        leave_count = Leaves.objects.filter(employeeId=employee_id).count()
        leave = Leaves.objects.create(
            employeeId=employee_id,
            leaveDate=leave_date,
            duration=duration,
            endOfLeave=end_of_leave + timedelta (days=1),
            leaveNumber=leave_count + 1,
            isDelayed=False
        )
        leave.save()
        messages.success (request, 'تمت إضافة الرخصة بنجاح')
        return redirect('show_employee_leaves', employee_id=employee_id)

    return render(request, 'add_employee_leave.html', {'employee': employee})


@admin_required
@login_required
def add_employee(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        PPR = request.POST.get('username')
        department_id = request.POST.get('department')
        password = request.POST.get('password')
        isAdmin = request.POST.get('isAdmin') == 'TRUE'
        full_name = first_name + ' ' + last_name
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
            PPR=PPR,
            full_name=full_name,
            department=department,
            isAdmin=isAdmin
        )
        messages.success(request, ' تم اضافة الموظف بنجاح')
        departments = Department.objects.all()
        context = {'departments': departments,
                   'success_message': ' تم اضافة الموظف بنجاح'}
        return render(request, 'addEmployee.html', context)
    else:
        departments = Department.objects.all()
        context = {'departments': departments}
        return render(request, 'addEmployee.html', context)


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.employee.isAdmin:
                return redirect('admin_home')
            else:
                return redirect('home')
        else:
            error = "Invalid username or password."
            return render(request, 'login.html', {'error': error})
    else:
        return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return render(request, 'login.html')


@login_required
def home_view(request):
    user_department = request.user.employee.department
    today = date.today()
    current_month = today.month

    leaves_list = Leaves.objects.filter(
        employeeId__department=user_department,
        isDelayed=False
    ).filter(
        Q(leaveDate__year=today.year, leaveDate__month=current_month) |
        Q(endOfLeave__year=today.year, endOfLeave__month=current_month) |
        Q(leaveDate__lt=today, endOfLeave__gt=today)
    )

    paginator = Paginator(leaves_list, 10)
    page = request.GET.get('page')

    try:
        leaves = paginator.page(page)
    except PageNotAnInteger:
        leaves = paginator.page(1)
    except EmptyPage:
        leaves = paginator.page(paginator.num_pages)

    return render(request, 'home.html', {'leaves': leaves})


@admin_required
def admin_view(request):
    today = date.today()
    current_month = today.month
    leaves_list = Leaves.objects.filter(
        Q(leaveDate__year=today.year, leaveDate__month=current_month) |
        Q(endOfLeave__year=today.year, endOfLeave__month=current_month) |
        Q(leaveDate__lt=today, endOfLeave__gt=today)
    )
    paginator = Paginator(leaves_list, 10)
    page = request.GET.get('page')

    try:
        leaves = paginator.page(page)
    except PageNotAnInteger:
        leaves = paginator.page(1)
    except EmptyPage:
        leaves = paginator.page(paginator.num_pages)

    return render(request, 'admin/home.html', {'leaves': leaves})


@login_required
def not_admin(request):
    return render(request, 'admin/notAdmin.html', {})


@admin_required
@login_required
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


@admin_required
def edit_department(request, department_id):
    if request.method == 'POST':
        try:
            department = Department.objects.get(pk=department_id)
            department.name = request.POST.get('name')
            department.save()
            messages.success(request, 'تم تعديل الشعبة بنجاح!')
            return redirect(reverse('add_department'))
        except holidays.DoesNotExist:
            messages.error(request, 'شعبة غير موجودة!')
            return render(request, 'editDepartment.html', {'department': None})
    else:
        try:
            department = Department.objects.get(pk=department_id)
            return render(request, 'editDepartment.html', {'department': department})
        except Department.DoesNotExist:
            messages.error(request, 'شعبة غير موجودة!')
            return redirect('add_department')


@admin_required
@login_required
def manage_holidays(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        starting_date = request.POST.get('starting_date')
        duration = request.POST.get('duration')
        holiday = holidays.objects.create(
            name=name, holidayStartingDay=starting_date, duration=duration)
        messages.success(request, "تمت اضافة العطلة بنجاح")
        return redirect('manage_holidays')
    else:
        holidays_list = holidays.objects.all()
        paginator = Paginator(holidays_list, 10)
        page = request.GET.get('page')
        try:
            holidays_page = paginator.page(page)
        except PageNotAnInteger:
            holidays_page = paginator.page(1)
        except EmptyPage:
            holidays_page = paginator.page(paginator.num_pages)
        return render(request, 'manageHolidays.html', {'holidays': holidays_page})


@admin_required
@login_required
def edit_holiday(request, holiday_id):
    if request.method == 'POST':
        try:
            holiday = holidays.objects.get(pk=holiday_id)
            holiday.name = request.POST.get('name')
            holiday.holidayStartingDay = request.POST.get('starting_date')
            holiday.duration = request.POST.get('duration')
            holiday.save()
            messages.success(request, 'تم تعديل العطلة بنجاح!')
            return redirect(reverse('manage_holidays'))
        except holidays.DoesNotExist:
            messages.error(request, 'عطلة غير موجودة!')
            return render(request, 'editHoliday.html', {'holiday': None})
    else:
        try:
            holiday = holidays.objects.get(pk=holiday_id)
            return render(request, 'editHoliday.html', {'holiday': holiday})
        except holidays.DoesNotExist:
            messages.error(request, 'عطلة غير موجودة!')
            return redirect('manage_holidays')


@admin_required
@login_required
def search_results(request):
    name = request.GET.get('name', None)
    username = request.GET.get('username', None)
    start_date_str = request.GET.get('start_date', None)
    end_date_str = request.GET.get('end_date', None)
    leaves_list = Leaves.objects.all()

    if name:
        leaves_list = leaves_list.filter(
            Q(employeeId__full_name__icontains=name)
        )

    if username:
        leaves_list = leaves_list.filter(
            Q(employeeId__PPR=username)
        )

    if start_date_str and end_date_str:
        try:
            start_date = date.fromisoformat(start_date_str)
            end_date = date.fromisoformat(end_date_str)
            leaves_list = leaves_list.filter(
                Q(leaveDate__gte=start_date) & Q(leaveDate__lte=end_date)
            )
        except ValueError:
            pass

    return render(request, 'search_results.html', {'leaves': leaves_list})


@admin_required
@login_required
def search_form(request):
    return render(request, 'search.html')


@login_required()
def employee_leaves(request):
    employee_id = request.user.employee.id
    employee = Employee.objects.get(pk=employee_id)
    leaves = Leaves.objects.filter(employeeId=employee)
    return render(request, 'my_leaves.html', {'employee': employee, 'leaves': leaves})


@admin_required
@login_required
def all_employees(request):
    employees = Employee.objects.all().order_by('full_name')
    paginator = Paginator(employees, 10)
    page = request.GET.get('page')
    try:
        employees = paginator.page(page)
    except PageNotAnInteger:
        employees = paginator.page(1)
    except EmptyPage:
        employees = paginator.page(paginator.num_pages)
    return render(request, 'all_employees.html', {'employees': employees})


@admin_required
@login_required
def edit_employee(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    departments = Department.objects.all()

    if request.method == 'POST':
        if 'delete' in request.POST:
            employee = Employee.objects.get(id=employee_id)
            user = employee.username
            user.delete()
            employee.delete()
            return redirect('/all_employees')

        department_id = request.POST.get('department')
        try:
            department = Department.objects.get(pk=department_id)
        except Department.DoesNotExist:
            messages.error(request, 'القسم غير موجود!')
            return redirect('all_employees')

        isAdmin_str = request.POST.get('isAdmin')
        isAdmin = isAdmin_str.lower() == 'true' if isAdmin_str else False

        employee.department = department
        employee.isAdmin = isAdmin

        employee.save()

        user = employee.username
        user.save()

        messages.success(request, 'تم تعديل الموظف بنجاح!')
        return redirect('all_employees')

    return render(request, 'editEmployee.html', {'employee': employee, 'departments': departments})


@admin_required
@login_required
def delete_holiday(request, holiday_id):
    try:
        holiday = holidays.objects.get(pk=holiday_id)
        holiday.delete()
        return redirect('manage_holidays')
    except holidays.DoesNotExist:
        pass
    return redirect('manage_holidays')


@admin_required
@login_required
def edit_leave(request, leave_id):
    try:
        leave = Leaves.objects.get(pk=leave_id)
    except Leaves.DoesNotExist:
        return redirect('add_leave')

    if request.method == 'POST':
        leave_date = request.POST.get('leaveDate')
        duration = request.POST.get('duration')

        try:
            leave_date = datetime.strptime(leave_date, '%Y-%m-%d').date()
        except ValueError:
            context = {'leave': leave,
                       'error': 'Invalid date format. Please use YYYY-MM-DD.'}
            return render(request, 'modify_leave.html', context)

        end_of_leave = leave_date + timedelta(days=int(duration) - 1)
        current_date = leave_date

        while current_date <= end_of_leave:
            if current_date.weekday() in (SUNDAY, SATURDAY):
                end_of_leave += timedelta(days=1)
            elif holidays.objects.filter(holidayStartingDay=current_date).exists():
                end_of_leave += timedelta(days=1)

            current_date += timedelta(days=1)

        new_leave = Leaves.objects.create(
            employeeId=leave.employeeId,
            leaveDate=leave_date,
            duration=duration,
            endOfLeave=end_of_leave + timedelta(days=1),
            leaveNumber=leave.leaveNumber + 1
        )
        new_leave.save()

        leave.isDelayed = True
        leave.save()

        current_url = request.path_info
        if 'my_leaves' in current_url:
            return redirect('my_leaves')
        else:
            return redirect('my_leaves')

    context = {'leave': leave}
    return render(request, 'modify_leave.html', context)



def show_employee_leaves(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    leaves = Leaves.objects.filter(employeeId=employee)
    return render(request, 'employee_leaves.html', {'employee': employee, 'leaves': leaves})
