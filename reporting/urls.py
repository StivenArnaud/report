from django.urls import path

from reporting import views


app_name = 'reporting'


urlpatterns = [
    path('add-report/', views.add_report, name='add_report'),
    path('detail-report/<uuid:report_id>/', views.detail_report, name='detail_report'),
    path('add-task/<uuid:report_id>/', views.add_task, name='add_task'),
    path('delete-task/<uuid:task_id>/', views.delete_task, name='delete_task'),
    path('edit-task/<uuid:task_id>/', views.edit_task, name='edit_task'),
    path('complete-task/<uuid:task_id>/', views.complete_task, name='complete_task'),
    path('edit-report/<uuid:report_id>/', views.edit_report, name='edit_report'),
    path('list-reports/', views.list_reports, name='list_reports'),
    path('period-form/', views.period_form, name='period_form'),
    path('mark-report/<uuid:report_id>/', views.mark_report, name='mark_report'),
    path('reports-calendar-data/<uuid:user_id>', views.get_reports_calendar_data, name='reports_calendar_data'),
]