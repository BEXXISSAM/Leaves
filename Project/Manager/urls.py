from django.urls import path, include
from .views import *


urlpatterns = [
    path('login/', user_login, name='login'),
    path('add_employee/', add_employee, name='add_employee'),
    path('', user_login, name='login'),
    path('home/', home_view, name='home'),
    path('add_department/', add_department, name='add_department'),
    path('add_leave/', add_leave, name='add_leave'),
    path('manage_holidays/', manage_holidays, name='manage_holidays'),
    path('admin_home/', admin_view, name='admin_home'),
    path('the_user_is_not_an_admin/', not_admin, name='not_admin'),
    path('search_results/', search_results, name='search_results'),
    path('search/', search_form, name='search_form'),
    path('edit_holiday/<int:holiday_id>/', edit_holiday, name='edit_holiday'),
    path('my_leaves/', employee_leaves, name='my_leaves'),
    path('all_employees', all_employees, name='all_employees'),
    path('edit_department/<int:department_id>/', edit_department, name='edit_department'),
    path('edit_employee/<int:employee_id>', edit_employee, name='edit_employee'),
    path('delete_holiday/<int:holiday_id>/', delete_holiday, name='delete_holiday'),
    path('edit_leave/<int:leave_id>/', edit_leave, name='edit_leave'),
]
