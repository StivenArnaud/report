import requests
from datetime import datetime
from django.utils import timezone
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.forms import PasswordChangeForm

# Create your views here.
from authentication.models import User, Profile
from authentication.forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm
from pointing.models import Presence, PrecenceItem
from reporting.models import Report

def login_view(request):
    msg = _("")
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password'])
            if user:
                login(request, user)

                messages.success(request, _(f"Salut {user.get_full_name()} ! Nous sommes content de vous revoir"))
                url = request.META.get('HTTP_REFERER')
                try:
                    query = requests.utils.urlparse(url).query
                    params = dict(x.split('=') for x in query.split('&'))
                    if 'next' in params:
                        next_page = params['next']
                        return redirect(next_page)
                except:
                    return redirect('reporting:list_reports')
            else:
                msg = _("Adresse e-mail ou mot de passe incorrect!")
        else:
            msg = _("Veillez renseigner correctement tous les champs !!")

    else:
        form = LoginForm()

    context = {
        'form': form,
        'message': msg,
    }

    return render(request, 'frontend/authentication/login.html', context)



def user_register(request):
    message = _("")
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                phone=form.cleaned_data['phone'],
                email=form.cleaned_data['email'],
                username=form.cleaned_data['email'],
                password=form.cleaned_data['phone'],
                role=form.cleaned_data['role'],
                company=request.user.company,
                identifier=form.cleaned_data['identifier'],
            )
            user.username = user.email
            user.set_password(form.cleaned_data['phone'])
            user.save()
            messages.success(request, _(f"Salut {user.get_full_name()} ! Votre compte a été créé avec succès."))

            return redirect('authentication:list_users')
            #return render(request, 'frontend/authentication/partials/add_user.html', {'single_user': user})
        else:
            messages.error(request, _("Veillez renseigner correctement tous les champs !!"))
            #print(form.errors)
            #return HttpResponse('')
            return redirect('authentication:list_users')
    else:
        form = RegisterForm()

        #return HttpResponse('')
        return redirect('authentication:list_users')




@login_required
def list_users(request):
    all_users = []
    users = []
    if request.user.role == User.EMPLOYEE:
        return redirect('reporting:list_reports')

    if request.user.role == User.RH or request.user.role == User.ADMIN:
        users = User.objects.select_related('responsible').all()

    if request.user.role == User.RESPONSIBLE:
        users = User.objects.select_related('responsible').filter(responsible=request.user)

    responsible_users = User.objects.filter(role__in=[User.RESPONSIBLE, User.RH, User.ADMIN])

    paginator = Paginator(users, 10)
    page = request.GET.get('page')

    try:
        all_users = paginator.page(page)
    except PageNotAnInteger:
        all_users = paginator.page(1)
    except EmptyPage:
        all_users = paginator.page(paginator.num_pages)

    context = {
        'all_users': all_users,
        'employee_count': users.filter(role=User.EMPLOYEE).count(),
        'rh_count': users.filter(role=User.RH).count(),
        'responsible_count': users.filter(role=User.RESPONSIBLE).count(),
        'responsible_users': responsible_users,
    }

    return render(request, 'frontend/authentication/list_users.html', context)



@login_required
def user_detail(request, user_id):
    try:
        single_user = User.objects.select_related('company', 'responsible').get(pk=user_id,
                                                                                company=request.user.company)
    except:
        raise Http404('User does not exist')

    if 'HX-Request' in request.headers:
        calendar_date = request.GET.get('date')

        report = None
        presence_items = []
        date_aware = None
        if calendar_date:
            date_naive = datetime.strptime(calendar_date, "%Y-%m-%d")
            date_aware = timezone.make_aware(date_naive)
            presence_items = PrecenceItem.objects.filter(date=date_aware, user=single_user)
            try:
                report = Report.objects.filter(user=single_user, published=True, created__date=date_aware).first()
            except:
                pass
        context = {
            'report': report,
            'presence_items': presence_items,
            'calendar_date': date_aware,
            'single_user': single_user,
        }

        return render(request, 'frontend/authentication/partials/summary_user.html', context)

    try:
        presences = Presence.objects.prefetch_related('items').filter(user=single_user)
    except:
        raise Http404('User does not exist')

    context = {
        'single_user': single_user,
        'presences': presences,
    }

    return render(request, 'frontend/authentication/user_detail.html', context)




@login_required
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/')


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("Mot de passe modifie avec succes !"))
            return redirect('authentication:list_users')
        else:
            messages.error(request, _("Veuillez remplir tous les champs !"))
    else:
        form = PasswordChangeForm(request.user)

    context = {
        'form': form,
    }

    return render(request, 'frontend/authentication/change_password.html', context)


@login_required
def user_settings(request):
    try:
        old_profile = Profile.objects.get(user=request.user, company=request.user.company)
    except:
        old_profile = None

    if request.method == 'POST':
        form = UpdateUserForm(request.POST, request.FILES, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=old_profile or None)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.company = user.company
            profile.save()

            messages.success(request, _("Vos informations ont ete modifie avec succes !"))
            return redirect('reporting:list_reports')
        else:
            messages.error(request, _("Veuillez remplir tous les champs !"))
    else:
        form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=old_profile or None)

    context = {
        'form': form,
        'profile_form': profile_form,
    }

    return render(request, 'frontend/authentication/user_settings.html', context)

@login_required
def profile_view(request, user_id):
    try:
        user = User.objects.get(pk=user_id, company=request.user.company)
        profile = Profile.objects.get(user=user, company=request.user.company)
    except:
        profile = None

    context = {
        'single_user': user,
        'profile': profile,
    }

    return render(request, 'frontend/authentication/profile.html', context)
