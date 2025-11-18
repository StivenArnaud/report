from django import forms


from reporting.models import Report, Task

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ('title', 'type')


class EditReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ('type', 'employee_comments', 'file', 'date_start', 'date_end')

class MarkReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ('responsible_comments', 'marks')


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title',)


class EditTaskForm(forms.Form):
    title_edit = forms.Textarea()


