from django.contrib import admin
from .models import Employee, Leaves, Department, holidays


admin.site.register(Employee)
admin.site.register(Leaves)
admin.site.register(Department)
admin.site.register(holidays)
