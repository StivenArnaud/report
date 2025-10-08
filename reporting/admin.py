from django.contrib import admin

# Register your models here.
from reporting.models import Report, Task


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'type')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'report')
