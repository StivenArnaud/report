from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.translation import gettext_lazy as _
from datetime import datetime
from django.http import HttpResponse
from django.db.models import Q

# Create your views here.
from authentication.models import User
from reporting.models import Report, Task
from reporting.forms import ReportForm, TaskForm, EditReportForm, MarkReportForm
from reporting.utils import temps_restant_jour


@login_required
def add_report(request):
    report = Report.objects.create(
        user=request.user,
        title=f"Rapport de : {request.user.get_full_name()} - {datetime.now().date().strftime('%d/%m/%Y')}",
    )

    return redirect('reporting:edit_report', report_id=report.id)



@login_required
def edit_report(request, report_id):
    report = get_object_or_404(Report, pk=report_id, user=request.user)
    tasks = report.tasks.all()
    temps_restant = temps_restant_jour(report.created)

    if temps_restant is None:
        return redirect('reporting:list_reports')

    if request.method == 'POST':
        form = EditReportForm(request.POST, request.FILES, instance=report)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            report.published = True
            report.save()
            messages.success(request, _("Votre rapport a ete envoye avec succes !"))
            return redirect('reporting:list_reports')
        else:
            print(form.errors)
    else:
        form = EditReportForm(instance=report)
    context = {
        'form': form,
        'report': report,
        'tasks': tasks,
        'temps_restant': temps_restant,
    }
    return render(request, 'frontend/reporting/add_report.html', context)


@login_required
def detail_report(request, report_id):
    report = get_object_or_404(Report, pk=report_id)
    tasks = report.tasks.all()

    context = {
        'report': report,
        'tasks': tasks,
    }

    return render(request, 'frontend/reporting/detail_report.html', context)


@login_required
def list_reports(request):
    reports = []
    report_type = request.GET.getlist('report_type')

    if request.user.role == User.EMPLOYEE:
        reports = Report.objects.prefetch_related('tasks', 'user__responsible').filter(user=request.user)

    elif request.user.role == User.RESPONSIBLE:
        reports = Report.objects.prefetch_related('tasks', 'user__responsible').filter(
            Q(user__responsible=request.user, published=True) | Q(user=request.user))

    else:
        reports = Report.objects.prefetch_related('tasks', 'user__responsible').filter(
            Q(published=True) | Q(user=request.user))

    if report_type:
        reports = reports.filter(type__in=report_type)

    paginator = Paginator(reports, 10)
    page = request.GET.get('page')

    try:
        reports = paginator.page(page)
    except PageNotAnInteger:
        reports = paginator.page(1)
    except EmptyPage:
        reports = paginator.page(paginator.num_pages)

    if 'HX-Request' in request.headers:
        return render(request, 'frontend/reporting/partials/list_reports_card.html', {'reports': reports})

    context = {
        'reports': reports,
        'report_types': Report.REPORT_TYPES_CHOICES,
    }

    return render(request, 'frontend/reporting/list_reports.html', context)


@login_required
def add_task(request, report_id):
    report = get_object_or_404(Report, pk=report_id, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.report = report
            task.user = request.user
            task.save()
            return render(request, 'frontend/reporting/partials/task-item.html', {'task': task})
        else:
            return HttpResponse('')
    else:
        form = TaskForm()
        return HttpResponse('')


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    task.delete()
    return HttpResponse('')

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return render(request, 'frontend/reporting/partials/task-item.html', {'task': task})
        else:
            return HttpResponse('')

    else:
        form = TaskForm(instance=task)
        return HttpResponse('')

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    task.is_completed = not task.is_completed
    task.save()
    return HttpResponse('')


@login_required
def period_form(request):
    send = False
    period = request.GET.get('type')
    if period == Report.RH:
        send = True
    return render(request, 'frontend/reporting/partials/period_form.html', {'send': send})


@login_required
def mark_report(request, report_id):
    report = get_object_or_404(Report, pk=report_id, user=request.user)
    if request.method == 'POST':
        form = MarkReportForm(request.POST)
        if form.is_valid():
            report.responsible_comments = form.cleaned_data['responsible_comments']
            report.marks = form.cleaned_data['marks']
            report.save()
            messages.success(request, _("La note a ete attribuee avec succes !"))
            return redirect('reporting:list_reports')
        else:
           messages.error(request, _("Veuillez remplir tous les champs !"))
    else:
        form = MarkReportForm()

    context = {
        'form': form,
    }




