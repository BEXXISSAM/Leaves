from django.urls import path, include
from .views import user_login, add_employee, home_view, add_department, add_leave


urlpatterns = [
    path('login/', user_login, name='login'),
    path('add_employee/', add_employee, name='addEmployee'),
    path('', user_login, name='login'),
    path('home/', home_view, name='home'),
    path('add_department/', add_department, name='add_department'),
    path('add_leave/', add_leave, name='add_leave'),

]
