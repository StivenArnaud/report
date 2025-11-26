import calendar
from datetime import datetime, timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.translation import gettext_lazy as _
from datetime import datetime
from django.http import HttpResponse, JsonResponse, Http404
from django.db.models import Q
from django.utils import timezone
from openpyxl.styles.builtins import total

# Create your views here.
from authentication.models import User
from reporting.models import Report, Task
from reporting.forms import ReportForm, TaskForm, EditReportForm, MarkReportForm, EditTaskForm



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
    temps_restant = report.temps_restant_jour()

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
    try:
        report = Report.objects.select_related('marks_user', 'admin_marks_user').get(id=report_id)
        tasks = report.tasks.all()
    except:
        raise Http404('Rapport inexistant')

    context = {
        'report': report,
        'tasks': tasks,
    }

    return render(request, 'frontend/reporting/detail_report.html', context)


@login_required
def list_reports(request):
    reports = []
    report_type = request.GET.getlist('report_type')
    draft = request.GET.get('draft')

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

    if draft:
        reports = reports.filter(published=False, user=request.user)

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
def delete_report(request, report_id):
    report = get_object_or_404(Report, pk=report_id, user=request.user)
    report.delete()
    return HttpResponse('')

@login_required
def publish_report(request, report_id):
    report = get_object_or_404(Report, pk=report_id, user=request.user)
    report.published = True
    report.save()
    return render(request, 'frontend/reporting/partials/report_card_item.html', {'report': report})


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
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        form = EditTaskForm(request.POST)
        if form.is_valid():
            task.title = request.POST.get('title_edit')
            task.user = request.user
            task.save()
            return render(request, 'frontend/reporting/partials/task-item.html', {'task': task})
        else:
            return HttpResponse('')

    else:
        return render(request, 'frontend/reporting/partials/task-form.html', {'task': task})

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
    report = get_object_or_404(Report, pk=report_id)

    if request.user.role == User.EMPLOYEE:
        return redirect('reporting:detail_report', report_id=report_id)

    if request.method == 'POST':
        form = MarkReportForm(request.POST)
        if form.is_valid():
            if request.user.role == User.RESPONSIBLE or request.user.role == User.RH:
                report.responsible_comments = form.cleaned_data['responsible_comments']
                report.marks = form.cleaned_data['marks']
                report.marks_user = request.user
                report.save()
                messages.success(request, _("La note a ete attribuee avec succes !"))

            elif request.user.role == User.ADMIN:
                report.admin_comments = form.cleaned_data['responsible_comments']
                report.admin_marks = form.cleaned_data['marks']
                report.admin_marks_user = request.user
                report.save()
                messages.success(request, _("La note a ete attribuee avec succes !"))

            else:
                messages.error(request, _("Vous n'avez pas le droit d'attribuer une note !"))

            return redirect('reporting:list_reports')
        else:
           messages.error(request, _("Veuillez remplir tous les champs !"))
    else:
        form = MarkReportForm()

    context = {
        'form': form,
    }


@login_required
def get_reports_calendar_data(request, user_id):
    """Endpoint pour récupérer les données des rapports pour le calendrier"""
    now = timezone.now()

    user = get_object_or_404(User, id=user_id)

    # Récupération sécurisée des paramètres
    year_str = request.GET.get('year')
    month_str = request.GET.get('month')

    try:
        year = int(year_str) if year_str else now.year
    except ValueError:
        year = now.year

    try:
        month = int(month_str) if month_str else now.month
    except ValueError:
        month = now.month

    # Validation des bornes du mois
    if not (1 <= month <= 12):
        month = now.month

    # Début du mois
    start_date = datetime(year, month, 1)

    # Fin du mois (dernier jour inclus)
    _, last_day = calendar.monthrange(year, month)
    end_date = datetime(year, month, last_day, 23, 59, 59)

    # Rendre les dates timezone-aware
    start_date = timezone.make_aware(start_date, timezone.get_current_timezone())
    end_date = timezone.make_aware(end_date, timezone.get_current_timezone())

    # Récupérer les rapports du mois
    reports = Report.objects.filter(
        created__gte=start_date,
        created__lt=end_date,
        user=user,
        published=True,
    ).select_related('user')

    # Structurer les données par date
    calendar_data = {}
    for report in reports:
        date_key = report.created.strftime('%Y-%m-%d')
        if date_key not in calendar_data:
            calendar_data[date_key] = {
                'RQ': 0, 'RH': 0, 'JRA': 0, 'QUIZ': 0, 'total': 0
            }

        calendar_data[date_key][report.type] += 1
        calendar_data[date_key]['total'] += 1

    return JsonResponse(calendar_data)


@login_required
def monitoring_report(request):
    return render(request, 'frontend/reporting/monitoring_report.html')


def get_week_days(start_date):
    """Retourne les dates du lundi au dimanche à partir d'un lundi donné."""
    return [start_date + timedelta(days=i) for i in range(7)]


@login_required
def weekly_daily_reports(request):
    """
    Retourne les rapports quotidiens pour une semaine donnée,
    envoyée par HTMX via week_start (YYYY-MM-DD).
    """
    # 1) Récupérer la date envoyée par HTMX
    week_start_str = request.GET.get("week_start")
    total_reports = 0
    published_reports = 0
    not_published_reports = 0

    if week_start_str:
        try:
            week_start = datetime.strptime(week_start_str, "%Y-%m-%d").date()
        except ValueError:
            week_start = timezone.localdate()
    else:
        # Semaine courante
        today = timezone.localdate()
        week_start = today - timedelta(days=today.weekday())  # lundi

    # 2) Construire la liste des jours de la semaine (lundi → dimanche)
    week_days = get_week_days(week_start)

    # 3) Charger tous les utilisateurs actifs
    users = User.objects.filter(is_active=True).order_by("last_name", "first_name")

    # 4) Précharger tous les rapports quotidiens (type = RQ) de la semaine
    reports = Report.objects.filter(
        type=Report.RQ,
        created__date__in=week_days
    ).select_related("user")

    # 5) Créer un dictionnaire pour accéder rapidement aux rapports par utilisateur et par jour
    # report_map = {user_id: {date: report}}
    report_map = {}
    for r in reports:
        report_map.setdefault(r.user_id, {})
        # Utilisation de r.created.date() pour ne garder que la date
        report_map[r.user_id][r.created.date()] = r

    # 6) Construire la structure people_data pour le template
    people_data = []
    for user in users:
        person = {
            "name": f"{user.last_name} {user.first_name}",
            "inserted": True,  # actif
            "days": []
        }

        for day in week_days:
            rep = report_map.get(user.id, {}).get(day)
            total_reports += 1
            published_reports += 1 if rep else 0
            not_published_reports += 1 if not rep else 0

            person["days"].append({
                "transmitted": rep.published if rep else False
            })

        people_data.append(person)

    # 7) Retour HTMX : template partiel avec le tableau
    if 'HX-Request' in request.headers:
        return render(request, 'frontend/reporting/partials/people_table.html', {
            'people_data': people_data,
            'week_start': week_start,
            'week_days': week_days,
            'percent_published': published_reports / total_reports * 100 if total_reports else 0,
            'percent_not_published': not_published_reports / total_reports * 100 if total_reports else 0,
        })

    # 8) Fallback JSON pour test si non-HTMX
    return JsonResponse({"week_start": str(week_start)})




